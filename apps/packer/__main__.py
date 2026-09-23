#!/usr/bin/env python3

# Copyright (c) 2026 Usui Ryuichiro
# SPDX-License-Identifier: MIT

import argparse
import json
import os
from pathlib import Path
from typing import Optional


def read_text(file: Path) -> Optional[str]:
    try:
        return file.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        print(f"Warning: skipped non-UTF-8 file: {file}")
        return None


def build_directory_tree(root: Path) -> dict:
    tree = {"./": {"files": []}}

    for current_dir, dirs, filenames in os.walk(root):
        current_path = Path(current_dir)
        relative = current_path.relative_to(root)

        node = tree["./"]

        for part in relative.parts:
            node = node.setdefault(
                f"{part}/",
                {"files": []},
            )

        dirs[:] = sorted(
            directory
            for directory in dirs
            if not directory.startswith(".")
        )

        for filename in sorted(filenames):
            if filename.startswith("."):
                continue

            node["files"].append(filename)

    return tree


def pack(root: Path, output: Path) -> None:
    files = []
    directories = build_directory_tree(root)

    for current_dir, dirs, filenames in os.walk(root):
        current_path = Path(current_dir)

        dirs[:] = sorted(
            directory
            for directory in dirs
            if not directory.startswith(".")
        )

        for filename in sorted(filenames):
            if filename.startswith("."):
                continue

            file = current_path / filename
            body = read_text(file)

            if body is None:
                continue

            relative = file.relative_to(root)

            path = (
                "./"
                if relative.parent == Path(".")
                else f"./{relative.parent.as_posix()}"
            )

            files.append({
                "path": path,
                "name": file.name,
                "body": body,
            })

    output.write_text(
        json.dumps(
            {
                "directories": directories,
                "files": files,
            },
            ensure_ascii=False,
            indent=4,
        ),
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Pack a directory into a JSON file."
    )

    parser.add_argument(
        "directory",
        type=Path,
        help="Directory to pack",
    )

    parser.add_argument(
        "output",
        type=Path,
        help="Output JSON file",
    )

    args = parser.parse_args()

    if not args.directory.is_dir():
        parser.error(f"directory not found: {args.directory}")

    pack(args.directory, args.output)


if __name__ == "__main__":
    main()
