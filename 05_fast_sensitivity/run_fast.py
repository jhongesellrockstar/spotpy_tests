from pathlib import Path
import sys,shutil
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from src.experiments import run_hydrology
p=run_hydrology("fast",325,"nse",42,output_root=Path(__file__).parent/"outputs"/"runs")
shutil.copy2(p/"fast_sensitivity.csv",Path(__file__).parent/"outputs"/"fast_sensitivity.csv")
print("FAST_SENSITIVITY_OK")
