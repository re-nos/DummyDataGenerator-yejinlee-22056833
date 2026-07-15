from dummy_data_generator.generators import (
    generate_inventory,
    generate_orders,
    generate_production_queue,
    generate_samples,
)
from dummy_data_generator.persistence import (
    INVENTORY_FILENAME,
    ORDERS_FILENAME,
    PRODUCTION_QUEUE_FILENAME,
    SAMPLES_FILENAME,
    read_dataset,
    write_dataset,
)


def test_write_dataset_creates_expected_files(tmp_path):
    samples = generate_samples(5, seed=1)
    orders = generate_orders(samples, 10, seed=2)
    inventory = generate_inventory(samples, seed=3)
    production_queue = generate_production_queue(orders, samples, seed=4)

    write_dataset(
        tmp_path,
        samples=samples,
        orders=orders,
        inventory=inventory,
        production_queue=production_queue,
    )

    assert (tmp_path / SAMPLES_FILENAME).exists()
    assert (tmp_path / ORDERS_FILENAME).exists()
    assert (tmp_path / INVENTORY_FILENAME).exists()
    assert (tmp_path / PRODUCTION_QUEUE_FILENAME).exists()


def test_write_then_read_dataset_round_trip(tmp_path):
    samples = generate_samples(5, seed=1)
    orders = generate_orders(samples, 10, seed=2)
    inventory = generate_inventory(samples, seed=3)
    production_queue = generate_production_queue(orders, samples, seed=4)

    write_dataset(
        tmp_path,
        samples=samples,
        orders=orders,
        inventory=inventory,
        production_queue=production_queue,
    )
    loaded = read_dataset(tmp_path)

    assert loaded["samples"] == samples
    assert loaded["orders"] == orders
    assert loaded["inventory"] == inventory
    assert loaded["production_queue"] == production_queue


def test_write_dataset_creates_output_dir_if_missing(tmp_path):
    output_dir = tmp_path / "nested" / "data"
    samples = generate_samples(2, seed=1)

    write_dataset(
        output_dir,
        samples=samples,
        orders=[],
        inventory=[],
        production_queue=[],
    )

    assert output_dir.exists()
    assert (output_dir / SAMPLES_FILENAME).exists()
