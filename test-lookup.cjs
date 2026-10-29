const fs=require('fs'),vm=require('vm'),assert=require('assert/strict');
const html=fs.readFileSync(__dirname+'/index.html','utf8');const data=JSON.parse(html.match(/<script id="property-data" type="application\/json">([\s\S]*?)<\/script>/)[1]);
assert.equal(data.length,77355);assert.equal(new Set(data.map(r=>r[0])).size,data.length);
for(const r of data){if(!r[5])continue;const [c,p,a,w]=r[5];assert.ok(Math.abs((c-p)-a)<.00001);assert.ok(Math.abs(Math.floor((Math.round(Math.abs(a)*100)+26)/52)/100-w)<.00001);}
const nodes=new Map();function el(){return {textContent:'',value:'',hidden:false,children:[],classList:{toggle(){}},remove(){},focus(){},addEventListener(){},append(x){this.children.push(x)},replaceChildren(){this.children=[]}};}
const document={getElementById(id){if(!nodes.has(id))nodes.set(id,el());return nodes.get(id)},createElement:el};document.getElementById('property-data').textContent=JSON.stringify(data);
const ctx=vm.createContext({document,Intl,console,setTimeout,clearTimeout});vm.runInContext(html.match(/<\/script><script>([\s\S]*?)<\/script>/)[1],ctx);
for(const [query,id] of [['8 rintoul st','1131997'],['8a lipman st','1127865'],['1131214','1131214'],['9 newtown ave','1131214']]){nodes.get('query').value=query;vm.runInContext('search()',ctx);assert.ok(nodes.get('account').textContent.includes(id));assert.equal(nodes.get('property').hidden,false);}
assert.equal(nodes.get('annual').textContent,'$442.82');assert.equal(nodes.get('weekly').textContent,'$8.52');
nodes.get('query').value='rintoul st';vm.runInContext('search()',ctx);assert.ok(nodes.get('matches').children.length>1);assert.ok(nodes.get('matches').children.every(e=>e.children.some(c=>c.className==='result-amount')));
nodes.get('query').value='zzzz-no-such-property';vm.runInContext('search()',ctx);assert.ok(nodes.get('status').textContent.startsWith('No matching'));assert.equal(nodes.get('property').hidden,true);
nodes.get('query').value='1206560';vm.runInContext('search()',ctx);assert.equal(nodes.get('figures').hidden,true);assert.equal(nodes.get('exception').hidden,false);assert.ok(nodes.get('exception').textContent.includes('property not found'));
console.log('All precomputed arithmetic, unique-account, automatic result, multi-result and no-match checks passed');
