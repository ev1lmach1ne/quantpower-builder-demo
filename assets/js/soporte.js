(() => {
  'use strict';
  const API = 'https://api.quantpowerbuilder.com';
  const CLAVE_SESION = 'qp_cuenta';
  const $ = (id) => document.getElementById(id);

  function leerSesion() {
    try {
      const sesion = JSON.parse(localStorage.getItem(CLAVE_SESION) || 'null');
      return sesion && typeof sesion.token === 'string' && sesion.exp * 1000 > Date.now()
        ? sesion : null;
    } catch { return null; }
  }

  function uuidV4() {
    if (crypto.randomUUID) return crypto.randomUUID();
    const b = crypto.getRandomValues(new Uint8Array(16));
    b[6] = (b[6] & 0x0f) | 0x40;
    b[8] = (b[8] & 0x3f) | 0x80;
    const h = Array.from(b, (x) => x.toString(16).padStart(2, '0')).join('');
    return `${h.slice(0, 8)}-${h.slice(8, 12)}-${h.slice(12, 16)}-${h.slice(16, 20)}-${h.slice(20)}`;
  }

  function mostrarSesion(sesion) {
    $('soporte-sesion-requerida').hidden = Boolean(sesion);
    $('soporte-formulario').hidden = !sesion;
    if (sesion) {
      $('soporte-cuenta').textContent = 'Tu sesión está activa. El reporte se asociará a tu cuenta.';
    }
  }

  let sesion = leerSesion();
  mostrarSesion(sesion);

  $('form-soporte').addEventListener('submit', async (evento) => {
    evento.preventDefault();
    sesion = leerSesion();
    if (!sesion) {
      mostrarSesion(null);
      $('soporte-login-mensaje').textContent = 'Tu sesión ha caducado. Inicia sesión para enviar la solicitud.';
      return;
    }

    const form = evento.currentTarget;
    const boton = form.querySelector('button[type="submit"]');
    const datosForm = new FormData(form);
    const titulo = String(datosForm.get('titulo') || '').trim();
    const descripcion = String(datosForm.get('descripcion') || '').trim();
    const categoria = String(datosForm.get('categoria') || '');
    if (!titulo || titulo.length > 160) {
      $('soporte-estado').textContent = 'Escribe un título de hasta 160 caracteres.';
      $('soporte-estado').className = 'cuenta-estado error';
      return;
    }
    if (!descripcion || descripcion.length > 8000) {
      $('soporte-estado').textContent = 'La descripción debe tener entre 1 y 8.000 caracteres.';
      $('soporte-estado').className = 'cuenta-estado error';
      return;
    }

    boton.disabled = true;
    $('soporte-estado').textContent = 'Enviando…';
    $('soporte-estado').className = 'cuenta-estado';
    try {
      const respuesta = await fetch(API + '/api/reportes', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          id: uuidV4(), titulo, descripcion, categoria,
          email: '', version: 'Web', sistema: 'Navegador web',
          pestana: 'Página de soporte', sesion_token: sesion.token,
        }),
      });
      const resultado = await respuesta.json().catch(() => ({}));
      if (!respuesta.ok || !resultado.ok) {
        if (respuesta.status === 401 || respuesta.status === 403) {
          localStorage.removeItem(CLAVE_SESION);
          sesion = null;
          mostrarSesion(null);
          $('soporte-login-mensaje').textContent = 'La sesión caducó o ya no es válida. Inicia sesión de nuevo.';
          return;
        }
        throw new Error(resultado.mensaje || 'No se pudo enviar la solicitud. Inténtalo de nuevo.');
      }
      form.reset();
      $('soporte-estado').textContent = `Solicitud enviada al equipo. Referencia: ${resultado.id}`;
      $('soporte-estado').className = 'cuenta-estado ok';
    } catch (error) {
      $('soporte-estado').textContent = error.message || 'No se pudo conectar con el servicio de soporte.';
      $('soporte-estado').className = 'cuenta-estado error';
    } finally {
      boton.disabled = false;
    }
  });
})();
