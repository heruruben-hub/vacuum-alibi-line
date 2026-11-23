#!/usr/bin/env python3
"""The Vacuum's Alibi — one deadpan line from a robot vacuum.

Writes the vacuum's excuse for missing a spot to /output/entry.txt,
then re-reads the file and verifies it is a single line of 1-200
characters, as the make.fun gate requires.
"""

import os
import sys

LINE = (
    "My sensors insist that spot is a sleeping dog, "
    "so I have tiptoed around it for six months. It is a rug."
)

OUTPUT_PATH = "/output/entry.txt"
MAX_CHARS = 200


def main() -> int:
    line = LINE.strip()
    if not line:
        print("error: entry line is empty", file=sys.stderr)
        return 1
    if len(line) > MAX_CHARS:
        print(
            f"error: entry line is {len(line)} characters, "
            f"over the {MAX_CHARS} limit",
            file=sys.stderr,
        )
        return 1
    if "\n" in line or "\r" in line:
        print("error: entry line must be a single line", file=sys.stderr)
        return 1

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(line + "\n")

    # Re-read and verify what actually landed on disk.
    with open(OUTPUT_PATH, "r", encoding="utf-8") as f:
        written = f.read()
    if written != line + "\n":
        print("error: verification failed, file contents differ", file=sys.stderr)
        return 1
    if not 1 <= len(written.strip()) <= MAX_CHARS:
        print("error: verification failed, length out of range", file=sys.stderr)
        return 1

    print(f"wrote {len(line)} characters to {OUTPUT_PATH}")
    print(line)
    return 0


if __name__ == "__main__":
    sys.exit(main())
