#!/usr/bin/env sh
# Genera la voz en off de cada escena con Kokoro-82M v1.0 (voz neuronal, en local) y escribe src/tiempos.json.
# Requisitos: espeak-ng, ffmpeg, python3 con onnxruntime, numpy y soundfile, y una carpeta KOKORO_DIR con:
#   kokoro-v1.0-q8.onnx                          (paquete npm kokoro-q8-shards, partes unidas)
#   kjs/package/voices/*.bin                     (paquete npm kokoro-js)
#   package/kokoro-int8-en-v0_19/tokens.txt      (vocabulario de fonemas)
# Uso: KOKORO_DIR=/ruta VOZ=ef_dora sh scripts/voz.sh
set -e
cd "$(dirname "$0")/.."
: "${KOKORO_DIR:?Define KOKORO_DIR}"
VOZ="${VOZ:-ef_dora}"
mkdir -p public/voz
python3 - "$KOKORO_DIR" "$VOZ" <<'PY'
import json, subprocess, sys
kdir, voz = sys.argv[1:3]
g = json.load(open('scripts/guion.json'))
tiempos = []
for e in g:
    raw = f"/tmp/voz-{e['id']}.wav"
    subprocess.run(['python3', 'scripts/kokoro_tts.py', kdir, voz, e['voz'], raw, '1.1'], check=True, capture_output=True)
    out = f"public/voz/{e['id']}.wav"
    # Recorta silencios del principio y del final, normaliza y pasa a 48 kHz para Remotion
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', raw, '-af',
                    'silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse,'
                    'loudnorm=I=-16:TP=-1.5', '-ar', '48000', '-ac', '1', out], check=True)
    d = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', out],
                             capture_output=True, text=True).stdout)
    tiempos.append(dict(id=e['id'], titulo=e['titulo'], texto=e['texto'], audio=f"voz/{e['id']}.wav", dur=round(d, 3)))
json.dump(tiempos, open('src/tiempos.json', 'w'), ensure_ascii=False, indent=1)
for t in tiempos: print(f"{t['id']:13s} {t['dur']:5.2f} s")
print('total voz', round(sum(t['dur'] for t in tiempos), 1), 's')
PY
