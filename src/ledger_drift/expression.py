def extract_changed_lines(diff_lines: list[str]) -> tuple[list[str], list[str]]:
    old_lines = []
    new_lines = []

    for line in diff_lines:
        if line.startswith("-") and not line.startswith("---"):
            old_lines.append(line[1:].strip())

        if line.startswith("+") and not line.startswith("+++"):
            new_lines.append(line[1:].strip())

    return old_lines, new_lines

def extract_rhs_expression(line: str) -> str | None:
    if "=" not in line:
        return None

    left, right = line.split("=", 1)
    return right.strip()

def isolate_expression_change(diff_lines: list[str]) -> tuple[str, str] | None:
    old_lines, new_lines = extract_changed_lines(diff_lines)

    if len(old_lines) != 1 or len(new_lines) != 1:
        return None

    old_expr = extract_rhs_expression(old_lines[0])
    new_expr = extract_rhs_expression(new_lines[0])

    if old_expr is None or new_expr is None:
        return None

    return old_expr, new_expr
