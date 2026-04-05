---
name: autoacad-analyze
description: Use when interpreting experiment outputs, checking whether data supports the claims, and deciding whether to proceed, refine, or pivot.
---

# AutoAcad Analyze

## Overview

Use this stage to convert raw results into decisions.

## Workflow

1. Summarize actual metrics with exact numbers.
2. Compare against the planned hypotheses and contribution claims.
3. Check whether baselines are strong enough and whether ablations explain the gains.
4. Note statistical limitations, variance issues, missing runs, or unsupported claims.
5. Decide explicitly:
   - `PROCEED`: evidence is sufficient for drafting.
   - `REFINE`: implementation or data quality needs another pass.
   - `PIVOT`: the claim set should change.
6. Update `PROGRESS.md` with the decision and rationale.

## Output Standard

Every conclusion must cite the exact result artifact it comes from.
