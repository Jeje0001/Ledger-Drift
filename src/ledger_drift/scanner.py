from pathlib import Path

IGNORED_DIRS = {
    ".git",
    "__pycache__",
    "venv",
    ".venv",
    "node_modules",
    "dist",
    "build",
    "ledger_drift"
}

def find_python_files(root: Path) -> list[Path]:
    python_files = []

    for path in root.rglob("*.py"):
        should_ignore = False

        for part in path.parts:
            if part in IGNORED_DIRS:
                should_ignore = True
                break

        if should_ignore:
            continue

        python_files.append(path)

    return python_files
