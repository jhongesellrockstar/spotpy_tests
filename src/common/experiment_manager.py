"""Non-overwriting experiment folders and provenance files."""
from __future__ import annotations
from datetime import datetime
from pathlib import Path
import json, logging, platform, sys, time
import spotpy

class Experiment:
    def __init__(self, algorithm: str, objective: str, config: dict, root: str | Path = "runs"):
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        self.id = f"{stamp}_{algorithm}_{objective}"; self.path = Path(root) / self.id
        self.figures = self.path / "figures"; self.figures.mkdir(parents=True)
        (self.path / "config.json").write_text(json.dumps(config, indent=2, default=str), encoding="utf-8")
        env = {"python": sys.version, "spotpy": spotpy.__version__, "platform": platform.platform()}
        (self.path / "environment.json").write_text(json.dumps(env, indent=2), encoding="utf-8")
        logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s",
                            handlers=[logging.FileHandler(self.path / "run.log", encoding="utf-8"), logging.StreamHandler()], force=True)
        self.started = time.perf_counter()
    def save_json(self, name: str, value: dict):
        (self.path / name).write_text(json.dumps(value, indent=2, default=float), encoding="utf-8")
    @property
    def elapsed(self): return time.perf_counter() - self.started
