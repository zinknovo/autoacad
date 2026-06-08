# AutoAcad Upstream Review

This file is generated automatically from upstream context plus local AutoAcad files.

Reviewed AutoResearchClaw HEAD: `ea77ec19fefe9198ac1364d2cdb4f9e928cf0705`
Reviewed AI-Researcher HEAD: `f9a6f8480860c193afff600eeffe3defcee8a978`

# AutoAcad vs Upstream Comparison

## Summary

AutoAcad is a streamlined, skill-based research-paper package focused on a clean 9-stage workflow (prepare → export) with strong emphasis on evidence discipline, anti-fabrication, and reproducible experiments. The upstream projects (AutoResearchClaw and AI-Researcher) are significantly more complex systems with autonomous orchestration, multi-agent collaboration, Docker integration, and domain-specific execution agents. AutoAcad's strength lies in its simplicity and modularity as a Claude Code skill package, while the upstreams are full research automation platforms.

## Recommended File Updates

### references/experiment-rules.md
**Add compute budget scaling rules from upstream** — AutoResearchClaw's `prompts.default.yaml` has more detailed time-budget scaling conditions (e.g., `<300s`, `<120s` tiers) and explicit anti-pattern checks that are stronger than the current AutoAcad version.

**Change:** Add explicit `TIME_ESTIMATE` print requirement (you have it partially) and the **mandatory time guard at 80% budget** phrasing from upstream.

### references/restricts.md
**Strengthen NumPy 2.x compatibility section** — Upstream lists additional removed aliases: `np.bool`, `np.int`, `np.float`, `np.complex`, `np.str`, `np.object`. AutoAcad currently only mentions `np.trapezoid`, `erfinv`, and `np.math`.

**Change:** Add the full list of removed NumPy numeric type aliases to match upstream's stricter compatibility enforcement.

### prepare/SKILL.md
**Add reference codebase discovery guidance** — AI-Researcher's `Prepare Agent` has structured logic for evaluating GitHub repositories (stars, recency, README quality, code clarity, Python/PyTorch preference). AutoAcad's prepare stage currently lacks this.

**Change:** Add a "Reference Codebase Evaluation" subsection with criteria for assessing existing codebases.

### run/SKILL.md
**Add pilot-run discipline** — AutoResearchClaw requires running one small pilot before the main experiment loop. AutoAcad's `experiment-rules.md` mentions it, but `run/SKILL.md` doesn't explicitly require it in its stage instructions.

**Change:** Add "Run 1 small pilot condition before scaling to full experiment grid" as an explicit step.

### analyze/SKILL.md
**Add research decision framing** — AutoResearchClaw's pipeline has explicit `PROCEED/REFINE/PIVOT` decision gates after analysis. AutoAcad's pipeline.md mentions these, but `analyze/SKILL.md` should surface them more prominently.

**Change:** Add a "Research Decision" subsection with the three outcomes and criteria for each, connecting to the loop points in `pipeline.md`.

## No-Change Areas

- **references/pipeline.md** — Comprehensive and matches upstream stage groupings; no changes needed.
- **references/paper-structure.md** — Well-defined target word counts and section purposes; upstream doesn't add structurally different guidance.
- **survey/SKILL.md** — Adequate for the skill-based approach; upstream's search strategy doesn't warrant changes.
- **ideate/SKILL.md** — Sufficient; upstream's hypothesis generation is similar.
- **plan/SKILL.md** — Appropriate for AutoAcad's scope; upstream's experiment design detail is overly complex for this package.
- **draft/SKILL.md** — Good alignment with paper structure rules.
- **review/SKILL.md** — Strong evidence-consistency checks already present.
- **export/SKILL.md** — Adequate finalization guidance.

The package's core identity as a lightweight skill system (rather than a full autonomous pipeline) is well-maintained. The recommended changes are targeted additions that strengthen existing rules without bloating the package or shifting its design philosophy.
