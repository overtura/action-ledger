from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

from action_ledger.models import ActionItem
from action_ledger.parser import scan_paths


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="action-ledger")
    subparsers = parser.add_subparsers(dest="command", required=True)

    scan = subparsers.add_parser("scan", help="Scan Markdown files for action items.")
    scan.add_argument("paths", nargs="+", help="Markdown files or directories to scan.")
    scan.add_argument(
        "--format",
        choices=["table", "json", "markdown"],
        default="table",
        help="Output format.",
    )
    scan.add_argument("--output", help="Write the report to a file.")
    scan.add_argument("--max-open", type=int, help="Fail when open item count is above N.")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "scan":
        items = scan_paths([Path(path) for path in args.paths])
        report = render_report(items, output_format=args.format)
        write_or_print(report, output=args.output)
        open_count = count_by_status(items).get("open", 0)
        if args.max_open is not None and open_count > args.max_open:
            print(
                f"Open action count {open_count} is greater than --max-open {args.max_open}.",
                file=sys.stderr,
            )
            return 1
        return 0
    raise AssertionError(f"Unhandled command: {args.command}")


def render_report(items: list[ActionItem], *, output_format: str) -> str:
    if output_format == "json":
        return render_json(items)
    if output_format == "markdown":
        return render_markdown(items)
    return render_table(items)


def render_json(items: list[ActionItem]) -> str:
    payload = {
        "summary": {
            "total": len(items),
            "by_status": dict(count_by_status(items)),
            "by_kind": dict(count_by_kind(items)),
        },
        "items": [item.to_json() for item in items],
    }
    return json.dumps(payload, indent=2, sort_keys=True)


def render_table(items: list[ActionItem]) -> str:
    lines = [
        "Action Ledger Report",
        f"Total: {len(items)}",
        f"Open: {count_by_status(items).get('open', 0)}",
        "",
        "STATUS    KIND      SOURCE:LINE  TEXT",
        "--------  --------  -----------  ----",
    ]
    for item in items:
        lines.append(
            f"{item.status:<8}  {item.kind:<8}  "
            f"{item.source.as_posix()}:{item.line:<4}  {item.text}"
        )
    return "\n".join(lines)


def render_markdown(items: list[ActionItem]) -> str:
    lines = [
        "# Action Ledger Report",
        "",
        f"- Total: {len(items)}",
        f"- Open: {count_by_status(items).get('open', 0)}",
        "",
        "| Status | Kind | Source | Text |",
        "| ------ | ---- | ------ | ---- |",
    ]
    for item in items:
        source = f"{item.source.as_posix()}:{item.line}"
        lines.append(f"| {item.status} | {item.kind} | `{source}` | {item.text} |")
    return "\n".join(lines)


def count_by_status(items: list[ActionItem]) -> Counter[str]:
    return Counter(item.status for item in items)


def count_by_kind(items: list[ActionItem]) -> Counter[str]:
    return Counter(item.kind for item in items)


def write_or_print(report: str, *, output: str | None) -> None:
    if output:
        Path(output).write_text(report + "\n", encoding="utf-8", newline="\n")
        return
    print(report)


if __name__ == "__main__":
    sys.exit(main())
