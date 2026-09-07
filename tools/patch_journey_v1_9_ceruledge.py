from pathlib import Path
p=Path(__file__).resolve().parents[1]/'app'/'src'/'main'/'assets'/'index.html'
s=p.read_text(encoding='utf-8')
js=r'''
// Journey 1.9 — Violet-specific Ceruledge build.
SV_BUILDS[937]={name:'Ceruledge',role:'Atacante físico Fire / Ghost',nature:'Adamant',ability:'Flash Fire',item:'Muscle Band',moves:['Bitter Blade','Shadow Claw','Swords Dance','Psycho Cut'],note:'Em Violet, Ceruledge ocupa o slot de Fire. Bitter Blade combina dano e recuperação, enquanto Swords Dance aumenta o poder para confrontos mais longos.'};
'''
if 'Violet-specific Ceruledge build' not in s:
    s=s.replace('</body>','<script>'+js+'</script>\n</body>',1)
p.write_text(s,encoding='utf-8')
print('Ceruledge v1.9 patch applied')
