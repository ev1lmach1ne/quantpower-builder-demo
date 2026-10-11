// Renderiza historia.html a PNG con Playwright y Chromium.
// Uso (desde la raíz del repositorio): node redes/03-vortex-historias/renderizar.js
const path = require('path');
const { chromium } = require(process.env.PLAYWRIGHT_PATH || 'playwright');
const CHROMIUM = process.env.CHROMIUM || '/opt/pw-browsers/chromium';
(async () => {
  const b = await chromium.launch({ executablePath: CHROMIUM });
  for (const n of [1, 2]) {
    const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
    await p.goto('file://' + path.join(__dirname, 'historia.html') + '?h=' + n);
    const over = await p.evaluate((n) => { const e = document.getElementById('s' + n); return e.scrollHeight - e.clientHeight; }, n);
    await p.screenshot({ path: path.join(__dirname, `historia-${n}-1080x1920.png`) });
    console.log('historia-' + n, over > 0 ? 'DESBORDA ' + over + 'px' : 'ok');
  }
  await b.close();
})();
