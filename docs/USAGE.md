# Usage Guide

Action Ledger scans Markdown files and directories.

## Scan Files

```bash
action-ledger scan README.md docs/USAGE.md
```

## Scan Directories

```bash
action-ledger scan docs
```

Directories are searched recursively for `*.md` files. Hidden `.git`
directories are skipped.

## JSON Output

```bash
action-ledger scan README.md docs --format json --output action-ledger-report.json
```

The JSON report contains:

- `summary`: total counts
- `items`: individual action items with source, line, kind, status, text, tags,
  and owner

## Markdown Output

```bash
action-ledger scan README.md docs --format markdown
```

Use Markdown output when you want to paste a report into an issue, pull request,
or release note.

## CI Thresholds

```bash
action-ledger scan README.md docs --max-open 10
```

When `--max-open` is provided, the command exits with status `1` if the open
item count is greater than the threshold.

TODO: Add PowerShell-specific examples for Windows users #docs
