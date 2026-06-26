# 액션 레저

액션 레저(Action Ledger)는 Markdown 문서, 회의록, README에 흩어진 작업 항목을
스캔하는 작은 CLI입니다. 체크박스, `TODO`, `FIXME`, `DECISION`과 한국어 별칭
`할일`, `수정`, `결정`을 찾아 사람이 읽기 쉬운 보고서나 자동화용 JSON으로
정리합니다.

이런 질문에 빠르게 답하고 싶을 때 사용합니다.

- 아직 열려 있는 작업은 무엇인가?
- 어떤 문서에 후속 작업이 남아 있는가?
- 어떤 결정이 기록되었는가?
- 열린 작업이 너무 많으면 CI를 실패시킬 수 있는가?

## 설치

```bash
python -m pip install -e .
```

개발 도구까지 설치하려면:

```bash
python -m pip install -e ".[dev]"
```

## 빠른 시작

현재 레포를 스캔합니다.

```bash
action-ledger scan README.md docs
```

자동화용 JSON을 작성합니다.

```bash
action-ledger scan README.md docs --format json --output action-ledger-report.json
```

열린 작업이 기준을 넘으면 CI를 실패시킵니다.

```bash
action-ledger scan README.md docs --max-open 10
```

## 지원하는 Markdown 패턴

체크박스 작업:

```markdown
- [ ] 릴리스 노트 발행 #release @owner
- [x] 온보딩 문서 업데이트 #docs
```

영어 마커:

```markdown
TODO: Windows 설치 예시 추가 #docs
FIXME: 임시 벤치마크 수치 교체
DECISION: 첫 버전은 의존성 없이 유지
```

한국어 마커:

```markdown
할일: PowerShell 예시 추가 #docs
수정: 오래된 출력 예시 갱신
결정: JSON 키는 자동화 호환성을 위해 영어로 유지
```

액션 레저는 `@owner` 같은 담당자와 `#docs` 같은 태그를 추출합니다.

## CLI

```text
action-ledger scan PATH [PATH ...] [--format table|json|markdown] [--output FILE] [--max-open N]
```

출력 형식:

- `table`: 기본 터미널 보고서
- `json`: 자동화용 JSON 보고서
- `markdown`: 이슈, PR, 문서에 붙여 넣기 좋은 Markdown 보고서

종료 코드:

- `0`: 스캔 성공, 열린 작업 수가 `--max-open` 기준 이하
- `1`: 스캔 성공, 열린 작업 수가 `--max-open` 기준 초과
- `2`: 명령 사용 오류

## 한국어 자가 개선 기준

이 레포는 self-improving maintainer bot의 테스트 대상입니다. 자가 개선 작업은
한국어 기준으로 작성합니다.

- 커밋 제목과 본문은 한국어로 작성합니다.
- PR 제목과 설명은 한국어로 작성합니다.
- Codex 작업 요약, 검증 결과, 남은 위험도 한국어로 작성합니다.
- Conventional 타입은 유지해도 됩니다. 예: `[feat] 태그 필터 문서 추가`
- CLI 명령어, 옵션명, JSON 키는 호환성을 위해 영어를 유지합니다.

권장 PR 설명 구조:

```markdown
## 목적

## 주요 변경

## 검증

## 남은 위험
```

## Self-Improvement Target

이 레포는 eval 기반 maintainer/docs bot의 target으로 쓰기 좋게 작게 구성되어
있습니다. 실제 CLI가 있고, 문서가 짧으며, target 전용 문서 eval이 포함되어
있습니다.

처음 연결할 때는 [자가 개선 기능 추가 매뉴얼](docs/SELF_IMPROVING_SETUP.md)을
따라 하세요.

권장 target 설정:

```env
TARGET_REPOSITORY=overtura/action-ledger
TARGET_DEFAULT_BRANCH=main
TARGET_WORKTREE=targets/action-ledger
TARGET_DOC_PATHS=README.md,docs
TARGET_EVALS_PATH=evals/docs_qa.jsonl
```

처음 시도하기 좋은 개선 작업:

- GitHub Actions 사용 예시 문서 추가
- `--format markdown` 출력 예시를 실제 표 형태로 보강
- fork target으로 먼저 실행하는 자가 개선 예시 추가
- `P1`, `P2` 같은 우선순위 마커 지원 검토

## 개발

```bash
python -m pip install -e ".[dev]"
python -m pytest
action-ledger scan README.md docs --format markdown
```

## 라이선스

MIT
