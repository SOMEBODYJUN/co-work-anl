// Re-evaluate the final embedded demo, including the historical car-lien closing in month 27.
'use strict';
const fs=require('node:fs'),path=require('node:path'),vm=require('node:vm'),assert=require('node:assert/strict');
const {createHash}=require('node:crypto'),{execFileSync}=require('node:child_process');
const w=path.resolve(__dirname,'../../..'),repo=path.resolve(w,'../..'),author=path.join(w,'research/tasks/household_engine');
const old='1580e869769a9410b88d040acf08bab394c6f9d2';
const sha=b=>createHash('sha256').update(b).digest('hex');
function unpack(raw){
  const html=raw.toString();
  const code=[...html.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(m=>m[1]);
  const data=Object.fromEntries([...html.matchAll(/<script id="([^"]+)" type="application\/json">([\s\S]*?)<\/script>/g)].map(m=>[m[1],JSON.parse(m[2])]));
  assert.equal(code.length,2);
  const box=vm.createContext({});vm.runInContext(code[0],box);
  return {E:box.HouseholdEngine,code,h:data['example-data'],s:data['scenario-data'],sha256:sha(raw)};
}
function observeCar(candidate){
  const {E,h,s}=candidate;
  const selected=E.enumerate(E.validateHousehold(h),500).strategies.find(q=>q.id==='S464');
  const r=E.simulate(h,s.find(q=>q.id==='severe'),selected).rows[26];
  return {loan:h.loans.find(q=>q.id==='auto'),actions:selected.actions,month:r.month,
          releaseFees:r.releaseFees,closingPrincipal:r.closingPrincipal,cash:r.cash,vehicle:r.vehicle};
}
const orig=unpack(execFileSync('git',['show',old+':work/boss 1/formal/calculator.html'],{cwd:repo}));
const now=unpack(fs.readFileSync(path.join(w,'formal/calculator.html')));
assert.equal(now.sha256,sha(fs.readFileSync(path.join(author,'calculator.html'))));
assert.equal(sha(now.code[0]),sha(fs.readFileSync(path.join(author,'engine.js'))));
assert.equal(sha(now.code[1]),sha(fs.readFileSync(path.join(author,'ui.js'))));
assert.deepEqual(now.s,JSON.parse(fs.readFileSync(path.join(w,'formal/scenarios.json'))));
assert.deepEqual(now.h,JSON.parse(fs.readFileSync(path.join(author,'synthetic_household.json'))));
assert.equal(now.h.dataKind,'synthetic_example');
const study=now.E.assess(now.h,now.s,500);
const feasible=study.results.filter(r=>Object.values(r.outcomes).every(x=>x.feasible));
const baseline=study.results[0].outcomes.severe;
const monthly=study.results.reduce((total,p)=>total+Object.values(p.outcomes).reduce((n,s)=>n+(s.firstFailure||120),0),0);
const observed={rules:study.results.length,commonFeasible:feasible.length,
     allDistinct:new Set(study.results.map(q=>q.trajectory)).size,commonFeasibleDistinct:new Set(feasible.map(q=>q.trajectory)).size,
     paretoRules:feasible.filter(q=>q.pareto).length,uniqueShortlist:study.shortlist.length,
     monthlyRows:monthly,baselineSevereFirstFailure:baseline.firstFailure,baselineSevereGap:baseline.failureBreakdown,
     baselineSevereTerminal:baseline.terminalReal};
assert.equal(observed.rules,500);assert.equal(observed.commonFeasible,134);assert.equal(observed.allDistinct,416);
assert.equal(observed.commonFeasibleDistinct,105);assert.equal(observed.paretoRules,6);assert.equal(monthly,168216);
assert.equal(observed.baselineSevereFirstFailure,101);assert.equal(baseline.terminalReal,null);
assert.equal(observed.baselineSevereGap.missedDebtService,0);
const before=observeCar(orig),after=observeCar(now);
assert.equal(before.loan.settlementFee,180);assert.equal(after.loan.saleMaturityReleaseFee,180);
assert.equal(before.releaseFees,180);assert.equal(after.releaseFees,180);assert.equal(before.month,27);
assert.equal(before.closingPrincipal,after.closingPrincipal);assert.equal(before.cash,after.cash);
console.log(JSON.stringify({reviewer:'/root/release_audit',scope:'Real executable product; invented household',
  htmlSha256:now.sha256,oldHTMLSha256:orig.sha256,sourceCodeSha256:sha(now.code[0]),uiSourceSha256:sha(now.code[1]),
  formalScenarioSha256:sha(fs.readFileSync(path.join(w,'formal/scenarios.json'))),scriptSha256:sha(fs.readFileSync(__filename)),
  inspectedHTMLDataMatch:[true,true],node:process.version,observed,winners:study.winners,
  oldAndCurrentDemoClosing:{before,after}},null,2));
