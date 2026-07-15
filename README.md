# Dummy Data Generator

S-Semi 시료 생산주문관리 시스템의 테스트/개발용 더미 데이터를 생성하는 CLI 도구입니다.
시료(Sample), 주문(Order), 재고(InventoryRecord), 생산 큐(ProductionQueueEntry) 데이터를
JSON 파일로 생성합니다.

## 설치

```bash
python -m venv .venv
.venv/Scripts/activate       # Windows
# source .venv/bin/activate  # macOS/Linux

pip install -e ".[dev]"
```

## 사용법

콘솔 스크립트로 실행:

```bash
dummy-data-gen --samples 10 --orders 30 --seed 42 --output-dir data
```

또는 모듈로 직접 실행:

```bash
python -m dummy_data_generator.cli --samples 10 --orders 30 --seed 42 --output-dir data
```

### 옵션

| 옵션 | 설명 | 기본값 |
|------|------|--------|
| `--samples` | 생성할 시료 개수 | `10` |
| `--orders` | 생성할 주문 개수 | `30` |
| `--inventory-min` | 시료별 재고 최소 수량 | `0` |
| `--inventory-max` | 시료별 재고 최대 수량 | `100` |
| `--seed` | 재현 가능한 결과를 위한 랜덤 시드 (미지정 시 매번 다른 결과) | `None` |
| `--output-dir` | 생성된 JSON 파일을 저장할 디렉토리 | `data` |

### 출력 파일

`--output-dir` 하위에 다음 4개 JSON 파일이 생성됩니다.

- `samples.json`: 시료 목록 (시료 ID, 이름, 평균 생산시간, 수율)
- `orders.json`: 주문 목록 (주문 ID, 시료 ID, 고객명, 수량, 상태, 생성일시)
- `inventory.json`: 시료별 재고 수량
- `production_queue.json`: `PRODUCING` 상태 주문에 대한 FIFO 생산 큐
  (부족분, 실 생산량, 총 생산시간)

## 테스트

```bash
pytest
```

## 프로젝트 구조

```
src/dummy_data_generator/
  models.py        # Sample, Order, InventoryRecord, ProductionQueueEntry 도메인 모델
  generators.py     # seed 기반 더미 데이터 생성 함수
  persistence.py    # JSON 저장/로드
  cli.py            # dummy-data-gen 콘솔 진입점
tests/               # pytest 테스트
```

자세한 도메인 규칙(주문 상태 흐름, 생산량 계산식 등)은 `S_Semi_Project_PRD.md`를 참고하세요.
