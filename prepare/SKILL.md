---
name: autoacad-prepare
description: Use when starting a paper project and needing to inventory local code, docs, datasets, constraints, and source materials before literature review or experiment planning.
---

# AutoAcad Prepare

## Overview

Use this stage to establish the paper project's ground truth before any literature or experiment work.

## Workflow

1. Read the project docs first: abstract draft, experiment design notes, whole-paper concept notes, and any constraints file.
2. Inventory code, data, examples, and docs that the paper must describe faithfully.
3. Detect hardware constraints early. Record whether the project is CPU-only, CUDA, or Apple MPS.
4. Identify missing prerequisites: absent docs, missing dataset paths, missing template, or missing baseline implementations.
5. Initialize the canonical project tree with `../scripts/init_paper_project.py` if the project is not structured yet.
6. Write the first stage plan and the initial `PROGRESS.md` entry before moving on.
7. **For reference codebase selection (if applicable):**
   - Review searching results and repositories for relevance to innovative ideas.
   - **Selection criteria (from AI-Researcher):**
     - Repositories with more stars are more recommended.
     - Repositories created more recently are more recommended; too old repositories are not recommended.
     - More detailed `README.md` file means more readable codebase and more reproducible, so more recommended.
     - More clear code structure, code comments, and inline code explanations mean more readable codebase and more maintainable, so more recommended.
     - Prefer repositories with `python` language, and running coding in the local machine rather than in docker. For deep learning projects, prefer `pytorch` framework.
   - Choose at least 5 repositories as reference codebases, aiming for accuracy and minimal number.

## Required Outputs

- A concise source-of-truth inventory.
- A list of blocked inputs and assumptions.
- A confirmed project tree rooted at `<project>-paper/`.
- A first-pass environment note in `PROGRESS.md`.
- If applicable, a list of determined reference codebases, paths, and papers.
