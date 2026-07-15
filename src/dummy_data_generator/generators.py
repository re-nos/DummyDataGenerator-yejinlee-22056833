"""시료/주문/재고 더미 데이터를 생성하는 함수 모음.

모든 함수는 ``seed``를 통해 재현 가능한 결과를 생성한다. 전역 ``random`` 상태에
의존하지 않고 함수 내부에서 ``random.Random(seed)`` 인스턴스를 사용한다.
"""

from __future__ import annotations

import random
from datetime import datetime, timedelta

from dummy_data_generator.models import InventoryRecord, Order, OrderStatus, Sample

_SAMPLE_NAME_PREFIXES = ["Wafer", "Die", "Chip", "Module", "Sensor"]
_SAMPLE_NAME_SUFFIXES = ["A", "B", "C", "X", "Pro", "Lite"]

_CUSTOMER_POOL = [
    "ETRI 연구소",
    "SK Fab",
    "Seoul Univ. Nano Lab",
    "KAIST 반도체연구실",
    "Fabless Korea",
    "Nexus Semicon",
    "대전 반도체연구원",
]

_ORDER_STATUS_WEIGHTS = {
    OrderStatus.RESERVED: 0.35,
    OrderStatus.CONFIRMED: 0.25,
    OrderStatus.PRODUCING: 0.2,
    OrderStatus.RELEASE: 0.15,
    OrderStatus.REJECTED: 0.05,
}

_ORDER_BASE_TIME = datetime(2026, 1, 1)


def generate_samples(count: int, *, seed: int | None = None) -> list[Sample]:
    """시료 더미 데이터를 ``count``개 생성한다."""
    if count < 0:
        raise ValueError("count는 0 이상이어야 합니다")

    rng = random.Random(seed)
    samples = []
    for i in range(count):
        prefix = rng.choice(_SAMPLE_NAME_PREFIXES)
        suffix = rng.choice(_SAMPLE_NAME_SUFFIXES)
        samples.append(
            Sample(
                sample_id=f"SMP-{i + 1:04d}",
                name=f"{prefix}-{suffix}",
                avg_production_time=round(rng.uniform(5.0, 60.0), 1),
                yield_rate=round(rng.uniform(0.5, 0.99), 2),
            )
        )
    return samples


def generate_orders(
    samples: list[Sample], count: int, *, seed: int | None = None
) -> list[Order]:
    """주어진 시료 목록을 참조하는 주문 더미 데이터를 ``count``개 생성한다."""
    if not samples:
        raise ValueError("samples는 비어있을 수 없습니다")
    if count < 0:
        raise ValueError("count는 0 이상이어야 합니다")

    rng = random.Random(seed)
    statuses = list(_ORDER_STATUS_WEIGHTS.keys())
    weights = list(_ORDER_STATUS_WEIGHTS.values())

    orders = []
    for i in range(count):
        sample = rng.choice(samples)
        created_at = _ORDER_BASE_TIME + timedelta(minutes=rng.randint(0, 10_000))
        orders.append(
            Order(
                order_id=f"ORD-{i + 1:04d}",
                sample_id=sample.sample_id,
                customer_name=rng.choice(_CUSTOMER_POOL),
                quantity=rng.randint(1, 50),
                status=rng.choices(statuses, weights=weights, k=1)[0],
                created_at=created_at.isoformat(),
            )
        )
    return orders


def generate_inventory(
    samples: list[Sample],
    *,
    min_quantity: int = 0,
    max_quantity: int = 100,
    seed: int | None = None,
) -> list[InventoryRecord]:
    """시료별 재고 더미 데이터를 생성한다 (시료당 1건)."""
    if min_quantity < 0 or max_quantity < min_quantity:
        raise ValueError("min_quantity/max_quantity 범위가 올바르지 않습니다")

    rng = random.Random(seed)
    return [
        InventoryRecord(
            sample_id=sample.sample_id,
            quantity=rng.randint(min_quantity, max_quantity),
        )
        for sample in samples
    ]
