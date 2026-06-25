# Contributing

## Local Setup

```bash
python -m pip install -e ".[dev]"
python -m pytest
```

## Pull Request Checklist

- [ ] The CLI still works with `action-ledger scan README.md docs`.
- [ ] Tests pass with `python -m pytest`.
- [ ] Documentation is updated for behavior changes.
- [ ] No generated reports are committed.
