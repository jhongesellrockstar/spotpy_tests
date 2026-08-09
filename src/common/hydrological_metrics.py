"""Small, independently testable hydrological metrics (observed first)."""
from __future__ import annotations
import numpy as np

def _arrays(observed, simulated):
    obs = np.asarray(observed, dtype=float)
    sim = np.asarray(simulated, dtype=float)
    if obs.ndim != 1 or sim.ndim != 1 or len(obs) != len(sim) or len(obs) == 0:
        raise ValueError("Observed and simulated must be non-empty 1-D arrays of equal length")
    if not (np.isfinite(obs).all() and np.isfinite(sim).all()):
        raise ValueError("Metrics do not accept NaN or infinite values")
    return obs, sim

def nse(observed, simulated) -> float:
    obs, sim = _arrays(observed, simulated)
    denominator = np.sum((obs - np.mean(obs)) ** 2)
    if denominator == 0:
        raise ValueError("NSE is undefined for constant observations")
    return float(1 - np.sum((sim - obs) ** 2) / denominator)

def kge(observed, simulated) -> float:
    obs, sim = _arrays(observed, simulated)
    if np.mean(obs) == 0 or np.std(obs) == 0 or np.mean(sim) == 0:
        raise ValueError("KGE is undefined for zero mean/variance inputs")
    r = np.corrcoef(obs, sim)[0, 1]
    alpha = np.std(sim) / np.std(obs)
    beta = np.mean(sim) / np.mean(obs)
    return float(1 - np.sqrt((r - 1) ** 2 + (alpha - 1) ** 2 + (beta - 1) ** 2))

def rmse(observed, simulated) -> float:
    obs, sim = _arrays(observed, simulated)
    return float(np.sqrt(np.mean((sim - obs) ** 2)))

def mae(observed, simulated) -> float:
    obs, sim = _arrays(observed, simulated)
    return float(np.mean(np.abs(sim - obs)))

def pbias(observed, simulated) -> float:
    obs, sim = _arrays(observed, simulated)
    if np.sum(obs) == 0:
        raise ValueError("PBIAS is undefined when observed sum is zero")
    return float(100 * np.sum(sim - obs) / np.sum(obs))

def r2(observed, simulated) -> float:
    obs, sim = _arrays(observed, simulated)
    return float(np.corrcoef(obs, sim)[0, 1] ** 2)

def all_metrics(observed, simulated) -> dict[str, float]:
    return {"NSE": nse(observed, simulated), "KGE": kge(observed, simulated),
            "RMSE": rmse(observed, simulated), "MAE": mae(observed, simulated),
            "PBIAS": pbias(observed, simulated), "R2": r2(observed, simulated)}

