# Post 04 · Carrusel divulgativo: MAE/MFE, walk-forward y Montecarlo

Basado en el artículo «Más allá del backtest - MAE, MFE, walk-forward y
Montecarlo en la práctica».

Imágenes (8 diapositivas, súbelas en orden):

- `vertical-1.png` … `vertical-8.png` → carrusel de Instagram, LinkedIn y Facebook (4:5).
- `historia-1.png` … `historia-8.png` → TikTok (modo foto) e historias (9:16).
  Dejan libres las zonas que tapa la interfaz de la app.

Enlace: <https://quantpowerbuilder.com/articulos/>

> **Publica primero el artículo.** La última diapositiva y los textos remiten a
> él; si aún no está en la web, el enlace no lo mostrará.

---

## Instagram (carrusel)

Tu backtest cuenta una sola historia. ¿Cómo sabes si es verdad? 🔍

Tres técnicas para comprobarlo antes de arriesgar dinero, con un ejemplo calculado paso a paso:

📌 MAE y MFE: cuánto va en contra cada operación antes de ganar y cuánto beneficio devuelve.
📌 Walk-forward: optimizar con el pasado y comprobar con datos que el sistema no vio.
📌 Montecarlo: 10.000 secuencias para ver que la peor caída del backtest no es la peor posible.

El ejemplo gana un +128 % en 8 años con una caída máxima del −11,9 %. Aun así, el Montecarlo dice que conviene prepararse para un −19 %.

💾 Guárdalo para tu próximo backtest.
👉 Artículo completo: enlace en la bio.

Ejemplo didáctico con datos sintéticos. No es una recomendación de inversión.

#backtesting #tradingalgoritmico #trading #quant #montecarlo #walkforward #gestiondelriesgo #QuantPowerBuilder

---

## TikTok (modo foto)

Tu backtest cuenta una sola historia 👀 Estas 3 técnicas te dicen si es verdad: MAE/MFE, walk-forward y Montecarlo.

El ejemplo: +128 % en 8 años con una caída del −11,9 %… y aun así la peor caída posible es mayor de lo que parece 📉

Artículo completo en quantpowerbuilder.com/articulos (enlace en el perfil).
Ejemplo didáctico con datos sintéticos.

#backtesting #trading #tradingalgoritmico #quant #aprendeentiktok #QuantPowerBuilder

---

## LinkedIn (documento o carrusel de imágenes)

Un backtest bonito no demuestra nada. Solo cuenta una de las muchas historias que podrían haber pasado.

He preparado un resumen visual de tres técnicas que uso para separar una ventaja real de una casualidad:

1. MAE y MFE: lo que pasa dentro de cada operación. En el ejemplo, las ganadoras apenas retroceden, lo que apunta a un stop más ajustado. Pero ajustar el stop de seguimiento a 3 ATR costaría casi un tercio de la rentabilidad.
2. Walk-forward: optimizar con dos años y comprobar con los seis meses siguientes, doce veces seguidas. Fuera de muestra, el sistema mantiene el 82 % de su rendimiento.
3. Montecarlo: 10.000 secuencias de las mismas operaciones. La caída máxima del backtest fue del −11,9 %; en el peor 5 % de los casos llega al −19,2 %. Ese es el número con el que dimensionar el riesgo.

El artículo completo, con todas las tablas y gráficos:
https://quantpowerbuilder.com/articulos/

Ejemplo didáctico con datos sintéticos; no es una recomendación de inversión.

#Backtesting #TradingAlgoritmico #AnalisisCuantitativo #GestionDelRiesgo

> En LinkedIn, el formato que más alcance suele dar es el «documento»: une
> `vertical-1.png` … `vertical-8.png` en un PDF y súbelo como documento.

---

## Texto alternativo por diapositiva

1. Portada: «Tu backtest cuenta una sola historia» y las tres técnicas: MAE y MFE, walk-forward y Montecarlo.
2. El ejemplo: un sistema de tendencia gana un 128 % en 8 años con una caída máxima del 11,9 %, frente al 5 % y una caída del 62,9 % de comprar y mantener.
3. MAE: gráfico de dispersión del retroceso máximo frente al resultado de cada operación; 9 de cada 10 ganadoras no retroceden más de 0,86 R.
4. MFE: gráfico del avance máximo frente al resultado; las ganadoras capturan menos de la mitad de su recorrido.
5. Walk-forward: doce ventanas de optimización y comprobación; fuera de muestra gana un 82,6 % en 6 años, con 10 de 12 ventanas en positivo.
6. Montecarlo: 50 curvas simuladas alrededor del backtest; la caída en el peor 5 % llega al 19,2 % y solo el 0,3 % de las simulaciones pierde dinero.
7. El orden de trabajo en cinco pasos: hipótesis, backtest realista, MAE y MFE, walk-forward y Montecarlo.
8. Invitación a leer el artículo completo en quantpowerbuilder.com/articulos.
