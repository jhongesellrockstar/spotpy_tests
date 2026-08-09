from pathlib import Path
from external_model_runner import run_external_model
root=Path(__file__).resolve().parents[1]
result=run_external_model({"runoff_coeff":0.45,"et_loss":0.08},root/"03_hydrology_demo"/"data"/"input.csv")
out=Path(__file__).parent/"output.csv"; result.to_csv(out,index=False)
print(result.head().to_string(index=False)); print("EXTERNAL_MODEL_ADAPTER_OK",out)

