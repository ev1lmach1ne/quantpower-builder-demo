"""Monta publicacion.html: cabecera y estilos comunes + 8 diapositivas con los SVG de graficos/ incrustados.
Uso (desde redes/15-ordenes-limite): python3 scripts/graficos.py && python3 scripts/montar.py
Las etiquetas entre «» son las del editor «④ Ejecución de la orden de entrada» de QuantPower Builder."""
import re

N = 8
html = open('publicacion.html').read()
cab = html[:html.index('<body>')]
cab = re.sub(r'<!--.*?-->', '''<!--
  Carrusel «5 formas de entrar con orden límite» (v0.8). Se renderiza a PNG con redes/renderizar.sh.
  Parámetros: ?s=1…8 y ?f=vertical (1080×1350, por defecto) o ?f=tiktok (1080×1920).
  Generado con scripts/montar.py; los gráficos (graficos/*.svg) son datos simulados de scripts/graficos.py.
  Fuente: editor de ejecución del programa (anclas de «Orden límite en», «Mientras la orden espera»,
  «Caducidad y cancelación» y «Ajuste sobre el ancla»).
-->''', cab, count=1, flags=re.S)
extra = '''  .tiles .tile.ancho { grid-column: span 2; }
  .ui { color: var(--text-strong); font-weight: 700; }
  .opts { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
  .opt { padding: 14px 18px; border-radius: 14px; border: 1px solid var(--border); background: rgba(26,42,69,.6); font-size: 21px; line-height: 1.3; color: var(--text-muted); }
  .opt b { display: block; font-size: 23px; color: var(--text-strong); margin-bottom: 4px; }
  .opt.sel { border: 2px solid var(--amber); background: rgba(241,196,15,.07); }
  .opt.sel b { color: var(--amber); }
  .tiktok .opt { font-size: 19px; padding: 12px 14px; }
  .tiktok .opt b { font-size: 21px; }
  .leyenda.tres { grid-template-columns: 1fr 1fr 1fr; }
  .costes { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
  .coste { padding: 14px 18px; border-radius: 14px; font-size: 21px; line-height: 1.3; color: var(--text-muted); }
  .coste b { display: block; font-size: 23px; margin-bottom: 4px; }
  .coste.lim { border: 2px solid rgba(46,204,113,.6); background: rgba(46,204,113,.07); }
  .coste.lim b { color: var(--green); }
  .coste.mer { border: 1px solid var(--border); background: rgba(26,42,69,.6); }
  .coste.mer b { color: var(--text-strong); }
  .tiktok .coste { font-size: 19px; padding: 12px 14px; }
  .tiktok .tile.ancho { padding: 14px 20px; }
  body:not(.tiktok) .slide[data-s="1"] .hero { font-size: 92px; }
  body:not(.tiktok) .slide[data-s="4"] .chart { width: 80%; align-self: center; }
  body:not(.tiktok) .slide[data-s="4"] .lead { font-size: 27px; }
</style>'''
cab = cab[:cab.index('  .tiles .tile.ancho')] + '</style>\n</head>\n' if '.tiles .tile.ancho' in cab else cab
if True:  # se puede volver a ejecutar sin duplicar estilos
    cab = cab.replace('</style>', extra, 1)
svg = lambda n: open(f'graficos/{n}.svg').read().replace('<svg ', '<svg class="chart" ', 1)

def slide(n, cuerpo, pie='<span>Datos simulados con fines ilustrativos</span><b>quantpowerbuilder.com</b>'):
    return f'''<section class="slide" data-s="{n}">
  <div class="grid"></div>
  <div class="top"><div class="logo"></div><strong>QuantPower Builder</strong><span class="count">Órdenes límite · {n}/{N}</span></div>
{cuerpo}
  <div class="foot">{pie}</div>
</section>
'''

def forma(k, titulo, lead, grafico, despues):
    return f'''  <span class="eyebrow">Forma {k} de 5 · «Orden límite en»</span>
  <h2 class="titulo"><span class="num">{k}</span>{titulo}</h2>
  <p class="lead">{lead}</p>
  {svg(grafico)}
{despues}'''

S = []
S.append(slide(1, '''  <span class="badge">Nuevo en la v0.8</span>
  <div class="hero">5 formas de entrar con <span>orden límite.</span></div>
  <p class="lead">En la ejecución de la entrada eliges <span class="ui">«A mercado»</span> u <span class="ui">«Orden límite»</span>. Con orden límite, la señal no compra al open: <b>deja la orden esperando en un nivel.</b></p>
  <div class="tiles">
    <div class="tile"><i>1</i><b>Un indicador de tus reglas</b><span>Media, banda…</span></div>
    <div class="tile"><i>2</i><b>Perfil de volumen</b><span>HVN, LVN, POC, VAH o VAL</span></div>
    <div class="tile"><i>3</i><b>Distancia en ATR</b><span>Desde el cierre de la señal</span></div>
    <div class="tile"><i>4</i><b>Vela de la señal</b><span>Low/high, 50 % o apertura</span></div>
    <div class="tile ancho"><i>5</i><b>Fibonacci del último tramo ZigZag</b><span>Retroceso del 23,6 % al 78,6 %</span></div>
  </div>''', '<span>Desliza para ver cada una</span><b>quantpowerbuilder.com</b>'))

S.append(slide(2, '''  <span class="eyebrow">Paso 1 · La confirmación</span>
  <h2>Primero, el setup tiene que <span>confirmarse.</span></h2>
  <p class="lead">Ejemplo de largo en el ES a 1 minuto. Varias variables a la vez, en modo <span class="ui">«Todas · AND»</span>:</p>
  <div class="checks">
    <div class="check"><i>✓</i><span><b>Tendencia:</b> cierre por encima de la EMA 200</span></div>
    <div class="check"><i>✓</i><span><b>Divergencia alcista</b> en el RSI, confirmada en el segundo mínimo</span></div>
    <div class="check"><i>✓</i><span><b>Filtro de volatilidad:</b> ATR dentro de su rango</span></div>
    <div class="check"><i>✓</i><span><b>Horario de sesión:</b> Nueva York</span></div>
  </div>
  <div class="valido">SETUP VÁLIDO → la orden límite espera su nivel</div>''',
  '<span>También «Cualquiera · OR». Sin código</span><b>quantpowerbuilder.com</b>'))

S.append(slide(3, forma(1, 'Un indicador de tus reglas',
  'La orden espera en un indicador de precio que ya usas en las reglas (una media, una banda…). Aquí, la <b>EMA 20</b> en modo <span class="ui">«Actualizado»</span>: la orden se mueve con la media.',
  'media', '''  <div class="cards two"><div class="card"><b>«Fijo» o «Actualizado»</b>Fijo: el valor al cierre de la señal. Actualizado: sigue al indicador</div><div class="card"><b>Sin indicador en las reglas</b>Te propone una EMA 20 como punto de partida</div></div>''')))

S.append(slide(4, forma(2, 'Un nodo del perfil de volumen',
  'El perfil del <b>último bloque cerrado</b> se lee así. Aquí la orden espera en el <b>LVN</b>, el hueco bajo el precio:',
  'perfil', '''  <div class="leyenda tres">
    <div class="ley"><b style="color:var(--red)">POC</b>El precio con más volumen</div>
    <div class="ley"><b style="color:var(--text)">VAH</b>Techo del área de valor</div>
    <div class="ley"><b style="color:var(--text)">VAL</b>Suelo del área de valor</div>
    <div class="ley"><b style="color:var(--accent)">HVN</b>Montaña destacada (hasta 2 por perfil)</div>
    <div class="ley"><b style="color:#b38af6">LVN</b>Hueco real entre dos montañas</div>
    <div class="ley"><b style="color:var(--amber)">Ventana</b>Bloques (15m, 1h, D…) o N velas</div>
  </div>
  <p class="lead">En largos el nodo debe quedar <b>por debajo del precio</b>; si no hay ninguno, la señal no entra.</p>''')))

S.append(slide(5, forma(3, 'Una distancia en ATR',
  'Compra a <b>k × ATR por debajo del cierre</b> de la vela de la señal (en ventas, por encima). Por defecto, <b>0,5 × ATR</b>.',
  'atr', '''  <div class="cards two"><div class="card"><b>Se adapta a la volatilidad</b>Mercado nervioso, orden más lejos; mercado tranquilo, más cerca</div><div class="card"><b>Nivel fijo</b>Se calcula una vez, al cierre de la vela de la señal</div></div>''')))

S.append(slide(6, forma(4, 'Un nivel de la vela de la señal',
  'La orden se coloca en un punto de la propia vela que dio la señal. Aquí, en el <b>50 %</b>:',
  'vela', '''  <div class="opts">
    <div class="opt"><b>Low / High</b>Low en largos, high en cortos</div>
    <div class="opt sel"><b>50 % de la vela</b>El punto medio del rango</div>
    <div class="opt"><b>Apertura de la vela</b>El open de la señal</div>
    <div class="opt"><b>+ Ajuste en ATR</b>Acerca o aleja la orden</div>
  </div>''')))

S.append(slide(7, forma(5, 'Fibonacci del último tramo ZigZag',
  'El ZigZag marca los pivotes y la orden espera en un retroceso del último tramo: <b>23,6 · 38,2 · 50 · 61,8 · 78,6 %</b>. Aquí, el 61,8 %.',
  'fibonacci', '''  <div class="cards two"><div class="card"><b>ZigZag ajustable</b>Desviación del 5 % y 10 velas entre pivotes, por defecto</div><div class="card"><b>Se cancela sola</b>Si el ZigZag confirma un tramo nuevo</div></div>''')))

S.append(slide(8, '''  <span class="eyebrow">Paso 3 · Mientras la orden espera</span>
  <h2>Tú decides cuánto <span>espera la orden.</span></h2>
  <div class="opts">
    <div class="opt"><b>«Fijo» o «Actualizado»</b>En indicador y perfil: nivel congelado o que se mueve con el ancla</div>
    <div class="opt"><b>«Caduca tras»</b>N velas sin ejecutarse (3 por defecto; o sin caducidad)</div>
    <div class="opt"><b>«Cancelar si avanza a favor»</b>1,5 R por defecto: el movimiento se fue sin ti</div>
    <div class="opt"><b>«Ajuste sobre el ancla»</b>± ATR: positivo la acerca al precio; negativo la aleja</div>
  </div>
  <div class="warn"><b>Reglas fijas:</b> la orden solo se coloca bajo el cierre en compras (sobre él en ventas), la señal contraria la cancela y hay una sola orden viva por setup.</div>
  <div class="costes">
    <div class="coste lim"><b>Orden límite</b>Sin slippage y comisión maker. Puede no ejecutarse</div>
    <div class="coste mer"><b>A mercado</b>Siempre entra, con slippage y comisión taker</div>
  </div>
  <div class="button">quantpowerbuilder.com</div>''', '<span>Últimas licencias gratis de por vida</span><b>v0.8</b>'))

guion = html[html.index('<script>'):]
open('publicacion.html', 'w').write(cab + '<body>\n\n' + '\n'.join(S) + '\n' + guion)
print('ok', len(S))
