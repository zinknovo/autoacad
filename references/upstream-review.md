# AutoAcad Upstream Review

This file is generated automatically from upstream context plus local AutoAcad files.

Reviewed AutoResearchClaw HEAD: `84dad0a401404739cfcc47851cd1d282b671bb2f`
Reviewed AI-Researcher HEAD: `f9a6f8480860c193afff600eeffe3defcee8a978`

# Comparison Report: Local AutoAcad vs. Upstream (AutoResearchClaw + AI-Researcher)

## Summary

The local AutoAcad package is a **well-structured, streamlined research-paper pipeline** that has successfully adapted concepts from both upstream projects. Compared to the upstream sources:

- **AutoResearchClaw** is a full-featured research automation system with 23+ stages, CLI tools, Docker sandboxing, multi-agent subsystems, and a sophisticated Human-in-the-Loop (HITL) system. It operates as an **installed tool** with config files (`prompts.default.yaml`), skills libraries, and a framework for collaborative research.

- **AI-Researcher** is a comprehensive end-to-end system focused on **autonomous scientific innovation** with a strong emphasis on code-based research, idea generation from reference papers, and Docker-based execution environments.

- **AutoAcad** is a **lightweight, prompt-based skill package** designed for Claude Code. It strips away the infrastructure complexity (Docker, CLI tools, multi-agent orchestration) while preserving the core research workflow logic.

The local package is **largely aligned** with upstream practices, but there are specific gaps and upgrade opportunities in how it handles topic constraints, experiment reproducibility, paper structure validation, and pipeline integration.

---

## Recommended File Updates

### 1. `references/restricts.md` — Add Topic Constraint Clarification from AutoResearchClaw

**Current state:** Has topic lock, evidence discipline, anti-fabrication, and writing discipline sections. Missing the explicit `=== HARD TOPIC CONSTRAINT ===` block from AutoResearchClaw's `prompts.default.yaml`.

**Recommended change:** Add the structured topic constraint block from the upstream prompt template:

```markdown
## Topic Constraint Enforcement

When the user provides a specific topic, enforce these rules:

=== HARD TOPIC CONSTRAINT ===
- The paper MUST be about the specified topic.
- Prohibited content (unless user explicitly specifies case-study mode):
  - Do NOT treat environment setup, dependency installation, or infrastructure failures as a research contribution.
  - Do NOT present debugging logs, system errors, or configuration issues as experimental findings.
  - Do NOT drift to tangential topics not directly related to the stated topic.
  - Every section MUST connect back to the core research question.
  - The Abstract and Introduction MUST clearly state the research problem derived from the topic.
  - The Method section MUST describe a technical approach, not a workflow.
  - The Results section MUST report quantitative outcomes of experiments, not environment status.
=== END CONSTRAINT ===
```

**Reasoning:** This explicit block is more actionable for LLM agents than the existing prose description. AutoResearchClaw uses this template variable injection pattern to ensure the constraint is evaluated at every stage.

---

### 2. `references/pipeline.md` — Add Missing Stages from AutoResearchClaw

**Current state:** Lists 9 stage groups (A-I) with simple descriptions. Missing:
- Explicit "code generation" stage and "code fix/repair" loop
- "Experimental archive" stage (storing not just results but experiment metadata, configs, and environment snapshots)
- "Knowledge archive" stage for saving insights for future projects

**Recommended change:** Extend the Stage Groups table:

| Group | Stages | Goal |
|-------|--------|------|
| ...existing groups... | | |
| D. Design | experiment design, **code generation**, **code validation/repair**, resource planning | Specify and implement the evaluation program |
| G. Writing | outline, draft, peer review, revision, **experimental draft consistency check** | Convert evidence into a paper |
| H. Finalization | quality gate, **experiment archive**, **knowledge archive**, export, citation verify | Prepare the final package |

**Reasoning:** AutoResearchClaw explicitly separates "code generation" (Stage 10) and "experiment run" into distinct stages with repair/refinement loops. AI-Researcher also emphasizes code generation as a core research function. Adding these stages makes the pipeline more complete without adding infrastructure complexity.

---

### 3. `references/pipeline.md` — Add Comparison Loop Points from AutoResearchClaw

**Current state:** Loop points are vague: "After analysis: PROCEED, REFINE, or PIVOT".

**Recommended change:** Add structured loop semantics inspired by AutoResearchClaw's HITL system:

```markdown
## Loop Point Semantics

At each gate and analysis point, produce a structured decision:

### Decision Types
- **PROCEED**: Evidence is sufficient. Continue to next stage group.
- **REFINE**: Claims exist but experiments are incomplete. Return to Experiment Design or Execution.
- **PIVOT**: Hypothesis is unsupported. Return to Literature or Synthesis stage. Record the failed hypothesis in PROGRESS.md.

### Gate-Specific Checks
- **literature_screen**: Stop if the shortlist has <5 papers or >30% are non-peer-reviewed sources.
- **code_generation**: Stop if pilot experiment fails or does not converge within the compute budget.
- **experiment_design**: Stop if baselines, ablations, or metrics are under-specified.
- **quality_gate**: Stop if claims outrun evidence or if the paper is materially under-developed.
```

**Reasoning:** AutoResearchClaw's HITL system uses structured decision gates with explicit recovery paths. This provides clearer guidance to the LLM on when to loop back and what threshold triggers a pivot.

---

### 4. `run/SKILL.md` — Add Experiment Execution Safeguards from Upstream

**Current state:** Likely has basic experiment execution instructions.

**Recommended change:** Add the compute budget enforcement block from AutoResearchClaw's `prompts.default.yaml`:

```markdown
## Compute Budget Enforcement

When executing experiments:
1. **Estimate first**: Run one small pilot condition, measure time, then print `TIME_ESTIMATE: <seconds>`.
2. **Scale rules**:
   - If total conditions > 100: reduce seeds to 3-5 (not 20)
   - If total conditions > 500: reduce to 2-3 representative conditions per factor
3. **Time guard**: Check elapsed time every 10 iterations; stop gracefully at 80% of budget, saving all results collected so far.
4. **Partial results**: Always print intermediate results to stdout so partial data is captured on timeout.
```

**Reasoning:** AutoResearchClaw has hardened these rules through practical usage (as evidenced by the v0.3.2 release notes mentioning anti-fabrication system and experiment diagnosis & repair loop). These concrete rules prevent runaway experiments and ensure partial data capture.

---

### 5. `analyze/SKILL.md` — Add Anti-Fabrication Verification from Upstream

**Current state:** Likely focused on result interpretation.

**Recommended change:** Add evidence verification step (adapted from AutoResearchClaw's VerifiedRegistry):

```markdown
## Claim-Result Verification

Before finalizing analysis:
1. Cross-reference every numeric claim in the draft against experiment results.
2. Verify that:
   - Loss curves are from actual optimizer runs (not synthetic)
   - Significance tests computed from real trial distributions
   - Dataset counts match actual data loaded
   - Ablation results reflect actual ablation runs (not full-model numbers reused)
3. Flag any unmatched or unverifiable claims for REFINE or re-analysis.
```

**Reasoning:** The AutoResearchClaw anti-fabrication system (VerifiedRegistry + experiment diagnosis & repair loop) is one of its strongest features. AI-Researcher also emphasizes rigorous result analysis. Adding this step ensures output integrity without requiring the infrastructure of a full verified registry.

---

### 6. `draft/SKILL.md` — Add Paper Structure Validation from AI-Researcher

**Current state:** References `paper-structure.md` for section goals.

**Recommended change:** Add a structure validation checklist at the end of the drafting process:

```markdown
## Paper Structure Validation

After drafting, verify:
- [ ] Every section is between 80-120% of its target word budget
- [ ] Figure 1 is planned or drafted
- [ ] Every method component mentioned has an ablation
- [ ] Baselines received comparable tuning effort (documented in appendix if needed)
- [ ] Citations support claims (not decorative)
- [ ] The core novelty is limited to 1-2 ideas
- [ ] Limitations section narrows claims, not hides risk
- [ ] Results section includes quantitative outcomes from actual experiments
- [ ] Abstract states: problem, method, key numeric result, conclusion
```

**Reasoning:** AI-Researcher's framework places strong emphasis on structured paper generation with validation. This checklist operationalizes the rules from `references/paper-structure.md` into an actionable validation step during drafting.

---

### 7. `plan/SKILL.md` — Add Experiment Plan Structure from AutoResearchClaw

**Current state:** Likely has experiment design guidance.

**Recommended change:** Add explicit YAML structure requirement (adapted from AutoResearchClaw's experiment_design prompt):

```markdown
## Experiment Plan Specification

Design the experiment plan with these required keys:
- **objectives**: What specific questions does each experiment answer?
- **datasets**: Which datasets, with counts and preprocessing details
- **baselines**: Minimum 2 baselines with comparable tuning effort
- **proposed_methods**: Technical description of each method variant
- **ablations**: One ablation per component claimed as effective
- **metrics**: Primary and secondary metrics with justification
- **risks**: What could break and what backup plans exist
- **compute_budget**: Estimated runtime with scaling rules applied

Format the plan as structured YAML for machine readability.
```

**Reasoning:** AutoResearchClaw's `experiment_design` prompt enforces structured output with eight required keys. This ensures completeness and machine-processing of experiment plans, which enables automated checks later in the pipeline.

---

## No-Change Areas

### `references/paper-structure.md`
**Reason:** Already well-aligned with both upstream sources. The word budgets, section purposes, and core paper rules (Figure 1, ablation requirement, comparable baselines) match best practices from AI-Researcher's paper generation pipeline.

### `prepare/SKILL.md`
**Reason:** The project initialization focus is appropriate. Both upstream sources have their own initialization procedures (AutoResearchClaw has `init_paper_project.py`, AI-Researcher has a prepare agent), but AutoAcad's approach is simpler and sufficient for its scope.

### `survey/SKILL.md`
**Reason:** Literature collection methodology is standard and well-handled. The upstream sources don't introduce novel survey patterns beyond what AutoAcad already captures.

### `ideate/SKILL.md`
**Reason:** Hypothesis generation is a creative step that both upstream sources handle through LLM prompting. AutoAcad's approach is adequate.

### `review/SKILL.md`
**Reason:** The peer review simulation is a well-established pattern. Both upstream sources use similar approaches. AutoAcad's current implementation covers the essential review dimensions.

### `export/SKILL.md`
**Reason:** Export procedures are straightforward and well-handled. Neither upstream source introduces significant innovations in this area beyond basic formatting and citation checking.

### `references/experiment-rules.md`
**Reason:** Already contains the compute budget constraints, scaling rules, and NumPy compatibility notes from AutoResearchClaw. The pilot/time_estimate and time guard requirements are present and matched.

### Pipeline-level integration
The `SKILL.md` file's routing table, operating rules, and bundled resources list are appropriate for AutoAcad's lightweight scope. No changes needed to the overall structure or routing logic.
