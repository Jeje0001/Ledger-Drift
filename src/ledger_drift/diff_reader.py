import subprocess


def get_git_diff() -> str:
    result = subprocess.run(
        ["git", "diff", "HEAD~1..HEAD"],
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

def function_changed(diff_lines: list[str], function_name: str) -> bool:
    for line in diff_lines:
        if function_name in line:
            return True
    return False
