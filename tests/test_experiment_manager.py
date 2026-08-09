from pathlib import Path
from src.common.experiment_manager import Experiment

def test_config_accepts_path(tmp_path):
    exp=Experiment("mc","nse",{"input_file":Path("input.csv")},tmp_path)
    assert 'input.csv' in (exp.path/"config.json").read_text()
