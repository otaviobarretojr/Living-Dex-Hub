from pathlib import Path
root=Path(__file__).resolve().parents[1]
html=(root/'app/src/main/assets/index.html').read_text(encoding='utf-8')
java=(root/'app/src/main/java/com/otaviobarreto/livingdex/MainActivity.java').read_text(encoding='utf-8')
gradle=(root/'app/build.gradle').read_text(encoding='utf-8')
checks={
 'marker':'living-dex-reference-ui" content="4.0"' in html,
 'reference-class':'reference-v4' in html,
 'light-theme':'--r4-bg:#f7f8fb' in html,
 'coral-accent':'--r4-red:#ff5555' in html,
 'reference-appbar':'function r4Appbar' in html,
 'content-first-home':'function r4Home' in html,
 'hero-map':"url('assets/maps/paldea-route.svg')" in html,
 'three-item-nav':'grid-template-columns:repeat(3,1fr)' in html,
 'animations':'@keyframes r4View' in html and '@keyframes r4Sheet' in html,
 'light-android-bg':'Color.rgb(247, 248, 251)' in java,
 'light-status-icons':'SYSTEM_UI_FLAG_LIGHT_STATUS_BAR' in java,
 'light-nav-icons':'SYSTEM_UI_FLAG_LIGHT_NAVIGATION_BAR' in java,
 'audio-resume':'ldhAndroidResumeAudio' in java,
 'version':'versionName \'4.3.0\'' in gradle and 'versionCode 55' in gradle,
 'no-old-windowinsets':'installSafeInsets' not in java and 'WindowInsets.Type.navigationBars' not in java,
}
for k,v in checks.items(): print(('PASS' if v else 'FAIL'),k)
missing=[k for k,v in checks.items() if not v]
if missing: raise SystemExit('Reference UI validation failed: '+', '.join(missing))
print(f'Reference UI validated: {len(checks)}/{len(checks)}')
