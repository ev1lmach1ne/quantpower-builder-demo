import { selectButtons, wireTabs } from "./ui.js";

const numbers = new Intl.NumberFormat("es-ES", { minimumFractionDigits: 2, maximumFractionDigits: 2 });
const prices = new Intl.NumberFormat("es-ES", { minimumFractionDigits: 4, maximumFractionDigits: 4 });
const compact = new Intl.NumberFormat("es-ES", { maximumFractionDigits: 4 });
const times = new Intl.DateTimeFormat("es-ES", { timeZone: "UTC", day: "2-digit", month: "2-digit", hour: "2-digit", minute: "2-digit", hourCycle: "h23" });
const imageUrl = (asset) => new URL(`../images/${asset}`, import.meta.url).href;
const defaultPeriods = { trend: 20, reversion: 20, momentum: 12, profile: 60 };

function fillTrades(trades) {
  document.getElementById("trades-body").replaceChildren(...trades.map((trade) => {
    const row = document.createElement("tr");
    const cells = [String(trade.number).padStart(2, "0"), `V${trade.signalIndex + 1}`, `V${trade.start + 1}`,
      prices.format(trade.entry), `V${trade.end + 1} · ${trade.exitPhase}`, prices.format(trade.exit),
      `${trade.pnl > 0 ? "+" : ""}${numbers.format(trade.pnl)} u.m.`, trade.reason];
    for (const [index, value] of cells.entries()) {
      const cell = document.createElement("td");
      cell.textContent = value;
      if (index === 6) cell.className = trade.pnl >= 0 ? "positive" : "negative";
      row.append(cell);
    }
    return row;
  }));
}

export async function initGallery() {
  const sampleButtons = [...document.querySelectorAll("[data-sample]")];
  const viewButtons = [...document.querySelectorAll("[data-result-view]")];
  const image = document.getElementById("sample-image");
  const inspection = document.getElementById("inspection-trade");
  const settings = Object.fromEntries(Object.entries(defaultPeriods).map(([id, period]) => [id, { period, risk: 1 }]));
  let data;
  let selected = document.querySelector('[data-preset][aria-pressed="true"]').dataset.preset;
  // Recoge también los controles restaurados por el navegador antes del fetch.
  settings[selected] = { period: Number(document.getElementById("builder-period").value),
    risk: Number(document.getElementById("builder-risk").value) };
  let view = "chart";
  let sample;

  const moment = (index, close = false) => times.format(new Date(Date.parse(data.timestamps[index]) + (close ? 3600000 : 0))) + " UTC";
  const inspect = () => {
    const trade = sample.trades.find((item) => item.number === Number(inspection.value));
    document.getElementById("inspection-detail").hidden = !trade;
    document.querySelector(".inspection-figure").hidden = !trade;
    if (!trade) return;
    document.getElementById("inspection-signal").textContent = `Cierre de V${trade.signalIndex + 1}`;
    document.getElementById("inspection-signal-time").textContent = moment(trade.signalIndex, true);
    const cross = trade.evidence[0];
    const threshold = trade.evidence[1];
    document.getElementById("inspection-condition").textContent =
      `${compact.format(cross.previousLeft)} ≤ ${compact.format(cross.previousRight)} en t−1; ` +
      `${compact.format(cross.left)} > ${compact.format(cross.right)} en t.` +
      (threshold ? ` Confirmación: ${compact.format(threshold.left)} ${threshold.operator} ${compact.format(threshold.right)}.` : " Perfil anterior ya cerrado.");
    document.getElementById("inspection-entry").textContent = `Open de V${trade.start + 1}`;
    document.getElementById("inspection-entry-time").textContent = moment(trade.start);
    document.getElementById("inspection-fill").textContent =
      `Open ${prices.format(trade.entryOpen)} → llenado ${prices.format(trade.entry)}. Slippage 0,02 %; la señal procede de la vela anterior.`;
    document.getElementById("inspection-exit").textContent = `V${trade.end + 1} · ${trade.reason}`;
    document.getElementById("inspection-exit-time").textContent = trade.exitPhase === "intrabar"
      ? `${moment(trade.end)} – ${moment(trade.end, true)}` : moment(trade.end, trade.exitPhase === "cierre");
    document.getElementById("inspection-reason").textContent =
      `${trade.exitPhase}: llenado ${prices.format(trade.exit)}.` +
      (trade.exitSignalIndex !== null ? ` Decisión al cierre de V${trade.exitSignalIndex + 1}.` : "") +
      ` Resultado neto: ${numbers.format(trade.pnl)} u.m.`;
    const facts = [
      ["ATR(14) de t", compact.format(trade.atr)], ["Stop inicial", prices.format(trade.stop)],
      ["TP 2R", prices.format(trade.takeProfit)], ["Unidades", compact.format(trade.units)],
      ["Riesgo nominal", `${numbers.format(trade.entryEquity * sample.risk / 100)} u.m.`],
      ["Comisión total", `${numbers.format(trade.commission)} u.m.`],
    ];
    document.getElementById("inspection-facts").replaceChildren(...facts.map(([label, value]) => {
      const item = document.createElement("span");
      const strong = document.createElement("strong");
      item.append(`${label}: `);
      strong.textContent = value;
      item.append(strong);
      return item;
    }));
    document.getElementById("inspection-image").src = imageUrl(trade.detailImage);
    document.getElementById("inspection-open").href = imageUrl(trade.detailImage);
    document.getElementById("inspection-image").alt = `Operación ${trade.number}: señal en V${trade.signalIndex + 1}, entrada en V${trade.start + 1} y salida en V${trade.end + 1} por ${trade.reason}.`;
  };

  const render = () => {
    if (!data) return;
    sample = data.variants.find((item) => item.id === selected && item.period === settings[selected].period && item.risk === settings[selected].risk);
    if (!sample) return;
    const tab = sampleButtons.find((button) => button.dataset.sample === selected);
    selectButtons(sampleButtons, tab, "aria-selected");
    selectButtons(viewButtons, viewButtons.find((button) => button.dataset.resultView === view));
    document.getElementById("sample-panel").setAttribute("aria-labelledby", tab.id);
    document.getElementById("sample-panel").dataset.configuration = sample.key;
    document.getElementById("sample-title").textContent = sample.title;
    document.getElementById("sample-description").textContent = sample.description;
    document.getElementById("sample-parameters").textContent = `${selected === "profile" ? `Letra TPO ${sample.period} min · Sesión diaria` : `Periodo ${sample.period}`} · Riesgo ${compact.format(sample.risk)} % · Solo largos · H1 UTC`;
    document.getElementById("result-chart").hidden = view === "trades";
    document.getElementById("result-trades").hidden = view !== "trades";
    const asset = view === "equity" ? sample.equityImage : sample.image;
    image.src = imageUrl(asset);
    image.setAttribute("height", view === "equity" ? "520" : "600");
    image.alt = view === "equity" ? `Capital y drawdown del motor: ${sample.title}. Datos sintéticos.`
      : `${selected === "profile" ? "Mapas de calor TPO diarios consecutivos, señales y ejecuciones" : "Señales y ejecuciones"} del motor: ${sample.description}`;
    document.getElementById("chart-open").href = image.src;
    document.getElementById("sample-caption").textContent = view === "equity"
      ? "Curva marcada a mercado y drawdown producidos por el mismo backtest de la tabla. Capital inicial: 10.000 u.m."
      : selected === "profile"
        ? "Mapas de calor al cierre de cada sesión UTC. POC rojo y VAH/VAL grises; niveles anteriores punteados. Las señales usan el perfil anterior cerrado. S: señal · E: entrada al open siguiente · X: salida."
        : "S: señal al cierre de t. E: entrada en la apertura de t+1. X: salida al precio de llenado del motor. Serie sintética descargable.";
    for (const element of document.querySelectorAll("[data-metric]")) {
      const key = element.dataset.metric;
      const value = sample.metrics[key];
      element.textContent = key === "profitFactor" && sample.metrics.profitFactorInfinite ? "∞"
        : value === null ? "—" : key === "count" ? String(value)
          : key.endsWith("Pct") ? `${value > 0 ? "+" : ""}${numbers.format(value)} %` : numbers.format(value);
      element.title = key === "profitFactor" && sample.metrics.profitFactorInfinite ? "Sin operaciones perdedoras en esta muestra sintética." : "";
    }
    fillTrades(sample.trades);
    const previousTrade = inspection.value;
    inspection.replaceChildren(...sample.trades.map((trade) => {
      const option = document.createElement("option");
      option.value = trade.number;
      option.textContent = `#${trade.number} · V${trade.start + 1} → V${trade.end + 1}`;
      return option;
    }));
    if (!sample.trades.length) inspection.replaceChildren(new Option("Sin operaciones", ""));
    else if (sample.trades.some((trade) => String(trade.number) === previousTrade)) inspection.value = previousTrade;
    inspect();
    document.dispatchEvent(new CustomEvent("quantpower:example-rendered", { detail: {
      sample: selected, period: sample.period, risk: sample.risk,
    } }));
    document.documentElement.dataset.examplesReady = "true";
  };

  document.addEventListener("quantpower:example", (event) => {
    const { sample: family, period, risk, resetView } = event.detail || {};
    if (!Object.hasOwn(settings, family)) return;
    if (data && !data.variants.some((item) => item.id === family && item.period === period && item.risk === risk)) return;
    settings[family] = { period, risk };
    selected = family;
    if (resetView) view = "chart";
    render();
  });
  wireTabs(sampleButtons, (button) => { selected = button.dataset.sample; render(); });
  for (const button of viewButtons) button.addEventListener("click", () => { view = button.dataset.resultView; render(); });
  inspection.addEventListener("change", inspect);
  try {
    const response = await fetch(new URL("../../content/examples.json", import.meta.url), { signal: AbortSignal.timeout(8000) });
    if (!response.ok) throw new Error("Ejemplos no disponibles");
    const manifest = await response.json();
    if (manifest.schemaVersion !== 2 || !Array.isArray(manifest.variants) || !Array.isArray(manifest.timestamps)) throw new Error("Ejemplos incompletos");
    data = manifest;
    render();
  } catch {
    document.getElementById("sample-caption").textContent = "Los ejemplos técnicos no están disponibles en este momento.";
  }
}
