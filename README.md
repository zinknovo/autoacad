# AutoAcad

AutoAcad is a layered academic-paper workflow skill package for Codex-compatible agents.

It combines:

- paper-pipeline structure inspired by `aiming-lab/AutoResearchClaw`
- research-workflow patterns from `HKUDS/AI-Researcher`
- local packaging, update routing, and validation logic for daily use

## Package Layout

- `SKILL.md`: top-level routing entry
- `prepare/` to `export/`: stage-oriented subskills
- `references/`: constraints, pipeline, update routing, and upstream summaries
- `scripts/`: project scaffolding and consistency checks
- `templates/`: reusable paper-project templates

## Upstream Tracking

The package includes a local upstream refresh script:

- `scripts/update_from_upstreams.py`

It snapshots selected files from:

- `aiming-lab/AutoResearchClaw`
- `HKUDS/AI-Researcher`

and generates:

- `references/upstreams.md`
- `references/upstream-snapshots/`
- optionally `references/upstream-review.md`

## Notes

- This repository is the source of truth for the `autoacad` skill.
- Local installations can symlink the active skill directory to this repository.
