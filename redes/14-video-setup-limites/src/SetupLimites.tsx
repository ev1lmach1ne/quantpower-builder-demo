import {AbsoluteFill, Easing, Img, Sequence, interpolate, staticFile, useCurrentFrame} from 'remotion';
import {Audio} from '@remotion/media';
import mercado from './mercado.json';
import {ESCENAS, FPS, PAUSA, escena} from './tiempos';

// Paleta de los carteles de QuantPower Builder
const C = {
  bg: '#111828', bgDeep: '#0d1424', panel: '#141e30', border: '#253a60', borderSoft: '#202d44',
  text: '#c8d6e5', strong: '#e6edf3', muted: '#9aaec7', accent: '#4fc3f7', green: '#2ecc71',
  red: '#e74c3c', amber: '#f1c40f', purple: '#b38af6',
};
const FONT = 'Inter, "Segoe UI", Arial, sans-serif';
const MONO = '"DejaVu Sans Mono", Consolas, monospace';

// Geometría (1080×1920 con márgenes para la interfaz de TikTok: ~360 arriba, ~340 abajo, ~150 a la derecha)
const X0 = 80, X1 = 930;
const PY0 = 600, PY1 = 1130; // panel de precio
const RY0 = 1170, RY1 = 1330; // panel del RSI
const PMIN = 5279, PMAX = 5313;
const N = mercado.barras.length;
const PASO = (X1 - X0) / N;
const x = (i: number) => X0 + PASO * (i + 0.5);
const y = (p: number) => PY1 - ((p - PMIN) / (PMAX - PMIN)) * (PY1 - PY0);
const yr = (r: number) => RY1 - (r / 100) * (RY1 - RY0);
const fmt = (p: number) => p.toFixed(2).replace('.', ',');

const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;
const suave = Easing.bezier(0.16, 1, 0.3, 1);

// Progreso 0→1 dentro de una escena, entre dos fracciones de su duración
const prog = (frame: number, id: string, a = 0, b = 1) => {
  const e = escena(id);
  return interpolate(frame, [e.inicio + e.duracion * a, e.inicio + e.duracion * b], [0, 1], {...clamp, easing: suave});
};
const desde = (frame: number, id: string) => frame >= escena(id).inicio;

// Cuántas velas se ven en cada momento
const velasVisibles = (f: number) => {
  const tramos: [string, number, number, number][] = [
    ['mercado', 0, 31, 0.9], ['minimo1', 31, 37, 0.5], ['minimo2', 37, 56, 0.75],
    ['confirmacion', 56, 58, 0.3], ['perfil', 58, 65, 0.35], ['ejecucion', 65, N, 0.85],
  ];
  let v = 0;
  for (const [id, a, b, fin] of tramos) {
    if (desde(f, id)) v = interpolate(f, [escena(id).inicio, escena(id).inicio + escena(id).duracion * fin], [a, b], clamp);
  }
  return v;
};

const Cabecera = ({frame}: {frame: number}) => {
  const actual = [...ESCENAS].reverse().find((e) => frame >= e.inicio)!;
  return (
    <>
      <div style={{position: 'absolute', left: X0, top: 362, right: 150, display: 'flex', alignItems: 'center', gap: 18}}>
        <Img src={staticFile('logo.png')} style={{width: 64, height: 64, borderRadius: '50%', clipPath: 'circle(48%)', objectFit: 'cover'}} />
        <span style={{fontSize: 30, fontWeight: 700, color: C.strong}}>QuantPower Builder</span>
        <span style={{marginLeft: 'auto', padding: '6px 16px', borderRadius: 8, background: C.accent, color: C.bgDeep, fontSize: 22, fontWeight: 800, letterSpacing: '.1em'}}>v0.8</span>
      </div>
      <div
        key={actual.id}
        style={{
          position: 'absolute', left: X0, top: 452, right: 150, fontSize: 50, fontWeight: 800, letterSpacing: '-.02em', color: C.strong,
          opacity: interpolate(frame, [actual.inicio, actual.inicio + 12], [0, 1], clamp),
          translate: interpolate(frame, [actual.inicio, actual.inicio + 12], ['0px 18px', '0px 0px'], {...clamp, easing: suave}),
        }}
      >
        {actual.titulo}
      </div>
    </>
  );
};

const Velas = ({frame}: {frame: number}) => {
  const v = velasVisibles(frame);
  return (
    <g>
      {mercado.barras.map((b, i) => {
        if (i > v) return null;
        const op = Math.min(1, v - i + 0.4);
        const sube = b.c >= b.o;
        const col = sube ? C.green : C.red;
        const top = y(Math.max(b.o, b.c)), bot = y(Math.min(b.o, b.c));
        return (
          <g key={i} opacity={op}>
            <line x1={x(i)} x2={x(i)} y1={y(b.h)} y2={y(b.l)} stroke={col} strokeWidth={2} />
            <rect x={x(i) - PASO * 0.34} width={PASO * 0.68} y={top} height={Math.max(bot - top, 2)} fill={col} rx={1.5} />
          </g>
        );
      })}
    </g>
  );
};

const Rsi = ({frame}: {frame: number}) => {
  const v = velasVisibles(frame);
  const pts = mercado.rsi
    .map((r, i) => (r === null || i > v ? null : `${x(i).toFixed(1)},${yr(r).toFixed(1)}`))
    .filter(Boolean);
  return (
    <g>
      <rect x={X0} y={RY0} width={X1 - X0} height={RY1 - RY0} fill={C.panel} stroke={C.borderSoft} rx={10} />
      {[30, 70].map((l) => (
        <line key={l} x1={X0} x2={X1} y1={yr(l)} y2={yr(l)} stroke={C.border} strokeDasharray="6 6" />
      ))}
      <text x={X0 + 14} y={RY0 + 30} fill={C.muted} fontSize={22} fontFamily={MONO}>RSI 14</text>
      <text x={X1 - 12} y={yr(30) - 6} fill={C.muted} fontSize={18} textAnchor="end" fontFamily={MONO}>30</text>
      {pts.length > 1 && <polyline points={pts.join(' ')} fill="none" stroke={C.accent} strokeWidth={3} />}
    </g>
  );
};

const Perfil = ({frame}: {frame: number}) => {
  if (!desde(frame, 'perfil')) return null;
  const p = prog(frame, 'perfil', 0.3, 0.6);
  const resalta = prog(frame, 'perfil', 0.55, 0.75);
  const max = Math.max(...mercado.perfil.map((q) => q.vol));
  const alto = Math.abs(y(1) - y(0));
  return (
    <g>
      {mercado.perfil.map((q) => {
        const c = q.precio + 0.5;
        const esHvn = c === mercado.hvn || c === mercado.objetivo;
        const esLvn = c === mercado.lvn;
        const w = (q.vol / max) * 250 * p;
        const color = esHvn ? C.accent : esLvn ? C.purple : '#4fc3f7';
        const op = esHvn || esLvn ? interpolate(resalta, [0, 1], [0.22, 0.75]) : 0.18;
        return <rect key={q.precio} x={X1 - w} y={y(q.precio + 1) + 1} width={w} height={alto - 2} fill={color} opacity={op} rx={2} />;
      })}
      {[
        {p: mercado.objetivo, t: 'HVN', c: C.accent},
        {p: mercado.lvn, t: 'LVN', c: C.purple},
        {p: mercado.hvn, t: 'HVN', c: C.accent},
      ].map((n) => (
        <g key={n.p + n.t} opacity={resalta}>
          <rect x={X1 - 92} y={y(n.p) - 19} width={84} height={38} rx={8} fill={C.bgDeep} stroke={n.c} strokeWidth={2} />
          <text x={X1 - 50} y={y(n.p) + 8} fill={n.c} fontSize={22} fontWeight={800} textAnchor="middle" fontFamily={FONT}>{n.t}</text>
        </g>
      ))}
    </g>
  );
};

const Divergencia = ({frame}: {frame: number}) => {
  const {min1, min2} = mercado;
  const v = velasVisibles(frame);
  const m1 = desde(frame, 'minimo1') && v >= min1.barra + 1 ? 1 : 0;
  const linea = prog(frame, 'minimo2', 0.75, 0.95);
  const m2 = linea > 0 ? 1 : 0;
  const largoP = Math.hypot(x(min2.barra) - x(min1.barra), y(min2.precio) - y(min1.precio));
  const largoR = Math.hypot(x(min2.rsiBarra) - x(min1.rsiBarra), yr(min2.rsi) - yr(min1.rsi));
  const etiquetas = prog(frame, 'minimo2', 0.85, 1);
  return (
    <g>
      {m1 > 0 && (
        <g opacity={interpolate(frame, [escena('minimo1').inicio + escena('minimo1').duracion * 0.5, escena('minimo1').inicio + escena('minimo1').duracion * 0.65], [0, 1], clamp)}>
          <circle cx={x(min1.barra)} cy={y(min1.precio) + 14} r={11} fill="none" stroke={C.amber} strokeWidth={4} />
          <circle cx={x(min1.rsiBarra)} cy={yr(min1.rsi)} r={11} fill="none" stroke={C.amber} strokeWidth={4} />
          <text x={x(min1.barra)} y={y(min1.precio) + 56} fill={C.amber} fontSize={24} fontWeight={700} textAnchor="middle" fontFamily={FONT}>Mínimo 1</text>
        </g>
      )}
      {m2 > 0 && (
        <g>
          <circle cx={x(min2.barra)} cy={y(min2.precio) + 14} r={11} fill="none" stroke={C.amber} strokeWidth={4} />
          <circle cx={x(min2.rsiBarra)} cy={yr(min2.rsi)} r={11} fill="none" stroke={C.amber} strokeWidth={4} />
          <line x1={x(min1.barra)} y1={y(min1.precio) + 14} x2={x(min2.barra)} y2={y(min2.precio) + 14} stroke={C.red} strokeWidth={4}
            strokeDasharray={largoP} strokeDashoffset={largoP * (1 - linea)} />
          <line x1={x(min1.rsiBarra)} y1={yr(min1.rsi)} x2={x(min2.rsiBarra)} y2={yr(min2.rsi)} stroke={C.green} strokeWidth={4}
            strokeDasharray={largoR} strokeDashoffset={largoR * (1 - linea)} />
          <g opacity={etiquetas}>
            <text x={x(min2.barra)} y={y(min2.precio) + 56} fill={C.amber} fontSize={24} fontWeight={700} textAnchor="middle" fontFamily={FONT}>Mínimo 2</text>
            <text x={(x(min1.barra) + x(min2.barra)) / 2} y={y(min2.precio) + 92} fill={C.red} fontSize={22} fontWeight={700} textAnchor="middle" fontFamily={FONT}>precio: mínimo más bajo</text>
            <text x={(x(min1.rsiBarra) + x(min2.rsiBarra)) / 2} y={RY0 + 34} fill={C.green} fontSize={22} fontWeight={700} textAnchor="middle" fontFamily={FONT}>RSI: mínimo más alto</text>
          </g>
        </g>
      )}
    </g>
  );
};

const Confirmacion = ({frame}: {frame: number}) => {
  if (!desde(frame, 'confirmacion')) return null;
  const marca = prog(frame, 'confirmacion', 0.25, 0.35);
  const fuera = 1 - prog(frame, 'perfil', 0, 0.2);
  const items = ['Divergencia alcista en el RSI', 'Segundo mínimo confirmado', 'Volatilidad (ATR) en rango'];
  const valido = prog(frame, 'confirmacion', 0.82, 0.92);
  const c = mercado.confirmacion;
  return (
    <g opacity={fuera}>
      <rect x={x(c) - PASO * 0.6} y={PY0} width={PASO * 1.2} height={PY1 - PY0} fill={C.green} opacity={0.12 * marca} />
      <text x={x(c)} y={y(mercado.barras[c].h) - 18} fill={C.green} fontSize={22} fontWeight={800} textAnchor="middle" opacity={marca} fontFamily={FONT}>Confirmado</text>
      <g opacity={prog(frame, 'confirmacion', 0.3, 0.4)}>
        <rect x={600} y={640} width={325} height={250} rx={16} fill={C.bgDeep} stroke={C.border} strokeWidth={2} />
        {items.map((t, k) => {
          const ok = prog(frame, 'confirmacion', 0.4 + k * 0.13, 0.48 + k * 0.13);
          return (
            <g key={t} transform={`translate(620 ${690 + k * 58})`}>
              <circle cx={14} cy={-8} r={15} fill={ok > 0.5 ? C.green : 'none'} stroke={ok > 0.5 ? C.green : C.border} strokeWidth={3} />
              <text x={14} y={-1} fill={C.bgDeep} fontSize={20} fontWeight={900} textAnchor="middle" opacity={ok} fontFamily={FONT}>✓</text>
              <text x={40} y={-1} fill={ok > 0.5 ? C.strong : C.muted} fontSize={17} fontWeight={600} fontFamily={FONT}>{t}</text>
            </g>
          );
        })}
        <g opacity={valido}>
          <rect x={620} y={838} width={285} height={40} rx={10} fill={C.green} />
          <text x={762} y={866} fill={C.bgDeep} fontSize={22} fontWeight={900} textAnchor="middle" letterSpacing=".12em" fontFamily={FONT}>SETUP VÁLIDO</text>
        </g>
      </g>
    </g>
  );
};

const Ordenes = ({frame}: {frame: number}) => {
  if (!desde(frame, 'ordenes')) return null;
  const v = velasVisibles(frame);
  const xi = x(mercado.barraOrdenes) + PASO;
  // Primero se ofrecen los dos niveles candidatos; después se elige uno y ahí se marcan las órdenes límite
  const ofrece = prog(frame, 'ordenes', 0.12, 0.22);
  const elige = prog(frame, 'ordenes', 0.36, 0.46);
  const elegido = mercado.ordenes[0];
  const niveles = [
    ...mercado.ordenes.map((o) => ({
      p: o.precio, col: o.tipo === 'LVN' ? C.purple : C.accent, t0: 0.46,
      txt: `Compra límite · ${o.contratos} ct · ${fmt(o.precio)} (${o.tipo})`, lleno: o.barra !== null && v > o.barra,
    })),
    {p: mercado.stop, col: C.red, t0: 0.6, txt: `Stop · ${fmt(mercado.stop)}`, lleno: false},
    {p: mercado.objetivo, col: C.green, t0: 0.7, txt: `Objetivo · ${fmt(mercado.objetivo)} (HVN)`, lleno: false},
  ];
  const objetivo = mercado.barraObjetivo !== null && v > mercado.barraObjetivo;
  return (
    <g>
      {mercado.candidatos.map((c) => {
        const esElegido = c.tipo === elegido.tipo && c.precio === elegido.precio;
        const col = c.tipo === 'LVN' ? C.purple : C.accent;
        // El candidato no elegido se apaga; el elegido se convierte en la línea de la orden
        const op = ofrece * (esElegido ? 1 - prog(frame, 'ordenes', 0.46, 0.52) : 1 - 0.75 * elige);
        return (
          <g key={c.tipo} opacity={op}>
            <line x1={xi} x2={X1} y1={y(c.precio)} y2={y(c.precio)} stroke={col} strokeWidth={3} strokeDasharray="4 8" />
            <rect x={X0 + 6} y={y(c.precio) - 21} width={360} height={42} rx={9} fill={C.bgDeep} stroke={col} strokeWidth={esElegido ? 2 + 2 * elige : 2} opacity={0.9} />
            <text x={X0 + 20} y={y(c.precio) + 8} fill={col} fontSize={21} fontWeight={700} fontFamily={FONT}>
              {`Nivel ${c.tipo} · ${fmt(c.precio)}`}{esElegido && elige > 0.5 ? '  ← elegido' : ''}
            </text>
          </g>
        );
      })}
      {niveles.map((n) => {
        const a = prog(frame, 'ordenes', n.t0, n.t0 + 0.1);
        return (
          <g key={n.txt} opacity={a}>
            <line x1={xi} x2={X1} y1={y(n.p)} y2={y(n.p)} stroke={n.col} strokeWidth={n.lleno ? 4 : 3} strokeDasharray={n.lleno ? undefined : '10 8'} />
            <rect x={X0 + 6} y={y(n.p) - 21} width={n.lleno ? 545 : 420} height={42} rx={9} fill={C.bgDeep} stroke={n.col} strokeWidth={2} opacity={0.88} />
            <text x={X0 + 20} y={y(n.p) + 8} fill={n.col} fontSize={21} fontWeight={700} fontFamily={FONT}>
              {n.txt}{n.lleno ? '  ✓ ejecutada' : ''}
            </text>
          </g>
        );
      })}
      {objetivo && (
        <g>
          <rect x={590} y={y(mercado.objetivo) - 80} width={300} height={46} rx={10} fill={C.green} />
          <text x={740} y={y(mercado.objetivo) - 49} fill={C.bgDeep} fontSize={23} fontWeight={900} textAnchor="middle" fontFamily={FONT}>Objetivo alcanzado</text>
        </g>
      )}
    </g>
  );
};

const Grafico = ({frame}: {frame: number}) => {
  const entra = interpolate(frame, [0, 20], [0, 1], clamp);
  const cierre = prog(frame, 'cierre', 0, 0.15);
  const precios = [5280, 5290, 5300, 5310];
  return (
    <svg width={1080} height={1920} style={{position: 'absolute', inset: 0, opacity: entra * (1 - 0.92 * cierre) * (1 - prog(frame, 'articulo', 0, 0.15))}}>
      <rect x={X0} y={PY0 - 10} width={X1 - X0} height={PY1 - PY0 + 20} fill={C.panel} stroke={C.borderSoft} rx={12} />
      {precios.map((p) => (
        <g key={p}>
          <line x1={X0} x2={X1} y1={y(p)} y2={y(p)} stroke={C.borderSoft} />
          <text x={X0 + 10} y={y(p) - 8} fill={C.muted} fontSize={18} fontFamily={MONO} opacity={0.8}>{p}</text>
        </g>
      ))}
      <text x={X0 + 4} y={RY1 + 28} fill={C.muted} fontSize={18} fontFamily={FONT}>ES · 1 min · datos simulados con fines ilustrativos</text>
      <Perfil frame={frame} />
      <Velas frame={frame} />
      <Rsi frame={frame} />
      <Divergencia frame={frame} />
      <Confirmacion frame={frame} />
      <Ordenes frame={frame} />
    </svg>
  );
};

type Palabra = {w: string; t: number};

// Agrupa las palabras en páginas que quepan en el cuadro: se cierra página al acabar una frase,
// en una coma si ya va larga, o a la fuerza hacia los 120 caracteres
const paginar = (palabras: Palabra[]) => {
  const pags: number[][] = [];
  let actual: number[] = [];
  let largo = 0;
  palabras.forEach((p, i) => {
    actual.push(i);
    largo += p.w.length + 1;
    const fin = /[.?!]$/.test(p.w);
    const coma = /,$/.test(p.w);
    if ((fin && largo >= 60) || (coma && largo >= 95) || largo >= 120) {
      pags.push(actual);
      actual = [];
      largo = 0;
    }
  });
  if (actual.length) pags.push(actual);
  return pags;
};

// Subtítulo: cada palabra se ilumina cuando suena (tiempos de la transcripción) y el texto pasa por páginas.
// Si la escena no trae tiempos por palabra, se reparten a lo largo de la frase.
const Subtitulo = ({frame}: {frame: number}) => {
  const e = [...ESCENAS].reverse().find((s) => frame >= s.inicio)!;
  if (!e.texto) return null;
  const habla = (e.duracion - PAUSA * FPS - (e.id === 'cierre' ? 45 : 0)) / FPS;
  const lista: Palabra[] = e.palabras ?? e.texto.split(' ').map((w, i, arr) => ({w, t: (i / arr.length) * habla}));
  const seg = (frame - e.inicio) / FPS;
  const k = lista.filter((p) => p.t <= seg + 0.04).length;
  const pags = paginar(lista);
  const activa = pags.find((pg) => pg.includes(Math.max(0, k - 1))) ?? pags[0];
  const pagina = activa.map((i) => lista[i].w).join(' ');
  return (
    <div
      style={{
        // Anclado abajo y con letra según la longitud, para que el texto no se salga del cuadro ni de la zona segura
        position: 'absolute', left: X0, right: 150, top: 1372, minHeight: 200, maxHeight: 208, boxSizing: 'border-box',
        padding: '18px 24px', borderRadius: 18, overflow: 'hidden',
        background: 'rgba(13,20,36,.88)', border: `1px solid ${C.border}`, fontSize: pagina.length > 140 ? 29 : 33, lineHeight: 1.3, fontWeight: 600,
        opacity: interpolate(frame, [e.inicio, e.inicio + 8], [0, 1], clamp),
      }}
    >
      {activa.map((i) => (
        <span key={i} style={{color: i < k ? C.strong : 'rgba(154,174,199,.55)'}}>{lista[i].w} </span>
      ))}
    </div>
  );
};

const Cierre = ({frame}: {frame: number}) => {
  if (!desde(frame, 'cierre')) return null;
  const a = prog(frame, 'cierre', 0.05, 0.25) * (1 - prog(frame, 'articulo', 0, 0.12));
  if (a <= 0 && desde(frame, 'articulo')) return null;
  const puntos = ['Divergencias solo cuando se confirman', 'Perfil de volumen con HVN y LVN', 'Órdenes límite en el nivel que elijas'];
  return (
    <div style={{position: 'absolute', left: X0, right: 150, top: 610, opacity: a, translate: interpolate(a, [0, 1], ['0px 40px', '0px 0px'])}}>
      <div style={{display: 'inline-block', padding: '10px 22px', borderRadius: 8, background: C.accent, color: C.bgDeep, fontSize: 24, fontWeight: 800, letterSpacing: '.14em'}}>NUEVO EN LA V0.8</div>
      <div style={{marginTop: 22, fontSize: 70, lineHeight: 1.05, fontWeight: 800, letterSpacing: '-.03em', color: C.strong}}>
        Del setup a <span style={{color: C.accent}}>tu nivel de entrada.</span>
      </div>
      <div style={{marginTop: 30, display: 'grid', gap: 14}}>
        {puntos.map((t, k) => (
          <div key={t} style={{
            display: 'flex', alignItems: 'center', gap: 18, padding: '18px 22px', borderRadius: 16, border: `1px solid ${C.border}`,
            background: 'rgba(26,42,69,.75)', fontSize: 30, color: C.strong, fontWeight: 600,
            opacity: prog(frame, 'cierre', 0.2 + k * 0.08, 0.3 + k * 0.08),
          }}>
            <span style={{width: 44, height: 44, borderRadius: '50%', background: C.green, color: C.bgDeep, display: 'grid', placeItems: 'center', fontWeight: 900}}>✓</span>
            {t}
          </div>
        ))}
      </div>
      <div style={{marginTop: 30, padding: '24px 0', borderRadius: 20, background: C.accent, color: C.bgDeep, textAlign: 'center', fontSize: 40, fontWeight: 800, opacity: prog(frame, 'cierre', 0.45, 0.55)}}>
        quantpowerbuilder.com
      </div>
      <div style={{marginTop: 16, textAlign: 'center', fontSize: 26, fontWeight: 700, color: C.amber, opacity: prog(frame, 'cierre', 0.55, 0.65)}}>
        Últimas licencias gratis de por vida
      </div>
    </div>
  );
};

// Escena final: portada del artículo publicado hoy, dentro de un marco de móvil
const Articulo = ({frame}: {frame: number}) => {
  if (!desde(frame, 'articulo')) return null;
  const a = prog(frame, 'articulo', 0, 0.25);
  const W = 600, H = Math.round((W * 1400) / 1080);
  return (
    <div style={{position: 'absolute', left: X0, right: 150, top: 540, opacity: a, display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 26}}>
      <div style={{padding: '10px 22px', borderRadius: 8, background: C.accent, color: C.bgDeep, fontSize: 24, fontWeight: 800, letterSpacing: '.14em'}}>NUEVO ARTÍCULO · YA EN LA WEB</div>
      <div style={{
        width: W + 24, padding: 12, borderRadius: 36, background: '#0a1020', border: `2px solid ${C.border}`,
        boxShadow: '0 30px 80px rgba(0,0,0,.55), 0 0 0 1px rgba(79,195,247,.15)', transformOrigin: 'top center',
        translate: interpolate(a, [0, 1], ['0px 80px', '0px 0px']),
        scale: interpolate(frame, [escena('articulo').inicio, escena('articulo').inicio + escena('articulo').duracion], [0.96, 1.02], clamp),
      }}>
        <Img src={staticFile('articulo-portada.png')} style={{display: 'block', width: W, height: H, borderRadius: 26, objectFit: 'cover', objectPosition: 'top'}} />
      </div>
      <div style={{textAlign: 'center', fontSize: 30, fontWeight: 800, color: C.strong, lineHeight: 1.25, opacity: prog(frame, 'articulo', 0.25, 0.45)}}>
        Level 1, Level 2 y Level 3: qué datos ofrece el mercado
      </div>
      <div style={{fontSize: 30, fontWeight: 700, color: C.accent, opacity: prog(frame, 'articulo', 0.35, 0.55)}}>quantpowerbuilder.com/articulos</div>
    </div>
  );
};

export const SetupLimites = () => {
  const frame = useCurrentFrame();
  return (
    <AbsoluteFill style={{fontFamily: FONT, background: `radial-gradient(900px 700px at 90% 20%, rgba(79,195,247,.12), transparent 60%), linear-gradient(180deg, ${C.bg} 0%, ${C.bgDeep} 100%)`}}>
      <Grafico frame={frame} />
      <Cabecera frame={frame} />
      <Cierre frame={frame} />
      <Articulo frame={frame} />
      <Subtitulo frame={frame} />
      {ESCENAS.filter((e) => e.audio).map((e) => (
        <Sequence key={e.id} name={`Voz · ${e.id}`} from={e.inicio} durationInFrames={e.duracion}>
          <Audio src={staticFile(e.audio)} />
        </Sequence>
      ))}
    </AbsoluteFill>
  );
};
