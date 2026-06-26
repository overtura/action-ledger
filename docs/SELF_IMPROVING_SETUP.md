# 자가 개선 기능 추가 매뉴얼

이 문서는 `action-ledger`를 `self-improving-maintainer-bot`의 target repo로
연결하는 절차입니다. 목표는 이 레포의 문서, eval, 작은 코드 개선 작업을 로컬
Codex 앱으로 반복 실행하는 것입니다.

## 전체 흐름

```text
action-ledger 문서/eval 확인
  -> maintainer bot .env에 target repo 등록
  -> target 전용 eval 실행
  -> Codex task 생성
  -> 로컬 Codex로 target repo 수정
  -> 사람이 diff 검토
  -> 한국어 커밋/PR 작성
```

## 1. 준비물

- 로컬에 `self-improving-maintainer-bot` repo가 있어야 합니다.
- 로컬에 이 `action-ledger` repo가 있어야 합니다.
- Codex 앱 또는 Codex CLI가 로그인되어 있어야 합니다.
- GitHub에 자동 PR을 만들려면 maintainer bot repo에 `BOT_GITHUB_TOKEN` secret이
  필요합니다.

Codex 로그인 확인:

```powershell
cd "E:\Project Archieve\self-improving-maintainer-bot"
python -m self_maintainer_bot.cli codex-status
```

정상 출력 예:

```text
PASS codex-cli: ...
PASS codex-login: Logged in using ChatGPT
```

## 2. maintainer bot에 target 등록

`self-improving-maintainer-bot`의 `.env`를 엽니다. 없으면 먼저 만듭니다.

```powershell
Copy-Item .env.example .env
```

로컬 `action-ledger`를 바로 target으로 쓰려면 다음처럼 설정합니다.

```env
TARGET_REPOSITORY=local/action-ledger
TARGET_DEFAULT_BRANCH=main
TARGET_WORKTREE=E:\Project Archieve\action-ledger
TARGET_DOC_PATHS=README.md,docs
TARGET_EVALS_PATH=evals/docs_qa.jsonl
CODEX_TIMEOUT_SECONDS=3600
```

GitHub에 `overtura/action-ledger`로 올린 뒤에는 다음처럼 바꿉니다.

```env
TARGET_REPOSITORY=overtura/action-ledger
TARGET_DEFAULT_BRANCH=main
TARGET_WORKTREE=targets/action-ledger
TARGET_DOC_PATHS=README.md,docs
TARGET_EVALS_PATH=evals/docs_qa.jsonl
CODEX_TIMEOUT_SECONDS=3600
```

## 3. target 상태 확인

로컬 경로 target을 쓰는 경우에는 clone이 필요 없습니다.

```powershell
python -m self_maintainer_bot.cli target-status
```

확인할 항목:

- `Repository`가 `local/action-ledger` 또는 `overtura/action-ledger`인지 확인합니다.
- `Doc files`가 1개 이상인지 확인합니다.
- `Eval file exists`가 `yes`인지 확인합니다.

GitHub repo target을 쓰는 경우에는 먼저 target을 준비합니다.

```powershell
python -m self_maintainer_bot.cli prepare-target
python -m self_maintainer_bot.cli target-status
```

## 4. target 전용 eval 실행

```powershell
python -m self_maintainer_bot.cli validate-evals
python -m self_maintainer_bot.cli eval-docs --fail-under 1
```

이 레포의 기본 eval은 `evals/docs_qa.jsonl`에 있습니다. 정상이라면 `5/5 passed`
처럼 모든 case가 통과해야 합니다.

eval이 실패하면 먼저 다음을 확인합니다.

- README나 `docs/`에 기대 답변이 실제로 있는가?
- `must_include`가 너무 엄격하지 않은가?
- `must_not_include`가 정상 답변까지 막지 않는가?

## 5. Codex task 생성

먼저 실행 없이 task만 만듭니다.

```powershell
python -m self_maintainer_bot.cli codex-local-loop --scope docs
```

생성되는 task는 `self-improving-maintainer-bot\runs\codex-tasks\` 아래에 저장됩니다.
task 내용을 보고 범위가 맞으면 실제 실행합니다.

```powershell
python -m self_maintainer_bot.cli codex-local-loop --scope docs --execute
```

또는 PowerShell wrapper를 사용합니다.

```powershell
.\scripts\codex-local-loop.ps1 -Scope docs -Execute
```

## 6. 권장 scope

- `docs`: README, docs 문서 개선
- `evals`: eval case 추가 또는 보정
- `prompts`: maintainer bot prompt 개선
- `code`: CLI나 parser 같은 코드 개선
- `mixed`: 문서, eval, 코드가 같이 필요한 작업

처음에는 `docs`만 사용하세요. `code`나 `mixed`는 diff가 커지기 쉽습니다.

## 7. 변경 검토

Codex 실행 후 `action-ledger` repo에서 diff를 확인합니다.

```powershell
cd "E:\Project Archieve\action-ledger"
git status --short
git diff
python -m pytest
action-ledger scan README.md docs --format markdown --max-open 20
```

검토 기준:

- 사용자에게 보이는 문구는 한국어인가?
- 커밋 설명과 PR 설명도 한국어로 작성할 수 있는 변경인가?
- CLI 옵션명과 JSON 키는 기존 호환성을 유지하는가?
- 생성된 report 파일이 커밋 대상에 들어가지 않았는가?

## 8. 한국어 커밋 작성

커밋 메시지는 한국어를 기본으로 합니다.

```powershell
git add README.md docs evals src tests
git commit -m "[docs] 사용 가이드 예시 보강

- PowerShell 실행 예시를 추가
- Markdown 보고서 설명을 보강
- pytest와 CLI smoke test로 검증"
```

기능 변경이면:

```powershell
git commit -m "[feat] 태그 필터 기능 추가

- --tag 옵션으로 특정 태그만 출력하도록 구현
- parser 결과 필터링 테스트 추가
- pytest로 회귀 검증"
```

## 9. 한국어 PR 작성

PR 제목 예:

```text
[docs] PowerShell 사용 예시 보강
```

PR 본문 기본 구조:

```markdown
## 목적

Windows 사용자가 바로 따라 할 수 있도록 PowerShell 예시를 보강합니다.

## 주요 변경

- `docs/USAGE.md`에 PowerShell 실행 예시 추가
- README의 자가 개선 안내 링크 정리

## 검증

- `python -m pytest`
- `action-ledger scan README.md docs --format markdown --max-open 20`

## 남은 위험

- 실제 GitHub Actions 환경에서는 별도 확인이 필요합니다.
```

## 10. 반복 운영 루틴

```powershell
# maintainer bot repo
python -m self_maintainer_bot.cli target-status
python -m self_maintainer_bot.cli eval-docs --fail-under 0
python -m self_maintainer_bot.cli codex-local-loop --scope docs
python -m self_maintainer_bot.cli codex-local-loop --scope docs --execute

# action-ledger repo
git status --short
git diff
python -m pytest
action-ledger scan README.md docs --format markdown --max-open 20
```

초기에는 사람이 매번 diff를 읽고 커밋/PR을 만듭니다. 자동 커밋이나 자동 merge는
충분히 안정화된 뒤에만 고려하세요.
