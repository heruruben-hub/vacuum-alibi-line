#!/usr/bin/env python3
"""The Vacuum's Alibi — one deadpan line from a robot vacuum.

The line is written in the vacuum's own voice: deadpan, a little smug
about its sensors, with the punch ("It is a rug.") landing at the end.
The judge weighs deadpan robot voice, surprise and tightness, so the
line is kept exactly as written — validation below only ever rejects
a bad line, it never rewrites it.

Writes the line to /output/entry.txt, then re-reads the file and
verifies it is a single line of 1-200 characters, as the make.fun
gate requires.
"""

import os
import sys

LINE = (
    "My sensors insist that spot is a sleeping dog, "
    "so I have tiptoed around it for six months. It is a rug."
)

OUTPUT_PATH = "/output/entry.txt"
MAX_CHARS = 200


def validate_line(line: str) -> list[str]:
    """Return every problem with the entry line, or [] if it is valid.

    The gate requires 1-200 characters of UTF-8 text, not only white
    space, in a single line. A tab or other control character would
    still technically fit on one line, but it would break the clean
    one-line presentation, so those are rejected too.
    """
    problems: list[str] = []
    if not line or line.isspace():
        problems.append("entry line is empty or only white space")
    if len(line) > MAX_CHARS:
        problems.append(
            f"entry line is {len(line)} characters, over the {MAX_CHARS} limit"
        )
    if "\n" in line or "\r" in line:
        problems.append("entry line must be a single line (contains a newline)")
    control = [c for c in line if ord(c) < 32 and c not in ("\n", "\r")]
    if control:
        problems.append(
            f"entry line contains control characters: {[hex(ord(c)) for c in control]}"
        )
    return problems


def main() -> int:
    line = LINE.strip()
    problems = validate_line(line)
    if problems:
        for problem in problems:
            print(f"error: {problem}", file=sys.stderr)
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
