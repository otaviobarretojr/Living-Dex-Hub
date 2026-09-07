package com.otaviobarreto.livingdex;

import android.app.Activity;
import android.content.Intent;
import android.graphics.Color;
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;
import android.view.View;
import android.webkit.WebChromeClient;
import android.webkit.WebResourceRequest;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;

public class MainActivity extends Activity {
    private WebView webView;
    private static final int APP_BG = Color.rgb(247, 248, 251);

    @Override public void onCreate(Bundle state) {
        super.onCreate(state);
        getWindow().setStatusBarColor(APP_BG);
        getWindow().setNavigationBarColor(APP_BG);
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.Q) {
            getWindow().setNavigationBarContrastEnforced(false);
            getWindow().setStatusBarContrastEnforced(false);
        }
        int flags = View.SYSTEM_UI_FLAG_LIGHT_STATUS_BAR;
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) flags |= View.SYSTEM_UI_FLAG_LIGHT_NAVIGATION_BAR;
        getWindow().getDecorView().setSystemUiVisibility(flags);

        webView = new WebView(this);
        webView.setBackgroundColor(APP_BG);
        webView.setOverScrollMode(View.OVER_SCROLL_NEVER);
        setContentView(webView);

        WebSettings settings = webView.getSettings();
        settings.setJavaScriptEnabled(true);
        settings.setDomStorageEnabled(true);
        settings.setDatabaseEnabled(true);
        settings.setAllowFileAccess(true);
        settings.setAllowContentAccess(true);
        settings.setMediaPlaybackRequiresUserGesture(false);
        settings.setSupportZoom(false);
        settings.setBuiltInZoomControls(false);
        settings.setDisplayZoomControls(false);
        settings.setTextZoom(100);
        settings.setMixedContentMode(WebSettings.MIXED_CONTENT_NEVER_ALLOW);
        settings.setSafeBrowsingEnabled(true);

        webView.setWebChromeClient(new WebChromeClient());
        webView.setWebViewClient(new WebViewClient() {
            @Override public void onPageFinished(WebView view, String url) {
                super.onPageFinished(view, url);
                injectMobileLibraryFix(view);
            }

            @Override public boolean shouldOverrideUrlLoading(WebView view, WebResourceRequest request) {
                Uri uri = request.getUrl();
                String host = uri.getHost();
                if (host == null) return false;
                if (host.equals("pokeapi.co") || host.equals("raw.githubusercontent.com")) return false;
                String scheme = uri.getScheme();
                if ("http".equals(scheme) || "https".equals(scheme)) {
                    try { startActivity(new Intent(Intent.ACTION_VIEW, uri)); } catch (Exception ignored) {}
                }
                return true;
            }
        });

        if (state == null || webView.restoreState(state) == null) {
            webView.loadUrl("file:///android_asset/index.html");
        }
    }

    private void injectMobileLibraryFix(WebView view) {
        String js = "(function(){" +
            "if(window.__ldhLibraryMobileFix)return;window.__ldhLibraryMobileFix=true;" +
            "var css='@media(max-width:600px){' +" +
            "'#games{padding-left:18px!important;padding-right:18px!important;padding-bottom:120px!important}' +" +
            "'#games h1{font-size:32px!important;line-height:1.08!important;margin-bottom:8px!important}' +" +
            "'#games>p{font-size:15px!important;line-height:1.4!important;margin-bottom:20px!important}' +" +
            "'#games .game-grid,#games .games-grid,#games .library-grid,#games [class*=gamesGrid],#games [class*=gameGrid]{display:grid!important;grid-template-columns:1fr!important;gap:16px!important}' +" +
            "'#games .game-card,#games .gameCard,#games [class*=game-card],#games [class*=gameCard]{width:100%!important;max-width:none!important;min-height:0!important;height:auto!important;margin:0!important;border-radius:24px!important;overflow:hidden!important}' +" +
            "'#games .game-card button,#games .gameCard button,#games [class*=game-card] button,#games [class*=gameCard] button{min-height:52px!important;border-radius:16px!important;font-size:16px!important;margin-top:12px!important}' +" +
            "'}';" +
            "var s=document.createElement('style');s.id='ldh-mobile-library-fix';s.textContent=css;document.head.appendChild(s);" +
            "function fix(){if(innerWidth>600)return;var root=document.getElementById('games');if(!root)return;" +
            "var buttons=[].slice.call(root.querySelectorAll('button,a')).filter(function(x){return /Abrir\\s+Dex/i.test(x.textContent||'')});" +
            "buttons.forEach(function(btn){var card=btn;for(var i=0;i<7&&card.parentElement;i++){card=card.parentElement;var t=card.textContent||'';if(/entradas/i.test(t)&&/Abrir\\s+Dex/i.test(t))break;}" +
            "card.style.width='100%';card.style.maxWidth='none';card.style.height='auto';card.style.minHeight='0';card.style.margin='0 0 16px';card.style.overflow='hidden';card.style.borderRadius='24px';" +
            "btn.style.width='100%';btn.style.minHeight='52px';btn.style.marginTop='12px';btn.style.position='relative';btn.style.inset='auto';" +
            "[].slice.call(card.querySelectorAll('*')).forEach(function(el){var tx=(el.textContent||'').trim();" +
            "if(/^\\d+%\\s*DEX$/i.test(tx)||(/^\\d+%$/i.test(tx)&&el.children.length===0)){el.style.position='static';el.style.inset='auto';el.style.width='auto';el.style.height='auto';el.style.minWidth='0';el.style.transform='none';el.style.borderRadius='999px';el.style.padding='7px 11px';el.style.display='inline-flex';el.style.alignItems='center';el.style.justifyContent='center';el.style.fontSize='13px';el.style.margin='8px 0';}" +
            "if(/^(NINTENDO SWITCH\\s*){2,}$/i.test(tx)&&el.children.length===0)el.textContent='NINTENDO SWITCH';" +
            "});" +
            "});}" +
            "fix();setTimeout(fix,120);setTimeout(fix,600);" +
            "new MutationObserver(function(){clearTimeout(window.__ldhFixTimer);window.__ldhFixTimer=setTimeout(fix,60)}).observe(document.body,{childList:true,subtree:true});" +
            "})();";
        view.evaluateJavascript(js, null);
    }

    @Override protected void onSaveInstanceState(Bundle outState) {
        if (webView != null) webView.saveState(outState);
        super.onSaveInstanceState(outState);
    }

    @Override protected void onResume() {
        super.onResume();
        if (webView != null) {
            webView.onResume();
            webView.postDelayed(() -> {
                if (webView != null) {
                    webView.evaluateJavascript("if(typeof ldhAndroidResumeAudio==='function'){ldhAndroidResumeAudio()}", null);
                    injectMobileLibraryFix(webView);
                }
            }, 120);
        }
    }

    @Override protected void onPause() {
        if (webView != null) webView.onPause();
        super.onPause();
    }

    @Override protected void onDestroy() {
        if (webView != null) {
            webView.stopLoading();
            webView.setWebChromeClient(null);
            webView.setWebViewClient(null);
            webView.destroy();
            webView = null;
        }
        super.onDestroy();
    }

    @Override public void onBackPressed() {
        if (webView == null) { super.onBackPressed(); return; }
        webView.evaluateJavascript("(typeof androidHandleBack==='function'&&androidHandleBack())?'1':'0'", value -> {
            if ("\"1\"".equals(value)) return;
            if (webView != null && webView.canGoBack()) webView.goBack();
            else MainActivity.super.onBackPressed();
        });
    }
}
