# Adaptador de modelo externo

`external_model_runner.py` crea un directorio único, escribe parámetros, ejecuta un proceso con `cwd`, timeout y captura de salida, valida retorno/output y limpia según configuración. Ejecute `run_demo.py`. Este es exactamente el límite de integración que después ocupará `swatplus.exe`.

```text
SPOTPY -> parámetros -> adaptador -> parameters.json -> proceso externo
       <- objetivo <- q_sim       <- output.csv      <- proceso externo
```

