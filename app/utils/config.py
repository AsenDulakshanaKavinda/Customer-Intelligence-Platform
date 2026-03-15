from pathlib import Path
from hydra import initialize_config_dir, compose

CONFIG_PATH = Path(__file__).resolve().parents[2] / "configs"

if not CONFIG_PATH.exists():
    raise FileNotFoundError(f"Config directory not found at {CONFIG_PATH}")

def load_config():
    config_path = str(CONFIG_PATH)
    try:
        with initialize_config_dir(version_base=None, config_dir=config_path):
            cfg = compose(config_name="config")
        return cfg
    except Exception as e:
        raise RuntimeError(f"Error while loading configurations: {str(e)}")

cfg = load_config()