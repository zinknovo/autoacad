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

## NumPy 2.x Compatibility Notes

- Use `np.trapezoid` instead of `np.trapz`.
- Use `scipy.special.erfinv` instead of `np.erfinv`.
- Use Python built-in scalar types instead of removed NumPy aliases.
- Use `math` instead of `np.math`.

## Result Saving

- Save machine-readable outputs in `results/`.
- Keep enough metadata to reproduce the final table: seeds, configs, hardware, runtime, commit or version marker if available.

## Code Anti-Patterns (for experiment code)

- Do NOT generate random numbers and pretend they are experiment results.
- Do NOT use `random.uniform()` to simulate a decreasing loss curve.
- Do NOT hardcode metric values or use trivial arithmetic as metrics.
- Do NOT run a fixed number of iterations without any convergence check.
- Do NOT implement convergence_rate or similar metrics as dummy return values.

## Domain-Specific Scaling Patterns

- For ML experiments (default): follow the budget-scaling rules above; use numpy/stdlib for rapid prototyping before framework-specific implementation.
- For high-energy physics: leverage domain executors (ColliderAgent, MadGraph5, Delphes) for simulation-based experiments; budget scaling applies to simulation steps.
- For biology: use COBRApy for genome-scale metabolic modelling; scale reaction/enzyme conditions rather than trial seeds.
- For statistics: use simulation-study patterns; scale by number of Monte Carlo replicates, reducing seeds when budget is tight.
- For other domains (chemistry, materials): use generic Docker executor with domain-specific images; budget scaling is mandatory.