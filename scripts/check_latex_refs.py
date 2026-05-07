#!/usr/bin/env python3
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEX_PATH = ROOT / "neurips_2026.tex"
BIB_PATH = ROOT / "references.bib"

CITE_RE = re.compile(r"\\cite\w*\*?(?:\[[^\]]*\])*\{([^}]*)\}")
LABEL_RE = re.compile(r"\\label\{([^}]*)\}")
REF_RE = re.compile(r"\\(?:ref|eqref|autoref)\{([^}]*)\}")
BIB_RE = re.compile(r"@\w+\s*\{\s*([^,\s]+)", re.MULTILINE)


def strip_comments(text: str) -> str:
    lines = []
    for line in text.splitlines():
        cut = None
        escaped = False
        for i, ch in enumerate(line):
            if ch == "\\":
                escaped = not escaped
                continue
            if ch == "%" and not escaped:
                cut = i
                break
            escaped = False
        lines.append(line[:cut] if cut is not None else line)
    return "\n".join(lines)


def main() -> int:
    if not TEX_PATH.exists():
        print(f"Missing TeX file: {TEX_PATH}", file=sys.stderr)
        return 2
    if not BIB_PATH.exists():
        print(f"Missing bibliography file: {BIB_PATH}", file=sys.stderr)
        return 2

    tex = strip_comments(TEX_PATH.read_text(encoding="utf-8", errors="ignore"))
    bib = BIB_PATH.read_text(encoding="utf-8", errors="ignore")

    cite_keys = []
    for match in CITE_RE.finditer(tex):
        cite_keys.extend(k.strip() for k in match.group(1).split(",") if k.strip())
    cite_keys = sorted(set(cite_keys))

    bib_keys = sorted(set(BIB_RE.findall(bib)))
    labels = LABEL_RE.findall(tex)
    refs = sorted(set(REF_RE.findall(tex)))

    missing_cites = sorted(set(cite_keys) - set(bib_keys))
    unused_bib = sorted(set(bib_keys) - set(cite_keys))
    duplicate_labels = sorted({label for label in labels if labels.count(label) > 1})
    missing_refs = sorted(set(refs) - set(labels))

    failed = False
    if missing_cites:
        failed = True
        print("Missing BibTeX entries:")
        for key in missing_cites:
            print(f"  - {key}")
    if duplicate_labels:
        failed = True
        print("Duplicate LaTeX labels:")
        for label in duplicate_labels:
            print(f"  - {label}")
    if missing_refs:
        failed = True
        print("Missing LaTeX labels for refs:")
        for label in missing_refs:
            print(f"  - {label}")

    print(f"cite_keys={len(cite_keys)} bib_keys={len(bib_keys)} labels={len(set(labels))} refs={len(refs)}")
    if unused_bib:
        print("Unused BibTeX entries:")
        for key in unused_bib:
            print(f"  - {key}")

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
