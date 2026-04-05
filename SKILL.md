---
name: autoacad
description: Use when running an end-to-end academic paper project or upgrading a research idea into a submission-grade workflow with literature review, experiments, writing, review, and export.
---

# AutoAcad

## Overview

AutoAcad is a layered research-paper package. It keeps the lightweight repo-and-experiment workflow from `academic` and adds the heavier paper pipeline: stage gates, evidence checks, paper drafting, review, and export.

Use the narrowest subskill that matches the current stage. Use the package root only when the task spans multiple stages or the user wants an end-to-end workflow.

## Route by Stage

| Need | Use |
| --- | --- |
| Inventory the project, docs, data, codebase, and constraints | `autoacad-prepare` |
| Collect papers, benchmark families, datasets, and theory notes | `autoacad-survey` |
| Turn synthesis into hypotheses, claims, and contribution framing | `autoacad-ideate` |
| Design experiments, baselines, ablations, and project structure | `autoacad-plan` |
| Implement and run experiments with pilot timing and self-repair | `autoacad-run` |
| Interpret metrics, decide proceed/refine/pivot, and surface evidence gaps | `autoacad-analyze` |
| Produce outline, section drafts, figure plan, and paper wording | `autoacad-draft` |
| Stress-test methodology-evidence consistency and reviewer objections | `autoacad-review` |
| Prepare final package, citations, archive, and export checks | `autoacad-export` |

## Operating Rules

1. Treat `references/restricts.md` as the hard floor. Do not present environment issues, setup failures, or debugging artifacts as research contributions.
2. Use `references/pipeline.md` to map the current request onto the 25-stage loop. Do not pretend the workflow is linear when evidence requires a refine or pivot.
3. Use `references/experiment-rules.md` before generating or modifying experiment code.
4. Use `references/paper-structure.md` before drafting or revising paper text.
5. If the user wants a new project scaffold, run `scripts/init_paper_project.py` rather than recreating folders ad hoc.
6. Track progress in `PROGRESS.md` and per-stage plans in `plans/`. If the project does not have them yet, initialize them first.

## Bundled Resources

- `references/pipeline.md`: stage groups, loop points, and gate semantics.
- `references/restricts.md`: topic lock, evidence discipline, and anti-fabrication rules.
- `references/experiment-rules.md`: pilot timing, time-guard, convergence, and numerical-stability requirements.
- `references/paper-structure.md`: section goals, word budgets, and paper-quality checks.
- `references/source-blueprint.md`: normalized mapping from the original long-form mega-prompt into AutoAcad layers.
- `references/update-playbook.md`: maintainer guide for updating AutoAcad when the upstream long-form prompt changes.
- `references/upstreams.md`: generated summary of current `AutoResearchClaw` and `AI-Researcher` upstream state.
- `references/upstream-snapshots/`: local copies of tracked upstream source files for review.
- `references/upstream-review.md`: optional LLM-generated recommendations based on upstream drift.
- `templates/PROGRESS.template.md`: reproducibility and iteration log template.
- `templates/stage-plan.template.md`: per-stage planning template.
- `templates/paper-tree.template.md`: canonical paper project tree.
- `scripts/init_paper_project.py`: scaffold a paper project directory.
- `scripts/check_stage_outputs.py`: verify required folders and stage artifacts exist.
- `scripts/check_results_vs_claims.py`: compare results JSON against draft text to catch unsupported numeric claims.
- `scripts/update_from_upstreams.py`: refresh upstream snapshots and generate AutoAcad update reports.
