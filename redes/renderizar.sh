#!/usr/bin/env sh
# Renderiza los carteles HTML de redes/ a PNG con Chromium sin interfaz.
# Uso: sh redes/renderizar.sh  (desde la raíz del repositorio)
# Requiere Chromium; define CHROMIUM si no está en la ruta por defecto.
set -e
CHROMIUM="${CHROMIUM:-$(ls /opt/pw-browsers/chromium_headless_shell-*/chrome-linux/headless_shell 2>/dev/null | head -1)}"
CHROMIUM="${CHROMIUM:-$(command -v chromium || command -v google-chrome)}"
ROOT="$(cd "$(dirname "$0")/.." && pwd)"

url() { # html[?parámetros]  formato
  case "$1" in *\?*) echo "file://$ROOT/$1&f=$2" ;; *) echo "file://$ROOT/$1?f=$2" ;; esac
}

render() { # html[?parámetros]  formato  ancho  alto  salida
  "$CHROMIUM" --no-sandbox --hide-scrollbars --allow-file-access-from-files \
    --force-device-scale-factor=1 --window-size="$3,$4" \
    --screenshot="$5" "$(url "$1" "$2")" >/dev/null 2>&1
  echo "→ $5"
}

DIR="$ROOT/redes/01-presentacion"
render redes/01-presentacion/cartel.html vertical 1080 1350 "$DIR/cartel-1080x1350.png"
render redes/01-presentacion/cartel.html cuadrado 1080 1080 "$DIR/cartel-1080x1080.png"
render redes/01-presentacion/cartel.html tiktok 1080 1920 "$DIR/cartel-1080x1920.png"

DIR="$ROOT/redes/03-licencia-de-por-vida"
render redes/03-licencia-de-por-vida/cartel.html vertical 1080 1350 "$DIR/cartel-1080x1350.png"
render redes/03-licencia-de-por-vida/cartel.html cuadrado 1080 1080 "$DIR/cartel-1080x1080.png"
render redes/03-licencia-de-por-vida/cartel.html historia 1080 1920 "$DIR/cartel-1080x1920.png"

DIR="$ROOT/redes/04-backtesting-carrusel"
for s in 1 2 3 4 5 6 7 8; do
  render "redes/04-backtesting-carrusel/carrusel.html?s=$s" vertical 1080 1350 "$DIR/vertical-$s.png"
  render "redes/04-backtesting-carrusel/carrusel.html?s=$s" historia 1080 1920 "$DIR/historia-$s.png"
done

# La misma serie como 6 publicaciones independientes (MAE y MFE juntas en la diapositiva 34)
mkdir -p "$DIR/sueltas"
n=0
for s in 1 2 34 5 6 7; do
  n=$((n + 1))
  render "redes/04-backtesting-carrusel/carrusel.html?s=$s&modo=suelta&n=$n&de=6" vertical 1080 1350 "$DIR/sueltas/post-$n-vertical.png"
  render "redes/04-backtesting-carrusel/carrusel.html?s=$s&modo=suelta&n=$n&de=6" historia 1080 1920 "$DIR/sueltas/post-$n-tiktok.png"
done

DIR="$ROOT/redes/05-acceso-anticipado"
render redes/05-acceso-anticipado/cartel.html tiktok 1080 1920 "$DIR/cartel-1080x1920.png"
render redes/05-acceso-anticipado/cartel.html vertical 1080 1350 "$DIR/cartel-1080x1350.png"

DIR="$ROOT/redes/06-anuncio-articulo"
render redes/06-anuncio-articulo/cartel.html tiktok 1080 1920 "$DIR/cartel-1080x1920.png"
render redes/06-anuncio-articulo/cartel.html vertical 1080 1350 "$DIR/cartel-1080x1350.png"

DIR="$ROOT/redes/07-articulo-publicado"
render redes/07-articulo-publicado/cartel.html tiktok 1080 1920 "$DIR/cartel-1080x1920.png"
render redes/07-articulo-publicado/cartel.html vertical 1080 1350 "$DIR/cartel-1080x1350.png"

DIR="$ROOT/redes/08-descargar-datos"
for s in 1 2 3; do
  render "redes/08-descargar-datos/publicacion.html?s=$s" vertical 1080 1350 "$DIR/vertical-$s.png"
  render "redes/08-descargar-datos/publicacion.html?s=$s" tiktok 1080 1920 "$DIR/tiktok-$s.png"
done

DIR="$ROOT/redes/09-anuncio-niveles"
render redes/09-anuncio-niveles/cartel.html tiktok 1080 1920 "$DIR/cartel-1080x1920.png"
render redes/09-anuncio-niveles/cartel.html vertical 1080 1350 "$DIR/cartel-1080x1350.png"

DIR="$ROOT/redes/10-niveles-de-datos"
for s in 1 2 3 4 5; do
  render "redes/10-niveles-de-datos/publicacion.html?s=$s" vertical 1080 1350 "$DIR/vertical-$s.png"
  render "redes/10-niveles-de-datos/publicacion.html?s=$s" tiktok 1080 1920 "$DIR/tiktok-$s.png"
done

DIR="$ROOT/redes/11-futuros-1min"
render redes/11-futuros-1min/cartel.html tiktok 1080 1920 "$DIR/cartel-1080x1920.png"
render redes/11-futuros-1min/cartel.html vertical 1080 1350 "$DIR/cartel-1080x1350.png"

DIR="$ROOT/redes/12-descarga-licencia"
render redes/12-descarga-licencia/cartel.html tiktok 1080 1920 "$DIR/cartel-1080x1920.png"
render redes/12-descarga-licencia/cartel.html vertical 1080 1350 "$DIR/cartel-1080x1350.png"

DIR="$ROOT/redes/13-novedades-v08"
for s in 1 2 3 4 5 6 7; do
  render "redes/13-novedades-v08/publicacion.html?s=$s" vertical 1080 1350 "$DIR/vertical-$s.png"
  render "redes/13-novedades-v08/publicacion.html?s=$s" tiktok 1080 1920 "$DIR/tiktok-$s.png"
done
# El vídeo se genera aparte con: node redes/13-novedades-v08/video/grabar.js

DIR="$ROOT/redes/15-ordenes-limite"
for s in 1 2 3 4 5 6 7 8; do
  render "redes/15-ordenes-limite/publicacion.html?s=$s" vertical 1080 1350 "$DIR/vertical-$s.png"
  render "redes/15-ordenes-limite/publicacion.html?s=$s" tiktok 1080 1920 "$DIR/tiktok-$s.png"
done
