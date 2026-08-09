from pathlib import Path
import importlib.util,subprocess,pytest,pandas as pd

ROOT=Path(__file__).parents[1]
def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path);module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module
runner=load("external_model_runner",ROOT/"08_external_model_adapter"/"external_model_runner.py")
parser=load("output_parser",ROOT/"09_swatplus_adapter_prototype"/"output_parser.py")
config=load("swat_config",ROOT/"09_swatplus_adapter_prototype"/"config.py")

def test_external_runner(tmp_path):
    result=runner.run_external_model({"runoff_coeff":.4,"et_loss":.1},ROOT/"03_hydrology_demo"/"data"/"input.csv",work_root=tmp_path)
    assert len(result)==30 and (result.q_sim>=0).all() and not list(tmp_path.iterdir())
def test_external_failure(tmp_path):
    with pytest.raises(runner.ExternalModelError,match="returncode"):
        runner.run_external_model({"runoff_coeff":.4,"et_loss":.1},ROOT/"03_hydrology_demo"/"data"/"input.csv",work_root=tmp_path,fail=True)
def test_timeout(monkeypatch,tmp_path):
    def timeout(*args,**kwargs): raise subprocess.TimeoutExpired(args[0],kwargs["timeout"])
    monkeypatch.setattr(runner.subprocess,"run",timeout)
    with pytest.raises(runner.ExternalModelError,match="timeout"):
        runner.run_external_model({"runoff_coeff":.4,"et_loss":.1},ROOT/"03_hydrology_demo"/"data"/"input.csv",work_root=tmp_path)
def test_output_parser(tmp_path):
    p=tmp_path/"out.csv";p.write_text("date,q_sim\n2020-01-01,1.2\n")
    assert parser.parse_verified_flow_csv(p).q_sim.iloc[0]==1.2
def test_config(): assert config.load_config()["WARMUP_YEARS"]==2

