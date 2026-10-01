# QuantPower Builder — Web de portfolio

**Analiza y construye tu ventaja.** Una landing de QuantPower Systems para
presentar el constructor visual, el motor de backtesting y el flujo completo
de investigación cuantitativa.

- Web: <https://ev1lmach1ne.github.io/quantpower-builder-demo/>
- Versiones públicas: <https://github.com/ev1lmach1ne/quantpower-builder-demo/releases>

## Estructura

```text
index.html                 Contenido, navegación y estructura accesible
assets/css/tokens.css      Paleta y tokens del tema Noche del software
assets/css/site.css        Componentes y adaptación a distintos tamaños
assets/js/builder.js       Constructor visual ilustrativo
assets/js/gallery.js       Indicadores, capital y tabla de operaciones
assets/js/releases.js      Consulta de la última Release pública
assets/js/ui.js            Navegación, pestañas y ejemplo de exportación
assets/images/             Ilustraciones originales y vista para redes
content/examples.json      Operaciones y métricas de los ejemplos sintéticos
content/demo-h1.csv        Serie sintética reproducible, OHLC H1 en UTC
content/site.json          Repositorio, nombres del ZIP y referencia opcional
.github/workflows/pages.yml Publicación automática en GitHub Pages
```

La web es estática y no necesita Node, un servidor de aplicaciones ni claves
de API. Utiliza rutas relativas para funcionar bajo la ruta del proyecto de
GitHub Pages. Sirve los archivos mediante HTTP para usar los módulos JavaScript.

## Probar en local

En este proyecto, abre `web/previsualizar.bat` o ejecuta desde la raíz:

```powershell
venv\Scripts\python.exe -m http.server 8765 --bind 127.0.0.1 --directory web
```

Abre <http://127.0.0.1:8765/>. En la copia pública, sirve la raíz del repositorio
con `python -m http.server 8765 --bind 127.0.0.1`.

## Publicación independiente

En el proyecto de desarrollo, la landing está en `web/`. Su exportador copia
exclusivamente HTML, estilos, JavaScript de la web, ilustraciones, contenido
sintético, este README y el workflow de Pages. El software de escritorio se
desarrolla en su repositorio privado.

```powershell
venv\Scripts\python.exe web\tools\exportar_sitio.py --directorio "RUTA_DEL_REPOSITORIO_PUBLICO"
venv\Scripts\python.exe web\tools\exportar_sitio.py --zip "dist\QuantPowerBuilder_Web.zip"
```

Para actualizar una copia pública existente, añade `--actualizar`. Revisa el
diff de esa copia antes de hacer commit y push. El workflow publica la rama
`main`; en Settings → Pages debe estar seleccionado **GitHub Actions**.

## Actualizar la demo descargable

La fuente de versiones es `content/site.json`. Está configurada para el
repositorio público `ev1lmach1ne/quantpower-builder-demo` y reconoce estos assets:

- `QuantPowerBuilder_Windows_x64.zip`
- `QuantPowerSystems_Windows_x64.zip`

1. Genera y comprueba el paquete portable que quieras distribuir. Si parte de
   una Release ya empaquetada, el proyecto incluye una utilidad que conserva
   el ejecutable y sustituye las copias legibles de fuentes por bytecode:

   ```powershell
   venv\Scripts\python.exe web\tools\preparar_demo_publica.py "ZIP_ORIGINAL" "ZIP_PUBLICO" --sha256-original "SHA256_DE_LA_RELEASE"
   ```

   El Python utilizado debe tener el mismo formato de bytecode que el
   intérprete embebido. El bytecode sigue siendo analizable.
2. Revisa que el paquete no entrega fuentes privadas legibles ni configuración
   personal. La utilidad del proyecto de desarrollo es:

   ```powershell
   venv\Scripts\python.exe web\tools\validar_demo.py "RUTA_DEL_ZIP"
   ```

   La revisión permite únicamente los cargadores genéricos conocidos de los
   scripts, con su bytecode adjunto. Verifica también el ejecutable, el
   constructor, los recursos y los resultados de simulación antes de publicar.

3. Crea una Release pública, adjunta el ZIP completo con uno de los nombres
   indicados e incluye notas de versión e instrucciones de actualización.
4. Publica la Release como versión oficial, no como borrador ni prerelease, y
   márcala como **Latest**.

La web consulta la API pública de GitHub y actualiza versión, tamaño, fecha,
descarga y notas sin cambiar su código. Antes de la primera Release muestra
**Demo en preparación**. Si la Release todavía no incluye el ZIP, enlaza a
esa publicación. Si la API no responde, permite consultar las Releases.

### Referencia para cuando la API no responde

`fallbackRelease` puede contener una copia de los campos públicos de una Release:

```json
{
  "tag_name": "vX.Y.Z",
  "html_url": "https://github.com/ev1lmach1ne/quantpower-builder-demo/releases/tag/vX.Y.Z",
  "published_at": "2026-10-01T12:00:00Z",
  "draft": false,
  "prerelease": false,
  "assets": [{
    "name": "QuantPowerBuilder_Windows_x64.zip",
    "state": "uploaded",
    "size": 123456789,
    "browser_download_url": "https://github.com/ev1lmach1ne/quantpower-builder-demo/releases/download/vX.Y.Z/QuantPowerBuilder_Windows_x64.zip"
  }]
}
```

Sustituye los valores de ejemplo por los de una publicación real. La web
identifica esta información como **versión de referencia**. Los enlaces se
validan para pertenecer al repositorio de Releases configurado.

## Ilustraciones y contenido

Las gráficas de operaciones y capital se generan con los indicadores,
`generar_senales_sistema()`, `simular()` y `calcular_metricas()` de la aplicación
sobre una serie sintética de semilla fija. No se colocan operaciones a mano.
Los diagramas de Walk-Forward y Montecarlo se identifican como esquemas
metodológicos. No se consultan históricos o sistemas privados.

```powershell
venv\Scripts\python.exe web\tools\generar_ilustraciones.py
```

El generador usa el entorno Python del proyecto y Pillow; estos no son
requisitos para servir la web. La página sirve 27 combinaciones precalculadas
de periodo/riesgo del constructor y un ejemplo TPO; el motor no se publica
como JavaScript. Cambiar las opciones carga los resultados de esa combinación.

### Contrato de ejecución

- Serie OHLC H1 en UTC; 50 velas de calentamiento sin entradas.
- Señal calculada con la vela cerrada `t` y entrada al open de `t+1`.
- Stop inicial fijo: 1,5 × ATR(14) de `t`.
- Objetivo: 2 × distancia inicial al stop (RR 1:2).
- Dimensionamiento por riesgo nominal del 0,5 %, 1 % o 2 % según el selector.
- Comisión: 0,05 % por lado; slippage: 0,02 % aplicado a los fills.
- Salidas por condición al open siguiente; stop/TP en su vela de activación.
- Las salidas intrabar describen la vela y su precio, sin inventar un instante
  de tick que no existe en OHLC.
- Curvas, drawdown, tabla, zoom e inspector comparten las mismas operaciones.

Los cruces y las confirmaciones son visibles en el inspector. El zoom conserva
los indicadores calculados sobre todo el histórico, no los reinicia en su ventana.
El CSV de la serie sintética se puede descargar desde la galería.

## Verificación en el proyecto de desarrollo

```powershell
venv\Scripts\python.exe -m pytest tests/test_web_motor.py tests/test_web_publicacion.py -q -o addopts=''
python web\tools\verificar_web.py --salida "RUTA_TEMPORAL"
```

La verificación de navegador utiliza Playwright con Microsoft Edge para comprobar tamaños,
interacciones, recursos, navegación por teclado y distintos estados de la
API de Releases. Guarda capturas de escritorio y móvil en la carpeta indicada.
Instala `playwright` en un entorno de verificación independiente; no es una
dependencia del software de escritorio ni de la web publicada. También admite
Chrome mediante `--navegador chrome`.

## Procedencia técnica

La paleta procede del tema `oscuro_noche` en `gui/temas.py`. El contenido del
producto se contrastó con las notas v0.7.6 y la memoria `estado_inicial`, origen
`MEMORIA_INICIAL.json`: `DTC-01` (Numba), `DTC-06` (registro de estrategias),
`RGN-11` y `DTC-08` (optimización IS y validación), y `DEP-07` (scripts externos).

La publicación de un ejecutable puede dificultar la copia directa de fuentes,
pero no elimina la posibilidad de ingeniería inversa.
