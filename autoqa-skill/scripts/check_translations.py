#!/usr/bin/env python3
"""Check parity markers for AutoQA's critical English, CN, and HK documents."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


GROUPS = (
    ("README.md", "README_CN.md", "README_HK.md"),
    (
        "autoqa-skill/references/rookie-qa-pedia.md",
        "autoqa-skill/references/rookie-qa-pedia_CN.md",
        "autoqa-skill/references/rookie-qa-pedia_HK.md",
    ),
    (
        "autoqa-skill/assets/templates/HUMAN-E2E.md",
        "autoqa-skill/assets/templates/HUMAN-E2E_CN.md",
        "autoqa-skill/assets/templates/HUMAN-E2E_HK.md",
    ),
)
VERSION_RE = re.compile(r"<!--\s*sync-version:\s*([^>]+?)\s*-->")
KEY_RE = re.compile(r"<!--\s*sync-key:\s*([a-z0-9-]+)\s*-->")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".", help="Repository root")
    return parser.parse_args()


def main() -> int:
    root = Path(parse_args().root).resolve()
    errors: list[str] = []
    for group in GROUPS:
        documents: list[tuple[str, str, set[str]]] = []
        for relative in group:
            path = root / relative
            if not path.is_file():
                errors.append(f"missing critical translation: {relative}")
                continue
            text = path.read_text(encoding="utf-8")
            version_match = VERSION_RE.search(text)
            if not version_match:
                errors.append(f"missing sync-version: {relative}")
                version = ""
            else:
                version = version_match.group(1).strip()
            keys = set(KEY_RE.findall(text))
            if not keys:
                errors.append(f"missing sync-key markers: {relative}")
            if not all(Path(member).name in text for member in group):
                errors.append(f"language switcher does not link all variants: {relative}")
            documents.append((relative, version, keys))
        if len(documents) != len(group):
            continue
        versions = {version for _, version, _ in documents}
        if len(versions) != 1:
            errors.append(
                "sync-version mismatch: " + ", ".join(f"{path}={version}" for path, version, _ in documents)
            )
        expected_keys = documents[0][2]
        for path, _, keys in documents[1:]:
            missing = sorted(expected_keys - keys)
            extra = sorted(keys - expected_keys)
            if missing or extra:
                errors.append(f"sync-key mismatch in {path}: missing={missing}, extra={extra}")
    for error in errors:
        print(f"ERROR: {error}")
    if errors:
        print(f"Translation check failed: {len(errors)} error(s)")
        return 1
    print(f"Translation check passed: {len(GROUPS)} document group(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
