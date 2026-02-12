
---

#  Ledger Drift

**Silent Financial Logic Drift Detection**

Ledger Drift detects unintended financial behavior changes in code before they merge.

It analyzes Git diffs, simulates the mathematical impact of logic changes, and flags tolerance breaches — without executing your code.

Local-first. CI-ready. No telemetry.

---

## Why Ledger Drift Exists

Financial bugs are rarely syntax errors.

They are silent logic shifts:

* `0.05` → `0.5`
* rounding removed
* interest multiplier changed
* FX rate applied incorrectly

These changes pass linting.
They pass unit tests.
They pass code review.

They quietly alter money.

Ledger Drift answers one question:

> Did this code change alter financial behavior in a way we didn’t intend?

---

## What Ledger Drift Does

* Scans your repository for money-handling functions
* Detects financial behavior changes in diffs
* Simulates impact under a deterministic scenario (e.g. `amount=1000`)
* Quantifies absolute and percentage delta
* Scores severity against configurable tolerance
* Produces human-readable financial impact reports
* Exposes CI-friendly exit codes
* Supports clean JSON output for automation

---

## What Ledger Drift Does NOT Do

Ledger Drift is intentionally conservative.

It:

* Does not execute your code
* Does not import your modules
* Does not access production data
* Does not connect to external services
* Does not guarantee financial correctness
* Does not replace accounting or financial review
* Does not send telemetry

Ledger Drift is an early warning system — not an oracle.

---

## Installation

After publishing to PyPI:

```
pip install ledger-drift
```

---

## Quickstart

Initialize Ledger Drift in your repository:

```
ledger-drift init
```

This scans your codebase for money-handling functions and generates:

```
ledgerdrift.yml
```

Analyze changes:

```
ledger-drift analyze
```

Machine-readable output (for CI or automation):

```
ledger-drift analyze --json
```

---

## Example Output

```
Ledger Drift v0.1.0
1 HIGH DRIFT detected in monitored functions

❌ HIGH FINANCIAL DRIFT
────────────────────
Function: calculate_fee
File:     src/tests/fake_pricing.py
Tolerance: 0.02

Scenario: amount=1000

Before:
  fee = 600.00

After:
  fee = 500.00

Impact:
  -100.00 per transaction (-16.67%)

This change exceeds the configured tolerance.

Severity: DANGEROUS
Mode: CI-safe (fail_on_drift = false)

Exit code: 1
```

Designed to be Slack-pasteable and CI-readable.

---

## Configuration

Ledger Drift generates a `ledgerdrift.yml` file during initialization.

Example:

```
version: 1
fail_on_drift: false

rules:
  - type: fee_standard
    file: src/pricing.py
    function: calculate_fee
    tolerance: 0.02
```

### Configuration Fields

* `version` — configuration schema version
* `fail_on_drift` — set to `true` to enforce blocking behavior in CI
* `rules` — monitored functions and their tolerance thresholds

When `fail_on_drift: true`, dangerous drift returns exit code `2`.

When `fail_on_drift: false`, drift returns exit code `1` (CI-safe mode).

---

## Exit Code Contract

Severity → Exit Code

* SAFE → 0
* WARNING → 1
* DANGEROUS → 2

This allows CI systems to gate deployments automatically.

---

## Design Philosophy

Ledger Drift is intentionally limited.

It focuses on:

* Financial behavior drift
* Deterministic simulation
* Conservative evaluation
* Honest failure when unsafe

It does not attempt:

* Full program analysis
* Dynamic execution
* Production monitoring
* Accounting verification

V1 solves one problem well:

Behavioral drift in financial logic.

---

## License

MIT License



Commit that.
Push it.
That’s Phase 6 foundation done properly.
