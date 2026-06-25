# 자가 개선 target 메모

이 레포는 maintainer/docs bot을 실제로 테스트하기 위한 target repo입니다.

## 테스트 target으로 적합한 이유

- 테스트 가능한 실제 CLI가 있습니다.
- 문서가 짧아서 안전하게 개선할 수 있습니다.
- `evals/docs_qa.jsonl`에 target 전용 문서 eval이 있습니다.
- 일부 문서 개선 여지를 의도적으로 남겨두었습니다.
- 커밋 설명과 PR 설명의 기본 언어가 한국어로 정의되어 있습니다.

## 권장 bot 루프

```bash
python -m self_maintainer_bot.cli prepare-target
python -m self_maintainer_bot.cli target-status
python -m self_maintainer_bot.cli eval-docs --fail-under 0
python -m self_maintainer_bot.cli codex-local-loop --scope docs
```

## eval이 모두 통과했을 때

실패한 eval case가 없으면 큰 기능 변경보다 no-op 판단이나 낮은 위험의 문서 정리를
우선합니다. 이 경우 eval case를 약화하거나 삭제하지 말고, 최신 리포트가 어떤
문서 근거로 통과했는지만 확인합니다.

최소 확인 항목:

- 최신 리포트의 모든 case가 `passed: true`인지 확인합니다.
- `missing`과 `forbidden`이 비어 있으면 eval 조정 없이 문서 근거만 기록합니다.
- PowerShell에서 리포트를 직접 볼 때는 `Get-Content -Encoding UTF8`처럼 인코딩을 지정합니다.
- 한국어 출력이 깨져 보이면 `passed`, `missing`, `forbidden` 필드를 먼저 확인하고,
  답변 근거는 README와 `docs/`의 실제 문장으로 대조합니다.
- 개선 여지가 분명하지 않으면 작업을 no-op으로 종료할 수 있습니다.
- no-op으로 종료하더라도 확인한 리포트, 실행한 검증, 남은 위험은 작업 요약에 남깁니다.

## 한국어 운영 기준

자가 개선 작업에서 생성되는 요약, 커밋 설명, PR 설명은 한국어로 작성합니다.
CLI 명령어와 JSON 키는 기존 사용자를 깨뜨리지 않기 위해 영어를 유지합니다.
PR 본문은 `목적`, `주요 변경`, `검증`, `남은 위험` 순서로 정리합니다.

fork target으로 먼저 실행하는 예시는 README의 개선 후보에 기록되어 있습니다.
