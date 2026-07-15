"""S-Semi PRD의 도메인 엔티티를 표현하는 데이터 모델."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import Enum


class OrderStatus(str, Enum):
    """PRD CHAPTER 1-4에 정의된 주문 상태."""

    RESERVED = "RESERVED"
    REJECTED = "REJECTED"
    PRODUCING = "PRODUCING"
    CONFIRMED = "CONFIRMED"
    RELEASE = "RELEASE"


@dataclass(frozen=True)
class Sample:
    """시료: 시료 ID, 이름, 평균 생산시간, 수율."""

    sample_id: str
    name: str
    avg_production_time: float
    yield_rate: float

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "Sample":
        return cls(**data)


@dataclass(frozen=True)
class Order:
    """시료 주문: 시료 ID, 고객명, 주문 수량, 상태."""

    order_id: str
    sample_id: str
    customer_name: str
    quantity: int
    status: OrderStatus
    created_at: str

    def to_dict(self) -> dict:
        data = asdict(self)
        data["status"] = self.status.value
        return data

    @classmethod
    def from_dict(cls, data: dict) -> "Order":
        data = dict(data)
        data["status"] = OrderStatus(data["status"])
        return cls(**data)


@dataclass(frozen=True)
class InventoryRecord:
    """시료별 재고 수량."""

    sample_id: str
    quantity: int

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "InventoryRecord":
        return cls(**data)


@dataclass(frozen=True)
class ProductionQueueEntry:
    """생산 라인 큐 항목: 재고 부족으로 PRODUCING 전환된 주문의 생산 계획."""

    order_id: str
    sample_id: str
    shortage: int
    actual_quantity: int
    total_production_time: float
    queue_position: int

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "ProductionQueueEntry":
        return cls(**data)
