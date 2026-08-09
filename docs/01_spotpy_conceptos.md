# Conceptos y API real de SPOTPY 1.6.7

SPOTPY desacopla un modelo de los métodos que muestrean o optimizan sus parámetros. Un **parámetro calibrable** es una entrada incierta expuesta al algoritmo; su distribución prior expresa qué valores se consideran antes de observar la respuesta, y sus límites inferior/superior acotan el dominio. *Sampling* genera conjuntos; una iteración evalúa uno. `simulation()` ejecuta el modelo, `evaluation()` entrega observaciones y `objectivefunction()` resume su concordancia en una métrica o likelihood.

Una población es un conjunto de candidatos simultáneos; una cadena es una secuencia dependiente típica de MCMC; un complejo es una subpoblación de SCE-UA. Convergencia indica estabilización según el criterio del algoritmo. La posterior combina prior y evidencia (algoritmos bayesianos). Sensibilidad atribuye variación de salida a entradas; incertidumbre cuantifica dispersión; calibración busca parámetros con mejor objetivo.

## Contrato setup

- `parameters()`: retorna `spotpy.parameter.generate(...)` con nombres, distribuciones y límites.
- `simulation(vector)`: recibe el conjunto candidato y devuelve una serie simulada.
- `evaluation()`: devuelve la serie observada con igual longitud/orden.
- `objectivefunction(simulation, evaluation, params=None)`: devuelve un escalar (o vector en flujos multiobjetivo compatibles).

```text
PARAMETROS
    |
    v
SPOTPY ALGORITHM
    |
    v
simulation() -> MODELO -> SERIE SIMULADA --+
                                             |
OBSERVADO -----------------------------------+--> objectivefunction()
                                                   |
                                                   v
                                                METRICA
                                                   |
                                                   v
                                           NUEVA ITERACION
```

## API comprobada

En `spotpy.algorithms` 1.6.7 existen `mc`, `lhs`, `fast`, `sceua`, `dds`, `padds`, `dream`, `demcz`, `nsgaii` y otros. Firmas verificadas: MC/LHS `sample(repetitions)`; FAST `sample(repetitions, M=4)`; SCE-UA `sample(repetitions, ngs=20, kstop=100, pcento=1e-7, peps=1e-7, max_loop_inc=None)`; DDS `sample(repetitions, trials=1, x_initial=...)`; PA-DDS y DREAM tienen opciones propias. PA-DDS se anuncia en el propio código como beta, por lo cual no se usa para una recomendación productiva.

MC y LHS exploran; SCE-UA evoluciona complejos; DDS perturba dinámicamente menos dimensiones; FAST estima sensibilidad espectral; DREAM/DE-MCz muestrean distribuciones posteriores y requieren diagnóstico/concepto probabilístico. SPOTPY ofrece bases `csv`, `ram`, `sql`, `hdf5`, `custom` y `noData` (la disponibilidad de HDF5 requiere su dependencia).

Fuentes verificadas: [documentación oficial](https://spotpy.readthedocs.io/en/latest/), [repositorio oficial](https://github.com/thouska/spotpy), [metadatos PyPI](https://pypi.org/project/spotpy/). También se inspeccionaron las firmas y fuentes del paquete instalado, que son la autoridad para las ejecuciones de este laboratorio.

