#!/usr/bin/env python3
"""Create an App Roast run without overwriting an existing report (stdlib only)."""

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import tempfile


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", required=True)
    parser.add_argument("--output", type=Path, help="Run directory; default: .agents/app-grill/<timestamp>-<target> under the current project root")
    parser.add_argument("--language", default="en", help="Final report language recorded in metadata; the agent translates the English scaffold")
    parser.add_argument("--tone", choices=("professional", "roast", "brutal"), default="roast")
    args = parser.parse_args()
    now = datetime.now(timezone.utc)
    slug = re.sub(r"[^a-z0-9]+", "-", args.target.lower()).strip("-")[:48] or "app"
    output = args.output or Path(".agents/app-grill") / (now.strftime("%Y%m%dT%H%M%S%fZ-") + slug)
    template = Path(__file__).resolve().parents[1] / "assets" / "report-template.md"
    text = template.read_text(encoding="utf-8")
    values = {
        "title_yaml": "App Roast: " + args.target,
        "target_yaml": args.target,
        "created_yaml": now.isoformat(timespec="seconds"),
        "language_yaml": args.language,
        "tone_yaml": args.tone,
    }
    text = re.sub(r"\{\{(\w+)\}\}", lambda m: json.dumps(values[m.group(1)], ensure_ascii=False), text)
    report = output / "report.md"
    try:
        output.mkdir(parents=True, exist_ok=True)
        if report.exists() or report.is_symlink():
            parser.exit(2, f"Report already exists; resume it or choose a new directory: {report}\n")
        evidence = output / "evidence"
        evidence.mkdir(exist_ok=True)
        with tempfile.TemporaryFile(dir=evidence) as probe:
            probe.write(b"app-roast write check\n")
            probe.flush()
    except OSError as exc:
        parser.exit(1, f"Cannot prepare audit directory {output}: {exc}\n")
    created = False
    try:
        with report.open("x", encoding="utf-8") as handle:
            created = True
            handle.write(text)
    except FileExistsError:
        parser.exit(2, f"Report already exists; resume it or choose a new directory: {report}\n")
    except (OSError, UnicodeError) as exc:
        cleanup_note = ""
        if created:
            try:
                report.unlink()
            except OSError as cleanup_error:
                cleanup_note = f" Partial report remains at {report}: {cleanup_error}."
        parser.exit(1, f"Cannot write audit report {report}: {exc}.{cleanup_note}\n")
    print(report.resolve())


if __name__ == "__main__":
    main()
