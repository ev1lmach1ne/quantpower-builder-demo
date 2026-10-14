// El enlace público usa la invitación estática y funciona con el PC apagado.
export async function initDiscordLinks() {
  const enlaces = [...document.querySelectorAll('[data-discord-link]')];
  if (!enlaces.length) return;
  try {
    const respuesta = await fetch(new URL('../../content/site.json', import.meta.url), { cache: 'no-cache' });
    if (!respuesta.ok) return;
    const datos = await respuesta.json();
    const url = datos.discordInvite;
    if (typeof url !== 'string' || !/^https:\/\/(?:discord\.gg\/|discord\.com\/invite\/)[A-Za-z0-9_-]+$/.test(url)) return;
    enlaces.forEach((enlace) => { enlace.href = url; });
  } catch { /* conservar el enlace al receptor si no se carga la configuración */ }
}

initDiscordLinks();
