# CLAUDE.md — Commercial Contract Drafting & Legal Review Automation (Skill #142)

**Slug:** `commercial-contract-drafting-review`  •  **Cluster:** `legal-compliance`  •  **Source idea:** 142  •  **Phase:** Built (v1, production-ready)

## Tagline
Automates commercial-contract drafting and review, flagging risk clauses against current law and precedent (informational, not legal advice).

## Problem This Skill Solves
Businesses sign commercial contracts without spotting one-sided indemnities, ambiguous terms, or missing protections, creating dispute risk. This skill provides a structured drafting/review with risk flags.

## Harness Flow Summary
1. **Intake** (`sub-intake`) — gather structured inputs, scope, goals, jurisdiction, and offline-mode preference.
2. **Framework selection** (`sub-framework-selector`) — choose named world-renowned framework(s) and justify.
3. **Research** (`WebSearch`/`WebFetch` + `SECOND-KNOWLEDGE-BRAIN.md`) — gather highest-tier evidence; degrade gracefully offline.
4. **Scoring** (`sub-scoring-engine`) — multi-dimensional weighted scores with citations and certainty grades.
5. **Challenge** — devil’s-advocate review of assumptions and weak evidence.
6. **Roadmap** (`sub-improvement-roadmap`) — prioritized effort/impact recommendations.
7. **Compliance check** (`sub-compliance-check`) — MANDATORY before final output.
8. **Synthesize** — assemble the professional deliverable; pass Quality Gates.

## Gates
- **Compliance gate:** `sub-compliance-check` MUST run before the final deliverable, attaching required disclaimers.
- **Evidence gate:** every score must cite a source or chosen framework.
- **Roadmap traceability gate:** every recommendation must link to a scored finding.

## Sub-skills
- `skills/sub-compliance-check.md` — Compliance Check: Verify outputs against applicable regulations/standards and attach the required informational/non-advice disclaimers before final delivery.
- `skills/sub-intake.md` — Intake & Context Gathering: Collect the structured inputs, scope, and goals needed to run the analysis; ask clarifying questions when key facts are missing.
- `skills/sub-framework-selector.md` — Evaluation Framework Selector: Pick the most appropriate named world-renowned framework(s) for the case and justify the choice.
- `skills/sub-scoring-engine.md` — Scoring Engine: Apply the multi-dimensional rubric to produce weighted scores with evidence citations for each dimension.
- `skills/sub-improvement-roadmap.md` — Improvement Roadmap: Generate a prioritized, effort/impact-ranked set of recommendations traceable to the scored findings.
- `skills/main.md` — Main harness: orchestrates the sub-skills in order, runs challenge and synthesis, enforces gates.

## Tools Required
- `WebSearch`, `WebFetch` — live evidence and standards updates
- `Read`, `Write` — load knowledge base, emit deliverables
- `Bash` — run `tools/knowledge_updater.py`
- Skill tool — invoke sub-skills in sequence

## Knowledge Sources
- Authoritative domain sources:
  - https://www.unidroit.org/instruments/commercial-contracts/unidroit-principles-2016
  - https://uncitral.un.org/en/texts/salegoods/conventions/cisg
  - https://www.law.cornell.edu/ucc/2
  - https://www.americanbar.org/groups/business_law/
  - https://www.americanbar.org/groups/public_contract_law/
  - https://www.ali.org/publications/show/restatement-second-contracts/
- Crawl queries:
  - `commercial contract risk clause trends`
  - `limitation of liability enforceability case`
  - `force majeure drafting post pandemic`
  - `SaaS agreement data protection clauses`

## Supporting Tools
- `tools/knowledge_updater.py` — crawl4ai pipeline that grows `SECOND-KNOWLEDGE-BRAIN.md` (weekly cron recommended).
- `tools/requirements.txt` — runtime dependencies for the updater.
- `tests/test_knowledge_updater.py` — unit tests for deduplication, scoring, and formatting.

## Cross-Skill Cluster Wiring (legal-compliance)
This skill is designed to be reused by sibling skills in the `legal-compliance` cluster:
- **Sub-skills are composable.** Any parent skill may invoke `sub-intake`, `sub-framework-selector`, `sub-scoring-engine`, `sub-improvement-roadmap`, or `sub-compliance-check` by name and pass a case context object.
- **Shared knowledge base.** `SECOND-KNOWLEDGE-BRAIN.md` is a common reference for contract-law frameworks; sibling skills can `Read` it directly.
- **Shared compliance gate.** `sub-compliance-check` enforces the cluster-wide informational-only policy and can be imported into other legal-compliance harnesses.
- **Shared tool runner.** `tools/knowledge_updater.py` accepts `--brain` and `--source`/`--query` overrides so other skills can reuse the same crawl pipeline with their own brain files.

## Active Development Tasks
- [x] Scaffold full deliverable set
- [x] Define 5 sub-skills
- [x] Expand SECOND-KNOWLEDGE-BRAIN.md with real, citable sources
- [x] Add regression cases and unit tests for `knowledge_updater.py`
- [x] Complete Phase 5 cluster integration and cross-references

## Related Root Docs
- `PROJECT-detail.md` — full technical spec
- `PROJECT-DEVELOPMENT-PHASE-TRACKING.md` — phase roadmap (100% complete)
- `SECOND-KNOWLEDGE-BRAIN.md` — self-improving knowledge base
