import { initNavigation } from "./ui.js";

const year = document.getElementById("current-year");
if (year) year.textContent = new Date().getFullYear();
initNavigation();
