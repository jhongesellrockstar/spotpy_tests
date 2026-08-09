# Demostración multiobjetivo NSGA-II

Ejecute `python 11_multiobjective/run_nsga2.py`. SPOTPY 1.6.7 minimiza tres pérdidas separadas: `1-NSE`, `1-KGE` y `|PBIAS|/100`. No se suman ni se afirma que la terna sea científicamente óptima.

Un candidato domina a otro si no es peor en ningún objetivo y es estrictamente mejor en al menos uno. El frente de Pareto contiene candidatos no dominados; desplazarse por él implica trade-offs. La población y generaciones son pequeñas: prueba el contrato multiobjetivo, no estabiliza un frente científico. PA-DDS existe pero el propio paquete lo marca beta, por lo que no se ejecuta como solución de producción.

