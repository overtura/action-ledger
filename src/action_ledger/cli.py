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

    scan = subparsers.add_parser("scan", help="Markdown 파일에서 작업 항목을 스캔합니다.")
    scan.add_argument("paths", nargs="+", help="스캔할 Markdown 파일 또는 디렉터리입니다.")
    scan.add_argument(
        "--format",
        choices=["table", "json", "markdown"],
        default="table",
        help="출력 형식입니다.",
    )
    scan.add_argument("--output", help="보고서를 파일로 씁니다.")
    scan.add_argument("--max-open", type=int, help="열린 항목 수가 N보다 많으면 실패합니다.")
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
                f"열린 작업 수 {open_count}개가 --max-open {args.max_open} 기준을 넘었습니다.",
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
        "액션 레저 보고서",
        f"전체: {len(items)}",
        f"열림: {count_by_status(items).get('open', 0)}",
        "",
        "상태      종류      출처:줄      내용",
        "--------  --------  -----------  ----",
    ]
    for item in items:
        lines.append(
            f"{display_status(item.status):<8}  {display_kind(item.kind):<8}  "
            f"{item.source.as_posix()}:{item.line:<4}  {item.text}"
        )
    return "\n".join(lines)


def render_markdown(items: list[ActionItem]) -> str:
    lines = [
        "# 액션 레저 보고서",
        "",
        f"- 전체: {len(items)}",
        f"- 열림: {count_by_status(items).get('open', 0)}",
        "",
        "| 상태 | 종류 | 출처 | 내용 |",
        "| ------ | ---- | ------ | ---- |",
    ]
    for item in items:
        source = f"{item.source.as_posix()}:{item.line}"
        lines.append(
            f"| {display_status(item.status)} | {display_kind(item.kind)} | "
            f"`{source}` | {item.text} |"
        )
    return "\n".join(lines)


def count_by_status(items: list[ActionItem]) -> Counter[str]:
    return Counter(item.status for item in items)


def count_by_kind(items: list[ActionItem]) -> Counter[str]:
    return Counter(item.kind for item in items)


def display_status(status: str) -> str:
    labels = {
        "open": "열림",
        "done": "완료",
        "recorded": "기록",
    }
    return labels.get(status, status)


def display_kind(kind: str) -> str:
    labels = {
        "task": "작업",
        "todo": "할일",
        "fixme": "수정",
        "decision": "결정",
    }
    return labels.get(kind, kind)


def write_or_print(report: str, *, output: str | None) -> None:
    if output:
        Path(output).write_text(report + "\n", encoding="utf-8", newline="\n")
        return
    print(report)


if __name__ == "__main__":
    sys.exit(main())
