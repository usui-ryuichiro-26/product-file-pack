#!/usr/bin/env python3

import argparse
import json
from pathlib import Path


def create_directories(
    tree: dict,
    output_dir: Path,
) -> None:
    for name, node in tree.items():
        # files はディレクトリではなくファイル一覧
        if name == "files":
            continue

        directory = output_dir / name.rstrip("/")

        directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        # ディレクトリの中身を再帰的に処理
        if isinstance(node, dict):
            create_directories(
                node,
                directory,
            )


def unpack(input_file: Path, output_dir: Path) -> None:
    data = json.loads(
        input_file.read_text(encoding="utf-8")
    )

    # ディレクトリ構造を復元
    create_directories(
        data.get("directories", {}),
        output_dir,
    )

    # ファイルを復元
    for entry in data.get("files", []):
        relative_dir = entry["path"].removeprefix("./")

        if relative_dir == ".":
            relative_dir = ""

        destination = (
            output_dir
            / relative_dir
            / entry["name"]
        )

        destination.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        destination.write_text(
            entry["body"],
            encoding="utf-8",
        )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Unpack a JSON file into a directory."
    )

    parser.add_argument(
        "input",
        type=Path,
        help="Input JSON file",
    )

    parser.add_argument(
        "directory",
        type=Path,
        help="Output directory",
    )

    args = parser.parse_args()

    if not args.input.is_file():
        parser.error(
            f"input file not found: {args.input}"
        )

    unpack(
        args.input,
        args.directory,
    )


if __name__ == "__main__":
    main()
