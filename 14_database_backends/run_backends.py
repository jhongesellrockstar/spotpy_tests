"""Exercise RAM, CSV, and built-in SQLite databases with identical samples."""
from pathlib import Path
import os, sqlite3, sys, time
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import pandas as pd
import spotpy
from src.experiments import RosenbrockSetup

rows=[]
experiment_dir = Path(__file__).parent.resolve()
os.chdir(experiment_dir)
for backend in ("ram", "csv", "sql"):
    # SPOTPY's SQL writer also uses dbname as the SQL table identifier.  A
    # Windows absolute path contains ':' and is invalid SQL, so use a safe
    # relative name while cwd points at this experiment directory.
    dbname = f"backend_{backend}"
    start=time.perf_counter(); sampler=spotpy.algorithms.mc(RosenbrockSetup(),dbname=dbname,dbformat=backend,save_sim=False,random_state=42);sampler.sample(20)
    if backend=="ram": count=len(sampler.getdata()); artifact="none (process memory)"
    elif backend=="csv": count=len(spotpy.analyser.load_csv_results(dbname)); artifact="backend_csv.csv"
    else:
        with sqlite3.connect(dbname+".db") as connection: count=connection.execute(f'SELECT COUNT(*) FROM "{dbname}"').fetchone()[0]
        artifact="backend_sql.db"
    rows.append({"backend":backend,"records":count,"runtime_seconds":time.perf_counter()-start,"persistent":backend!="ram","artifact":artifact})
pd.DataFrame(rows).to_csv(experiment_dir/"backend_summary.csv",index=False)
print(pd.DataFrame(rows).to_string(index=False)); print("DATABASE_BACKENDS_OK")
