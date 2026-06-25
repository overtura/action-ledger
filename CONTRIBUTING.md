# 기여 가이드

## 로컬 설정

```bash
python -m pip install -e ".[dev]"
python -m pytest
```

## PR 체크리스트

- [ ] `action-ledger scan README.md docs`가 계속 동작합니다.
- [ ] `python -m pytest`가 통과합니다.
- [ ] 동작 변경이 있으면 문서를 갱신했습니다.
- [ ] 생성된 보고서를 커밋하지 않았습니다.
- [ ] 커밋 제목, 커밋 본문, PR 제목, PR 본문을 한국어로 작성했습니다.
