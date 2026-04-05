---
name: autoacad-run
description: Use when implementing and running paper experiments that need pilot timing, numerical safety, iterative repair, and reproducible outputs.
---

# AutoAcad Run

## Overview

Use this stage to execute experiments under strict anti-fabrication rules.

## Hard Rules

1. Run a pilot first and print a concrete time estimate before scaling.
2. Use real algorithms, real objectives, and real metrics. Never fake curves or report synthetic-looking numbers as findings.
3. Implement real convergence checks. Do not rely on fixed loops alone.
4. If NaN, Inf, or runtime warnings appear, fix the root cause. Do not patch over it with silent coercion.
5. Save partial results before a time guard triggers.

## Workflow

1. Generate or update runnable code.
2. Run a minimal pilot.
3. Inspect logs, warnings, and intermediate metrics.
4. Repair failures at the source.
5. Re-run until the pilot is stable.
6. Scale only within the compute budget.
7. Save structured outputs in `results/`.

## Required Artifacts

- Executable code under `code/`.
- Structured run outputs in `results/`.
- A run log or summary sufficient to reproduce the final numbers.
