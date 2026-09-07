from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
maps = ROOT / 'app/src/main/assets/assets/maps'
maps.mkdir(parents=True, exist_ok=True)
image = maps / 'paldea-correct-order.jpg'
bad_source = maps / 'paldea-correct-order.jpg.b64'

# Stable guide artwork used as the local base map. The app adds its own
# 19 interactive hotspots, level/progress UI and completion state on top.
url = 'https://www.powerpyx.com/wp-content/uploads/pokemon-scarlet-violet-all-gym-leaders-titans-team-star.jpg'
req = Request(url, headers={'User-Agent': 'Mozilla/5.0 LivingDexHub/4.9'})
with urlopen(req, timeout=30) as response:
    data = response.read()

if not data.startswith(b'\xff\xd8\xff') or len(data) < 20000:
    raise RuntimeError('Paldea map download is not a valid JPEG')

image.write_bytes(data)
# Prevent the obsolete text transport from overwriting the validated image.
if bad_source.exists():
    bad_source.unlink()

print(f'Paldea map asset prepared: {len(data)} bytes')
