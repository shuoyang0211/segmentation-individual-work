"""
Launches the interactive world editor for creating and editing `.world`
board files. This is a thin CLI wrapper around the Bevy-based editor
provided by `segmentation_core`.

Usage examples:
    # Edit an existing board file
    uv run scripts/creator.py --load worlds/small.world

    # Create a new blank board (20x15) and save to a path when pressing 'S'
    uv run scripts/creator.py --size 20x15 --out worlds/new_level.world

Controls (inside the editor window):
    Mouse:
      - Left-click / drag: paint with the selected tool
    Tools:
      - E: place Empty
      - W: place Wall
      - A or 1: place Player 1 start [only one on the board]
      - B or 2: place Player 2 start [only one on the board]
    Other:
      - S: save (to --out if provided; otherwise to --load path, or a default name)
      - Tab: edit the save path
      - G: toggle grid lines
      - +/-: zoom
      - Esc: quit
"""

from __future__ import annotations

import argparse

from segmentation_core import run_editor


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Bevy world editor.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--load",
        type=str,
        help="path to an existing .world file to load",
    )
    group.add_argument(
        "--size",
        type=str,
        help="dimensions of a new empty board, formatted as WIDTHxHEIGHT (e.g., 20x15)",
    )
    parser.add_argument(
        "--out",
        type=str,
        default=None,
        help="save path used when pressing 'S'. if omitted, falls back to --load, then a default name",
    )
    return parser


def main() -> None:
    args = build_arg_parser().parse_args()
    run_editor(load=args.load, size=args.size, out=args.out)


if __name__ == "__main__":
    main()
