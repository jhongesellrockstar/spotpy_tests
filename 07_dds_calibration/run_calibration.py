from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from src.experiments import run_hydrology
run_hydrology("dds",120,"nse",42,output_root=Path(__file__).parent/"outputs")
