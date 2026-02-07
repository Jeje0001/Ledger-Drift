from pathlib import Path

KEYWORDS = [
    "amount",
    "fee",
    "price",
    "rate",
    "balance",
    "total",
    "interest",
    "fx",
]

NUMERIC_PATTERNS = [
    "* 0.",
    "/ 100",
]


def scan_file_for_money_patterns(file_path: Path) -> list[dict]:
    findings = []

    try:
        lines = file_path.read_text().splitlines()
    except Exception:
        return findings  

    line_number = 1

    for line in lines:
        lowered_line = line.lower()

        for keyword in KEYWORDS:
            if keyword in lowered_line:
                findings.append({
                    "file": str(file_path),
                    "line": line_number,
                    "match": keyword,
                    "content": line.strip(),
                })
                break 
        for pattern in NUMERIC_PATTERNS:
            if pattern in line:
                findings.append({
                    "file": str(file_path),
                    "line": line_number,
                    "match": pattern,
                    "content": line.strip(),
                })
                break

        line_number += 1

    return findings
