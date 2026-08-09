"""Didactic five-parameter conceptual rainfall-runoff model."""
from __future__ import annotations
import numpy as np

PARAMETER_RANGES = {
    "runoff_coeff": (0.05, 0.85), "soil_capacity": (20.0, 250.0),
    "et_factor": (0.2, 1.5), "quick_recession": (0.15, 0.95),
    "base_recession": (0.005, 0.25),
}

def simulate(precip, pet, runoff_coeff: float, soil_capacity: float,
             et_factor: float, quick_recession: float, base_recession: float) -> np.ndarray:
    precip = np.asarray(precip, dtype=float); pet = np.asarray(pet, dtype=float)
    if precip.shape != pet.shape or precip.ndim != 1:
        raise ValueError("Precipitation and PET must be equal-length 1-D arrays")
    if not (np.isfinite(precip).all() and np.isfinite(pet).all()):
        raise ValueError("Forcing contains NaN or infinity")
    if soil_capacity <= 0:
        raise ValueError("soil_capacity must be positive")
    soil = 0.5 * soil_capacity; quick = base = 0.0; flow = []
    for rain, demand in zip(precip, pet):
        evap = min(soil, max(0.0, demand * et_factor * soil / soil_capacity))
        soil -= evap
        infiltration = min(max(0.0, rain * (1 - runoff_coeff)), soil_capacity - soil)
        soil += infiltration
        excess = max(0.0, rain - infiltration)
        recharge = 0.02 * soil
        soil -= recharge
        quick += excess; base += recharge
        q_quick = quick_recession * quick; q_base = base_recession * base
        quick -= q_quick; base -= q_base
        flow.append(q_quick + q_base)
    return np.asarray(flow)

