#!/usr/bin/env sh
# Renderiza los carteles HTML de redes/ a PNG con Chromium sin interfaz.
# Uso: sh redes/renderizar.sh  (desde la raíz del repositorio)
# Requiere Chromium; define CHROMIUM si no está en la ruta por defecto.
set -e
CHROMIUM="${CHROMIUM:-$(ls /opt/pw-browsers/chromium_headless_shell-*/chrome-linux/headless_shell 2>/dev/null | head -1)}"
CHROMIUM="${CHROMIUM:-$(command -v chromium || command -v google-chrome)}"
ROOT="$(cd "$(dirname "$0")/.." && pwd)"

render() { # html  formato  ancho  alto  salida
  "$CHROMIUM" --no-sandbox --hide-scrollbars --allow-file-access-from-files \
    --force-device-scale-factor=1 --window-size="$3,$4" \
    --screenshot="$5" "file://$ROOT/$1?f=$2" >/dev/null 2>&1
  echo "→ $5"
}

DIR="$ROOT/redes/01-presentacion"
render redes/01-presentacion/cartel.html vertical 1080 1350 "$DIR/cartel-1080x1350.png"
render redes/01-presentacion/cartel.html cuadrado 1080 1080 "$DIR/cartel-1080x1080.png"
