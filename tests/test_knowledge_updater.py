# -*- coding: utf-8 -*-
"""Unit tests for tools/knowledge_updater.py.

Run with: python -m pytest tests/test_knowledge_updater.py
These tests avoid network calls and validate deduplication, hashing, relevance
scoring, and append formatting.
"""
from pathlib import Path
import sys

# Add tools directory to import path
sys.path.insert(0, str(Path(__file__).parent.parent / "tools"))

import knowledge_updater as ku


class FakeCrawler:
    """Crawl4ai-compatible fake that returns deterministic markdown."""
    def __init__(self, markdown_by_url):
        self.markdown_by_url = markdown_by_url
        self.calls = []

    def warmup(self):
        pass

    def run(self, url):
        self.calls.append(url)
        class Result:
            pass
        r = Result()
        r.markdown = self.markdown_by_url.get(url, "")
        return r


def test_hash_is_deterministic():
    h1 = ku._hash("https://example.com/a")
    h2 = ku._hash("https://example.com/a")
    assert h1 == h2
    assert len(h1) == 16


def test_existing_hashes_extracted():
    text = "foo <!--hash:abcdef0123456789--> bar <!--hash:0000000000000000-->"
    assert ku._existing_hashes(text) == {"abcdef0123456789", "0000000000000000"}


def test_relevance_score_increases_with_keywords():
    base = ku.relevance_score("Title", "Abstract")
    hit = ku.relevance_score("Contract drafting", "Indemnity liability clause")
    assert hit > base


def test_fetch_web_entries_returns_venue_and_year():
    crawler = FakeCrawler({
        "https://example.org/ucc": "# UCC Article 2\n\nSales of goods in 2021.",
    })
    entries = ku.fetch_web_entries(["https://example.org/ucc"], crawler)
    assert len(entries) == 1
    e = entries[0]
    assert e.title == "UCC Article 2"
    assert e.year == "2021"
    assert e.venue == "https://example.org/ucc"


def test_score_entries_filters_zero_relevance():
    entries = [
        ku.Entry(title="XYZ random page", authors="—", year="2025", venue="x", url="https://x", abstract="nothing relevant"),
        ku.Entry(title="Contract indemnity clause", authors="—", year="2025", venue="x", url="https://y", abstract="limitation of liability"),
    ]
    scored = ku.score_entries(entries)
    assert len(scored) == 1
    assert scored[0].title == "Contract indemnity clause"


def test_append_entries_dedups_by_hash(tmp_path):
    brain = tmp_path / "brain.md"
    brain.write_text("# Brain\n<!--hash:0000000000000000-->\n", encoding="utf-8")
    e1 = ku.Entry(title="Old", authors="—", year="2025", venue="v", url="https://old", abstract="...")
    e2 = ku.Entry(title="New", authors="—", year="2025", venue="v", url="https://new", abstract="contract indemnity")
    # Force known hashes for deterministic test
    e1.hash_ = "0000000000000000"
    e2.hash_ = "1111111111111111"
    added = ku.append_entries([e1, e2], str(brain))
    assert added == 1
    text = brain.read_text(encoding="utf-8")
    assert "New" in text
    assert "Old" not in text


def test_append_entries_dry_run_does_not_write(tmp_path):
    brain = tmp_path / "brain.md"
    brain.write_text("# Brain\n", encoding="utf-8")
    e = ku.Entry(title="New", authors="—", year="2025", venue="v", url="https://new", abstract="contract indemnity")
    added = ku.append_entries([e], str(brain), dry_run=True)
    assert added == 1
    assert brain.read_text(encoding="utf-8") == "# Brain\n"


def test_update_brain_without_crawler_does_nothing(tmp_path):
    brain = tmp_path / "brain.md"
    brain.write_text("# Brain\n", encoding="utf-8")
    # Monkeypatch the crawler factory to None
    original = ku._create_crawler
    ku._create_crawler = lambda: None
    try:
        result = ku.update_brain(str(brain), sources=[], queries=[])
        assert result == 0
    finally:
        ku._create_crawler = original

def test_strip_html_extracts_text():
    raw = "<html><head><title>Page</title></head><body><p>Contract indemnity clause.</p></body></html>"
    text = ku._strip_html(raw)
    assert "Contract indemnity clause." in text
    assert "<html>" not in text


def test_simple_requests_fetcher_extracts_title_and_body():
    html = "<html><head><title>UCC Article 2 Update</title></head><body>Changes to commercial contracts in 2024.</body></html>"

    class FakeResponse:
        text = html
        def raise_for_status(self):
            pass

    def fake_get(url, **kwargs):
        assert url == "https://example.com/ucc"
        return FakeResponse()

    fetcher = ku._SimpleRequestsFetcher(get_fn=fake_get)
    result = fetcher.run("https://example.com/ucc")
    assert "UCC Article 2 Update" in result.markdown
    assert "2024" in result.markdown
