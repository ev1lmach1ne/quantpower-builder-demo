"""Genera el mercado simulado del vídeo (ES a 1 minuto, datos ficticios) y calcula RSI(14), perfil de volumen,
HVN/LVN y las órdenes límite. Escribe src/mercado.json. Uso: python3 scripts/mercado.py"""
import json, os, random

random.seed(11)
# Tramos (barra final, precio objetivo, ruido, volumen base). El camino está pensado para que haya:
# zona alta (HVN objetivo), caída rápida (LVN), consolidación (HVN), mínimo 1 brusco, mínimo 2 más bajo pero lento
# (divergencia alcista en el RSI), confirmación, impulso, retroceso que llena las órdenes y subida al objetivo.
TRAMOS = [(14, 5308.5, .9, 1400), (20, 5290.0, .5, 900), (32, 5289.5, .6, 1500), (35, 5283.0, .4, 1700),
          (40, 5288.5, .5, 1100), (48, 5288.0, .6, 1400), (55, 5281.75, .35, 800), (57, 5286.75, .3, 1300),
          (63, 5299.0, .5, 1000), (67, 5299.5, .5, 900), (74, 5288.75, .45, 1100), (95, 5311.0, .6, 1200)]
tick = lambda p: round(p * 4) / 4
bars, p, i0 = [], 5309.0, 0
for fin, obj, ruido, vol in TRAMOS:
    n = fin - i0
    for k in range(n):
        o = p
        p = p + (obj - p) / (n - k) + random.gauss(0, ruido * .5)
        c = p
        h = max(o, c) + abs(random.gauss(0, ruido * .6)) + .25
        l = min(o, c) - abs(random.gauss(0, ruido * .6)) - .25
        bars.append(dict(o=tick(o), h=tick(h), l=tick(l), c=tick(c), v=int(vol * random.uniform(.7, 1.3))))
    i0 = fin

# Ajustes puntuales: mínimos exactos de la divergencia y vela de confirmación
L1, L2, CONF = 33, 54, 56
bars[L1]['l'] = 5283.0
bars[L2]['l'] = 5281.75
for j in range(len(bars)):
    if j not in (L1, L2) and 30 <= j <= 58:
        bars[j]['l'] = max(bars[j]['l'], 5283.75 if j < 45 else 5282.25)
    b = bars[j]; b['h'] = max(b['h'], b['o'], b['c']); b['l'] = min(b['l'], b['o'], b['c'])

closes = [b['c'] for b in bars]
def rsi(c, n=14):
    out = [None] * len(c); g = l = 0
    for i in range(1, n + 1):
        d = c[i] - c[i - 1]; g += max(d, 0); l += max(-d, 0)
    g /= n; l /= n; out[n] = 100 - 100 / (1 + g / l if l else 1e9)
    for i in range(n + 1, len(c)):
        d = c[i] - c[i - 1]; g = (g * (n - 1) + max(d, 0)) / n; l = (l * (n - 1) + max(-d, 0)) / n
        out[i] = 100 - 100 / (1 + (g / l if l else 1e9))
    return out
R = rsi(closes)
# Mínimos del RSI cerca de cada mínimo del precio
r1 = min(range(L1 - 2, L1 + 3), key=lambda j: R[j]); r2 = min(range(L2 - 2, L2 + 3), key=lambda j: R[j])

# Perfil de volumen hasta la barra en la que se colocan las órdenes (1 punto por casilla)
ORD = 64
perfil = {}
for b in bars[:ORD + 1]:
    lo, hi = int(b['l']), int(b['h'])
    n = hi - lo + 1
    for pr in range(lo, hi + 1):
        perfil[pr] = perfil.get(pr, 0) + b['v'] / n
precios = sorted(perfil)
suave = {pr: sum(perfil.get(pr + d, 0) * w for d, w in ((-1, .25), (0, .5), (1, .25))) for pr in precios}
hvn = max((pr for pr in precios if 5286 <= pr <= 5290), key=lambda pr: suave[pr])
lvn = min((pr for pr in precios if 5292 <= pr <= 5297), key=lambda pr: suave[pr])
objetivo = max((pr for pr in precios if 5304 <= pr <= 5311), key=lambda pr: suave[pr])
stop = hvn - 4
# El usuario elige uno de los niveles del perfil para esperar la ejecución; en el ejemplo, el HVN
candidatos = [dict(tipo='LVN', precio=lvn + .5), dict(tipo='HVN', precio=hvn + .5)]
ordenes = [dict(tipo='HVN', precio=hvn + .5, contratos=2)]
for o in ordenes:
    o['barra'] = next((j for j in range(ORD + 1, len(bars)) if bars[j]['l'] <= o['precio']), None)
media = sum(o['precio'] * o['contratos'] for o in ordenes) / sum(o['contratos'] for o in ordenes)
barra_obj = next((j for j in range(ORD + 1, len(bars)) if bars[j]['h'] >= objetivo + .5), None)

datos = dict(barras=bars, rsi=[None if x is None else round(x, 2) for x in R],
             min1=dict(barra=L1, precio=bars[L1]['l'], rsiBarra=r1, rsi=round(R[r1], 1)),
             min2=dict(barra=L2, precio=bars[L2]['l'], rsiBarra=r2, rsi=round(R[r2], 1)),
             confirmacion=CONF, barraOrdenes=ORD,
             perfil=[dict(precio=pr, vol=round(perfil[pr])) for pr in precios],
             hvn=hvn + .5, lvn=lvn + .5, objetivo=objetivo + .5, stop=stop, candidatos=candidatos, ordenes=ordenes,
             media=round(media, 2), barraObjetivo=barra_obj)
os.makedirs('src', exist_ok=True)
json.dump(datos, open('src/mercado.json', 'w'))
print('barras', len(bars), '| min1', bars[L1]['l'], 'RSI', round(R[r1], 1), '| min2', bars[L2]['l'], 'RSI', round(R[r2], 1))
print('mínimo global 25-60:', min(b['l'] for b in bars[25:60]), '| conf cierre', bars[CONF]['c'], '> máx', bars[L2]['h'])
print('HVN', hvn + .5, 'LVN', lvn + .5, 'objetivo', objetivo + .5, 'stop', stop, '| precio en ORD', bars[ORD]['c'])
print('llenados', [(o['tipo'], o['precio'], o['barra']) for o in ordenes], 'media', round(media, 2), 'objetivo en barra', barra_obj)
print('mín tras órdenes', min(b['l'] for b in bars[ORD+1:]), '(stop', stop, ')')
