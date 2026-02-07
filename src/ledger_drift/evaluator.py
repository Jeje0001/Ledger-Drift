import ast


ALLOWED_NODES = (
    ast.Expression,
    ast.BinOp,
    ast.Add,
    ast.Sub,
    ast.Mult,
    ast.Div,
    ast.Constant,
    ast.Name,
)


def is_safe_expression(expr: str, allowed_names: set[str]) -> bool:
    try:
        tree = ast.parse(expr, mode="eval")
    except SyntaxError:
        return False

    for node in ast.walk(tree):
        if not isinstance(node, ALLOWED_NODES):
            return False

        if isinstance(node, ast.Name) and node.id not in allowed_names:
            return False

    return True


def evaluate_expression(expr: str, context: dict[str, float]) -> float:
    tree = ast.parse(expr, mode="eval")

    compiled = compile(tree, filename="<expr>", mode="eval")

    return eval(compiled, {}, context)

def safe_evaluate(expr: str, context: dict[str, float]) -> float | None:
    if not is_safe_expression(expr, set(context.keys())):
        return None

    try:
        return evaluate_expression(expr, context)
    except Exception:
        return None
