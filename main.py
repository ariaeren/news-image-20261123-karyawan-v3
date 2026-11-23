#!/usr/bin/env python3
"""Copy the pre-rendered entry image byte-for-byte to the make.fun output directory.

No rendering, network access or environment-derived code execution happens here.
"""

import os
from pathlib import Path


def source_image() -> Path:
    """Prefer the bundled image; fall back to /bot when it is present."""
    local = Path(__file__).resolve().parent / "entry.png"
    if local.is_file():
        return local

    bot_copy = Path("/bot") / "entry.png"
    if bot_copy.is_file():
        return bot_copy

    raise FileNotFoundError("entry.png was not found beside main.py or in /bot")


def main() -> None:
    payload = source_image().read_bytes()
    output_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output")
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "entry.png").write_bytes(payload)


if __name__ == "__main__":
    main()
