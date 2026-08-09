# Incertidumbre bayesiana didáctica

Ejecute `python 12_uncertainty/run_dream.py`. Los priors son uniformes dentro de los cinco rangos. La función objetivo es `gaussianLikelihoodMeasErrorOut`, una log-likelihood gaussiana de SPOTPY que integra el error de medición; NSE no se usa como likelihood.

DREAM usa siete cadenas (mínimo compatible con `delta=3`), 140 evaluaciones nominales y diagnóstico R-hat. `convergence.json` es la autoridad: el script nunca declara convergencia sólo por terminar. `posterior_top20.csv` es un subconjunto didáctico de mayor likelihood, no una posterior robusta con 30 observaciones y presupuesto pequeño. Burn-in, longitud efectiva, autocorrelación, sensibilidad al prior y modelo de error requieren estudio antes de inferencia científica. DE-MCz está disponible pero queda no probado para evitar duplicar una demostración casi idéntica sin nuevo conocimiento.

