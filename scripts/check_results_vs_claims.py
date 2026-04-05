#!/usr/bin/env python3
"""Check whether numeric results from JSON appear in a paper draft."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def flatten_numbers(node: Any, prefix: str = ""):
    if isinstance(node, dict):
        for key, value in node.items():
            new_prefix = f"{prefix}.{key}" if prefix else str(key)
            yield from flatten_numbers(value, new_prefix)
    elif isinstance(node, list):
        for idx, value in enumerate(node):
            new_prefix = f"{prefix}[{idx}]"
            yield from flatten_numbers(value, new_prefix)
    elif isinstance(node, (int, float)) and not isinstance(node, bool):
        yield prefix, float(node)


def candidate_formats(value: float):
    rounded = [
        f"{value}",
        f"{value:.1f}",
        f"{value:.2f}",
        f"{value:.3f}",
        f"{value:.4f}",
        f"{value:.2%}",
        f"{value:.1%}",
    ]
    return {item.rstrip('0').rstrip('.') if '.' in item and '%' not in item else item for item in rounded}


def main() -> int:
    parser = argparse.ArgumentParser(description="Check result numbers against a draft file.")
    parser.add_argument("results_json")
    parser.add_argument("paper_file")
    args = parser.parse_args()

    results_path = Path(args.results_json).expanduser().resolve()
    paper_path = Path(args.paper_file).expanduser().resolve()

    results = json.loads(results_path.read_text())
    paper_text = paper_path.read_text()

    missing = []
    for path, value in flatten_numbers(results):
        formats = candidate_formats(value)
        if not any(token in paper_text for token in formats):
            missing.append({"path": path, "value": value, "formats_checked": sorted(formats)})

    report = {
        "results_json": str(results_path),
        "paper_file": str(paper_path),
        "checked_numbers": sum(1 for _ in flatten_numbers(results)),
        "missing_numbers": missing,
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if not missing else 1


if __name__ == "__main__":
    raise SystemExit(main())
