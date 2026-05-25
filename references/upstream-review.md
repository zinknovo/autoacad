# AutoAcad Upstream Review

This file is generated automatically from upstream context plus local AutoAcad files.

Reviewed AutoResearchClaw HEAD: `b5804c5fa0acecc01f56bdf52995e11bb74474cc`
Reviewed AI-Researcher HEAD: `f9a6f8480860c193afff600eeffe3defcee8a978`

## Summary

The local AutoAcad package has a well-structured, staged research workflow that aligns broadly with both upstream systems (AutoResearchClaw and AI-Researcher). However, there are gaps and opportunities for refinement in specific reference files and SKILL.md descriptions. The core architectural decisions (stage gates, loop points, discipline rules) are solid, but some areas lack the depth or specificity present in the upstream versions.

---

## Recommended File Updates

### `references/experiment-rules.md`

**Current state:** Good foundation with pilot timing, time budget, numerical discipline, and NumPy 2.x compatibility notes. However, the compute budget scaling rules are slightly less detailed than AutoResearchClaw's `prompts.default.yaml` `compute_budget` block.

**Recommended update:**
- Add an explicit **sandbox package restriction** section (copy from AutoResearchClaw's `pkg_hint_sandbox` block): "AVAILABLE PACKAGES (sandbox mode): Python stdlib, numpy, math, random, statistics, json. Do NOT use: torch, tensorflow, jax, sklearn, pandas, scipy, matplotlib, or any deep learning framework."
- Add a **"Time Estimation Protocol"** sub-section: "Print a 'TIME_ESTIMATE: Xs' line before the main loop, estimating total runtime based on a small pilot (run 1 condition, extrapolate)". This is present in your `references/experiment-rules.md` but could be more prominent.
- Add a **"Partial Results Mandate"**: "Always print intermediate results so partial data is captured on timeout" — similar to AutoResearchClaw's requirement.

**Rationale:** AutoResearchClaw has more rigid, machine-readable scaling rules (e.g., "If time_budget < 300s: limit total optimization steps to ≤5,000 per run"). These are valuable guardrails that your package could adopt or adapt.

---

### `references/restricts.md`

**Current state:** Strong topic lock and anti-fabrication rules. However, it lacks a dedicated **"Anti-Hallucination"** sub-section.

**Recommended update:**
- Add an "Anti-Hallucination Verification" sub-section (inspired by AutoResearchClaw's HITL system):
  - "No fabricated loss curves, significance tests, dataset counts, trial counts, or ablation results."
  - "No retrospective wording that implies a stronger experiment than was actually run." (already partially present)
  - **New rule:** "If an experiment failed or produced NaN/Inf, report it as such. Do not silently drop failed conditions from the table."
  - "All numeric claims in the paper must trace back to a specific `results/` file or log line."

**Rationale:** The upstream AutoResearchClaw has a dedicated anti-fabrication system (`VerifiedRegistry` + experiment diagnosis/repair loop). While you don't need the full system, adding explicit anti-fabrication rules strengthens the evidence discipline.

---

### `references/pipeline.md`

**Current state:** Good stage groups, gate semantics, and loop points. But it lacks explicit **"Preparation"** and **"Post-Processing"** stages that AI-Researcher includes (e.g., codebase analysis, repository selection).

**Recommended update:**
- Add a **"Group A. Preparation"** precursor stage (before "Definition"): 
  - `topic init` → "Analyze existing codebases, reference implementations, and GitHub repositories relevant to the topic"
  - Reference: AI-Researcher's prepare_agent.py (`case_resolved` function) which surveys GitHub repos, checks README quality, code structure, star counts, and recency to select 5-8 reference codebases.
- Add a **"File Output Verification"** sub-section to the "E. Execution" group: "Before declaring an experiment complete, verify that `results.json` exists, is parseable, and contains the expected metric keys." (Inspired by AI-Researcher's structured output expectations)

**Rationale:** AI-Researcher has a dedicated agent for assessing and selecting reference codebases. This is a gap in your pipeline that makes it harder for users to leverage existing implementations.

---

### `prepare/SKILL.md`

**Current state:** Likely focuses on inventorying the project, docs, data, and constraints based on the root `SKILL.md` route table.

**Recommended update:**
- Add a step to "Survey and select 5-8 reference codebases from GitHub (check stars, recency, README quality, code structure, Python/pytorch preference)" — modeled after AI-Researcher's prepare_agent.py.
- Add a step: "Run `scripts/init_paper_project.py` if project scaffolding doesn't exist" — this is already in the root SKILL.md but should be explicitly called out in the prepare subskill.

**Rationale:** AI-Researcher's prepare agent performs detailed codebase analysis that goes beyond simple inventory. Your prepare stage could benefit from this richer pre-work.

---

### `ideate/SKILL.md`

**Current state:** Likely focuses on hypothesis generation and contribution framing.

**Recommended update:**
- Add a sub-step: "Generate at least 2 falsifiable hypotheses (each with: rationale, measurable prediction, failure condition)" — borrowed from AutoResearchClaw's `hypothesis_gen` stage.
- Add a step: "Map each hypothesis to available reference codebases/datasets from the prepare stage" — ensuring ideation is grounded in actual resources.

**Rationale:** AutoResearchClaw's hypothesis generation is more structured (rationale, prediction, failure condition). Adding this structure improves falsifiability.

---

### `analyze/SKILL.md`

**Current state:** Likely focuses on interpreting metrics, deciding proceed/refine/pivot, and surfacing evidence gaps.

**Recommended update:**
- Add a step: "Validate that every numeric claim in the draft has a corresponding entry in `results/` files" — supported by your existing `scripts/check_results_vs_claims.py`.
- Add a sub-step for "Statistical rigor check": "Apply convergence checks based on objective or parameter change; report NaN/Inf sources explicitly" — from your experiment rules.

**Rationale:** This bridges the gap between raw results and paper claims, which is a core function of the analyze stage.

---

### `review/SKILL.md`

**Current state:** Likely focuses on stress-testing methodology-evidence consistency and reviewer objections.

**Recommended update:**
- Add a section: **"Anti-Hallucination Review"**: "Check for fabricated loss curves, hand-waved significance tests, invented dataset counts, trial counts, or ablation results." (from restricts.md)
- Add: "Verify that every ablation mentioned in the paper actually ran and has results in `results/`" — inspired by AutoResearchClaw's anti-fabrication system.

**Rationale:** The review stage is the last line of defense against unsupported claims. Explicit anti-fabrication checks strengthen this stage.

---

## No-Change Areas

### `survey/SKILL.md`
Your survey stage (collect papers, benchmark families, datasets, theory notes) is well-aligned with both upstream systems. The AutoResearchClaw literature stages (search strategy, collect, screen, extract) and AI-Researcher's literature review are conceptually similar. No changes needed.

### `plan/SKILL.md`
Your plan stage (design experiments, baselines, ablations, project structure) is comprehensive. Both upstream systems have similar experiment design stages. No changes needed.

### `run/SKILL.md`
Your run stage (implement and run experiments with pilot timing and self-repair) is already well-specified with time guards, partial result saving, and reproducibility checks. The NumPy 2.x compatibility notes are more detailed than upstream. No changes needed.

### `draft/SKILL.md`
Your draft stage (outline, section drafts, figure plan, paper wording) with the paper-structure.md reference is solid. The drafting order (outline → figure plan → method/experiments → results/discussion → introduction/related work → abstract → revision) is excellent. No changes needed.

### `export/SKILL.md`
Your export stage (prepare final package, citations, archive, export checks) covers the same ground as AutoResearchClaw's `export_publish` stage and AI-Researcher's manuscript creation. No changes needed.

### `references/paper-structure.md`
Your paper structure (target words per section, core rules, drafting order) is more detailed than both upstream systems. The per-section word budgets and "Figure 1 must be planned before full drafting" rule are strong. No changes needed.

---

## Summary Table

| File | Update Needed | Priority |
|------|--------------|----------|
| `references/experiment-rules.md` | Add sandbox restriction, time estimation protocol, partial results mandate | **Medium** |
| `references/restricts.md` | Add anti-hallucination verification sub-section, failed experiment reporting rule | **High** |
| `references/pipeline.md` | Add preparation stage (codebase analysis), file output verification | **Medium** |
| `prepare/SKILL.md` | Add reference codebase selection (GitHub survey), scaffold check | **High** |
| `ideate/SKILL.md` | Add structured hypothesis template, hypothesis-resource mapping | **Low** |
| `analyze/SKILL.md` | Add claim-to-results validation step, NaN/Inf reporting | **Medium** |
| `review/SKILL.md` | Add anti-hallucination review, ablation verification | **High** |
| `survey/SKILL.md` | No changes needed | — |
| `plan/SKILL.md` | No changes needed | — |
| `run/SKILL.md` | No changes needed | — |
| `draft/SKILL.md` | No changes needed | — |
| `export/SKILL.md` | No changes needed | — |
| `references/paper-structure.md` | No changes needed | — |
