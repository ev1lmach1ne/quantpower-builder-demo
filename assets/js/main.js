import { initBuilder } from "./builder.js";
import { initGallery } from "./gallery.js";
import { initReleases } from "./releases.js";
import { initExportExample, initNavigation } from "./ui.js";

document.getElementById("current-year").textContent = new Date().getFullYear();
initNavigation();
initBuilder();
initExportExample();
await Promise.allSettled([initGallery(), initReleases()]);
