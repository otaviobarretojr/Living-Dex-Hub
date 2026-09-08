#!/usr/bin/env node
'use strict';
const fs=require('fs'),path=require('path'),vm=require('vm'),assert=require('assert');
const ROOT=path.resolve(__dirname,'..'),A=path.join(ROOT,'app/src/main/assets');
const listeners=new Map();
global.window=global;global.CustomEvent=class{constructor(type,opts={}){this.type=type;this.detail=opts.detail||{}}};
global.addEventListener=(type,fn)=>{if(!listeners.has(type))listeners.set(type,[]);listeners.get(type).push(fn)};
global.dispatchEvent=e=>{for(const fn of listeners.get(e.type)||[])fn(e);return true};
global.document={documentElement:{style:{}},body:{style:{},classList:{add(){},remove(){}}},getElementById:()=>null,querySelector:()=>null,addEventListener:()=>{}};global.scrollTo=()=>{};
global.localStorage=(()=>{const m=new Map();return{getItem:k=>m.has(k)?m.get(k):null,setItem:(k,v)=>m.set(k,String(v)),removeItem:k=>m.delete(k),clear:()=>m.clear(),dump:()=>Object.fromEntries(m)}})();
function run(file){vm.runInThisContext(fs.readFileSync(path.join(A,file),'utf8'),{filename:file})}
(async()=>{
  // Business event: add -> duplicate no-op -> remove = exactly two confirmed changes.
  global.state={caught:{},games:{},activeGameId:'sv'};global.currentGame={id:'sv',name:'Scarlet / Violet'};global.currentPokemon={id:912,name:'Quaxly'};
  global.ld75Registered=id=>!!state.caught[Number(id)];
  global.ld75CommitBox=(id,on)=>{id=Number(id);if(on)state.caught[id]=true;else delete state.caught[id];return on};
  const changes=[];addEventListener('ld:box-entry-changed',e=>changes.push(e.detail));run('collection-reliability-v8.js');
  ld75CommitBox(912,true);assert.strictEqual(state.caught[912],true);assert.strictEqual(changes.length,1);assert.strictEqual(changes[0].registered,true);
  ld75CommitBox(912,true);assert.strictEqual(changes.length,1,'same persisted state must not emit another event');
  ld75CommitBox(912,false);assert.strictEqual(!!state.caught[912],false);assert.strictEqual(changes.length,2);assert.strictEqual(changes[1].registered,false);

  // Context: consulting another Box must never become the primary game.
  listeners.clear();localStorage.clear();state={caught:{},games:{},activeGameId:'sv'};global.state=state;localStorage.setItem('ld8.primaryGame','sv');
  global.GAMES=[{id:'sv',name:'Scarlet / Violet'},{id:'letsgo',name:"Let's Go Pikachu / Eevee"},{id:'bdsp',name:'BDSP'}];
  global.currentGame=GAMES[0];global.currentDex=[];global.activeSubdex=null;global.dexRegistryFor=id=>[{id:id+':main'}];global.loadSubdex=async()=>[{id:1},{id:2}];
  global.saveState=()=>{localStorage.setItem('ldh.state.snapshot',JSON.stringify(state))};global.persist=global.saveState;
  run('game-context-v8.js');
  const ok=await ld813SetBoxGame('letsgo',{open:false});assert.strictEqual(ok,true);assert.strictEqual(ld813PrimaryGameId(),'sv');assert.strictEqual(ld813BoxContextId(),'letsgo');assert.strictEqual(state.activeGameId,'sv');assert.strictEqual(currentGame.id,'letsgo');
  const p=await ld813SetPrimaryGame('bdsp');assert.strictEqual(p,true);assert.strictEqual(state.activeGameId,'bdsp');assert.strictEqual(ld813PrimaryGameId(),'bdsp');
  await ld813SetBoxGame('letsgo',{open:false});assert.strictEqual(state.activeGameId,'bdsp');assert.strictEqual(ld813BoxContextId(),'letsgo');

  // Reopen simulation: persisted state + context keys survive a process restart.
  state.caught[906]=true;state.games['sv:906']=true;saveState();
  const diskState=localStorage.getItem('ldh.state.snapshot');assert.ok(diskState,'state snapshot persisted');
  const persistedPrimary=localStorage.getItem('ld8.primaryGame'),persistedBox=localStorage.getItem('ld8.boxContextGame');
  global.state=state=JSON.parse(diskState);global.currentGame=GAMES.find(x=>x.id===persistedPrimary);global.currentDex=[];
  assert.strictEqual(state.caught[906],true,'caught Pokemon must survive reopen');assert.strictEqual(state.games['sv:906'],true,'game registration must survive reopen');
  assert.strictEqual(persistedPrimary,'bdsp','primary context survives reopen');assert.strictEqual(persistedBox,'letsgo','consultation context survives reopen');assert.strictEqual(state.activeGameId,'bdsp','persisted active state remains primary');
  console.log('JOURNEY RELIABILITY: PASS • add/remove/no-op • primary/Box isolation • collection persistence • reopen context persistence');
})().catch(e=>{console.error('JOURNEY RELIABILITY: FAIL',e);process.exit(1)});
