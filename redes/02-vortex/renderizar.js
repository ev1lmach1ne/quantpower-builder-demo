// Renderiza cartel.html a PNG con Playwright y Chromium.
// Uso (desde la raíz del repositorio): node redes/02-vortex/renderizar.js
// Ajusta CHROMIUM si no está en la ruta por defecto.
const path = require('path');
const { chromium } = require(process.env.PLAYWRIGHT_PATH || 'playwright');
const CHROMIUM = process.env.CHROMIUM || '/opt/pw-browsers/chromium';
const dir = __dirname;
const salidas = [
  ['vertical', 1080, 1920, 'cartel-1080x1920.png'],
  ['corto', 1080, 1350, 'cartel-1080x1350.png'],
];
(async () => {
  const b = await chromium.launch({ executablePath: CHROMIUM });
  for (const [f, w, h, out] of salidas) {
    const p = await b.newPage({ viewport: { width: w, height: h } });
    await p.goto('file://' + path.join(dir, 'cartel.html') + '?f=' + f);
    const overflow = await p.evaluate(() => {
      const el = document.getElementById('poster');
      return el.scrollHeight - el.clientHeight;
    });
    await p.screenshot({ path: path.join(dir, out) });
    console.log(out, overflow > 0 ? 'DESBORDA ' + overflow + 'px' : 'ok');
  }
  await b.close();
})();
