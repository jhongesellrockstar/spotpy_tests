# eFAST

Ejecute `python 13_efast_sensitivity/run_efast.py`. SPOTPY 1.6.7 exige 71 corridas para cinco parámetros con frecuencias Cukier. La implementación devuelve fracciones de varianza parcial del NSE.

FAST ya probado usa un diseño por parámetro y entrega S1/ST; eFAST usa un conjunto de frecuencias extendido y este analizador entrega contribuciones parciales, no la misma tabla S1/ST. Con el mínimo exacto sólo se demuestra operatividad: no se establece una comparación científica de estabilidad.

