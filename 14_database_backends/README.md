# Bases de resultados

Ejecute `python 14_database_backends/run_backends.py`. RAM, CSV y SQLite reciben las mismas 20 muestras MC y deben conservar 20 registros.

RAM es rápida y efímera; CSV es transparente/portable, pero ancho cuando guarda series; SQLite es persistente, consultable y forma parte de Python. HDF5 aparece en la API, pero PyTables/HDF5 no está instalado: no se añadió una dependencia pesada sólo para esta prueba. `custom` es una interfaz de extensión, no un backend listo sin implementación del usuario.

En Windows, el writer SQL de SPOTPY reutiliza `dbname` como nombre de tabla. Una ruta absoluta (`C:...`) falla como SQL; el script cambia `cwd` al directorio del experimento y usa `backend_sql` como nombre relativo seguro.
