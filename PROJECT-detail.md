# PROJECT-detail.md — Commercial Contract Drafting & Legal Review Automation (Skill #142)

## Executive Summary
Automates commercial-contract drafting and review, flagging risk clauses against current law and precedent (informational, not legal advice). This skill is a full Claude harness in the **legal-compliance** cluster. It runs a research-first, framework-grounded workflow that scores the subject against named world-renowned methodologies and returns a prioritized improvement roadmap, while continuously updating its knowledge base.

## Problem Statement
Businesses sign commercial contracts without spotting one-sided indemnities, ambiguous terms, or missing protections, creating dispute risk. This skill provides a structured drafting/review with risk flags.

## Target Users & Use Cases
Practitioners, reviewers, and decision-makers who need an expert-grade, evidence-based assessment in this domain. Trigger examples:
1. **Risk review** — User: "Review this supplier contract for risks" → COMPLIANCE/disclaimer first; skill redlines indemnity/liability/IP, scores risk, roadmap.
2. **Drafting** — User: "Draft a mutual NDA for two startups" → Skill drafts balanced NDA, flags choices needing legal sign-off.
3. **One-sided clause** — User: "Is this liability clause fair to me?" → Skill flags uncapped liability/one-sidedness, suggests balanced alternative.
4. **Compliance gate** — User: "Is this contract legally binding for sure?" → COMPLIANCE: states informational only, recommends licensed attorney for the jurisdiction.
5. **Degraded mode** — User: "Review offline" → Falls back to SECOND-KNOWLEDGE-BRAIN, signals it can't check latest statutes/precedent.

## Harness Architecture
```
/commercial-contract-drafting-review (main.md)
   ├── sub-intake .................... gather inputs & scope
   ├── sub-framework-selector ........ choose world-renowned framework(s)
   ├── [research] WebSearch/WebFetch + SECOND-KNOWLEDGE-BRAIN
   ├── sub-scoring-engine ............ multi-dimensional weighted scoring
   ├── [challenge] devil's-advocate assumption review
   ├── sub-improvement-roadmap ....... prioritized effort/impact actions
   ├── [GATE] sub-compliance-check (BLOCKING)
   └── synthesize ................... professional deliverable + quality gates
```

## Full Sub-Skill Catalog
### sub-compliance-check — Compliance Check
- **Purpose:** Verify outputs against applicable regulations/standards and attach the required informational/non-advice disclaimers before final delivery.
- **Inputs:** case context from prior stage.
- **Outputs:** structured result passed to the next stage.
- **Tools:** Read, WebSearch/WebFetch (as needed).
- **Quality gate:** output is complete, evidence-cited, and consistent with frameworks before proceeding.

### sub-intake — Intake & Context Gathering
- **Purpose:** Collect the structured inputs, scope, and goals needed to run the analysis; ask clarifying questions when key facts are missing.
- **Inputs:** case context from prior stage.
- **Outputs:** structured result passed to the next stage.
- **Tools:** Read, WebSearch/WebFetch (as needed).
- **Quality gate:** output is complete, evidence-cited, and consistent with frameworks before proceeding.

### sub-framework-selector — Evaluation Framework Selector
- **Purpose:** Pick the most appropriate named world-renowned framework(s) for the case and justify the choice.
- **Inputs:** case context from prior stage.
- **Outputs:** structured result passed to the next stage.
- **Tools:** Read, WebSearch/WebFetch (as needed).
- **Quality gate:** output is complete, evidence-cited, and consistent with frameworks before proceeding.

### sub-scoring-engine — Scoring Engine
- **Purpose:** Apply the multi-dimensional rubric to produce weighted scores with evidence citations for each dimension.
- **Inputs:** case context from prior stage.
- **Outputs:** structured result passed to the next stage.
- **Tools:** Read, WebSearch/WebFetch (as needed).
- **Quality gate:** output is complete, evidence-cited, and consistent with frameworks before proceeding.

### sub-improvement-roadmap — Improvement Roadmap
- **Purpose:** Generate a prioritized, effort/impact-ranked set of recommendations traceable to the scored findings.
- **Inputs:** case context from prior stage.
- **Outputs:** structured result passed to the next stage.
- **Tools:** Read, WebSearch/WebFetch (as needed).
- **Quality gate:** output is complete, evidence-cited, and consistent with frameworks before proceeding.


## Evaluation Frameworks (World-Renowned, Citable)
| Framework / Standard | Role in this skill |
|---|---|
| UCC & CISG | US commercial code and international sale-of-goods convention. |
| UNIDROIT Principles | International commercial-contract principles. |
| Risk-allocation analysis | Indemnity, limitation of liability, warranties, IP. |
| Plain-language drafting | Clarity, defined terms, antecedent consistency. |
| Boilerplate review | Governing law, dispute resolution, force majeure, assignment. |

## Scoring Model
| Dimension | Weight | What is assessed |
|---|---|---|
| Risk allocation | 25% | indemnity, liability caps, warranties |
| Legal compliance & enforceability | 25% | governing law, regulatory, unenforceable terms |
| Clarity & completeness | 20% | defined terms, ambiguity, gaps |
| Commercial fairness / balance | 15% | one-sidedness, leverage |
| Dispute & exit provisions | 15% | termination, dispute resolution, remedies |
Each dimension is scored 0-100 with cited evidence; the weighted total yields an overall grade (A: 90+, B: 75-89, C: 60-74, D: <60).

## Skill File Format Specification
- Frontmatter: `name`, `description`.
- Required sections: Role & Persona, Workflow (Harness Flow), Sub-skills Available, Tools, Output Format, Quality Gates.

## E2E Execution Flow
1. Parse user request; if inputs are insufficient, `sub-intake` asks targeted questions.
2. `sub-framework-selector` picks framework(s) and justifies the choice.
3. Research stage gathers highest-tier evidence (see evidence hierarchy); degrade gracefully to SECOND-KNOWLEDGE-BRAIN if offline.
4. `sub-scoring-engine` scores each dimension with citations.
5. Challenge stage stress-tests conclusions.
6. `sub-improvement-roadmap` produces ranked actions.
7. `sub-compliance-check` attaches disclaimers and verifies regulatory alignment.
8. Synthesize deliverable; run Quality Gates; present.

**Error handling:** missing inputs → ask; conflicting evidence → present both and grade certainty; tool failure → fallback + explicit limitation notice.

## SECOND-KNOWLEDGE-BRAIN Integration
- Sources:
  - https://www.unidroit.org/instruments/commercial-contracts/unidroit-principles-2016
  - https://uncitral.un.org/en/texts/salegoods/conventions/cisg
  - https://www.law.cornell.edu/ucc/2
  - https://www.americanbar.org/groups/business_law/
  - https://www.americanbar.org/groups/public_contract_law/
  - https://www.ali.org/publications/show/restatement-second-contracts/
- ArXiv categories: n/a
- Crawl queries: commercial contract risk clause trends; limitation of liability enforceability case; force majeure drafting post pandemic; SaaS agreement data protection clauses
- Append format: dated entries with Title, Authors, Year, Venue, DOI/URL, key finding, relevance.

## Supporting Tools Spec
- `tools/knowledge_updater.py`: CLI (`--brain`, `--dry-run`, `--source`, `--query`, `--verbose`). Inputs = source list + queries; outputs = appended SECOND-KNOWLEDGE-BRAIN entries; schedule = weekly cron; dedup by URL/DOI hash; graceful degradation if crawl4ai/network unavailable; optional `requests` + `BeautifulSoup` fallback.
- `tools/requirements.txt`: lists `crawl4ai`, `requests`, `beautifulsoup4`, `lxml`.
- `tests/test_knowledge_updater.py`: 10 unit tests covering hashing, dedup, scoring, HTML stripping, and the requests fallback.

## Quality Gates (must all pass before final output)
- Every score cites at least one source or the chosen framework.
- Compliance check passed; disclaimers attached.
- Challenge stage completed; key assumptions tested.
- Roadmap items are prioritized by effort and impact and traceable to findings.
- Limitations and evidence certainty are stated explicitly.

## Test Scenarios
1. **Risk review** — User: "Review this supplier contract for risks" → COMPLIANCE/disclaimer first; skill redlines indemnity/liability/IP, scores risk, roadmap.
2. **Drafting** — User: "Draft a mutual NDA for two startups" → Skill drafts balanced NDA, flags choices needing legal sign-off.
3. **One-sided clause** — User: "Is this liability clause fair to me?" → Skill flags uncapped liability/one-sidedness, suggests balanced alternative.
4. **Compliance gate** — User: "Is this contract legally binding for sure?" → COMPLIANCE: states informational only, recommends licensed attorney for the jurisdiction.
5. **Degraded mode** — User: "Review offline" → Falls back to SECOND-KNOWLEDGE-BRAIN, signals it can't check latest statutes/precedent.

## Key Design Decisions
1. Framework-grounded scoring (no ad-hoc criteria).
2. Research-first with graceful degradation to the local knowledge brain.
3. Mandatory challenge stage to counter confirmation bias.
4. Hard safety/compliance gates for this regulated/sensitive domain.
5. Self-improving knowledge base via weekly crawl.

## Active Development Tasks
- [x] Scaffold full deliverable set
- [x] Define 5 sub-skills
- [x] Productionize `tools/knowledge_updater.py` with CLI, fallback fetcher, and unit tests
- [x] Populate `SECOND-KNOWLEDGE-BRAIN.md` with real, citable sources
- [x] Complete Phase 5 cross-skill cluster integration
