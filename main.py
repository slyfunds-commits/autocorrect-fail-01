#!/usr/bin/env python3
"""Funniest Autocorrect Fail R1 — "The Quarterly Resort".

Writes the keeper line to /output/entry.txt and verifies it byte-exact.
Stdlib only. Gate: UTF-8, 1-199 chars, not only whitespace, no trailing newline.
"""

import os
import sys

LINE = "Hi Mr. Davies, the quarterly resort is ready for review. Sorry for the delay, the dog ate my draft."

OUT = "/output/entry.txt"


def problems(text):
    found = []
    if not 1 <= len(text) <= 199:
        found.append(f"length {len(text)} outside 1-199")
    if not text.strip():
        found.append("only whitespace")
    if text.endswith("\n"):
        found.append("trailing newline")
    return found


def main():
    bad = problems(LINE)
    if bad:
        print("invalid entry:", "; ".join(bad), file=sys.stderr)
        return 1
    os.makedirs("/output", exist_ok=True)
    with open(OUT, "w", encoding="utf-8", newline="") as fh:
        fh.write(LINE)
    raw = open(OUT, "rb").read()
    if raw != LINE.encode("utf-8"):
        print("mismatch: entry.txt bytes differ from LINE", file=sys.stderr)
        return 1
    # Second pass: decode the written bytes and re-run the gate on them,
    # so a write that silently changed the text cannot slip through.
    decoded = raw.decode("utf-8")
    bad = problems(decoded)
    if bad or decoded != LINE:
        print("re-gate failed:", "; ".join(bad) or "decoded text differs", file=sys.stderr)
        return 1
    print(f"chars={len(LINE)} bytes={len(raw)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
