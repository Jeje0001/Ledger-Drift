
def infer_rule_type(function_name: str) -> str:
    name = function_name.lower()

    if "fee" in name:
        return "fee_standard"

    if "rate" in name or "percent" in name:
        return "percentage_guard"

    return "rounding_guard"
