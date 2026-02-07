import yaml
from pathlib import Path


def load_config(path: Path = Path("ledgerdrift.yml")) -> dict:
    if not path.exists():
        raise FileNotFoundError("ledgerdrift.yml not found")

    with path.open("r") as f:
        return yaml.safe_load(f)
