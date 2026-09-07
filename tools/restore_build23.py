from pathlib import Path
import base64
import gzip

ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = ROOT / "archive" / "build-23"
OUT = ROOT / "Living_Dex_Hub_Build_23_0.html"

parts = sorted(ARCHIVE.glob("part-*.b64"))
if not parts:
    raise SystemExit("Nenhum snapshot encontrado.")

payload = "".join(p.read_text(encoding="utf-8").strip() for p in parts)
OUT.write_bytes(gzip.decompress(base64.b64decode(payload)))
print(f"Build 23 restaurado em: {OUT}")
