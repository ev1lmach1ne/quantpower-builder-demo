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

# Serie de 6 publicaciones sueltas

Las mismas ideas como publicaciones independientes, en la carpeta `sueltas/`:
`post-N-tiktok.png` (9:16) y `post-N-vertical.png` (4:5). MAE y MFE van juntas
en la publicación 3. Cada imagen lleva el enlace al artículo y, en las de
datos, el contexto del ejemplo.

Ritmo sugerido: una cada 1 o 2 días, en orden, cuando el artículo ya esté
publicado. En TikTok usa solo la descripción de una línea (más líneas abren un
panel negro y desplazan la imagen) y pon el resto en un comentario fijado.

## 1/6 · Tu backtest cuenta una sola historia

**Descripción:** 👀 Tu backtest cuenta una sola historia · Serie 1/6 #backtesting

**Comentario fijado:**
Un backtest es solo una de las muchas historias posibles. En esta serie, 3 técnicas para saber si la tuya es real, todas disponibles en QuantPower Builder. 👉 quantpowerbuilder.com/articulos
#QuantPowerBuilder #backtesting #trading #quant

## 2/6 · El ejemplo

**Descripción:** 📊 +128 % frente a +5 %: ¿suerte o ventaja? · Serie 2/6 #backtesting

**Comentario fijado:**
Sistema de tendencia: ruptura de 60 velas, filtro de media de 200 y stop de seguimiento, 153 operaciones en 8 años. Así se construye y se prueba un sistema en QuantPower Builder. Ejemplo didáctico con datos sintéticos. 👉 quantpowerbuilder.com
#QuantPowerBuilder #backtesting #tradingalgoritmico #trading

## 3/6 · MAE y MFE

**Descripción:** 🔍 Lo que pasa dentro de cada operación: MAE y MFE · Serie 3/6 #trading

**Comentario fijado:**
MAE = lo máximo que una operación va en contra antes de cerrarse. MFE = lo máximo que llega a ir a favor. En QuantPower Builder los ves en cada operación: la MAE te dice dónde poner el stop y la MFE cuánto beneficio devuelve tu salida. 👉 quantpowerbuilder.com
#QuantPowerBuilder #MAE #MFE #gestiondelriesgo #backtesting

## 4/6 · Walk-forward

**Descripción:** 🔁 Optimiza con el pasado, comprueba con el futuro · Serie 4/6 #quant

**Comentario fijado:**
Optimiza con 2 años, comprueba en los 6 meses siguientes y repite. QuantPower Builder separa la optimización in-sample de la evaluación out-of-sample y walk-forward. 👉 quantpowerbuilder.com
#QuantPowerBuilder #walkforward #backtesting #quant #tradingalgoritmico

## 5/6 · Montecarlo

**Descripción:** 🎲 La caída de tu backtest no es la peor · Serie 5/6 #trading

**Comentario fijado:**
10.000 simulaciones con las mismas operaciones para ver la caída que de verdad puedes sufrir. El Montecarlo de QuantPower Builder te da el abanico completo de resultados. 👉 quantpowerbuilder.com
#QuantPowerBuilder #montecarlo #gestiondelriesgo #trading #backtesting

## 6/6 · El orden importa

**Descripción:** ✅ El orden importa · Serie 6/6, artículo en el perfil #backtesting

**Comentario fijado:**
Hipótesis → backtest → MAE/MFE → walk-forward → Montecarlo. Todo el flujo, en una sola plataforma: QuantPower Builder. Artículo completo 👉 quantpowerbuilder.com/articulos
#QuantPowerBuilder #backtesting #tradingalgoritmico #quant #trading

---

## Carrusel completo (8 imágenes en una publicación)

**Descripción:** 👀 3 técnicas para saber si tu backtest es real · enlace en el perfil #backtesting
