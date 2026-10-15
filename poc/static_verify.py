#!/usr/bin/env python3
"""Non-invasive source verifier for GHSA-9gxw-qpx8-x9c7."""

from pathlib import Path
import sys


CHECKS = {
    "app/Http/Requests/MediaUploadRequest.php": [
        "config('app.demo_mode', false)",
        "mimetypes:",
    ],
    "app/Concerns/HandlesMediaOperations.php": [
        "'svg' => ['image/svg+xml']",
        "isDangerousFile",
        "validateFileHeaders",
    ],
}


def main() -> int:
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} /path/to/laradashboard", file=sys.stderr)
        return 2

    root = Path(sys.argv[1]).resolve()
    findings = 0
    for relative, markers in CHECKS.items():
        path = root / relative
        if not path.is_file():
            print(f"[?] Missing: {relative}")
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        present = [marker for marker in markers if marker in text]
        print(f"[{'!' if present else '-'}] {relative}: {len(present)}/{len(markers)} relevant markers")
        for marker in present:
            print(f"    {marker}")
        findings += len(present)

    print(f"\nObserved relevant source markers: {findings}")
    print("Manual review is required; marker presence alone is not proof of exploitability.")
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
