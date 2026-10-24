"""Monta publicacion.html: 2 diapositivas con un ejemplo de Heikin Ashi combinado con EMA 50 y RSI 14.
Uso (desde redes/19-heikin-ashi-combinado): python3 scripts/graficos.py && python3 scripts/montar.py
Reutiliza la cabecera y los estilos de ../15-ordenes-limite/publicacion.html."""
import json, re

N = 2
info = json.load(open('graficos/info.json'))
base = open('../15-ordenes-limite/publicacion.html').read()
cab = base[:base.index('<body>')]
cab = cab.replace(cab[cab.index('<title>'):cab.index('</title>') + 8], '<title>Heikin Ashi combinado — QuantPower Builder</title>')
cab = re.sub(r'<!--.*?-->', '''<!--
  Ejemplo «Heikin Ashi + EMA 50 + RSI 14» (confirmación HA: próximamente, v0.8.1). Se renderiza con redes/renderizar.sh.
  Parámetros: ?s=1…2 y ?f=vertical (1080×1350, por defecto) o ?f=tiktok (1080×1920).
  Generado con scripts/montar.py; el gráfico (graficos/combinado.svg) son datos simulados de scripts/graficos.py.
-->''', cab, count=1, flags=re.S)
cab = cab.replace('</style>', '''  .conf { display: grid; gap: 10px; }
  .cf { display: grid; grid-template-columns: 52px 1fr auto; align-items: center; gap: 16px; padding: 13px 20px; border-radius: 16px;
    border: 1px solid var(--border); background: rgba(26,42,69,.6); font-size: 23px; color: var(--text-muted); }
  .cf b { display: block; font-size: 25px; color: var(--text-strong); }
  .cf i { display: grid; place-items: center; width: 46px; height: 46px; border-radius: 50%; font-style: normal; font-size: 22px; font-weight: 900; border: 3px solid; }
  .cf em { font-style: normal; font-family: var(--mono); font-size: 20px; color: var(--text-muted); }
  .tiktok .cf { padding: 10px 16px; font-size: 20px; }
  .tiktok .cf b { font-size: 22px; }
  .slide[data-s="1"] .chart { width: 70%; align-self: center; }
  .tiktok .slide[data-s="1"] .chart { width: 74%; }
  .slide[data-s="1"] .valido { padding: 12px 20px; font-size: 26px; }
  body:not(.tiktok) .slide[data-s="1"] { gap: 18px; }
</style>''', 1)
svg = open('graficos/combinado.svg').read().replace('<svg ', '<svg class="chart" ', 1)

def slide(n, cuerpo, pie):
    return f'''<section class="slide" data-s="{n}">
  <div class="grid"></div>
  <div class="top"><div class="logo"></div><strong>QuantPower Builder</strong><span class="count">Heikin Ashi + 2 · {n}/{N}</span></div>
{cuerpo}
  <div class="foot">{pie}</div>
</section>
'''

FILA = {
    'ha': ('var(--green)', 'Heikin Ashi', 'Cambia a verde y suma 3 velas seguidas'),
    'rsi': ('#b38af6', 'Momento · RSI 14', 'Cruza y se mantiene por encima de 50'),
    'ema': ('var(--accent)', 'Tendencia · EMA 50', 'El cierre real supera la EMA 50'),
}
act, ent = info['activacion'], info['entrada']
filas = ''
for n, k in enumerate(info['orden'], 1):
    col, t, d = FILA[k]
    cuando = 'misma vela de la entrada' if act[k] == ent else f'{ent - act[k]} velas antes'
    filas += f'    <div class="cf"><i style="color:{col};border-color:{col}">{n}</i><span><b>{t}</b>{d}</span><em>{cuando}</em></div>\n'

S = [slide(1, f'''  <span class="eyebrow">Ejemplo · largo con 3 confirmaciones</span>
  <h2>Tres confirmaciones, <span>una entrada.</span></h2>
  {svg}
  <div class="conf">
{filas}  </div>
  <div class="valido">ENTRADA: las 3 a la vez («Todas · AND»)</div>''',
  '<span>Datos simulados con fines ilustrativos</span><b>quantpowerbuilder.com</b>'),
  slide(2, '''  <span class="eyebrow">Por qué combinarlas</span>
  <h2>Cada una filtra <span>algo distinto.</span></h2>
  <div class="cards">
    <div class="card"><b style="color:var(--accent)">Tendencia · EMA 50</b>No compras contra la tendencia: el precio ya está por encima de su media</div>
    <div class="card"><b style="color:#b38af6">Momento · RSI 14</b>El impulso acompaña: por encima de 50 dominan las subidas</div>
    <div class="card"><b style="color:var(--green)">Heikin Ashi · N velas</b>El giro ya está en marcha: 3 velas verdes seguidas, no una sola</div>
  </div>
  <div class="warn"><b>El precio de cada condición:</b> más confirmaciones dan menos entradas y algo más tardías, pero más filtradas. Pruébalo con el backtest antes de decidir cuántas exigir.</div>
  <p class="lead">La EMA y el RSI ya están en el constructor. <b>Heikin Ashi como confirmación llega en la v0.8.1.</b></p>
  <div class="button">quantpowerbuilder.com</div>''', '<span>Últimas licencias gratis de por vida</span><b>v0.8.1</b>')]

guion = base[base.index('<script>'):]
open('publicacion.html', 'w').write(cab + '<body>\n\n' + '\n'.join(S) + '\n' + guion)
print('ok', len(S))
