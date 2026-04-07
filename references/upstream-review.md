# AutoAcad Upstream Review

Generated: 2026-04-07T21:57:17.196257+00:00

This file is generated automatically from upstream context plus local AutoAcad files.

# AutoAcad vs. Upstreams Comparison Report

## Summary

The local AutoAcad package maintains a well-structured, stage-gated research workflow that aligns with core principles from both upstream sources but has notable differences in implementation focus. AutoResearchClaw provides a more comprehensive autonomous pipeline with 23 stages, multi-agent subsystems, and human-in-the-loop capabilities, while AI-Researcher emphasizes reference-based ideation and codebase analysis. AutoAcad sits between them as a practical, file-based workflow package focused on reproducibility and evidence discipline.

Key alignment areas: staged research process, anti-fabrication rules, experiment discipline, and paper structure guidance. Key divergence: AutoAcad lacks the autonomous execution infrastructure and multi-agent orchestration present in both upstreams.

## Recommended File Updates

### references/pipeline.md
**Add from AutoResearchClaw:**
- Expand stage groups from 9 to match the 23-stage pipeline (topic_init through export_publish)
- Include explicit loop points after experiment_run and analysis stages
- Add gate semantics for literature_screen, experiment_design, and quality_gate
- Reference the "PROCEED/REFINE/PIVOT" decision framework from analysis stage

**Add from AI-Researcher:**
- Clarify the two input modes: detailed idea description vs. reference-based ideation
- Add preparation stage that includes codebase analysis and repository selection criteria

### references/restricts.md
**Enhance from AutoResearchClaw prompts.default.yaml:**
- Strengthen the "HARD TOPIC CONSTRAINT" section with explicit prohibitions:
  - "Do NOT treat environment setup, dependency installation, or infrastructure failures as a research contribution"
  - "Do NOT present debugging logs, system errors, or configuration issues as experimental findings"
  - "Every section MUST connect back to the core research question"
- Add compute budget constraints with scaling rules for different time budgets

### references/experiment-rules.md
**Update from AutoResearchClaw:**
- Add explicit compute budget scaling rules:
  - "If total conditions > 100: reduce seeds to 3-5 (not 20)"
  - "If total conditions > 500: reduce to 2-3 representative conditions per factor"
  - Time budget thresholds for optimization steps (≤5,000 steps for <300s, ≤1,000 steps for <120s)
- Mandate TIME_ESTIMATE printing before main loops
- Require time guard implementation that saves partial results at 80% budget
- Clarify sandbox package restrictions (numpy + stdlib only for certain modes)

### prepare/SKILL.md
**Incorporate from AI-Researcher prepare_agent.py:**
- Add repository selection criteria:
  1. Stars count as popularity indicator
  2. Recency (avoid too old repositories)
  3. Detailed README.md for reproducibility
  4. Clear code structure and comments
  5. Python preference with local execution over Docker
  6. PyTorch preference for deep learning projects
- Include guidance for analyzing 5-8 repositories before final selection
- Add tools for code structure analysis and file reading during preparation

### survey/SKILL.md
**Add from AutoResearchClaw:**
- Include literature screening gate criteria
- Emphasize DOI/arXiv ID preservation for all collected papers
- Add thematic comparison requirements for positioning in related work

### ideate/SKILL.md
**Enhance from both upstreams:**
- Add hypothesis generation format: rationale, measurable prediction, failure condition
- Include both modes: detailed idea description vs. reference-based ideation
- Emphasize falsifiability of all hypotheses

### run/SKILL.md
**Update from AutoResearchClaw:**
- Add anti-fabrication system references
- Include experiment diagnosis and repair loop
- Reference convergence checking requirements
- Add result saving with complete metadata (seeds, configs, hardware, runtime, version markers)

### draft/SKILL.md
**Enhance from AutoResearchClaw:**
- Add paper quality audit references (AI-slop detection, 7-dim review scoring)
- Include NeurIPS checklist consideration
- Emphasize claim-evidence consistency checking

## No-Change Areas

### references/paper-structure.md
The existing structure with word budgets, section purposes, and drafting order is comprehensive and aligns well with both upstreams. The target word counts and section purposes are more detailed than what's provided in the upstream snippets.

### analyze/SKILL.md
The existing focus on metrics interpretation, proceed/refine/pivot decisions, and evidence gap identification is sufficient and aligns with both upstream analysis approaches.

### review/SKILL.md
The stress-testing of methodology-evidence consistency and reviewer objection simulation is adequately covered and doesn't require updates from the provided upstream content.

### export/SKILL.md
The final package preparation, citations, archive, and export checks are well-defined and don't need updates from the limited upstream export_publish prompt.

### plan/SKILL.md
The experiment design, baselines, ablations, and project structure planning are adequately covered in the existing skill and align with AutoResearchClaw's experiment_design stage.

### The core SKILL.md package root
The routing table, operating rules, and bundled resources structure is effective and provides clear stage-based navigation. The layered approach (subskills for stages, root for end-to-end) is a good design that doesn't need fundamental changes.

**Note**: The upstreams show extensive infrastructure (Docker sandboxes, multi-agent systems, CLI tools, HITL interfaces) that AutoAcad deliberately omits as it focuses on the workflow layer rather than execution infrastructure. This is a design choice rather than a gap.
