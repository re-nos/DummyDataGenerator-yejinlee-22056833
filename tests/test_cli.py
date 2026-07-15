from dummy_data_generator.cli import main
from dummy_data_generator.persistence import (
    INVENTORY_FILENAME,
    ORDERS_FILENAME,
    PRODUCTION_QUEUE_FILENAME,
    SAMPLES_FILENAME,
    read_dataset,
)


def test_main_generates_dataset_with_requested_counts(tmp_path):
    output_dir = tmp_path / "out"

    exit_code = main(
        [
            "--samples",
            "5",
            "--orders",
            "20",
            "--seed",
            "1",
            "--output-dir",
            str(output_dir),
        ]
    )

    assert exit_code == 0
    assert (output_dir / SAMPLES_FILENAME).exists()
    assert (output_dir / ORDERS_FILENAME).exists()
    assert (output_dir / INVENTORY_FILENAME).exists()
    assert (output_dir / PRODUCTION_QUEUE_FILENAME).exists()

    dataset = read_dataset(output_dir)
    assert len(dataset["samples"]) == 5
    assert len(dataset["orders"]) == 20
    assert len(dataset["inventory"]) == 5


def test_main_is_deterministic_given_same_seed(tmp_path):
    first_dir = tmp_path / "first"
    second_dir = tmp_path / "second"

    main(["--samples", "5", "--orders", "10", "--seed", "42", "--output-dir", str(first_dir)])
    main(["--samples", "5", "--orders", "10", "--seed", "42", "--output-dir", str(second_dir)])

    assert read_dataset(first_dir) == read_dataset(second_dir)


def test_main_prints_summary(tmp_path, capsys):
    main(
        [
            "--samples",
            "3",
            "--orders",
            "5",
            "--seed",
            "1",
            "--output-dir",
            str(tmp_path / "out"),
        ]
    )

    captured = capsys.readouterr()
    assert "samples: 3건" in captured.out
    assert "orders: 5건" in captured.out
