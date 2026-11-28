"use strict";
const assert=require("node:assert/strict");
const crypto=require("node:crypto");
const fs=require("node:fs");
const path=require("node:path");
const vm=require("node:vm");
const {execFileSync}=require("node:child_process");
const ROOT=execFileSync("git",["rev-parse","--show-toplevel"],{cwd:__dirname,encoding:"utf8"}).trim();
const prefix=path.relative(ROOT,__dirname).split(path.sep).join("/")+"/";
const frozen="1580e869769a9410b88d040acf08bab394c6f9d2";
const old=name=>execFileSync("git",["show",frozen+":"+prefix+name],{cwd:ROOT,encoding:"utf8"});
const digest=t=>crypto.createHash("sha256").update(t).digest("hex");
const oldSource=old("engine.js"),freshSource=fs.readFileSync(path.join(__dirname,"engine.js"),"utf8");
const context=vm.createContext({});
new vm.Script(oldSource,{filename:"frozen-household-engine.js"}).runInContext(context);
const before=context.HouseholdEngine,after=require("./engine.js");
const beforeH=JSON.parse(old("synthetic_household.json")),afterH=require("./synthetic_household.json");
const beforePaths=JSON.parse(old("scenarios.json")),afterPaths=require("./scenarios.json");
assert.deepEqual(afterPaths,beforePaths);
const economicOld=JSON.parse(JSON.stringify(afterH));
for(const l of economicOld.loans){
  const reference=beforeH.loans.find(q=>q.id===l.id);
  for(const key of Object.keys(l))if(!Object.hasOwn(reference,key))delete l[key];
}
assert.deepEqual(economicOld,beforeH);
const a=before.assess(beforeH,beforePaths,500),b=after.assess(afterH,afterPaths,500);
assert.equal(a.results.length,b.results.length);
const jointA=crypto.createHash("sha256"),jointB=crypto.createHash("sha256");
const differences=[],economicFields=new Set();let rowCount=0,pairs=0;
function observe(row){
  return Object.entries(row).map(([key,val])=>{
    economicFields.add(key);
    return typeof val==="number"?Math.round(val*100):val;
  });
}
for(let i=0;i<a.results.length;i++){
  const x=a.results[i],y=b.results[i];assert.equal(x.strategy.id,y.strategy.id);
  assert.equal(JSON.stringify(x.strategy.actions),JSON.stringify(y.strategy.actions));
  for(const s of beforePaths){
    const aa=before.inspect(a,x.strategy.id,s.id).rows,bb=after.inspect(b,y.strategy.id,s.id).rows;
    assert.deepEqual(Object.keys(aa[0]),Object.keys(bb[0]));
    const tx=JSON.stringify(aa.map(observe)),ty=JSON.stringify(bb.map(observe));
    jointA.update(tx+"\n");jointB.update(ty+"\n");rowCount+=aa.length;pairs++;
    if(tx!==ty)differences.push({policy:x.strategy.id,scenario:s.id,oldRows:aa.length,newRows:bb.length});
  }
}
const priorCar=beforeH.loans.find(l=>l.id==="auto"),currentCar=afterH.loans.find(l=>l.id==="auto");
const titleOld=before.inspect(a,"S464","severe").rows[26],titleNew=after.inspect(b,"S464","severe").rows[26];
const addedLoanFields=afterH.loans.map(l=>({loan:l.id,fields:Object.fromEntries(Object.entries(l).filter(([k])=>!Object.hasOwn(beforeH.loans.find(prior=>prior.id===l.id),k)))}));
const report={inputKind:"synthetic_example",priorCommit:frozen,priorEngineSHA256:digest(oldSource),currentEngineSHA256:digest(freshSource),
  inputChange:"Only newly explicit limits and sale-contract permissions were added to the three synthetic loans. The old fields and all scenario parameters compare equal.",
  addedLoanFields,
  syntheticCarTitleFee:{priorCommit:frozen,priorFeeField:"settlementFee",oldFixedFee:priorCar.settlementFee,newMaturitySaleReleaseFee:currentCar.saleMaturityReleaseFee,
    oldAndNewEvent:{policy:"S464",scenario:"severe",month:27,oldReleaseFees:titleOld.releaseFees,newReleaseFees:titleNew.releaseFees,oldClosingPrincipal:titleOld.closingPrincipal,newClosingPrincipal:titleNew.closingPrincipal},
    reason:"The older application's explicit fixed 180 CNY was charged on closing this vehicle sale even when the shortened loan reached contractual maturity. The migrated fixed 180 applies only to a sale requiring lien discharge; ordinary scheduled payment remains independent of any early-payment permission."},
  oldRules:a.results.length,newRules:b.results.length,oldCommon:a.commonCount,newCommon:b.commonCount,
  matchedPolicyScenarioPairs:pairs,observedMonthsCompared:rowCount,comparedMonthlyFields:[...economicFields],
  comparison:"Every exposed monthly ledger field. Monetary/numeric values compared after cent-level rounding; null/boolean values and cutoff lengths must match.",
  oldJointRowsSHA256:jointA.digest("hex"),newJointRowsSHA256:jointB.digest("hex"),differingPolicyScenarioPairs:differences,
  oldWinners:JSON.parse(JSON.stringify(a.winners)),newWinners:b.winners};
fs.writeFileSync(path.join(__dirname,"contract_migration_replay.json"),JSON.stringify(report,null,2)+"\n");
console.log(JSON.stringify({policyScenarioPairs:pairs,observedMonths:rowCount,differences:differences.length,old:report.oldJointRowsSHA256,current:report.newJointRowsSHA256}));
if(differences.length||report.oldJointRowsSHA256!==report.newJointRowsSHA256)process.exitCode=1;
