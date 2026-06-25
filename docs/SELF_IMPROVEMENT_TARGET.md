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

## 한국어 운영 기준

자가 개선 작업에서 생성되는 요약, 커밋 설명, PR 설명은 한국어로 작성합니다.
CLI 명령어와 JSON 키는 기존 사용자를 깨뜨리지 않기 위해 영어를 유지합니다.

수정: fork를 대상으로 먼저 실행하는 예시를 추가합니다.
