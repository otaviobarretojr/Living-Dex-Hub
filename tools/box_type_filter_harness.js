#!/usr/bin/env node
'use strict';
const fs=require('fs'),path=require('path'),assert=require('assert');
const A=path.resolve(__dirname,'../app/src/main/assets');
const ux=fs.readFileSync(path.join(A,'product-ux-v8.js'),'utf8');
const db=JSON.parse(fs.readFileSync(path.join(A,'pokemon-offline-core-v8.json'),'utf8'));
assert(ux.includes("version:'8.0-f5.2'"),'F5.2 marker missing');
assert(ux.includes('async function slotTypes'),'slotTypes must resolve asynchronously');
assert(ux.includes('await window.ld8OfflineCore?.get?.(id)'),'offline type lookup must be awaited');
assert(ux.includes("if(type==='all'){paint(root,slots,slots.map(baseMatch),run);return}"),'Todos os tipos must restore synchronously');
assert(ux.includes('const matches=await Promise.all'),'type filtering must wait for all local type lookups');
assert(ux.includes('if(type!==wanted)return;paint(root,slots,matches,run)'),'stale async results must not repaint current filter');
assert(ux.includes('typeCache.clear()'),'type cache must reset when Box context changes');
const p=db.pokemon||{};
assert.strictEqual(db.count,1025);assert.strictEqual(Object.keys(p).length,1025);
function has(id,t){return Array.isArray(p[String(id)]?.types)&&p[String(id)].types.includes(t)}
assert(has(7,'water'),'Squirtle water');assert(has(1,'grass')&&has(1,'poison'),'Bulbasaur dual type');assert(has(4,'fire'),'Charmander fire');assert(has(912,'water'),'Quaxly water');assert(has(906,'grass'),'Sprigatito grass');
for(const t of ['normal','fire','water','electric','grass','ice','fighting','poison','ground','flying','psychic','bug','rock','ghost','dragon','dark','steel','fairy']) assert(Object.values(p).some(x=>Array.isArray(x.types)&&x.types.includes(t)),`missing type ${t}`);
console.log('BOX TYPE FILTER: PASS • async lookup • reversible all-types • dual types • 18/18 coverage');
