# AutoAcad

AutoAcad is a multi-stage academic paper workflow package for local coding agents.

It merges two sources:

- `aiming-lab/AutoResearchClaw`: stage-gated paper pipeline, review loops, evidence discipline
- `HKUDS/AI-Researcher`: repo-first research workflow, idea generation, experiment planning

The package is organized as a skill bundle, but most of the content is agent-agnostic:

- Markdown instructions
- reusable templates
- local Python helper scripts

The current source of truth is this repository.

## What It Contains

- `SKILL.md`
  - top-level router for end-to-end paper work
- `prepare/`, `survey/`, `ideate/`, `plan/`, `run/`, `analyze/`, `draft/`, `review/`, `export/`
  - narrow stage-specific subskills
- `references/`
  - hard constraints, paper structure, experiment rules, upstream mapping, upstream snapshots
- `templates/`
  - `PROGRESS.md`, stage plan, and paper project tree templates
- `scripts/`
  - project scaffolding
  - stage-output checks
  - results-vs-claims checks
  - upstream refresh logic
- `agents/openai.yaml`
  - lightweight metadata for OpenAI/Codex-style skill discovery

## Package Layout

```text
autoacad/
├── SKILL.md
├── prepare/           # project inventory and local context
├── survey/            # literature search, screening, synthesis
├── ideate/            # hypotheses, gaps, contribution framing
├── plan/              # experiments, baselines, ablations, resource plan
├── run/               # implementation, pilot timing, iterative repair
├── analyze/           # result reading, proceed/refine/pivot decisions
├── draft/             # outline, section drafting, figure planning
├── review/            # reviewer simulation, evidence checks, rebuttal prep
├── export/            # final package, citation checks, export
├── references/        # constraints, upstream mapping, snapshots
├── templates/         # reusable project templates
├── scripts/           # local helper scripts
└── agents/            # optional agent-specific metadata
```

## How To Use It

Use the root package when the task spans multiple stages, for example:

- starting a paper project from a rough idea
- turning an implementation into a submission-grade paper workflow
- running the full loop from literature to experiments to draft

Use the narrow subskills when the current task is clearly scoped:

- `prepare/` for local repo, docs, data, and constraint inventory
- `survey/` for literature collection and screening
- `ideate/` for hypotheses and contribution shaping
- `plan/` for experiment and ablation design
- `run/` for real experiment execution
- `analyze/` for evidence-based decisions
- `draft/` for writing
- `review/` for stress-testing claims
- `export/` for final packaging

Operational rule:

- use the narrowest skill that fits the current stage
- use root `SKILL.md` only when orchestration across stages is required

## Agent Compatibility

AutoAcad is not Codex-only.

The package works best with any local agent system that can:

1. read a `SKILL.md`-style instruction file
2. follow relative references inside the package
3. run local scripts when needed

That includes:

- Codex
- Claude Code setups with local skills directories
- Gemini CLI setups with local skills directories
- OpenCode setups with local skills directories
- any custom agent runner that can route to local Markdown prompt bundles

Why the repo previously said "Codex-compatible":

- this repo currently includes `agents/openai.yaml`, which is a small OpenAI/Codex-facing metadata file
- but the actual package logic lives in plain Markdown and Python, so the bundle itself is broader than Codex

In short:

- `agents/openai.yaml` is agent-specific metadata
- the rest of the repo is mostly agent-neutral

## Install From GitHub

### Codex

Clone or symlink the repo into your Codex skills directory:

```bash
git clone https://github.com/zinknovo/autoacad.git "$CODEX_HOME/skills/autoacad"
```

If your Codex setup uses `~/.codex/skills`:

```bash
git clone https://github.com/zinknovo/autoacad.git ~/.codex/skills/autoacad
```

### Claude Code

```bash
git clone https://github.com/zinknovo/autoacad.git ~/.claude/skills/autoacad
```

### Gemini CLI

```bash
git clone https://github.com/zinknovo/autoacad.git ~/.gemini/skills/autoacad
```

### OpenCode

```bash
git clone https://github.com/zinknovo/autoacad.git ~/.config/opencode/skills/autoacad
```

### Generic Local-Agent Setup

If your agent does not have a built-in skill directory convention:

1. clone this repository anywhere local
2. point your agent's prompt/skill loader at `SKILL.md`
3. allow the agent to resolve relative files inside the repo

## Updating

AutoAcad tracks two upstreams:

- `AutoResearchClaw`
- `AI-Researcher`

Refresh upstream state with:

```bash
python3 scripts/update_from_upstreams.py \
  --repos-dir /path/to/local/upstream/repos \
  --skill-dir /path/to/autoacad
```

This updates:

- `references/upstreams.md`
- `references/upstream-snapshots/`
- optionally `references/upstream-review.md`

The intended maintenance model is:

- daily or weekly local automation runs the refresh
- the maintainer reviews upstream drift
- only minimal mapped files are updated in this repo

See:

- `references/source-blueprint.md`
- `references/update-playbook.md`

## Local Project Scaffolding

To initialize a paper project structure:

```bash
python3 scripts/init_paper_project.py --help
```

Other useful checks:

```bash
python3 scripts/check_stage_outputs.py --help
python3 scripts/check_results_vs_claims.py --help
```

## Design Notes

AutoAcad intentionally keeps three layers separate:

1. workflow routing
2. hard research constraints
3. local helper scripts

That separation is what makes it maintainable across agent ecosystems instead of locking it to a single client.
