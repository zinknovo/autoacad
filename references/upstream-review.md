# AutoAcad Upstream Review

This file is generated automatically from upstream context plus local AutoAcad files.

Reviewed AutoResearchClaw HEAD: `be4ba4755bf1b52220f25e13b2293b5956590070`
Reviewed AI-Researcher HEAD: `f9a6f8480860c193afff600eeffe3defcee8a978`

# Upstream Comparison Report: AutoAcad vs AutoResearchClaw & AI-Researcher

## Summary

AutoAcad's local package is already well-aligned with both upstream projects in several core areas (evidence discipline, compute budget scaling, anti-fabrication rules). The main gaps are: (1) missing executor selection guidance for domain-specific experiments (HEP, biology, chemistry), (2) no explicit `results.json` output requirement across all stages, and (3) the `ideate` and `plan` stages lack upstream's structured hypothesis-generation and experiment-design YAML requirements. Additionally, the `prepare` stage should incorporate AI-Researcher's reference-codebase evaluation criteria (stars, recency, README quality) and the `export` stage should align with upstream's final formatting requirements.

## Recommended File Updates

---

### `references/pipeline.md`

**Add Executor Selection Section (from AutoResearchClaw v0.5.0)**

Append after the "Loop Points" section:

```markdown
## Executor Selection

Auto-select the domain executor from the research domain when available:
- ML: sandbox with numpy/stdlib (no torch/tensorflow unless user requires)
- High-energy physics: ColliderAgent simulation chain (Lagrangian → FeynRules → MadGraph5 → Delphes)
- Biology: COBRApy genome-scale metabolic modelling
- Statistics: simulation-study agent
- Chemistry/materials: generic Docker executor with domain-specific images
- If no domain executor applies, fall back to the ML sandbox or generic executor

Record executor choice in PROGRESS.md alongside experiment metadata.
```

---

### `references/experiment-rules.md`

**Add Domain-Specific Scaling Patterns (from AutoResearchClaw v0.5.0)**

Append to the existing "Domain-Specific Scaling Patterns" section:

```markdown
- For high-energy physics: leverage domain executors (ColliderAgent, MadGraph5, Delphes) for simulation-based experiments; budget scaling applies to simulation steps.
- For biology: use COBRApy for genome-scale metabolic modelling; scale reaction/enzyme conditions rather than trial seeds.
- For statistics: use simulation-study patterns; scale by number of Monte Carlo replicates, reducing seeds when budget is tight.
- For chemistry and materials: use generic Docker executor with domain-specific images; budget scaling is mandatory.
```

**Strengthen Results-saving Requirement (from AutoResearchClaw prompts)**

Modify the "Result Saving" section to match upstream's mandatory format:

```markdown
- **Mandatory output format:** `main.py` must print metric lines as `name: value` (one per line) AND write a `results.json` file with structured experiment results (e.g. per-algorithm, per-function, per-dimension metrics as nested dicts/lists).
```

*Current text says "Save machine-readable outputs in `results/`" without specifying the required format — align with upstream.*

---

### `references/restricts.md`

**Add Code Anti-Patterns Detail (from AutoResearchClaw prompts.default.yaml)**

Expand the "Code Generation Rules" section to explicitly include:

```markdown
- FORBIDDEN: subprocess, os.system, eval, exec, shutil, socket
- If you report convergence_rate, define it as iterations_to_convergence / max_iterations — it MUST differ between algorithms
- Do NOT run a fixed number of iterations without any convergence check
- Do NOT use `random.uniform()` to simulate a decreasing loss curve
```

*Current text has these but they're scattered — consolidate into a single `### Code Anti-Patterns` block following upstream's explicit list.*

---

### `prepare/SKILL.md`

**Add Reference Codebase Evaluation Criteria (from AI-Researcher prepare_agent.py)**

Add a "Reference Selection Criteria" section:

```markdown
## Reference Codebase Selection Criteria

When identifying reference codebases during preparation:
1. Repositories with more stars are more recommended.
2. Repositories created more recently are more recommended; [IMPORTANT] too old repositories are not recommended.
3. More detailed `README.md` files mean more readable codebases and more reproducible, so more recommended.
4. More clear code structure, code comments, and inline code explanations mean more readable and maintainable, so more recommended.
5. Prefer repositories with `python` language and local-machine execution over Docker; prefer `pytorch` framework for deep learning projects.

Select at least 5 reference codebases. The decision should be as accurate as possible, with as few repositories as needed.
```

---

### `ideate/SKILL.md`

**Add Hypothesis Generation Requirements (from AutoResearchClaw prompts.default.yaml)**

Strengthen the ideation stage with falsifiability structure:

```markdown
## Hypothesis Requirements

Generate at least 2 falsifiable hypotheses from synthesis.
For each hypothesis, provide:
- Rationale
- Measurable prediction
- Failure condition

Format as structured markdown. Hypotheses MUST be testable against the experiment design from the plan stage.
```

---

### `plan/SKILL.md`

**Add Experiment Design YAML Requirements (from AutoResearchClaw prompts.default.yaml)**

Update the planning stage to require structured output:

```markdown
## Experiment Plan Format

Design an experiment plan as YAML with these required keys:
- objectives
- datasets
- baselines
- proposed_methods
- ablations
- metrics
- risks
- compute_budget
```

---

### `run/SKILL.md`

**Add Code Generation Requirements (from AutoResearchClaw prompts.default.yaml)**

Strengthen the run stage with upstream's code-generation constraints:

```markdown
## Code Generation Rules

When generating experiment code:
1. Implement REAL algorithms (e.g., gradient descent, Adam, SGD) using numpy arrays — NOT `random.uniform()` loops that fake results.
2. Define REAL objective/loss functions (e.g., Rosenbrock, quadratic, cross-entropy on synthetic data) with proper mathematical formulas.
3. Run REAL optimization loops that compute gradients and update parameters.
4. Collect REAL metrics (loss values, convergence rates) from actual optimization.
5. Use convergence stopping criteria (stop when objective change < 1e-8 for N consecutive iterations) — do NOT run fixed iteration counts.
6. `main.py` must print metric lines as `name: value` (one per line) AND write a `results.json` file with structured experiment results.
7. Use deterministic seeds (`numpy.random.seed` or `random.seed`).
```

---

### `export/SKILL.md`

**Add Publication Formatting Requirements (from AutoResearchClaw prompts.default.yaml)**

Align export with upstream formatting expectations:

```markdown
## Formatting Requirements

- Format revised paper into clean final markdown for publication export.
- Preserve content quality and readability.
- Ensure numeric claims match `results.json` exactly — run `check_results_vs_claims.py` before export.
- Verify all citations resolve to real papers (DOI, arXiv ID, URL).
```

---

### `draft/SKILL.md`

**Add Figure 1 Planning Requirement (from AutoResearchClaw paper-structure guidance)**

Strengthen the drafting stage with upstream's figure-first discipline:

```markdown
## Drafting Discipline

- Figure 1 must be planned before full drafting
- Every effective component mentioned in the paper needs an ablation
- Baselines must receive comparable tuning effort
- Citations must support claims, not decorate them
```

*Current `references/paper-structure.md` already has these — ensure draft/SKILL.md references it explicitly.*

---

## No-Change Areas

The following files/sections already meet or exceed upstream standards and require no updates:

| File/Area | Reason |
|-----------|--------|
| **`references/experiment-rules.md` — Pilot and Time Budget** | Already contains all mandatory scaling rules, time estimates, and guard logic from AutoResearchClaw. |
| **`references/restricts.md` — Topic Lock & Anti-Fabrication** | Fully aligned with upstream's hard constraints; includes additional NumPy 2.x compatibility rules. |
| **Overall SKILL.md — Compute Budget Rules** | Already matches upstream's budget-scaling guidance (reduce seeds, limit steps, time guard). |
| **Stage routing table** | Correctly maps all 9 AutoAcad stages to upstream's 25-stage pipeline; no routing gaps. |
| **`review/SKILL.md`** | No upstream-specific requirements; AutoAcad's review stage already covers evidence-consistency checking and reviewer simulation beyond upstream. |
| **`analyze/SKILL.md`** | Upstream doesn't specify unique analyze-stage requirements beyond what AutoAcad already implements (proceed/refine/pivot decisions). |
| **`survey/SKILL.md`** | Already aligned with upstream's literature collection and screening requirements. |
| **`references/paper-structure.md`** | Already includes upstream's section budgets and quality gates; no changes needed. |

---

## Implementation Priority

Implement changes in this order:
1. **`references/experiment-rules.md`** — Add mandatory `results.json` format (critical for reproducibility)
2. **`references/pipeline.md`** — Add executor selection (needed by run stage)
3. **`prepare/SKILL.md`** — Add reference codebase criteria (foundational for project setup)
4. **`ideate/SKILL.md`** and **`plan/SKILL.md`** — Add structured hypothesis/experiment-plan formats
5. **`run/SKILL.md`** — Strengthen code generation rules
6. **`export/SKILL.md`** and **`draft/SKILL.md`** — Final alignment with upstream formatting
