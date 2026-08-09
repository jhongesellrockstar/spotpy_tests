# Auditoría de funcionalidades SPOTPY 1.6.7

Baseline: Python 3.12.13, SPOTPY 1.6.7, 22 tests aprobados y Git limpio antes de esta etapa. “Disponible” fue verificado contra el paquete instalado; “probada” exige ejecución en este repositorio.

| Funcionalidad | Disponible | Estado en este repo | Evidencia | Prioridad SWAT+ IGP |
|---|---|---|---|---|
| MC | Sí | PROBADA | `02_rosenbrock`, demo hidrológica | Media: baseline/exploración |
| LHS | Sí | PROBADA | ejecución CLI registrada | Alta: diseño inicial eficiente |
| FAST | Sí | PROBADA | 325 evaluaciones, S1/ST | Alta: priorizar parámetros |
| eFAST | Sí | PROBADA (didáctica) | `13_efast_sensitivity`, 71 corridas | Media: sensibilidad extendida |
| SCE-UA | Sí | PROBADA | NSE 0.954195 | Alta: calibración global |
| DDS | Sí | PROBADA | NSE 0.963318 | Alta: solver costoso |
| MCMC | Sí | NO PROBADA | clase presente | Media, exige likelihood/diagnóstico |
| MLE | Sí | NO PROBADA | clase presente | Media |
| SA | Sí | NO PROBADA | clase presente | Baja frente a métodos ya probados |
| ROPE | Sí | NO PROBADA | clase presente | Baja/media |
| DE-MCz | Sí (`demcz`) | NO PROBADA | clase presente | Media para incertidumbre |
| DREAM | Sí | DEMOSTRADA PARCIALMENTE | 140 registros, R-hat > 1.2 | Alta, pero requiere serie/modelo de error reales |
| ABC | Sí | NO PROBADA | clase presente | Baja actualmente |
| FSCABC | Sí | NO PROBADA | clase presente | Baja actualmente |
| PA-DDS | Sí | NO PROBADA | fuente instalada advierte beta | Media experimental, no producción |
| NSGA-II | Sí (`NSGAII`) | DEMOSTRADA PARCIALMENTE | 48 evaluaciones, 8 no dominados | Alta para objetivos múltiples |
| Funciones objetivo | Sí | PROBADA parcialmente | NSE/KGE/RMSE/MAE/PBIAS/R² | Alta |
| Likelihoods | Sí | DEMOSTRADA PARCIALMENTE | likelihood gaussiana integrada en DREAM | Alta para incertidumbre formal |
| Firmas hidrológicas | Sí | DEMOSTRADA PARCIALMENTE | 8 firmas compatibles con 30 días | Media; necesita series largas/unidades |
| Análisis posterior | Sí | DEMOSTRADA PARCIALMENTE | top 20% por likelihood | Media; no posterior robusta |
| Gelman-Rubin | Sí | DEMOSTRADA PARCIALMENTE | R-hat final 2.07–4.47; no convergió | Alta para DREAM/DE-MCz |
| Geweke | Sí (plot/análisis interno) | NO PROBADA | función presente | Media, diagnóstico complementario |
| Multiobjetivo | Sí | DEMOSTRADA PARCIALMENTE | NSGA-II y frente CSV/PNG | Alta |
| CSV | Sí | PROBADA | `results.csv`, backend demo | Alta, auditable |
| RAM | Sí | PROBADA | 20 registros | Media, pruebas rápidas |
| SQL (SQLite) | Sí | PROBADA | 20 registros; workaround Windows documentado | Media |
| HDF5 | API presente | NO APLICABLE TODAVÍA | PyTables/HDF5 ausente | Baja; sólo grandes volúmenes |
| Custom database | Interfaz presente | NO PROBADA | requiere implementación del usuario | Baja |
| Secuencial (`seq`) | Sí | PROBADA | todos los experimentos | Alta/baseline |
| Multiprocessing (`mpc`,`umpc`) | Sí en API | NO APLICABLE TODAVÍA | `pathos`/`multiprocess` ausentes | Alta futura, tras aislamiento SWAT+ |
| MPI | Sí en API | NO APLICABLE TODAVÍA | `mpi4py` ausente por diseño | Media futura/clúster |

Conclusión: el siguiente salto útil no es probar algoritmos por inventario. Es formalizar unidades/datos SWAT+, un modelo de error para likelihood, calibración/validación temporal y aislamiento por worker.

