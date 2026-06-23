# Commercial Contract Drafting & Legal Review Automation

[![Skill Cluster](https://img.shields.io/badge/cluster-legal--compliance-blue)](https://github.com/dungnotnull/commercial-contract-drafting-review)
[![Status](https://img.shields.io/badge/status-production--ready-brightgreen)](./PROJECT-DEVELOPMENT-PHASE-TRACKING.md)
[![Tests](https://img.shields.io/badge/tests-10%20passing-success)](./tests/test_knowledge_updater.py)
[![License](https://img.shields.io/badge/license-MIT-lightgrey)](./LICENSE)

> **A production-grade Claude skill for automated commercial-contract drafting and legal review.**
> It flags risk clauses against current law and precedent, scores contracts across five dimensions, and returns a prioritized improvement roadmap.
>
> **Always informational — never legal advice.**

---

## Table of Contents

- [Overview](#overview)
- [Why This Exists](#why-this-exists)
- [Key Capabilities](#key-capabilities)
- [Architecture](#architecture)
- [Sub-Skills](#sub-skills)
- [Scoring Model](#scoring-model)
- [Knowledge Base](#knowledge-base)
- [Installation](#installation)
- [Usage](#usage)
- [Testing](#testing)
- [Roadmap](#roadmap)
- [Safety & Compliance](#safety--compliance)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)

---

## Overview

This repository implements **Skill #142** in the `legal-compliance` cluster: a full Claude harness that runs a research-first, framework-grounded workflow for commercial-contract analysis.

It is designed for:

- **Practitioners** reviewing supplier, SaaS, licensing, or services agreements.
- **Founders and operators** drafting NDAs, partnership terms, or vendor contracts.
- **Compliance teams** who need a structured, evidence-based risk screen before legal sign-off.

The skill does **not** replace an attorney. It replaces guesswork with a transparent, cite-heavy, auditable workflow.

---

## Why This Exists

Businesses sign commercial contracts every day without spotting:

- One-sided indemnities and uncapped liability.
- Ambiguous defined terms or missing schedules.
- Unenforceable governing-law or dispute-resolution clauses.
- Asymmetric termination, assignment, or force-majeure provisions.

The result is hidden dispute risk, surprise exposure, and expensive renegotiation. This skill provides a structured drafting/review process that names the frameworks it uses, scores every finding, and produces a traceable improvement plan.

---

## Key Capabilities

| Capability | What it does |
|---|---|
| **Intake & Scoping** | Asks only the questions that are missing; supports review, drafting, redline, compare, one-sided-check, and enforceability-check modes. |
| **Framework Selection** | Chooses from UCC Article 2, CISG, UNIDROIT Principles 2016, Restatement (Second) of Contracts, risk-allocation analysis, plain-language drafting, and boilerplate review. |
| **Research** | Uses live `WebSearch`/`WebFetch`; falls back to a curated `SECOND-KNOWLEDGE-BRAIN.md` when offline. |
| **Multi-Dimensional Scoring** | Scores 5 weighted dimensions 0–100 with cited evidence and certainty grades. |
| **Devil’s Advocate Challenge** | Stress-tests assumptions and downgrades conclusions when evidence is weak. |
| **Prioritized Roadmap** | Ranks recommendations by impact-to-effort ratio, every item traceable to a scored finding. |
| **Mandatory Compliance Gate** | Attaches informational disclaimers, attorney recommendations, and blocks output if safety checks fail. |
| **Self-Improving Knowledge** | Weekly `knowledge_updater.py` pipeline crawls authoritative sources, deduplicates, and appends dated entries. |

---

## Architecture

```text
/commercial-contract-drafting-review (skills/main.md)
   ├── sub-intake .................... gather inputs, scope, goals, jurisdiction
   ├── sub-framework-selector ........ choose world-renowned framework(s)
   ├── [research] WebSearch/WebFetch + SECOND-KNOWLEDGE-BRAIN
   ├── sub-scoring-engine ............ multi-dimensional weighted scoring
   ├── [challenge] devil's-advocate assumption review
   ├── sub-improvement-roadmap ....... prioritized effort/impact actions
   ├── [GATE] sub-compliance-check ... BLOCKING before final delivery
   └── synthesize .................... professional report + quality gates
```

### Evidence Hierarchy

1. Primary statute/treaty/principle text (UCC, CISG, UNIDROIT Principles).
2. Authoritative commentary or bar association guidance.
3. Peer-reviewed legal scholarship or practitioner treatise.
4. High-quality practitioner summary.
5. Internal knowledge base (`SECOND-KNOWLEDGE-BRAIN.md`).

---

## Sub-Skills

| File | Role |
|---|---|
| [`skills/main.md`](./skills/main.md) | Orchestrates the full harness, enforces gates, synthesizes deliverables. |
| [`skills/sub-intake.md`](./skills/sub-intake.md) | Structured intake with JSON output and clarifying-question logic. |
| [`skills/sub-framework-selector.md`](./skills/sub-framework-selector.md) | Picks and justifies the analytical framework(s). |
| [`skills/sub-scoring-engine.md`](./skills/sub-scoring-engine.md) | Applies the 5-dimension rubric with citations and certainty grades. |
| [`skills/sub-improvement-roadmap.md`](./skills/sub-improvement-roadmap.md) | Ranks recommendations by impact ÷ effort. |
| [`skills/sub-compliance-check.md`](./skills/sub-compliance-check.md) | Final safety gate; attaches disclaimers; blocks if checks fail. |

---

## Scoring Model

| Dimension | Weight | What is assessed |
|---|---|---|
| **Risk allocation** | 25% | Indemnity, liability caps, warranties, IP indemnity, insurance. |
| **Legal compliance & enforceability** | 25% | Governing law, regulatory alignment, unenforceable terms, public policy limits. |
| **Clarity & completeness** | 20% | Defined terms, ambiguity, gaps, plain-language drafting. |
| **Commercial fairness / balance** | 15% | One-sidedness, mutuality, leverage, unconscionability risk. |
| **Dispute & exit provisions** | 15% | Termination, dispute resolution, remedies, force majeure, assignment. |

### Grade Mapping

| Overall Score | Grade |
|---|---|
| 90–100 | A |
| 75–89 | B |
| 60–74 | C |
| 0–59 | D |

Every dimension score must cite a source or framework before the deliverable can be released.

---

## Knowledge Base

The [`SECOND-KNOWLEDGE-BRAIN.md`](./SECOND-KNOWLEDGE-BRAIN.md) file is a self-improving domain knowledge base.

### Currently Seeded Sources

- **UCC Article 2** — Cornell Law School Legal Information Institute.
- **CISG** — UNCITRAL.
- **UNIDROIT Principles 2016** — UNIDROIT.
- **Restatement (Second) of Contracts** — American Law Institute.
- **A Manual of Style for Contract Drafting** — Kenneth A. Adams.
- **Contract Drafting: Powerful Prose in Transactional Practice** — Tina L. Stark.
- **The Law of Contracts and the Uniform Commercial Code** — Pamela Tepper.
- **Drafting and Analyzing Contracts** — Scott J. Burnham.
- **ABA Business Law Section** and **Public Contract Law Section**.

### Keeping It Current

```bash
# Dry run: see what would be appended without touching the brain
python tools/knowledge_updater.py --dry-run --verbose

# Production update
python tools/knowledge_updater.py --verbose

# Add a custom source or query
python tools/knowledge_updater.py --source https://example.com/contract-law --query "limitation of liability trends"
```

The updater supports `crawl4ai` and degrades gracefully to `requests` + `BeautifulSoup` if needed. It deduplicates by SHA-256 hash of the URL/DOI.

---

## Installation

```bash
# Clone the repository
git clone https://github.com/dungnotnull/commercial-contract-drafting-review.git
cd commercial-contract-drafting-review

# Install Python dependencies for the knowledge updater
pip install -r tools/requirements.txt
```

### Dependencies

- `crawl4ai>=0.3.0` (preferred crawler)
- `requests>=2.28.0` (HTTP fallback)
- `beautifulsoup4>=4.11.0` (HTML parsing)
- `lxml>=4.9.0` (optional faster parser)

---

## Usage

This skill is designed to be invoked through Claude’s skill harness, but the underlying files are human-readable and directly usable:

1. Open [`skills/main.md`](./skills/main.md).
2. Follow the 8-stage workflow.
3. For each stage, open the corresponding `sub-*.md` file for the exact input/output schema.
4. Use `SECOND-KNOWLEDGE-BRAIN.md` as the offline knowledge base.
5. Run the knowledge updater weekly to pull new sources.

### Example Scenarios

The [`tests/test-scenarios.md`](./tests/test-scenarios.md) file contains validated scenarios:

1. Risk review of a supplier contract.
2. Drafting a mutual NDA for startups.
3. Checking whether a liability clause is one-sided.
4. Compliance gate for “Is this contract legally binding?”
5. Degraded/offline review using only the local knowledge base.

---

## Testing

```bash
# Run all unit tests
python -m pytest tests/test_knowledge_updater.py -v
```

Current test coverage:

- Hash determinism and extraction of existing hashes.
- Relevance scoring.
- Web-entry extraction with title and year parsing.
- Score filtering for zero relevance.
- Append deduplication and dry-run safety.
- Graceful degradation when no crawler is available.
- HTML-to-text stripping.
- Requests fallback fetcher.

---

## Roadmap

Tracked in [`PROJECT-DEVELOPMENT-PHASE-TRACKING.md`](./PROJECT-DEVELOPMENT-PHASE-TRACKING.md).

| Phase | Status |
|---|---|
| 0 — Research & Skill Architecture | ✅ Complete |
| 1 — Core Sub-Skills | ✅ Complete |
| 2 — Main Harness + Quality Gates | ✅ Complete |
| 3 — SECOND-KNOWLEDGE-BRAIN Pipeline | ✅ Complete |
| 4 — Testing & Validation | ✅ Complete |
| 5 — Integration & Cross-Skill Wiring | ✅ Complete |

---

## Safety & Compliance

This skill operates under a strict **informational-only** policy:

- It does **not** provide legal, financial, tax, or regulatory advice.
- It does **not** guarantee outcomes or enforceability.
- It always recommends consulting a **licensed attorney** in the relevant jurisdiction.
- It refuses to facilitate unlawful, deceptive, or harmful terms.
- A **mandatory compliance gate** blocks final delivery if any safety check fails.

---

## Contributing

Contributions are welcome, especially in these areas:

- Additional authoritative sources in `SECOND-KNOWLEDGE-BRAIN.md`.
- New test scenarios for edge cases or jurisdictions.
- Improvements to `tools/knowledge_updater.py` (rate limiting, robots.txt respect, better search-provider integration).
- Translations or jurisdiction-specific compliance checklists.

Please keep all contributions aligned with the evidence hierarchy and the informational-only policy.

---

## License

MIT — see [`LICENSE`](./LICENSE).

---

## Acknowledgments

- Frameworks: UCC, CISG, UNIDROIT Principles, Restatement (Second) of Contracts.
- Authoritative sources: Cornell LII, UNCITRAL, UNIDROIT, ABA, ALI.
- Practitioner scholarship: Kenneth A. Adams, Tina L. Stark, Pamela Tepper, Scott J. Burnham.
- Built as a Claude skill in the `legal-compliance` cluster.
