#!/usr/bin/env python3
from pathlib import Path
import re
R=Path(__file__).resolve().parents[1]
main=(R/'app/src/main/java/com/otaviobarreto/livingdex/MainActivity.java').read_text(encoding='utf-8')
manifest=(R/'app/src/main/AndroidManifest.xml').read_text(encoding='utf-8')
net=(R/'app/src/main/res/xml/network_security_config.xml').read_text(encoding='utf-8')
gradle=(R/'app/build.gradle').read_text(encoding='utf-8')
perms=re.findall(r'<uses-permission[^>]+android:name="([^"]+)"',manifest)
checks={
 'single permission only':perms==['android.permission.INTERNET'],
 'cleartext disabled manifest':'android:usesCleartextTraffic="false"' in manifest,
 'network security linked':'android:networkSecurityConfig="@xml/network_security_config"' in manifest,
 'network config cleartext disabled':'cleartextTrafficPermitted="false"' in net,
 'system trust only':'<certificates src="system"/>' in net,
 'web debugging disabled':'WebView.setWebContentsDebuggingEnabled(false)' in main,
 'mixed content blocked':'MIXED_CONTENT_NEVER_ALLOW' in main,
 'safe browsing enabled':'setSafeBrowsingEnabled(true)' in main,
 'local storage enabled':'setDomStorageEnabled(true)' in main,
 'stable back path':'onBackPressed()' in main and 'androidHandleBack' in main,
 'no risky modern back':'OnBackInvokedDispatcher' not in main,
 'no risky insets migration':'WindowInsetsController' not in main,
 'state restore preserved':'webView.restoreState(state)' in main and 'webView.saveState(outState)' in main,
 'lifecycle preserved':'webView.onResume()' in main and 'webView.onPause()' in main and 'webView.destroy()' in main,
 'target sdk 35':'targetSdk 35' in gradle and 'compileSdk 35' in gradle,
 'min sdk 26':'minSdk 26' in gradle,
 'release signed config':'enableV2Signing true' in gradle and 'enableV3Signing true' in gradle,
}
failed=[k for k,v in checks.items() if not v]
for k,v in checks.items(): print(('OK   ' if v else 'FAIL ')+k)
if failed: raise SystemExit('ANDROID RELEASE AUDIT failed: '+', '.join(failed))
print(f'ANDROID RELEASE AUDIT: {len(checks)}/{len(checks)} checks OK • stable wrapper preserved • no permission creep • network hardened')
