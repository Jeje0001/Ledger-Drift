from pathlib import Path

def find_enclosing_function(file_path: Path, target_line: int) -> str | None:
    try:
        lines = file_path.read_text().splitlines()
    except Exception:
        return None

    index = target_line - 1

    while index >= 0:
        line = lines[index].strip()

        if line.startswith("def "):
            name_part = line.split("def ")[1]
            function_name = name_part.split("(")[0].strip()
            return function_name

        index -= 1

    return None
