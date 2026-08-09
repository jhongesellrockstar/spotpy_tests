"""Small NSGA-II demonstration: three separate losses, never a weighted sum."""
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import spotpy
from src.common.data_loader import load_hydrology_csv
from src.common.hydrological_metrics import kge, nse, pbias
from src.common.hydrology_model import PARAMETER_RANGES, simulate

class MultiObjectiveSetup:
    n_var = len(PARAMETER_RANGES)
    def __init__(self, data):
        self.data = data
        self.params = [spotpy.parameter.Uniform(name, *bounds) for name, bounds in PARAMETER_RANGES.items()]
    def parameters(self): return spotpy.parameter.generate(self.params)
    def simulation(self, vector):
        return simulate(self.data.precip_mm, self.data.pet_mm,
                        **{name: float(vector[i]) for i, name in enumerate(PARAMETER_RANGES)})
    def evaluation(self): return self.data.q_obs.to_numpy(float)
    def objectivefunction(self, simulation, evaluation, params=None):
        return [1 - nse(evaluation, simulation), 1 - kge(evaluation, simulation), abs(pbias(evaluation, simulation)) / 100]

def nondominated(losses: np.ndarray) -> np.ndarray:
    keep = np.ones(len(losses), dtype=bool)
    for i, candidate in enumerate(losses):
        keep[i] = not np.any(np.all(losses <= candidate, axis=1) & np.any(losses < candidate, axis=1))
    return keep

data = load_hydrology_csv(ROOT / "03_hydrology_demo" / "data" / "input.csv")
dbname = str(Path(__file__).parent / "nsga2_results")
sampler = spotpy.algorithms.NSGAII(MultiObjectiveSetup(data), dbname=dbname, dbformat="csv", save_sim=False, random_state=42)
sampler.sample(generations=5, n_obj=3, n_pop=12)
results = spotpy.analyser.load_csv_results(dbname)
frame = pd.DataFrame.from_records(results)
losses = frame[["like1", "like2", "like3"]].to_numpy(float)
front = frame.loc[nondominated(losses)].copy()
front.rename(columns={"like1":"loss_1_minus_nse", "like2":"loss_1_minus_kge", "like3":"loss_abs_pbias_scaled"}).to_csv(Path(__file__).parent / "pareto_front.csv", index=False)
fig, ax = plt.subplots(figsize=(6.4, 4.8)); ax.scatter(1-frame.like1, 1-frame.like2, c="0.75", label="Evaluados")
ax.scatter(1-front.like1, 1-front.like2, c=front.like3, cmap="viridis_r", edgecolor="black", label="No dominados")
ax.set(xlabel="NSE", ylabel="KGE", title="NSGA-II: trade-off NSE/KGE (color = |PBIAS|/100)"); ax.legend(); fig.tight_layout(); fig.savefig(Path(__file__).parent / "pareto_front.png", dpi=180); plt.close(fig)
print(f"NSGAII_MULTIOBJECTIVE_OK evaluated={len(frame)} pareto={len(front)}")

