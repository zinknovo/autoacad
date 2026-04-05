# AutoAcad Pipeline

AutoAcad uses a staged loop, not a straight line. The purpose of the pipeline is to make it obvious when to keep moving and when to go back.

## Stage Groups

| Group | Stages | Goal |
| --- | --- | --- |
| A. Definition | topic init, problem decompose | Define scope and research questions. |
| B. Literature | search strategy, collect, screen, extract | Build a real evidence base. |
| C. Synthesis | synthesis, hypothesis gen, theoretical bounds | Turn papers into falsifiable claims. |
| D. Design | experiment design, code generation, resource planning | Specify the evaluation program. |
| E. Execution | experiment run, iterative refine | Produce reproducible results. |
| F. Analysis | result analysis, research decision | Choose proceed, refine, or pivot. |
| G. Writing | outline, draft, peer review, revision | Convert evidence into a paper. |
| H. Finalization | quality gate, archive, export, citation verify | Prepare the final package. |
| I. External scrutiny | third-party review, rebuttal | Simulate harsh review and respond. |

## Gate Semantics

- `literature_screen`: stop if the shortlist is weak or off-topic.
- `experiment_design`: stop if baselines, ablations, or metrics are under-specified.
- `quality_gate`: stop if claims outrun evidence or if the paper is materially under-developed.

## Loop Points

- After analysis: `PROCEED`, `REFINE`, or `PIVOT`.
- After rebuttal review: either refine experiments or restructure the paper.
- Record each loop in `PROGRESS.md` with a version label such as `v1`, `v2`, `v3`.

## Minimum Cycle Discipline

Do at least two full passes over the evidence-and-writing loop for any paper intended for submission.
