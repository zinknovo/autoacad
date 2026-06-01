# AutoAcad Upstream Review

This file is generated automatically from upstream context plus local AutoAcad files.

Reviewed AutoResearchClaw HEAD: `e040e1dd9afcbda017f72181788a861e2e64d70c`
Reviewed AI-Researcher HEAD: `f9a6f8480860c193afff600eeffe3defcee8a978`

# AutoAcad Upstream Comparison Report

## Summary

AutoAcad is well-aligned with both upstream systems in its core philosophy of staged, iterative research with evidence discipline. The main gaps are concentrated in:

1. **Multi-domain executor support** — both upstreams have added domain-specific experiment agents (HEP, biology, statistics) that AutoAcad lacks
2. **Human-in-the-Loop (HITL) modes** — AutoResearchClaw v0.4.0 added rich intervention modes and co-pilot capabilities
3. **Anti-fabrication verification** — AutoResearchClaw added a VerifiedRegistry system for claim verification
4. **Additional script/automation utilities** — both upstreams have more mature tooling ecosystems

No structural redesign is needed — the gaps are additive rather than architectural.

---

## Recommended File Updates

### survey/SKILL.md
**Add:** Domain-specific survey strategies (HEP, biology, statistics)  
**Why:** Both upstreams now route to domain specialists; survey preparation should acknowledge domain-specific paper sources (e.g., InspireHEP, PubMed, arXiv category tags).  
**Add a sentence** like: "For non-ML domains (HEP, biology, statistics), adapt search strategy to domain-specific venues and preprint servers (InspireHEP, PubMed, bioRxiv)."

### ideate/SKILL.md
**Add:** HITL-style hypothesis co-creation guidance  
**Why:** AutoResearchClaw v0.4.0 added "Idea Workshop" for hypothesis co-creation; AutoAcad's ideate stage should acknowledge that human-in-the-loop ideation is an option.  
**Add a line** in Operating Rules: "If user desires collaborative ideation, support hypothesis refinement through iterative narrowing with user feedback."

### plan/SKILL.md
**Add:** Compute budget scaling rules (already present in experiment-rules.md, but should be cross-referenced)  
**Why:** The scaling rules are currently only in experiment-rules.md; planners should see them earlier.  
**Change:** Add "Refer to references/experiment-rules.md for compute budget scaling rules before finalizing experiment conditions."

### run/SKILL.md
**Add:** Multi-domain executor awareness and time-guard reinforcement  
**Why:** AutoResearchClaw now has ColliderAgent for HEP, COBRApy for biology, simulation-study agent for statistics; AutoAcad should at minimum note that domain-specific executors may be needed beyond the default sandbox.  
**Change:** Add "Domain-specific executors (e.g., ColliderAgent for HEP, COBRApy for biology) may override default sandbox — check experiment plan for domain requirements." Also reinforce: "Run early pilot to generate TIME_ESTIMATE; implement time guard before main execution."

### analyze/SKILL.md
**Add:** Anti-fabrication verification step  
**Why:** AutoResearchClaw's VerifiedRegistry checks draft claims against experiment results; AutoAcad should add a similar verification gate.  
**Change:** Add at the end: "Before analysis completes, run a claim-evidence consistency check: verify every numerical claim in current draft against recorded results. Flag any unsupported numbers."

### draft/SKILL.md
**Add:** Figure 1 planning requirement (move from paper-structure.md reference into operative SKILL)  
**Why:** The paper-structure.md says "Figure 1 must be planned before full drafting" but this is a high-level reference; the draft SKILL should operationalize it.  
**Change:** Add rule: "Before writing section text, plan Figure 1 content and placement. Define all sub-figures, axis labels, and expected visual patterns."

### review/SKILL.md
**Add:** Third-party review and rebuttal simulation  
**Why:** AutoAcad pipeline.md mentions Stage I (External scrutiny) but review/SKILL.md doesn't mention simulating harsh review or rebuttal.  
**Change:** Add: "After internal review, optionally simulate third-party peer review with focus on methodology gaps and claim overreach. Prepare a rebuttal letter addressing anticipated objections."

### export/SKILL.md
**Add:** Citation verification step and archive preparation  
**Why:** Both upstreams emphasize DOI/arXiv ID preservation and citation verification; AutoAcad has citation_verify in resources but export/SKILL.md doesn't mention it.  
**Change:** Add: "Verify all citations have resolvable DOIs or arXiv IDs. Prepare README with reproduction instructions. Archive results/, plans/, and code/ alongside the final paper."

### references/pipeline.md
**Minor update:** Add "anti-fabrication verification" as a sub-step in the Analysis group  
**Why:** AutoResearchClaw formalized claim verification as a pipeline step; AutoAcad should reflect this.  
**Change:** In Stage F (Analysis), add bullet: "- claim-evidence consistency check: verify all numerical claims against saved results before proceed decision."

---

## No-Change Areas

### references/restricts.md
Already comprehensive. The topic lock, evidence discipline, anti-fabrication rules, and writing discipline match or exceed upstream constraints. No update needed.

### references/experiment-rules.md
Well-aligned with both upstreams. Already includes:
- Pilot and time budget with specific scaling rules
- Numerical discipline (convergence checks, NaN handling)
- NumPy 2.x compatibility notes
- Result saving requirements

### references/paper-structure.md
Target structure and core rules are sound. The drafting order, section word budgets, and ablation requirements align with best practices from both upstreams.

### prepare/SKILL.md
The prepare stage focuses on project inventory — this is lightweight by design. Neither upstream's prepare equivalent introduces material differences that would warrant changes.

### SKILL.md (root)
The routing table and bundled resources list are comprehensive. No structural changes needed — the gaps identified above are additive to sub-skills, not to the root dispatch.
