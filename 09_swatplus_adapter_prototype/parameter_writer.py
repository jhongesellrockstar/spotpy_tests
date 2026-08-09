"""Safe placeholder interface; deliberately does not edit real SWAT+ files."""
from pathlib import Path
import json
def write_parameters(workdir: str|Path, parameters: dict) -> Path:
    target=Path(workdir)/"spotpy_parameters_mock.json"
    target.write_text(json.dumps(parameters,indent=2),encoding="utf-8")
    return target
