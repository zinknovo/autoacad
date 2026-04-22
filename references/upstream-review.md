# AutoAcad Upstream Review

This file is generated automatically from upstream context plus local AutoAcad files.

Reviewed AutoResearchClaw HEAD: `684ddb223d33fc485bad87be135abc29427da048`
Reviewed AI-Researcher HEAD: `f9a6f8480860c193afff600eeffe3defcee8a978`

# AutoAcad vs. Upstreams Comparison

## Summary

The local AutoAcad package shows strong alignment with upstream principles from both AutoResearchClaw and AI-Researcher, but lacks some specific technical constraints and implementation details from the upstreams. AutoAcad excels at providing a structured, stage-gated research workflow with clear documentation, but could benefit from incorporating more concrete experiment rules, compute budget management, and topic constraint enforcement from the upstreams.

Key differences:
- **AutoResearchClaw** provides detailed compute budget constraints, sandbox package restrictions, and anti-fabrication systems
- **AI-Researcher** offers sophisticated codebase analysis and reference integration workflows
- **AutoAcad** maintains cleaner stage separation and documentation but lacks some implementation specifics

## Recommended File Updates

### 1. `references/experiment-rules.md`
**Add compute budget constraints from AutoResearchClaw:**
```markdown
## Compute Budget Management
- Total execution time limit must be estimated and respected
- Implement scaling rules:
  - If total conditions > 100: reduce seeds to 3-5 (not 20)
  - If total conditions > 500: reduce to 2-3 representative conditions per factor
  - If time_budget < 300s: limit total optimization steps to ≤5,000 per run
  - If time_budget < 120s: limit total optimization steps to ≤1,000 per run
- Always print `TIME_ESTIMATE: <seconds>` line before main loop based on pilot run
- Implement time guard: check elapsed time periodically and stop gracefully at 80% of budget, saving partial results
```

**Add sandbox package restrictions:**
```markdown
## Package Constraints (Sandbox Mode)
Available packages: Python stdlib, numpy, math, random, statistics, json
Do NOT use: torch, tensorflow, jax, sklearn, pandas, scipy, matplotlib, or any deep learning framework
Write experiments using ONLY numpy and stdlib unless explicitly permitted
```

### 2. `references/restricts.md`
**Strengthen topic constraint from AutoResearchClaw prompts:**
```markdown
## Hard Topic Constraint
- The paper MUST be about the stated research topic
- PROHIBITED content (unless user explicitly specifies case-study mode):
  - Do NOT treat environment setup, dependency installation, or infrastructure failures as research contributions
  - Do NOT present debugging logs, system errors, or configuration issues as experimental findings
  - Do NOT drift to tangential topics not directly related to the stated topic
- Every section MUST connect back to the core research question
- The Abstract and Introduction MUST clearly state the research problem
- The Method section MUST describe a technical approach, not a workflow
- The Results section MUST report quantitative outcomes of experiments, not environment status
```

### 3. `prepare/SKILL.md`
**Add reference codebase analysis from AI-Researcher:**
```markdown
## Reference Codebase Selection Criteria
When analyzing existing repositories for reference:
1. Repositories with more stars are more recommended
2. Repositories created more recently are more recommended (too old repositories are not recommended)
3. More detailed `README.md` file means more readable codebase and more reproducible
4. More clear code structure, code comments, and inline code explanations mean more readable and maintainable
5. Prefer repositories with `python` language, running locally rather than in docker
6. For deep learning projects, prefer `pytorch` framework
7. Choose at least 5 repositories as reference codebases when available
```

### 4. `run/SKILL.md`
**Add convergence and stability requirements from AutoResearchClaw:**
```markdown
## Algorithm Implementation Requirements
- Implement REAL algorithms (e.g., gradient descent, Adam, SGD) using numpy arrays
- Define REAL objective/loss functions with proper mathematical formulas
- Run REAL optimization loops that compute gradients and update parameters
- MUST implement convergence stopping criteria (e.g., stop when objective change < 1e-8 for N consecutive iterations)
- Do NOT just run a fixed number of iterations without convergence check
- If reporting convergence_rate, define it as iterations_to_convergence / max_iterations
```

## No-Change Areas

### 1. `references/pipeline.md`
The 25-stage loop structure with stage groups and gate semantics is comprehensive and well-aligned with both upstreams. The loop points (PROCEED/REFINE/PIVOT) and minimum cycle discipline are appropriate.

### 2. `references/paper-structure.md`
The target structure with word budgets, core paper rules, and drafting order is well-defined and doesn't require updates from upstreams.

### 3. `survey/SKILL.md`, `ideate/SKILL.md`, `plan/SKILL.md`
These stage skills maintain appropriate separation of concerns and don't need structural changes from upstream inputs.

### 4. `analyze/SKILL.md`, `draft/SKILL.md`, `review/SKILL.md`, `export/SKILL.md`
These implementation-focused skills are sufficiently detailed and don't require updates from the provided upstream snippets.

### 5. Core SKILL.md structure
The route-by-stage table, operating rules, and bundled resources in the main SKILL.md are well-organized and don't need restructuring. The stage separation logic is clear and effective.

**Note**: The upstreams show extensive additional systems (HITL co-pilot, MetaClaw integration, multi-agent subsystems) that are beyond the scope of AutoAcad's current lightweight package design. These represent architectural differences rather than gaps requiring updates.
