# Agent Instructions

This repository is a small Python CLI. Keep changes focused and easy to review.

- Preserve the public CLI command: `action-ledger scan`.
- Prefer standard library code unless a dependency removes meaningful complexity.
- Update docs when CLI behavior changes.
- Run `python -m pytest` before committing code changes.
- Keep generated reports untracked.
- Do not add network calls to the scanner.
