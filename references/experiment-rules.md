# AutoAcad Experiment Rules

## Pilot and Time Budget

- Run one small pilot before the main loop.
- Print `TIME_ESTIMATE: <seconds>` or equivalent before scaling.
- If total conditions explode, reduce seeds or shrink the grid rather than pretending everything ran.
- Add a time guard that saves partial results before budget exhaustion.

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
