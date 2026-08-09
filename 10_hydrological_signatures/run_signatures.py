"""Compute only signatures that remain interpretable for a 30-day demo series."""
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import pandas as pd
from spotpy.hydrology import signatures
from src.common.data_loader import load_hydrology_csv

data = load_hydrology_csv(ROOT / "03_hydrology_demo" / "data" / "input.csv")
q = data.q_obs.to_numpy(float)
methods = {
    "mean_flow": signatures.get_mean,
    "q05_exceedance": signatures.get_q5,
    "q50_exceedance": signatures.get_q50,
    "q95_exceedance": signatures.get_q95,
    "coefficient_variation": signatures.get_qcv,
    "mean_over_median_skewness": signatures.get_skewness,
    "lag1_autocorrelation": signatures.get_ac,
    "zero_flow_frequency": signatures.get_zero_q_freq,
}
units = {
    "mean_flow": "UNIDAD NO DEFINIDA EN EL LABORATORIO ACTUAL",
    "q05_exceedance": "UNIDAD NO DEFINIDA EN EL LABORATORIO ACTUAL",
    "q50_exceedance": "UNIDAD NO DEFINIDA EN EL LABORATORIO ACTUAL",
    "q95_exceedance": "UNIDAD NO DEFINIDA EN EL LABORATORIO ACTUAL",
    "coefficient_variation": "[-]", "mean_over_median_skewness": "[-]",
    "lag1_autocorrelation": "[-]", "zero_flow_frequency": "% de pasos",
}
rows = [{"signature": name, "value": float(function(q)), "unit": units[name],
         "input": "q_obs; 30 valores diarios; sin NaN"} for name, function in methods.items()]
out = Path(__file__).parent / "hydrological_signatures.csv"
pd.DataFrame(rows).to_csv(out, index=False)
print(pd.DataFrame(rows).to_string(index=False)); print("HYDROLOGICAL_SIGNATURES_OK", out)

