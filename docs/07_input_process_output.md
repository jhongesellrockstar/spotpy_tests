# Diccionario maestro INPUT / PROCESS / OUTPUT

## Convenciones y deficiencias

El archivo `03_hydrology_demo/data/input.csv` contiene 30 fechas diarias consecutivas. Los sufijos `precip_mm` y `pet_mm` establecen milímetros; el código no define si son acumulados/promedios, aunque por el modelo se usan como valores por paso diario. `q_obs` y `q_sim` se etiquetan como “demo units”: **UNIDAD NO DEFINIDA EN EL LABORATORIO ACTUAL**. No se inventa m³/s.

### Datos hidrológicos de entrada

| Campo | Tipo Python / CSV | Unidad | Obligatorio | Rango/temporalidad | Interpretación y validación |
|---|---|---|---|---|---|
| `date` | `pandas.Timestamp` / ISO `YYYY-MM-DD` | fecha | sí | única, creciente; actual diaria | instante del paso; inválida/duplicada/desordenada → error |
| `precip_mm` | `float` / decimal | mm por paso (semántica exacta no documentada) | sí | >=0; actual diaria | precipitación; no numérico/NaN/negativo → error |
| `pet_mm` | `float` / decimal | mm por paso (semántica exacta no documentada) | sí | >=0; actual diaria | evapotranspiración potencial; no numérico/NaN/negativo → error |
| `q_obs` | `float` / decimal | UNIDAD NO DEFINIDA EN EL LABORATORIO ACTUAL | sí | >=0; actual diaria | caudal observado didáctico; no numérico/NaN/negativo → error |

No se codifica un máximo físico universal: depende de clima, área, unidad y resolución de la futura cuenca. El lector exige las cuatro columnas, archivo existente, tabla no vacía y ausencia total de NaN.

### Parámetros del modelo didáctico

Todos usan `spotpy.parameter.Uniform(min,max)`.

| parameter_name | min | max | distribución | unidad | significado en el código |
|---|---:|---:|---|---|---|
| `runoff_coeff` | 0.05 | 0.85 | Uniform | [-] | fracción de lluvia separada de la infiltración potencial |
| `soil_capacity` | 20 | 250 | Uniform | mm (consistente con almacenamiento/precipitación del código) | capacidad máxima del reservorio de suelo |
| `et_factor` | 0.2 | 1.5 | Uniform | [-] | factor multiplicador de PET |
| `quick_recession` | 0.15 | 0.95 | Uniform | [-], fracción por paso | descarga del reservorio rápido en cada paso |
| `base_recession` | 0.005 | 0.25 | Uniform | [-], fracción por paso | descarga del reservorio base en cada paso |

Son parámetros pedagógicos, no parámetros SWAT+ ni rangos calibrables recomendados para una cuenca real.

## Experimentos 01–09

| Experimento | INPUTS concretos | PROCESAMIENTO | OUTPUTS concretos |
|---|---|---|---|
| 01 Smoke | entorno Python, imports | inspecciona versiones, algoritmos y objetivos | stdout; marcador `SPOTPY_SMOKE_TEST_OK` |
| 02 Rosenbrock | `x[-2,2]`, `y[-1,3]`, `config.py` | MC/SCE-UA; minimiza `(1-x)^2+100(y-x²)^2` | `results.csv`, `metrics.json`, `parameters.csv`, `parameter_space.png`, config/entorno/log |
| 03 Hydrology | `data/input.csv`, cinco rangos, NSE, seed 42 | lector → modelo → setup → MC → análisis | resultado SPOTPY, serie inicial/mejor, métricas, parámetros, trazas/hidrograma |
| 04 Comparison | `config/experiment.json` | ejecuta MC/LHS/SCE-UA/DDS | `comparison.csv` y runs individuales |
| 05 FAST | datos/rangos, 325 evaluaciones, `M=4` | diseño FAST; S1/ST del NSE | `fast_sensitivity.csv`, barra S1/ST, base y provenance |
| 06 SCE-UA | datos/rangos, 120 nominales | minimiza `-NSE`; complejos; 225 internas/88 guardadas en baseline | parámetros/serie/gráficos; NSE 0.954195 |
| 07 DDS | datos/rangos, 120 | maximiza NSE; vecindad dinámica | parámetros/serie/gráficos; NSE 0.963318; comparación SCE-UA/DDS |
| 08 Externo | parameters JSON, input CSV, timeout | working dir UUID → subprocess → validación/cleanup | `output.csv(date,q_sim)`, stdout/stderr internos, errores explícitos |
| 09 SWAT+ prototype | `config/swatplus_example.json` con placeholders | valida config; se niega a ejecutar ruta no verificada | mensaje de prototipo; ninguna salida SWAT+ real |

## Experimentos 10–14

| Experimento | INPUTS | PROCESAMIENTO | OUTPUTS |
|---|---|---|---|
| 10 Firmas | `q_obs`, 30 pasos diarios | 8 firmas compatibles; excluye anualizadas/recesión | `hydrological_signatures.csv`; unidades heredadas o [-]/% |
| 11 NSGA-II | datos, cinco priors, 12 individuos × diseño de 5 generaciones | minimiza tres pérdidas separadas; filtra dominancia | `nsga2_results.csv`, `pareto_front.csv`, `pareto_front.png` |
| 12 DREAM | datos, priors uniformes, likelihood gaussiana, 7 cadenas | DREAM 140; R-hat; top 20% por likelihood | base, R-hat, `convergence.json`, posterior y trazas |
| 13 eFAST | datos/rangos, 71 corridas Cukier | fracción espectral de varianza del NSE | `efast_sensitivity.csv/.png`, base |
| 14 Backends | Rosenbrock, 20 muestras, seed 42 | mismo MC a RAM/CSV/SQLite | `backend_summary.csv`, CSV y DB SQLite; RAM sin archivo |

## Formato de un run hidrológico

| Archivo | Formato/columnas | Unidad | Interpretación |
|---|---|---|---|
| `config.json` | JSON: example, algorithm, repetitions, objective, seed, database, input | mixta | solicitud reproducible |
| `environment.json` | JSON: Python, SPOTPY, plataforma | no aplica | provenance de software |
| `run.log` | texto UTF-8 | no aplica | eventos y errores detallados |
| `results.csv` | `like1`, cinco `par*`, `simulation_0…29`, `chain` | por campo | cada fila es una evaluación guardada |
| `metrics.json` | NSE/KGE/RMSE/MAE/PBIAS/R², objetivos, tiempos/conteos | ver métricas | resumen del mejor interno |
| `parameters.csv` | cinco parámetros | tabla de parámetros | conjunto mejor según orientación real del algoritmo |
| `initial_parameters.csv` | cinco puntos medios | tabla de parámetros | baseline no calibrada |
| `initial_simulation.csv` | `date,q_obs,q_sim_initial` | Q: unidad no definida | comparación inicial |
| `best_simulation.csv` | `date,q_obs,q_sim` | Q: unidad no definida | mejor serie recalculada |
| `figures/*.png` | hidrograma y trazas | ejes según campo | diagnóstico visual |

### Columnas SPOTPY verificadas

- `like1`, `like2`…: objetivos/likelihoods en el orden devuelto. La orientación depende del algoritmo/setup.
- `par<name>`: valor del parámetro; ejemplos reales `parrunoff_coeff`, `parsoil_capacity`.
- `simulation_0`…`simulation_29`: simulación por posición temporal cuando `save_sim=True`; el CSV no conserva fecha, que se recupera del input alineado.
- `chain`: identificador de cadena o subpoblación. En MC observado `1.0`; en NSGA-II identifica individuo; en DREAM identifica cadena. No asumir una semántica única entre algoritmos.

## Métricas como outputs

| Métrica | Unidad | Ideal | Interpretación mínima |
|---|---|---:|---|
| NSE | [-] | 1 | eficiencia relativa a la media observada |
| KGE | [-] | 1 | correlación, variabilidad y sesgo medio |
| RMSE | misma unidad desconocida de Q | 0 | magnitud cuadrática del error |
| MAE | misma unidad desconocida de Q | 0 | error absoluto medio |
| PBIAS | % | 0 | signo positivo = sobreestimación con convención local |
| R² | [-] | 1 | asociación lineal; no garantiza ausencia de sesgo |

## Tabla crítica etapa–entrada–salida

| Etapa | Entrada | Formato | Unidad | Proceso | Salida | Formato | Unidad |
|---|---|---|---|---|---|---|---|
| Datos climáticos | `input.csv: date,precip_mm,pet_mm` | CSV | fecha, mm, mm | validación Pandas | forcing validado | DataFrame | mismas |
| Observación | `q_obs` | CSV float | no definida | validación/alineamiento | evaluación | ndarray | no definida |
| Modelo | forcing + cinco parámetros | arrays/scalars | mixta | balances de reservorios | `q_sim` | ndarray | no definida |
| SPOTPY parameters | rangos Uniform | objetos parameter | mixta | `parameters()` | vector candidato | ParameterSet | mixta |
| Simulation | vector + forcing | Python | mixta | `simulation()` | serie candidata | array | no definida |
| Evaluation | `q_obs` | DataFrame | no definida | `evaluation()` | serie referencia | array | no definida |
| Objective | sim + obs | arrays | no definida | `objectivefunction()` | NSE/KGE/etc. | float/list | [-], %, o Q |
| Sampling | setup + runs + seed | config/CLI | no aplica | `sample()` | evaluaciones | CSV/RAM/SQL | mixta |
| FAST | 325 conjuntos | SPOTPY design | parámetros | Fourier | S1/ST | CSV/PNG | [-] |
| SCE-UA | 120 nominales | sampler | no aplica | complejos/minimiza -NSE | calibrado | CSV/JSON/PNG | mixta |
| DDS | 120 | sampler | no aplica | dimensiones dinámicas/maximiza NSE | calibrado | CSV/JSON/PNG | mixta |
| Modelo externo | JSON + CSV | archivos | mixta | subprocess/timeout/parser | `output.csv` | CSV | no definida |
| Futuro SWAT+ | copia + parámetros verificados | archivos SWAT+ por definir | por definir | `swatplus.exe` | Q simulada | archivo por verificar | objetivo futuro: m³/s |

La última fila es arquitectura, no una integración implementada.

