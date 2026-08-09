from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT))
from config import REPETITIONS,SEED
from src.experiments import run_rosenbrock
run_rosenbrock("sceua",REPETITIONS,SEED,Path(__file__).parent/"outputs"/"results")
