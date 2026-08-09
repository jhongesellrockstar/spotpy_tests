# Guía de ejecución

Desde Anaconda Prompt, active `spotpy-igp` y sitúese en la raíz. Ejemplos:

```bat
python 01_smoke_test\run_smoke_test.py
python run_experiment.py --example rosenbrock --algorithm mc --runs 100
python 03_hydrology_demo\run_demo.py
python run_experiment.py --example hydrology --algorithm lhs --runs 100
python run_experiment.py --example hydrology --algorithm fast --runs 325
python run_experiment.py --example hydrology --algorithm sceua --runs 500
python run_experiment.py --example hydrology --algorithm dds --runs 500
python 08_external_model_adapter\run_demo.py
python 09_swatplus_adapter_prototype\run_calibration.py
python -m pytest -v
```

Cada CLI crea `runs/<timestamp_microseconds>_<algorithm>_<objective>/` con config, entorno, log, base SPOTPY, métricas, parámetros, mejor serie y figuras. Para una nueva cuenca, copie el config de ejemplo y reemplace el CSV manteniendo esquema; para SWAT+ primero implemente y pruebe `parameter_writer`/`output_parser` contra una copia controlada.

