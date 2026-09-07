from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
main=(ROOT/'app/src/main/java/com/otaviobarreto/livingdex/MainActivity.java').read_text(encoding='utf-8')
gradle=(ROOT/'app/build.gradle').read_text(encoding='utf-8')
manifest=(ROOT/'app/src/main/AndroidManifest.xml').read_text(encoding='utf-8')
html=(ROOT/'app/src/main/assets/index.html').read_text(encoding='utf-8')
checks={
 'android_back_bridge':'androidHandleBack' in main and 'evaluateJavascript' in main,
 'webview_state':'restoreState(state)' in main and 'saveState(outState)' in main,
 'lifecycle':'webView.onPause()' in main and 'webView.onResume()' in main and 'webView.destroy()' in main,
 'safe_browsing':'setSafeBrowsingEnabled(true)' in main,
 'mixed_content_blocked':'MIXED_CONTENT_NEVER_ALLOW' in main,
 'external_links':'Intent.ACTION_VIEW' in main,
 'dom_storage':'setDomStorageEnabled(true)' in main,
 'https_only':'android:usesCleartextTraffic="false"' in manifest,
 'network_security':'android:networkSecurityConfig="@xml/network_security_config"' in manifest,
 'ui14':'name="living-dex-ui" content="1.4"' in html and 'function androidHandleBack()' in html,
 'release_build':'release {' in gradle,
}
failed=[k for k,v in checks.items() if not v]
print({'passed':len(checks)-len(failed),'total':len(checks),'failed':failed})
if failed: raise SystemExit('Android release readiness failed: '+', '.join(failed))
