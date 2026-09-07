from pathlib import Path
p=Path(__file__).resolve().parents[1]/'app'/'src'/'main'/'assets'/'index.html'
s=p.read_text(encoding='utf-8')
if 'living-dex-audio-always-on" content="2.5"' not in s:
    s=s.replace('</head>','<meta name="living-dex-audio-always-on" content="2.5"/>\n</head>',1)
css=r'''
/* Audio 2.5 — always-on app audio, controlled by Android media volume */
#ldhAudioQuick,#ldhAudioSettings,.audio-quick,.audio-settings{display:none!important}
'''
if '/* Audio 2.5' not in s:s=s.replace('</style>',css+'\n</style>',1)
js=r'''
// Audio 2.5 — always on while the app is active. Android media volume is the user-facing volume control.
function ldh25NormalizeAudio(){
 try{ldhAudioPrefs.music=true;ldhAudioPrefs.sfx=true;ldhAudioPrefs.volume=1}catch(e){}
 try{localStorage.setItem(LDH_AUDIO_KEY,JSON.stringify({music:true,sfx:true,volume:1}))}catch(e){}
 const q=document.getElementById('ldhAudioQuick');if(q)q.remove();
 const p=document.getElementById('ldhAudioSettings');if(p)p.remove();
}
function ldh25RestoreGains(){
 if(!ldhCtx)return;
 const t=ldhCtx.currentTime;
 if(ldhMusicGain)ldhMusicGain.gain.setTargetAtTime(1,t,.06);
 if(ldhSfxGain)ldhSfxGain.gain.setTargetAtTime(1,t,.04);
}
function ldh25Start(){
 ldh25NormalizeAudio();
 try{ldhEnsureAudio()}catch(e){}
 if(!ldhCtx)return;
 const after=()=>{ldh25RestoreGains();if(!ldhLoopTimer){try{ldhScheduleStep();ldhLoopTimer=setInterval(ldhScheduleStep,720)}catch(e){}}};
 try{const r=ldhCtx.resume();if(r&&typeof r.then==='function')r.then(after).catch(()=>{});else after()}catch(e){after()}
}
window.ldhToggleMusic=function(){ldh25Start()};
window.ldhToggleSfx=function(){ldh25Start()};
window.ldhSetVolume=function(){ldh25Start()};
window.ldhApplyAudio=function(){ldh25Start()};
window.ldhPersistAudio=function(){ldh25NormalizeAudio()};
window.ldhRenderAudioUI=function(){ldh25NormalizeAudio()};
window.ldhInjectSettings=function(){ldh25NormalizeAudio()};
window.ldhQuickButton=function(){ldh25NormalizeAudio()};
window.ldhStartLoop=function(){ldh25NormalizeAudio();ldhEnsureAudio();if(!ldhCtx)return;ldh25RestoreGains();if(ldhCtx.state==='suspended'){try{ldhCtx.resume()}catch(e){}}if(!ldhLoopTimer){ldhScheduleStep();ldhLoopTimer=setInterval(ldhScheduleStep,720)}};
window.ldhStopLoop=function(){if(ldhLoopTimer){clearInterval(ldhLoopTimer);ldhLoopTimer=null}};
window.ldhAndroidResumeAudio=ldh25Start;
window.addEventListener('pageshow',()=>{if(ldhStarted)ldh25Start()});
window.addEventListener('focus',()=>{if(ldhStarted)ldh25Start()});
document.addEventListener('visibilitychange',()=>{if(!document.hidden&&ldhStarted)ldh25Start()});
document.addEventListener('pointerdown',()=>{ldhStarted=true;ldh25Start()},{once:true,capture:true});
setTimeout(()=>{
 ldh25NormalizeAudio();
 if(new URLSearchParams(location.search).has('audio25qa')){
  const ok=ldhAudioPrefs.music===true&&ldhAudioPrefs.sfx===true&&Number(ldhAudioPrefs.volume)===1&&!document.getElementById('ldhAudioQuick')&&!document.getElementById('ldhAudioSettings')&&typeof window.ldhAndroidResumeAudio==='function';
  document.documentElement.setAttribute('data-audio25-qa',ok?'1':'0');
  document.documentElement.setAttribute('data-audio25-music',String(ldhAudioPrefs.music));
  document.documentElement.setAttribute('data-audio25-sfx',String(ldhAudioPrefs.sfx));
  document.documentElement.setAttribute('data-audio25-volume',String(ldhAudioPrefs.volume));
 }
},80);
'''
s=s.replace('</body>','<script>'+js+'</script>\n</body>',1)
p.write_text(s,encoding='utf-8')
print('Audio always-on 2.5 applied')
