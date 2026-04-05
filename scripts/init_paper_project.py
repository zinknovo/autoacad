#!/usr/bin/env python3
"""Initialize a paper project tree for AutoAcad."""

from __future__ import annotations

import argparse
from pathlib import Path

ROOT_FILES = {
    "MEGA_PROMPT.md": "# MEGA_PROMPT\n\nFill this with the project-specific pipeline instructions.\n",
    "RESTRICTS.yaml": "# Fill with project-specific hard constraints.\n",
}

SECTION_FILES = {
    "introduction.tex": "% Introduction\n",
    "related_work.tex": "% Related Work\n",
    "method.tex": "% Method\n",
    "experiments.tex": "% Experiments\n",
    "results.tex": "% Results\n",
    "discussion.tex": "% Discussion\n",
    "limitations.tex": "% Limitations\n",
    "conclusion.tex": "% Conclusion\n",
}

MAIN_TEX = r"""\documentclass{article}
\begin{document}
% Replace with the target conference template and proper inputs.
\input{sections/introduction}
\input{sections/related_work}
\input{sections/method}
\input{sections/experiments}
\input{sections/results}
\input{sections/discussion}
\input{sections/limitations}
\input{sections/conclusion}
\end{document}
"""

PROGRESS_TEMPLATE = Path(__file__).resolve().parent.parent / "templates" / "PROGRESS.template.md"
STAGE_PLAN_TEMPLATE = Path(__file__).resolve().parent.parent / "templates" / "stage-plan.template.md"


def write_if_missing(path: Path, content: str) -> None:
    if not path.exists():
        path.write_text(content)


def main() -> int:
    parser = argparse.ArgumentParser(description="Initialize an AutoAcad paper project tree.")
    parser.add_argument("project_root", help="Target project directory")
    parser.add_argument("--with-paper-skeleton", action="store_true", help="Create paper/mypaper skeleton files")
    args = parser.parse_args()

    root = Path(args.project_root).expanduser().resolve()
    root.mkdir(parents=True, exist_ok=True)

    dirs = [
        root / "code",
        root / "data",
        root / "docs",
        root / "plans",
        root / "results",
        root / "paper",
        root / "paper" / "mypaper",
        root / "paper" / "mypaper" / "figures",
        root / "paper" / "mypaper" / "sections",
    ]
    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)

    for name, content in ROOT_FILES.items():
        write_if_missing(root / name, content)

    if PROGRESS_TEMPLATE.exists():
        write_if_missing(root / "PROGRESS.md", PROGRESS_TEMPLATE.read_text())
    else:
        write_if_missing(root / "PROGRESS.md", "# PROGRESS\n")

    if STAGE_PLAN_TEMPLATE.exists():
        write_if_missing(root / "plans" / "stage-00-init.md", STAGE_PLAN_TEMPLATE.read_text().replace("<stage-name>", "topic-init"))

    if args.with_paper_skeleton:
        write_if_missing(root / "paper" / "mypaper" / "main.tex", MAIN_TEX)
        for name, content in SECTION_FILES.items():
            write_if_missing(root / "paper" / "mypaper" / "sections" / name, content)

    print(root)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
