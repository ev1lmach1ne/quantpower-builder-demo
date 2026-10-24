"""Monta publicacion.html: carrusel de 6 diapositivas sobre Heikin Ashi como confirmación de entrada (v0.8.1).
Uso (desde redes/18-heikin-ashi): python3 scripts/graficos.py && python3 scripts/montar.py
Reutiliza la cabecera y los estilos de ../15-ordenes-limite/publicacion.html. Función anunciada por el equipo:
Heikin Ashi como confirmación de entradas al cambiar de color, con N velas consecutivas en una dirección."""
import re

N = 6
base = open('../15-ordenes-limite/publicacion.html').read()
cab = base[:base.index('<body>')]
cab = cab.replace(cab[cab.index('<title>'):cab.index('</title>') + 8], '<title>Heikin Ashi — QuantPower Builder</title>')
cab = re.sub(r'<!--.*?-->', '''<!--
  Carrusel «Heikin Ashi para confirmar entradas» (próximamente, v0.8.1). Se renderiza a PNG con redes/renderizar.sh.
  Parámetros: ?s=1…6 y ?f=vertical (1080×1350, por defecto) o ?f=tiktok (1080×1920).
  Generado con scripts/montar.py; los gráficos (graficos/*.svg) son datos simulados de scripts/graficos.py.
-->''', cab, count=1, flags=re.S)
cab = cab.replace('</style>', '''  .formulas { display: grid; gap: 12px; }
  .fx { display: grid; grid-template-columns: 210px 1fr; align-items: center; gap: 16px; padding: 18px 22px; border-radius: 16px;
    border: 1px solid var(--border); background: rgba(26,42,69,.6); }
  .fx b { font-size: 26px; color: var(--text-strong); }
  .fx code { font-family: var(--mono); font-size: 25px; color: var(--accent); }
  .tiktok .fx { grid-template-columns: 180px 1fr; padding: 14px 18px; }
  .tiktok .fx code { font-size: 22px; }
  .par { display: grid; gap: 8px; }
  .par .chart { width: 70%; justify-self: center; }
  .rot { font-family: var(--mono); font-size: 20px; letter-spacing: .12em; text-transform: uppercase; color: var(--text-muted); text-align: center; }
  .rot b { color: var(--accent); }
  .tiktok .par .chart { width: 80%; }
  .vela { flex: none; display: inline-block; width: 26px; border-radius: 4px; position: relative; }
</style>''', 1)
svg = lambda n: open(f'graficos/{n}.svg').read().replace('<svg ', '<svg class="chart" ', 1)

def slide(n, cuerpo, pie='<span>Próximamente en la v0.8.1</span><b>quantpowerbuilder.com</b>'):
    return f'''<section class="slide" data-s="{n}">
  <div class="grid"></div>
  <div class="top"><div class="logo"></div><strong>QuantPower Builder</strong><span class="count">Heikin Ashi · {n}/{N}</span></div>
{cuerpo}
  <div class="foot">{pie}</div>
</section>
'''

S = []
S.append(slide(1, '''  <span class="badge amber">Próximamente · v0.8.1</span>
  <div class="hero">Heikin Ashi para <span>confirmar tus entradas.</span></div>
  <p class="lead">Velas que promedian el precio para ver la tendencia sin tanto ruido. En la v0.8.1 podrás usarlas <b>como confirmación de la entrada</b> de tus setups.</p>
  <div class="tiles">
    <div class="tile"><i>Σ</i><b>Qué es</b><span>Velas calculadas con medias del precio</span></div>
    <div class="tile"><i>👁</i><b>Cómo se lee</b><span>Color, cuerpo y mechas</span></div>
    <div class="tile"><i>⇄</i><b>Cambio de color</b><span>El impulso gira a tu favor</span></div>
    <div class="tile"><i>N</i><b>Velas seguidas</b><span>Tú eliges cuántas confirmar</span></div>
  </div>''', '<span>Desliza para verlo</span><b>quantpowerbuilder.com</b>'))

S.append(slide(2, '''  <span class="eyebrow">Qué es Heikin Ashi</span>
  <h2>Velas hechas con <span>medias del precio.</span></h2>
  <p class="lead">«Heikin Ashi» significa «barra media» en japonés. Cada vela se calcula con la vela real y con la vela Heikin Ashi anterior:</p>
  <div class="formulas">
    <div class="fx"><b>Cierre HA</b><code>(O + H + L + C) / 4</code></div>
    <div class="fx"><b>Apertura HA</b><code>(Apertura HA ant. + Cierre HA ant.) / 2</code></div>
    <div class="fx"><b>Máximo HA</b><code>máx(H, Apertura HA, Cierre HA)</code></div>
    <div class="fx"><b>Mínimo HA</b><code>mín(L, Apertura HA, Cierre HA)</code></div>
  </div>
  <div class="warn"><b>Ojo:</b> el cierre HA es una media, no un precio al que se pueda operar. Sirve para leer la tendencia, no para fijar precios.</div>''',
  '<span>O, H, L, C: apertura, máximo, mínimo y cierre reales</span><b>quantpowerbuilder.com</b>'))

S.append(slide(3, f'''  <span class="eyebrow">El mismo mercado, dos lecturas</span>
  <h2>Menos ruido, <span>tendencia más clara.</span></h2>
  <div class="par">
    <div class="rot">Velas normales</div>
    {svg('normal')}
    <div class="rot"><b>Heikin Ashi</b></div>
    {svg('ha')}
  </div>
  <p class="lead">En la subida, las velas normales alternan colores; las Heikin Ashi forman <b>rachas del mismo color.</b></p>''',
  '<span>Datos simulados con fines ilustrativos</span><b>quantpowerbuilder.com</b>'))

S.append(slide(4, '''  <span class="eyebrow">Cómo se leen</span>
  <h2>Color, cuerpo <span>y mechas.</span></h2>
  <div class="cards">
    <div class="card"><b style="color:var(--green)">Verde sin mecha inferior</b>Impulso alcista fuerte</div>
    <div class="card"><b style="color:var(--red)">Roja sin mecha superior</b>Impulso bajista fuerte</div>
    <div class="card"><b>Cuerpo pequeño con mechas largas</b>Indecisión: el impulso pierde fuerza</div>
    <div class="card"><b style="color:var(--accent)">Cambio de color</b>Posible giro del impulso, que se confirma si siguen velas del nuevo color</div>
  </div>'''))

S.append(slide(5, f'''  <span class="eyebrow">En la v0.8.1 · Confirmación de entrada</span>
  <h2>Tu setup señala; <span>Heikin Ashi confirma.</span></h2>
  {svg('confirmacion')}
  <div class="checks">
    <div class="check"><i>1</i><span><b>El setup da la señal</b> con tus reglas de siempre</span></div>
    <div class="check"><i>2</i><span><b>Heikin Ashi cambia de color</b> en la dirección de la señal</span></div>
    <div class="check"><i>3</i><span><b>N velas seguidas</b> en esa dirección (aquí, 3) → entrada</span></div>
  </div>''', '<span>Datos simulados con fines ilustrativos</span><b>quantpowerbuilder.com</b>'))

S.append(slide(6, '''  <span class="eyebrow">Qué podrás hacer</span>
  <h2>Entra cuando el impulso <span>ya va contigo.</span></h2>
  <div class="cards two">
    <div class="card"><b>Confirma cualquier setup</b>Se suma a las condiciones que ya tienes</div>
    <div class="card"><b>Tú eliges N</b>Cuántas velas seguidas exiges para entrar</div>
    <div class="card"><b>Largos y cortos</b>Velas verdes para comprar, rojas para vender</div>
    <div class="card"><b>Menos entradas a contrapié</b>Esperas a que el impulso gire antes de entrar</div>
  </div>
  <p class="lead">El precio confirma antes de que arriesgues: <b>más velas seguidas, más confirmación</b>, a cambio de entrar algo más tarde.</p>
  <div class="button">quantpowerbuilder.com</div>''', '<span>Últimas licencias gratis de por vida</span><b>v0.8.1</b>'))

guion = base[base.index('<script>'):]
open('publicacion.html', 'w').write(cab + '<body>\n\n' + '\n'.join(S) + '\n' + guion)
print('ok', len(S))
