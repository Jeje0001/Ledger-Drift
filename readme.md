# Ledger Drift

Ledger Drift is a local CLI tool that detects unintended financial logic changes in code diffs.

It is designed to catch silent money-impacting changes before they are merged.

---

## What Ledger Drift Does

- Analyzes code diffs for changes to financial logic
- Flags potential drift in money-related calculations
- Produces clear, human-readable CLI output
- Runs entirely locally with no network calls

---

## What Ledger Drift Does NOT Do

- Execute your code
- Access production data
- Guarantee financial correctness
- Replace accounting, audits, or compliance systems

Ledger Drift is an early warning tool, not a source of truth.

---

## Quickstart

```bash
pip install ledger-drift
ledger-drift init
ledger-drift analyze
