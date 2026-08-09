from pathlib import Path
import inspect, sys
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT))
import spotpy, numpy, scipy, pandas, matplotlib

print("SPOTPY", spotpy.__version__, Path(spotpy.__file__).resolve())
print("DEPENDENCIES", {"numpy":numpy.__version__,"scipy":scipy.__version__,"pandas":pandas.__version__,"matplotlib":matplotlib.__version__})
algorithms=[n for n in ("mc","lhs","fast","sceua","dds","padds","dream","nsgaii","demcz") if hasattr(spotpy.algorithms,n)]
objectives=[n for n in ("nashsutcliffe","kge","rmse","mae","pbias","rsquared") if hasattr(spotpy.objectivefunctions,n)]
print("ALGORITHMS", algorithms); print("OBJECTIVE_FUNCTIONS", objectives)
assert {"mc","lhs","fast","sceua","dds","padds","dream"}.issubset(algorithms)
assert {"nashsutcliffe","kge","rmse","mae","pbias","rsquared"}.issubset(objectives)
print("SPOTPY_SMOKE_TEST_OK")
