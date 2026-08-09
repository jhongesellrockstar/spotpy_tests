# SPOTPY y datos climáticos

SPOTPY no es una librería principal de limpieza de precipitación/temperatura, SIG, DEM, uso o tipo de suelo. Es la capa experimental alrededor de un modelo.

```text
PREPROCESAMIENTO (Pandas/Xarray/GIS, control de calidad)
        |
        v
INPUTS SWAT+ -> SWAT+ SOLVER -> CAUDAL SIMULADO
                                      |
                                      v
                                   SPOTPY
                    + sensibilidad + calibración
                    + optimización + incertidumbre + evaluación
```

Pandas encaja para CSV, fechas, faltantes y alineamiento; Xarray para cubos NetCDF; herramientas GIS para ráster/vectores y HRU. La responsabilidad de SPOTPY comienza cuando existe un contrato reproducible: parámetros → ejecución → salida simulada → observación alineada → objetivo.

