#!/usr/bin/env python3
"""Write the one-line roast to the grader's output file.

The competition gate checks that /output/entry.txt is UTF-8 text of
1 to 320 characters, not only white space. This program reads the roast
from roast.txt beside it, validates it against that gate, and writes it
byte-identically to $MAKEFUN_OUTPUT_DIR/entry.txt (default /output),
via a temp file renamed into place so a partial write never lands.
Run with --check to validate roast.txt without writing anything.
"""

import argparse
import os
from pathlib import Path

MAX_CHARS = 320


def load_roast(here: Path) -> str:
    """Read roast.txt beside this file and validate it against the gate."""
    try:
        line = (here / "roast.txt").read_text(encoding="utf-8").strip()
    except FileNotFoundError:
        raise SystemExit("roast.txt not found beside main.py")
    except UnicodeDecodeError:
        raise SystemExit("roast.txt is not valid UTF-8")
    if not line:
        raise SystemExit("roast.txt is empty")
    if "\n" in line or "\r" in line:
        raise SystemExit("roast must be a single line")
    if len(line) > MAX_CHARS:
        raise SystemExit(
            f"roast is {len(line)} characters, over the {MAX_CHARS} limit"
        )
    return line


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Write the one-line roast to the grader's output file."
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="validate roast.txt against the gate without writing entry.txt",
    )
    args = parser.parse_args()
    here = Path(__file__).resolve().parent
    line = load_roast(here)
    if args.check:
        print(f"roast OK: {len(line)} characters, 1 line")
        return
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output")
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "entry.txt"
    write_atomic(target, line)
    verify_output(target, line)


def write_atomic(target: Path, line: str) -> None:
    """Write via a temp file in the same directory, then rename into place."""
    tmp = target.with_suffix(".tmp")
    with tmp.open("w", encoding="utf-8") as fh:
        fh.write(line)
        fh.flush()
        os.fsync(fh.fileno())
    os.replace(tmp, target)


def verify_output(target: Path, line: str) -> None:
    """Re-read the written file and confirm it round-trips byte-identically."""
    if target.read_text(encoding="utf-8") != line:
        raise SystemExit("entry.txt did not round-trip byte-identically")


if __name__ == "__main__":
    main()
