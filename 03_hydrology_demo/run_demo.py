from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT))
from src.experiments import run_hydrology
run_hydrology("mc",50,"nse",42,Path(__file__).parent/"data"/"input.csv",Path(__file__).parent/"outputs")
