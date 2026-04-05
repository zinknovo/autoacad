# AutoAcad Source Blueprint

This file is the normalized source model behind AutoAcad. It is the place to update when a long upstream mega-prompt changes.

## Purpose

The original upstream text mixed several kinds of information together:

- pipeline stages
- hard constraints
- paper-writing requirements
- experiment execution rules
- project directory requirements
- model/tool environment assumptions

AutoAcad does not store those as one giant prompt. It splits them into stable layers so each part can be updated independently.

## Layer Mapping

| Upstream content type | AutoAcad file |
| --- | --- |
| stage list, gate points, refine/pivot loops | `references/pipeline.md` |
| anti-fabrication rules, topic lock, evidence discipline | `references/restricts.md` |
| pilot timing, convergence, NaN/Inf handling, compute scaling | `references/experiment-rules.md` |
| section lengths, figure strategy, ablation and baseline expectations | `references/paper-structure.md` |
| project tree, `PROGRESS.md`, `plans/`, `results/` shape | `templates/paper-tree.template.md`, `templates/PROGRESS.template.md`, `templates/stage-plan.template.md` |
| project bootstrapping behavior | `scripts/init_paper_project.py` |
| artifact existence checks | `scripts/check_stage_outputs.py` |
| result-vs-paper numeric consistency checks | `scripts/check_results_vs_claims.py` |

## Current Imported Decisions

### Pipeline

- Preserve the 9 stage groups.
- Preserve gate stages for literature, experiment design, and final quality.
- Preserve explicit loop points: `PROCEED`, `REFINE`, `PIVOT`, and rebuttal-driven returns.
- Preserve the requirement to do at least two evidence-and-writing passes.

### Constraints

- Keep the topic lock strict.
- Forbid presenting environment issues as contributions.
- Forbid fabricated experimental numbers, trial counts, and unsupported claims.

### Experiment Discipline

- Require a pilot run before scale-up.
- Require printed time estimation before long jobs.
- Require real convergence logic and root-cause fixes for NaN/Inf.
- Require reproducible structured results.

### Paper Discipline

- Keep the paper centered on 1-2 ideas.
- Treat Figure 1 as a first-class planning artifact.
- Require strong baselines and explicit ablations.
- Keep section depth close to top-tier conference expectations.

## What AutoAcad Deliberately Did Not Import Literally

- exact prompt boilerplate for every stage
- model-name placeholders
- hardcoded venue placeholders
- tool names that only make sense in another runtime
- workflow text that duplicates what a subskill already says

Those items were converted into smaller files so AutoAcad can evolve without becoming one huge brittle prompt.
