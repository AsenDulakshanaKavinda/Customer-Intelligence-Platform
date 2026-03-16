from pathlib import Path
from hydra import initialize_config_dir, compose
from omegaconf import DictConfig

# Resolve the absolute path to the 'configs' directory relative to this file.
CONFIG_PATH = Path(__file__).resolve().parents[2] / "configs"

if not CONFIG_PATH.exists():
    raise FileNotFoundError(f"Config directory not found at {CONFIG_PATH}")

def load_config() -> DictConfig:
    """
    Initializes Hydra and composes the project configuration.

    This function locates the configuration directory, initializes the 
    Hydra context, and merges the default 'config.yaml' into a single 
    DictConfig object.

    Returns:
        DictConfig: A dictionary-like object containing the merged configurations.

    Raises:
        RuntimeError: If Hydra fails to initialize or the config file is missing/invalid.
    """

    config_path = str(CONFIG_PATH)
    try:
        with initialize_config_dir(version_base=None, config_dir=config_path):
            cfg = compose(config_name="config")
        return cfg
    except Exception as e:
        raise RuntimeError(f"Error while loading configurations: {str(e)}")

cfg = load_config()