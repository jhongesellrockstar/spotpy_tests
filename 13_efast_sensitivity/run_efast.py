"""Run SPOTPY eFAST at its current five-parameter minimum sample size."""
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import spotpy
from src.common.data_loader import load_hydrology_csv
from src.common.hydrology_model import PARAMETER_RANGES
from src.common.spotpy_setup import HydrologySetup

data = load_hydrology_csv(ROOT / "03_hydrology_demo" / "data" / "input.csv")
setup = HydrologySetup(data, objective="nse", minimize=False)
dbname = str(Path(__file__).parent / "efast_results")
sampler = spotpy.algorithms.efast(setup, dbname=dbname, dbformat="csv", save_sim=False, random_state=42)
sampler.sample(71, freq="cukier")
results = spotpy.analyser.load_csv_results(dbname)
indices = spotpy.analyser.efast_sensitivity(results["like1"], len(PARAMETER_RANGES), 71, sampler.freq_cukier(len(PARAMETER_RANGES)))
summary = pd.DataFrame({"parameter":list(PARAMETER_RANGES), "partial_variance_fraction":indices}).sort_values("partial_variance_fraction", ascending=False)
summary.to_csv(Path(__file__).parent / "efast_sensitivity.csv", index=False)
fig, ax = plt.subplots(); summary.set_index("parameter").plot.bar(y="partial_variance_fraction", legend=False, ax=ax); ax.set_ylabel("Fracción de varianza parcial"); fig.tight_layout(); fig.savefig(Path(__file__).parent / "efast_sensitivity.png", dpi=180); plt.close(fig)
print(summary.to_string(index=False)); print("EFAST_SENSITIVITY_OK")

