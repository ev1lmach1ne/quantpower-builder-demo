import { selectButtons } from "./ui.js";

const presets = {
  trend: {
    signal: "EMA rápida cruza por encima de EMA lenta",
    reference: "Referencia: EMA 50",
    confirmation: "RSI por encima de 50",
    options: [10, 20, 30],
    defaultPeriod: 20,
    describe: (period) => `EMA ${period} cruce por encima de EMA 50 y RSI supere 50`,
  },
  reversion: {
    signal: "Precio cruza por encima de Bollinger inferior",
    reference: "Bandas: 2 desviaciones estándar",
    confirmation: "RSI por debajo de 40",
    options: [14, 20, 30],
    defaultPeriod: 20,
    describe: (period) => `el precio cruce por encima de la banda inferior de Bollinger (${period}, 2σ) y RSI esté por debajo de 40`,
  },
  momentum: {
    signal: "MACD cruza por encima de su señal",
    reference: "MACD lento: 26 · Señal: 9",
    confirmation: "ADX por encima de 20",
    options: [8, 12, 16],
    defaultPeriod: 12,
    describe: (period) => `MACD (${period}, 26, 9) cruce por encima de su señal y ADX supere 20`,
  },
};

export function initBuilder() {
  const buttons = [...document.querySelectorAll("[data-preset]")];
  const period = document.getElementById("builder-period");
  const risk = document.getElementById("builder-risk");
  let selected = "trend";
  const update = () => {
    const formattedRisk = new Intl.NumberFormat("es-ES", { maximumFractionDigits: 1 }).format(Number(risk.value));
    document.getElementById("builder-summary").textContent =
      `Entrar cuando ${presets[selected].describe(period.value)}. Aplicar un riesgo nominal del ${formattedRisk} % por setup con stop a 1,5 × ATR.`;
  };
  const choosePreset = (button) => {
    selected = button.dataset.preset;
    const preset = presets[selected];
    selectButtons(buttons, button);
    document.getElementById("builder-signal").textContent = preset.signal;
    document.getElementById("builder-reference").textContent = preset.reference;
    document.getElementById("builder-confirmation").textContent = preset.confirmation;
    period.replaceChildren(...preset.options.map((value) => {
      const option = document.createElement("option");
      option.value = value;
      option.textContent = `${value} velas`;
      option.selected = value === preset.defaultPeriod;
      return option;
    }));
    update();
  };
  for (const button of buttons) button.addEventListener("click", () => choosePreset(button));
  period.addEventListener("change", update);
  risk.addEventListener("change", update);
  document.getElementById("builder-preview").addEventListener("click", () => {
    document.dispatchEvent(new CustomEvent("quantpower:example", { detail: { sample: selected } }));
  });
  update();
}
