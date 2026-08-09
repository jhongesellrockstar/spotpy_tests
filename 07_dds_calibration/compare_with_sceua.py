"""Build a transparent SCE-UA vs DDS table from latest local runs."""
from pathlib import Path
import json,pandas as pd
root=Path(__file__).resolve().parents[1]
rows=[]
for algorithm,folder in (("sceua",root/"06_sceua_calibration"/"outputs"),("dds",root/"07_dds_calibration"/"outputs")):
    candidates=sorted((p for p in folder.iterdir() if p.is_dir() and (p/"metrics.json").is_file()),key=lambda p:p.stat().st_mtime)
    if not candidates: raise SystemExit(f"Run {algorithm} calibration first")
    m=json.loads((candidates[-1]/"metrics.json").read_text())
    rows.append({"algorithm":algorithm,"runs":m["evaluations_completed"],"runtime_seconds":m["runtime_seconds"],"best_NSE":m["NSE"],"best_KGE":m["KGE"],"RMSE":m["RMSE"],"PBIAS":m["PBIAS"]})
out=Path(__file__).parent/"outputs"/"comparison_sceua_dds.csv"
pd.DataFrame(rows).to_csv(out,index=False);print(pd.DataFrame(rows).to_string(index=False));print("CALIBRATION_COMPARISON_OK",out)
