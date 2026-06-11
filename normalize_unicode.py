#!/usr/bin/env python3
"""Pre-flight normalization utility.

Normalizes visually-confusable Unicode variants to a single canonical
codepoint per group, then applies NFC. Default mapping reflects the
orthographic conventions that caused the BLEU~100 artifact (raised dot)
plus common apostrophe/dash/space variants. Edit CANONICAL to suit your
language's conventions BEFORE first use, and apply the SAME mapping to
corpora, references, and model outputs.

Usage: python normalize_unicode.py input.txt output.txt
"""
import sys, unicodedata

CANONICAL = {
    # raised dots -> MIDDLE DOT (U+00B7); change target if your orthography differs
    "\u2219": "\u00b7", "\u2022": "\u00b7", "\u30fb": "\u00b7",
    # apostrophes -> RIGHT SINGLE QUOTATION MARK (U+2019)
    "'": "\u2019", "\u02bc": "\u2019", "`": "\u2019", "\u2018": "\u2019",
    # double quotes -> straight
    "\u201c": '"', "\u201d": '"',
    # dashes -> hyphen-minus (review per language; en dash in numerals may be wanted)
    "\u2010": "-", "\u2011": "-", "\u2013": "-", "\u2014": "-",
    # spaces -> plain space
    "\u00a0": " ", "\u2009": " ", "\u200a": " ",
    # zero-width characters -> removed
    "\u200b": "", "\u200c": "", "\u200d": "", "\ufeff": "",
}

def normalize(text: str) -> str:
    for src, dst in CANONICAL.items():
        text = text.replace(src, dst)
    return unicodedata.normalize("NFC", text)

def main(inp, outp):
    with open(inp, encoding="utf-8") as f:
        data = f.read()
    with open(outp, "w", encoding="utf-8") as f:
        f.write(normalize(data))
    print(f"normalized {inp} -> {outp}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(__doc__); sys.exit(2)
    main(sys.argv[1], sys.argv[2])
