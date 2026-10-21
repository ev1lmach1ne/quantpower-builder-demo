# Post 15 · 5 formas de entrar con orden límite (carrusel de 8, v0.8)

Imágenes (`n` de 1 a 8):

- `tiktok-n.png` → TikTok e historias (9:16).
- `vertical-n.png` → Instagram, Facebook y LinkedIn (4:5).

Contenido revisado contra el editor «④ Ejecución de la orden de entrada» del programa: las cinco anclas de
«Orden límite en», «Mientras la orden espera» (Fijo / Actualizado), «Caducidad y cancelación» y «Ajuste sobre el ancla».
Gráficos con datos simulados (`scripts/graficos.py`); la página se monta con `scripts/montar.py`.

## TikTok

**Descripción (una línea):**

🎯 5 formas de entrar con orden límite en QuantPower Builder v0.8 #QuantPowerBuilder

**Comentario fijado:**

Primero se confirma el setup con varias condiciones a la vez (tendencia, divergencia, volatilidad y sesión). Después eliges dónde espera la orden límite: un indicador de tus reglas, un nodo del perfil de volumen (POC, VAH, VAL, HVN o LVN), una distancia en ATR, un nivel de la vela de la señal o un retroceso de Fibonacci del último tramo ZigZag. Nuevo en la v0.8 de QuantPower Builder.
👉 quantpowerbuilder.com
#QuantPowerBuilder #ordeneslimite #volumeprofile #tradingalgoritmico #trading

## Instagram, Facebook y LinkedIn

🎯 No persigas el precio: deja que venga a tu nivel.

En la v0.8 de QuantPower Builder, cuando un setup se confirma puedes elegir entre entrar a mercado o dejar una orden límite esperando. Hay 5 formas de colocarla:

1️⃣ Un indicador de tus reglas: una media, una banda… (fija o actualizada vela a vela).
2️⃣ Un nodo del perfil de volumen: POC, VAH, VAL, HVN o LVN, por bloques de tiempo o ventana móvil.
3️⃣ Una distancia en ATR desde el cierre de la señal (0,5 × ATR por defecto).
4️⃣ Un nivel de la vela de la señal: low/high, 50 % o apertura.
5️⃣ Un retroceso de Fibonacci del último tramo ZigZag (del 23,6 % al 78,6 %).

Y tú decides cuánto espera: caduca tras N velas, se cancela si el precio avanza a favor sin ti y puedes ajustarla ± ATR. Sin slippage y con comisión maker.

👉 quantpowerbuilder.com

#QuantPowerBuilder #ordeneslimite #volumeprofile #fibonacci #tradingalgoritmico #trading
