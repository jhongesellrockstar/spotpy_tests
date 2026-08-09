"""Execution and analysis shared by the CLI and numbered examples."""
from __future__ import annotations
from pathlib import Path
import contextlib, io, json, logging, random
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import spotpy
from .common.data_loader import load_hydrology_csv
from .common.experiment_manager import Experiment
from .common.hydrological_metrics import all_metrics
from .common.hydrology_model import PARAMETER_RANGES, simulate
from .common.spotpy_setup import HydrologySetup

ALGORITHMS = {"mc": spotpy.algorithms.mc, "lhs": spotpy.algorithms.lhs,
              "sceua": spotpy.algorithms.sceua, "dds": spotpy.algorithms.dds,
              "fast": spotpy.algorithms.fast}

def _records(results) -> pd.DataFrame:
    return pd.DataFrame.from_records(results)

def run_hydrology(algorithm="sceua", repetitions=120, objective="nse", seed=42,
                  input_file="03_hydrology_demo/data/input.csv", output_root="runs") -> Path:
    algorithm = algorithm.lower()
    if algorithm not in ALGORITHMS: raise ValueError(f"Algorithm must be one of {sorted(ALGORITHMS)}")
    if repetitions < 2: raise ValueError("repetitions must be >= 2")
    if algorithm == "fast" and repetitions < 325:
        logging.warning("FAST adjusted from %s to 325 runs (5 parameters, M=4)", repetitions); repetitions = 325
    config = dict(example="hydrology", algorithm=algorithm, repetitions=repetitions,
                  objective_function=objective, seed=seed, database_format="csv", input_file=input_file)
    exp = Experiment(algorithm, objective, config, output_root)
    data = load_hydrology_csv(input_file)
    initial_params = {name: (bounds[0] + bounds[1]) / 2 for name, bounds in PARAMETER_RANGES.items()}
    initial_sim = simulate(data.precip_mm, data.pet_mm, **initial_params)
    minimize = algorithm == "sceua"
    setup = HydrologySetup(data, objective, minimize=minimize)
    dbname = str(exp.path / "results")
    random.seed(seed); np.random.seed(seed)
    sampler = ALGORITHMS[algorithm](setup, dbname=dbname, dbformat="csv", save_sim=True, random_state=seed)
    if algorithm == "sceua": sampler.sample(repetitions, ngs=6, kstop=10)
    elif algorithm == "dds": sampler.sample(repetitions)
    elif algorithm == "fast": sampler.sample(repetitions, M=4)
    else: sampler.sample(repetitions)
    results = spotpy.analyser.load_csv_results(dbname)
    frame = _records(results); like = frame["like1"].astype(float)
    database_best = float(like.min() if minimize else like.max())
    best_values = sampler.status.params_min if minimize else sampler.status.params_max
    algorithm_best = float(sampler.status.objectivefunction_min if minimize else sampler.status.objectivefunction_max)
    params = {name: float(value) for name, value in zip(PARAMETER_RANGES, best_values)}
    qbest = simulate(data.precip_mm, data.pet_mm, **params)
    metrics = all_metrics(data.q_obs, qbest)
    metrics.update({"algorithm_best_objective": algorithm_best, "database_best_objective": database_best,
                    "runtime_seconds": exp.elapsed, "algorithm": algorithm,
                    "evaluations_completed": int(sampler.status.rep), "runs_saved": len(frame)})
    exp.save_json("metrics.json", metrics)
    pd.DataFrame([params]).to_csv(exp.path / "parameters.csv", index=False)
    pd.DataFrame([initial_params]).to_csv(exp.path / "initial_parameters.csv", index=False)
    pd.DataFrame({"date": data.date, "q_obs": data.q_obs, "q_sim_initial": initial_sim}).to_csv(exp.path / "initial_simulation.csv", index=False)
    pd.DataFrame({"date": data.date, "q_obs": data.q_obs, "q_sim": qbest}).to_csv(exp.path / "best_simulation.csv", index=False)
    fig, ax = plt.subplots(figsize=(9, 4)); ax.plot(data.date, data.q_obs, label="Observed"); ax.plot(data.date, qbest, label="Best simulation")
    ax.set(ylabel="Discharge (demo units)", title=f"{algorithm.upper()} best run"); ax.legend(); fig.autofmt_xdate(); fig.tight_layout(); fig.savefig(exp.figures / "hydrograph_best_run.png"); plt.close(fig)
    fig, ax = plt.subplots(); ax.plot(frame.index, like); ax.set(xlabel="Saved run", ylabel="Stored objective", title="Objective trace"); fig.tight_layout(); fig.savefig(exp.figures / "objective_trace.png"); plt.close(fig)
    fig, axes = plt.subplots(len(PARAMETER_RANGES), 1, figsize=(8, 8), sharex=True)
    for ax, name in zip(axes, PARAMETER_RANGES): ax.plot(frame.index, frame[f"par{name}"], lw=.8); ax.set_ylabel(name)
    axes[-1].set_xlabel("Saved run"); fig.tight_layout(); fig.savefig(exp.figures / "parameter_trace.png"); plt.close(fig)
    if algorithm == "fast":
        # SPOTPY 1.6.7 still prints intermediate arrays when print_to_console=False.
        # Capture them in the detailed log and keep the terminal concise.
        captured = io.StringIO()
        with contextlib.redirect_stdout(captured):
            indices = spotpy.analyser.get_sensitivity_of_fast(results, print_to_console=False)
        logging.debug("SPOTPY FAST analyser output:\n%s", captured.getvalue())
        sensitivity = pd.DataFrame({"parameter": list(PARAMETER_RANGES), "S1": indices["S1"], "ST": indices["ST"]}).sort_values("ST", ascending=False)
        sensitivity.to_csv(exp.path / "fast_sensitivity.csv", index=False)
        fig, ax = plt.subplots(); sensitivity.set_index("parameter")[["S1", "ST"]].plot.bar(ax=ax); fig.tight_layout(); fig.savefig(exp.figures / "fast_sensitivity.png"); plt.close(fig)
    logging.info("Experiment %s complete: NSE=%.4f", exp.id, metrics["NSE"])
    print(f"EXPERIMENT_OK {exp.path}")
    return exp.path

class RosenbrockSetup:
    params = [spotpy.parameter.Uniform("x", -2, 2), spotpy.parameter.Uniform("y", -1, 3)]
    def parameters(self): return spotpy.parameter.generate(self.params)
    def simulation(self, vector): return [float(vector[0]), float(vector[1])]
    def evaluation(self): return [1.0, 1.0]
    def objectivefunction(self, simulation, evaluation, params=None):
        x, y = simulation; return (1 - x) ** 2 + 100 * (y - x*x) ** 2

def run_rosenbrock(algorithm="mc", repetitions=100, seed=42, output_root="runs") -> Path:
    if algorithm not in {"mc", "sceua"}: raise ValueError("Rosenbrock supports mc or sceua")
    exp = Experiment(algorithm, "rosenbrock_min", {"example":"rosenbrock","algorithm":algorithm,"repetitions":repetitions,"seed":seed}, output_root)
    cls = spotpy.algorithms.mc if algorithm == "mc" else spotpy.algorithms.sceua
    sampler = cls(RosenbrockSetup(), dbname=str(exp.path / "results"), dbformat="csv", save_sim=False, random_state=seed)
    sampler.sample(repetitions, ngs=3, kstop=10) if algorithm == "sceua" else sampler.sample(repetitions)
    frame = _records(spotpy.analyser.load_csv_results(str(exp.path / "results")))
    params={"x":float(sampler.status.params_min[0]),"y":float(sampler.status.params_min[1])}
    exp.save_json("metrics.json", {"rosenbrock":float(sampler.status.objectivefunction_min),"distance_to_optimum":float(np.hypot(params['x']-1,params['y']-1)),"runtime_seconds":exp.elapsed})
    pd.DataFrame([params]).to_csv(exp.path / "parameters.csv", index=False)
    fig, ax=plt.subplots(); ax.scatter(frame.parx,frame.pary,c=frame.like1,s=16); ax.scatter([1],[1],marker="*",s=180,label="Optimum"); ax.legend(); fig.tight_layout(); fig.savefig(exp.figures/"parameter_space.png"); plt.close(fig)
    print(f"ROSENBROCK_OK {exp.path}"); return exp.path
