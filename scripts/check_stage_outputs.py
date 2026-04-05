#!/usr/bin/env python3
"""Check whether a paper project has the expected stage artifacts."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

REQUIRED_PATHS = [
    "PROGRESS.md",
    "code",
    "data",
    "docs",
    "plans",
    "results",
    "paper/mypaper",
]

OPTIONAL_STAGE_HINTS = {
    "literature": ["docs", "results"],
    "experiments": ["code", "results"],
    "paper": ["paper/mypaper", "PROGRESS.md"],
}


def main() -> int:
    parser = argparse.ArgumentParser(description="Check AutoAcad stage outputs.")
    parser.add_argument("project_root")
    args = parser.parse_args()

    root = Path(args.project_root).expanduser().resolve()
    report = {"project_root": str(root), "required": {}, "optional_stage_hints": {}}

    for rel in REQUIRED_PATHS:
        report["required"][rel] = (root / rel).exists()

    for stage, rels in OPTIONAL_STAGE_HINTS.items():
        report["optional_stage_hints"][stage] = {rel: (root / rel).exists() for rel in rels}

    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
