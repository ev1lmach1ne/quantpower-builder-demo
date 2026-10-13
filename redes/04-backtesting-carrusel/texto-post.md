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

---

# Serie de 7 publicaciones sueltas

Las mismas ideas como publicaciones independientes, en la carpeta `sueltas/`:
`post-N-tiktok.png` (9:16) y `post-N-vertical.png` (4:5). Cada imagen lleva el
enlace al artículo y, en las de datos, el contexto del ejemplo, así que se
entienden solas.

Ritmo sugerido: una cada 1 o 2 días, en este orden, empezando cuando el
artículo ya esté publicado. En TikTok, el enlace va en el perfil.

Hashtags comunes: #backtesting #trading #tradingalgoritmico #quant #QuantPowerBuilder

## 1/7 · Tu backtest cuenta una sola historia

Tu backtest cuenta una sola historia 👀 ¿Cómo sabes si es verdad o pura suerte?

Empiezo una serie con las 3 técnicas que uso para comprobarlo antes de arriesgar dinero: MAE/MFE, walk-forward y Montecarlo.

Serie backtesting 1/7 · Sígueme para no perderte las siguientes.

## 2/7 · El ejemplo

+128 % en 8 años con una caída máxima del −11,9 %. Comprar y mantener el mismo activo: +5 % y una caída del −62,9 % 📊

Un resultado así es justo el que más conviene examinar antes de creérselo. En las próximas publicaciones lo ponemos a prueba.

Serie backtesting 2/7 · Ejemplo didáctico con datos sintéticos.

## 3/7 · MAE

¿Cuánto va en contra una operación antes de ganar? Eso es la MAE 📉

En el ejemplo, la mitad de las ganadoras no retrocede más de 0,32 R. Eso te dice dónde poner el stop… pero el cambio siempre hay que validarlo.

Serie backtesting 3/7 · Artículo completo: enlace en el perfil.

## 4/7 · MFE

¿Cuánto beneficio devuelven tus operaciones? Eso es la MFE 💸

Las ganadoras capturan menos de la mitad de su recorrido. La tentación es ajustar el stop de seguimiento… y a 3 ATR cuesta casi un tercio de la rentabilidad.

Serie backtesting 4/7 · Artículo completo: enlace en el perfil.

## 5/7 · Walk-forward

Optimiza con el pasado, comprueba con el futuro 🔁

Walk-forward: elegir parámetros con 2 años y probarlos en los 6 meses siguientes, 12 veces. Fuera de muestra, el ejemplo gana un +82,6 % en 6 años con 10 de 12 ventanas en positivo.

Serie backtesting 5/7 · Artículo completo: enlace en el perfil.

## 6/7 · Montecarlo

La caída que viste en tu backtest no es la peor 🎲

10.000 simulaciones con las mismas operaciones: el backtest cayó un −11,9 %, pero en el peor 5 % de los casos la caída llega al −19,2 %. Ese es el número con el que hay que calcular el riesgo.

Serie backtesting 6/7 · Artículo completo: enlace en el perfil.

## 7/7 · El orden importa

Cierre de la serie: el orden en que aplicar todo esto ✅

1. Hipótesis y costes antes de mirar resultados
2. Backtest realista
3. MAE y MFE para la gestión
4. Walk-forward para los parámetros
5. Montecarlo para el riesgo

Ninguna técnica convierte un sistema malo en bueno, pero juntas te dicen si el tuyo lo es.

Serie backtesting 7/7 · Artículo completo con tablas y gráficos: enlace en el perfil.

---

## TikTok: descripciones de una línea + comentario fijado

En TikTok, una descripción de más de una línea abre un panel negro bajo la
imagen y la desplaza hacia arriba. Para cada publicación de la serie, usa solo
la línea de descripción y fija como comentario el texto largo de la sección
anterior («Serie de 7 publicaciones sueltas»).

1. 👀 Tu backtest cuenta una sola historia · Serie 1/7 #backtesting
2. 📊 +128 % frente a +5 %: ¿suerte o ventaja? · Serie 2/7 #backtesting
3. 📉 ¿Cuánto va en contra antes de ganar? MAE · Serie 3/7 #trading
4. 💸 ¿Cuánto beneficio devuelves? MFE · Serie 4/7 #trading
5. 🔁 Optimiza con el pasado, comprueba con el futuro · Serie 5/7 #quant
6. 🎲 La caída de tu backtest no es la peor · Serie 6/7 #trading
7. ✅ El orden importa · Serie 7/7, artículo en el perfil #backtesting

Carrusel completo (8 imágenes en una publicación):
👀 3 técnicas para saber si tu backtest es real · enlace en el perfil #backtesting
