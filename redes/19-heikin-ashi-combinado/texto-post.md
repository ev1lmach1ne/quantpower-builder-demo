# Post 19 · Heikin Ashi + EMA 50 + RSI 14: tres confirmaciones, una entrada (2 diapositivas)

Imágenes (`n` = 1 y 2):

- `tiktok-n.png` → TikTok e historias (9:16).
- `vertical-n.png` → Instagram, Facebook y LinkedIn (4:5).

Ejemplo con datos simulados (`scripts/graficos.py`; las velas donde se cumple cada condición se calculan y quedan en
`graficos/info.json`). La EMA y el RSI ya están en el constructor; Heikin Ashi como confirmación llega en la v0.8.1.

## TikTok

**Descripción (una línea):**

🧩 Heikin Ashi + EMA 50 + RSI: tres confirmaciones, una entrada #QuantPowerBuilder

**Comentario fijado:**

Ejemplo de largo en QuantPower Builder con tres confirmaciones en modo «Todas · AND»: Heikin Ashi cambia a verde y suma 3 velas seguidas, el RSI 14 cruza y se mantiene por encima de 50, y el cierre supera la EMA 50. Cada una se cumple en una vela distinta: la entrada espera a que estén las tres. La confirmación Heikin Ashi llega en la v0.8.1.
👉 quantpowerbuilder.com
#QuantPowerBuilder #heikinashi #rsi #tradingalgoritmico #backtesting

## Instagram, Facebook y LinkedIn

🧩 Tres confirmaciones, una entrada.

Ejemplo de largo combinando Heikin Ashi con dos indicadores, cada uno con su confirmación técnica:

1️⃣ Heikin Ashi: cambia a verde y suma 3 velas seguidas → el giro ya está en marcha.
2️⃣ RSI 14: cruza y se mantiene por encima de 50 → el impulso acompaña.
3️⃣ EMA 50: el cierre la supera → ya no compras contra la tendencia.

Cada condición se cumple en una vela distinta. Con «Todas · AND», la entrada llega solo cuando coinciden las tres.

Más confirmaciones dan menos entradas y algo más tardías, pero más filtradas: pruébalo con el backtest antes de decidir cuántas exigir.

La EMA y el RSI ya están en el constructor de QuantPower Builder; Heikin Ashi como confirmación llega en la v0.8.1.

👉 quantpowerbuilder.com

#QuantPowerBuilder #heikinashi #rsi #mediasmoviles #tradingalgoritmico #backtesting #trading
