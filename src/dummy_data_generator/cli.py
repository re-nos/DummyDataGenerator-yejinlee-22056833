"""더미 데이터 생성 CLI 진입점."""

from __future__ import annotations

import argparse
from pathlib import Path

from dummy_data_generator.generators import (
    generate_inventory,
    generate_orders,
    generate_production_queue,
    generate_samples,
)
from dummy_data_generator.persistence import write_dataset


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="dummy-data-gen",
        description="S-Semi 시료 생산주문관리 시스템용 테스트 더미 데이터 생성기",
    )
    parser.add_argument(
        "--samples", type=int, default=10, help="생성할 시료 개수 (기본값: 10)"
    )
    parser.add_argument(
        "--orders", type=int, default=30, help="생성할 주문 개수 (기본값: 30)"
    )
    parser.add_argument(
        "--inventory-min",
        type=int,
        default=0,
        help="시료별 재고 최소 수량 (기본값: 0)",
    )
    parser.add_argument(
        "--inventory-max",
        type=int,
        default=100,
        help="시료별 재고 최대 수량 (기본값: 100)",
    )
    parser.add_argument(
        "--seed", type=int, default=None, help="재현 가능한 결과를 위한 랜덤 시드"
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("data"),
        help="생성된 JSON 파일을 저장할 디렉토리 (기본값: data)",
    )
    return parser


def run(args: argparse.Namespace) -> dict[str, int]:
    samples = generate_samples(args.samples, seed=args.seed)
    orders = generate_orders(samples, args.orders, seed=args.seed)
    inventory = generate_inventory(
        samples,
        min_quantity=args.inventory_min,
        max_quantity=args.inventory_max,
        seed=args.seed,
    )
    production_queue = generate_production_queue(orders, samples, seed=args.seed)

    write_dataset(
        args.output_dir,
        samples=samples,
        orders=orders,
        inventory=inventory,
        production_queue=production_queue,
    )

    return {
        "samples": len(samples),
        "orders": len(orders),
        "inventory": len(inventory),
        "production_queue": len(production_queue),
    }


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    summary = run(args)

    print(f"더미 데이터 생성 완료: {args.output_dir}")
    for key, count in summary.items():
        print(f"  - {key}: {count}건")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
