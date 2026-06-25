from pathlib import Path

from action_ledger.cli import main


def test_scan_json_output_file(tmp_path: Path) -> None:
    notes = tmp_path / "notes.md"
    output = tmp_path / "report.json"
    notes.write_text("- [ ] Ship the first release #release\n", encoding="utf-8")

    code = main(["scan", str(notes), "--format", "json", "--output", str(output)])

    assert code == 0
    report = output.read_text(encoding="utf-8")
    assert '"total": 1' in report
    assert '"#release"' in report


def test_max_open_returns_failure_when_threshold_is_exceeded(tmp_path: Path) -> None:
    notes = tmp_path / "notes.md"
    notes.write_text("- [ ] One\n- [ ] Two\n", encoding="utf-8")

    code = main(["scan", str(notes), "--max-open", "1"])

    assert code == 1


def test_markdown_output_uses_korean_labels(tmp_path: Path, capsys) -> None:
    notes = tmp_path / "notes.md"
    notes.write_text("할일: 한국어 보고서 확인 #docs\n", encoding="utf-8")

    code = main(["scan", str(notes), "--format", "markdown"])

    captured = capsys.readouterr()
    assert code == 0
    assert "# 액션 레저 보고서" in captured.out
    assert "| 열림 | 할일 |" in captured.out
