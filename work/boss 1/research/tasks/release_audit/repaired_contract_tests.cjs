// Independent boundary checks written against contract terms, executed on the final HTML's embedded engine.
'use strict';
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const crypto = require('node:crypto');
const assert = require('node:assert/strict');

const own = __dirname;
const workspace = path.resolve(own, '../../..');
const file = process.argv[2] || path.join(workspace, 'formal/calculator.html');
const html = fs.readFileSync(file);
const scripts = [...html.toString().matchAll(/<script>([\s\S]*?)<\/script>/g)];
assert.equal(scripts.length, 2);
const sandbox = vm.createContext({});
vm.runInContext(scripts[0][1],sandbox);
const E = sandbox.HouseholdEngine;
const sha = x => crypto.createHash('sha256').update(x).digest('hex');
const originalBytes = fs.readFileSync(path.join(own, 'pre_repair_cases.json'));
const original = JSON.parse(originalBytes);
const patchedBytes = fs.readFileSync(path.join(own, 'post_repair_contract_inputs.json'));
const terms = JSON.parse(patchedBytes);
assert.equal(sha(originalBytes), terms.old_inputs_sha256);
const quiet = {id:'quiet',name:'合同',paths:[]};
const limited = {...original.contract_household.loans[0],...terms.per_action_only_patch};
const hh = (extra={}) => ({...E.blank(),cash:13000,minimumLiving:0,...extra});
const oneLoan = (fields={}) => hh({loans:[{...limited,...fields}]});
const plan = actions => ({id:'independent',actions});
const obs = [];
const check = (label,callback) => {
  try {const result=callback();obs.push({label,pass:true,result});}
  catch (error){obs.push({label,pass:false,reason:error.stack.split('\n').slice(0,4).join('\n')});}
};
const equalApprox = (actual,wanted,tolerance=1e-7) => assert.ok(Number.isFinite(actual)&&Math.abs(actual-wanted)<=tolerance,`expected ${wanted}, got ${actual}`);
const sim = (h,acts,s=quiet) => E.simulate(h,s,plan(acts));
const early = (amount,month=1,mode='shorten') => ({kind:'prepay',loan:'loan',month,mode,...(mode==='full'?{}:{amount})});
const income = (id,kind) => ({...E.templates.incomes,id,name:id,kind,monthly:1000});
const prop = {id:'home',name:'闲置房',use:'idle',value:4000,saleValue:4000,canSell:true,carry:0,rent:0,
              saleLag:0,lock:1,saleFee:0,closingFee:0};
const car = {id:'car',name:'闲置车',value:4000,saleValue:4000,canSell:true,necessary:false,carry:0,
             saleLag:0,lock:1,saleFee:0,closingFee:0};
const stock = {id:'stock',name:'质押证券',value:4000,annualReturn:0,fee:0,settle:0,unlock:1,
               restriction:'pledged',purpose:'允许交易',kind:'stock'};
const broad = hh({minimumLiving:700,incomes:[income('salary','wage'),income('bonus','bonus'),income('shop','business'),income('other','other')],
  expenses:[{id:'medical',name:'医疗',monthly:0,kind:'medical'}],properties:[prop],vehicles:[car],
  financial:[{...stock,restriction:'free'},{...stock,id:'term',kind:'deposit',restriction:'free',maturity:24}],
  loans:[{...limited,id:'floating',rateType:'floating'},{...limited,id:'fixed'}]});
const targetScenario = (key,target,value=0.5) => ({id:'test',name:'定向压力',paths:[E.path(key,value,1,1,target)]});
const wrongTargets = [
  ['wageFactor','sallary',.5],['wageFactor','medical',.5],['wageFactor','shop',.5],['businessFactor','salary',.5],
  ['otherIncomeFactor','bonus',.5],['unemploymentMonths','home',3],['recoveryMonths','car',2],
  ['reemploymentFactor','floating',.8],['propertyShock','car',-.2],['rentFactor','stock',.5],
  ['vacancyAdd','medical',.1],['propertyAnnual','term',-.02],['saleHaircut','stock',.1],['saleDelay','floating',2],
  ['financialShock','term',-.2],['securityAnnual','home',.05],['concentrationHaircut','car',.1],
  ['loanRateDelta','fixed',.01],['inflationAnnual','salary',.01],['cashRateDelta','salary',.01]
];
const targeted = [['wageFactor','salary',.5],['wageFactor','bonus',.5],['businessFactor','shop',.5],['otherIncomeFactor','other',.5],
  ['unemploymentMonths','salary',1],['recoveryMonths','shop',2],['reemploymentFactor','other',.9],
  ['propertyShock','home',-.2],['propertyAnnual','home',.02],['rentFactor','home',.7],['vacancyAdd','home',.1],
  ['saleHaircut','car',.05],['saleDelay','home',1],['financialShock','stock',-.1],['securityAnnual','stock',.02],
  ['concentrationHaircut','stock',.1],['loanRateDelta','floating',.02],['inflationAnnual','*',.02],['cashRateDelta','*',.01]];
for(const [key,target,value] of wrongTargets){
  check('reject '+key+' targeting '+target,()=>{
    const sc=targetScenario(key,target,value);
    assert.throws(()=>E.assess(broad,[sc],100));
    assert.throws(()=>sim(broad,[],sc));
    return 'assess and simulate both rejected before a household result';
  });
}
for(const [key,target,value] of targeted){
  check('accept matching '+key+' target '+target,()=>{
    const sc=targetScenario(key,target,value);
    const prep=E.prepare(broad,[sc]);
    assert.equal(prep.scenarios.length,1);
    return 'valid target accepted';
  });
}
check('shared wildcard template with zero assets and incomes',()=>{
  assert.equal(E.prepare(hh(),[targetScenario('wageFactor','*')]).scenarios.length,1);
});
check('real wage for target has first-month gap 200 and no terminal',()=>{
  const h=hh({...original.wage_household});
  const r=E.assess(h,[{id:'test',name:'降薪',paths:[E.path('wageFactor',.5,1,120,'salary')]}],100);
  const s=r.results[0].outcomes.test;
  assert.equal(r.commonCount,0);assert.equal(s.firstFailure,1);assert.equal(s.worstGap,200);assert.equal(s.terminalReal,null);
  return {firstFailure:s.firstFailure,gap:s.worstGap};
});
check('cap is included; no generated alternative exceeds per-action cap or permits full settlement',()=>{
  const r=E.assess(oneLoan(),[quiet],100);
  const all=r.results.filter(x=>x.strategy.actions.length).map(x=>({mode:x.strategy.actions[0].mode,principal:x.outcomes.quiet.prepaid,feasible:x.feasible}));
  assert.ok(all.some(x=>x.feasible&&Math.abs(x.principal-1000)<1e-7));
  assert.ok(all.every(x=>x.mode!=='full'&&x.principal<=1000+1e-7));
  return {rules:all,winners:r.winners};
});
for(const [amount,ok] of [[100,true],[1000,true],[1001,false],[99,false]]) {
  for(const mode of ['shorten','recast'])check(mode+' voluntary amount '+amount,()=>{
    const s=sim(oneLoan(),[early(amount,1,mode)]).summary;
    assert.equal(s.feasible,ok);equalApprox(s.prepaid,ok?amount:0);
    return {prepaid:s.prepaid,blocked:s.blocked.length};
  });
}
check('partial-only and capped full payoff both blocked',()=>{
  for(const contract of [{allowFull:false,prepayMax:'unlimited'}, {allowFull:true,prepayMax:1000}]){
    const s=sim(oneLoan(contract),[early(null,1,'full')]).summary;
    assert.equal(s.feasible,false);assert.equal(s.prepaid,0);assert.ok(s.blocked.length>0);
  }
});
check('unlimited full prepayment requires explicit permission and retires post-scheduled balance',()=>{
  const h=oneLoan({allowFull:true,prepayMax:'unlimited'});
  const s=sim(h,[early(null,1,'full')]).summary;
  assert.equal(s.feasible,true);equalApprox(s.prepaid,9211.512113216582);equalApprox(s.interestTotal,100);
  return {prepaid:s.prepaid,interest:s.interestTotal};
});
check('descending old-format/unknown policies preserve normal contract and generate no unsupported early actions',()=>{
  const h=oneLoan({prepayMax:null,prepayPeriodMax:null,allowFull:null});
  const r=E.assess(h,[quiet],100);
  assert.equal(r.results.length,1);const s=r.results[0].outcomes.quiet;
  assert.equal(s.feasible,true);equalApprox(s.endDebt,0);equalApprox(s.terminalReal,2338.1453585989957);
  return {rules:r.results.length,ending:s.terminalReal};
});
check('reverse calculation cannot exceed the per-action cap',()=>{
  const r=E.reverse(oneLoan(),quiet,E.baseStrategy(),{loanId:'loan'});
  equalApprox(r.affordablePrepay.largestTested,1000,.011);return r.affordablePrepay;
});
check('period remainder and first reset apply before/after the boundary',()=>{
  const h=oneLoan(terms.one_month_left_period);
  for(const [month,money,ok] of [[1,250,true],[1,251,false],[2,1000,true],[2,1001,false]]){
    const s=sim(h,[early(money,month)]).summary;
    assert.equal(s.feasible,ok);equalApprox(s.prepaid,ok?money:0);
  }
  const r=E.reverse(h,quiet,E.baseStrategy(),{loanId:'loan'});
  equalApprox(r.affordablePrepay.largestTested,250,.011);
  return {firstWindowAvailable:r.affordablePrepay.largestTested,nextWindowHasAtLeast:1000};
});
check('two voluntary payments share the quota; first reset restores the periodic capacity',()=>{
  const h=oneLoan(terms.three_months_left_period);
  const legal=sim(h,[early(200,1),early(100,2),early(1000,4)]).summary;
  assert.equal(legal.feasible,true);equalApprox(legal.prepaid,1300);
  const excess=sim(h,[early(200,1),early(101,2)]).summary;
  assert.equal(excess.feasible,false);equalApprox(excess.prepaid,200);
  return {validTotal:legal.prepaid,paidBeforeBlockedSecond:excess.prepaid};
});
const assetGroups={home:'properties',car:'vehicles',stock:'financial'};
const samples={home:prop,car,stock};
function saleCase(id,contract,month=1){
  const h=hh({[assetGroups[id]]:[samples[id]],
    loans:[{...limited,id:'loan',principal:2000,annualRate:0,method:'bullet',months:3,collateral:id,transferWithLien:true,...contract}]});
  const action=id==='stock'?{kind:'liquidate',asset:id,mode:'all',month}:{kind:'list',asset:id,month};
  return sim(h,[action]);
}
for(const id of ['home','car','stock']){
  for(const [reason,restriction] of [['amount cap',{allowFull:true}],['full permission',{allowFull:false,prepayMax:'unlimited'}],['explicit sale exclusion',{allowFull:true,prepayMax:'unlimited',salePayoffRule:'forbidden'}]]){
    check(id+' early sale honors '+reason,()=>{
      const r=saleCase(id,{...terms.sale_under_ordinary_early_payment_terms,...restriction});
      assert.equal(r.summary.feasible,false);assert.ok(r.summary.blocked.length>0);
      assert.equal(r.rows[0][id==='stock'?'financial':id==='home'?'property':'vehicle'],4000);
      equalApprox(r.rows[0].debt,2000);return {firstMonthDebt:r.rows[0].debt,blocks:r.summary.blocked};
    });
  }
  check(id+' independent sale clause with separate fee retires collateral only once',()=>{
    const r=saleCase(id,terms.sale_with_independent_closing_clause);
    assert.equal(r.summary.feasible,true);equalApprox(r.rows[0].debt,0);
    equalApprox(r.rows[0].cash,14795);equalApprox(r.rows[0].closingPrincipal,2000);equalApprox(r.rows[0].releaseFees,205);
    return {cash:r.rows[0].cash,releaseFee:r.rows[0].releaseFees,principal:r.rows[0].closingPrincipal};
  });
  check(id+' ordinary maturity does not require early repayment permission',()=>{
    const r=saleCase(id,terms.scheduled_due_without_early_permissions,3);
    equalApprox(r.rows[2].debt,0);equalApprox(r.rows[2].cash,15000);assert.equal(r.summary.feasible,true);
    return {cash:r.rows[2].cash,endDebt:r.rows[2].debt};
  });
}
check('scheduled principal released on sale consumes no early-payment quota',()=>{
  const sameTerms={...terms.sale_under_ordinary_early_payment_terms,allowFull:true,method:'principal',months:2};
  const exact=saleCase('home',{...sameTerms,prepayMax:1000});
  const excess=saleCase('home',{...sameTerms,prepayMax:999.99});
  assert.equal(exact.summary.feasible,true);equalApprox(exact.rows[0].debt,0);equalApprox(exact.rows[0].cash,15000);
  assert.equal(excess.summary.feasible,false);equalApprox(excess.rows[0].debt,1000);
  return {grossPrincipalOnClosing:exact.rows[0].closingPrincipal,scheduledPrincipal:1000,extraPrincipal:1000};
});
const releaseControl=terms.distinct_car_release_costs;
const carDebt={...limited,principal:releaseControl.loanPrincipal,annualRate:0,method:'bullet',months:releaseControl.loanTermMonths,
  collateral:'car',transferWithLien:true,allowFull:true,prepayMax:'unlimited',prepayFee:0,
  settlementFee:releaseControl.ordinaryEarlyClosingFee,salePayoffRule:'same_terms',
  saleMaturityReleaseFee:releaseControl.additionalReleaseFeeOnlyForSaleInContractMaturityMonth};
const carHouse=(changes={})=>hh({cash:releaseControl.openingCash,vehicles:[car],loans:[{...carDebt,...changes}]});
const sellCar=month=>({kind:'list',asset:'car',month});
check('ordinary maturity without a sale incurs no transaction-only discharge charge',()=>{
  const r=sim(carHouse(),[]);
  equalApprox(r.rows[1].cash,11000);equalApprox(r.rows[1].releaseFees,0);equalApprox(r.rows[1].debt,0);
  return {cash:r.rows[1].cash,releaseFee:r.rows[1].releaseFees};
});
check('same-month lien discharge pays only the specified separate 180 transaction charge',()=>{
  const r=sim(carHouse(),[sellCar(2)]);
  equalApprox(r.rows[1].cash,14820);equalApprox(r.rows[1].releaseFees,180);equalApprox(r.rows[1].closingPrincipal,2000);
  equalApprox(r.rows[2].cash,14820);
  return {cash:r.rows[1].cash,releaseFee:r.rows[1].releaseFees,prepayFees:r.rows[1].prepayFees};
});
check('voluntary payoff before sale incurs 23 only and no later transaction-only lien charge',()=>{
  const r=sim(carHouse(),[early(null,1,'full'),sellCar(2)]);
  equalApprox(r.rows[0].cash,10977);equalApprox(r.rows[0].prepayFees,23);
  equalApprox(r.rows[1].cash,14977);equalApprox(r.rows[1].releaseFees,0);equalApprox(r.rows[1].debt,0);
  return {month1Cash:r.rows[0].cash,month2Cash:r.rows[1].cash,releaseFeeOnSale:r.rows[1].releaseFees};
});
check('sale after scheduled redemption does not repeat the loan discharge',()=>{
  const r=sim(carHouse(),[sellCar(3)]);
  equalApprox(r.rows[1].cash,11000);equalApprox(r.rows[2].cash,15000);
  equalApprox(r.rows[2].closingPrincipal,0);equalApprox(r.rows[2].releaseFees,0);
  return {month2:r.rows[1].cash,month3:r.rows[2].cash};
});
check('fee explicitly included in asset costs is charged once; explicitly unknown fee blocks active closing',()=>{
  const h=carHouse({saleMaturityReleaseFee:'in_asset_cost'});h.vehicles=[{...car,closingFee:180}];
  const r=sim(h,[sellCar(2)]);equalApprox(r.rows[1].cash,14820);equalApprox(r.rows[1].saleFees,180);equalApprox(r.rows[1].releaseFees,0);
  const unknown=sim(carHouse({saleMaturityReleaseFee:null}),[sellCar(2)]);
  assert.equal(unknown.summary.feasible,false);equalApprox(unknown.rows[1].debt,0);equalApprox(unknown.rows[1].vehicle,4000);
  return {inclusiveAssetFee:r.rows[1].saleFees,unknownSaleBlocked:unknown.summary.blocked.length};
});
const failed=obs.filter(o=>!o.pass);
console.log(JSON.stringify({
  reviewer:'/root/release_audit',scope:'Independent synthetic contract and household-target controls. Embedded engine in Node; no browser operations.',
  formalHTMLSha256:sha(html),engineSha256:sha(scripts[0][1]),scriptSha256:sha(fs.readFileSync(__filename)),
  originalCasesSha256:sha(originalBytes),postRepairInputSha256:sha(patchedBytes),node:process.version,
  assertions:obs.length,passed:obs.length-failed.length,failed:failed.length,cases:obs
},null,2));
process.exitCode=failed.length?1:0;
