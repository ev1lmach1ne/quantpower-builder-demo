import { selectButtons, wireTabs } from "./ui.js";

const NS = "http://www.w3.org/2000/svg";
const colors = { text: "#9aaec7", grid: "#253a60", accent: "#4fc3f7", green: "#2ecc71", red: "#e74c3c" };
const percentage = new Intl.NumberFormat("es-ES", { minimumFractionDigits: 3, maximumFractionDigits: 3, signDisplay: "always" });
const number = new Intl.NumberFormat("es-ES");
const format = (value) => `${percentage.format(value)} %`;
const L = 82, R = 1008, TOP = 72, BOTTOM = 326, LOWER_TOP = 420, LOWER_BOTTOM = 534;

function node(tag, attributes = {}, content) {
  const element = document.createElementNS(NS, tag);
  for (const [key, value] of Object.entries(attributes)) element.setAttribute(key, value);
  if (content !== undefined) element.textContent = content;
  return element;
}

function text(x, y, content, attributes = {}) {
  return node("text", { x, y, fill: colors.text, "font-size": 11, "font-family": "Segoe UI,Arial,sans-serif", ...attributes }, content);
}

export async function initAnalyzer() {
  const buttons = [...document.querySelectorAll("[data-analysis-period]")];
  const root = document.getElementById("analysis-chart");
  const from = document.getElementById("analysis-from");
  const to = document.getElementById("analysis-to");
  let data;
  let period = "dia";
  let curve;
  let svg;
  let overlays;
  let current = 0;
  let range = null;
  let dragStart = null;
  let yScale;
  let stepScale;
  const x = (index) => L + index * (R - L) / (curve.x.length - 1);

  const summarize = () => {
    document.getElementById("analysis-point").textContent = curve.labels[current];
    document.getElementById("analysis-point-total").textContent = format(curve.y[current]);
    document.getElementById("analysis-point-step").textContent = format(curve.steps[current]);
    const summary = document.getElementById("analysis-range-result");
    if (range) {
      const delta = curve.y[range[1]] - curve.y[range[0]];
      summary.textContent = `${curve.labels[range[0]]} → ${curve.labels[range[1]]}: ${percentage.format(delta)} p.p. de cambio en la curva acumulada.`;
    } else summary.textContent = "Arrastra sobre el gráfico o elige Inicio y Fin para medir un tramo.";
  };

  const drawOverlay = () => {
    overlays.replaceChildren();
    if (range) {
      const start = x(range[0]), end = x(range[1]);
      overlays.append(node("rect", { x: start, y: TOP, width: Math.max(1, end - start), height: LOWER_BOTTOM - TOP, fill: colors.accent, opacity: .065 }));
      for (const xx of [start, end]) overlays.append(node("path", { d: `M${xx} ${TOP}V${LOWER_BOTTOM}`, stroke: colors.accent, "stroke-width": 1.1, opacity: .65 }));
    }
    const xx = x(current), yy = yScale(curve.y[current]), sy = stepScale(curve.steps[current]);
    overlays.append(node("path", { d: `M${xx} ${TOP}V${LOWER_BOTTOM}`, stroke: colors.accent, "stroke-dasharray": "4 4", opacity: .9 }));
    overlays.append(node("path", { d: `M${L} ${yy}H${R}`, stroke: colors.accent, "stroke-dasharray": "3 5", opacity: .4 }));
    overlays.append(node("circle", { cx: xx, cy: yy, r: 5, fill: "#0d1424", stroke: colors.accent, "stroke-width": 2 }));
    overlays.append(node("circle", { cx: xx, cy: sy, r: 3.5, fill: colors.accent }));
    const labelX = Math.max(L + 6, Math.min(R - 190, xx + 13));
    overlays.append(node("rect", { x: labelX, y: TOP + 6, width: 184, height: 56, rx: 5, fill: "#1a2a45", stroke: colors.grid }));
    overlays.append(text(labelX + 10, TOP + 24, `${curve.labels[current]} · ${format(curve.y[current])}`, { fill: "#e6edf3", "font-size": 12 }));
    overlays.append(text(labelX + 10, TOP + 46, `Paso: ${format(curve.steps[current])}`, { "font-size": 10 }));
    summarize();
  };

  const setRange = (start, end) => {
    range = [Math.min(start, end), Math.max(start, end)];
    from.value = range[0];
    to.value = range[1];
    drawOverlay();
  };

  const indexAt = (event) => {
    const point = svg.createSVGPoint();
    point.x = event.clientX;
    point.y = event.clientY;
    const local = point.matrixTransform(svg.getScreenCTM().inverse());
    return Math.max(0, Math.min(curve.x.length - 1, Math.round((local.x - L) / (R - L) * (curve.x.length - 1))));
  };

  const render = () => {
    if (!data) return;
    curve = data.curves[period];
    current = Math.min(12, curve.x.length - 1);
    range = null;
    dragStart = null;
    const selected = buttons.find((button) => button.dataset.analysisPeriod === period);
    selectButtons(buttons, selected, "aria-selected");
    document.getElementById("analysis-panel").setAttribute("aria-labelledby", selected.id);
    document.getElementById("analysis-panel").dataset.period = period;
    document.getElementById("analysis-title").textContent = `Cambio acumulado medio — ${curve.title}`;
    document.getElementById("analysis-count").textContent = `${number.format(curve.count)} periodos completos`;
    document.getElementById("analysis-total").textContent = format(curve.total);
    document.getElementById("analysis-total").className = curve.total >= 0 ? "positive" : "negative";
    document.getElementById("analysis-sample").textContent = `${number.format(data.barCount)} velas · 2018–2023 · H1 · UTC`;
    document.getElementById("analysis-open").href = new URL(`../images/${curve.image}`, import.meta.url).href;
    for (const select of [from, to]) {
      select.replaceChildren(...curve.labels.map((label, index) => new Option(label, index)));
    }
    to.value = curve.x.length - 1;
    const low = Math.min(0, ...curve.y), high = Math.max(0, ...curve.y);
    const pad = Math.max((high - low) * .16, .002);
    yScale = (value) => BOTTOM - (value - low + pad) / (high - low + 2 * pad) * (BOTTOM - TOP);
    const extent = Math.max(...curve.steps.map(Math.abs), .001) * 1.2;
    stepScale = (value) => (LOWER_TOP + LOWER_BOTTOM) / 2 - value / extent * (LOWER_BOTTOM - LOWER_TOP) / 2;
    if (!svg) {
      svg = node("svg", { viewBox: "0 0 1100 580", role: "img", tabindex: 0, "aria-describedby": "analysis-help" });
      svg.addEventListener("pointermove", (event) => {
        current = indexAt(event);
        if (dragStart !== null) setRange(dragStart, current);
        else drawOverlay();
      });
      svg.addEventListener("pointerdown", (event) => {
        if (!event.isPrimary || event.button !== 0) return;
        current = indexAt(event);
        dragStart = current;
        svg.setPointerCapture(event.pointerId);
        svg.focus({ preventScroll: true });
        drawOverlay();
      });
      const endDrag = () => {
        if (dragStart !== null && dragStart !== current) setRange(dragStart, current);
        dragStart = null;
      };
      svg.addEventListener("pointerup", endDrag);
      svg.addEventListener("pointercancel", () => { dragStart = null; });
      svg.addEventListener("keydown", (event) => {
        if (event.key === "Escape") { range = null; drawOverlay(); return; }
        const next = { ArrowLeft: current - 1, ArrowRight: current + 1, Home: 0, End: curve.x.length - 1 }[event.key];
        if (next === undefined) return;
        event.preventDefault();
        current = Math.min(curve.x.length - 1, Math.max(0, next));
        drawOverlay();
      });
      root.replaceChildren(svg);
    }
    svg.setAttribute("aria-label", `${curve.title}: cambio acumulado medio y cambio medio por paso, ${curve.count} periodos de datos sintéticos.`);
    svg.replaceChildren(node("title", {}, `Cambio acumulado medio — ${curve.title}`));
    const shapes = node("g", { "aria-hidden": true });
    shapes.append(text(L, 28, "TRAYECTORIA MEDIA ACUMULADA", { fill: colors.accent, "font-size": 12 }));
    shapes.append(text(R, 28, `${number.format(curve.count)} periodos`, { "text-anchor": "end" }));
    for (let i = 0; i < 5; i++) {
      const value = low - pad + i * (high - low + 2 * pad) / 4;
      shapes.append(node("path", { d: `M${L} ${yScale(value)}H${R}`, stroke: colors.grid, opacity: .65 }));
      shapes.append(text(L - 13, yScale(value) + 4, format(value), { "text-anchor": "end", "font-size": 10 }));
    }
    shapes.append(node("path", { d: `M${L} ${yScale(0)}H${R}`, stroke: colors.text, opacity: .5, "stroke-dasharray": "4 5" }));
    for (let i = 1; i < curve.y.length; i++) {
      shapes.append(node("path", { d: `M${x(i - 1)} ${yScale(curve.y[i - 1])}L${x(i)} ${yScale(curve.y[i])}`, fill: "none", stroke: curve.y[i] >= curve.y[i - 1] ? colors.green : colors.red, "stroke-width": 2.3 }));
    }
    curve.y.forEach((value, index) => shapes.append(node("circle", { cx: x(index), cy: yScale(value), r: 2.5, fill: "#c8d6e5", opacity: .65 })));
    const finalY = yScale(curve.total), color = curve.total >= 0 ? colors.green : colors.red;
    shapes.append(node("path", { d: `M${R} ${finalY - 6}l6 6-6 6-6-6Z`, fill: color }));
    shapes.append(text(R - 8, finalY - 15, `Total: ${format(curve.total)}`, { fill: color, "text-anchor": "end", "font-size": 12 }));
    shapes.append(text(L, 394, "CAMBIO MEDIO POR PASO", { fill: colors.accent, "font-size": 12 }));
    shapes.append(node("path", { d: `M${L} ${stepScale(0)}H${R}`, stroke: colors.text, opacity: .45 }));
    const barWidth = Math.min(38, (R - L) / curve.x.length * .72);
    curve.steps.forEach((value, index) => shapes.append(node("rect", { x: x(index) - barWidth / 2, y: Math.min(stepScale(0), stepScale(value)), width: barWidth, height: Math.max(.4, Math.abs(stepScale(value) - stepScale(0))), fill: value >= 0 ? colors.green : colors.red, opacity: .78 })));
    const stride = Math.max(1, Math.floor(curve.x.length / 10));
    const ticks = curve.x.filter((_, index) => index % stride === 0);
    if (!ticks.includes(curve.x.length - 1)) ticks.push(curve.x.length - 1);
    for (const index of ticks) {
      for (const yy of [351, 558]) shapes.append(text(x(index), yy, curve.labels[index], { "text-anchor": "middle", "font-size": 10 }));
    }
    overlays = node("g", { "pointer-events": "none", "aria-hidden": true });
    svg.append(shapes, overlays);
    drawOverlay();
    document.documentElement.dataset.analyzerReady = "true";
  };

  wireTabs(buttons, (button) => { period = button.dataset.analysisPeriod; render(); });
  for (const select of [from, to]) select.addEventListener("change", () => { if (data) setRange(Number(from.value), Number(to.value)); });
  document.getElementById("analysis-clear").addEventListener("click", () => {
    if (!data) return;
    range = null;
    from.value = 0;
    to.value = curve.x.length - 1;
    drawOverlay();
  });
  try {
    const response = await fetch(new URL("../../content/analyzer.json", import.meta.url), { signal: AbortSignal.timeout(8000) });
    if (!response.ok) throw new Error("Datos del Analizador no disponibles");
    const manifest = await response.json();
    if (manifest.schemaVersion !== 1 || !["dia", "semana", "mes", "anio"].every((key) => {
      const c = manifest.curves?.[key];
      return c && c.x.length === c.y.length && c.x.length === c.steps.length && c.labels.length === c.x.length && c.count > 0;
    })) throw new Error("Curvas incompletas");
    data = manifest;
    render();
  } catch {
    document.getElementById("analysis-range-result").textContent = "Puedes consultar la ilustración ampliada. La interacción no está disponible en este momento.";
  }
}
