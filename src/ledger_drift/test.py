from pathlib import Path
from heuristics import scan_file_for_money_patterns

results = scan_file_for_money_patterns(Path("some_file.py"))
print(results)
