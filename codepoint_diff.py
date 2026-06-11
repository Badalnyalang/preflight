#!/usr/bin/env python3
"""Pre-flight gate (2): Unicode codepoint inventory diff.

Compares the codepoint inventories of two text files (e.g. references vs.
hypotheses, or train vs. test) and reports characters that appear in one
but not the other, plus visually-confusable variants (e.g. U+2219 vs U+00B7).

Usage: python preflight_codepoint_diff.py file_a.txt file_b.txt
"""
import sys, unicodedata
from collections import Counter

CONFUSABLE_GROUPS = [
    {"\u2219", "\u00b7", "\u2022", "\u30fb"},        # raised dots / bullets
    {"'", "\u2019", "\u02bc", "\u2018", "`"},         # apostrophes
    {'"', "\u201c", "\u201d"},                        # quotes
    {"-", "\u2010", "\u2011", "\u2013", "\u2014"},    # hyphens/dashes
    {" ", "\u00a0", "\u2009", "\u200a"},              # spaces
]

def inventory(path):
    counts = Counter()
    with open(path, encoding="utf-8", errors="replace") as f:
        for line in f:
            counts.update(line.rstrip("\n"))
    return counts

def name(ch):
    try: return unicodedata.name(ch)
    except ValueError: return "<unnamed>"

def main(a_path, b_path):
    a, b = inventory(a_path), inventory(b_path)
    only_a, only_b = set(a) - set(b), set(b) - set(a)
    print(f"== Only in {a_path} ({len(only_a)}) ==")
    for ch in sorted(only_a):
        print(f"  U+{ord(ch):04X} {name(ch)}  x{a[ch]}")
    print(f"== Only in {b_path} ({len(only_b)}) ==")
    for ch in sorted(only_b):
        print(f"  U+{ord(ch):04X} {name(ch)}  x{b[ch]}")
    print("== Confusable variants present (normalize before any metric!) ==")
    flagged = False
    for group in CONFUSABLE_GROUPS:
        present = [ch for ch in group if ch in a or ch in b]
        if len(present) > 1:
            flagged = True
            print("  " + "  ".join(f"U+{ord(ch):04X}({name(ch)})" for ch in present))
    if not flagged:
        print("  none detected")
    sys.exit(1 if (only_a or only_b or flagged) else 0)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(__doc__); sys.exit(2)
    main(sys.argv[1], sys.argv[2])
