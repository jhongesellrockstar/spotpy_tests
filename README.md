# SPOTPY Laboratory for SWAT+ IGP

Laboratorio reproducible, didáctico y modular para evaluar SPOTPY 1.6.7 como capa de experimentación científica alrededor de modelos hidrológicos y, posteriormente, SWAT+ IGP (PP00089). No ejecuta ni modifica un proyecto SWAT+ real.

## Inicio rápido (Anaconda Prompt)

```bat
cd C:\Users\ACER\Documents\GitHub\spotpy_tests
conda env create -f environment.yml
conda activate spotpy-igp
python 01_smoke_test\run_smoke_test.py
python -m pytest -v
```

Las versiones exactas están en `environment.yml` y `requirements.txt`. MPI no es necesario. Consulte `docs/00_environment_report.md` si `conda` no está en PATH de PowerShell.

## Ruta de aprendizaje

### Nivel 1 — Instalación y smoke test

- **QUÉ APRENDO:** entorno, módulos, algoritmos y métricas disponibles.
- **QUÉ EJECUTO:** `python 01_smoke_test/run_smoke_test.py`.
- **INPUT:** entorno Python.
- **OUTPUT:** inventario y `SPOTPY_SMOKE_TEST_OK`.
- **PUEDO MODIFICAR:** `environment.yml`, sólo para una recreación consciente.
- **SIGNIFICADO:** confirma disponibilidad, no calidad de calibración.

### Nivel 2 — Rosenbrock

- **QUÉ APRENDO:** setup, parámetros, sampling y minimización.
- **QUÉ EJECUTO:** `python 02_rosenbrock/run_mc.py` o `run_sceua.py`.
- **INPUT:** rangos de `x,y`.
- **OUTPUT:** CSV, mejor punto, distancia a `(1,1)` y gráfico.
- **PUEDO MODIFICAR:** `02_rosenbrock/config.py`.
- **SIGNIFICADO:** menor Rosenbrock/distancia implica mejor aproximación.

### Nivel 3 — Modelo hidrológico

- **QUÉ APRENDO:** separar forcing, modelo, observación, setup y análisis.
- **QUÉ EJECUTO:** `python 03_hydrology_demo/run_demo.py`.
- **INPUT:** `03_hydrology_demo/data/input.csv`.
- **OUTPUT:** mejor serie, métricas, parámetros y figuras.
- **PUEDO MODIFICAR:** reemplazar sólo el CSV conservando esquema.
- **SIGNIFICADO:** prueba integración, no representa una cuenca peruana real.

### Nivel 4 — Funciones objetivo

- **QUÉ APRENDO:** NSE, KGE, RMSE, MAE, PBIAS, R² y signos.
- **QUÉ EJECUTO:** `python run_experiment.py --example hydrology --algorithm lhs --runs 100 --objective kge`.
- **INPUT:** objetivo CLI y datos.
- **OUTPUT:** `metrics.json` con métricas naturales.
- **PUEDO MODIFICAR:** `--objective`; implementación en `src/common/hydrological_metrics.py`.
- **SIGNIFICADO:** consulte `docs/02_metricas_hidrologicas.md`; no compare escalas ciegamente.

### Nivel 5 — Sensibilidad FAST

- **QUÉ APRENDO:** índices espectrales de primer orden y total.
- **QUÉ EJECUTO:** `python 05_fast_sensitivity/run_fast.py` (325 mínimo del ejemplo).
- **INPUT:** cinco rangos y NSE.
- **OUTPUT:** `outputs/fast_sensitivity.csv` y gráfico.
- **PUEDO MODIFICAR:** rangos del modelo/configuración.
- **SIGNIFICADO:** ST alto prioriza influencia; no identifica automáticamente el mejor valor.

### Nivel 6 — Calibración SCE-UA

- **QUÉ APRENDO:** complejos, búsqueda global y convención de minimización.
- **QUÉ EJECUTO:** `python 06_sceua_calibration/run_calibration.py`.
- **INPUT:** CSV, rangos y `-NSE` interno.
- **OUTPUT:** hidrograma, trazas, parámetros y métricas.
- **PUEDO MODIFICAR:** runs/objetivo mediante CLI o wrapper.
- **SIGNIFICADO:** mejor ajuste del ejemplo, no validación independiente.

### Nivel 7 — Calibración DDS

- **QUÉ APRENDO:** búsqueda que reduce dinámicamente dimensiones.
- **QUÉ EJECUTO:** `python 07_dds_calibration/run_calibration.py`.
- **INPUT/OUTPUT:** mismos del nivel anterior; DDS maximiza NSE directamente.
- **PUEDO MODIFICAR:** runs, semilla, objetivo.
- **SIGNIFICADO:** compare tiempo/calidad sólo para este caso y presupuesto.

### Nivel 8 — Modelo externo

- **QUÉ APRENDO:** archivos, `subprocess`, cwd, retorno, stdout/stderr, timeout y cleanup.
- **QUÉ EJECUTO:** `python 08_external_model_adapter/run_demo.py`.
- **INPUT:** parámetros JSON y forcing CSV.
- **OUTPUT:** `output.csv` validado.
- **PUEDO MODIFICAR:** adaptador y modelo ficticio.
- **SIGNIFICADO:** demuestra el puente técnico, no SWAT+.

### Nivel 9 — Arquitectura SWAT+ IGP

- **QUÉ APRENDO:** responsabilidades y aislamiento por worker.
- **QUÉ EJECUTO:** `python 09_swatplus_adapter_prototype/run_calibration.py`.
- **INPUT:** `config/swatplus_example.json`, deliberadamente no configurado.
- **OUTPUT:** validación segura del prototipo; ninguna simulación real.
- **PUEDO MODIFICAR:** config y módulos después de verificar un proyecto real.
- **SIGNIFICADO:** arquitectura preparada, no integración científica terminada.

## Arquitectura

`src/common` contiene lector, modelo, métricas, setup y gestor de experimentos. Los directorios numerados son lecciones/scripts cortos. `run_experiment.py` es el acceso unificado. `runs/` conserva ejecuciones sin sobrescritura; sólo `.gitkeep` se versiona. `tests/` valida contratos y fallos.

Documentación: conceptos (`docs/01_spotpy_conceptos.md`), métricas (`docs/02_metricas_hidrologicas.md`), responsabilidad climática (`docs/03_spotpy_y_datos_climaticos.md`), matriz SWAT+ (`docs/04_spotpy_para_swatplus_igp.md`) y comandos (`docs/05_execution_guide.md`). La ampliación incluye auditoría funcional (`docs/06_auditoria_funcionalidades_spotpy.md`), matriz input–proceso–output (`docs/07_input_process_output.md`), estrategia paralela (`docs/08_parallelization_strategy.md`), resumen para reunión (`docs/09_resumen_para_reunion.md`), hoja rápida (`docs/10_cheatsheet_spotpy_igp.md`) y el manual compilado (`latex/SPOTPY_IGP_Manual.pdf`).

Los niveles 10–14 añaden firmas hidrológicas, NSGA-II multiobjetivo, DREAM con diagnóstico de convergencia, eFAST y comparación RAM/CSV/SQL. Son ejercicios avanzados ejecutados con presupuestos didácticos; sus README locales explican entradas, salidas y límites.

## Límites científicos

Los datos son pequeños y demostrativos. Antes de inferencias reales se requieren control de calidad, warm-up, división calibración/validación, unidades, incertidumbre observacional, presupuestos suficientes, diagnóstico de convergencia y análisis multiobjetivo cuando proceda.
