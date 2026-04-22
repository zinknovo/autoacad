# AutoAcad Experiment Rules

## Pilot and Time Budget

- Run one small pilot before the main loop.
- Print `TIME_ESTIMATE: <seconds>` or equivalent before scaling.
- If total conditions explode, reduce seeds or shrink the grid rather than pretending everything ran.
- Add a time guard that saves partial results before budget exhaustion.
- **Compute Budget Constraint:**
  - Total execution time limit: respect user-specified time budget.
  - Design experiments that complete within this budget.
  - **Scaling Rules (mandatory):**
    - If total conditions > 100: reduce seeds to 3-5 (not 20).
    - If total conditions > 500: reduce to 2-3 representative conditions per factor.
    - If time_budget < 300s: limit total optimization steps to ≤5,000 per run.
    - If time_budget < 120s: limit total optimization steps to ≤1,000 per run.
    - Always print intermediate results so partial data is captured on timeout.
  - **Mandatory:** print a "TIME_ESTIMATE: Xs" line before the main loop, estimating total runtime based on a small pilot (run 1 condition, extrapolate).
  - **Mandatory:** implement a time guard — check elapsed time periodically and stop gracefully if approaching 80% of budget, saving all results collected so far.

## Numerical Discipline

- Implement real objective functions and real update rules.
- Implement convergence checks based on objective or parameter change.
- When NaN or Inf appears, identify the source: learning rate, normalization, zero division, overflow, unstable log, and so on.
- Do not hide instability with blanket `try/except`, `nan_to_num`, or silent clipping unless that is the actual documented method.

## Result Saving

- Save machine-readable outputs in `results/`.
- Keep enough metadata to reproduce the final table: seeds, configs, hardware, runtime, commit or version marker if available.

## NumPy Compatibility Notes

- Use `np.trapezoid` instead of `np.trapz`.
- Use `scipy.special.erfinv` instead of `np.erfinv`.
- Use Python built-in scalar types instead of removed NumPy aliases.
- Use `math` instead of `np.math`.
