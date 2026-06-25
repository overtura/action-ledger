from __future__ import annotations

import re
from pathlib import Path

from action_ledger.models import ActionItem


CHECKBOX_RE = re.compile(r"^\s*[-*]\s+\[(?P<mark>[ xX])\]\s+(?P<text>.+)$")
MARKER_RE = re.compile(r"\b(?P<kind>TODO|FIXME|DECISION):\s*(?P<text>.+)")
OWNER_RE = re.compile(r"(?<!\w)@(?P<owner>[A-Za-z0-9_.-]+)")
TAG_RE = re.compile(r"(?<!\w)#(?P<tag>[A-Za-z0-9_.-]+)")


def discover_markdown_files(paths: list[Path]) -> list[Path]:
    files: list[Path] = []
    for path in paths:
        if path.is_file() and path.suffix.lower() == ".md":
            files.append(path)
        elif path.is_dir():
            files.extend(
                item
                for item in path.rglob("*.md")
                if ".git" not in item.parts and item.is_file()
            )
    return sorted(unique_paths(files))


def scan_paths(paths: list[Path]) -> list[ActionItem]:
    items: list[ActionItem] = []
    for path in discover_markdown_files(paths):
        items.extend(scan_file(path))
    return items


def scan_file(path: Path) -> list[ActionItem]:
    items: list[ActionItem] = []
    for line_number, line in enumerate(
        path.read_text(encoding="utf-8", errors="replace").splitlines(),
        start=1,
    ):
        checkbox = CHECKBOX_RE.search(line)
        if checkbox:
            text = checkbox.group("text").strip()
            mark = checkbox.group("mark").lower()
            items.append(
                build_item(
                    source=path,
                    line=line_number,
                    kind="task",
                    status="done" if mark == "x" else "open",
                    text=text,
                )
            )
            continue

        marker = MARKER_RE.search(line)
        if marker:
            kind = marker.group("kind").lower()
            status = "recorded" if kind == "decision" else "open"
            items.append(
                build_item(
                    source=path,
                    line=line_number,
                    kind=kind,
                    status=status,
                    text=marker.group("text").strip(),
                )
            )
    return items


def build_item(
    *,
    source: Path,
    line: int,
    kind: str,
    status: str,
    text: str,
) -> ActionItem:
    owner_match = OWNER_RE.search(text)
    tags = [f"#{match.group('tag')}" for match in TAG_RE.finditer(text)]
    return ActionItem(
        source=source,
        line=line,
        kind=kind,
        status=status,
        text=text,
        owner=f"@{owner_match.group('owner')}" if owner_match else None,
        tags=tags,
    )


def unique_paths(paths: list[Path]) -> list[Path]:
    seen: set[Path] = set()
    result: list[Path] = []
    for path in paths:
        resolved = path.resolve()
        if resolved in seen:
            continue
        seen.add(resolved)
        result.append(path)
    return result
