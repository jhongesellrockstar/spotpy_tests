from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from src.experiments import RosenbrockSetup
__all__=["RosenbrockSetup"]
