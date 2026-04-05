# AutoAcad Update Playbook

Use this file when the upstream long-form research prompt changes and you want to update AutoAcad without rewriting the whole package.

## Fast Rule

Do not edit everything.

First classify the change, then update only the matching layer.

## Update Routing

### 1. The upstream changes the stage order, adds a gate, or changes refine/pivot logic

Edit:

- `references/pipeline.md`

Typical examples:

- adding a new gate after paper draft
- changing rebuttal to loop back into experiments
- changing the minimum number of cycles

### 2. The upstream adds or tightens a hard rule

Edit:

- `references/restricts.md`

Typical examples:

- banning a new anti-pattern
- making topic discipline stricter
- adding a new evidence red line

### 3. The upstream changes experiment execution requirements

Edit:

- `references/experiment-rules.md`
- `run/SKILL.md`
- scripts only if the rule needs executable support

Typical examples:

- changing pilot timing requirements
- adding a new resource guard
- requiring a new numerical-stability check

### 4. The upstream changes paper structure or writing expectations

Edit:

- `references/paper-structure.md`
- `draft/SKILL.md`
- `review/SKILL.md` if review criteria also change

Typical examples:

- new word-count targets
- stronger ablation requirements
- new figure or appendix expectations

### 5. The upstream changes the required project tree

Edit:

- `templates/paper-tree.template.md`
- `templates/PROGRESS.template.md`
- `templates/stage-plan.template.md`
- `scripts/init_paper_project.py`

### 6. The upstream adds a concrete verification rule

If the rule is only guidance:

- update the relevant `SKILL.md` or `references/*.md`

If the rule should be machine-checkable:

- add or update a script under `scripts/`

## Practical Update Workflow

1. Paste the new upstream text into chat.
2. State what changed, not just the whole text again.
3. Route each change to one of the layers above.
4. Update the minimal set of files.
5. Re-run:
   - script syntax check
   - skill frontmatter check
   - maintenance sync

## Good Update Requests

- “新增了一个 quality gate，要加到 AutoAcad。”
- “实验部分要求先跑 3 个 seed 的 pilot，再扩全量。”
- “写作要求把 Discussion 和 Limitations 的字数提高了。”
- “目录结构里 paper/mypaper 下要再加 appendix/。”

## Bad Update Requests

- “把这段 2 万字 prompt 全部重新塞进去。”

That would recreate the same maintenance problem AutoAcad was designed to avoid.
