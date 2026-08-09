from pathlib import Path
import pandas as pd
def parse_verified_flow_csv(path: str|Path, warmup_years: int=0):
    """Prototype parser for a configured CSV, not an assertion about SWAT+ native filenames."""
    frame=pd.read_csv(path)
    if not {"date","q_sim"}.issubset(frame): raise ValueError("Configured output parser expects date,q_sim")
    frame["date"]=pd.to_datetime(frame.date,errors="raise")
    if frame.q_sim.isna().any(): raise ValueError("Simulated flow contains NaN")
    if warmup_years: frame=frame[frame.date >= frame.date.min()+pd.DateOffset(years=warmup_years)]
    return frame.reset_index(drop=True)
