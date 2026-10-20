#!/usr/bin/env sh
# Genera la voz en off de cada escena con SVOX Pico (es-ES, sin conexión) y escribe src/tiempos.json.
# Requiere: libttspico-utils, ffmpeg y python3. Uso: sh scripts/voz.sh
set -e
cd "$(dirname "$0")/.."
mkdir -p public/voz
python3 - <<'PY'
import json, subprocess
g = json.load(open('scripts/guion.json'))
tiempos = []
for e in g:
    raw = f"/tmp/voz-{e['id']}.wav"
    subprocess.run(['pico2wave', '-l', 'es-ES', '-w', raw, e['voz']], check=True)
    out = f"public/voz/{e['id']}.wav"
    # Un poco más rápida y con algo de presencia; 48 kHz para Remotion
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', raw, '-af',
                    'atempo=1.08,highpass=f=80,acompressor=threshold=-18dB:ratio=3,loudnorm=I=-16:TP=-1.5',
                    '-ar', '48000', '-ac', '1', out], check=True)
    d = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', out],
                             capture_output=True, text=True).stdout)
    tiempos.append(dict(id=e['id'], titulo=e['titulo'], texto=e['texto'], audio=f"voz/{e['id']}.wav", dur=round(d, 3)))
json.dump(tiempos, open('src/tiempos.json', 'w'), ensure_ascii=False, indent=1)
for t in tiempos: print(f"{t['id']:13s} {t['dur']:5.2f} s")
print('total voz', round(sum(t['dur'] for t in tiempos), 1), 's')
PY
