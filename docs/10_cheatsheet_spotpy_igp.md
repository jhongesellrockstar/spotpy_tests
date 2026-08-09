# SPOTPY IGP — hoja rápida

**SPOTPY:** framework Python independiente del modelo para muestreo, optimización, sensibilidad e incertidumbre de parámetros.

| INPUT | PROCESS | OUTPUT |
|---|---|---|
| parámetros y priors | `parameters()` | parameter sets (`par*`) |
| modelo/forzantes | `simulation()` | simulaciones (`simulation_*`) |
| observaciones | `evaluation()` | referencia alineada |
| métrica/likelihood | `objectivefunction()` | objetivos (`like*`) |
| algoritmo/runs/seed | `sampler.sample()` | CSV/JSON, sensibilidad, calibrados, posterior según método |

```text
datos -> modelo <- parámetros <- SPOTPY
           |                      ^
           v                      |
       simulación -> objetivo ----+
                         ^
                    observación
```

**Probados:** MC, LHS, FAST, SCE-UA, DDS. **Demostraciones nuevas:** firmas, NSGA-II, DREAM sin convergencia, eFAST, RAM/CSV/SQLite. **Pendiente importante:** incertidumbre convergente, multiprocessing/MPI, unidades/datos reales e integración SWAT+ real.

Comando base: `conda activate spotpy-igp` y `python run_experiment.py --example hydrology --algorithm sceua --runs 500`.

