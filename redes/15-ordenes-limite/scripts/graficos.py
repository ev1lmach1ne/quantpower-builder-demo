"""Gráficos SVG del carrusel «5 formas de entrar con orden límite» (datos simulados con fines ilustrativos).
Cada gráfico ilustra un ancla real de «Orden límite en» del editor de ejecución de QuantPower Builder.
Uso: python3 scripts/graficos.py  → escribe graficos/*.svg"""
import json, math, os, random

W, H = 920, 470
X0, X1, Y0, Y1 = 20, 900, 20, 450
C = dict(green='#2ecc71', red='#e74c3c', accent='#4fc3f7', amber='#f1c40f', purple='#b38af6', muted='#9aaec7',
         text='#c8d6e5', strong='#e6edf3', grid='#202d44', panel='#141e30', deep='#0d1424')
FONT = 'Inter, Segoe UI, Arial, sans-serif'

def serie(semilla, tramos, p0=100.0):
    """Velas OHLC a partir de tramos (barras, precio objetivo, ruido)."""
    random.seed(semilla); b = []; p = p0
    for n, obj, ruido in tramos:
        for k in range(n):
            o = p; p = p + (obj - p) / (n - k) + random.gauss(0, ruido)
            h = max(o, p) + abs(random.gauss(0, ruido * .7)); l = min(o, p) - abs(random.gauss(0, ruido * .7))
            b.append([o, h, l, p])
    return b

def ema(c, n):
    k = 2 / (n + 1); out = [c[0]]
    for x in c[1:]: out.append(out[-1] + k * (x - out[-1]))
    return out

def atr(b, n=14):
    tr = [b[0][1] - b[0][2]] + [max(x[1], p[3]) - min(x[2], p[3]) for p, x in zip(b, b[1:])]
    out = [tr[0]]
    for t in tr[1:]: out.append(out[-1] + (t - out[-1]) / n)
    return out

class Lienzo:
    def __init__(s, b, lo=None, hi=None, x1=X1):
        s.b = b; s.x1 = x1
        s.lo = lo if lo is not None else min(x[2] for x in b); s.hi = hi if hi is not None else max(x[1] for x in b)
        pad = (s.hi - s.lo) * .08; s.lo -= pad; s.hi += pad
        s.paso = (x1 - X0) / len(b); s.o = []
    def x(s, i): return X0 + s.paso * (i + .5)
    def y(s, p): return Y1 - (p - s.lo) / (s.hi - s.lo) * (Y1 - Y0)
    def velas(s, hasta=None):
        for i, (o, h, l, c) in enumerate(s.b[:hasta]):
            col = C['green'] if c >= o else C['red']
            s.o.append(f'<line x1="{s.x(i):.1f}" x2="{s.x(i):.1f}" y1="{s.y(h):.1f}" y2="{s.y(l):.1f}" stroke="{col}" stroke-width="2"/>')
            t, bt = s.y(max(o, c)), s.y(min(o, c))
            s.o.append(f'<rect x="{s.x(i) - s.paso * .33:.1f}" y="{t:.1f}" width="{s.paso * .66:.1f}" height="{max(bt - t, 2):.1f}" fill="{col}" rx="1.5"/>')
    def linea(s, vals, col, w=3, dash=None, desde=0, op=1):
        pts = ' '.join(f'{s.x(i):.1f},{s.y(v):.1f}' for i, v in enumerate(vals) if i >= desde)
        d = f' stroke-dasharray="{dash}"' if dash else ''
        s.o.append(f'<polyline points="{pts}" fill="none" stroke="{col}" stroke-width="{w}" opacity="{op}"{d}/>')
    def nivel(s, p, col, txt, x_ini=None, dash='10 8', w=3, lado='derecha'):
        xi = x_ini if x_ini is not None else X0
        s.o.append(f'<line x1="{xi:.1f}" x2="{s.x1:.1f}" y1="{s.y(p):.1f}" y2="{s.y(p):.1f}" stroke="{col}" stroke-width="{w}" stroke-dasharray="{dash}"/>')
        if txt:
            ancho = 13.2 * len(txt) + 24
            xr = s.x1 - ancho - 4 if lado == 'derecha' else xi + 6
            s.o.append(f'<rect x="{xr:.1f}" y="{s.y(p) - 20:.1f}" width="{ancho:.1f}" height="40" rx="9" fill="{C["deep"]}" stroke="{col}" stroke-width="2"/>')
            s.o.append(f'<text x="{xr + 12:.1f}" y="{s.y(p) + 8:.1f}" fill="{col}" font-size="22" font-weight="700" font-family="{FONT}">{txt}</text>')
    def marca(s, i, p, col, txt=None, arriba=False):
        s.o.append(f'<circle cx="{s.x(i):.1f}" cy="{s.y(p):.1f}" r="12" fill="none" stroke="{col}" stroke-width="4"/>')
        if txt:
            dy = -26 if arriba else 42
            s.o.append(f'<text x="{s.x(i):.1f}" y="{s.y(p) + dy:.1f}" fill="{col}" font-size="22" font-weight="800" text-anchor="middle" font-family="{FONT}">{txt}</text>')
    def svg(s, extra=''):
        return (f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">'
                f'<rect x="0" y="0" width="{W}" height="{H}" rx="18" fill="{C["panel"]}"/>' + ''.join(s.o) + extra + '</svg>')

def primer_toque(b, nivel_por_barra, desde):
    for i in range(desde, len(b)):
        if b[i][2] <= nivel_por_barra[i]: return i
    return None


def etiqueta(L, x, y, txt, col, ancla='start', tam=22):
    ancho = tam * .6 * len(txt) + 24
    xr = x if ancla == 'start' else x - ancho
    L.o.append(f'<rect x="{xr:.1f}" y="{y - 20:.1f}" width="{ancho:.1f}" height="40" rx="9" fill="{C["deep"]}" stroke="{col}" stroke-width="2"/>')
    L.o.append(f'<text x="{xr + 12:.1f}" y="{y + 8:.1f}" fill="{col}" font-size="{tam}" font-weight="800" font-family="{FONT}">{txt}</text>')

def orden(L, desde, hasta, p, col=None):
    """Tramo de la orden límite esperando (fija) desde la vela de la señal hasta la ejecución."""
    col = col or C['amber']
    L.o.append(f'<line x1="{L.x(desde):.1f}" x2="{L.x(hasta):.1f}" y1="{L.y(p):.1f}" y2="{L.y(p):.1f}" stroke="{col}" stroke-width="4" stroke-dasharray="10 7"/>')

os.makedirs('graficos', exist_ok=True)
info = {}

# 1 · Indicador de tus reglas: tendencia alcista, la orden «Actualizada» sigue a la EMA 20 vela a vela
b = serie(3, [(20, 101, .35), (16, 109, .45), (9, 106.2, .35), (15, 112, .45)])
c = [x[3] for x in b]; e = ema(c, 20)
SEN = 36
j = min(range(SEN + 1, SEN + 12), key=lambda i: b[i][2] - e[i])  # el retroceso llega a la media
b[j][2] = min(b[j][2], e[j] - .05)
L = Lienzo(b); L.velas(); L.linea(e, C['accent'], 4)
f = primer_toque(b, e, SEN + 1)
L.o.append(f'<polyline points="{" ".join(f"{L.x(i):.1f},{L.y(e[i]):.1f}" for i in range(SEN, f + 1))}" fill="none" stroke="{C["amber"]}" stroke-width="5" stroke-dasharray="6 6"/>')  # la orden sigue a la media
L.marca(SEN, b[SEN][1], C['amber'], 'Señal', arriba=True)
L.marca(f, e[f], C['green'], 'Ejecutada')
L.o.append(f'<text x="{L.x(52):.1f}" y="{L.y(e[52]) + 40:.1f}" fill="{C["accent"]}" font-size="22" font-weight="800" text-anchor="middle" font-family="{FONT}">EMA 20</text>')
open('graficos/media.svg', 'w').write(L.svg()); info['media'] = dict(senal=SEN, ejec=f, velas_espera=f - SEN)

# 2 · Perfil de volumen interpretado sobre el último bloque cerrado: POC, VAH, VAL, HVN y LVN
random.seed(5)
b = []; p = 101.0
def tramo_rango(n, centro, ancho, ruido, vol):
    global p
    for _ in range(n):
        o = p; p = p + (centro - p) * .35 + random.gauss(0, ruido); p = max(centro - ancho, min(centro + ancho, p))
        h = max(o, p) + abs(random.gauss(0, ruido * .6)); l = min(o, p) - abs(random.gauss(0, ruido * .6))
        b.append([o, h, l, p, vol])
def tramo_recta(n, obj, ruido, vol):
    global p
    for k in range(n):
        o = p; p = p + (obj - p) / (n - k) + random.gauss(0, ruido * .4)
        h = max(o, p) + abs(random.gauss(0, ruido * .3)); l = min(o, p) - abs(random.gauss(0, ruido * .3))
        b.append([o, h, l, p, vol])
tramo_rango(22, 101.4, 1.1, .4, 1.15)     # montaña inferior (HVN)
tramo_recta(3, 106.0, .4, .6)             # cruce rápido: hueco (LVN)
tramo_rango(22, 106.2, 1.0, .4, 1.25)     # montaña superior (POC)
BLOQUE = len(b)                           # 38 velas = el bloque ya cerrado
tramo_rango(5, 106.6, .7, .35, 1.0)
SEN = len(b) - 1
tramo_recta(4, 103.5, .3, 1.0)            # retroceso hasta el hueco
tramo_recta(9, 108.6, .45, 1.0)
FILAS = 0.5
perfil = {}
for o, h, l, c_, v in b[:BLOQUE]:
    k0, k1 = int(math.floor(l / FILAS)), int(math.floor(h / FILAS))
    for k in range(k0, k1 + 1): perfil[k] = perfil.get(k, 0) + v / (k1 - k0 + 1)
ks = sorted(perfil); tot = sum(perfil.values())
suav = {k: sum(perfil.get(k + d, 0) for d in (-1, 0, 1)) / 3 for k in ks}
poc = max(ks, key=lambda k: perfil[k])
lo_k = hi_k = poc; acum = perfil[poc]
while acum < .7 * tot:
    arriba, abajo = perfil.get(hi_k + 1, 0), perfil.get(lo_k - 1, 0)
    if arriba >= abajo: hi_k += 1; acum += arriba
    else: lo_k -= 1; acum += abajo
picos = [k for k in ks if suav[k] >= suav.get(k - 1, 0) and suav[k] >= suav.get(k + 1, 0)]
hvn_inf = max([k for k in picos if k * FILAS < 103.5], key=lambda k: suav[k])
lvn = min([k for k in ks if hvn_inf < k < poc], key=lambda k: suav[k])
P = lambda k: (k + .5) * FILAS
niv = dict(poc=P(poc), vah=(hi_k + 1) * FILAS, val=lo_k * FILAS, hvn=P(hvn_inf), lvn=P(lvn))
ordenp = niv['lvn']
j = min(range(SEN + 1, SEN + 6), key=lambda i: b[i][2])
b[j][2] = min(b[j][2], ordenp - .08)
bb = [x[:4] for x in b]
L = Lienzo(bb, x1=690)
L.o.append(f'<rect x="{X0}" y="{Y0}" width="{L.x(BLOQUE - 1) + L.paso / 2 - X0:.1f}" height="{Y1 - Y0}" rx="10" fill="{C["accent"]}" opacity=".05"/>')
L.o.append(f'<text x="{X0 + 14}" y="{Y0 + 30}" fill="{C["muted"]}" font-size="20" font-weight="700" font-family="{FONT}">Último bloque cerrado → perfil</text>')
L.o.append(f'<rect x="700" y="{L.y(niv["vah"]):.1f}" width="200" height="{L.y(niv["val"]) - L.y(niv["vah"]):.1f}" fill="{C["muted"]}" opacity=".08"/>')
mx = max(perfil.values())
for k in ks:
    w = perfil[k] / mx * 170
    if k == poc: col, op = C['red'], .95
    elif k == hvn_inf: col, op = C['accent'], .95
    elif k == lvn: col, op = C['purple'], .95
    else: col, op = C['accent'], (.38 if lo_k <= k <= hi_k else .16)
    L.o.append(f'<rect x="700" y="{L.y((k + 1) * FILAS) + 1:.1f}" width="{w:.1f}" height="{abs(L.y((k + 1) * FILAS) - L.y(k * FILAS)) - 2:.1f}" fill="{col}" opacity="{op}" rx="2"/>')
for clave, col in (('vah', C['muted']), ('val', C['muted']), ('lvn', C['purple'])):
    L.o.append(f'<line x1="{L.x(BLOQUE - 1):.1f}" x2="{X1}" y1="{L.y(niv[clave]):.1f}" y2="{L.y(niv[clave]):.1f}" stroke="{col}" stroke-width="2" stroke-dasharray="5 6"/>')
L.velas()
f = primer_toque(bb, [ordenp] * len(bb), SEN + 1)
orden(L, SEN, f, ordenp)
L.marca(SEN, bb[SEN][1], C['amber'], 'Señal', arriba=True)
L.marca(f, ordenp, C['green'], 'Ejecutada')
ys = []
for clave, txt, col in sorted((('vah', 'VAH', C['muted']), ('poc', 'POC', C['red']), ('lvn', 'LVN', C['purple']), ('hvn', 'HVN', C['accent']), ('val', 'VAL', C['muted'])), key=lambda t: L.y(niv[t[0]])):
    yy = max(L.y(niv[clave]), ys[-1] + 42) if ys else L.y(niv[clave]); ys.append(yy)
    etiqueta(L, 896, yy, txt, col, ancla='end', tam=19)
open('graficos/perfil.svg', 'w').write(L.svg())
info['perfil'] = dict(niv, bloque=BLOQUE, senal=SEN, cierre_senal=round(bb[SEN][3], 2), ejec=f)

# 3 · Distancia en ATR: compra fija 0,5 × ATR por debajo del cierre de la vela de la señal
b = serie(11, [(9, 103, .7), (8, 105, .8), (10, 107.5, .8)])
a = atr(b)
SEN = 16; K = .5
ordenp = b[SEN][3] - K * a[SEN]
for i in (SEN + 1,): b[i][2] = max(b[i][2], ordenp + .12)  # la vela siguiente aún no llega
j = SEN + 2
b[j][2] = min(b[j][2], ordenp - .05)
L = Lienzo(b); L.velas()
f = primer_toque(b, [ordenp] * len(b), SEN + 1)
xf = L.x(f + 4)
L.o.append(f'<line x1="{L.x(SEN) - 16:.1f}" x2="{xf:.1f}" y1="{L.y(b[SEN][3]):.1f}" y2="{L.y(b[SEN][3]):.1f}" stroke="{C["text"]}" stroke-width="2" stroke-dasharray="4 5"/>')
orden(L, SEN, f + 4, ordenp)
xb = xf + 12
L.o.append(f'<path d="M{xb - 8:.1f},{L.y(b[SEN][3]):.1f} H{xb:.1f} V{L.y(ordenp):.1f} H{xb - 8:.1f}" fill="none" stroke="{C["amber"]}" stroke-width="3"/>')
etiqueta(L, xb + 10, (L.y(b[SEN][3]) + L.y(ordenp)) / 2, '0,5 × ATR', C['amber'])
L.marca(SEN, b[SEN][1], C['amber'], 'Señal', arriba=True)
L.marca(f, ordenp, C['green'])
L.o.append(f'<text x="{L.x(f) + 24:.1f}" y="{L.y(ordenp) + 44:.1f}" fill="{C["green"]}" font-size="22" font-weight="800" font-family="{FONT}">Ejecutada</text>')
open('graficos/atr.svg', 'w').write(L.svg()); info['atr'] = dict(senal=SEN, ejec=f, atr=round(a[SEN], 3))

# 4 · Nivel de la vela de la señal: low, 50 % o apertura; aquí la orden en el 50 %
random.seed(4)
b = serie(17, [(6, 101.2, .25), (3, 100.6, .2)])
b.append([100.7, 103.6, 99.6, 103.3])   # vela de la señal: gran vela alcista
SEN = len(b) - 1
b += [[103.3, 103.8, 102.4, 102.6], [102.6, 102.8, 101.5, 101.95], [101.95, 103.3, 101.85, 103.1], [103.1, 104.2, 102.9, 104.0], [104.0, 104.6, 103.7, 104.4]]
o_, h_, l_, c_ = b[SEN]
mitad = (h_ + l_) / 2
L = Lienzo(b, x1=640)
for p_, txt, col in ((o_, 'Apertura', C['muted']), (mitad, '50 % de la vela', C['amber']), (l_, 'Low (largos)', C['muted'])):
    w = 4 if col == C['amber'] else 2
    L.o.append(f'<line x1="{L.x(SEN) - L.paso * .45:.1f}" x2="{X1 - 4}" y1="{L.y(p_):.1f}" y2="{L.y(p_):.1f}" stroke="{col}" stroke-width="{w}" stroke-dasharray="{"10 7" if w == 4 else "5 6"}"/>')
    etiqueta(L, 660, L.y(p_), txt, col, tam=21)
L.velas()
f = primer_toque(b, [mitad] * len(b), SEN + 1)
L.marca(SEN, h_, C['amber'], 'Señal', arriba=True)
L.marca(f, mitad, C['green'], 'Ejecutada')
open('graficos/vela.svg', 'w').write(L.svg()); info['vela'] = dict(senal=SEN, ejec=f)

# 5 · Fibonacci del último tramo ZigZag: orden en el 61,8 % del último tramo
b = serie(21, [(8, 104, .3), (10, 99.5, .35), (16, 109.5, .4), (8, 103.9, .35), (10, 108.5, .45)])
lows = lambda r: min(r, key=lambda i: b[i][2]); highs = lambda r: max(r, key=lambda i: b[i][1])
p0 = lows(range(0, 3)); p1 = highs(range(3, 12)); p2 = lows(range(p1, 22)); p3 = highs(range(p2, 37))
lo, hi = b[p2][2], b[p3][1]
NIV = (.236, .382, .5, .618, .786)
nivf = {r: hi - (hi - lo) * r for r in NIV}
SEN = p3 + 2
j = min(range(SEN + 1, SEN + 8), key=lambda i: b[i][2])
b[j][2] = min(b[j][2], nivf[.618] - .05)
L = Lienzo(b, x1=750)
for r in NIV:
    col = C['amber'] if r == .618 else C['muted']; w = 4 if r == .618 else 2
    L.o.append(f'<line x1="{L.x(p3):.1f}" x2="770" y1="{L.y(nivf[r]):.1f}" y2="{L.y(nivf[r]):.1f}" stroke="{col}" stroke-width="{w}" stroke-dasharray="{"10 7" if w == 4 else "8 8"}"/>')
    etiqueta(L, 780, L.y(nivf[r]), f'{r * 100:.1f} %'.replace('.', ','), col)
L.velas()
piv = [(p0, b[p0][2]), (p1, b[p1][1]), (p2, lo), (p3, hi)]
L.o.append(f'<polyline points="{" ".join(f"{L.x(i):.1f},{L.y(v):.1f}" for i, v in piv)}" fill="none" stroke="{C["purple"]}" stroke-width="3.5" opacity=".9"/>')
for i, v in piv: L.o.append(f'<circle cx="{L.x(i):.1f}" cy="{L.y(v):.1f}" r="7" fill="{C["purple"]}"/>')
xm, ym = (L.x(p2) + L.x(p3)) / 2, (L.y(lo) + L.y(hi)) / 2
L.o.append(f'<text x="{xm - 22:.1f}" y="{ym:.1f}" fill="{C["purple"]}" font-size="21" font-weight="800" text-anchor="end" font-family="{FONT}">Último tramo</text>')
f = primer_toque(b, [nivf[.618]] * len(b), SEN + 1)
L.marca(SEN, b[SEN][1], C['amber'], 'Señal', arriba=True)
L.marca(f, nivf[.618], C['green'], 'Ejecutada')
open('graficos/fibonacci.svg', 'w').write(L.svg()); info['fibonacci'] = dict(pivotes=[p0, p1, p2, p3], senal=SEN, ejec=f)

if os.path.exists('graficos/bollinger.svg'): os.remove('graficos/bollinger.svg')
json.dump(info, open('graficos/info.json', 'w'), indent=1)
print(json.dumps(info))
