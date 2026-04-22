# AutoAcad Hard Constraints

## Topic Lock

- Keep every section tied to the paper's actual research question.
- Do not present setup work, dependency fixes, or infrastructure cleanup as research contributions.
- Do not drift into adjacent topics just because literature is easier to find there.
- **Hard Topic Constraint:** The paper MUST be about the specified topic.
- **Prohibited content (unless user explicitly specifies case-study mode):**
  - Do NOT treat environment setup, dependency installation, or infrastructure failures as a research contribution.
  - Do NOT present debugging logs, system errors, or configuration issues as experimental findings.
  - Do NOT drift to tangential topics not directly related to the stated topic.
  - Every section MUST connect back to the core research question.
  - The Abstract and Introduction MUST clearly state the research problem derived from the topic.
  - The Method section MUST describe a technical approach, not a workflow.
  - The Results section MUST report quantitative outcomes of experiments, not environment status.

## Evidence Discipline

- Real papers only. Preserve DOI, arXiv ID, URL, and cite keys when available.
- Real experiments only. Report numbers that came from executed code and saved results.
- Real claims only. If the code or logs do not show it, the paper cannot claim it.

## Anti-Fabrication Rules

- No fake loss curves.
- No hand-waved significance tests.
- No invented dataset counts, trial counts, or ablation results.
- No retrospective wording that implies a stronger experiment than was actually run.

## Writing Discipline

- Keep the core novelty to 1-2 ideas.
- Use limitations to narrow claims rather than hide risk.
- Prefer precise negative statements over vague optimism when evidence is weak.
