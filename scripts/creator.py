"""Launch interactive editor for world files."""

from __future__ import annotations

import argparse

from segmentation_core import run_editor


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Segmentation world editor.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--load",
        type=str,
        help="Path to an existing world file to load.",
    )
    group.add_argument(
        "--size",
        type=str,
        help="Dimensions of a new empty world, as WIDTHxHEIGHT (e.g., 20x15)",
    )
    parser.add_argument(
        "--out",
        type=str,
        default=None,
        help="Save path used when pressing 'S'. Can be edited in GUI",
    )
    return parser


def main() -> None:
    args = build_arg_parser().parse_args()
    run_editor(load=args.load, size=args.size, out=args.out)


if __name__ == "__main__":
    main()
