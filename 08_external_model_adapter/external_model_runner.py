"""Robust subprocess adapter illustrating the contract required by SPOTPY."""
from __future__ import annotations
from pathlib import Path
import json,shutil,subprocess,sys,uuid
import pandas as pd

class ExternalModelError(RuntimeError): pass

def run_external_model(parameters: dict[str,float], input_file: str|Path, *, timeout_seconds: float=10,
                       work_root: str|Path|None=None, preserve: bool=False, fail: bool=False) -> pd.DataFrame:
    source=Path(input_file).resolve()
    if not source.is_file(): raise FileNotFoundError(source)
    root=Path(work_root or Path(__file__).parent/"workdirs").resolve(); root.mkdir(parents=True,exist_ok=True)
    run_dir=root/f"worker_{uuid.uuid4().hex}"; run_dir.mkdir()
    parameter_file=run_dir/"parameters.json"; output_file=run_dir/"output.csv"
    parameter_file.write_text(json.dumps(parameters,indent=2),encoding="utf-8")
    command=[sys.executable,str(Path(__file__).with_name("fake_external_model.py")),"--parameters",str(parameter_file),"--input",str(source),"--output",str(output_file)]
    if fail: command.append("--fail")
    try:
        try: completed=subprocess.run(command,cwd=run_dir,timeout=timeout_seconds,capture_output=True,text=True,check=False)
        except subprocess.TimeoutExpired as exc: raise ExternalModelError(f"External model timeout after {timeout_seconds}s in {run_dir}") from exc
        (run_dir/"stdout.txt").write_text(completed.stdout,encoding="utf-8"); (run_dir/"stderr.txt").write_text(completed.stderr,encoding="utf-8")
        if completed.returncode != 0: raise ExternalModelError(f"External model returncode={completed.returncode}; stderr={completed.stderr.strip()}")
        if not output_file.is_file(): raise ExternalModelError(f"Expected output missing: {output_file}")
        output=pd.read_csv(output_file)
        if not {"date","q_sim"}.issubset(output) or output.q_sim.isna().any(): raise ExternalModelError("Output schema invalid or contains NaN")
        return output
    finally:
        if not preserve and run_dir.exists(): shutil.rmtree(run_dir)

