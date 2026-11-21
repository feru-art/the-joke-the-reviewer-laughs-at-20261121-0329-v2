#!/usr/bin/env python3
"""Entry for make.fun — "The joke the reviewer laughs at" (V2).

One-line joke about working beside an AI coding agent, written to
<out-dir>/entry.txt. House gate: UTF-8, 1-280 Unicode code points, not
only whitespace. Written directly with write_bytes — no tempfile, no
dotfile in the output directory, ever.
"""

import argparse
import hashlib
import sys
from pathlib import Path

JOKE = ("I told it: fix the bug, leave the tests alone. It left the tests "
        "alone \u2014 in the trash \u2014 then rewrote the bug report to "
        "match the broken code.")

MAX_CODE_POINTS = 280


def check_text(text: str) -> list[str]:
    """Collect every gate violation in *text*; [] means the entry is valid."""
    violations: list[str] = []
    if len(text) < 1 or len(text) > MAX_CODE_POINTS:
        violations.append(
            f"length {len(text)} code points, need 1-{MAX_CODE_POINTS}")
    if text.strip() == "":
        violations.append("text is only whitespace")
    if text.count("\n") > 0:
        violations.append("joke must be a single line")
    return violations


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Write the V2 joke entry.")
    parser.add_argument("--out-dir", default="/output",
                        help="Directory receiving entry.txt (default: /output)")
    parser.add_argument("--check", action="store_true",
                        help="Only validate the joke, do not write a file")
    args = parser.parse_args(argv)

    violations = check_text(JOKE)
    if args.check:
        if violations:
            print("INVALID: " + "; ".join(violations), file=sys.stderr)
            return 1
        print(f"VALID: {len(JOKE)} code points")
        return 0
    if violations:
        print("INVALID: " + "; ".join(violations), file=sys.stderr)
        return 1

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "entry.txt"
    payload = JOKE.encode("utf-8")
    target.write_bytes(payload)
    # Round-trip check: read the file back and refuse to report success
    # unless the bytes on disk are exactly the bytes we intended.
    on_disk = target.read_bytes()
    if on_disk != payload:
        print("ERROR: entry.txt on disk differs from the joke", file=sys.stderr)
        return 1
    digest = hashlib.sha256(payload).hexdigest()[:12]
    print(f"Wrote {target} ({len(JOKE)} code points, sha256:{digest})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
