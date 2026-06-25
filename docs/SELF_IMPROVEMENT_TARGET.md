# Self-Improvement Target Notes

This repository is designed to be a realistic target for a maintainer/docs bot.

## Why This Works As A Test Target

- It has a real CLI with behavior that can be tested.
- It has short docs that can be improved safely.
- It includes target-specific documentation eval cases in `evals/docs_qa.jsonl`.
- It has a few intentional documentation gaps for future improvements.

## Suggested Bot Loop

```bash
python -m self_maintainer_bot.cli prepare-target
python -m self_maintainer_bot.cli target-status
python -m self_maintainer_bot.cli eval-docs --fail-under 0
python -m self_maintainer_bot.cli codex-local-loop --scope docs
```

FIXME: Add an example showing how to run the bot against a fork first.
