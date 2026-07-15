from dummy_data_generator.models import (
    InventoryRecord,
    Order,
    OrderStatus,
    ProductionQueueEntry,
    Sample,
)


def test_sample_to_dict_and_back():
    sample = Sample(
        sample_id="SMP-0001",
        name="Wafer-A",
        avg_production_time=12.5,
        yield_rate=0.92,
    )

    data = sample.to_dict()

    assert data == {
        "sample_id": "SMP-0001",
        "name": "Wafer-A",
        "avg_production_time": 12.5,
        "yield_rate": 0.92,
    }
    assert Sample.from_dict(data) == sample


def test_order_to_dict_serializes_status_as_string():
    order = Order(
        order_id="ORD-0001",
        sample_id="SMP-0001",
        customer_name="Acme Labs",
        quantity=10,
        status=OrderStatus.RESERVED,
        created_at="2026-01-01T00:00:00",
    )

    data = order.to_dict()

    assert data["status"] == "RESERVED"
    assert Order.from_dict(data) == order


def test_inventory_record_round_trip():
    record = InventoryRecord(sample_id="SMP-0001", quantity=42)

    assert InventoryRecord.from_dict(record.to_dict()) == record


def test_production_queue_entry_round_trip():
    entry = ProductionQueueEntry(
        order_id="ORD-0001",
        sample_id="SMP-0001",
        shortage=8,
        actual_quantity=9,
        total_production_time=112.5,
        queue_position=0,
    )

    assert ProductionQueueEntry.from_dict(entry.to_dict()) == entry
