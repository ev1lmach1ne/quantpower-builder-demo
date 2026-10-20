// Graba video.html fotograma a fotograma (30 fps) y lo monta en MP4 con ffmpeg.
// Uso (desde la raíz del repositorio): node redes/13-novedades-v08/video/grabar.js
const { chromium } = require("playwright");
const { execFileSync } = require("child_process");
const fs = require("fs"), path = require("path"), os = require("os");

const DIR = __dirname, FPS = 30, DURACION = 36, W = 1080, H = 1920;
const tmp = fs.mkdtempSync(path.join(os.tmpdir(), "qpb-video-"));

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: W, height: H }, deviceScaleFactor: 1 });
  await page.goto("file://" + path.join(DIR, "video.html"));
  await page.waitForLoadState("load");
  await page.evaluate(() => document.getAnimations().forEach(a => a.pause()));
  const total = FPS * DURACION;
  for (let f = 0; f < total; f++) {
    const ms = (f / FPS) * 1000;
    await page.evaluate(t => document.getAnimations().forEach(a => { a.currentTime = t; }), ms);
    await page.screenshot({ path: path.join(tmp, String(f).padStart(5, "0") + ".jpg"), type: "jpeg", quality: 92 });
  }
  await browser.close();
  const out = path.join(DIR, "novedades-v08-1080x1920.mp4");
  execFileSync("ffmpeg", ["-y", "-loglevel", "error", "-framerate", String(FPS), "-i", path.join(tmp, "%05d.jpg"),
    "-c:v", "libx264", "-preset", "slow", "-crf", "18", "-pix_fmt", "yuv420p", "-movflags", "+faststart", out]);
  fs.copyFileSync(path.join(tmp, String(Math.round(FPS * 2)).padStart(5, "0") + ".jpg"), path.join(DIR, "video-portada.jpg"));
  fs.rmSync(tmp, { recursive: true, force: true });
  console.log("→ " + out);
})();
