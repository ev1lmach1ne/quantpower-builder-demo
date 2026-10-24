"""Gráfico del ejemplo «Heikin Ashi + EMA 50 + RSI» (datos simulados con fines ilustrativos).
Uso (desde redes/19-heikin-ashi-combinado): python3 scripts/graficos.py  (SEMILLA=n para otra serie)"""
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


def heikin_ashi(b):
    """HA close = (O+H+L+C)/4; HA open = media del HA open y HA close anteriores; máx/mín con los extremos reales."""
    ha = []
    for i, (o, h, l, c) in enumerate(b):
        hc = (o + h + l + c) / 4
        ho = (o + c) / 2 if i == 0 else (ha[-1][0] + ha[-1][3]) / 2
        ha.append([ho, max(h, ho, hc), min(l, ho, hc), hc])
    return ha


def rsi(c, n=14):
    """RSI de Wilder."""
    out = [50.0]; g = p = 0.0
    for i in range(1, len(c)):
        d = c[i] - c[i - 1]; up, dn = max(d, 0), max(-d, 0)
        if i <= n: g += up / n; p += dn / n
        else: g = (g * (n - 1) + up) / n; p = (p * (n - 1) + dn) / n
        out.append(100 - 100 / (1 + g / p) if p else 100.0)
    return out

SEMILLA = int(os.environ.get('SEMILLA', 5))
VISTA = 64     # velas que se dibujan (las anteriores solo calientan la EMA 50 y el RSI)
b = serie(SEMILLA, [(40, 95, .6), (22, 92, .55), (14, 94.5, .55), (30, 101, .6)], p0=100)
c = [x[3] for x in b]; e = ema(c, 50); r = rsi(c); ha = heikin_ashi(b)
verde = [x[3] >= x[0] for x in ha]
racha = [0] * len(b)
for i in range(len(b)): racha[i] = (racha[i - 1] + 1 if i and verde[i] else (1 if verde[i] else 0))
cond = {'ema': [c[i] > e[i] for i in range(len(b))], 'rsi': [r[i] > 50 for i in range(len(b))], 'ha': [racha[i] >= 3 for i in range(len(b))]}
ini = len(b) - VISTA
entrada = next(i for i in range(ini + 10, len(b)) if all(cond[k][i] for k in cond))
def desde(k):  # primera vela del tramo en el que la condición sigue cumpliéndose en la entrada
    i = entrada
    while cond[k][i - 1]: i -= 1
    return i
activ = {k: desde(k) for k in cond}
orden = sorted(activ, key=activ.get)
print('activ', {k: v - ini for k, v in activ.items()}, 'entrada', entrada - ini)
if len(set(activ.values())) < 3: raise SystemExit('condiciones en la misma vela: prueba otra SEMILLA')

v = lambda xs: xs[ini:]
L = Lienzo(v(ha))
xi = lambda i: L.x(i - ini)
NOMBRE = {'ema': 'Cierre > EMA 50', 'rsi': 'RSI > 50', 'ha': '3 velas HA verdes'}
COL = {'ema': C['accent'], 'rsi': C['purple'], 'ha': C['green']}
# bandas y guías verticales (se dibujan también en el panel del RSI)
guias = []
L.o.append(f'<rect x="{xi(entrada) - L.paso / 2:.1f}" y="{Y0}" width="{L.paso:.1f}" height="{Y1 - Y0}" fill="{C["green"]}" opacity=".16"/>')
for n, k in enumerate(orden, 1):
    guias.append((xi(activ[k]), COL[k], n))
    L.o.append(f'<line x1="{xi(activ[k]):.1f}" x2="{xi(activ[k]):.1f}" y1="{Y0}" y2="{Y1}" stroke="{COL[k]}" stroke-width="2" stroke-dasharray="5 6" opacity=".8"/>')
L.linea(v(e), C['accent'], 3.5)
L.velas()
L.o.append(f'<text x="{L.x(4):.1f}" y="{L.y(e[ini + 4]) - 14:.1f}" fill="{C["accent"]}" font-size="20" font-weight="800" font-family="{FONT}">EMA 50</text>')
for x, col, n in guias:
    L.o.append(f'<circle cx="{x:.1f}" cy="{Y0 + 22}" r="17" fill="{C["deep"]}" stroke="{col}" stroke-width="3"/><text x="{x:.1f}" y="{Y0 + 30}" fill="{col}" font-size="21" font-weight="900" text-anchor="middle" font-family="{FONT}">{n}</text>')
etiqueta(L, xi(entrada) + 16, L.y(ha[entrada][2]) + 44, 'Entrada: las 3 a la vez', C['green'], tam=20)
L.o.append(f'<text x="{X0 + 12}" y="{Y1 - 8}" fill="{C["muted"]}" font-size="18" font-weight="700" font-family="{FONT}">Velas Heikin Ashi</text>')

# panel del RSI
RH, R0, R1 = 240, 24, 216
yr = lambda val: R1 - (val - 20) / 60 * (R1 - R0)
p = [f'<g transform="translate(0,{H + 10})"><rect x="0" y="0" width="{W}" height="{RH}" rx="18" fill="{C["panel"]}"/>']
p.append(f'<rect x="{xi(entrada) - L.paso / 2:.1f}" y="{R0}" width="{L.paso:.1f}" height="{R1 - R0}" fill="{C["green"]}" opacity=".16"/>')
for x, col, n in guias: p.append(f'<line x1="{x:.1f}" x2="{x:.1f}" y1="{R0}" y2="{R1}" stroke="{col}" stroke-width="2" stroke-dasharray="5 6" opacity=".8"/>')
p.append(f'<line x1="{X0}" x2="{X1}" y1="{yr(50):.1f}" y2="{yr(50):.1f}" stroke="{C["muted"]}" stroke-width="2" stroke-dasharray="8 7"/>')
pts = ' '.join(f'{xi(i):.1f},{yr(max(20, min(80, r[i]))):.1f}' for i in range(ini, len(b)))
p.append(f'<polyline points="{pts}" fill="none" stroke="{C["purple"]}" stroke-width="3.5"/>')
p.append(f'<text x="{X0 + 12}" y="{R0 + 22}" fill="{C["purple"]}" font-size="20" font-weight="800" font-family="{FONT}">RSI 14</text>')
p.append(f'<text x="{X1 - 8}" y="{yr(50) - 10:.1f}" fill="{C["muted"]}" font-size="18" font-weight="700" text-anchor="end" font-family="{FONT}">50</text>')
p.append('</g>')
svg = L.svg(''.join(p)).replace(f'viewBox="0 0 {W} {H}"', f'viewBox="0 0 {W} {H + 10 + RH}"', 1)
os.makedirs('graficos', exist_ok=True)
open('graficos/combinado.svg', 'w').write(svg)
json.dump(dict(semilla=SEMILLA, orden=orden, activacion={k: activ[k] - ini for k in cond}, entrada=entrada - ini,
               nombres=NOMBRE), open('graficos/info.json', 'w'), ensure_ascii=False, indent=1)
