#!/usr/bin/env python3
"""Render the verification log into a readable markdown report.

Reads data/verification.json (the machine-readable record of which URLs were
opened, when, and what they actually said) and writes reports/verification-report.md.

Nothing is invented here: every line is copied from the JSON. If the JSON is
empty, the report is empty.

Run: python3 scripts/report_verify.py
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
data = json.loads((ROOT / "data/verification.json").read_text(encoding="utf-8"))
out = ROOT / "reports/verification-report.md"

s = data.get("summary", {})
lines = [
    "# Verification report",
    "",
    f"- Pass date: **{data.get('retrieved_utc')}**",
    f"- Session: `{data.get('session')}`",
    f"- URLs opened: **{s.get('urls_opened')}** — confirmed {s.get('confirmed')}, "
    f"corrected {s.get('corrected')}, flagged {s.get('flagged')}",
    "",
    "## Method",
    "",
    data.get("method", ""),
    "",
    "## Passes",
    "",
    "| # | Pass | What it did | Result |",
    "|---|---|---|---|",
]
for p in data.get("passes", []):
    lines.append(f"| {p['id']} | {p['name']} | {p['what']} | {p['result']} |")

lines += ["", "## Checks", "", "| ID | Source | Rows | Outcome | What the page said |", "|---|---|---|---|---|"]
for c in data.get("checks", []):
    findings = c["findings"].replace("|", "\\|")
    lines.append(f"| {c['id']} | [{c['label']}]({c['url']}) | {', '.join(c.get('rows', []))} | "
                 f"**{c['outcome']}** | {findings} |")

lines += ["", "## Irregularities raised", "", "| Row | What is irregular | Flag | Severity |", "|---|---|---|---|"]
for d in data.get("discrepancies", []):
    lines.append(f"| {d['row']} | {d['what']} | `{d['flag']}` | {d['severity']} |")

lines += ["", "## Deliberately not re-checked", ""]
for n in data.get("not_rechecked", []):
    lines.append(f"- {n['url']} — {n['why']}")

lines += ["", "## What no website can verify", ""]
for u in s.get("unverifiable_online", []):
    lines.append(f"- {u}")

lines += ["", "## Standing recommendation", "",
          "Re-run `python3 scripts/audit.py` after every review, then repeat the hallucination pass by hand: "
          "pick any number in the dataset and try to find it on the linked page. If it is not there, delete it "
          "and mark the field unverified.", ""]

out.parent.mkdir(exist_ok=True)
out.write_text("\n".join(lines), encoding="utf-8")
print(f"wrote {out.relative_to(ROOT)} ({len(data.get('checks', []))} checks)")
