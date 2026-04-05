---
name: autoacad-plan
description: Use when designing experiment plans, baselines, ablations, compute budgets, and project structure for a research-paper project.
---

# AutoAcad Plan

## Overview

Use this stage to convert ideas into an executable experiment program.

## Workflow

1. Read the method concept and literature synthesis together.
2. Design datasets, task definitions, baselines, proposed method variants, ablations, metrics, risks, and compute budget.
3. Require strong baselines. Do not accept obviously weak or untuned comparators.
4. Require ablations for every claimed effective component.
5. Define evidence coverage up front:
   - What tables are needed?
   - What plots are needed?
   - What statistical checks are needed?
6. Create a pilot run plan first. Estimate total runtime before scaling.
7. Write the stage plan into `plans/` and update `PROGRESS.md`.

## Deliverables

- Experiment plan YAML or equivalent structured artifact.
- Resource schedule with dependencies and estimated runtime.
- Explicit go/no-go criteria for the first pilot.
