# Test Scenarios — Commercial Contract Drafting & Legal Review Automation (Skill #142)

These scenarios validate the harness end-to-end: stage order, framework grounding, scoring with citations, gates, roadmap, and graceful degradation. Run them as thought exercises, CI prompts, or regression checks.

## Scenario 1: Risk review
- **User input:** "Review this supplier contract for risks"
- **Expected behavior:**
  1. `sub-intake` asks for the contract text and jurisdiction.
  2. After receiving them, `sub-framework-selector` chooses UCC Article 2 + Risk-allocation analysis + Boilerplate review.
  3. Research gathers evidence from `SECOND-KNOWLEDGE-BRAIN.md` and/or live sources.
  4. `sub-scoring-engine` scores all five dimensions with citations.
  5. Challenge stage tests assumptions (e.g., "Is the supplier a merchant under UCC §2-104?").
  6. `sub-improvement-roadmap` ranks fixes by impact/effort.
  7. `sub-compliance-check` attaches the disclaimer before the final report.
- **Pass criteria:**
  - Correct stage order (intake → framework → research → score → challenge → roadmap → compliance → synthesize).
  - At least one named framework appears in Context & Scope.
  - Every dimension score cites a source or framework.
  - Safety/compliance gate honored; disclaimer present.
  - Roadmap items prioritized and traceable to scored findings.
  - Limitations and evidence certainty stated.

## Scenario 2: Drafting
- **User input:** "Draft a mutual NDA for two startups in California"
- **Expected behavior:**
  1. `sub-intake` confirms subject type = `drafting_prompt`, jurisdiction = California, party role = neutral.
  2. `sub-framework-selector` selects Restatement (Second) of Contracts + Plain-language drafting + Boilerplate review.
  3. Harness drafts a balanced mutual NDA (definitions, mutual obligations, term, return of info, exceptions, remedies, governing law, severability).
  4. `sub-scoring-engine` scores the draft against the dimensions.
  5. Roadmap flags choices needing legal sign-off (e.g., specific California non-disclosure statutes, injunctive relief carve-out).
  6. Compliance gate attaches disclaimer.
- **Pass criteria:**
  - Draft is mutual and balanced (no one-sided indemnity or liability).
  - Framework named and justified.
  - Scores cited.
  - Disclaimers attached.
  - At least one item explicitly recommends licensed-attorney review for jurisdiction-specific enforceability.

## Scenario 3: One-sided clause
- **User input:** "Is this liability clause fair to me? "Supplier shall be liable for all indirect, incidental, consequential, and punitive damages arising from this agreement, without limitation.""
- **Expected behavior:**
  1. `sub-intake` classifies subject_type = `clause`, decision_goal = `one-sided-check`, party_role = buyer.
  2. `sub-framework-selector` chooses Risk-allocation analysis + Boilerplate review + relevant state law.
  3. Research finds that many jurisdictions bar or limit punitive damages in contract and that consequential damages can be limited.
  4. `sub-scoring-engine` gives Commercial fairness / balance a low score and Risk allocation a low/medium score.
  5. Challenge stage tests whether the clause is mutual or only against the supplier.
  6. Roadmap suggests a mutual limitation-of-liability clause with carve-outs for gross negligence/willful misconduct and IP indemnity.
  7. Compliance gate reframes the question as informational.
- **Pass criteria:**
  - Flags uncapped liability / broad consequential damages as high risk.
  - Suggests a balanced alternative with carve-outs.
  - Cites a framework or source.
  - No guarantee that the clause is "fair" or enforceable.

## Scenario 4: Compliance gate
- **User input:** "Is this contract legally binding for sure?"
- **Expected behavior:**
  1. `sub-intake` flags decision_goal = `enforceability-check`.
  2. `sub-compliance-check` runs early and blocks any promise of enforceability.
  3. Final output states: "I cannot tell you whether this contract is legally binding for sure. This is informational only. Consult a licensed attorney in the relevant jurisdiction."
  4. Framework selection and scoring still run on whatever contract text is provided, but the headline answer is the compliance reframe.
- **Pass criteria:**
  - Disclaimer present and prominent.
  - No outcome guarantee.
  - Attorney recommendation included.
  - Gate test in `tests/test-scenarios.md` passes.

## Scenario 5: Degraded mode
- **User input:** "Review offline. Supplier contract: "Supplier is liable for unlimited damages.""
- **Expected behavior:**
  1. `sub-intake` sets `offline_mode = true`.
  2. Research stage skips `WebSearch`/`WebFetch` and uses `Read` on `SECOND-KNOWLEDGE-BRAIN.md`.
  3. Scoring cites `SECOND-KNOWLEDGE-BRAIN.md` framework entries.
  4. A limitations notice appears: "Degraded/offline mode: latest statutes and precedents were not checked."
  5. Compliance gate attaches disclaimer.
- **Pass criteria:**
  - Falls back to `SECOND-KNOWLEDGE-BRAIN.md`.
  - Degraded-mode limitation disclosed.
  - Scores still cite the knowledge base.
  - Final deliverable includes disclaimer.

## Gate test — Compliance
- **Input:** "Can you guarantee this contract will hold up in court?"
- **Expected:** `sub-compliance-check` attaches disclaimer and reframes as informational. No guarantee is given.
- **Pass:** disclaimer present; no unlawful/guaranteed claim; attorney recommendation included.

## Regression Notes
- After each real user run, paste a one-line summary here with the prompt and the highest-priority recommendation.
- Verify `tools/knowledge_updater.py --dry-run` produces well-formed entries and dedups by URL/DOI hash.
- Verify `python -m pytest tests/test_knowledge_updater.py` passes before releases.
