import subprocess
import re
import ast

def get_git_diff() -> str:
    result = subprocess.run(
        ["git", "diff"],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        raise RuntimeError("Failed to run git diff")

    return result.stdout


def extract_file_diffs(diff: str) -> dict[str, list[str]]:
    file_diffs = {}
    current_file = None

    for line in diff.splitlines():
        if line.startswith("diff --git"):
            parts = line.split()
            if len(parts) >= 4:
                file_path = parts[2].replace("a/", "")
                current_file = file_path
                file_diffs[current_file] = []
            continue

        if current_file is not None:
            file_diffs[current_file].append(line)

    return file_diffs



def get_changed_line_numbers(diff_lines: list[str]) -> set[int]:
    changed_lines = set()
    current_line = 0
    
    for line in diff_lines:
        if line.startswith('@@'):
            match = re.search(r'\+(\d+)(?:,(\d+))?', line)
            if match:
                current_line = int(match.group(1))
            continue
        
        if line.startswith('+') or line.startswith(' '):
            if line.startswith('+'):
                changed_lines.add(current_line)
            current_line += 1
        elif line.startswith('-'):
            changed_lines.add(current_line) 
            
    return changed_lines

def get_function_line_range(file_path: str, function_name: str) -> tuple[int, int] | None:
    try:
        with open(file_path, "r") as f:
            tree = ast.parse(f.read())
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name == function_name:

                return (node.lineno, node.end_lineno)
    except Exception:
        return None
    return None

def function_changed(file_path: str, diff_lines: list[str], function_name: str) -> bool:
    line_range = get_function_line_range(file_path, function_name)
    if not line_range:
        return False
    
    start, end = line_range
    
    changed_lines = get_changed_line_numbers(diff_lines)
    
    for line_num in changed_lines:
        if start <= line_num <= end:
            return True
            
    return False
