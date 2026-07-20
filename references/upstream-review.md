# AutoAcad Upstream Review

This file is generated automatically from upstream context plus local AutoAcad files.

Reviewed AutoResearchClaw HEAD: `e2e23c93b4943fd21cc531deb09850d8fda55357`
Reviewed AI-Researcher HEAD: `f9a6f8480860c193afff600eeffe3defcee8a978`

## Summary

The upstream systems (AutoResearchClaw and AI-Researcher) have evolved in several important ways that your local AutoAcad package should track. AutoResearchClaw v0.5.0 introduces multi-domain experiment agents (HEP, biology, statistics) and the ARC-Bench benchmark (55 topics), while AI-Researcher adds a reference-codebase-driven preparation phase and automated algorithm validation/refinement. However, AutoAcad already has strong scaffolding for these concepts. The updates needed are incremental—primarily adding domain-specific executor routing to `experiment-rules.md` and aligning `pipeline.md` with the new upstream stage structures—not a full rewrite.

---

## Recommended File Updates

### references/experiment-rules.md

**Add a new top-level section before "Code Anti-Patterns":**

```markdown
## Domain-Specific Scaling Patterns

- For ML experiments (default): follow the budget-scaling rules above; use numpy/stdlib for rapid prototyping before framework-specific implementation.
- For high-energy physics: leverage domain executors (ColliderAgent, MadGraph5, Delphes) for simulation-based experiments; budget scaling applies to simulation steps.
- For biology: use COBRApy for genome-scale metabolic modelling; scale reaction/enzyme conditions rather than trial seeds.
- For statistics: use simulation-study patterns; scale by number of Monte Carlo replicates, reducing seeds when budget is tight.
- For other domains (chemistry, materials): use generic Docker executor with domain-specific images; budget scaling is mandatory.
```

**Why:** AutoResearchClaw v0.5.0 added multi-domain experiment agents covering HEP, biology, and statistics. Without explicit scaling guidance for these domains, AutoAcad will default to ML-style seed reductions that are inappropriate for simulation-based domains. This addition keeps your package aligned with upstream capability without changing existing ML rules.

### references/pipeline.md

**In the "Stage Groups" table, add a new group before "H. Finalization":**

| Group | Stages | Goal |
| --- | --- | --- |
| I. External scrutiny | third-party review, rebuttal | Simulate harsh review and respond. |

**Why:** AutoResearchClaw's HITL system (v0.4.0) and AI-Researcher's automated result analysis both push toward an explicit external-review stage. Your pipeline currently ends at finalization. Adding this group makes the loop explicit (analysis → review → refine/pivot) and matches the upstream emphasis on stress-testing methodology-evidence consistency.

**In "Loop Points", add after "After analysis:":**

```markdown
- After rebuttal review: either refine experiments or restructure the paper.
```

**Why:** AI-Researcher's algorithm validation/refinement pattern requires a documented loop point after external scrutiny. Without this, reviewers who identify methodology gaps have no defined path back to experiment design.

### references/restricts.md

**Under "Topic Lock", add a subsection before "Evidence Discipline":**

```markdown
- **Hard Topic Constraint:** The paper MUST be about the specified topic.
- **Prohibited content (unless user explicitly specifies case-study mode):**
  - Do NOT treat environment setup, dependency installation, or infrastructure failures as a research contribution.
  - Do NOT present debugging logs, system errors, or configuration issues as experimental findings.
  - Do NOT drift to tangential topics not directly related to the stated topic.
  - Every section MUST connect back to the core research question.
  - The Abstract and Introduction MUST clearly state the research problem derived from the topic.
  - The Method section MUST describe a technical approach, not a workflow.
  - The Results section MUST report quantitative outcomes of experiments, not environment status.
```

**Why:** AutoResearchClaw's `topic_constraint` block (in `prompts.default.yaml`) explicitly lists these prohibitions. Your current `restricts.md` only says "Keep every section tied to the paper's actual research question" and "Do not present setup work...as research contributions." The upstream has much stronger, more specific guardrails against topic drift and infrastructure-as-contribution. This change aligns your hard constraints with theirs without changing the anti-fabrication rules you already have.

### prepare/SKILL.md

**Add to "Operating Rules" or "Input Requirements":**

```markdown
- If reference codebases are provided, verify they exist, have README files, and are compatible with Python 3.11+. Skip repositories that are archived, unmaintained, or have fewer than 10 stars unless domain-specific.
- If no reference codebases are provided but reference papers are, search GitHub for matching repositories and evaluate at least 5 before selecting 2-4 for detailed review.
```

**Why:** AI-Researcher's preparation agent (`prepare_agent.py`) systematically evaluates GitHub repositories (stars, recency, README quality, code structure). AutoAcad's `prepare` stage currently has no guidance for repository evaluation. This addition lets the stage handle the reference-based ideation mode from AI-Researcher Level 2 ("I have some reference papers, please come up with an innovative idea...").

---

## No-Change Areas

The following files are already well-aligned with upstream structure and do not need updates:

- **references/paper-structure.md** — Your word budgets, section goals, and drafting order match or exceed what upstream provides. No change needed.

- **survey/SKILL.md** — No upstream changes to literature collection or screening methodology.

- **ideate/SKILL.md** — Hypothesis generation patterns are stable across all three systems.

- **plan/SKILL.md** — Experiment design requirements are already covered by your `experiment-rules.md` and `pipeline.md`.

- **run/SKILL.md** — Experiment execution rules are handled by `experiment-rules.md`, which you are updating.

- **analyze/SKILL.md** — Result analysis patterns are generic enough that no upstream-specific additions are needed.

- **draft/SKILL.md** — Drafting instructions remain consistent across AutoResearchClaw and AI-Researcher.

- **review/SKILL.md** — Review mechanics (methodology-evidence consistency, reviewer objections) are already encoded.

- **export/SKILL.md** — Export formatting is a finalization step with no upstream changes.
