# Resumen para reunión (lectura aproximada: 3 minutos)

1. **Solicitud.** Evaluar SPOTPY como capa reproducible de sensibilidad, calibración y experimentación alrededor de SWAT+ IGP, PP00089.
2. **Qué es.** SPOTPY genera conjuntos de parámetros, llama un modelo definido por Python y registra simulaciones/objetivos. No preprocesa DEM, HRU ni clima.
3. **Instalación.** Entorno Conda `spotpy-igp`: Python 3.12.13, SPOTPY 1.6.7, stack científico versionado; sin MPI.
4. **Probado.** MC, LHS, FAST, SCE-UA, DDS; ahora firmas, NSGA-II, DREAM didáctico, eFAST y RAM/CSV/SQLite.
5. **Inputs.** Cinco rangos, modelo lluvia–caudal, `date`, `precip_mm`, `pet_mm`, `q_obs`, objetivo y semilla. La unidad de `q_obs` aún no está definida.
6. **Ejecución.** `parameters()` propone; `simulation()` corre; `evaluation()` entrega observado; `objectivefunction()` puntúa; `sample()` repite.
7. **Outputs.** CSV `like*/par*/simulation_*/chain`, JSON de métricas/entorno/config, parámetros, mejor serie, figuras y logs.
8. **Resultados reales.** FAST: 325 evaluaciones. SCE-UA: NSE 0.954195. DDS: NSE 0.963318. Baseline: 22 tests aprobados.
9. **FAST.** Atribuye variación de la métrica a rangos de parámetros; `runoff_coeff` dominó en el modelo didáctico. No busca un óptimo.
10. **Calibración.** SCE-UA evoluciona complejos y en SPOTPY minimiza `-NSE`; DDS maximiza NSE y reduce dimensiones perturbadas. Ninguno es universalmente superior.
11. **SWAT+.** SPOTPY → parámetros → escritor → copia privada del proyecto → `swatplus.exe` → parser → Q simulada → objetivo.
12. **Falta.** Proyecto/ejecutable real, archivos y parámetros verificados, Q en m³/s, warm-up, alineamiento, calibración/validación y concurrencia segura.
13. **Próximo paso.** Una corrida SWAT+ real, única y reproducible sobre copia controlada; validar parser/unidades antes de cualquier campaña.

