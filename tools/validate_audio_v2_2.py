from pathlib import Path
p=Path(__file__).resolve().parents[1]/'app'/'src'/'main'/'assets'/'index.html'
s=p.read_text(encoding='utf-8')
checks={
 'Audio 2.2 marker':'living-dex-audio" content="2.2' in s,
 'Original theme comment':'original ambient theme' in s and 'no Nintendo/Pokemon music samples' in s,
 'Audio prefs':'LDH_AUDIO_KEY' in s and 'ldh_audio_v22' in s,
 'Music toggle':'function ldhToggleMusic' in s and '>Música<' in s,
 'SFX toggle':'function ldhToggleSfx' in s and '>Efeitos<' in s,
 'Volume':'function ldhSetVolume' in s and 'type="range"' in s,
 'First gesture':'pointerdown' in s and 'ldhFirstGesture' in s,
 'Visibility pause':'visibilitychange' in s and 'ldhStopLoop' in s,
 'Capture SFX':"ldhSfx(el.classList.contains('is-owned')?'back':'capture')" in s,
 'Settings panel':'ldhAudioSettings' in s and 'Ambiente do Living Dex Hub' in s,
 'Quick audio button':'ldhAudioQuick' in s,
 'Navigation preserved':'living-dex-navigation" content="2.1' in s,
 'Map preserved':'living-dex-paldea-map" content="2.0' in s,
 'No audio external dependency':'new Audio(' not in s and '<audio' not in s,
}
for k,v in checks.items(): print(('PASS' if v else 'FAIL'),k)
failed=[k for k,v in checks.items() if not v]
if failed: raise SystemExit('Audio 2.2 validation failed: '+', '.join(failed))
print(f'AUDIO 2.2 VALIDADO: {len(checks)}/{len(checks)}')