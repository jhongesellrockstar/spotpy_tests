# Métricas hidrológicas y signos

Sea `Oᵢ` observado, `Sᵢ` simulado y `n` el número de instantes.

| Métrica | Ecuación resumida | Rango / ideal | Dirección e interpretación |
|---|---|---|---|
| NSE | `1-Σ(S-O)²/Σ(O-Ō)²` | `(-∞,1]`, ideal 1 | maximizar; 0 equivale a usar la media observada |
| KGE | `1-sqrt((r-1)²+(α-1)²+(β-1)²)` | `(-∞,1]`, ideal 1 | maximizar; combina correlación, variabilidad y sesgo medio |
| RMSE | `sqrt(mean((S-O)²))` | `[0,∞)`, ideal 0 | minimizar; penaliza más errores grandes |
| MAE | `mean(|S-O|)` | `[0,∞)`, ideal 0 | minimizar; error absoluto medio |
| PBIAS | `100 Σ(S-O)/ΣO` | real, ideal 0 | minimizar `|PBIAS|`; positivo significa sobreestimación con esta convención |
| R² | `corr(O,S)²` | `[0,1]`, ideal 1 | maximizar; asociación, no ausencia de sesgo |

`src/common/hydrological_metrics.py` implementa las seis y los tests comparan NSE con SPOTPY. SPOTPY documenta firmas como `(evaluation, simulation)`; nuestro API público usa `(observed, simulated)`.

## Regla operativa de signo

La fuente instalada fija SCE-UA a **minimize** y DDS a **maximize**. Para NSE/KGE, SCE-UA recibe el negativo y DDS recibe el valor natural. Para RMSE, los samplers maximizadores reciben `-RMSE`; al activar SCE-UA se invierte de nuevo, quedando RMSE positivo para minimizar. MC/LHS/FAST no “deciden” el óptimo durante sampling; el analizador selecciona máximo de score natural. Los JSON siempre reportan métricas naturales para evitar interpretar un `like1` con signo interno.

