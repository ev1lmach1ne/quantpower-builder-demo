const API = "https://api.github.com/repos/";
const repositoryPattern = /^[A-Za-z0-9][A-Za-z0-9_.-]*\/[A-Za-z0-9][A-Za-z0-9_.-]*$/;

function trustedReleaseUrl(value, repository, asset = false) {
  try {
    const url = new URL(value);
    const prefix = `/${repository}/releases/${asset ? "download/" : "tag/"}`;
    return url.protocol === "https:" && url.hostname === "github.com" && !url.username
      && !url.password && url.pathname.startsWith(prefix) ? url.href : null;
  } catch { return null; }
}

export function normalizeRelease(release, config) {
  if (!release || release.draft || release.prerelease || !release.tag_name || !Array.isArray(release.assets)) return null;
  const pageUrl = trustedReleaseUrl(release.html_url, config.releaseRepository);
  if (!pageUrl) return null;
  let asset;
  for (const name of config.assetNames) {
    asset = release.assets.find((item) => item.name === name && item.state === "uploaded");
    if (asset) break;
  }
  const downloadUrl = asset && trustedReleaseUrl(asset.browser_download_url, config.releaseRepository, true);
  const validSize = asset && Number.isFinite(asset.size) && asset.size > 0;
  return {
    version: release.tag_name,
    publishedAt: release.published_at,
    pageUrl,
    downloadUrl: validSize ? downloadUrl : null,
    size: validSize ? asset.size : null,
  };
}

function setButton(href, label, icon = "i-download", external = false) {
  const button = document.getElementById("demo-download");
  button.href = href;
  button.querySelector("span").textContent = label;
  button.querySelector("use").setAttribute("href", `#${icon}`);
  if (external) {
    button.target = "_blank";
    button.rel = "noopener noreferrer";
  } else {
    button.removeAttribute("target");
    button.removeAttribute("rel");
  }
}

function displayRelease(release, snapshot = false) {
  document.getElementById("release-version").textContent = release.version;
  document.getElementById("release-size").textContent = release.size
    ? `${new Intl.NumberFormat("es-ES", { maximumFractionDigits: 1 }).format(release.size / 1048576)} MiB` : "ZIP pendiente";
  const published = new Date(release.publishedAt);
  document.getElementById("release-date").textContent = Number.isNaN(published.getTime()) ? "Ver Release"
    : new Intl.DateTimeFormat("es-ES", { day: "numeric", month: "short", year: "numeric", timeZone: "UTC" }).format(published);
  document.getElementById("release-notes").href = release.pageUrl;
  document.getElementById("release-status").textContent = snapshot
    ? "Versión de referencia · Consulta las novedades para ver si hay una actualización."
    : release.downloadUrl ? "Demo disponible · Última versión publicada." : "La última publicación todavía no incluye el ZIP de Windows.";
  if (release.downloadUrl) {
    setButton(release.downloadUrl, "Descargar demo para Windows");
    document.getElementById("download-note").textContent = "Descarga directa desde GitHub Releases. Descomprime el ZIP completo antes de abrir la aplicación.";
  } else {
    setButton(release.pageUrl, "Ver la publicación", "i-external", true);
    document.getElementById("download-note").textContent = "El paquete estará disponible cuando se adjunte el ZIP a esta Release.";
  }
}

export async function initReleases() {
  let config;
  try {
    const response = await fetch(new URL("../../content/site.json", import.meta.url), { signal: AbortSignal.timeout(8000) });
    if (!response.ok) throw new Error("Configuración no disponible");
    config = await response.json();
    if (!repositoryPattern.test(config.releaseRepository) || !Array.isArray(config.assetNames)) throw new Error("Repositorio no configurado");
  } catch {
    document.getElementById("release-status").textContent = "La información de descarga no está disponible en este momento.";
    return;
  }
  const releasesUrl = `https://github.com/${config.releaseRepository}/releases`;
  document.getElementById("release-notes").href = releasesUrl;
  try {
    const response = await fetch(`${API}${config.releaseRepository}/releases/latest`, {
      headers: { Accept: "application/vnd.github+json" },
      credentials: "omit",
      signal: AbortSignal.timeout(8000),
    });
    if (response.status === 404) {
      document.getElementById("release-status").textContent = "La primera demo pública está en preparación.";
      return;
    }
    if (!response.ok) throw new Error("GitHub no disponible");
    const release = normalizeRelease(await response.json(), config);
    if (!release) throw new Error("Publicación no válida");
    displayRelease(release);
  } catch {
    const snapshot = normalizeRelease(config.fallbackRelease, config);
    if (snapshot) displayRelease(snapshot, true);
    else {
      document.getElementById("release-version").textContent = "Consultar en GitHub";
      document.getElementById("release-status").textContent = "Consulta GitHub Releases para ver la versión disponible.";
      setButton(releasesUrl, "Consultar las descargas", "i-external", true);
      document.getElementById("download-note").textContent = "No se ha podido consultar la versión automáticamente. Puedes comprobar las publicaciones en GitHub.";
    }
  }
}
