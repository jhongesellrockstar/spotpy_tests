from pathlib import Path
import json
root=Path(__file__).parent/"outputs"/"results"
runs=sorted((p for p in root.glob("*") if p.is_dir()),key=lambda p:p.stat().st_mtime)
if not runs: raise SystemExit("No results. Run run_mc.py or run_sceua.py first.")
latest=runs[-1]
print("Latest:",latest); print((latest/"metrics.json").read_text(encoding="utf-8")); print((latest/"parameters.csv").read_text(encoding="utf-8"))
