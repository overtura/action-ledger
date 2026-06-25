from pathlib import Path

from action_ledger.parser import scan_paths


def test_scan_paths_extracts_tasks_markers_tags_and_owner(tmp_path: Path) -> None:
    notes = tmp_path / "notes.md"
    notes.write_text(
        "\n".join(
            [
                "# Notes",
                "- [ ] Publish release notes #release @alex",
                "- [x] Update onboarding docs #docs",
                "TODO: Add Windows examples #docs",
                "FIXME: Replace placeholder data",
                "DECISION: Keep version 0.1 dependency-free",
                "할일: PowerShell 예시 추가 #docs",
                "수정: 오래된 출력 예시 갱신",
                "결정: 기본 문서는 한국어로 작성",
            ]
        ),
        encoding="utf-8",
    )

    items = scan_paths([notes])

    assert [item.kind for item in items] == [
        "task",
        "task",
        "todo",
        "fixme",
        "decision",
        "todo",
        "fixme",
        "decision",
    ]
    assert [item.status for item in items] == [
        "open",
        "done",
        "open",
        "open",
        "recorded",
        "open",
        "open",
        "recorded",
    ]
    assert items[0].owner == "@alex"
    assert items[0].tags == ["#release"]
    assert items[2].tags == ["#docs"]
    assert items[5].tags == ["#docs"]


def test_scan_paths_discovers_markdown_files_in_directories(tmp_path: Path) -> None:
    docs = tmp_path / "docs"
    docs.mkdir()
    (docs / "usage.md").write_text("할일: 사용법 문서화\n", encoding="utf-8")
    (docs / "ignore.txt").write_text("TODO: Ignore me\n", encoding="utf-8")

    items = scan_paths([docs])

    assert len(items) == 1
    assert items[0].source.name == "usage.md"
