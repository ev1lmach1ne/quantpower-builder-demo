"""Usa una grabación propia como voz en off: la corta en bloques, la procesa y escribe src/tiempos.json.
Uso: python3 scripts/voz_propia.py grabacion.m4a bloques.json cortes.json
- bloques.json: [{id, titulo, texto}] en el orden del vídeo (el texto es el subtítulo).
- cortes.json: {"cortes": [segundos donde empieza cada bloque salvo el primero], "fin": segundos}.
Procesado: limpieza de ruido, tono algo más grave (-1,4 semitonos, conservando formantes), un 4 % más rápida,
presencia de locutor, de-esser, compresión y volumen normalizado."""
import json, subprocess, sys
src, fb, fc = sys.argv[1:4]
bloques = json.load(open(fb)); c = json.load(open(fc))
lim = [0.0] + c['cortes'] + [c['fin']]
FILTRO = ('highpass=f=80,afftdn=nf=-28,'
          'silenceremove=start_periods=1:start_threshold=-40dB,areverse,silenceremove=start_periods=1:start_threshold=-40dB,areverse,'
          'rubberband=pitch=0.92:tempo=1.04:formant=preserved,'
          'equalizer=f=180:t=q:w=1:g=2,equalizer=f=3500:t=q:w=1.2:g=3,deesser,'
          'acompressor=threshold=-20dB:ratio=3:attack=5:release=80,loudnorm=I=-16:TP=-1.5')
tiempos = []
for i, b in enumerate(bloques):
    out = f"public/voz/{b['id']}.wav"
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(lim[i]), '-to', str(lim[i + 1]), '-i', src,
                    '-af', FILTRO, '-ar', '48000', '-ac', '1', out], check=True)
    d = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', out],
                             capture_output=True, text=True).stdout)
    tiempos.append(dict(id=b['id'], titulo=b['titulo'], texto=b['texto'], audio=f"voz/{b['id']}.wav", dur=round(d, 3)))
json.dump(tiempos, open('src/tiempos.json', 'w'), ensure_ascii=False, indent=1)
for t in tiempos: print(f"{t['id']:13s} {t['dur']:5.2f} s")
print('total', round(sum(t['dur'] for t in tiempos), 1), 's')
