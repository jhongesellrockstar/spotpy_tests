from pathlib import Path
import pandas as pd,pytest
from src.common.data_loader import load_hydrology_csv,align_series

SAMPLE=Path(__file__).parents[1]/"03_hydrology_demo"/"data"/"input.csv"
def test_reader_valid(): assert len(load_hydrology_csv(SAMPLE))==30
def test_reader_missing():
    with pytest.raises(FileNotFoundError): load_hydrology_csv("does_not_exist.csv")
@pytest.mark.parametrize("content",["date,precip_mm\n2020-01-01,1\n","date,precip_mm,pet_mm,q_obs\nbad,1,2,3\n","date,precip_mm,pet_mm,q_obs\n2020-01-01,1,2,NaN\n","date,precip_mm,pet_mm,q_obs\n2020-01-01,x,2,3\n"])
def test_reader_invalid(tmp_path,content):
    p=tmp_path/"bad.csv";p.write_text(content)
    with pytest.raises(ValueError): load_hydrology_csv(p)
def test_alignment():
    d=pd.to_datetime(["2020-01-01","2020-01-02"])
    assert len(align_series(pd.DataFrame({"date":d,"q_obs":[1,2]}),pd.DataFrame({"date":d,"q_sim":[1,2]})))==2
def test_alignment_mismatch():
    with pytest.raises(ValueError): align_series(pd.DataFrame({"date":pd.to_datetime(["2020-01-01"]),"q_obs":[1]}),pd.DataFrame({"date":pd.to_datetime(["2020-01-02"]),"q_sim":[1]}))

