# AutoAcad Domain Executor Selection

Imported from AutoResearchClaw v0.5.0 (multi-domain experiment agents + ARC-Bench). Use during `plan/` and `run/` to pick the experiment executor before applying budget scaling from `experiment-rules.md`.

## Routing Table

| Domain | Executor | Notes |
| --- | --- | --- |
| ML (default) | sandbox with numpy/stdlib | No torch/tensorflow/jax/sklearn/pandas/scipy unless the user requires it. |
| High-energy physics | ColliderAgent chain: Lagrangian → FeynRules → MadGraph5 → Delphes | Simulation step count is the budget-scalable unit. |
| Biology | COBRApy genome-scale metabolic modelling | Scale reaction/enzyme conditions, not trial seeds. |
| Statistics | simulation-study agent | Scale by number of Monte Carlo replicates; reduce seeds when budget is tight. |
| Chemistry / materials | generic Docker executor with domain-specific image | Budget scaling is mandatory. |

## Selection Rule

1. Infer domain from the research topic and `problem-decompose` output.
2. If the domain matches a row above, select that executor and record the choice in `PROGRESS.md`.
3. If no domain executor applies, fall back to the ML sandbox or the generic executor.
4. Print the chosen executor and the resulting budget-scaling decision before the main run.

## Reporting Requirement

- Record `executor`, `executor_reason`, and the applied scaling rule in `PROGRESS.md` under the `experiment-run` entry.
- Save domain-specific logs (MadGraph output, COBRApy JSON, Docker container logs) under `results/<domain>/` alongside the standard `results.json`.

## What AutoAcad Does Not Import

- Cloud-specific infrastructure (e.g. Magnus cloud) — substitute local or user-provided compute.
- ARC-Bench manifests and rubrics — those live upstream; use them only if the user explicitly wants benchmark replication.
