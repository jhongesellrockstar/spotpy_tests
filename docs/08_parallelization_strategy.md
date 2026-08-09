# Estrategia de paralelización

SPOTPY 1.6.7 selecciona `parallel="seq"`, `"mpc"`, `"umpc"` o `"mpi"`. El laboratorio sólo ha probado `seq`. `mpc/umpc` importan `pathos`; esa dependencia no está instalada. MPI requiere `mpi4py`, deliberadamente ausente.

| Modo | Orden | Dependencia actual | Estado | Uso recomendado |
|---|---|---|---|---|
| `seq` | determinista | ninguna adicional | probado | desarrollo, depuración, baseline |
| `mpc` | preserva orden | pathos/multiprocess | no disponible | workstation, después de probar aislamiento |
| `umpc` | por finalización | pathos/multiprocess | no disponible | modelos con tiempos variables; cuidado con orden |
| `mpi` | distribuido | mpi4py + runtime MPI | no disponible | clúster, etapa posterior |

```text
SPOTPY coordinator
  +-- worker 1 -> copia SWAT 1 -> archivos/salida 1
  +-- worker 2 -> copia SWAT 2 -> archivos/salida 2
  +-- worker 3 -> copia SWAT 3 -> archivos/salida 3
```

Nunca compartir el mismo proyecto mutable. Cada worker necesita directorio UUID, parámetros, stdout/stderr, timeout y cleanup/preservación independientes. La base de resultados debe escribirse de manera compatible con concurrencia; CSV compartido no debe ser manipulado por el ejecutable. Primero medir una corrida SWAT+ secuencial, luego 2 workers y comprobar igualdad contra baseline, después escalar considerando CPU, RAM, disco y licencias. Preprocesamiento fijo y observaciones se comparten como sólo lectura; escritura de parámetros, solver y outputs son por worker; análisis agregado ocurre después.

