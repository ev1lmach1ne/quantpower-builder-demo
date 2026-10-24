"""Monta publicacion.html: 6 publicaciones sueltas sobre lo nuevo de la v0.8, una por tema.
Uso (desde redes/17-v08-por-temas): python3 scripts/montar.py
Reutiliza la cabecera y los estilos de ../15-ordenes-limite/publicacion.html. Todo el contenido sale de las
notas de la v0.8 (docs/releases/v0.8.md del programa); no se nombra a ningún proveedor de datos."""
import random, re

N = 6
base = open('../15-ordenes-limite/publicacion.html').read()
cab = base[:base.index('<body>')]
cab = cab.replace(cab[cab.index('<title>'):cab.index('</title>') + 8], '<title>Novedades de la v0.8 por temas — QuantPower Builder</title>')
cab = re.sub(r'<!--.*?-->', '''<!--
  Serie «Novedades de la v0.8 por temas»: 6 publicaciones sueltas. Se renderiza a PNG con redes/renderizar.sh.
  Parámetros: ?s=1…6 y ?f=vertical (1080×1350, por defecto) o ?f=tiktok (1080×1920).
  Generado con scripts/montar.py. Fuente: notas de la versión v0.8 del programa.
-->''', cab, count=1, flags=re.S)
cab = cab.replace('</style>', '''  .lista { display: grid; gap: 12px; }
  .it { display: grid; grid-template-columns: 56px 1fr; gap: 18px; align-items: center; padding: 16px 22px; border-radius: 16px;
    border: 1px solid var(--border); background: rgba(26,42,69,.6); font-size: 24px; line-height: 1.3; color: var(--text-muted); }
  .it b { display: block; color: var(--text-strong); font-size: 27px; margin-bottom: 2px; }
  .it i { display: grid; place-items: center; width: 56px; height: 56px; border-radius: 14px; font-style: normal; font-size: 28px;
    background: rgba(79,195,247,.14); color: var(--accent); }
  .tiktok .it { padding: 12px 18px; font-size: 21px; grid-template-columns: 48px 1fr; gap: 14px; }
  .tiktok .it b { font-size: 24px; }
  .tiktok .it i { width: 48px; height: 48px; font-size: 24px; }
  .vis { padding: 22px 26px; border-radius: 18px; border: 1px solid var(--border); background: rgba(20,30,48,.85); }
  .vis small { display: block; font-family: var(--mono); font-size: 19px; letter-spacing: .1em; text-transform: uppercase; color: var(--text-muted); margin-bottom: 12px; }
  .rango { position: relative; height: 14px; border-radius: 99px; background: var(--border); margin: 26px 18px 14px; }
  .rango span { position: absolute; left: 22%; right: 18%; top: 0; bottom: 0; border-radius: 99px; background: var(--accent); }
  .rango i { position: absolute; top: 50%; width: 34px; height: 34px; margin: -17px 0 0 -17px; border-radius: 50%; background: var(--text-strong); border: 5px solid var(--accent); }
  .fechas { display: flex; justify-content: space-between; font-family: var(--mono); font-size: 20px; color: var(--text-muted); }
  .fechas b { color: var(--text-strong); }
  .conex { display: flex; align-items: center; gap: 12px; font-size: 22px; color: var(--text); }
  .conex::before { content: ""; width: 16px; height: 16px; border-radius: 50%; background: var(--green); box-shadow: 0 0 0 7px rgba(46,204,113,.18); }
  .nucleos { display: grid; grid-template-columns: repeat(8, 1fr); gap: 10px; }
  .nucleos span { height: 74px; border-radius: 12px; background: linear-gradient(180deg, rgba(79,195,247,.95), rgba(79,195,247,.45)); display: grid; place-items: end center;
    padding-bottom: 8px; font-family: var(--mono); font-size: 18px; font-weight: 700; color: var(--bg-deep); }
  .antes { display: grid; grid-template-columns: 1fr 70px 1fr; align-items: center; gap: 10px; text-align: center; }
  .antes div { padding: 20px 10px; border-radius: 18px; border: 1px solid var(--border); background: rgba(26,42,69,.6); }
  .antes div.ya { border: 2px solid var(--green); background: rgba(46,204,113,.08); }
  .antes small { display: block; font-size: 20px; color: var(--text-muted); }
  .antes strong { display: block; font-size: 58px; font-weight: 800; letter-spacing: -.03em; color: var(--text-strong); }
  .antes .ya strong { color: var(--green); }
  .antes > span { font-size: 44px; color: var(--accent); }
  .tiktok .antes strong { font-size: 50px; }
  .perfil-mini { display: grid; grid-template-columns: 1fr 1.1fr; gap: 18px; align-items: center; }
  .perfil-mini svg { width: 100%; display: block; }
</style>''', 1)

def slide(n, cuerpo, pie='<span>Disponible en la v0.8</span><b>quantpowerbuilder.com</b>'):
    return f'''<section class="slide" data-s="{n}">
  <div class="grid"></div>
  <div class="top"><div class="logo"></div><strong>QuantPower Builder</strong><span class="count">Novedades v0.8 · {n}/{N}</span></div>
{cuerpo}
  <div class="foot">{pie}</div>
</section>
'''

def items(filas):
    return '  <div class="lista">\n' + ''.join(f'    <div class="it"><i>{i}</i><span><b>{t}</b>{d}</span></div>\n' for i, t, d in filas) + '  </div>'

def perfil_svg():
    """Perfil de volumen ilustrativo: dos montañas, PoC en rojo y área de valor sombreada."""
    random.seed(7); filas = 22; w, h = 420, 330
    vol = [60 * __import__('math').exp(-((k - 15) / 3.2) ** 2) + 38 * __import__('math').exp(-((k - 5) / 2.6) ** 2) + random.uniform(2, 6) for k in range(filas)]
    poc = max(range(filas), key=vol.__getitem__); tot = sum(vol); lo = hi = poc; acum = vol[poc]
    while acum < .7 * tot:
        a = vol[hi + 1] if hi + 1 < filas else -1; z = vol[lo - 1] if lo > 0 else -1
        if a >= z: hi += 1; acum += a
        else: lo -= 1; acum += z
    alto = h / filas; mx = max(vol); o = [f'<svg viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg">']
    y = lambda k: h - (k + 1) * alto
    o.append(f'<rect x="0" y="{y(hi):.1f}" width="{w}" height="{(hi - lo + 1) * alto:.1f}" fill="#9aaec7" opacity=".08" rx="6"/>')
    for k, v in enumerate(vol):
        col, op = ('#e74c3c', 1) if k == poc else ('#4fc3f7', .85 if lo <= k <= hi else .3)
        o.append(f'<rect x="0" y="{y(k) + 1.5:.1f}" width="{v / mx * (w - 90):.1f}" height="{alto - 3:.1f}" rx="3" fill="{col}" opacity="{op}"/>')
    for k, t, col in ((poc, 'PoC', '#e74c3c'), (hi, 'VAH', '#9aaec7'), (lo, 'VAL', '#9aaec7')):
        o.append(f'<text x="{w - 4}" y="{y(k) + alto / 2 + 8:.1f}" text-anchor="end" font-family="Inter, Segoe UI, Arial, sans-serif" font-size="22" font-weight="800" fill="{col}">{t}</text>')
    return ''.join(o) + '</svg>'

S = []
S.append(slide(1, '''  <span class="badge">Nuevo en la v0.8</span>
  <h2>Descargar datos, <span>más claro y más seguro.</span></h2>
  <div class="vis"><small>Elige el rango arrastrando</small>
    <div class="rango"><span></span><i style="left:22%"></i><i style="left:82%"></i></div>
    <div class="fechas"><span>Primera fecha real</span><b>Solo fechas con datos</b></div>
  </div>
''' + items([
    ('🌍', 'Proveedor nuevo', 'Acciones, ETFs, índices, divisas y cripto de más de 60 bolsas, con modo de prueba sin cuenta'),
    ('🔑', '«Probar conexión»', 'La clave de cada proveedor en un panel propio, con indicador de conexión'),
    ('⚠️', 'Sin descargas repetidas', 'Te avisa si ya tienes ese archivo, para no bajarlo (ni pagarlo) dos veces'),
    ('↻', 'Reanudar descargas', 'Si se cierra el programa o se va la luz, continúa donde se quedó'),
])))

S.append(slide(2, f'''  <span class="badge">Herramienta nueva</span>
  <h2>Perfil de volumen <span>en tus gráficos y reglas.</span></h2>
  <div class="vis perfil-mini">{perfil_svg()}
    <div class="lista" style="gap:10px">
      <div class="ley"><b style="color:var(--red)">PoC</b>El precio con más volumen</div>
      <div class="ley"><b style="color:var(--text)">Área de valor</b>Donde se concentra el 70 % del volumen</div>
      <div class="ley"><b style="color:var(--accent)">Nodos</b>Zonas de mucho y de poco volumen</div>
    </div>
  </div>
''' + items([
    ('⚙️', 'Configurable', 'Periodo (día, semana, mes…), resolución, ancho y perfil terminado, en formación o ambos'),
    ('🧩', 'En las reglas', 'Usa sus niveles en las condiciones de tus sistemas'),
    ('🚀', 'Dos sistemas listos', '«Ruptura de valor» y «Reversión de valor»'),
])))

S.append(slide(3, '''  <span class="badge">Optimizador</span>
  <h2>Prueba más parámetros, <span>en menos tiempo.</span></h2>
  <div class="vis"><small>Hasta 8 núcleos trabajando a la vez</small>
    <div class="nucleos">''' + ''.join(f'<span>{k}</span>' for k in range(1, 9)) + '''</div>
  </div>
''' + items([
    ('🔢', 'Los números de tus reglas', 'Periodos de indicadores, umbrales… no solo los de la plantilla'),
    ('👆', 'Perfiles de un clic', 'Configuraciones preparadas con rangos razonables para cada parámetro'),
    ('🚫', 'Combinaciones sin sentido, fuera', 'Por ejemplo, una media rápida más lenta que la lenta'),
])))

S.append(slide(4, '''  <span class="badge">Constructor y resultados</span>
  <h2>Construye y analiza <span>con menos fricción.</span></h2>
  <div class="pills"><span>Supertrend</span><span>CCI</span><span>Aroon</span><span>OBV</span></div>
''' + items([
    ('🗺️', 'Resumen visual del setup', 'El flujo de entradas, salidas y gestión, y aviso de lo que falta'),
    ('⌨️', 'Avanza con el teclado', 'Espacio o Enter para pasar por las tarjetas del constructor'),
    ('🔍', 'Modo gráfico en Resultados', 'Amplía el gráfico o sepáralo en su propia ventana'),
    ('🕘', 'Futuros en su horario regular', 'Initial Balance y TPO con la sesión regular de cada producto de CME'),
]), '<span>Indicadores nuevos en el catálogo</span><b>quantpowerbuilder.com</b>'))

S.append(slide(5, '''  <span class="badge">Rendimiento</span>
  <h2>Más rápido <span>y más fiable.</span></h2>
  <div class="antes">
    <div><small>Patrones de vela en 1 min · antes</small><strong>Horas</strong></div><span>→</span>
    <div class="ya"><small>Ahora</small><strong>~30 s</strong></div>
  </div>
''' + items([
    ('💾', 'Sin acumular GB de memoria', 'La detección de patrones en históricos largos ya no satura el equipo'),
    ('📊', 'Progreso real', 'Panel de actividad en Descargar, Importar y Análisis, con registro técnico'),
    ('✅', 'Backtests más correctos', 'Parciales al 100 % cierran la posición y un setup ya no cierra la operación de otro'),
    ('📉', 'Drawdowns bien calculados', 'También cuando la cuenta no llega a recuperarse'),
])))

S.append(slide(6, '''  <span class="badge">Cuenta y soporte</span>
  <h2>Hablamos contigo <span>dentro del programa.</span></h2>
''' + items([
    ('💬', 'Pestaña Soporte', 'Ves las respuestas del equipo a tus mensajes y contestas desde la app'),
    ('🐞', '«Solicitar un cambio o reportar un bug»', 'Elige el tipo: cambio, bug, indicador nuevo, sistema o estrategia, o consulta'),
    ('👤', 'Pestaña Cuenta', 'Tu correo, licencia, Discord y cierre de sesión, en Ajustes por secciones'),
    ('🔒', 'Cerrar sesión sin perder nada', 'Bloquea la pantalla; al volver a entrar conservas tu trabajo'),
]) + '''
  <div class="button">quantpowerbuilder.com</div>''', '<span>Últimas licencias gratis de por vida</span><b>v0.8</b>'))

guion = base[base.index('<script>'):]
open('publicacion.html', 'w').write(cab + '<body>\n\n' + '\n'.join(S) + '\n' + guion)
print('ok', len(S))
