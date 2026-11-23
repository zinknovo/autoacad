# AutoAcad Upstream Review

This file is generated automatically from upstream context plus local AutoAcad files.

Reviewed AutoResearchClaw HEAD: `be4ba4755bf1b52220f25e13b2293b5956590070`
Reviewed AI-Researcher HEAD: `6183315df2d475fbfd123ea7a0756cc54a632d57`

# AutoAcad Upstream Sync Recommendations

## Summary

AutoAcad's core pipeline is well aligned with the AutoResearchClaw stage-gate model, and `references/restricts.md` already captures most of the topic-lock, anti-fabrication, and NumPy 2.x rules from `prompts.default.yaml`. The main drift is:

- AutoResearchClaw **v0.5.0** introduces **domain-specialist executors** (ColliderAgent / COBRApy / statistics simulation / Docker chemistry) and an **ARC-Bench** with per-topic manifests (research question + conditions + metrics + datasets) and rubrics. AutoAcad's `pipeline.md` still treats "experiment execution" as a single monolithic stage and only vaguely references `domain-executor.md`.
- AutoResearchClaw **v0.4.0** HITL introduces intervention modes (`full-auto`, `gate-only`, `checkpoint`, `step-by-step`, `co-pilot`, `custom`), SmartPause, and claim verification. `plan/SKILL.md` and `review/SKILL.md` don't currently surface them.
- AutoResearchClaw has a first-class **VerifiedRegistry + experiment diagnosis & repair loop** (v0.3.2). `run/SKILL.md` should reflect it, but `restricts.md` and `experiment-rules.md` already cover the underlying intent.
- AI-Researcher's `prepare_agent.py` shows a **structured reference-codebase preparation outcome** (`reference_codebases`, `reference_paths`, `reference_papers`) with explicit repo-selection criteria (stars, recency, README quality, code-structure clarity, language/framework preference). AutoAcad's prepare stage is under-specified and doesn't produce this artifact.
- AI-Researcher's **Level 1 vs Level 2 input** distinction (detailed idea vs reference-paper ideation) is a useful entry-point clarification missing from `SKILL.md` route and from `ideate/SKILL.md`.
- `paper-structure.md` is missing explicit ARC-Bench rubric-style **grading criteria** (required to check `quality_gate` against benchmarks rather than just word counts).

Everything below is scoped; no whole-package rewrite is proposed.

---

## Recommended File Updates

### `references/pipeline.md`
- Under **Stage Groups**, split Group E ("Execution") into two sub-rows: `E1. Executor selection` (map research domain → domain executor using the v0.5.0 routing table) and `E2. Experiment run + iterative refine`. This matches the v0.5.0 routing model without inventing new stages.
- Add a short subsection **"Domain executors (v0.5.0)"** listing the four executors (ML sandbox, ColliderAgent, COBRApy, statistics simulation) and the fallback (Docker generic) with a pointer to `experiment-rules.md#domain-executor-selection`. Do not duplicate the routing table.
- Add a new gate row: `executor_selection` — "stop if the research domain is ambiguous or no executor clearly applies; resolve to ML sandbox + explicit note."
- Under **Loop Points**, add HITL-style modes as an overlay, not a stage: `gate-only` / `checkpoint` / `step-by-step` / `co-pilot` / `custom` (per v0.4.0). One line each, plus a pointer to `plan/SKILL.md`.
- Add a short subsection **"ARC-Bench topic manifests"** noting that when the project targets a benchmarked topic, the manifest (research question, conditions, metrics, datasets) and its rubric drive `quality_gate`, not word counts.
- In **Minimum Cycle Discipline**, add: "If a run cannot select a domain executor, record the fallback explicitly in `PROGRESS.md` — do not silently use the ML sandbox."

### `references/restricts.md`
- The **Topic Lock**, **Evidence Discipline**, **Anti-Fabrication**, **NumPy 2.x**, and **Code Generation Rules** sections already match upstream closely — leave content as-is.
- Add one bullet under **Code Generation Rules**: "If ARC-Bench manifest or rubric applies, ground all reported metrics in the manifest's declared metrics; do not substitute convenience metrics."
- Add one bullet under **Topic Lock**: "When using a domain executor, the technical approach section must describe the domain method (e.g., Lagrangians, metabolic flux, simulation study), not the executor orchestration."
- Add a short new section **"Benchmark Discipline (ARC-Bench)"** — 3–4 bullets: use manifest conditions verbatim unless documented as a deviation, cite the rubric source, log deviations in `PROGRESS.md`.

### `references/experiment-rules.md`
- The **Pilot and Time Budget**, **Numerical Discipline**, **Convergence**, **NumPy**, **Result Saving**, **Anti-Patterns**, and **Domain Executor Selection** sections are close to upstream — retain them.
- Expand **Domain Executor Selection** to spell out routing criteria (domain keyword / task type / required tooling) and the fallback path (already referenced via `domain-executor.md`). Currently this is a single-line pointer; make it five or six actionable bullets so the planner can actually route.
- Add an **"Experiment diagnosis and repair"** subsection (from v0.3.2): when a run fails numerically or diverges, first attempt (a) identify the instability source per Numerical Discipline, (b) retune the smallest responsible hyperparameter, (c) only then reduce scope. Record each repair attempt in `PROGRESS.md`.
- Add a **"Claim verification hook"** subsection: before handing results to `draft`/`review`, run `scripts/check_results_vs_claims.py`; treat failures as refine signals, not exportable.
- Cross-reference `scripts/check_results_vs_claims.py` from **Result Saving** so authors know the intended output format is enforced downstream.

### `references/paper-structure.md`
- Keep the **Target Structure** table.
- Add a short **"Rubric-aligned quality checks"** subsection: for ARC-Bench topics, map each rubric item (novelty / correctness / experimental rigor / writing) to the section that must evidence it. Do not add new sections.
- Add one rule under **Core Paper Rules**: "Benchmark-derived numbers must trace back to the manifest's declared metrics and be reproduced by `results.json`."

### `prepare/SKILL.md`
- Mirror AI-Researcher's `prepare_agent.py` outcome. Require the prepare stage to emit a structured artifact — `prep.json` (or markdown table) with `reference_codebases`, `reference_paths`, `reference_papers`, plus one-line rationale per entry.
- Add explicit **repo-selection criteria** (from AI-Researcher, tightened): recency, README completeness, code-structure clarity, language/framework match, active maintenance. Cap the shortlist at 5–8 repos.
- Add an **"Input mode" section**: Level 1 (detailed idea provided) vs Level 2 (reference papers only, derive idea). Declare which mode the current project is in within `PROGRESS.md`.
- Add a checklist item: "Confirm whether the target is an ARC-Bench topic; if so, capture the manifest path."

### `survey/SKILL.md`
- Add a "Benchmark family awareness" item: when the topic is close to an ARC-Bench domain (ML, HEP, quantum, biology, statistics), record the relevant ARC-Bench topic IDs and manifest paths in the survey notes — so `plan`/`run` can reuse conditions and metrics rather than re-invent them.
- Add a note to preserve `DOI / arXiv ID / URL` consistently with `restricts.md` (already implied but list it here as an explicit output requirement).

### `ideate/SKILL.md`
- Add a **"Level 1 vs Level 2"** entry branch (from AI-Researcher): for Level 2, summarize the reference papers' shared gaps and propose 2–3 candidate ideas; for Level 1, ground ideation in the user's stated problem and only introduce references as support.
- Add: hypotheses must include a **measurable prediction and failure condition** — AutoResearchClaw's `hypothesis_gen` prompt requires this, and it is the cleanest way to make `analyze`'s proceed/refine/pivot decision testable.
- Add: at least 2 falsifiable hypotheses per cycle (matches upstream prompt).

### `plan/SKILL.md`
- Add a **"HITL mode selection"** line: choose `full-auto` / `gate-only` / `checkpoint` / `step-by-step` / `co-pilot` / `custom` (v0.4.0) and record it in `PROGRESS.md`. Default to `gate-only` for anything with real reviewer risk.
- Add a **"Domain executor selection"** step before resource planning — pick executor, then apply budget scaling rules from `experiment-rules.md`.
- Add a **"Benchmark manifest"** step: if targeting an ARC-Bench topic, import conditions/metrics/datasets from the manifest and record deviations in a `deviations.md`.
- Keep the existing experiment-design gate language; do not restructure the planning content beyond adding these three steps.

### `run/SKILL.md`
- Add a **"Diagnosis & repair loop"** subsection consistent with `experiment-rules.md`: detect → localize → retune smallest factor → rerun → record. Cap retries (e.g. 3 per condition) before escalating to `analyze`.
- Add: "Save partial results before any retry; never overwrite a failed run's `results.json` — write `results.run<N>.json`."
- Add: "On completion, invoke `scripts/check_results_vs_claims.py` and attach its report to `PROGRESS.md` before advancing."

### `analyze/SKILL.md`
- Add a **"Rubric-anchored decision"** line: when an ARC-Bench (or comparable) rubric applies, the `PROCEED / REFINE / PIVOT` decision must reference rubric items not yet evidenced.
- Add: "Emit an explicit evidence-gap list; each gap maps to either a `REFINE` action in `plan` or a `LIMITATIONS` entry in `draft`." This formalizes the existing "surface evidence gaps" phrase.

### `draft/SKILL.md`
- Add: "Every numeric claim must originate in `results.json` (or a cited paper for survey numbers). Cross-link to `scripts/check_results_vs_claims.py`."
- Add a **"Level 1 vs Level 2 framing"** note: for Level 1, the introduction must center the user's stated problem; for Level 2, it must center the gap across the reference papers — the two modes need different introductions, and this is the single most common placement error.
- Add: draft the **Figure 1 plan before full-text drafting** (already in `paper-structure.md`; surface it here).

### `review/SKILL.md`
- Add a **"Rubric-driven stress test"** step: check each rubric item against the section that should evidence it (from `paper-structure.md`), and record misses.
- Add a **"Claim verification"** step: run `scripts/check_results_vs_claims.py`; treat any failing claim as a blocking review issue, not a stylistic nit.
- Add a **"Claim-evidence registry"** note: enumerate every claim ↔ `results.json` key ↔ figure/table reference; use as the rebuttal-phase input.

### `export/SKILL.md`
- Add a **"Pre-export verification"** checklist binding: (a) `check_results_vs_claims.py` passes, (b) claim-evidence registry is complete for every metric cited, (c) ARC-Bench manifest referenced in the package if applicable, (d) `prep.json` and `results.run*.json` archived.
- Add: "Export must not modify numeric results or wording that would change claim strength — if a fix is required, loop back to `draft`/`review`."

---

## No-Change Areas

The following are already aligned with upstream (or soundly diverge) and should not be touched in this sync pass:

- `references/restricts.md` — top-level structure and Topic Lock / Evidence Discipline / Anti-Fabrication phrasing already matches `prompts.default.yaml#topic_constraint` and the code-generation anti-patterns.
- `references/experiment-rules.md#pilot-and-time-budget` — scaling thresholds (100 / 500 conditions, 300s / 120s steps, 80% guard) match the upstream `compute_budget` block verbatim in spirit.
- NumPy 2.x compatibility blocks in `restricts.md` and `experiment-rules.md` — match upstream verbatim.
- `references/paper-structure.md#target-structure` — word budgets and section ordering are AutoAcad-specific and well-formed; keep them.
- Root `SKILL.md` routing table — the nine-subskill layout is a clean decomposition of the upstream stages; only the `prepare`/`plan`/`run`/`review`/`export` subskills need the additions above.
- Bundled `scripts/*` — no changes required for this sync; they already support the flows referenced (`check_results_vs_claims.py` is the natural home for the rubric/claim checks listed above).
- `templates/PROGRESS.template.md` and `templates/stage-plan.template.md` — the additions above reference their use; no schema change needed this pass (a future pass could add HITL-mode and executor fields, but that's out of scope here).
