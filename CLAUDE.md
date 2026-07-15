# CLAUDE.md

이 파일은 Claude Code가 이 저장소에서 작업할 때 참고하는 가이드입니다.

## 커밋 컨벤션

[Conventional Commits](https://www.conventionalcommits.org/) 형식을 따릅니다.

```
<type>(<scope>): <subject>

<body>

<footer>
```

### type

| type | 설명 |
|------|------|
| `feat` | 새로운 기능 추가 |
| `fix` | 버그 수정 |
| `docs` | 문서 수정 |
| `style` | 코드 포맷팅, 세미콜론 등 (기능 변경 없음) |
| `refactor` | 코드 리팩토링 (기능 변경 없음) |
| `test` | 테스트 코드 추가/수정 |
| `chore` | 빌드 설정, 패키지 매니저 설정 등 |
| `perf` | 성능 개선 |

### scope

변경된 모듈, 기능, 파일 범위를 간단히 명시 (예: `generator`, `config`, `cli`)

### subject

- 한글 또는 영문으로 작성, 한 줄 요약
- 마침표 없이 작성
- 명령형으로 작성 (예: "추가함" 대신 "추가")

### 예시

```
feat(generator): 사용자 더미 데이터 생성 기능 추가

fix(cli): 옵션 파싱 시 발생하는 인덱스 오류 수정

docs: README에 사용법 예시 추가

refactor(config): 설정 로딩 로직 단순화
```

### body (선택)

- 무엇을, 왜 변경했는지 설명 (어떻게는 코드로 확인 가능하므로 생략)
- 72자 내에서 줄바꿈

### footer (선택)

- 이슈 참조: `Closes #123`
- Breaking Change 명시: `BREAKING CHANGE: <설명>`
