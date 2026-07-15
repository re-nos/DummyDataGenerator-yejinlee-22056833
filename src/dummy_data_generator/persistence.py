"""생성된 더미 데이터를 JSON 파일로 저장/로드하는 모듈."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable, TypeVar

from dummy_data_generator.models import (
    InventoryRecord,
    Order,
    ProductionQueueEntry,
    Sample,
)

T = TypeVar("T")

SAMPLES_FILENAME = "samples.json"
ORDERS_FILENAME = "orders.json"
INVENTORY_FILENAME = "inventory.json"
PRODUCTION_QUEUE_FILENAME = "production_queue.json"


def write_json(path: Path, items: Iterable) -> None:
    """to_dict()를 지원하는 모델 목록을 JSON 파일로 저장한다."""
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = [item.to_dict() for item in items]
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def read_json(path: Path, model_cls: type[T]) -> list[T]:
    """write_json으로 저장된 JSON 파일을 모델 목록으로 읽어온다."""
    payload = json.loads(path.read_text(encoding="utf-8"))
    return [model_cls.from_dict(item) for item in payload]


def write_dataset(
    output_dir: Path,
    *,
    samples: list[Sample],
    orders: list[Order],
    inventory: list[InventoryRecord],
    production_queue: list[ProductionQueueEntry],
) -> None:
    """더미 데이터 전체를 output_dir 하위 JSON 파일들로 저장한다."""
    output_dir = Path(output_dir)
    write_json(output_dir / SAMPLES_FILENAME, samples)
    write_json(output_dir / ORDERS_FILENAME, orders)
    write_json(output_dir / INVENTORY_FILENAME, inventory)
    write_json(output_dir / PRODUCTION_QUEUE_FILENAME, production_queue)


def read_dataset(output_dir: Path) -> dict[str, list]:
    """write_dataset으로 저장된 더미 데이터 전체를 읽어온다."""
    output_dir = Path(output_dir)
    return {
        "samples": read_json(output_dir / SAMPLES_FILENAME, Sample),
        "orders": read_json(output_dir / ORDERS_FILENAME, Order),
        "inventory": read_json(output_dir / INVENTORY_FILENAME, InventoryRecord),
        "production_queue": read_json(
            output_dir / PRODUCTION_QUEUE_FILENAME, ProductionQueueEntry
        ),
    }
