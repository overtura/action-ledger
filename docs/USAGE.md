# 사용 가이드

액션 레저는 Markdown 파일과 디렉터리를 스캔합니다.

## 파일 스캔

```bash
action-ledger scan README.md docs/USAGE.md
```

## 디렉터리 스캔

```bash
action-ledger scan docs
```

디렉터리는 재귀적으로 검색하며 `*.md` 파일만 읽습니다. 숨겨진 `.git`
디렉터리는 건너뜁니다.

## JSON 출력

```bash
action-ledger scan README.md docs --format json --output action-ledger-report.json
```

JSON 보고서는 자동화 호환성을 위해 영어 키와 상태 값을 유지합니다.

- `summary`: 전체 집계
- `items`: 개별 작업 항목
- `source`: 파일 경로
- `line`: 줄 번호
- `kind`: `task`, `todo`, `fixme`, `decision`
- `status`: `open`, `done`, `recorded`
- `text`: 항목 내용
- `tags`: `#docs` 같은 태그 목록
- `owner`: `@owner` 같은 담당자

## Markdown 출력

```bash
action-ledger scan README.md docs --format markdown
```

Markdown 출력은 이슈, PR, 릴리스 노트, 운영 문서에 붙여 넣기 좋습니다.
기본 문구와 표 제목은 한국어로 렌더링됩니다.

## CI 기준

```bash
action-ledger scan README.md docs --max-open 10
```

`--max-open`을 지정하면 열린 작업 수가 기준보다 많을 때 명령이 종료 코드
`1`로 실패합니다.

## PowerShell 예시

```powershell
action-ledger scan README.md docs --format markdown
action-ledger scan README.md docs --format json --output action-ledger-report.json
```

할일: `--tag` 필터가 추가되면 태그별 예시를 보강합니다 #docs
