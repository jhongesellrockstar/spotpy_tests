# Reporte SPOTPY IGP

## 1. Resumen ejecutivo

Se convirtió el repositorio vacío en un laboratorio modular de SPOTPY 1.6.7. Se verificaron MC, LHS, FAST, SCE-UA y DDS mediante ejecuciones reales; se implementaron datos/modelo hidrológico didácticos, métricas, persistencia, gráficos, adaptador externo y prototipo SWAT+ seguro. Los 22 tests pasan. El laboratorio es operativo; la integración SWAT+ real queda deliberadamente no activada hasta recibir/verificar proyecto y formatos.

## 2. Entorno utilizado

Windows 11, Conda `spotpy-igp`, Python 3.12.13. Activación: `conda activate spotpy-igp`. El Python 3.14 global y `base` no se modificaron. `pip check`: “No broken requirements found”. Detalle en `docs/00_environment_report.md`.

## 3. Versión de SPOTPY

SPOTPY 1.6.7 instalado desde wheel PyPI; NumPy 2.5.2, SciPy 1.18.0, Pandas 3.0.5, Matplotlib 3.11.1, pytest 9.1.1. `mpi4py` no está instalado.

## 4. Arquitectura implementada

`src/common` centraliza lector, métricas, modelo, setup y gestor de experimentos. `src/experiments.py` controla sampling/análisis. Directorios `01`–`09` contienen lecciones finas; `run_experiment.py` es el CLI. Configs/datos son externos; `runs/<id>` no sobrescribe ejecuciones. Se prefirió composición simple frente a una jerarquía abstracta.

## 5. Pruebas ejecutadas

Secuencia final 2026-08-09: smoke, Rosenbrock MC, demo MC, FAST (325), SCE-UA (120 solicitadas), DDS (120), adaptador externo y `pytest -v`. Todos devolvieron código 0. `pytest`: 22 passed en 3.89 s; tras la corrección de selección SCE-UA: 22 passed en 3.94 s.

También se ejecutó LHS con 40 muestras (NSE 0.9251) y el CLI con todos los algoritmos. Los comandos exactos están en la sección 18.

## 6. Resultados Rosenbrock

MC, 100 muestras, semilla 42: mínimo 0.188121; `x=0.763751`, `y=0.546941`; distancia al óptimo `(1,1)` = 0.510956. Se generó CSV y `parameter_space.png`. Un presupuesto pequeño explica que no alcance exactamente el óptimo.

## 7. Resultados modelo hidrológico

MC, 50 muestras: NSE 0.908542; KGE 0.898044; RMSE 0.929206; MAE 0.762732; PBIAS +7.299%; R² 0.918510. El CSV de 30 días es demostrativo, no evidencia científica de una cuenca real.

## 8. Análisis FAST

FAST, 325 evaluaciones (`M=4`), produjo:

| Parámetro | S1 | ST | ranking ST |
|---|---:|---:|---:|
| runoff_coeff | 0.48733 | 0.88951 | 1 |
| quick_recession | 0.20883 | 0.39920 | 2 |
| base_recession | 0.01075 | 0.04214 | 3 |
| soil_capacity | 0.00841 | 0.03988 | 4 |
| et_factor | 0.00247 | 0.02907 | 5 |

En este diseño/rangos/NSE, el coeficiente de escorrentía domina. Esto orienta priorización previa a SWAT+, pero no se transfiere directamente a parámetros reales. Archivo: `05_fast_sensitivity/outputs/fast_sensitivity.csv`.

## 9. Calibración SCE-UA

Se solicitaron 120; SPOTPY completó 225 evaluaciones internas, descartó 44 y guardó 88, comportamiento propio de la inicialización/evolución usada. Mejor interno: NSE 0.954195, KGE 0.860940, RMSE 0.657595, PBIAS −8.996%. SCE-UA minimizó `-NSE` (`like=-0.954195`). Se guardaron serie inicial/mejor, parámetros y tres gráficos.

## 10. Calibración DDS

120 evaluaciones guardadas/completadas. Mejor: NSE 0.963318, KGE 0.981289, RMSE 0.588474, PBIAS +0.292%. DDS maximizó NSE natural. Se generaron las mismas evidencias que SCE-UA.

## 11. Comparación de algoritmos

| algorithm | runs/evaluaciones | runtime s* | best NSE | best KGE | RMSE | PBIAS % |
|---|---:|---:|---:|---:|---:|---:|
| SCE-UA | 225 | 0.118 | 0.954195 | 0.860940 | 0.657595 | −8.996 |
| DDS | 120 | 0.162 | 0.963318 | 0.981289 | 0.588474 | +0.292 |

`*` Tiempo del núcleo Python local, demasiado corto para conclusiones de rendimiento. DDS fue mejor en este caso/semilla/presupuesto; no implica superioridad universal. CSV: `07_dds_calibration/outputs/comparison_sceua_dds.csv`.

## 12. Funcionamiento del adaptador externo

El proceso ficticio leyó JSON/CSV, produjo 30 caudales y devolvió código 0 con `FAKE_MODEL_OK`. El runner crea working directory UUID, usa `cwd`, timeout, stdout/stderr, returncode, valida output/NaN y limpia. Tests cubren éxito, fallo y timeout.

## 13. Arquitectura propuesta para SWAT+ IGP

Configuración → copia aislada por worker → escritor de parámetros verificado → `subprocess.run([swatplus.exe], cwd=..., timeout=..., capture_output=True, text=True)` → parser verificado → warm-up → alineamiento temporal/unidades → métrica → SPOTPY. El prototipo no inventa archivos internos ni toca un proyecto real.

## 14. Archivos a modificar para una nueva cuenca

Para la demo: `03_hydrology_demo/data/input.csv` y config/CLI. Para un modelo externo: adapter, parámetros y parser. Para SWAT+: `config/swatplus_example.json`, luego `parameter_definition.py`, `parameter_writer.py` y `output_parser.py` únicamente después de verificar archivos/semántica; preserve el runner genérico.

## 15. Limitaciones encontradas

- Datos y modelo son sintéticos/didácticos; no hay validación temporal independiente.
- FAST depende fuertemente de rangos, métrica y tamaño de muestra.
- SCE-UA excedió el límite nominal y no persistió todos los candidatos internos.
- PA-DDS declara estado beta en la fuente instalada. DREAM se ensayó sólo como diagnóstico didáctico con likelihood explícita; DE-MCz no se ensayó porque exige un diseño probabilístico y presupuesto adicionales.
- Sin MPI/paralelización y sin ejecución SWAT+ real por restricción explícita.
- Tiempos subsegundo no representan el solver Fortran.

## 16. Errores corregidos

1. La receta conda-forge arrastraba MPI: se canceló y se usó wheel PyPI sin MPI.
2. Una descarga Python 3.13 quedó corrupta en caché: se evitó sin tocar `base`, usando Python 3.12 compatible.
3. `parameters()` directo entrega registros estructurados: `simulation()` acepta registro o vector.
4. `Path` no era serializable en config: serialización central `default=str`; se añadió test.
5. El CSV SCE-UA omitía el mejor interno: el análisis usa `sampler.status` y registra por separado mejor interno/mejor persistido.
6. El analizador FAST imprime arrays aun con `print_to_console=False`: se captura en logging para terminal conciso.

## 17. Próximos pasos

Proporcionar una copia controlada de proyecto SWAT+ y documentar versión del ejecutable, parámetros/archivos exactos, salida de caudal, unidades/período/estación. Implementar pruebas de escritura/parser sobre fixtures, una sola corrida manual, baseline reproducible y recién después calibración pequeña. Añadir calibración/validación temporal y presupuestos científicos; evaluar paralelización sólo tras asegurar aislamiento por worker.

## 18. Comandos exactos para reproducir todo

```bat
cd C:\Users\ACER\Documents\GitHub\spotpy_tests
conda activate spotpy-igp
python 01_smoke_test\run_smoke_test.py
python 02_rosenbrock\run_mc.py
python 03_hydrology_demo\run_demo.py
python run_experiment.py --example hydrology --algorithm lhs --runs 40
python 05_fast_sensitivity\run_fast.py
python 06_sceua_calibration\run_calibration.py
python 07_dds_calibration\run_calibration.py
python 07_dds_calibration\compare_with_sceua.py
python 08_external_model_adapter\run_demo.py
python 09_swatplus_adapter_prototype\run_calibration.py
python -m pytest -v
python -m pip check
```

## Estado y evidencia

**ESTADO GENERAL: OPERATIVO** para el laboratorio; el adaptador SWAT+ real permanece intencionalmente como prototipo hasta recibir insumos verificados.

| Componente | Estado | Evidencia | Archivo/resultado |
|---|---|---|---|
| Entorno/import | Operativo | smoke código 0 | `docs/00_environment_report.md` |
| MC/LHS | Operativo | ejecuciones reales | `runs/` y outputs demo |
| Rosenbrock | Operativo | mínimo 0.188121 | `02_rosenbrock/outputs/results/` |
| Modelo/CSV | Operativo | NSE 0.908542; validaciones testeadas | `03_hydrology_demo/` |
| FAST | Operativo | S1/ST y gráfico | `05_fast_sensitivity/outputs/fast_sensitivity.csv` |
| SCE-UA | Operativo | NSE 0.954195 | `06_sceua_calibration/outputs/` |
| DDS | Operativo | NSE 0.963318 | `07_dds_calibration/outputs/` |
| Métricas | Operativo | comparación SPOTPY/tests | `src/common/hydrological_metrics.py` |
| Modelo externo | Operativo | éxito/fallo/timeout | `08_external_model_adapter/` |
| SWAT+ | Prototipo seguro | config validada; no ejecutado | `09_swatplus_adapter_prototype/` |
| Tests | Operativo | 22 passed | `tests/` |

## 19. COBERTURA DE SPOTPY 1.6.7

La matriz exhaustiva, con evidencia de API y prioridad para SWAT+, está en `docs/06_auditoria_funcionalidades_spotpy.md`. Resumen:

- **Implementado y probado:** setup SPOTPY; MC, LHS, FAST, eFAST, SCE-UA, DDS, NSGA-II y DREAM; métricas hidrológicas; firmas seleccionadas; backends RAM, CSV y SQL; adaptador de proceso externo secuencial.
- **Implementado parcialmente:** diagnóstico de convergencia DREAM (el ejercicio no convergió), multiobjetivo con presupuesto pequeño, incertidumbre didáctica, prototipo SWAT+ y comparación de backends.
- **Disponible pero no implementado:** MCMC, MLE, SA, ROPE, DE-MCz, ABC, FSCABC, PA-DDS, HDF5, base personalizada y paralelización `mpc`/`umpc`/MPI.
- **No prioritario por ahora:** ampliar el catálogo por cobertura nominal sin pregunta científica, o paralelizar antes de validar aislamiento, reinicio y determinismo del modelo externo.

## 20. Experimentos avanzados ejecutados

| Experimento | Ejecución | Resultado verificable | Interpretación |
|---|---:|---|---|
| Firmas hidrológicas | 30 observaciones | media 4.1473; Q5 9.585; Q50 3.100; Q95 0.6585 | Serie demasiado corta para firmas anuales o recesión robusta. |
| NSGA-II | 48 evaluaciones | 8 soluciones no dominadas | Frontera didáctica para `1-NSE`, `1-KGE` y `abs(PBIAS)/100`; no estable científicamente. |
| DREAM | 140 muestras, 7 cadenas | R-hat final 2.07–4.47; `converged=false` | Demuestra el flujo y evita afirmar convergencia inexistente. |
| eFAST | 71 evaluaciones | fracción parcial mayor: `runoff_coeff` 0.3138 | Presupuesto mínimo; sirve como verificación, no como análisis definitivo. |
| Backends | 20 registros por backend | RAM, CSV y SQL coherentes | SQL fue más lento en esta microprueba; no es benchmark del solver. |

## 21. Input → proceso → output

`docs/07_input_process_output.md` documenta cada experimento 01–14, sus parámetros, unidades justificables, funciones objetivo, archivos de salida y columnas reales de SPOTPY (`like*`, `par*`, `simulation_*`, `chain`). La unidad de `q_obs` permanece explícitamente desconocida; no se inventó m³/s.

## 22. Paralelización

`docs/08_parallelization_strategy.md` compara `seq`, `mpc`, `umpc` y MPI. El entorno actual sólo valida secuencial: faltan `pathos` y `mpi4py`. Para SWAT+ se requiere una copia independiente del proyecto por worker, rutas locales y recolección central; no se activó paralelismo sin esas garantías.

## 23. Manual, reunión y material operativo

- Manual fuente: `latex/main.tex`, 14 capítulos, bibliografía DOI y figuras vectoriales.
- PDF compilado: `latex/SPOTPY_IGP_Manual.pdf` (23 páginas).
- Registro de compilación: `latex/build.log`.
- Resumen de tres minutos: `docs/09_resumen_para_reunion.md`.
- Hoja rápida: `docs/10_cheatsheet_spotpy_igp.md`.

## 24. Validación final de la ampliación

El PDF se compiló con XeLaTeX/BibTeX, se renderizó a imágenes para inspección página por página y se verificaron índice, figuras, tablas y bibliografía. La suite conserva sus 22 pruebas; los cinco scripts avanzados concluyeron con código 0. DREAM no alcanzó convergencia y se reporta como tal. No se creó commit ni se hizo push.
