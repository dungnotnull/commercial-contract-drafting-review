# -*- coding: utf-8 -*-
"""knowledge_updater.py — self-improving crawl pipeline for Skill #142
(Commercial Contract Drafting & Legal Review Automation, cluster: legal-compliance).

Pattern (per CLAUDE.md):
  1. Fetch latest pages/standards from configured domain sources via crawl4ai or HTTP fallback
  2. Parse — extract title, authors, date, URL, abstract/key finding
  3. Score — rank by recency + domain-keyword relevance
  4. Append — add scored entries to SECOND-KNOWLEDGE-BRAIN.md (date-stamped)
  5. Deduplicate — skip entries already present (URL/DOI hash)

Recommended schedule: weekly cron.
Graceful degradation: if crawl4ai / network is unavailable, log and exit 0
so the skill keeps working off the existing knowledge base.
"""
from __future__ import annotations

import argparse
import datetime
import hashlib
import html
import logging
import os
import re
import sys
from dataclasses import dataclass, field
from typing import Iterable, List, Optional

# Default configuration. Override via CLI or set environment variables.
DEFAULT_WEB_SOURCES: List[str] = [
    "https://www.unidroit.org",
    "https://uncitral.un.org",
    "https://www.law.cornell.edu/ucc",
    "https://www.americanbar.org",
]

DEFAULT_SEARCH_QUERIES: List[str] = [
    "commercial contract risk clause trends",
    "limitation of liability enforceability case",
    "force majeure drafting post pandemic",
    "SaaS agreement data protection clauses",
]

ARXIV_CATEGORIES: List[str] = []  # Domain relies on standards bodies, not preprints.

RELEVANCE_KEYWORDS: List[str] = [
    "contract", "clause", "indemnity", "liability", "limitation", "warranty",
    "force majeure", "termination", "dispute resolution", "governing law",
    "CISG", "UNIDROIT", "UCC", "SaaS", "data protection", "commercial",
    "risk allocation", "boilerplate", "plain language", "enforceability",
]

TIMEOUT_SECONDS = 30
_logger = logging.getLogger("knowledge_updater")


@dataclass
class Entry:
    """A single knowledge-base entry."""
    title: str
    authors: str
    year: str
    venue: str
    url: str
    abstract: str
    source_type: str = "web"
    relevance: float = 0.0
    hash_: str = field(default="", init=False)

    def __post_init__(self):
        self.hash_ = _hash(self.url)


def _hash(value: str) -> str:
    """Return a short, deterministic SHA-256 hash of the URL/DOI."""
    return hashlib.sha256((value or "").encode("utf-8")).hexdigest()[:16]


def _existing_hashes(text: str) -> set:
    """Collect hashes already embedded in the knowledge brain."""
    return set(re.findall(r"<!--hash:([0-9a-f]{16})-->", text))


def relevance_score(title: str, abstract: str) -> float:
    """Return a 0–1 relevance score based on keyword overlap."""
    blob = f"{title} {abstract}".lower()
    hits = sum(1 for kw in RELEVANCE_KEYWORDS if kw.lower() in blob)
    return round(hits / max(1, len(RELEVANCE_KEYWORDS)), 3)


def _extract_title(markdown: str, default: str) -> str:
    """Try to pull an H1/H2 title from markdown or HTML."""
    for pattern in (r"^#\s+(.+?)$", r"^##\s+(.+?)$", r"<title>([^<]+)</title>"):
        m = re.search(pattern, markdown, re.MULTILINE | re.IGNORECASE)
        if m:
            return m.group(1).strip()[:200]
    return default


def _extract_year(markdown: str) -> str:
    """Find the most recent four-digit year in the text."""
    years = re.findall(r"\b(19\d{2}|20\d{2})\b", markdown)
    if years:
        return max(years)
    return str(datetime.date.today().year)


def _truncate(text: str, length: int = 600) -> str:
    text = text.replace("\n", " ").strip()
    if len(text) <= length:
        return text
    return text[:length].rsplit(" ", 1)[0] + "…"


def _strip_html(raw_html: str) -> str:
    """Convert HTML to plain text using BeautifulSoup if available, otherwise regex."""
    try:
        from bs4 import BeautifulSoup  # type: ignore
        soup = BeautifulSoup(raw_html, "html.parser")
        for elem in soup(["script", "style", "nav", "footer", "header"]):
            elem.decompose()
        return soup.get_text(separator="\n", strip=True)
    except Exception:
        # Regex fallback: remove tags and decode entities.
        text = re.sub(r"<[^>]+?>", "", raw_html)
        return html.unescape(text)


class _SimpleRequestsFetcher:
    """HTTP-only fallback that mimics the crawl4ai result interface."""

    def __init__(self, get_fn=None):
        self._get_fn = get_fn

    def warmup(self) -> None:
        pass

    def run(self, url: str):
        if self._get_fn is not None:
            resp = self._get_fn(url, timeout=TIMEOUT_SECONDS, headers={"User-Agent": "knowledge-updater/1.0"})
        else:
            import requests  # type: ignore
            resp = requests.get(url, timeout=TIMEOUT_SECONDS, headers={"User-Agent": "knowledge-updater/1.0"})
        resp.raise_for_status()
        text = _strip_html(resp.text)
        class Result:
            pass
        r = Result()
        r.markdown = text
        return r


def _create_crawler() -> Optional[object]:
    """Return a warmed-up crawler if available; otherwise a requests-based fetcher."""
    try:
        from crawl4ai import WebCrawler  # type: ignore
        crawler = WebCrawler()
        crawler.warmup()
        return crawler
    except Exception as exc:
        _logger.debug("crawl4ai WebCrawler unavailable (%s); trying fallback fetcher.", exc)

    try:
        import requests  # type: ignore
        fetcher = _SimpleRequestsFetcher()
        fetcher.warmup()
        _logger.info("Using requests-based fallback fetcher (crawl4ai not available).")
        return fetcher
    except Exception as exc:
        _logger.info("HTTP fallback unavailable (%s); skipping live crawl.", exc)
        return None


def fetch_web_entries(sources: Iterable[str], crawler: Optional[object] = None) -> List[Entry]:
    """Fetch each configured web source and convert it into a knowledge entry."""
    entries: List[Entry] = []
    if crawler is None:
        crawler = _create_crawler()
    if crawler is None:
        return entries

    for src in sources:
        try:
            result = crawler.run(url=src)
            markdown = getattr(result, "markdown", "") or ""
            if not markdown.strip():
                continue
            title = _extract_title(markdown, f"Update scan: {src}")
            year = _extract_year(markdown)
            entries.append(Entry(
                title=title,
                authors="—",
                year=year,
                venue=src,
                url=src,
                abstract=_truncate(markdown),
                source_type="web",
            ))
        except Exception as exc:
            _logger.warning("Failed to fetch %s: %s", src, exc)
    return entries


def fetch_search_entries(queries: Iterable[str], search_provider: Optional[object] = None) -> List[Entry]:
    """Fetch search results for each query if a search provider is wired.

    By default no provider is implemented to avoid requiring an API key.
    Production deployments can pass an object implementing `search(query)`
    returning a list of dicts with keys: title, url, snippet.
    """
    entries: List[Entry] = []
    if search_provider is None or not hasattr(search_provider, "search"):
        return entries

    for query in queries:
        try:
            for item in search_provider.search(query):
                if not item.get("url"):
                    continue
                entries.append(Entry(
                    title=item.get("title", query)[:200],
                    authors="—",
                    year=str(datetime.date.today().year),
                    venue="web-search",
                    url=item["url"],
                    abstract=_truncate(item.get("snippet", "")),
                    source_type="search",
                ))
        except Exception as exc:
            _logger.warning("Search provider failed for query %r: %s", query, exc)
    return entries


def score_entries(entries: Iterable[Entry]) -> List[Entry]:
    """Attach relevance scores and sort descending."""
    scored = []
    for e in entries:
        e.relevance = relevance_score(e.title, e.abstract)
        if e.relevance <= 0.0:
            continue
        scored.append(e)
    scored.sort(key=lambda e: e.relevance, reverse=True)
    return scored


def format_entry(entry: Entry, date: str) -> str:
    """Format a single entry for appending to SECOND-KNOWLEDGE-BRAIN.md."""
    return (
        f"- {date} — **{entry.title}** ({entry.venue}, {entry.year}) "
        f"[{entry.url}] relevance={entry.relevance:.3f} <!--hash:{entry.hash_}-->\n"
        f"  - *Key finding:* {entry.abstract}"
    )


def append_entries(entries: List[Entry], brain_path: str, dry_run: bool = False) -> int:
    """Append scored entries to the knowledge brain, skipping duplicates.

    Returns the number of entries appended.
    """
    if not os.path.exists(brain_path):
        _logger.error("Knowledge brain not found: %s", brain_path)
        return 0

    with open(brain_path, "r", encoding="utf-8") as f:
        text = f.read()

    seen = _existing_hashes(text)
    today = datetime.date.today().isoformat()
    added = 0
    lines: List[str] = []

    for entry in entries:
        if entry.hash_ in seen or not entry.url:
            continue
        lines.append(format_entry(entry, today))
        seen.add(entry.hash_)
        added += 1

    if added == 0:
        _logger.info("No new entries to append (network/dedup/relevance).")
        return 0

    if dry_run:
        _logger.info("DRY-RUN: would append %d entries.", added)
        for line in lines:
            _logger.info(line)
        return added

    section = f"\n### Auto-crawl {today}\n\n" + "\n\n".join(lines) + "\n"
    with open(brain_path, "a", encoding="utf-8") as f:
        f.write(section)
    _logger.info("Appended %d new entries to %s", added, brain_path)
    return added


def update_brain(
    brain_path: str,
    sources: Optional[List[str]] = None,
    queries: Optional[List[str]] = None,
    dry_run: bool = False,
    search_provider: Optional[object] = None,
) -> int:
    """Run the full update pipeline and return the number of appended entries."""
    sources = list(sources or DEFAULT_WEB_SOURCES)
    queries = list(queries or DEFAULT_SEARCH_QUERIES)

    crawler = _create_crawler()
    entries: List[Entry] = []

    if crawler is not None:
        entries.extend(fetch_web_entries(sources, crawler))
        entries.extend(fetch_search_entries(queries, search_provider))
    else:
        _logger.info("No crawler available; skipping fetch.")

    scored = score_entries(entries)
    return append_entries(scored, brain_path, dry_run=dry_run)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Update the SECOND-KNOWLEDGE-BRAIN.md knowledge base for Skill #142.",
    )
    parser.add_argument(
        "--brain",
        default=os.path.join(os.path.dirname(__file__), "..", "SECOND-KNOWLEDGE-BRAIN.md"),
        help="Path to SECOND-KNOWLEDGE-BRAIN.md (default: ../SECOND-KNOWLEDGE-BRAIN.md)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Fetch and score but do not write to the knowledge brain.",
    )
    parser.add_argument(
        "--source",
        action="append",
        dest="sources",
        help="Add a web source URL (repeatable).",
    )
    parser.add_argument(
        "--query",
        action="append",
        dest="queries",
        help="Add a search query (repeatable).",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable DEBUG logging.",
    )
    return parser


def main(argv: Optional[List[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    brain_path = os.path.abspath(args.brain)
    _logger.info("Running knowledge updater for skill #142 (commercial-contract-drafting-review)")
    _logger.info("Knowledge brain: %s", brain_path)

    try:
        update_brain(
            brain_path=brain_path,
            sources=args.sources,
            queries=args.queries,
            dry_run=args.dry_run,
        )
    except Exception as exc:
        _logger.error("Pipeline failed: %s", exc, exc_info=args.verbose)
        # Graceful degradation: keep skill working with existing brain.
        return 0

    return 0


if __name__ == "__main__":
    sys.exit(main())
