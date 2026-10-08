# Contenido para redes

Cada publicación vive en su carpeta numerada con:

- `cartel.html`: diseño editable del cartel (usa los colores del tema Noche y
  el logotipo de `assets/images/`).
- `cartel-1080x1350.png` y `cartel-1080x1080.png`: imágenes listas para subir.
- `texto-post.md`: texto del post por red social, con enlaces y hashtags.

Para regenerar los PNG después de editar un `cartel.html`, desde la raíz:

```sh
sh redes/renderizar.sh
```

Necesita Chromium (o Chrome); si no lo encuentra, indica su ruta con
`CHROMIUM=/ruta/a/chrome sh redes/renderizar.sh`. En Windows también puedes
abrir el HTML en el navegador, ajustar la ventana y hacer una captura.

Ten en cuenta que esta carpeta se publica con el resto del sitio en GitHub Pages.
