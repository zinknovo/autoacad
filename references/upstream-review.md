# AutoAcad Upstream Review

This file is generated automatically from upstream context plus local AutoAcad files.

Reviewed AutoResearchClaw HEAD: `5dc7fcc859a1b4ecddd871aca552d4d22517b768`
Reviewed AI-Researcher HEAD: `f9a6f8480860c193afff600eeffe3defcee8a978`

# AutoAcad vs. Upstreams Comparison Report

## Summary

The local AutoAcad package shows strong alignment with upstream research automation principles from both AutoResearchClaw and AI-Researcher, but with notable differences in implementation focus. AutoAcad is structured as a **modular skill package** for Claude, emphasizing stage-gated workflows and reproducibility checks, while the upstream projects are **full autonomous research systems** with broader infrastructure.

Key differences:
- **AutoResearchClaw** provides a complete 23-stage pipeline with HITL co-pilot systems, multi-agent subsystems, and sandboxed execution
- **AI-Researcher** focuses on autonomous scientific discovery with two input modes (detailed ideas vs. reference-based ideation)
- **AutoAcad** distills these into a lightweight, skill-based approach with strict evidence discipline and paper-structure rules

## Recommended File Updates

### 1. `references/pipeline.md`
**Add HITL intervention modes** from AutoResearchClaw:
```markdown
## Human-in-the-Loop Modes (Optional)
AutoAcad supports 6 intervention modes when used with co-pilot systems:
- `full-auto`: No human intervention (default)
- `gate-only`: Human approval required at stage gates
- `checkpoint`: Human review at major milestones
- `step-by-step`: Human approval per stage
- `co-pilot`: Real-time collaboration
- `custom`: User-defined intervention points
```

**Add pipeline branching** for parallel hypothesis exploration (from AutoResearchClaw HITL):
```markdown
## Parallel Exploration
When evidence suggests multiple viable directions, create pipeline branches:
- Branch at: hypothesis_gen, experiment_design, or analysis stages
- Track branches in `PROGRESS.md` with `branch: <name>` labels
- Merge or prune based on comparative results
```

### 2. `references/experiment-rules.md`
**Add complexity scoring and fallback** from AutoResearchClaw's OpenCode integration:
```markdown
## Code Generation Complexity Management
- Score code complexity before generation (simple: <100 lines, medium: 100-500, complex: >500)
- For complex implementations, consider using specialized code generation backends
- Implement graceful fallback: if complex generation fails, simplify the approach rather than halting
```

**Add anti-fabrication diagnostics** from AutoResearchClaw v0.3.2:
```markdown
## Experiment Diagnosis & Repair
When experiments fail:
1. Run diagnosis loop: check for NaN/Inf sources, convergence failures, memory issues
2. Implement repair strategies: adjust learning rates, add numerical stability terms
3. If repair fails after 3 attempts, trigger refine or pivot decision
```

### 3. `prepare/SKILL.md`
**Add reference-based ideation path** from AI-Researcher Level 2:
```markdown
## Reference-Based Preparation
When user provides papers without specific ideas:
1. Analyze reference papers for patterns, gaps, and combinable elements
2. Generate novel research concepts by synthesizing across references
3. Select 3-5 most promising directions based on feasibility and novelty
4. Proceed with the strongest candidate while tracking alternatives
```

**Add repository selection criteria** from AI-Researcher's prepare_agent:
```markdown
## Codebase Selection Criteria
When choosing reference implementations:
1. Prefer repositories with more stars (community validation)
2. Prefer recent repositories (avoid deprecated dependencies)
3. Prefer detailed README.md (reproducibility)
4. Prefer clear code structure with comments (maintainability)
5. Prefer Python implementations, especially PyTorch for DL
6. Select 5-8 repositories maximum to avoid cognitive overload
```

### 4. `run/SKILL.md`
**Add time budget scaling rules** from AutoResearchClaw prompts.default.yaml:
```markdown
## Compute Budget Scaling (Mandatory)
- If total conditions > 100: reduce seeds to 3-5 (not 20)
- If total conditions > 500: reduce to 2-3 representative conditions per factor
- If time_budget < 300s: limit total optimization steps to ≤5,000 per run
- If time_budget < 120s: limit total optimization steps to ≤1,000 per run
- Always print intermediate results so partial data is captured on timeout
```

### 5. `export/SKILL.md`
**Add publication formatting standards** from AutoResearchClaw export_publish stage:
```markdown
## Final Formatting Requirements
- Convert revised paper into clean markdown for publication export
- Preserve all citations, figures, and mathematical notation
- Ensure consistent heading hierarchy and formatting
- Verify all cross-references (figures, tables, sections) are correct
- Include metadata: title, authors, abstract, keywords
```

## No-Change Areas

### 1. `references/restricts.md`
**No changes needed** - AutoAcad's constraints are stricter and more focused than upstreams:
- Topic lock is more explicit than AutoResearchClaw's topic_constraint
- Evidence discipline aligns with both upstreams but is more concisely stated
- Anti-fabrication rules are comprehensive and appropriate for skill-based use

### 2. `references/paper-structure.md`
**No changes needed** - AutoAcad's structure is more detailed and practical:
- Word budgets per section provide concrete guidance missing in upstreams
- Drafting order is well-optimized for research writing
- Core paper rules (Figure 1, ablations, baseline tuning) are essential and correct

### 3. Stage-specific SKILL.md files (`survey/`, `ideate/`, `plan/`, `analyze/`, `draft/`, `review/`)
**No structural changes needed** - These already capture the essential workflows:
- Stage purposes are clearly defined and match upstream intentions
- Operating rules integrate well with the reference documents
- The modular approach works better for skill-based usage than the full pipeline implementations

### 4. Core package structure
**No changes needed** - AutoAcad's skill-based approach is appropriate:
- Bundled resources (templates, scripts, references) are comprehensive
- The stage-gated workflow with PROGRESS.md tracking is effective
- The skill decomposition allows targeted use without requiring full pipeline execution

**Rationale**: AutoAcad successfully distills the complex upstream systems into a usable skill package. The recommended updates add valuable features from upstreams without compromising AutoAcad's focused, evidence-based approach. The no-change areas represent strengths where AutoAcad's implementation is already superior or appropriately simplified for its use case.
