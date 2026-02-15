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
    old_lines = []
    new_lines = []

    for line in diff_lines:
        if line.startswith(('---', '+++', '@@')):
            continue

        prefix = line[0] if line else ''
        code = line[1:]

        if prefix == '-':
            clean_code = code.split('#')[0].strip()
            if "return" in clean_code or "=" in clean_code:
                old_lines.append(clean_code)

        elif prefix == '+':
            clean_code = code.split('#')[0].strip()
            if "return" in clean_code or "=" in clean_code:
                new_lines.append(clean_code)

    if len(old_lines) != 1 or len(new_lines) != 1:
        return None

    def extract_math_expression(code_line: str) -> str:
        if "return" in code_line:
            return code_line.split("return", 1)[1].strip()
        if "=" in code_line:
            return code_line.rsplit("=", 1)[1].strip()
        return code_line.strip()

    old_expr = extract_math_expression(old_lines[0])
    new_expr = extract_math_expression(new_lines[0])

    return old_expr, new_expr