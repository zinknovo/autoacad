# AutoAcad Prepare — Reference Codebase Selection

Imported from AI-Researcher `prepare_agent` (`research_agent/inno/agents/inno_agent/prepare_agent.py`). Use only when the prepare stage needs to pick reference codebases for an innovative idea.

## Selection Criteria

1. More stars → more recommended.
2. More recently created → more recommended. Too old → not recommended.
3. More detailed `README.md` → more readable, more reproducible → more recommended.
4. Clearer code structure, comments, and inline explanations → more maintainable → more recommended.
5. Prefer `python`; prefer running on the local machine over docker; for deep learning prefer `pytorch`.

## Workflow

1. Review the search results for repositories relevant to the innovative idea.
2. `git clone` the 5-8 repositories you actually need into the working directory; preserve repository names.
3. Inspect structure with the equivalent of `gen_code_tree_structure`.
4. Read `README.md` for purpose and function.
5. Read additional files for implementation detail.
6. Choose **at least 5** repositories. Accuracy first, count minimal second.
7. Emit the final determination via the `case_resolved` equivalent.

## Output Schema

```json
{
  "reference_codebases": ["<repo-name>", "..."],
  "reference_paths": ["<path>", "..."],
  "reference_papers": ["<paper-title>", "..."]
}
```

Record the same three fields in `PROGRESS.md` under the prepare stage entry. Downstream (`ideate`, `plan`, `run`) reads reference paths from there.