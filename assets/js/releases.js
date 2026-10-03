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
  if (!release || release.draft || !release.tag_name || !Array.isArray(release.assets)) return null;
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
    prerelease: Boolean(release.prerelease),
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
    button.removeAttribute("download");
  } else {
    button.removeAttribute("target");
    button.removeAttribute("rel");
    button.setAttribute("download", "QuantPowerBuilder_Windows_x64.zip");
  }
}

export function initDownloadFeedback() {
  const button = document.getElementById("demo-download");
  button.addEventListener("click", () => {
    const url = new URL(button.href);
    if (url.hostname !== "github.com" || !url.pathname.includes("/download/")) return;
    document.getElementById("download-note").textContent =
      "Solicitud de descarga enviada al navegador. Consulta su panel de descargas (Ctrl+J en Windows). Si no aparece, utiliza «Abrir descarga en GitHub».";
  });
}

function displayRelease(release, { snapshot = false, latest = false, total = 1 } = {}) {
  document.getElementById("release-version").textContent = release.version;
  document.getElementById("release-size").textContent = release.size
    ? `${new Intl.NumberFormat("es-ES", { maximumFractionDigits: 1 }).format(release.size / 1048576)} MiB` : "ZIP pendiente";
  const published = new Date(release.publishedAt);
  document.getElementById("release-date").textContent = Number.isNaN(published.getTime()) ? "Ver Release"
    : new Intl.DateTimeFormat("es-ES", { day: "numeric", month: "short", year: "numeric", timeZone: "UTC" }).format(published);
  document.getElementById("release-notes").href = release.pageUrl;
  const selectedInfo = latest
    ? `${release.prerelease ? "Última alpha publicada" : "Última versión publicada"} · `
    : `${release.prerelease ? "Alpha histórica" : "Versión histórica seleccionada"} · `;
  document.getElementById("release-status").textContent = snapshot
    ? `${selectedInfo}${release.downloadUrl ? "Demo disponible." : "ZIP pendiente."} Consulta las novedades para ver si hay una actualización.`
    : release.downloadUrl ? `${selectedInfo}Demo disponible.` : "La publicación seleccionada todavía no incluye el ZIP de Windows.";
  const help = document.getElementById("release-version-help");
  if (help) help.textContent = snapshot
    ? "Versión disponible mientras se consulta la lista de Releases."
    : `${total} versiones publicadas${latest ? " · última con ZIP seleccionada" : " · explorando el historial"}.`;
  if (release.downloadUrl) {
    setButton(release.downloadUrl, "Descargar demo para Windows");
    document.getElementById("download-note").textContent = "Descarga directa desde GitHub Releases. Descomprime el ZIP completo antes de abrir la aplicación.";
  } else {
    setButton(release.pageUrl, "Ver la publicación", "i-external", true);
    document.getElementById("download-note").textContent = "El paquete estará disponible cuando se adjunte el ZIP a esta Release.";
  }
}

function fillVersionSelector(releases, selectedTag, config) {
  const picker = document.getElementById("release-version-select");
  const releasesByTag = new Map();
  for (const release of releases) {
    const normalized = release?.version && release?.pageUrl
      ? release : normalizeRelease(release, config);
    if (normalized) releasesByTag.set(normalized.version, normalized);
  }
  const versions = [...releasesByTag.values()].sort((a, b) => {
    if (a.version === selectedTag) return -1;
    if (b.version === selectedTag) return 1;
    return Date.parse(b.publishedAt || "") - Date.parse(a.publishedAt || "");
  });
  picker.replaceChildren(...versions.map((release) => {
    const option = document.createElement("option");
    option.value = release.version;
    const estado = release.version === selectedTag
      ? ` · Última Versión${release.prerelease ? " · Alpha" : ""}`
      : release.prerelease ? " · Alpha" : "";
    option.textContent = `${release.version}${estado}${release.downloadUrl ? "" : " · ZIP pendiente"}`;
    option.dataset.releasePage = release.pageUrl;
    option.selected = release.version === selectedTag;
    return option;
  }));
  picker.hidden = false;
  const selected = versions.find((release) => release.version === picker.value);
  return { versions, selected: selected || versions[0] };
}

export async function initReleases() {
  let config;
  const versionPicker = document.getElementById("release-version-select");
  let releaseVersions = [];
  versionPicker?.addEventListener("change", () => {
    const selected = releaseVersions.find((release) => release.version === versionPicker.value);
    if (selected) displayRelease(selected, { latest: selected.version === releaseVersions[0]?.version, total: releaseVersions.length });
  });
  try {
    const response = await fetch(new URL("../../content/site.json", import.meta.url), { signal: AbortSignal.timeout(8000) });
    if (!response.ok) throw new Error("Configuración no disponible");
    config = await response.json();
    if (!repositoryPattern.test(config.releaseRepository) || !Array.isArray(config.assetNames)) throw new Error("Repositorio no configurado");
  } catch {
    document.getElementById("release-status").textContent = "Descarga directa disponible. Consulta las novedades en GitHub para confirmar la versión.";
    document.documentElement.dataset.releasesReady = "true";
    return;
  }
  const releasesUrl = `https://github.com/${config.releaseRepository}/releases`;
  document.getElementById("release-notes").href = releasesUrl;
  const snapshot = normalizeRelease(config.fallbackRelease, config);
  if (snapshot) displayRelease(snapshot, true);
  const headers = { Accept: "application/vnd.github+json" };
  const releaseEndpoint = `${API}${config.releaseRepository}/releases`;
  const versionsPromise = fetch(`${releaseEndpoint}?per_page=100`, {
      headers,
      credentials: "omit",
      signal: AbortSignal.timeout(8000),
    });
  try {
    const versionsResponse = await Promise.allSettled([versionsPromise]);
    const releasesResult = versionsResponse[0];
    let published = [];
    if (releasesResult.status === "fulfilled" && releasesResult.value.ok) {
      const releases = await releasesResult.value.json();
      if (Array.isArray(releases)) {
        published = releases.map((release) => normalizeRelease(release, config))
          .filter(Boolean)
          .sort((a, b) => Date.parse(b.publishedAt || "") - Date.parse(a.publishedAt || ""));
      }
    }
    if (published.length) {
      const latestDownload = published.find((release) => release.downloadUrl) || published[0];
      const collection = fillVersionSelector(published, latestDownload.version, config);
      releaseVersions = collection.versions;
      displayRelease(latestDownload, { latest: true, total: releaseVersions.length });
      return;
    }
    if (!snapshot) {
      const picker = document.getElementById("release-version-select");
      picker.replaceChildren(new Option("Versiones no disponibles", "", true, true));
      picker.disabled = true;
      const firstPublication = releasesResult.status === "fulfilled" && releasesResult.value.status === 404;
      if (firstPublication) {
        document.getElementById("release-version").textContent = "Pendiente de publicación";
        document.getElementById("release-size").textContent = "—";
        document.getElementById("release-date").textContent = "—";
        document.getElementById("release-status").textContent = "La primera demo pública está en preparación.";
        setButton(releasesUrl, "Consultar las publicaciones", "i-external", true);
        document.getElementById("download-note").textContent = "Cuando haya una Release oficial con el ZIP, la última versión aparecerá aquí automáticamente.";
        return;
      }
      document.getElementById("release-version").textContent = "Consultar en GitHub";
      document.getElementById("release-status").textContent = "Consulta GitHub Releases para ver la versión disponible.";
      setButton(releasesUrl, "Consultar las descargas", "i-external", true);
      document.getElementById("download-note").textContent = "No se ha podido consultar la versión automáticamente. Puedes comprobar las publicaciones en GitHub.";
    }
  } catch {
    if (snapshot) {
      const collection = fillVersionSelector([config.fallbackRelease], snapshot.version, config);
      releaseVersions = collection.versions;
      displayRelease(snapshot, { snapshot: true, latest: true, total: releaseVersions.length });
    }
    else {
      const picker = document.getElementById("release-version-select");
      picker.replaceChildren(new Option("Versiones no disponibles", "", true, true));
      picker.disabled = true;
      document.getElementById("release-version").textContent = "Consultar en GitHub";
      document.getElementById("release-status").textContent = "Consulta GitHub Releases para ver la versión disponible.";
      setButton(releasesUrl, "Consultar las descargas", "i-external", true);
      document.getElementById("download-note").textContent = "No se ha podido consultar la versión automáticamente. Puedes comprobar las publicaciones en GitHub.";
    }
  } finally {
    document.documentElement.dataset.releasesReady = "true";
  }
}
