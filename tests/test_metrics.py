import numpy as np,pytest,spotpy
from src.common.hydrological_metrics import nse,kge,rmse,mae,pbias,r2

def test_perfect_metrics():
    x=np.array([1.,2.,4.,8.])
    assert nse(x,x)==pytest.approx(1); assert kge(x,x)==pytest.approx(1)
    assert rmse(x,x)==0; assert mae(x,x)==0; assert pbias(x,x)==0; assert r2(x,x)==pytest.approx(1)
def test_nse_matches_spotpy():
    o=[1,2,3,5];s=[1,2.2,2.8,4.5]
    assert nse(o,s)==pytest.approx(spotpy.objectivefunctions.nashsutcliffe(o,s))
def test_pbias_sign():
    assert pbias([1,1],[2,2])==100
def test_metrics_reject_nan_and_lengths():
    with pytest.raises(ValueError): nse([1,np.nan],[1,2])
    with pytest.raises(ValueError): rmse([1],[1,2])

