from pathlib import Path
from dataclasses import dataclass

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
EXCEL_DATASET_PATH = DATA_DIR / "EC_EV_dataset (fixed error).xlsx"

@dataclass
class SimulationConfig:
    """Simulation control parameters."""
    time_step_hours: float = 0.25
    excel_path: Path = EXCEL_DATASET_PATH
    energy_balance_tolerance: float = 1e-4
