from pathlib import Path
import numpy as np,spotpy
from src.common.data_loader import load_hydrology_csv
from src.common.hydrology_model import simulate,PARAMETER_RANGES
from src.common.spotpy_setup import HydrologySetup

SAMPLE=Path(__file__).parents[1]/"03_hydrology_demo"/"data"/"input.csv"
def test_spotpy_import_and_algorithms():
    assert spotpy.__version__=="1.6.7"; assert all(hasattr(spotpy.algorithms,n) for n in ("mc","lhs","fast","sceua","dds"))
def test_model_is_finite_and_nonnegative():
    q=simulate([0,10,0],[2,2,2],.4,100,1,.5,.05)
    assert len(q)==3 and np.isfinite(q).all() and (q>=0).all()
def test_parameter_ranges_and_setup_contract():
    data=load_hydrology_csv(SAMPLE); setup=HydrologySetup(data)
    pars=setup.parameters(); sim=setup.simulation(pars)
    assert len(PARAMETER_RANGES)==5 and len(sim)==len(setup.evaluation())
    assert np.isfinite(setup.objectivefunction(sim,setup.evaluation()))
def test_sceua_sign_is_negated():
    data=load_hydrology_csv(SAMPLE); a=HydrologySetup(data,minimize=False); b=HydrologySetup(data,minimize=True)
    pars=a.parameters(); sim=a.simulation(pars); obs=a.evaluation()
    assert a.objectivefunction(sim,obs)==-b.objectivefunction(sim,obs)

