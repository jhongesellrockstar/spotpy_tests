"""Didactic DREAM run with an explicit Gaussian integrated-error log-likelihood."""
from pathlib import Path
import json, sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import spotpy
from src.common.data_loader import load_hydrology_csv
from src.common.hydrology_model import PARAMETER_RANGES, simulate

class BayesianHydrologySetup:
    def __init__(self, data):
        self.data = data
        self.params = [spotpy.parameter.Uniform(name, *bounds) for name, bounds in PARAMETER_RANGES.items()]
    def parameters(self): return spotpy.parameter.generate(self.params)
    def simulation(self, vector):
        return simulate(self.data.precip_mm, self.data.pet_mm,
                        **{name: float(vector[i]) for i, name in enumerate(PARAMETER_RANGES)})
    def evaluation(self): return self.data.q_obs.to_numpy(float)
    def objectivefunction(self, simulation, evaluation, params=None):
        return float(spotpy.likelihoods.gaussianLikelihoodMeasErrorOut(evaluation, simulation))

data = load_hydrology_csv(ROOT / "03_hydrology_demo" / "data" / "input.csv")
dbname = str(Path(__file__).parent / "dream_results")
sampler = spotpy.algorithms.dream(BayesianHydrologySetup(data), dbname=dbname, dbformat="csv", save_sim=False, random_state=42)
r_hats = sampler.sample(140, nChains=7, delta=3, convergence_limit=1.2, runs_after_convergence=20, acceptance_test_option=2)
results = spotpy.analyser.load_csv_results(dbname); frame = pd.DataFrame.from_records(results)
history = np.asarray(r_hats, dtype=float)
pd.DataFrame(history, columns=list(PARAMETER_RANGES)).to_csv(Path(__file__).parent / "gelman_rubin_history.csv", index=False)
final = history[-1] if len(history) else np.full(len(PARAMETER_RANGES), np.nan)
converged = bool(np.isfinite(final).all() and (final < 1.2).all())
(Path(__file__).parent / "convergence.json").write_text(json.dumps({"criterion":"all R-hat < 1.2", "final_r_hat":dict(zip(PARAMETER_RANGES, final.tolist())), "converged":converged, "interpretation":"Didactic budget; false means no convergence claim."}, indent=2), encoding="utf-8")
posterior = spotpy.analyser.get_posterior(results, percentage=20, maximize=True)
pd.DataFrame.from_records(posterior).to_csv(Path(__file__).parent / "posterior_top20.csv", index=False)
fig, axes = plt.subplots(len(PARAMETER_RANGES), 1, figsize=(8, 8), sharex=True)
for ax, name in zip(axes, PARAMETER_RANGES):
    for chain, group in frame.groupby("chain"): ax.plot(group[f"par{name}"].to_numpy(), lw=.7, alpha=.7)
    ax.set_ylabel(name)
axes[-1].set_xlabel("Paso guardado por cadena"); fig.tight_layout(); fig.savefig(Path(__file__).parent / "chain_traces.png", dpi=180); plt.close(fig)
print("DREAM_UNCERTAINTY_DEMO_OK", "converged=" + str(converged), "runs_saved=" + str(len(frame)))

