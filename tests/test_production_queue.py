import math

import pytest

from dummy_data_generator.generators import generate_production_queue
from dummy_data_generator.models import Order, OrderStatus, Sample

SAMPLE = Sample(
    sample_id="SMP-0001",
    name="Wafer-A",
    avg_production_time=10.0,
    yield_rate=0.5,
)


def _order(order_id, status, quantity, created_at):
    return Order(
        order_id=order_id,
        sample_id=SAMPLE.sample_id,
        customer_name="Acme Labs",
        quantity=quantity,
        status=status,
        created_at=created_at,
    )


def test_only_producing_orders_are_queued():
    orders = [
        _order("ORD-1", OrderStatus.RESERVED, 10, "2026-01-01T00:00:00"),
        _order("ORD-2", OrderStatus.PRODUCING, 10, "2026-01-01T00:01:00"),
        _order("ORD-3", OrderStatus.CONFIRMED, 10, "2026-01-01T00:02:00"),
    ]

    queue = generate_production_queue(orders, [SAMPLE], seed=1)

    assert len(queue) == 1
    assert queue[0].order_id == "ORD-2"


def test_queue_follows_fifo_order_by_created_at():
    orders = [
        _order("ORD-2", OrderStatus.PRODUCING, 5, "2026-01-01T00:05:00"),
        _order("ORD-1", OrderStatus.PRODUCING, 5, "2026-01-01T00:01:00"),
        _order("ORD-3", OrderStatus.PRODUCING, 5, "2026-01-01T00:10:00"),
    ]

    queue = generate_production_queue(orders, [SAMPLE], seed=1)

    assert [entry.order_id for entry in queue] == ["ORD-1", "ORD-2", "ORD-3"]
    assert [entry.queue_position for entry in queue] == [0, 1, 2]


def test_actual_quantity_and_total_time_follow_prd_formula():
    orders = [_order("ORD-1", OrderStatus.PRODUCING, 20, "2026-01-01T00:00:00")]

    queue = generate_production_queue(orders, [SAMPLE], seed=7)

    entry = queue[0]
    expected_actual_quantity = math.ceil(entry.shortage / SAMPLE.yield_rate)
    expected_total_time = round(
        SAMPLE.avg_production_time * expected_actual_quantity, 1
    )

    assert 1 <= entry.shortage <= 20
    assert entry.actual_quantity == expected_actual_quantity
    assert entry.total_production_time == expected_total_time


def test_unknown_sample_id_raises_value_error():
    orders = [_order("ORD-1", OrderStatus.PRODUCING, 5, "2026-01-01T00:00:00")]

    with pytest.raises(ValueError):
        generate_production_queue(orders, [], seed=1)
