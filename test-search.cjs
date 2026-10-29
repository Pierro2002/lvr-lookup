const fs=require('fs'),vm=require('vm'),assert=require('assert/strict');
const html=fs.readFileSync(__dirname+'/template.html','utf8');
const source=html.slice(html.indexOf('const aliases='),html.indexOf('const SEARCH='));
const ctx=vm.createContext({});vm.runInContext(source+';this.match=(a,q)=>addressMatches(norm(a),norm(q));',ctx);
for(const [a,q,expected] of [
 ['8 Example Street, Newtown','8 example st',true],
 ['81 Example Street, Newtown','8 example st',false],
 ['8A Example Street, Newtown','8 example st',false],
 ['8A Example Street, Newtown','8a example st',true],
 ['81A Example Street, Newtown','8a example st',false],
 ['8AB Example Street, Newtown','8a example st',false],
 ['8 Example Street, Newtown','8a example st',false],
 ['1 - 8 Example Street, Newtown','1/8 example st',true],
 ['1 - 81 Example Street, Newtown','1/8 example st',false],
 ['8 - 81 Example Street, Newtown','8 example st',false],
 ['1 - 8 Example Street, Newtown','8 example st',true],
 ['8A - 81 Example Street, Newtown','8a example st',false],
 ['8A Example Road, Newtown','8A example rd',true],
 ['8A Example Road, Newtown','8a example street',false],
 ['8A Example Street, Newtown','example st',true]
]) assert.equal(ctx.match(a,q),expected,JSON.stringify([a,q]));
console.log('15 address matching regression checks passed');
