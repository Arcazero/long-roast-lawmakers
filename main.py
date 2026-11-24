#!/usr/bin/env python3
"""Write the one-line roast to the grader's output file.

The competition gate checks that /output/entry.txt is UTF-8 text of
1 to 320 characters, not only white space. This program reads the roast
from roast.txt beside it, validates it against that gate, and writes it
byte-identically to $MAKEFUN_OUTPUT_DIR/entry.txt (default /output).
"""

import os
from pathlib import Path

MAX_CHARS = 320


def main() -> None:
    here = Path(__file__).resolve().parent
    line = (here / "roast.txt").read_text(encoding="utf-8").strip()
    if not line:
        raise SystemExit("roast.txt is empty")
    if "\n" in line or "\r" in line:
        raise SystemExit("roast must be a single line")
    if len(line) > MAX_CHARS:
        raise SystemExit(
            f"roast is {len(line)} characters, over the {MAX_CHARS} limit"
        )
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output")
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "entry.txt"
    target.write_text(line, encoding="utf-8")
    if target.read_text(encoding="utf-8") != line:
        raise SystemExit("entry.txt did not round-trip byte-identically")


if __name__ == "__main__":
    main()
