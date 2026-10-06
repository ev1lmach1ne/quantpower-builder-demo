# QuantPower Builder — Web de portfolio

**Analiza y construye tu ventaja.** Una landing de QuantPower Systems para
presentar el constructor visual, el motor de backtesting y el flujo completo
de investigación cuantitativa.

- Web: <https://quantpowerbuilder.com/>
- Versiones públicas: <https://github.com/ev1lmach1ne/quantpower-builder-demo/releases>

## Estructura

```text
index.html                 Contenido, navegación y estructura accesible
assets/css/tokens.css      Paleta y tokens del tema Noche del software
assets/css/site.css        Componentes y adaptación a distintos tamaños
assets/css/analyzer.css    Analizador interactivo e identidad corporativa
assets/js/analyzer.js      Curvas Día/Semana/Mes/Año, cursor y selección de tramo
assets/js/builder.js       Constructor visual ilustrativo
assets/js/gallery.js       Indicadores, capital y tabla de operaciones
assets/js/releases.js      Consulta de la última Release pública
assets/js/ui.js            Navegación, pestañas y ejemplo de exportación
assets/images/             Ilustraciones originales y vista para redes
content/examples.json      Operaciones y métricas de los ejemplos sintéticos
content/demo-h1.csv        Serie sintética reproducible, OHLC H1 en UTC
content/analyzer.json      Curvas del Analizador con su metodología y muestra
content/analizador-h1.csv   Serie sintética H1 de seis años, con retornos log
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

3. Crea una Release en el repositorio público `quantpower-builder-demo` y
   adjunta el ZIP completo con uno de los nombres indicados. Incluye notas de
   versión e instrucciones de actualización. Se admiten versiones estables y
   alpha. El repositorio privado conserva las Releases internas; si publicas
   en ambos repositorios, adjunta el portable revisado también a la Release
   pública. Un borrador no aparece en el selector.

El selector muestra las Releases públicas con su fecha, incluidas las versiones
alpha, y avisa si a alguna le falta el ZIP. La versión publicada más reciente
con ZIP compatible aparece seleccionada por defecto. Al elegir una versión
anterior se actualizan el tamaño, la fecha, las notas y la descarga. La lista
se consulta automáticamente en el repositorio público: al publicar una versión,
aparece en el selector sin editar el HTML. Los borradores no se ofrecen para
descarga.

Al publicar una Release en el repositorio demo, el workflow de Pages
lee automáticamente su ZIP y actualiza la referencia local de la versión
vigente. Este respaldo permite seguir descargando la última demo si la API
pública de Releases no responde. No hace falta editar el HTML ni copiar el ZIP
a la carpeta de GitHub Pages: adjúntalo una vez a la Release pública.

El HTML mantiene un enlace nativo de descarga sin depender de JavaScript ni de
la API. Cuando se publica una Release, el workflow fija en el HTML la URL exacta
de su ZIP y actualiza la versión de respaldo; así también funciona una alpha y
la descarga continúa disponible si falla la API. Mientras se consulta GitHub,
el botón nunca queda inactivo. Si una Release publicada no incluye el ZIP, se
mantiene disponible el respaldo anterior y la lista indica que falta el paquete.

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
como JavaScript. Cambiar la lógica, el periodo o el riesgo carga inmediatamente
los resultados de esa combinación, conservando la vista de gráfico, capital
u operaciones. El constructor y las pestañas de resultados comparten la
selección, y cada lógica recuerda sus parámetros. «Ver el ejemplo» lleva a la
galería y abre el gráfico de la configuración seleccionada.

El TPO se genera con `_perfiles_tpo()` y el mismo perfil `CRYPTO_24_7` usado
por sus señales: una sesión diaria de 00:00 a 24:00 UTC, letras de 60 minutos
y área de valor del 70 %. Cada sesión tiene su mapa de calor compacto, sin
solaparse con la siguiente: las celdas se alinean por nivel de precio y
conservan el gradiente temporal rojo/naranja/amarillo y la intensidad de la
GUI. El POC actual es rojo; VAH/VAL actuales son grises y las referencias
del perfil anterior se distinguen con líneas punteadas. Una última sesión
incompleta se identifica como «En formación».

Las ampliaciones TPO incluyen la sesión de referencia anterior y las sesiones
de la operación. Recortan los perfiles calculados sobre el histórico completo,
sin recalcular sus filas ni letras al hacer zoom. Son perfiles visuales al
cierre de cada sesión; las señales usan únicamente el perfil anterior cerrado.

### Contrato de ejecución

- Serie OHLC H1 en UTC; 50 velas de calentamiento sin entradas.
- Señal calculada con la vela cerrada `t` y entrada al open de `t+1`.
- Stop inicial fijo: 1,5 × ATR(14) de `t`.
- Objetivo: 2 × distancia inicial al stop (RR 1:2).
- Dimensionamiento por riesgo nominal del 0,5 %, 1 % o 2 % según el selector.
- Comisión: 0,05 % por lado; slippage: 0,02 % en entradas y salidas a mercado.
  Stop/TP se llenan a su nivel sin slippage adicional; un gap de stop usa el open.
- Salidas por condición al open siguiente; stop/TP en su vela de activación.
- Las salidas intrabar describen la vela y su precio, sin inventar un instante
  de tick que no existe en OHLC.
- Curvas, drawdown, tabla, zoom e inspector comparten las mismas operaciones.

Los cruces y las confirmaciones son visibles en el inspector. El zoom conserva
los indicadores calculados sobre todo el histórico, no los reinicia en su ventana.
El CSV de la serie sintética se puede descargar desde la galería.

## Analizador e identidad corporativa

La sección **Analizador** presenta un ejemplo de Intradía con los mismos
cálculos de `core.metrics.curvas_cambio_acumulado()` y el lenguaje visual de
`gui/widgets/analisis_graficos.py`: curva verde/roja, rombo del total, cambio
medio por paso y botones Día/Semana/Mes/Año.

El histórico del ejemplo es sintético, H1, UTC, 24/7, de 2018 a 2023 con la
frontera final de 2024. Contiene 52.585 observaciones y aporta 2.191 días,
313 semanas, 72 meses y 6 años completos. La última agrupación en curso se
excluye como en la aplicación. El promedio usa retornos **logarítmicos**
acumulados × 100; no se presenta como rentabilidad compuesta.

El cursor consulta valores y la selección de rango calcula `y(fin) − y(inicio)`
en puntos porcentuales. Puede hacerse mediante arrastre o con los selectores
Inicio/Fin; la consulta admite teclado. Se publican datos y SVG estáticos de
respaldo, no el código de cálculo del software.

```powershell
venv\Scripts\python.exe web\tools\generar_analizador.py
venv\Scripts\python.exe web\tools\preparar_marca.py
```

La imagen corporativa de la cabecera, presentación y pie procede de
`gui/assets/logo_inicio.png`, con una copia web optimizada que respeta su
composición y proporciones.

## Verificación en el proyecto de desarrollo

```powershell
venv\Scripts\python.exe -m pytest tests/test_web_motor.py tests/test_web_tpo.py tests/test_web_analizador.py tests/test_cambio_acumulado.py tests/test_web_publicacion.py -q -o addopts=''
python web\tools\verificar_web.py --salida "RUTA_TEMPORAL"
python web\tools\verificar_descarga.py --salida "RUTA_TEMPORAL"
```

La verificación de navegador utiliza Playwright con Microsoft Edge para comprobar tamaños,
interacciones, recursos, navegación por teclado y distintos estados de la
API de Releases. Guarda capturas de escritorio y móvil en la carpeta indicada.
Comprueba el clic real y el evento nativo de descarga, con y sin JavaScript;
cancela la transferencia después de comprobar el nombre del ZIP, evitando
descargar 391 MiB en cada ejecución.
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
