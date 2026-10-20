"""Voz neuronal Kokoro-82M v1.0 (q8) en español: fonemas con espeak-ng (es) y modelo ONNX local.
Uso: python3 kokoro_tts.py DIR_MODELO VOZ "texto" salida.wav [velocidad]"""
import sys, subprocess, re, numpy as np, onnxruntime as ort, soundfile as sf
d, voz, texto, out = sys.argv[1:5]
vel = float(sys.argv[5]) if len(sys.argv) > 5 else 1.0
vocab = {}
for line in open(f'{d}/package/kokoro-int8-en-v0_19/tokens.txt', encoding='utf-8'):
    s, i = line.rstrip('\n').rsplit(' ', 1)
    vocab[' ' if s == '' else s] = int(i)
def fonemas(t):
    r = subprocess.run(['espeak-ng', '-v', 'es', '-q', '--ipa=3', t], capture_output=True, text=True).stdout
    return re.sub(r'\s+', ' ', r.replace('_', '').replace('\n', ' ')).strip()
# espeak descarta la puntuación: se fonetiza por fragmentos y se vuelve a poner para que haya pausas
partes = re.split(r'([,.;:!?])', texto)
ipa = ''
for t in partes:
    if t in ',.;:!?':
        ipa = ipa.rstrip() + t + ' '
    elif t.strip():
        ipa += fonemas(t) + ' '
ipa = ipa.strip()
ids = [vocab[c] for c in ipa if c in vocab]
estilos = np.fromfile(f'{d}/kjs/package/voices/{voz}.bin', dtype=np.float32).reshape(-1, 1, 256)
sess = ort.InferenceSession(f'{d}/kokoro-v1.0-q8.onnx', providers=['CPUExecutionProvider'])
nombres = {i.name for i in sess.get_inputs()}
feed = {'input_ids': np.array([[0] + ids + [0]], dtype=np.int64), 'style': estilos[len(ids)],
        'speed': np.array([vel], dtype=np.float32)}
wav = sess.run(None, {k: v for k, v in feed.items() if k in nombres})[0].reshape(-1)
sf.write(out, wav, 24000)
print(ipa[:100], '|', len(ids), 'tokens', round(len(wav) / 24000, 2), 's')
