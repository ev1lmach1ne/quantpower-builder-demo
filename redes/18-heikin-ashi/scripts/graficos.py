"""Gráficos SVG del carrusel de Heikin Ashi (datos simulados con fines ilustrativos).
Uso (desde redes/18-heikin-ashi): python3 scripts/graficos.py"""
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

os.makedirs('graficos', exist_ok=True)
# Mercado simulado: bajada con ruido, giro y subida; las velas normales alternan colores, las HA no
b = serie(12, [(15, 96.2, .75), (5, 95.6, .55), (18, 104, .8)], p0=101)
ha = heikin_ashi(b)
lo = min(x[2] for x in b); hi = max(x[1] for x in b)
for nombre, datos in (('normal', b), ('ha', ha)):
    L = Lienzo(datos, lo=lo, hi=hi); L.velas()
    open(f'graficos/{nombre}.svg', 'w').write(L.svg())

# Confirmación: señal del setup, cambio de color HA y N = 3 velas HA seguidas a favor
color = ['v' if x[3] >= x[0] else 'r' for x in ha]
N = 3
giro = next(i for i in range(15, len(ha) - N) if color[i - 1] == 'r' and all(color[k] == 'v' for k in range(i, i + N)))
conf = giro + N - 1          # la entrada se confirma al cerrar la tercera vela HA verde seguida
SEN = giro - 1               # el setup ya había señalado, con el HA todavía en contra
L = Lienzo(ha, lo=lo, hi=hi)
L.o.append(f'<rect x="{L.x(conf - N + 1) - L.paso / 2:.1f}" y="{Y0}" width="{L.paso * N:.1f}" height="{Y1 - Y0}" rx="8" fill="{C["green"]}" opacity=".10"/>')
L.velas()
L.marca(SEN, ha[SEN][1], C['amber'], 'Señal', arriba=True)
L.marca(giro, ha[giro][2], C['accent'], 'Cambio de color')
for k in range(conf - N + 1, conf + 1):
    L.o.append(f'<text x="{L.x(k):.1f}" y="{L.y(ha[k][1]) - 14:.1f}" fill="{C["green"]}" font-size="22" font-weight="900" text-anchor="middle" font-family="{FONT}">{k - conf + N}</text>')
etiqueta(L, L.x(conf) + 24, L.y(ha[conf][2]) + 50, f'{N}ª vela seguida: entrada', C['green'], tam=21)
open('graficos/confirmacion.svg', 'w').write(L.svg())
json.dump(dict(senal=SEN, giro=giro, confirmacion=conf, N=N), open('graficos/info.json', 'w'))
print(SEN, giro, conf)
