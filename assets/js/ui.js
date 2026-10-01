export function selectButtons(buttons, selected, attribute = "aria-pressed") {
  for (const button of buttons) {
    const active = button === selected;
    button.setAttribute(attribute, String(active));
    if (attribute === "aria-selected") button.tabIndex = active ? 0 : -1;
  }
}

export function wireTabs(buttons, onSelect) {
  for (const button of buttons) {
    button.addEventListener("click", () => onSelect(button));
    button.addEventListener("keydown", (event) => {
      const index = buttons.indexOf(button);
      const next = {
        ArrowRight: (index + 1) % buttons.length,
        ArrowLeft: (index - 1 + buttons.length) % buttons.length,
        Home: 0,
        End: buttons.length - 1,
      }[event.key];
      if (next === undefined) return;
      event.preventDefault();
      buttons[next].focus();
      onSelect(buttons[next]);
    });
  }
}

export function initNavigation() {
  const toggle = document.querySelector(".menu-toggle");
  const nav = document.querySelector(".main-nav");
  const setOpen = (open, returnFocus = false) => {
    toggle.setAttribute("aria-expanded", String(open));
    toggle.setAttribute("aria-label", open ? "Cerrar navegación" : "Abrir navegación");
    nav.classList.toggle("is-open", open);
    if (returnFocus) toggle.focus();
  };
  toggle.addEventListener("click", () => setOpen(toggle.getAttribute("aria-expanded") !== "true"));
  nav.addEventListener("click", (event) => {
    if (event.target.closest("a")) setOpen(false);
  });
  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && toggle.getAttribute("aria-expanded") === "true") setOpen(false, true);
  });
  document.addEventListener("click", (event) => {
    if (!event.target.closest(".site-header")) setOpen(false);
  });
  const media = window.matchMedia("(min-width: 761px)");
  media.addEventListener("change", () => setOpen(false));
  const links = [...nav.querySelectorAll('a[href^="#"]')];
  if ("IntersectionObserver" in window) {
    const observer = new IntersectionObserver((entries) => {
      const visible = entries.filter((entry) => entry.isIntersecting);
      if (!visible.length) return;
      const id = visible[0].target.id;
      for (const link of links) {
        if (link.hash === `#${id}`) link.setAttribute("aria-current", "location");
        else link.removeAttribute("aria-current");
      }
    }, { rootMargin: "-20% 0px -55% 0px" });
    for (const link of links) {
      const section = document.querySelector(link.hash);
      if (section) observer.observe(section);
    }
  }
}

export function initExportExample() {
  const examples = {
    pine: `// Lógica ilustrativa · TradingView
fast = ta.ema(close, 20)
slow = ta.ema(close, 50)
confirm = ta.rsi(close, 14) > 50

if ta.crossover(fast, slow) and confirm
    strategy.entry("Long", strategy.long)`,
    mql: `// Lógica ilustrativa · MetaTrader 5
// Valores de la última vela cerrada
bool cross = fast_prev <= slow_prev
          && fast_closed > slow_closed;
bool confirm = rsi_closed > 50;

if (cross && confirm)
    trade.Buy(volume, _Symbol);`,
  };
  const buttons = [...document.querySelectorAll("[data-language]")];
  for (const button of buttons) {
    button.addEventListener("click", () => {
      selectButtons(buttons, button);
      document.getElementById("export-code").textContent = examples[button.dataset.language];
    });
  }
}
