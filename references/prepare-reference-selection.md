# AutoAcad Prepare — Reference Codebase Selection

## Context

When the prepare stage involves selecting reference codebases for an innovative idea, use the following criteria and workflow derived from AI-Researcher's prepare agent.

## Selection Criteria

1. Repositories with more stars are more recommended.
2. Repositories created more recently are more recommended; too old repositories are not recommended.
3. More detailed `README.md` file means more readable codebase and more reproducible, so more recommended.
4. More clear code structure, code comments, and inline code explanations mean more readable codebase and more maintainable, so more recommended.
5. Prefer repositories with `python` language, and running coding in the local machine rather than in docker. For deep learning projects, prefer `pytorch` framework.

## Workflow

1. Review the searching results for repositories relevant to the innovative ideas.
2. Clone candidate repositories (choose 5-8 repositories that are actually needed).
3. Use `gen_code_tree_structure` to inspect code structure.
4. Read `README.md` to understand purpose and function.
5. Read additional files to understand implementation details.
6. Choose at least 5 repositories as reference codebases — aim for accuracy and minimal number.
7. Record the determined reference codebases, paths, and associated papers.

## Output

Record the selected references in `PROGRESS.md` with:
- `reference_codebases`: list of repository names
- `reference_paths`: list of determined paths
- `reference_papers`: list of titles of associated reference papers