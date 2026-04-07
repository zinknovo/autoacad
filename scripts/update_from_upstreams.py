#!/usr/bin/env python3
"""Refresh AutoAcad upstream snapshots and generate update reports."""

from __future__ import annotations

import argparse
import json
import os
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable
from urllib import error, request


AUTORESEARCH_REPO_NAME = "AutoResearchClaw"
AI_RESEARCHER_REPO_NAME = "AI-Researcher"

AUTORESEARCH_FILES = [
    "README.md",
    "prompts.default.yaml",
]

AI_RESEARCHER_FILES = [
    "README.md",
    "research_agent/inno/agents/inno_agent/prepare_agent.py",
    "research_agent/inno/agents/inno_agent/survey_agent.py",
    "research_agent/inno/agents/inno_agent/idea_agent.py",
    "research_agent/inno/agents/inno_agent/plan_agent.py",
    "research_agent/inno/agents/inno_agent/judge_agent.py",
    "research_agent/inno/agents/inno_agent/exp_analyser.py",
]

GENERATED_REFERENCE_FILES = {
    "upstream-review.md",
    "upstreams.md",
}


@dataclass
class RepoSummary:
    name: str
    repo_dir: Path
    head: str | None
    tracked_files: list[str]
    notes: list[str]


def write_if_changed(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and path.read_text() == content:
        return
    path.write_text(content)


def read_text_if_exists(path: Path) -> str:
    return path.read_text() if path.exists() else ""


def repo_head(repo_dir: Path) -> str | None:
    head_file = repo_dir / ".git" / "HEAD"
    if not head_file.exists():
        return None
    try:
        import subprocess

        completed = subprocess.run(
            ["git", "-C", str(repo_dir), "rev-parse", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
        )
        return completed.stdout.strip()
    except Exception:
        return None


def copy_tracked_files(repo_dir: Path, files: Iterable[str], target_root: Path) -> list[str]:
    copied: list[str] = []
    for rel in files:
        src = repo_dir / rel
        if not src.exists():
            continue
        dst = target_root / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        content = src.read_text()
        write_if_changed(dst, content)
        copied.append(rel)
    return copied


def parse_autoresearchclaw_prompts(text: str) -> list[str]:
    stages: list[str] = []
    in_stages = False
    for raw_line in text.splitlines():
        if raw_line.startswith("stages:"):
            in_stages = True
            continue
        if in_stages:
            if raw_line and not raw_line.startswith(" "):
                break
            if raw_line.startswith("  ") and not raw_line.startswith("    "):
                stripped = raw_line.strip()
                if stripped.endswith(":"):
                    key = stripped[:-1]
                    if key and re.fullmatch(r"[a-z_]+", key):
                        stages.append(key)
    return stages


def parse_autoresearchclaw_readme(text: str) -> list[str]:
    notes: list[str] = []
    match = re.search(r"(\d+)\s+stages?\s+across\s+(\d+)\s+phases?", text, re.I)
    if match:
        notes.append(f"README pipeline headline: {match.group(1)} stages across {match.group(2)} phases.")
    if "OpenAlex" in text or "Semantic Scholar" in text:
        notes.append("README references real literature APIs.")
    if "quality gate" in text.lower():
        notes.append("README mentions explicit quality-gate style checks.")
    return notes


def parse_ai_researcher_readme(text: str) -> list[str]:
    notes: list[str] = []
    if "Manuscript Creation" in text:
        notes.append("README explicitly includes manuscript creation.")
    if "Resource Collector" in text:
        notes.append("README includes automated resource collection.")
    if "Idea Generator" in text:
        notes.append("README includes idea generation from collected resources.")
    return notes


def summarize_local_autoacad(skill_dir: Path) -> list[str]:
    subskills = sorted(p.name for p in skill_dir.iterdir() if p.is_dir() and (p / "SKILL.md").exists())
    refs = sorted(
        p.name
        for p in (skill_dir / "references").glob("*.md")
        if p.name not in GENERATED_REFERENCE_FILES
    )
    scripts = sorted(p.name for p in (skill_dir / "scripts").glob("*.py"))
    notes = [
        f"Local subskills: {', '.join(subskills)}.",
        f"Local reference files: {', '.join(refs)}.",
        f"Local scripts: {', '.join(scripts)}.",
    ]
    return notes


def repo_display_name(summary: RepoSummary) -> str:
    # Keep generated reports stable across local machines and CI runners.
    return summary.name


def extract_recorded_head(markdown: str, section: str) -> str | None:
    section_match = re.search(rf"## {re.escape(section)}\n(.*?)(?:\n## |\Z)", markdown, re.S)
    if not section_match:
        return None
    head_match = re.search(r"- HEAD: `([^`]+)`", section_match.group(1))
    if not head_match:
        return None
    head = head_match.group(1)
    return None if head == "missing" else head


def should_refresh_review(existing_upstreams_md: str, auto_head: str | None, ai_head: str | None) -> bool:
    recorded_auto_head = extract_recorded_head(existing_upstreams_md, "AutoResearchClaw")
    recorded_ai_head = extract_recorded_head(existing_upstreams_md, "AI-Researcher")
    return recorded_auto_head != auto_head or recorded_ai_head != ai_head


def build_review_markdown(review_text: str, auto_head: str | None, ai_head: str | None) -> str:
    return (
        "# AutoAcad Upstream Review\n\n"
        "This file is generated automatically from upstream context plus local AutoAcad files.\n\n"
        f"Reviewed AutoResearchClaw HEAD: `{auto_head or 'missing'}`\n"
        f"Reviewed AI-Researcher HEAD: `{ai_head or 'missing'}`\n\n"
        f"{review_text.rstrip()}\n"
    )


def review_has_current_heads(review_markdown: str, auto_head: str | None, ai_head: str | None) -> bool:
    expected_auto = f"Reviewed AutoResearchClaw HEAD: `{auto_head or 'missing'}`"
    expected_ai = f"Reviewed AI-Researcher HEAD: `{ai_head or 'missing'}`"
    return expected_auto in review_markdown and expected_ai in review_markdown


def build_upstreams_markdown(
    skill_dir: Path,
    auto_summary: RepoSummary,
    ai_summary: RepoSummary,
) -> str:
    local_notes = summarize_local_autoacad(skill_dir)
    prompts_text = read_text_if_exists(auto_summary.repo_dir / "prompts.default.yaml")
    auto_stages = parse_autoresearchclaw_prompts(prompts_text)
    lines = [
        "# AutoAcad Upstreams",
        "",
        "This file is generated by `scripts/update_from_upstreams.py`.",
        "",
        "## Source Policy",
        "",
        "- Primary upstream for paper-pipeline structure: `aiming-lab/AutoResearchClaw`.",
        "- Secondary upstream for academic-research workflow patterns: `HKUDS/AI-Researcher`.",
        "- AutoAcad keeps local judgment on what to import. It does not mirror either upstream blindly.",
        "",
        "## AutoResearchClaw",
        "",
        f"- Repo: `{repo_display_name(auto_summary)}`",
        f"- HEAD: `{auto_summary.head or 'missing'}`",
        f"- Tracked files: {', '.join(auto_summary.tracked_files) if auto_summary.tracked_files else 'none'}",
    ]
    if auto_stages:
        lines.append(f"- Detected prompt stages: {', '.join(auto_stages)}")
    for note in auto_summary.notes:
        lines.append(f"- {note}")
    lines += [
        "",
        "## AI-Researcher",
        "",
        f"- Repo: `{repo_display_name(ai_summary)}`",
        f"- HEAD: `{ai_summary.head or 'missing'}`",
        f"- Tracked files: {', '.join(ai_summary.tracked_files) if ai_summary.tracked_files else 'none'}",
    ]
    for note in ai_summary.notes:
        lines.append(f"- {note}")
    lines += [
        "",
        "## Local AutoAcad",
        "",
    ]
    lines.extend(f"- {note}" for note in local_notes)
    lines += [
        "",
        "## Maintenance Guidance",
        "",
        "- If AutoResearchClaw changes pipeline structure, update `references/pipeline.md` first.",
        "- If AI-Researcher changes research-agent decomposition, review whether any subskill routing or stage boundaries should change.",
        "- Treat generated upstream files as review inputs, not as files to copy-paste directly into core skill docs.",
        "",
    ]
    return "\n".join(lines) + "\n"


def extract_relevant_local_context(skill_dir: Path) -> str:
    parts = []
    for rel in [
        "SKILL.md",
        "references/pipeline.md",
        "references/restricts.md",
        "references/experiment-rules.md",
        "references/paper-structure.md",
    ]:
        path = skill_dir / rel
        if path.exists():
            parts.append(f"## {rel}\n\n{path.read_text()[:5000]}")
    return "\n\n".join(parts)


def extract_relevant_upstream_context(auto_repo: Path, ai_repo: Path) -> str:
    parts = []
    for label, repo, rels in [
        ("AutoResearchClaw", auto_repo, AUTORESEARCH_FILES),
        ("AI-Researcher", ai_repo, AI_RESEARCHER_FILES[:2]),
    ]:
        for rel in rels:
            path = repo / rel
            if path.exists():
                parts.append(f"## {label}:{rel}\n\n{path.read_text()[:7000]}")
    return "\n\n".join(parts)


def llm_review(skill_dir: Path, auto_repo: Path, ai_repo: Path) -> str | None:
    api_base = os.environ.get("OPENAI_API_BASE")
    api_key = os.environ.get("OPENAI_API_KEY")
    model = os.environ.get("OPENAI_MODEL_NAME") or "gpt-5"
    if not api_base or not api_key:
        return None

    prompt = (
        "You are updating a local research-skill package named AutoAcad. "
        "Compare the local package against the upstream structures from "
        "AutoResearchClaw and AI-Researcher. "
        "Return markdown with sections: Summary, Recommended File Updates, No-Change Areas. "
        "Keep recommendations specific to these target files: "
        "references/pipeline.md, references/restricts.md, references/experiment-rules.md, "
        "references/paper-structure.md, prepare/SKILL.md, survey/SKILL.md, ideate/SKILL.md, "
        "plan/SKILL.md, run/SKILL.md, analyze/SKILL.md, draft/SKILL.md, review/SKILL.md, export/SKILL.md. "
        "Do not suggest rewriting the whole package."
    )
    user_text = (
        "# Local AutoAcad\n\n"
        + extract_relevant_local_context(skill_dir)
        + "\n\n# Upstream Inputs\n\n"
        + extract_relevant_upstream_context(auto_repo, ai_repo)
    )
    body = {
        "model": model,
        "messages": [
            {"role": "system", "content": prompt},
            {"role": "user", "content": user_text},
        ],
    }
    payload = json.dumps(body).encode("utf-8")
    base = api_base.rstrip("/")
    req = request.Request(
        f"{base}/chat/completions",
        data=payload,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
        method="POST",
    )
    try:
        with request.urlopen(req, timeout=120) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except error.URLError:
        return None
    choices = data.get("choices") or []
    if not choices:
        return None
    message = choices[0].get("message") or {}
    content = message.get("content")
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        text_parts = []
        for item in content:
            if isinstance(item, dict) and item.get("type") == "text":
                text_parts.append(item.get("text", ""))
        return "\n".join(text_parts).strip() or None
    return None


def main() -> int:
    parser = argparse.ArgumentParser(description="Refresh AutoAcad upstream snapshots.")
    parser.add_argument("--repos-dir", required=True, help="Directory containing cloned upstream repos")
    parser.add_argument("--skill-dir", required=True, help="AutoAcad skill root")
    parser.add_argument(
        "--use-llm-if-configured",
        action="store_true",
        help="Generate an LLM review report when OPENAI_API_BASE and OPENAI_API_KEY are available",
    )
    args = parser.parse_args()

    repos_dir = Path(args.repos_dir).expanduser().resolve()
    skill_dir = Path(args.skill_dir).expanduser().resolve()
    refs_dir = skill_dir / "references"
    snapshots_dir = refs_dir / "upstream-snapshots"
    generated_at = datetime.now(timezone.utc).isoformat()
    existing_upstreams_md = read_text_if_exists(refs_dir / "upstreams.md")

    auto_repo = repos_dir / AUTORESEARCH_REPO_NAME
    ai_repo = repos_dir / AI_RESEARCHER_REPO_NAME

    auto_copied = copy_tracked_files(auto_repo, AUTORESEARCH_FILES, snapshots_dir / "AutoResearchClaw")
    ai_copied = copy_tracked_files(ai_repo, AI_RESEARCHER_FILES, snapshots_dir / "AI-Researcher")

    auto_summary = RepoSummary(
        name=AUTORESEARCH_REPO_NAME,
        repo_dir=auto_repo,
        head=repo_head(auto_repo),
        tracked_files=auto_copied,
        notes=parse_autoresearchclaw_readme(read_text_if_exists(auto_repo / "README.md")),
    )
    ai_summary = RepoSummary(
        name=AI_RESEARCHER_REPO_NAME,
        repo_dir=ai_repo,
        head=repo_head(ai_repo),
        tracked_files=ai_copied,
        notes=parse_ai_researcher_readme(read_text_if_exists(ai_repo / "README.md")),
    )

    upstreams_md = build_upstreams_markdown(skill_dir, auto_summary, ai_summary)
    write_if_changed(refs_dir / "upstreams.md", upstreams_md)

    review_file = refs_dir / "upstream-review.md"
    review_path: str | None = str(review_file) if review_file.exists() else None
    review_refreshed = False
    existing_review_md = read_text_if_exists(review_file)
    refresh_review = (
        not review_file.exists()
        or should_refresh_review(existing_upstreams_md, auto_summary.head, ai_summary.head)
        or not review_has_current_heads(existing_review_md, auto_summary.head, ai_summary.head)
    )
    if args.use_llm_if_configured and refresh_review:
        review_text = llm_review(skill_dir, auto_repo, ai_repo)
        if review_text:
            review_body = build_review_markdown(review_text, auto_summary.head, ai_summary.head)
            write_if_changed(review_file, review_body)
            review_path = str(review_file)
            review_refreshed = True

    print(json.dumps(
        {
            "generated_at": generated_at,
            "auto_research_claw_head": auto_summary.head,
            "ai_researcher_head": ai_summary.head,
            "review_refreshed": review_refreshed,
            "upstreams_md": str(refs_dir / "upstreams.md"),
            "upstream_review_md": review_path,
        },
        indent=2,
        sort_keys=True,
    ))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
