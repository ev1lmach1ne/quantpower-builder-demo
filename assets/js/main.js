import { initBuilder } from "./builder.js";
import { initGallery } from "./gallery.js";
import { initDownloadFeedback, initReleases } from "./releases.js";
import { initExportExample, initNavigation } from "./ui.js";
import { initAnalyzer } from "./analyzer.js";

document.getElementById("current-year").textContent = new Date().getFullYear();
initNavigation();
initBuilder();
initExportExample();
initDownloadFeedback();
await Promise.allSettled([initGallery(), initReleases(), initAnalyzer()]);
