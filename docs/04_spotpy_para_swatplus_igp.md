# Utilidad de SPOTPY para SWAT+ IGP

| Necesidad | SPOTPY 1.6.7 comprobado | Aplicación futura |
|---|---|---|
| Exploración | MC/LHS | cobertura inicial del espacio |
| Sensibilidad global | FAST | priorizar parámetros influyentes |
| Calibración global | SCE-UA | buscar ajustes por complejos |
| Calibración parsimoniosa | DDS | reducir dimensiones perturbadas durante la búsqueda |
| Multiobjetivo | PA-DDS/NSGA-II presentes | prototipar varios objetivos; PA-DDS indica estado beta y exige validación |
| Incertidumbre | DREAM/DE-MCz presentes | posterior sólo con likelihood y diagnóstico adecuados |
| Persistencia | CSV/RAM y otras bases | evidencia y análisis por experimento |
| Paralelización | modos soportados por SPOTPY | evaluar después; este laboratorio es secuencial y sin MPI |

## Qué NO hace SPOTPY

No genera DEM, delimita cuencas, procesa SIG, crea HRU, genera por sí solo archivos SWAT+ ni corrige datos climatológicos. Muestrea parámetros, controla ejecuciones mediante el setup, calcula objetivos y permite análisis de sensibilidad/calibración/incertidumbre.

Antes de SWAT+ real deben verificarse nombres/formato de archivos, unidades, variable de caudal, períodos, warm-up y semántica exacta de cada modificación. Nunca compartir un directorio mutable entre workers.

