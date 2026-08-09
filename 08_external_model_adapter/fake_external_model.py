"""Tiny command-line model: parameters JSON + forcing CSV -> output CSV."""
from __future__ import annotations
import argparse,json
from pathlib import Path
import pandas as pd

parser=argparse.ArgumentParser(); parser.add_argument("--parameters",required=True);parser.add_argument("--input",required=True);parser.add_argument("--output",required=True);parser.add_argument("--fail",action="store_true")
args=parser.parse_args()
if args.fail: raise SystemExit("Requested demonstration failure")
params=json.loads(Path(args.parameters).read_text(encoding="utf-8")); data=pd.read_csv(args.input)
if not {"date","precip_mm","pet_mm"}.issubset(data): raise ValueError("Input schema invalid")
data["q_sim"]=(data.precip_mm*float(params["runoff_coeff"])-data.pet_mm*float(params["et_loss"])).clip(lower=0)
data[["date","q_sim"]].to_csv(args.output,index=False)
print(f"FAKE_MODEL_OK rows={len(data)}")

