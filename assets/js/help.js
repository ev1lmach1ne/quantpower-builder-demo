// El índice queda accesible sin JavaScript; en móvil empieza plegado.
const navigation = document.querySelector('.help-sidebar details');
if (navigation && window.matchMedia('(max-width: 820px)').matches) {
  navigation.open = false;
}

// Un manifiesto compartido mantiene versión y fecha visibles en cada guía.
const metadataBlock = document.querySelector('[data-help-meta]');
const helpScript = document.currentScript;
if (metadataBlock && helpScript?.src) {
  const guideId = metadataBlock.dataset.helpMeta;
  const metadataUrl = new URL('../../ayuda/meta.json', helpScript.src);
  fetch(metadataUrl, { cache: 'no-cache' })
    .then(response => {
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      return response.json();
    })
    .then(metadata => {
      const guide = metadata.guides?.[guideId];
      if (!guide) return;
      const version = metadataBlock.querySelector('[data-software-version]');
      const date = metadataBlock.querySelector('[data-guide-date]');
      if (version) version.textContent = metadata.softwareVersion;
      if (date) {
        date.dateTime = guide.writtenOn;
        date.textContent = guide.writtenLabel;
      }
    })
    .catch(() => {}); // El HTML conserva metadatos de respaldo si falla la red.
}
