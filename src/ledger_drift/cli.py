from pathlib import Path
import typer

from ledger_drift.scanner import find_python_files
from ledger_drift.heuristics import scan_file_for_money_patterns
from ledger_drift.context import find_enclosing_function
from ledger_drift.exit_codes import *
from ledger_drift.rules import infer_rule_type
from ledger_drift.config import load_config
from ledger_drift.diff_reader import ( get_git_diff, extract_file_diffs, function_changed,)
from ledger_drift.expression import isolate_expression_change

app = typer.Typer(no_args_is_help=True)


@app.command()
def init():
    """Initialize Ledger Drift in the current repository."""
    typer.echo("Initializing Ledger Drift...\n")

    root = Path(".")
    python_files = find_python_files(root)

    findings = []

    for file_path in python_files:
        matches = scan_file_for_money_patterns(file_path)

        for match in matches:
            function_name = find_enclosing_function(
                file_path,
                match["line"]
            )

            if function_name is None:
                continue

            findings.append({
                "file": match["file"],
                "function": function_name
            })

    if not findings:
        typer.echo("No obvious money-handling logic found.")
        return

    typer.echo("Found money-related functions:\n")

    seen = set()

    for item in findings:
        key = (item["file"], item["function"])
        if key in seen:
            continue

        seen.add(key)
        typer.echo(f"- {item['file']}::{item['function']}")
    
        config_path = Path("ledgerdrift.yml")

    if config_path.exists():
        typer.echo("\nledgerdrift.yml already exists. Skipping config generation.")
        return

    

    lines = []
    lines.append("version: 1")
    lines.append("fail_on_drift: false")
    lines.append("")
    lines.append("rules:")

    added_any = False

    for file_path, function_name in seen:
        typer.echo(f"\nMonitor {file_path}::{function_name}?")
        confirm = typer.confirm("Add this function to Ledger Drift?", default=True)

        if not confirm:
            continue

        rule_type = infer_rule_type(function_name)

        lines.append(f"  - type: {rule_type}")
        lines.append(f"    file: {file_path}")
        lines.append(f"    function: {function_name}")
        lines.append(f"    tolerance: 0.02")
        lines.append("")

        added_any = True

    if not added_any:
        typer.echo("\nNo functions selected. No config generated.")
        return

    config_path.write_text("\n".join(lines))
    typer.echo("\nledgerdrift.yml created.")


@app.command()
def analyze():
    

    typer.echo("Analyzing repository for financial drift...\n")

    config = load_config()
    rules = config.get("rules", [])

    diff = get_git_diff()
    file_diffs = extract_file_diffs(diff)

    any_change = False

    for rule in rules:
        file_path = rule["file"]
        function_name = rule["function"]

        if file_path not in file_diffs:
            continue

        diff_lines = file_diffs[file_path]


        if function_changed(diff_lines, function_name):
            typer.echo(f"Detected change in {file_path}::{function_name}")
            any_change = True
            
            expr_change = isolate_expression_change(diff_lines)

            if expr_change is None:
                typer.echo(
                    f"Change detected in {file_path}::{function_name}, "
                    "but unable to isolate expression safely."
                )
                continue

            old_expr, new_expr = expr_change
            typer.echo("Expression change:")
            typer.echo(f"  OLD: {old_expr}")
            typer.echo(f"  NEW: {new_expr}")

    if not any_change:
        typer.echo("No relevant financial changes detected.")
        raise typer.Exit(code=0)

    raise typer.Exit(code=1)
