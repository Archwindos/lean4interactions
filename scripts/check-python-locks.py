#!/usr/bin/env python3
"""Check Python locks and freeze installed local references as version pins."""
from __future__ import annotations

import argparse
from importlib.metadata import version
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
LOCAL_DIRECT = re.compile(
    r"^([A-Za-z0-9_.-]+)\s*@\s*(?:file:|/|[A-Za-z]:[\\/])", re.IGNORECASE
)
LOCAL_REQUIREMENT = re.compile(
    r"^(?:-e\s+)?(?:file:|/|[A-Za-z]:[\\/]|\./|\.\./)", re.IGNORECASE
)


def normalize_freeze(text: str) -> str:
    """Conda packages may record a build-machine file URI in pip metadata."""
    lines = []
    for line in text.splitlines():
        match = LOCAL_DIRECT.match(line.strip())
        if match:
            name = match.group(1)
            line = f"{name}=={version(name)}"
        lines.append(line)
    return "\n".join(lines) + "\n"


def local_references(path: Path) -> list[str]:
    errors = []
    for number, line in enumerate(path.read_text().splitlines(), 1):
        requirement = line.strip()
        if requirement and not requirement.startswith("#") and (
            LOCAL_DIRECT.match(requirement) or LOCAL_REQUIREMENT.match(requirement)
        ):
            errors.append(f"{path}:{number}: local dependency reference: {requirement}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--freeze-installed", action="store_true",
                        help="Print normalized pip freeze output for this interpreter")
    parser.add_argument("--pip-lock", type=Path, default=ROOT / "locks/python-pip.txt")
    args = parser.parse_args()
    if args.freeze_installed:
        frozen = subprocess.check_output(
            [sys.executable, "-m", "pip", "freeze", "--exclude", "harsanyi-proof-archive"],
            text=True,
        )
        sys.stdout.write(normalize_freeze(frozen))
        return 0
    errors = local_references(args.pip_lock)
    conda_lock = ROOT / "locks/python-conda-linux-64.txt"
    if conda_lock.is_file():
        errors.extend(local_references(conda_lock))
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print("Python dependency locks contain no local file references.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
