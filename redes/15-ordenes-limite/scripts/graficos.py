"""Gráficos SVG del carrusel de órdenes límite (datos simulados con fines ilustrativos).
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

def sma_std(c, n):
    m, s = [], []
    for i in range(len(c)):
        w = c[max(0, i - n + 1):i + 1]; mu = sum(w) / len(w)
        m.append(mu); s.append(math.sqrt(sum((x - mu) ** 2 for x in w) / len(w)))
    return m, s

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

os.makedirs('graficos', exist_ok=True)
info = {}

# 1 · Media móvil: tendencia alcista, la orden espera el retroceso a la EMA 20 y la sigue vela a vela
b = serie(3, [(20, 101, .35), (16, 109, .45), (9, 106.2, .35), (15, 112, .45)])
c = [x[3] for x in b]; e = ema(c, 20)
SEN = 36
j = min(range(SEN + 1, SEN + 12), key=lambda i: b[i][2] - e[i])  # el retroceso llega a la media
b[j][2] = min(b[j][2], e[j] - .05)
L = Lienzo(b); L.velas(); L.linea(e, C['accent'], 4)
f = primer_toque(b, e, SEN + 1)
L.o.append(f'<line x1="{L.x(SEN):.1f}" x2="{L.x(f):.1f}" y1="{L.y(e[SEN]) + 0:.1f}" y2="{L.y(e[f]):.1f}" stroke="{C["amber"]}" stroke-width="3" stroke-dasharray="6 6"/>')
L.marca(SEN, b[SEN][1], C['amber'], 'Señal', arriba=True)
L.marca(f, e[f], C['green'], 'Ejecutada')
L.o.append(f'<text x="{L.x(52):.1f}" y="{L.y(e[52]) + 40:.1f}" fill="{C["accent"]}" font-size="22" font-weight="800" text-anchor="middle" font-family="{FONT}">EMA 20</text>')
open('graficos/media.svg', 'w').write(L.svg()); info['media'] = dict(senal=SEN, ejec=f)

# 2 · Bollinger: retroceso a la banda inferior dentro de una tendencia alcista
b = serie(8, [(22, 101.5, .4), (14, 107, .5), (8, 102.6, .45), (16, 110, .5)])
c = [x[3] for x in b]; m, sd = sma_std(c, 20); up = [a + 2 * s_ for a, s_ in zip(m, sd)]; dn = [a - 2 * s_ for a, s_ in zip(m, sd)]
SEN = 36
j = min(range(SEN + 1, SEN + 12), key=lambda i: b[i][2] - dn[i])  # el retroceso llega a la banda inferior
b[j][2] = min(b[j][2], dn[j] - .05)
L = Lienzo(b)
area = ' '.join(f'{L.x(i):.1f},{L.y(v):.1f}' for i, v in enumerate(up)) + ' ' + ' '.join(f'{L.x(i):.1f},{L.y(v):.1f}' for i, v in reversed(list(enumerate(dn))))
L.o.append(f'<polygon points="{area}" fill="{C["purple"]}" opacity=".08"/>')
L.linea(up, C['purple'], 2.5, op=.9); L.linea(dn, C['purple'], 2.5, op=.9); L.linea(m, C['purple'], 2, dash='6 6', op=.7)
L.velas()
f = primer_toque(b, dn, SEN + 1)
L.marca(SEN, b[SEN][1], C['amber'], 'Señal', arriba=True)
L.marca(f, dn[f], C['green'], 'Ejecutada')
L.o.append(f'<text x="{L.x(23):.1f}" y="{L.y(dn[23]) + 34:.1f}" fill="{C["purple"]}" font-size="22" font-weight="800" text-anchor="middle" font-family="{FONT}">Banda inferior</text>')
open('graficos/bollinger.svg', 'w').write(L.svg()); info['bollinger'] = dict(senal=SEN, ejec=f)

# 3 · Perfil de volumen interpretado: el mismo mercado del vídeo, con PoC, área de valor, HVN y LVN
mk = json.load(open('../14-video-setup-limites/src/mercado.json'))
bb = [[x['o'], x['h'], x['l'], x['c']] for x in mk['barras']]
perfil = {q['precio']: q['vol'] for q in mk['perfil']}
tot = sum(perfil.values()); poc = max(perfil, key=perfil.get)
va = {poc}; acum = perfil[poc]; lo_, hi_ = poc, poc
while acum < .7 * tot:
    a_ = perfil.get(hi_ + 1, 0); z_ = perfil.get(lo_ - 1, 0)
    if a_ >= z_ and (hi_ + 1) in perfil: hi_ += 1; acum += a_
    elif (lo_ - 1) in perfil: lo_ -= 1; acum += z_
    else: hi_ += 1; acum += a_
L = Lienzo(bb, x1=700); L.velas()
mx = max(perfil.values())
for p_, v in perfil.items():
    w = v / mx * 190; dentro = lo_ <= p_ <= hi_
    col = C['red'] if p_ == poc else (C['accent'] if p_ + .5 in (mk['hvn'], mk['objetivo']) else (C['purple'] if p_ + .5 == mk['lvn'] else '#4fc3f7'))
    op = .9 if p_ == poc or p_ + .5 in (mk['hvn'], mk['objetivo'], mk['lvn']) else (.35 if dentro else .16)
    L.o.append(f'<rect x="{X1 - w:.1f}" y="{L.y(p_ + 1) + 1:.1f}" width="{w:.1f}" height="{abs(L.y(p_ + 1) - L.y(p_)) - 2:.1f}" fill="{col}" opacity="{op}" rx="2"/>')
L.o.append(f'<rect x="{X1 - 196:.1f}" y="{L.y(hi_ + 1):.1f}" width="196" height="{L.y(lo_) - L.y(hi_ + 1):.1f}" fill="none" stroke="{C["muted"]}" stroke-dasharray="5 5" rx="6"/>')
for p_, t, col in [(hi_ + 1, 'VAH', C['muted']), (lo_, 'VAL', C['muted'])]:
    L.o.append(f'<text x="{X1 - 200:.1f}" y="{L.y(p_) + (18 if t == "VAH" else -6):.1f}" fill="{col}" font-size="18" font-weight="700" text-anchor="end" font-family="{FONT}">{t}</text>')
etiq = [(poc + .5, 'PoC', C['red']), (mk['objetivo'], 'HVN', C['accent']), (mk['lvn'], 'LVN', C['purple']), (mk['hvn'], 'HVN', C['accent'])]
usados = []
for p_, t, col in etiq:
    yy = L.y(p_)
    if any(abs(yy - u) < 34 for u in usados): continue
    usados.append(yy)
    L.o.append(f'<rect x="712" y="{yy - 18:.1f}" width="74" height="36" rx="8" fill="{C["deep"]}" stroke="{col}" stroke-width="2"/>')
    L.o.append(f'<text x="749" y="{yy + 8:.1f}" fill="{col}" font-size="20" font-weight="800" text-anchor="middle" font-family="{FONT}">{t}</text>')
orden = mk['ordenes'][0]
L.o.append(f'<line x1="{L.x(mk["barraOrdenes"]):.1f}" x2="700" y1="{L.y(orden["precio"]):.1f}" y2="{L.y(orden["precio"]):.1f}" stroke="{C["green"]}" stroke-width="3" stroke-dasharray="10 8"/>')
L.marca(orden['barra'], orden['precio'], C['green'], 'Ejecutada')
open('graficos/perfil.svg', 'w').write(L.svg())
info['perfil'] = dict(poc=poc + .5, vah=hi_ + 1, val=lo_, hvn=mk['hvn'], lvn=mk['lvn'], objetivo=mk['objetivo'], orden=orden['precio'])

# 4 · Fibonacci: retroceso del impulso; la orden espera en el 61,8 %
b = serie(21, [(10, 100.4, .3), (18, 110, .45), (12, 104.3, .4), (14, 113, .45)])
ini = min(range(0, 14), key=lambda i: b[i][2]); fin = max(range(14, 30), key=lambda i: b[i][1])
lo, hi = b[ini][2], b[fin][1]
niv = {r: hi - (hi - lo) * r for r in (.382, .5, .618)}
j = min(range(fin + 1, fin + 14), key=lambda i: b[i][2])  # el retroceso llega al 61,8 %
b[j][2] = min(b[j][2], niv[.618] - .05)
L = Lienzo(b)
L.o.append(f'<line x1="{L.x(ini):.1f}" y1="{L.y(lo):.1f}" x2="{L.x(fin):.1f}" y2="{L.y(hi):.1f}" stroke="{C["muted"]}" stroke-width="2" stroke-dasharray="4 6"/>')
for r, col in [(.382, C['muted']), (.5, C['muted']), (.618, C['amber'])]:
    L.nivel(niv[r], col, f'{r * 100:.1f} %'.replace('.', ',').replace(',0 %', ' %'), x_ini=L.x(fin), dash='8 8', w=2 if r != .618 else 3)
L.velas()
f = primer_toque(b, [niv[.618]] * len(b), fin + 1)
L.marca(fin, hi, C['amber'], 'Señal', arriba=True)
L.marca(f, niv[.618], C['green'], 'Ejecutada')
open('graficos/fibonacci.svg', 'w').write(L.svg()); info['fibonacci'] = dict(ejec=f)
json.dump(info, open('graficos/info.json', 'w'), indent=1)
print(json.dumps(info))
