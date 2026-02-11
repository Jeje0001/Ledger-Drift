import json

PRESENTATION_SEVERITY = {
    "LOW": "SAFE",
    "MEDIUM": "WARNING",
    "HIGH": "DANGEROUS",
}

EXIT_CODES = {
    "SAFE": 0,
    "WARNING": 1,
    "DANGEROUS": 2,
}


def render_human_report(findings,fail_on_drift):
    version = "0.1.0"

    high = 0
    medium = 0
    low = 0

    for finding in findings:
        if finding["severity"] == "HIGH":
            high += 1
        elif finding["severity"] == "MEDIUM":
            medium += 1
        elif finding["severity"] == "LOW":
            low += 1

    print(f"Ledger Drift v{version}")

    if high > 0:
        print(f"{high} HIGH DRIFT detected in monitored functions")
    else:
        print("No high-risk financial drift detected")

    print()

    # ----- PER-FINDING REPORT -----
    for finding in findings:
        engine_severity = finding["severity"]
        presentation_severity = PRESENTATION_SEVERITY[engine_severity]

        print("❌ HIGH FINANCIAL DRIFT")
        print("────────────────────")

        print(f"Function: {finding['function']}")
        print(f"File:     {finding['file']}")
        print(f"Tolerance: {finding['tolerance']}")
        print()

        print("Scenario:  amount = 1000")
        print()

        print("Before:")
        print(f"  fee = {finding['old']:.2f}")
        print()

        print("After:")
        print(f"  fee = {finding['new']:.2f}")
        print()

        print("Impact:")
        print(
            f"  {finding['delta']:+.2f} per transaction "
            f"({finding['percent']:+.2f}%)"
        )
        print()

        print("This change exceeds the configured tolerance.")
        print()
        print(f"Severity: {presentation_severity}")
        print()

    highest_severity = "LOW"

    for finding in findings:
        if finding["severity"] == "HIGH":
            highest_severity = "HIGH"
            break
        elif finding["severity"] == "MEDIUM":
            highest_severity = "MEDIUM"

    presentation = PRESENTATION_SEVERITY[highest_severity]

    if fail_on_drift:
        exit_code = EXIT_CODES[presentation]
    else:
        if presentation == "SAFE":
            exit_code = 0
        else:
            exit_code = 1
    
    if not fail_on_drift:
        print("Mode: CI-safe (fail_on_drift = false)")
    else:
        print("Mode: Enforcement (fail_on_drift = true)")

    return exit_code

def render_json_report(findings,fail_on_drift):
    high = 0
    medium = 0
    low = 0

    for finding in findings:
        if finding["severity"] == "HIGH":
            high += 1
        elif finding["severity"] == "MEDIUM":
            medium += 1
        elif finding["severity"] == "LOW":
            low += 1

    highest_severity = "LOW"

    for finding in findings:
        if finding["severity"] == "HIGH":
            highest_severity = "HIGH"
            break
        elif finding["severity"] == "MEDIUM":
            highest_severity = "MEDIUM"

    presentation = PRESENTATION_SEVERITY[highest_severity]

    if fail_on_drift:
        exit_code = EXIT_CODES[presentation]
    else:
        if presentation == "SAFE":
            exit_code = 0
        else:
            exit_code = 1


    output = {
        "version": "0.1.0",
        "summary": {
            "high": high,
            "medium": medium,
            "low": low,
        },
        "findings": [],
        "exit_code": exit_code,
    }

    for finding in findings:
        output["findings"].append({
            "function": finding["function"],
            "file": finding["file"],
            "severity": finding["severity"],
            "before": finding["old"],
            "after": finding["new"],
            "delta_pct": finding["percent"],
            "tolerance": finding["tolerance"],
        })

    print(json.dumps(output, indent=2))

    return exit_code
