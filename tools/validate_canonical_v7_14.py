from pathlib import Path
import json,re

ROOT=Path(__file__).resolve().parents[1]
HTML=ROOT/'app'/'src'/'main'/'assets'/'index.html'
WORKFLOW=ROOT/'.github'/'workflows'/'build-apk.yml'
s=HTML.read_text(encoding='utf-8')
w=WORKFLOW.read_text(encoding='utf-8')

checks={
 'canonical_marker':'living-dex-canonical-baseline" content="7.14.0"' in s,
 'canonical_audit':'window.ld714CanonicalAudit=function' in s,
 'public_surfaces':"const LD714_PUBLIC_SURFACES=['home','box']" in s,
 'legacy_quarantine':'#games,#dex,#gameDex,#nationalDex,#library,#livingDex,#global,#missing,#families,#planner,#forms,#storage,#settings{display:none!important}' in s,
 'six_games':"const LD73_SUPPORTED=['sv','za','swsh','bdsp','letsgo','arceus']" in s,
 'all_dex_audit':'living-dex-full-audit" content="7.13.0"' in s and 'window.ld713Audit=function' in s,
 'box_integrity':'living-dex-integrity-ux" content="7.11.0"' in s and 'blocked out-of-game Box write' in s,
 'detail_fix':'living-dex-detail-overlay-fix" content="7.12.5"' in s,
 'personal_music':'living-dex-personal-music" content="7.12.0"' in s and 'LD712_STORE' in s,
 'home_only_nav':'living-dex-home-only-bottom-nav" content="7.12.1"' in s,
 'box_footer_removed':'living-dex-box-footer-cleanup" content="7.12.2"' in s,
 'compact_box':'living-dex-box-viewport" content="7.12.3"' in s,
 'evolution_hints':'LD713_SPECIAL_EVOLUTION_HINTS' in s,
 'no_public_legacy_nav':"data-ld79=\"home\"" in s and "data-ld79=\"box\"" in s,
 'canonical_workflow_hook':'canonical/index.v7_14.xz.b64' in w,
}
failed=[k for k,v in checks.items() if not v]
print(json.dumps({'checks':checks,'passed':len(checks)-len(failed),'total':len(checks),'failed':failed},indent=2,ensure_ascii=False))
if failed: raise SystemExit('Canonical 7.14 validation failed: '+', '.join(failed))

# Syntax sanity for inline JS extraction is performed by node in CI.
