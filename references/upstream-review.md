# AutoAcad Upstream Review

This file is generated automatically from upstream context plus local AutoAcad files.

Reviewed AutoResearchClaw HEAD: `a72c2679adab22a66b86d304b7fe79a78ea4e8e3`
Reviewed AI-Researcher HEAD: `f9a6f8480860c193afff600eeffe3defcee8a978`

# AutoAcad Package Update Analysis

## Summary

The upstream packages (AutoResearchClaw and AI-Researcher) have evolved significantly beyond AutoAcad's current state. Key differences include:

- **AutoResearchClaw v0.5.0** introduces multi-domain experiment agents (HEP, biology, statistics), a structured benchmark (ARC-Bench with 55 topics), human-in-the-loop co-pilot modes, and anti-fabrication verification systems.
- **AI-Researcher** provides a reference-based ideation system with automated GitHub repository analysis and codebase selection for implementation.
- AutoAcad currently lacks: domain-specific executors, structured benchmark integration, HITL co-pilot modes, and reference codebase harvesting capabilities.

## Recommended File Updates

### `references/pipeline.md`
- **Add multi-domain stage routing:** Insert stage group annotations for domain-specific executors (HEP, biology, statistics, chemistry) alongside the existing ML-default pipeline.
- **Add HITL gate semantics:** Include `human_review` and `co-pilot_approval` as optional gate checkpoints after `experiment_design` and `quality_gate`.
- **Add reference-harvesting stage:** Insert a `prepare` stage (matching AI-Researcher's pattern) between Definition and Literature groups for collecting reference codebases from GitHub.

### `references/restricts.md`
- **Add anti-fabrication verification system:** Add rule: "Run `check_results_vs_claims.py` (or equivalent) before any paper text claims a numeric result. Do not state experimental findings that cannot be traced to saved `results.json` files."
- **Add reference codebase discipline:** Add rule: "When using reference codebases, document git commit hash, repository URL, and license. Do not incorporate code without attribution or without verifying compatibility with the project's license."

### `references/experiment-rules.md`
- **Add domain-specific scaling patterns for biology (COBRApy) and statistics (simulation studies):** These already exist in the current file but should be annotated with concrete budget-scaling examples (e.g., "For COBRApy: scale reaction/enzyme conditions rather than trial seeds" — already present, but add "Limit to 5 reaction perturbations per budget under 300s").
- **Add reference codebase cloning guidance:** Add rule: "When using reference codebases from GitHub, clone only the minimal subset needed (no full dataset downloads). Budget the clone time into the pilot estimate."

### `prepare/SKILL.md`
- **Significantly expand:** This file is essentially absent from the upstream comparison. Add AI-Researcher-style reference-harvesting workflow:
  - GitHub search strategy for relevant repositories
  - `gen_code_tree_structure`-equivalent for repository analysis
  - README evaluation criteria (stars, recency, documentation quality, framework preference)
  - Reference selection with `case_resolved`-equivalent output
  - Integration with `scripts/init_paper_project.py` to incorporate reference codebases

### `survey/SKILL.md`
- **Add domain-aware search strategy:** Extend the literature search to include domain-specific sources (HEP: INSPIRE, Biology: PubMed, Statistics: arXiv stat.ML). Currently the survey skill appears to be generic.

### `plan/SKILL.md`
- **Add HITL planning hooks:** Insert optional co-pilot review checkpoints after experiment design. Add reference codebase integration planning (which repositories to fork/adapt, which to reference only).

### `run/SKILL.md`
- **Add multi-domain executor routing:** Document that run automatically selects executor based on domain tag (ML → numpy/stdlib, HEP → ColliderAgent/MadGraph5/Delphes, Biology → COBRApy, Statistics → simulation agent, Other → generic Docker executor). Add domain auto-detection logic documentation.

### `analyze/SKILL.md`
- **Add domain-specific metric interpretations:** For HEP: cross-section significance, for Biology: flux balance analysis metrics, for Statistics: Monte Carlo standard errors. Currently only generic metrics are discussed.

### `review/SKILL.md`
- **Add anti-fabrication verification step:** Before final review, run claim-checking scripts (analogous to AutoResearchClaw's VerifiedRegistry). Add domain-specific review guidelines (e.g., for HEP: verify simulation parameters match detector specifications).

### `export/SKILL.md`
- **Add ARC-Bench compatibility check:** If the paper topic matches an ARC-Bench entry, add automatic rubric scoring and format validation. Add open-source contribution packaging (repository export with results, notebooks, and reproducibility artifacts).

## No-Change Areas

### `references/paper-structure.md`
The upstream packages do not specify a different paper structure. AutoAcad's section goals, word budgets, and core rules (Figure 1 planning, ablation requirements, comparable baseline tuning) remain aligned with best practices.

### `ideate/SKILL.md`
The ideation stage in AutoAcad is already hypothesis-focused. Upstream packages (AutoResearchClaw) emphasize falsifiable hypotheses, which AutoAcad's current `ideate` stage appears to support. The upstream "Idea Workshop" from HITL mode is an optional enhancement, not a structural gap.

### `draft/SKILL.md`
AutoAcad's drafting guidance (outline → figure plan → method/experiments → results → introduction → abstract) matches upstream best practices. No changes needed unless domain-specific writing templates are added later.
