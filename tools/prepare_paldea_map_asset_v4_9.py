from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]
assets = ROOT / 'app/src/main/assets'
maps = assets / 'assets/maps'
ui45 = assets / 'assets/ui45'
maps.mkdir(parents=True, exist_ok=True)
image = maps / 'paldea-correct-order.jpg'
legacy = maps / 'paldea-correct-order.jpg.b64'
source = ui45 / 'paldea-map.jpg'

# Reuse the Paldea artwork already synchronized earlier in the same build.
# This keeps CI deterministic and avoids an extra external request.
if not source.exists() or source.stat().st_size < 10000:
    raise RuntimeError('Synced local Paldea artwork is missing or invalid')
shutil.copyfile(source, image)
# Prevent the obsolete truncated text transport from overwriting the image
# in the following v4.9 patch step.
if legacy.exists():
    legacy.unlink()
print(f'Paldea map asset prepared from synced local artwork: {image.stat().st_size} bytes')
