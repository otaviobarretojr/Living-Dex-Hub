from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
html=ROOT/'app/src/main/assets/index.html'
java=ROOT/'app/src/main/java/com/otaviobarreto/livingdex/MainActivity.java'
s=html.read_text(encoding='utf-8')
j=java.read_text(encoding='utf-8')

checks={
    'marker':'living-dex-map-import" content="5.0"' in s,
    'file_input':'type="file"' in s and 'accept="image/png,image/jpeg,image/webp,image/*"' in s,
    'indexeddb':'indexedDB.open(REF50_DB,1)' in s and "REF50_KEY='paldea-map'" in s,
    'persistent_apply':'ref50ApplyStored' in s and 'URL.createObjectURL(blob)' in s,
    'reset_default':"assets/maps/paldea-correct-order.jpg" in s and 'ref50ResetMap' in s,
    'import_button':'aria-label="Importar mapa"' in s,
    'size_limit':'18*1024*1024' in s,
    'hotspots_preserved':'REF49_POS' in s and 'ref49-hotspot' in s,
    'android_callback':'onShowFileChooser' in j and 'ValueCallback<Uri[]>' in j,
    'android_result':'onActivityResult' in j and 'FILE_CHOOSER_REQUEST' in j,
}
for k,v in checks.items(): print(('PASS' if v else 'FAIL'),k)
failed=[k for k,v in checks.items() if not v]
assert not failed, failed
print('Map Import 5.0 validation passed')
