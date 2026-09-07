from pathlib import Path

p = Path(__file__).resolve().parents[1] / 'app' / 'src' / 'main' / 'assets' / 'index.html'
s = p.read_text(encoding='utf-8')

old = "['Data Pack sem overclaim',embeddedDexStatus().complete===false]"
new = "['Data Pack físico 12/12',embeddedDexStatus().complete===true]"
if old not in s:
    raise SystemExit('Teste legado do Data Pack não encontrado; revisar o QA antes de prosseguir.')
s = s.replace(old, new, 1)

# Smoke test must run after the local-first data structures have had a chance to initialize.
s = s.replace("setTimeout(()=>runRuntimeSmokeTest(),700)", "setTimeout(()=>runRuntimeSmokeTest(),1600)", 1)

p.write_text(s, encoding='utf-8')
print('Runtime QA atualizado para Data Pack físico 12/12.')
