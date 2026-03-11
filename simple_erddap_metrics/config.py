import yaml
from pathlib import Path

def load_config(config_path=None):

    if config_path is None:
        config_path = Path(__file__).parent / "resources" / "config.yaml"

    with open(config_path, "r") as f:
        config = yaml.safe_load(f)

    data_formats = set(config.get("data_formats", []))
    system_endpoints = set(config.get("system_endpoints", []))

    return data_formats, system_endpoints