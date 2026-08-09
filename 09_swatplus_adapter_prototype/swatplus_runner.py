"""Subprocess shell for a future verified SWAT+ executable."""
from pathlib import Path
import subprocess
def run_swatplus(executable: str|Path, workdir: str|Path, timeout: float):
    exe=Path(executable); cwd=Path(workdir)
    if not exe.is_file(): raise FileNotFoundError(f"SWAT+ executable not configured/verified: {exe}")
    if not cwd.is_dir(): raise FileNotFoundError(f"SWAT+ working directory missing: {cwd}")
    result=subprocess.run([str(exe)],cwd=cwd,timeout=timeout,capture_output=True,text=True,check=False)
    if result.returncode: raise RuntimeError(f"SWAT+ returncode={result.returncode}; stderr={result.stderr[-2000:]}")
    return result
