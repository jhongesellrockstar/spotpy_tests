"""SPOTPY setup for the hydrology demonstration."""
from __future__ import annotations
import spotpy
from .hydrology_model import PARAMETER_RANGES, simulate
from .hydrological_metrics import nse, kge, rmse

class HydrologySetup:
    def __init__(self, data, objective: str = "nse", minimize: bool = False):
        self.data = data; self.objective = objective.lower(); self.minimize = minimize
        self.params = [spotpy.parameter.Uniform(name, low, high)
                       for name, (low, high) in PARAMETER_RANGES.items()]
    def parameters(self):
        return spotpy.parameter.generate(self.params)
    def simulation(self, vector):
        # Algorithms pass a ParameterSet; a direct educational call to
        # parameters() returns SPOTPY's structured records with a random field.
        raw = vector["random"] if getattr(getattr(vector, "dtype", None), "names", None) else vector
        values = {p.name: float(raw[i]) for i, p in enumerate(self.params)}
        return simulate(self.data.precip_mm, self.data.pet_mm, **values)
    def evaluation(self):
        return self.data.q_obs.to_numpy(dtype=float)
    def objectivefunction(self, simulation, evaluation, params=None):
        functions = {"nse": nse, "kge": kge, "rmse": lambda o, s: -rmse(o, s)}
        if self.objective not in functions:
            raise ValueError(f"Unsupported objective: {self.objective}")
        score = functions[self.objective](evaluation, simulation)
        return -score if self.minimize else score
