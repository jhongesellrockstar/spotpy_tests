# Informe del entorno

Fecha de auditoría: 2026-08-09, Windows 11 (workstation ACER).

## Estado inicial

| Comando | Resultado |
|---|---|
| `python --version` | Python 3.14.4 global (`C:\Python314\python.exe`) |
| `where python` | `C:\Python314\python.exe`; alias WindowsApps |
| `conda --version` | No estaba en PATH; ejecutable localizado: `C:\Users\ACER\anaconda3\Scripts\conda.exe`, Conda 26.1.1 |
| `conda env list` | base, TW, corvusai, kanban_pp00089; no existía spotpy-igp |
| `pip --version` | pip 26.0.1 global, Python 3.14 |
| import SPOTPY global | `ModuleNotFoundError` |
| Git | rama `main`, remoto `origin`, árbol inicialmente limpio |

No se modificó `base` ni Python global. PyPI declara SPOTPY 1.6.7 compatible con Python >=3.10; se eligió Python 3.12 por compatibilidad publicada y wheels científicos maduros. La receta conda-forge de SPOTPY intentó incorporar MPI, por lo que se canceló y se instaló el wheel PyPI dentro de un entorno Conda mínimo.

## Entorno utilizado

| Componente | Versión |
|---|---|
| Python | 3.12.13 |
| SPOTPY | 1.6.7 |
| NumPy | 2.5.2 |
| SciPy | 1.18.0 |
| Pandas | 3.0.5 |
| Matplotlib | 3.11.1 |
| pytest | 9.1.1 |
| MPI/mpi4py | no instalado |

Desde Anaconda Prompt:

```bat
cd C:\Users\ACER\Documents\GitHub\spotpy_tests
conda env create -f environment.yml
conda activate spotpy-igp
python 01_smoke_test\run_smoke_test.py
python -m pytest -v
```

Si el entorno ya existe: `conda activate spotpy-igp`. Para recrearlo explícitamente: `conda env remove -n spotpy-igp` y luego `conda env create -f environment.yml` (la eliminación es decisión del usuario, no la ejecuta el laboratorio).

