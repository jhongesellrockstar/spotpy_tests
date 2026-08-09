"""Strict CSV input and observed/simulated alignment."""
from __future__ import annotations
from pathlib import Path
import pandas as pd

REQUIRED_COLUMNS = ("date", "precip_mm", "pet_mm", "q_obs")

def load_hydrology_csv(path: str | Path) -> pd.DataFrame:
    path = Path(path)
    if not path.is_file():
        raise FileNotFoundError(f"Hydrology input does not exist: {path}")
    frame = pd.read_csv(path)
    missing = [name for name in REQUIRED_COLUMNS if name not in frame.columns]
    if missing:
        raise ValueError(f"Missing required columns in {path}: {missing}")
    try:
        frame["date"] = pd.to_datetime(frame["date"], errors="raise")
        for name in REQUIRED_COLUMNS[1:]:
            frame[name] = pd.to_numeric(frame[name], errors="raise")
    except Exception as exc:
        raise ValueError(f"Invalid date or non-numeric value in {path}: {exc}") from exc
    if frame[list(REQUIRED_COLUMNS)].isna().any().any():
        raise ValueError(f"NaN values are not allowed in {path}")
    if frame.empty or frame["date"].duplicated().any() or not frame["date"].is_monotonic_increasing:
        raise ValueError(f"Dates must be unique, ordered, and non-empty in {path}")
    if (frame[["precip_mm", "pet_mm", "q_obs"]] < 0).any().any():
        raise ValueError(f"Hydrological input values must be non-negative in {path}")
    return frame

def align_series(observed: pd.DataFrame, simulated: pd.DataFrame) -> pd.DataFrame:
    for frame, value in ((observed, "q_obs"), (simulated, "q_sim")):
        if not {"date", value}.issubset(frame.columns):
            raise ValueError(f"Expected columns date and {value}")
    merged = observed[["date", "q_obs"]].merge(simulated[["date", "q_sim"]], on="date", validate="one_to_one")
    if len(merged) != len(observed) or len(merged) != len(simulated):
        raise ValueError("Observed and simulated dates/lengths do not align")
    if merged[["q_obs", "q_sim"]].isna().any().any():
        raise ValueError("Aligned series contain NaN")
    return merged

