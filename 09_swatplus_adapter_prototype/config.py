from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
def load_config(path=ROOT/"config"/"swatplus_example.json"):
    data=json.loads(Path(path).read_text(encoding="utf-8"))
    required={"SWAT_EXECUTABLE","SWAT_PROJECT_DIR","OBSERVED_FLOW_FILE","SIMULATED_FLOW_FILE","WARMUP_YEARS","TIMEOUT_SECONDS"}
    missing=required-data.keys()
    if missing: raise ValueError(f"Missing SWAT+ config keys: {sorted(missing)}")
    return data
