from pathlib import Path
import json,sys,pandas as pd
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from src.experiments import run_hydrology
cfg=json.loads((Path(__file__).parent/"config"/"experiment.json").read_text())
rows=[]
for name in cfg["algorithms"]:
 p=run_hydrology(name,cfg["repetitions"],cfg["objective_function"],cfg["seed"])
 m=json.loads((p/"metrics.json").read_text()); rows.append(m)
pd.DataFrame(rows).to_csv(Path(__file__).parent/"comparison.csv",index=False)
print("ALGORITHM_COMPARISON_OK")
