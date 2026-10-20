"""Usa una grabación propia como voz en off, cortada con las marcas de tiempo por palabra de la transcripción.
Uso: python3 scripts/voz_propia.py grabacion.m4a voz-propia/
La carpeta debe tener:
- transcripcion.json: salida de faster-whisper (segmentos con palabras y tiempos).
- bloques.json: [{id, titulo, rango: [primera palabra, última palabra + 1]}] en el orden del vídeo.
- correcciones.json: {índice de palabra: texto del subtítulo} para arreglar nombres, puntuación o errores.
Procesado: limpieza de ruido, tono algo más grave (-1,4 semitonos, conservando formantes), un 4 % más rápida,
presencia de locutor, de-esser, compresión y volumen normalizado. Escribe src/tiempos.json con las palabras y
el momento en que suena cada una, para iluminar el subtítulo a la vez que la voz."""
import json, subprocess, sys
src, carpeta = sys.argv[1:3]
TEMPO = 1.04
palabras = [w for s in json.load(open(f'{carpeta}/transcripcion.json')) for w in s['words']]
bloques = json.load(open(f'{carpeta}/bloques.json'))
corr = {int(k): v for k, v in json.load(open(f'{carpeta}/correcciones.json')).items() if not k.startswith('_')}
FILTRO = ('highpass=f=80,afftdn=nf=-28,'
          f'rubberband=pitch=0.92:tempo={TEMPO}:formant=preserved,'
          'equalizer=f=180:t=q:w=1:g=2,equalizer=f=3500:t=q:w=1.2:g=3,deesser,'
          'acompressor=threshold=-20dB:ratio=3:attack=5:release=80,loudnorm=I=-16:TP=-1.5')
tiempos = []
for b in bloques:
    a, z = b['rango']
    ini = palabras[a]['s'] - 0.2
    if a > 0: ini = max(ini, palabras[a - 1]['e'] + 0.05)
    fin = palabras[z - 1]['e'] + 0.3
    if z < len(palabras): fin = min(fin, palabras[z]['s'] - 0.05)
    out = f"public/voz/{b['id']}.wav"
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{ini:.3f}', '-to', f'{fin:.3f}', '-i', src,
                    '-af', FILTRO, '-ar', '48000', '-ac', '1', out], check=True)
    d = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', out],
                             capture_output=True, text=True).stdout)
    pal = []
    for i in range(a, z):
        texto = corr.get(i, palabras[i]['w'].strip())
        if texto:
            pal.append(dict(w=texto, t=round((palabras[i]['s'] - ini) / TEMPO, 3)))
    tiempos.append(dict(id=b['id'], titulo=b['titulo'], texto=' '.join(p['w'] for p in pal),
                        audio=f"voz/{b['id']}.wav", dur=round(d, 3), palabras=pal))
json.dump(tiempos, open('src/tiempos.json', 'w'), ensure_ascii=False, indent=1)
for t in tiempos: print(f"{t['id']:13s} {t['dur']:5.2f} s | {t['texto']}")
print('total', round(sum(t['dur'] for t in tiempos), 1), 's')
