# Action Ledger

Action Ledger scans Markdown notes, meeting docs, and repository docs for action
items. It finds checkboxes, `TODO`, `FIXME`, and `DECISION` markers, then writes
a compact report for humans or CI.

Use it when a repository keeps work in Markdown and you want a quick answer to:

- What is still open?
- Which files contain follow-up work?
- Which decisions were recorded?
- Should CI fail because too many open actions remain?

## Install

```bash
python -m pip install -e .
```

For development tools:

```bash
python -m pip install -e ".[dev]"
```

## Quick Start

Scan this repository:

```bash
action-ledger scan README.md docs
```

Write JSON for automation:

```bash
action-ledger scan README.md docs --format json --output action-ledger-report.json
```

Fail CI when open action items exceed a threshold:

```bash
action-ledger scan README.md docs --max-open 10
```

## Supported Markdown Patterns

Checkbox tasks:

```markdown
- [ ] Publish release notes #release @owner
- [x] Update onboarding docs #docs
```

Inline markers:

```markdown
TODO: Add Windows installation notes #docs
FIXME: Replace placeholder benchmark data
DECISION: Keep the first version dependency-free
```

Action Ledger extracts owners like `@owner` and tags like `#docs`.

## CLI

```text
action-ledger scan PATH [PATH ...] [--format table|json|markdown] [--output FILE] [--max-open N]
```

Output formats:

- `table`: default terminal report
- `json`: machine-readable report
- `markdown`: Markdown report for pull requests or docs

Exit codes:

- `0`: scan succeeded and open count is within `--max-open`
- `1`: scan succeeded but open count is greater than `--max-open`
- `2`: command usage error

## Self-Improvement Target

This repository is intentionally small enough to use as a target for an
eval-driven maintainer/docs bot. The docs are useful, but compact, and the
project has a real CLI that can be improved over time.

Suggested target configuration:

```env
TARGET_REPOSITORY=OWNER/action-ledger
TARGET_DEFAULT_BRANCH=main
TARGET_WORKTREE=targets/action-ledger
TARGET_DOC_PATHS=README.md,docs
TARGET_EVALS_PATH=evals/docs_qa.jsonl
```

Useful first improvement tasks:

- Improve the Windows examples in `docs/USAGE.md`.
- Add more examples for `--format markdown`.
- Add docs for interpreting the JSON schema.
- Add parser support for priority markers like `P1` or `P2`.

## Development

```bash
python -m pip install -e ".[dev]"
python -m pytest
action-ledger scan README.md docs --format markdown
```

## License

MIT
