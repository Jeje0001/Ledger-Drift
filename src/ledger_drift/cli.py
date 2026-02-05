import typer
from pathlib import Path
from ledger_drift.exit_codes import SUCCESS

app = typer.Typer(no_args_is_help=True)


@app.command()
def init():
    """Initialize Ledger Drift in the current repository."""
    config_path = Path("ledgerdrift.yml")

    if config_path.exists():
        typer.echo("ledgerdrift.yml already exists. Skipping initialization.")
        return

    default_config = (
        "version: 1\n"
        "fail_on_drift: false\n"
        "rules: []\n"
    )

    config_path.write_text(default_config)

    typer.echo("Created ledgerdrift.yml with default configuration.")



@app.command()
def analyze():
    """Analyze diffs for financial drift."""
    typer.echo("Analyzing repository for financial drift...")
    raise typer.Exit(code=SUCCESS)
