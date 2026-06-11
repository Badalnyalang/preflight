# lr-preflight

A minimal pre-flight toolkit for low-resource NLP development,
accompanying the paper "Where Low-Resource NLP Breaks: A Root-Cause
Analysis of Failure Modes from Building Language Technology for
Northeast India" (under review).

## Contents
- `codepoint_diff.py` - diff the Unicode codepoint inventories of two
  text files and flag visually-confusable variants (gate 2). Exit code
  1 if anything is off, so it can act as a hard gate in pipelines.
- `normalize_unicode.py` - normalize confusable variants to canonical
  codepoints plus NFC (review the mapping per language before use).
- `PREFLIGHT_CHECKLIST.md` - the eight-gate checklist from the paper.

## Quick start
```
python codepoint_diff.py references.txt hypotheses.txt
python normalize_unicode.py raw.txt clean.txt
```

No dependencies beyond Python 3.8+.

License: CC-BY-4.0
