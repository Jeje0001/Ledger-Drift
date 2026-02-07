def score_drift(percent_change: float, tolerance: float) -> str:
    abs_change = abs(percent_change)
    tolerance_pct = tolerance * 100

    if abs_change < tolerance_pct:
        return "LOW"

    if abs_change < 5 * tolerance_pct:
        return "MEDIUM"

    return "HIGH"
