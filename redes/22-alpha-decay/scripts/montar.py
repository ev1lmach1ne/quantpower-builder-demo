"""Monta publicacion.html: carrusel de 5 diapositivas del artículo «Alpha Decay» (sale el 28 oct a las 12:00).
Uso (desde redes/22-alpha-decay): python3 scripts/montar.py
Reutiliza la cabecera y los estilos de ../15-ordenes-limite/publicacion.html. Todo el contenido sale del artículo
articulos/alpha-decay-degradacion-ventaja/."""
import re

N = 5
base = open('../15-ordenes-limite/publicacion.html').read()
cab = base[:base.index('<body>')]
cab = cab.replace(cab[cab.index('<title>'):cab.index('</title>') + 8], '<title>Alpha Decay — QuantPower Builder</title>')
cab = re.sub(r'<!--.*?-->', '''<!--
  Carrusel «Alpha Decay» (artículo del 28 oct de 2026, 12:00). Se renderiza a PNG con redes/renderizar.sh.
  Parámetros: ?s=1…5 y ?f=vertical (1080×1350, por defecto) o ?f=tiktok (1080×1920).
  Generado con scripts/montar.py.
-->''', cab, count=1, flags=re.S)
cab = cab.replace('</style>', '''  .tabla { display: grid; gap: 10px; }
  .tf { display: grid; grid-template-columns: 1fr 44px 1fr; align-items: center; gap: 8px; }
  .tf div { padding: 14px 18px; border-radius: 14px; border: 1px solid var(--border); background: rgba(26,42,69,.6); font-size: 23px; line-height: 1.3; color: var(--text); }
  .tf div:last-child { border-color: rgba(79,195,247,.55); background: rgba(79,195,247,.07); color: var(--text-strong); font-weight: 700; }
  .tf span { text-align: center; font-size: 30px; color: var(--accent); }
  .tiktok .tf div { font-size: 20px; padding: 11px 14px; }
  .cifras { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }
  .cifra { padding: 26px 24px; border-radius: 20px; border: 2px solid var(--red); background: rgba(231,76,60,.07); }
  .cifra strong { display: block; font-size: 96px; font-weight: 800; letter-spacing: -.04em; color: var(--red); line-height: 1; }
  .cifra span { display: block; margin-top: 10px; font-size: 25px; line-height: 1.3; color: var(--text); }
  .tiktok .cifra strong { font-size: 80px; }
  .capas { display: grid; gap: 10px; }
  .capa { display: grid; grid-template-columns: 250px 1fr; align-items: center; gap: 18px; padding: 16px 22px; border-radius: 16px;
    border: 1px solid var(--border); background: rgba(26,42,69,.6); font-size: 22px; line-height: 1.3; color: var(--text-muted); }
  .capa b { font-size: 26px; color: var(--text-strong); }
  .capa:nth-child(1) { border-left: 6px solid var(--green); }
  .capa:nth-child(2) { border-left: 6px solid #b38af6; }
  .capa:nth-child(3) { border-left: 6px solid var(--accent); }
  .capa:nth-child(4) { border-left: 6px solid var(--amber); }
  .tiktok .capa { grid-template-columns: 200px 1fr; padding: 12px 16px; font-size: 20px; }
  .tiktok .capa b { font-size: 23px; }
  .hoy { display: flex; align-items: center; gap: 18px; padding: 18px 24px; border-radius: 18px; border: 2px solid var(--accent); background: rgba(79,195,247,.08); font-size: 30px; color: var(--text-strong); font-weight: 700; }
  .hoy strong { font-size: 48px; color: var(--accent); }
</style>''', 1)

def slide(n, cuerpo, pie='<span>Hoy, 12:00 · Artículos</span><b>quantpowerbuilder.com</b>'):
    return f'''<section class="slide" data-s="{n}">
  <div class="grid"></div>
  <div class="top"><div class="logo"></div><strong>QuantPower Builder</strong><span class="count">Alpha Decay · {n}/{N}</span></div>
{cuerpo}
  <div class="foot">{pie}</div>
</section>
'''

S = [
slide(1, '''  <span class="badge amber">Nuevo artículo · Hoy 12:00</span>
  <div class="hero">Alpha Decay: <span>tu ventaja también caduca.</span></div>
  <p class="lead">Una regla que funcionó durante años no viene con garantía para los veinte siguientes. Cambian los participantes, los costes y los entornos. <b>El reto no es adivinar el futuro: es detectar cuándo se erosiona la ventaja</b> y decidir qué capital merece seguir expuesto.</p>
  <div class="hoy"><strong>12:00</strong><span>Hoy, miércoles 28 de octubre</span></div>''', '<span>Desliza para ver un adelanto</span><b>quantpowerbuilder.com</b>'),
slide(2, '''  <span class="eyebrow">Qué se degrada exactamente</span>
  <h2>¿Mala racha o <span>ventaja perdida?</span></h2>
  <p class="lead">Una caída prolongada puede tener explicaciones distintas, y cada una pide una respuesta diferente:</p>
  <div class="tabla">
    <div class="tf"><div>Pérdidas dentro de lo que ya mostraban las simulaciones</div><span>→</span><div>Varianza normal o racha adversa</div></div>
    <div class="tf"><div>La rentabilidad bruta se mantiene, la neta cae</div><span>→</span><div>Más spread, slippage, impacto o rotación</div></div>
    <div class="tf"><div>La señal ordena peor los resultados que antes</div><span>→</span><div>La relación predictiva se debilita</div></div>
    <div class="tf"><div>La señal funciona, pero solo en algunos estados</div><span>→</span><div>Cambio de régimen o de capacidad</div></div>
  </div>'''),
slide(3, '''  <span class="eyebrow">El dato</span>
  <h2>Publicar una señal <span>también la desgasta.</span></h2>
  <p class="lead">McLean y Pontiff estudiaron <b>97 predictores</b> de retornos bursátiles. Los retornos de sus carteras fueron:</p>
  <div class="cifras">
    <div class="cifra"><strong>−26 %</strong><span>fuera de la muestra original</span></div>
    <div class="cifra"><strong>−58 %</strong><span>después de la publicación</span></div>
  </div>
  <div class="warn"><b>Ojo:</b> es un resultado sobre ese conjunto de predictores, no una vida útil universal. Sí es razón para tratar el alpha como una <b>hipótesis que necesita seguimiento</b>, no como una propiedad permanente.</div>''',
  '<span>McLean y Pontiff, The Journal of Finance, 2016</span><b>quantpowerbuilder.com</b>'),
slide(4, '''  <span class="eyebrow">La trampa de las reglas estáticas</span>
  <h2>15 o 20 años con <span>las mismas reglas.</span></h2>
  <div class="tabla">
    <div class="tf"><div>Especializar las reglas para el régimen reciente</div><span>→</span><div>Riesgo de ajustarse al ruido</div></div>
    <div class="tf"><div>Ampliar y filtrar para funcionar en todas partes</div><span>→</span><div>La ventaja se diluye y cae el Sharpe neto</div></div>
    <div class="tf"><div>No cambiar nada ni medir de nuevo</div><span>→</span><div>Riesgo asignado como si nada hubiera cambiado</div></div>
  </div>
  <p class="lead">La salida <b>no es reoptimizar cada vez que la curva baja:</b> eso convierte la volatilidad normal en una fábrica de parámetros nuevos.</p>'''),
slide(5, '''  <span class="eyebrow">Una arquitectura jerárquica</span>
  <h2>Separa qué operar <span>de cuánto arriesgar.</span></h2>
  <div class="capas">
    <div class="capa"><b>Ejecución</b>Cuándo entrar, salir o cancelar, y el tamaño operativo</div>
    <div class="capa"><b>Detección de entorno</b>Qué condiciones describe la información disponible, con su incertidumbre</div>
    <div class="capa"><b>Asignación de capital</b>Cuánto riesgo dar a cada estrategia, con límites</div>
    <div class="capa"><b>Supervisión</b>Si resultados y costes se alejan de lo validado</div>
  </div>
  <div class="button">Léelo hoy a las 12:00</div>''', '<span>Divulgativo · no es recomendación de inversión</span><b>quantpowerbuilder.com/articulos</b>'),
]
guion = base[base.index('<script>'):]
open('publicacion.html', 'w').write(cab + '<body>\n\n' + '\n'.join(S) + '\n' + guion)
print('ok', len(S))
