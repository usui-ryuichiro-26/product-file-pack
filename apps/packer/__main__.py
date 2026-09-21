#!/usr/bin/env python3

import argparse
import json
from pathlib import Path


def pack(root: Path, output: Path) -> None:
    files = []

    for file in sorted(root.rglob("*")):
        if not file.is_file():
            continue

        relative = file.relative_to(root)

        files.append({
            "path": f"./{relative.parent.as_posix()}",
            "name": file.name,
            "body": file.read_text(encoding="utf-8"),
        })

    output.write_text(
        json.dumps(
            {"files": files},
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
