import { selectButtons, wireTabs } from "./ui.js";

const numbers = new Intl.NumberFormat("es-ES", { minimumFractionDigits: 2, maximumFractionDigits: 2 });

function fillTrades(trades) {
  const body = document.getElementById("trades-body");
  body.replaceChildren(...trades.map((trade) => {
    const row = document.createElement("tr");
    const cells = [String(trade.number).padStart(2, "0"), trade.side, numbers.format(trade.entry),
      numbers.format(trade.exit), `${trade.pnl > 0 ? "+" : ""}${numbers.format(trade.pnl)} u.m.`, trade.reason];
    for (const [index, value] of cells.entries()) {
      const cell = document.createElement("td");
      cell.textContent = value;
      if (index === 4) cell.className = trade.pnl >= 0 ? "positive" : "negative";
      if (index === 1) cell.className = "trade-side";
      row.append(cell);
    }
    return row;
  }));
}

export async function initGallery() {
  const sampleButtons = [...document.querySelectorAll("[data-sample]")];
  const viewButtons = [...document.querySelectorAll("[data-result-view]")];
  const image = document.getElementById("sample-image");
  let examples;
  let selected = "trend";
  let view = "chart";
  const render = () => {
    const sample = examples.find((example) => example.id === selected);
    if (!sample) return;
    const currentTab = sampleButtons.find((button) => button.dataset.sample === selected);
    selectButtons(sampleButtons, currentTab, "aria-selected");
    selectButtons(viewButtons, viewButtons.find((button) => button.dataset.resultView === view));
    document.getElementById("sample-panel").setAttribute("aria-labelledby", currentTab.id);
    document.getElementById("sample-title").textContent = sample.title;
    document.getElementById("sample-description").textContent = sample.description;
    document.getElementById("result-chart").hidden = view === "trades";
    document.getElementById("result-trades").hidden = view !== "trades";
    const asset = view === "equity" ? sample.equityImage : sample.image;
    image.src = new URL(`../images/${asset}`, import.meta.url).href;
    document.getElementById("chart-open").href = image.src;
    image.alt = view === "equity" ? `Capital y drawdown sintéticos: ${sample.title}.` : `Gráfico ilustrativo: ${sample.description}`;
    document.getElementById("sample-caption").textContent = view === "equity"
      ? "Curva y drawdown calculados a partir de las mismas operaciones sintéticas de la tabla. Capital inicial: 10.000 u.m."
      : "Entradas y salidas sobre una serie sintética. Las cifras describen este ejemplo ilustrativo.";
    for (const element of document.querySelectorAll("[data-metric]")) {
      const key = element.dataset.metric;
      const value = sample.metrics[key];
      element.textContent = value === null ? "—" : key === "count" ? String(value)
        : key.endsWith("Pct") ? `${value > 0 ? "+" : ""}${numbers.format(value)} %` : numbers.format(value);
    }
    fillTrades(sample.trades);
  };
  try {
    const response = await fetch(new URL("../../content/examples.json", import.meta.url), { signal: AbortSignal.timeout(8000) });
    if (!response.ok) throw new Error("Ejemplos no disponibles");
    const data = await response.json();
    examples = data.examples;
    if (!Array.isArray(examples) || examples.length !== 4) throw new Error("Ejemplos incompletos");
    render();
  } catch {
    document.getElementById("sample-caption").textContent = "Visualización ilustrativa. Los ejemplos interactivos no están disponibles en este momento.";
    return;
  }
  wireTabs(sampleButtons, (button) => { selected = button.dataset.sample; render(); });
  for (const button of viewButtons) button.addEventListener("click", () => { view = button.dataset.resultView; render(); });
  document.addEventListener("quantpower:example", (event) => {
    if (examples.some((example) => example.id === event.detail?.sample)) {
      selected = event.detail.sample;
      view = "chart";
      render();
    }
  });
}
