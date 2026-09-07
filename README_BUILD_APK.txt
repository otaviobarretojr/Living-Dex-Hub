LIVING DEX HUB — ANDROID BUILD 29

O projeto está pronto para compilar APK via GitHub Actions.

OPÇÃO MAIS FÁCIL
1. Crie um repositório GitHub.
2. Envie todo o conteúdo desta pasta para a raiz do repositório.
3. Abra Actions > Build Living Dex APK.
4. Clique em Run workflow.
5. Ao terminar, baixe o artifact “LivingDexHub-APK”.
6. Dentro dele estará app-debug.apk.

O workflow instala Java 17 + Gradle 8.10.2 e executa:
  gradle :app:assembleDebug --stacktrace

APK esperado:
  app/build/outputs/apk/debug/app-debug.apk

ESTADO
- applicationId: com.otaviobarreto.livingdex
- versionCode: 29
- versionName: 1.0.0
- minSdk: 26
- targetSdk: 35
- compileSdk: 35
- Internet apenas HTTPS
- WebView com DOM Storage e JavaScript
- Ícone Android incluído
- Workflow de build automático incluído

IMPORTANTE
O APK debug gerado pelo GitHub Actions é instalável no Android.
Para publicação/uso final assinado como release, use um keystore próprio e configure assinatura de release.
