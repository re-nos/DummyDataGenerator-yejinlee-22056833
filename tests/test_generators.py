import pytest

from dummy_data_generator.generators import (
    generate_inventory,
    generate_orders,
    generate_samples,
)
from dummy_data_generator.models import OrderStatus


def test_generate_samples_count_and_uniqueness():
    samples = generate_samples(10, seed=1)

    assert len(samples) == 10
    assert len({s.sample_id for s in samples}) == 10


def test_generate_samples_yield_rate_and_time_within_range():
    samples = generate_samples(50, seed=1)

    for sample in samples:
        assert 0 < sample.yield_rate <= 1
        assert sample.avg_production_time > 0


def test_generate_samples_is_deterministic_given_same_seed():
    assert generate_samples(20, seed=42) == generate_samples(20, seed=42)


def test_generate_samples_rejects_negative_count():
    with pytest.raises(ValueError):
        generate_samples(-1, seed=1)


def test_generate_orders_references_existing_samples():
    samples = generate_samples(5, seed=1)
    orders = generate_orders(samples, 30, seed=2)

    sample_ids = {s.sample_id for s in samples}
    assert len(orders) == 30
    assert all(order.sample_id in sample_ids for order in orders)
    assert all(order.quantity > 0 for order in orders)
    assert all(isinstance(order.status, OrderStatus) for order in orders)


def test_generate_orders_requires_samples():
    with pytest.raises(ValueError):
        generate_orders([], 10, seed=1)


def test_generate_orders_is_deterministic_given_same_seed():
    samples = generate_samples(5, seed=1)

    assert generate_orders(samples, 10, seed=99) == generate_orders(
        samples, 10, seed=99
    )


def test_generate_inventory_one_record_per_sample():
    samples = generate_samples(7, seed=1)
    inventory = generate_inventory(samples, seed=3)

    assert len(inventory) == 7
    assert {r.sample_id for r in inventory} == {s.sample_id for s in samples}
    assert all(r.quantity >= 0 for r in inventory)


def test_generate_inventory_respects_quantity_bounds():
    samples = generate_samples(20, seed=1)
    inventory = generate_inventory(samples, min_quantity=10, max_quantity=15, seed=5)

    assert all(10 <= r.quantity <= 15 for r in inventory)


def test_generate_inventory_rejects_invalid_bounds():
    samples = generate_samples(3, seed=1)
    with pytest.raises(ValueError):
        generate_inventory(samples, min_quantity=10, max_quantity=5)
