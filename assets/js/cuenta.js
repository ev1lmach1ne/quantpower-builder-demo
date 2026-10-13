(() => {
  const local = ['localhost', '127.0.0.1'].includes(location.hostname);
  const API = local ? 'http://127.0.0.1:8787' : 'https://api.quantpowerbuilder.com';
  const CLAVE_SESION = 'qp_cuenta';
  const $ = (id) => document.getElementById(id);

  // ---- sesión (localStorage con 24 h de validez; funciona sin él) ----------
  let sesion = null;
  const leerSesion = () => {
    try {
      const s = JSON.parse(localStorage.getItem(CLAVE_SESION) || 'null');
      return s && s.token && s.exp * 1000 > Date.now() ? s : null;
    } catch (e) { return null; }
  };
  const guardarSesion = (s) => {
    sesion = s;
    try { s ? localStorage.setItem(CLAVE_SESION, JSON.stringify(s)) : localStorage.removeItem(CLAVE_SESION); } catch (e) { /* sin almacenamiento */ }
  };

  // ---- API -----------------------------------------------------------------
  const api = async (ruta, cuerpo) => {
    let r;
    try {
      r = await fetch(API + ruta, {
        method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(cuerpo),
      });
    } catch (e) {
      throw Object.assign(new Error('No se pudo conectar con el servidor. Inténtalo más tarde.'), { codigo: 'red' });
    }
    const datos = await r.json().catch(() => ({}));
    if (!r.ok || !datos.ok) {
      throw Object.assign(new Error(datos.mensaje || 'No se pudo completar la operación.'), { codigo: datos.codigo || '' });
    }
    return datos;
  };
  const conToken = (ruta, extra = {}) => api(ruta, { token: sesion.token, ...extra });

  // ---- utilidades de UI ----------------------------------------------------
  const mensaje = (form, texto, tipo) => {
    const p = form.querySelector('.cuenta-estado');
    p.textContent = texto || '';
    p.className = 'cuenta-estado' + (tipo ? ' ' + tipo : '');
  };
  const fecha = (ts) => new Date(ts * 1000).toLocaleDateString('es-ES', { dateStyle: 'long' });
  const hace = (ts) => {
    const m = Math.round((Date.now() / 1000 - ts) / 60);
    return m < 1 ? 'ahora' : m < 60 ? `hace ${m} min` : m < 1440 ? `hace ${Math.round(m / 60)} h` : `hace ${Math.round(m / 1440)} d`;
  };
  // Envuelve un envío de formulario: bloquea el botón y muestra errores.
  const enviar = (form, accion) => form.addEventListener('submit', async (ev) => {
    ev.preventDefault();
    const boton = form.querySelector('button[type="submit"]');
    boton.disabled = true;
    mensaje(form, 'Procesando…');
    try {
      await accion(new FormData(form), form);
    } catch (e) {
      if (e.codigo === 'token') { cerrarSesion(); }
      else mensaje(form, e.message, 'error');
    } finally {
      boton.disabled = false;
    }
  });

  // ---- vistas --------------------------------------------------------------
  const mostrarAcceso = () => { $('vista-acceso').hidden = false; $('vista-cuenta').hidden = true; };
  const cerrarSesion = () => { guardarSesion(null); $('aviso-promo').hidden = true; mostrarAcceso(); };

  const pintarPerfil = (p) => {
    $('cuenta-email').textContent = p.email;
    const lic = p.licencia;
    const etiquetas = { activa: 'Activa', sin_licencia: 'Sin licencia', caducada: 'Caducada', revocada: 'Revocada' };
    $('lic-estado').textContent = etiquetas[lic.estado] || lic.estado;
    $('lic-estado').className = 'cuenta-badge ' + lic.estado;
    const datos = $('lic-datos');
    datos.replaceChildren();
    const fila = (k, v) => { const dt = document.createElement('dt'); dt.textContent = k; const dd = document.createElement('dd'); dd.textContent = v; datos.append(dt, dd); };
    if (lic.clave) fila('Clave', lic.clave);
    if (lic.estado === 'activa') {
      fila('Vigencia', lic.expira ? 'hasta el ' + fecha(lic.expira) : 'sin caducidad');
      fila('Equipos', String(lic.max_equipos));
    }
    const necesitaClave = lic.estado !== 'activa';
    $('form-clave').hidden = !necesitaClave;
    $('lic-nota').textContent = lic.estado === 'activa'
      ? 'Ya puedes iniciar sesión en la aplicación con tu correo y contraseña.'
      : lic.estado === 'sin_licencia'
        ? 'Introduce tu clave aquí o en la aplicación, después de iniciar sesión.'
        : 'Tu licencia ya no es válida. Puedes activar una clave nueva.';
    const f = $('form-perfil');
    f.nombre.value = p.nombre; f.pais.value = p.pais; f.empresa.value = p.empresa;
    const ul = $('lista-equipos');
    ul.replaceChildren();
    if (!p.equipos.length) {
      const li = document.createElement('li'); li.textContent = 'Aún no has usado la aplicación en ningún equipo.'; ul.appendChild(li);
    }
    p.equipos.forEach((e) => {
      const li = document.createElement('li');
      const n = document.createElement('span'); n.textContent = e.nombre || 'Equipo';
      const u = document.createElement('span'); u.textContent = e.conectado ? 'conectado' : hace(e.ultimo); if (e.conectado) u.className = 'on';
      li.append(n, u); ul.appendChild(li);
    });
  };

  const cargarCuenta = async () => {
    try {
      pintarPerfil(await conToken('/api/cuenta/perfil'));
      $('vista-acceso').hidden = true; $('vista-cuenta').hidden = false;
    } catch (e) {
      cerrarSesion();
      if (e.codigo === 'red') mensaje($('form-login'), e.message, 'error');
    }
  };
  const iniciar = (datos) => { guardarSesion({ token: datos.token, exp: datos.exp }); return cargarCuenta(); };

  // ---- pestañas ------------------------------------------------------------
  const pestana = (cual) => {
    const login = cual === 'login';
    $('tab-login').setAttribute('aria-selected', login); $('tab-alta').setAttribute('aria-selected', !login);
    $('form-login').hidden = !login; $('form-alta').hidden = login;
  };
  $('tab-login').addEventListener('click', () => pestana('login'));
  $('tab-alta').addEventListener('click', () => pestana('alta'));
  if (location.hash === '#crear') pestana('alta');

  // ---- formularios ---------------------------------------------------------
  enviar($('form-login'), async (f, form) => {
    const email = String(f.get('email')).trim(), password = String(f.get('password'));
    if (!email || !password) throw new Error('Introduce tu correo y tu contraseña.');
    const datos = await api('/api/cuenta/login', { email, password });
    form.reset(); mensaje(form, '');
    await iniciar(datos);
  });

  enviar($('form-alta'), async (f, form) => {
    const email = String(f.get('email')).trim(), password = String(f.get('password'));
    if (!email) throw new Error('Introduce tu correo.');
    if (password.length < 8) throw new Error('La contraseña debe tener al menos 8 caracteres.');
    if (password !== String(f.get('password2'))) throw new Error('Las contraseñas no coinciden.');
    const datos = await api('/api/registro', { email, password });
    form.reset();
    if (datos.pendiente) {            // servidor apagado: el buzón guardó el correo, sin cuenta todavía
      mensaje(form, datos.mensaje || 'Ahora mismo no podemos crear cuentas. Hemos guardado tu correo y, '
        + 'mientras queden plazas de la promoción, te enviaremos tu clave de licencia por correo en un plazo máximo de 24 a 48 horas.', 'ok');
      return;
    }
    mensaje(form, '');
    await iniciar(datos);
    $('aviso-promo').hidden = !datos.promo;
  });

  // ---- clave de licencia: los guiones se añaden solos al teclear o pegar ----------
  const PREFIJO = 'QPB';
  const formatearClave = (texto) => {
    const limpio = String(texto).toUpperCase().replace(/[^A-Z0-9]/g, '');
    if (!limpio) return '';
    if (PREFIJO.startsWith(limpio)) return limpio;            // «Q», «QP», «QPB» a medio escribir
    const cuerpo = (limpio.startsWith(PREFIJO) ? limpio.slice(PREFIJO.length) : limpio).slice(0, 16);
    const grupos = cuerpo.match(/.{1,4}/g) || [];
    return PREFIJO + (grupos.length ? '-' + grupos.join('-') : '');
  };
  const campoClave = $('form-clave').elements.clave;
  campoClave.addEventListener('input', () => {
    const antes = campoClave.value;
    const caretAlFinal = campoClave.selectionStart === antes.length;
    // letras/dígitos a la izquierda del cursor (para recolocarlo tras reformatear)
    const previos = antes.slice(0, campoClave.selectionStart).toUpperCase().replace(/[^A-Z0-9]/g, '').length;
    const despues = formatearClave(antes);
    if (despues === antes) return;
    campoClave.value = despues;
    let pos = despues.length;
    if (!caretAlFinal) {
      const anadidoPrefijo = !antes.toUpperCase().replace(/[^A-Z0-9]/g, '').startsWith(PREFIJO)
        && despues.startsWith(PREFIJO) ? PREFIJO.length : 0;
      let vistos = 0;
      pos = 0;
      while (pos < despues.length && vistos < previos + anadidoPrefijo) {
        if (/[A-Z0-9]/.test(despues[pos])) vistos++;
        pos++;
      }
    }
    try { campoClave.setSelectionRange(pos, pos); } catch (e) { /* tipos de campo sin selección */ }
  });

  enviar($('form-clave'), async (f, form) => {
    const clave = String(f.get('clave')).trim().toUpperCase();
    if (!clave) throw new Error('Introduce tu clave de licencia.');
    await conToken('/api/cuenta/activar', { clave });
    form.reset();
    await cargarCuenta();
    mensaje(form, 'Licencia activada.', 'ok');
  });

  enviar($('form-perfil'), async (f, form) => {
    await conToken('/api/cuenta/guardar', {
      nombre: String(f.get('nombre')), pais: String(f.get('pais')), empresa: String(f.get('empresa')),
    });
    mensaje(form, 'Perfil guardado.', 'ok');
  });

  enviar($('form-password'), async (f, form) => {
    const nueva = String(f.get('nueva'));
    if (nueva.length < 8) throw new Error('La contraseña nueva debe tener al menos 8 caracteres.');
    await conToken('/api/cuenta/password', { actual: String(f.get('actual')), nueva });
    form.reset();
    mensaje(form, 'Contraseña cambiada.', 'ok');
  });

  $('btn-salir').addEventListener('click', cerrarSesion);

  sesion = leerSesion();
  if (sesion) cargarCuenta(); else mostrarAcceso();
})();
