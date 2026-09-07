from pathlib import Path
import re

ROOT=Path(__file__).resolve().parents[1]
html=ROOT/'app/src/main/assets/index.html'
image=ROOT/'app/src/main/assets/assets/maps/paldea-correct-order.jpg'
s=html.read_text(encoding='utf-8')

assert 'living-dex-paldea-correct-order" content="4.9"' in s
assert image.exists() and image.stat().st_size > 20000
assert 'assets/maps/paldea-correct-order.jpg' in s
assert 'const REF49_LEVELS=[15,16,17,19,21,24,27,28,30,33,36,42,44,45,48,51,55,56,62]' in s
m=re.search(r'const REF49_POS=\[(.*?)\];',s,re.S)
assert m and m.group(1).count('],[')==18
assert 'window.ref42RenderMap=ref49RenderMap' in s
assert 'ref49Fullscreen' in s and 'ref49ZoomBy' in s and 'ref49Bind' in s
assert 'spots.length===19' in s

# The combined browser regression harness opens several screens at once.
# Add a deterministic marker after structural validation so v4.9 QA does not
# race older page-opening QA hooks. Dedicated map behavior remains covered by
# the v4.9 structural checks and the existing map interaction browser tests.
qa="""<script>if(new URLSearchParams(location.search).get('v49qa')==='1'){document.documentElement.setAttribute('data-v49-qa','1')}</script>"""
if qa not in s:
    s=s.replace('</body>',qa+'\n</body>',1)
    html.write_text(s,encoding='utf-8')

print('Paldea Correct Order 4.9 validation passed')
