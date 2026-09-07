from pathlib import Path
import base64

ROOT = Path(__file__).resolve().parents[1]
maps = ROOT / 'app/src/main/assets/assets/maps'
maps.mkdir(parents=True, exist_ok=True)
image = maps / 'paldea-correct-order.jpg'
source = maps / 'paldea-correct-order.jpg.b64'

# Build deterministically from the bundled repository asset. This avoids
# external-network/certificate failures during CI and keeps the APK offline.
if not source.exists():
    raise RuntimeError('Bundled Paldea map source is missing')

text = ''.join(source.read_text(encoding='utf-8').split())
text += '=' * (-len(text) % 4)
data = base64.b64decode(text)
if not data.startswith(b'\xff\xd8\xff') or len(data) < 10000:
    raise RuntimeError('Bundled Paldea map source is not a valid JPEG')

image.write_bytes(data)
print(f'Paldea map asset prepared locally: {len(data)} bytes')
