# Firmas hidrológicas

Ejecute `python 10_hydrological_signatures/run_signatures.py`. Se calculan media, cuantiles de excedencia Q5/Q50/Q95, coeficiente de variación, razón media/mediana, autocorrelación de un día y frecuencia de ceros sobre `q_obs`.

La entrada tiene 30 pasos diarios y la unidad de caudal no está definida en el laboratorio. Por eso no se calculan ni interpretan como robustas firmas anualizadas, extremos por año, recesión o baseflow. Los cuantiles y la media conservan la unidad desconocida; razones/autocorrelación son adimensionales y frecuencia de ceros es porcentaje de pasos.

