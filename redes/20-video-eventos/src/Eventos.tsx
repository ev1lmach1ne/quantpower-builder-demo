import React from 'react';
import {AbsoluteFill, Easing, Img, Sequence, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';

// Vídeo sin voz sobre Analizador → Eventos (v0.8) con las capturas reales de la app (ES 1 min, 2010–2026).
// Zona segura de TikTok: ~360 px arriba, ~340 abajo y ~150 a la derecha.
export const FPS = 30;
const C = {bg: '#111828', deep: '#0d1424', panel: '#141e30', border: '#253a60', text: '#c8d6e5', strong: '#e6edf3',
  muted: '#9aaec7', accent: '#4fc3f7', green: '#2ecc71', red: '#e74c3c', amber: '#f1c40f'};
const FONT = 'Inter, "Segoe UI", Arial, sans-serif';

// Ventana donde se ve la captura (coordenadas del lienzo de 1080×1920)
const VW = {x: 60, y: 510, w: 870, h: 700};

type Zona = {x: number; y: number; w: number; h: number};
type Paso = {desde: number; zona: Zona; rotulo: React.ReactNode; marca?: Zona; color?: string};
type Escena = {img: string; iw: number; ih: number; titulo: string; pasos: Paso[]; dur: number};

const camara = (z: Zona) => {
  const s = Math.min(VW.w / z.w, VW.h / z.h);
  return {s, tx: VW.w / 2 - (z.x + z.w / 2) * s, ty: VW.h / 2 - (z.y + z.h / 2) * s};
};

const Fondo: React.FC = () => (
  <AbsoluteFill style={{background: `radial-gradient(900px 700px at 90% 15%, rgba(79,195,247,.16), transparent 60%), linear-gradient(180deg, ${C.bg}, ${C.deep})`}}>
    <AbsoluteFill style={{backgroundImage: 'linear-gradient(rgba(37,58,96,.28) 1px, transparent 1px), linear-gradient(90deg, rgba(37,58,96,.28) 1px, transparent 1px)', backgroundSize: '54px 54px', maskImage: 'linear-gradient(200deg, #000 0%, transparent 55%)'}} />
  </AbsoluteFill>
);

const Cabecera: React.FC<{titulo: string}> = ({titulo}) => (
  <div style={{position: 'absolute', left: 60, right: 150, top: 370, display: 'flex', alignItems: 'center', gap: 18, fontFamily: FONT}}>
    <Img src={staticFile('logo.png')} style={{width: 66, height: 66, borderRadius: '50%'}} />
    <div>
      <div style={{fontSize: 30, fontWeight: 700, color: C.strong}}>QuantPower Builder</div>
      <div style={{fontSize: 22, color: C.accent, fontWeight: 700, letterSpacing: '.08em', textTransform: 'uppercase'}}>{titulo}</div>
    </div>
  </div>
);

const Rotulo: React.FC<{children: React.ReactNode; inicio: number}> = ({children, inicio}) => {
  const f = useCurrentFrame();
  const o = interpolate(f - inicio, [0, 10], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const y = interpolate(f - inicio, [0, 12], [30, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: Easing.out(Easing.cubic)});
  return (
    <div style={{position: 'absolute', left: 60, width: 870, top: 1255, opacity: o, transform: `translateY(${y}px)`, fontFamily: FONT,
      padding: '28px 32px', borderRadius: 26, border: `2px solid ${C.border}`, background: 'rgba(20,30,48,.92)', color: C.text, fontSize: 40, lineHeight: 1.3}}>
      {children}
    </div>
  );
};

const B: React.FC<{c?: string; children: React.ReactNode}> = ({c = C.accent, children}) => <b style={{color: c, fontWeight: 800}}>{children}</b>;

const EscenaCaptura: React.FC<{e: Escena}> = ({e}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const entrada = spring({frame: f, fps, config: {damping: 18}});
  // cámara: se interpola entre las zonas de los pasos
  const ks = e.pasos.map((p) => camara(p.zona));
  const ts = e.pasos.map((p) => p.desde);
  const val = (k: 's' | 'tx' | 'ty') => {
    if (ks.length === 1) return ks[0][k];
    const inp: number[] = []; const out: number[] = [];
    ks.forEach((c, i) => { if (i > 0) { inp.push(ts[i]); out.push(ks[i - 1][k]); inp.push(ts[i] + 18); out.push(c[k]); } else { inp.push(0); out.push(c[k]); } });
    return interpolate(f, inp, out, {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: Easing.inOut(Easing.cubic)});
  };
  const s = val('s'), tx = val('tx'), ty = val('ty');
  const actual = [...e.pasos].reverse().find((p) => f >= p.desde) ?? e.pasos[0];
  const iActual = e.pasos.indexOf(actual);
  const marcaO = interpolate(f - actual.desde, [18, 28], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const salida = interpolate(f, [e.dur - 10, e.dur], [1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  return (
    <AbsoluteFill style={{opacity: salida}}>
      <Cabecera titulo={e.titulo} />
      <div style={{position: 'absolute', left: VW.x, top: VW.y - 20, width: VW.w, height: VW.h + 40, borderRadius: 26, overflow: 'hidden',
        border: `2px solid ${C.border}`, background: '#0b1220', boxShadow: '0 30px 80px rgba(0,0,0,.55)',
        transform: `translateY(${(1 - entrada) * 120}px) scale(${0.94 + entrada * 0.06})`, opacity: entrada}}>
        <div style={{position: 'absolute', left: 0, top: 20, width: e.iw, height: e.ih, transformOrigin: '0 0', transform: `translate(${tx}px, ${ty}px) scale(${s})`}}>
          <Img src={staticFile(e.img)} style={{width: e.iw, height: e.ih, display: 'block'}} />
          {actual.marca && (
            <div style={{position: 'absolute', left: actual.marca.x, top: actual.marca.y, width: actual.marca.w, height: actual.marca.h, opacity: marcaO,
              border: `${3 / s}px solid ${actual.color ?? C.amber}`, borderRadius: 6 / s, boxShadow: `0 0 ${18 / s}px ${actual.color ?? C.amber}`, background: 'rgba(241,196,15,.08)'}} />
          )}
        </div>
        <div style={{position: 'absolute', right: 18, top: 16, padding: '6px 14px', borderRadius: 8, background: C.amber, color: C.deep, fontFamily: FONT, fontWeight: 800, fontSize: 20, letterSpacing: '.1em'}}>BETA</div>
      </div>
      <Rotulo key={iActual} inicio={actual.desde + 6}>{actual.rotulo}</Rotulo>
    </AbsoluteFill>
  );
};

const GAPS: Escena = {img: 'gaps.png', iw: 1410, ih: 829, titulo: 'Eventos · Gaps', dur: 330, pasos: [
  {desde: 0, zona: {x: 0, y: 0, w: 1410, h: 829}, rotulo: <>Si el ES abre con <B>gap alcista</B>, ¿vuelve al cierre de ayer?</>},
  {desde: 75, zona: {x: 15, y: 250, w: 300, h: 240}, marca: {x: 26, y: 362, w: 272, h: 100},
    rotulo: <>Filtro: gap <B>alcista</B> de al menos <B>0,25 %</B>. Histórico 2010–2026 en velas de 5 min.</>},
  {desde: 160, zona: {x: 312, y: 305, w: 668, h: 175}, marca: {x: 318, y: 380, w: 656, h: 28},
    rotulo: <>Solo lo cierra el <B c={C.amber}>50,5 %</B> de las veces, frente al <B>94,5 %</B> de un día cualquiera (p &lt; 0,001).</>},
  {desde: 245, zona: {x: 312, y: 488, w: 668, h: 280}, marca: {x: 318, y: 612, w: 656, h: 28}, color: C.green,
    rotulo: <>Y el <B c={C.green}>57,1 %</B> de las sesiones termina por encima de la apertura.</>},
]};

const IB: Escena = {img: 'ib.png', iw: 1430, ih: 840, titulo: 'Eventos · Initial Balance', dur: 300, pasos: [
  {desde: 0, zona: {x: 0, y: 0, w: 1430, h: 840}, rotulo: <>Al cerrar la primera hora de Nueva York (<B>IB de 60 min</B>)…</>},
  {desde: 70, zona: {x: 22, y: 265, w: 300, h: 270}, marca: {x: 36, y: 286, w: 262, h: 30},
    rotulo: <>Sesión de <B>Nueva York</B>, IB de <B>60 min</B> y una hora para medir el primer toque.</>},
  {desde: 150, zona: {x: 322, y: 388, w: 600, h: 300}, marca: {x: 328, y: 420, w: 586, h: 52},
    rotulo: <>…¿qué toca antes? El máximo (<B c={C.amber}>IBH, 53,0 %</B>) o el mínimo (<B>IBL, 44,8 %</B>).</>},
  {desde: 235, zona: {x: 322, y: 388, w: 600, h: 300}, marca: {x: 328, y: 498, w: 586, h: 27}, color: C.accent,
    rotulo: <><B>Se queda en el rango</B> solo el 2,1 %. Calculado sobre <B>4.205 días</B>, con su IC del 95 %.</>},
]};

const PERFIL: Escena = {img: 'perfil.png', iw: 1447, ih: 841, titulo: 'Eventos · Perfil: dónde cierra', dur: 300, pasos: [
  {desde: 0, zona: {x: 0, y: 0, w: 1447, h: 841}, rotulo: <>Según la <B>forma del perfil de volumen</B>, ¿dónde cierra el periodo siguiente?</>},
  {desde: 70, zona: {x: 22, y: 265, w: 300, h: 260}, marca: {x: 34, y: 316, w: 272, h: 30},
    rotulo: <>Perfil de la <B>1.ª hora de Nueva York</B> con forma <B>D</B> → se mide la 2.ª hora.</>},
  {desde: 150, zona: {x: 320, y: 385, w: 866, h: 240}, marca: {x: 326, y: 470, w: 856, h: 27}, color: C.green,
    rotulo: <>La 2.ª hora cierra <B c={C.green}>sobre la VAH el 40,4 %</B>, frente al 33,8 % de base: <B c={C.green}>+6,6 pp</B>.</>},
  {desde: 230, zona: {x: 320, y: 385, w: 866, h: 240}, marca: {x: 326, y: 444, w: 856, h: 27}, color: C.red,
    rotulo: <>Y <B c={C.red}>dentro del área de valor</B> solo el 29,3 % (−6,9 pp). Ambas con p &lt; 0,001.</>},
]};

const Titular: React.FC<{dur: number; children: React.ReactNode; sub?: React.ReactNode; titulo: string}> = ({dur, children, sub, titulo}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const a = spring({frame: f, fps, config: {damping: 16}});
  const salida = interpolate(f, [dur - 10, dur], [1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  return (
    <AbsoluteFill style={{opacity: salida, fontFamily: FONT}}>
      <Cabecera titulo={titulo} />
      <div style={{position: 'absolute', left: 60, width: 870, top: 560, transform: `translateY(${(1 - a) * 60}px)`, opacity: a}}>
        {children}
      </div>
      {sub && <div style={{position: 'absolute', left: 60, width: 870, top: 1240, opacity: interpolate(f, [15, 30], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'})}}>{sub}</div>}
    </AbsoluteFill>
  );
};

const h1 = {fontSize: 92, lineHeight: 1.04, fontWeight: 800, letterSpacing: '-.03em', color: C.strong} as const;
const ficha = (t: React.ReactNode, i: number, f: number) => (
  <div key={i} style={{opacity: interpolate(f - 12 - i * 8, [0, 10], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}),
    padding: '22px 28px', borderRadius: 20, border: `2px solid ${C.border}`, background: 'rgba(26,42,69,.65)', fontSize: 36, color: C.text, marginBottom: 14}}>{t}</div>
);

const Intro: React.FC = () => (
  <Titular dur={95} titulo="Analizador · Eventos · v0.8"
    sub={<div style={{display: 'flex', gap: 14}}>{['ES', '1 min', '2010–2026'].map((t) => (
      <span key={t} style={{padding: '14px 26px', borderRadius: 999, border: `2px solid ${C.accent}`, background: 'rgba(79,195,247,.08)', fontSize: 34, fontWeight: 700, color: C.strong}}>{t}</span>))}</div>}>
    <div style={h1}>¿Qué pasa <span style={{color: C.accent}}>después de…?</span></div>
    <div style={{marginTop: 30, fontSize: 40, lineHeight: 1.35, color: C.muted}}>Un gap, el cierre del Initial Balance o la forma del perfil. <b style={{color: C.strong}}>Estadística real, no intuición.</b></div>
  </Titular>
);

const Leer: React.FC = () => {
  const f = useCurrentFrame();
  return (
    <Titular dur={125} titulo="Para leerlo bien">
      <div style={{...h1, fontSize: 76}}>Cada resultado, <span style={{color: C.accent}}>con su prueba.</span></div>
      <div style={{marginTop: 36}}>
        {[<><B>IC 95 %</B>: el margen de error de cada probabilidad</>, <><B>Base</B>: lo que pasa sin el evento, para comparar</>,
          <><B>p-valor</B>: si la diferencia es casualidad o no</>, <><B>IS / OOS</B>: dentro y fuera de muestra, para no engañarte</>].map((t, i) => ficha(t, i, f))}
      </div>
    </Titular>
  );
};

const Cierre: React.FC = () => (
  <Titular dur={125} titulo="Nuevo en la v0.8">
    <div style={{...h1, fontSize: 80}}>Analizador → <span style={{color: C.accent}}>Eventos.</span></div>
    <div style={{marginTop: 26, fontSize: 38, lineHeight: 1.35, color: C.muted}}>Gaps, Initial Balance, perfil de volumen, VWAP, patrones de vela… sobre tus propios datos.</div>
    <div style={{marginTop: 50, height: 110, borderRadius: 24, background: C.accent, color: C.deep, display: 'grid', placeItems: 'center', fontSize: 46, fontWeight: 800}}>quantpowerbuilder.com</div>
    <div style={{marginTop: 22, fontSize: 32, color: C.amber, fontWeight: 700, textAlign: 'center'}}>Últimas licencias gratis de por vida</div>
  </Titular>
);

const ESCENAS: [React.FC, number][] = [
  [Intro, 95], [() => <EscenaCaptura e={GAPS} />, GAPS.dur], [() => <EscenaCaptura e={IB} />, IB.dur],
  [() => <EscenaCaptura e={PERFIL} />, PERFIL.dur], [Leer, 125], [Cierre, 125],
];
export const DURACION = ESCENAS.reduce((a, [, d]) => a + d, 0);

export const Eventos: React.FC = () => {
  let t = 0;
  return (
    <AbsoluteFill>
      <Fondo />
      {ESCENAS.map(([Comp, d], i) => { const from = t; t += d; return <Sequence key={i} from={from} durationInFrames={d}><Comp /></Sequence>; })}
    </AbsoluteFill>
  );
};
