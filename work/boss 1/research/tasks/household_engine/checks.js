"use strict";
const fs=require("fs"),path=require("path"),assert=require("assert/strict"),E=require("./engine.js"),sample=require("./synthetic_household.json"),scenarios=require("./scenarios.json");
const tests=[],errors=[],flat={id:"flat",name:"无附加冲击",paths:[]};
const eq=(a,b,tol=1e-7)=>assert.ok(Math.abs(a-b)<tol,"Expected "+b+" got "+a);
const knownTerms={
  loans:{canPrepay:true,prepayFrom:1,prepayMin:0,prepayFee:0,settlementFee:0,transferWithLien:false,allowRecast:true,allowShorten:true},
  properties:{canSell:true,lock:1,saleLag:0,saleFee:0,closingFee:0},
  vehicles:{canSell:true,lock:1,saleLag:0,saleFee:0,closingFee:0,necessary:false},
  financial:{fee:0,settle:0,unlock:1,maturity:0,restriction:"free",purpose:"家庭可用"}
};
const row=(group,data)=>({...E.templates[group],...knownTerms[group],...data});
const dry=(over={})=>({...E.blank(),cash:0,minimumLiving:0,...over});
const act=(...actions)=>({id:"specified",actions});
const loan=(over={})=>row("loans",{id:"l",principal:1200,annualRate:0,months:12,...over});
const home=(over={})=>row("properties",{id:"p",value:100,saleValue:80,carry:0,rent:0,...over});
const sec=(over={})=>row("financial",{id:"f",value:100,annualReturn:0,...over});
const income=(monthly,over={})=>row("incomes",{id:"i",monthly,...over});
const listed=(over={})=>act({kind:"list",asset:"p",month:1,...over});
const sim=(h,a=E.baseStrategy(),s=flat)=>E.simulate(h,s,a);
function test(name,fn){try{const result=fn();tests.push({name,verdict:"pass",result:result??null});}catch(err){errors.push({name,message:err.message,stack:err.stack});}}
test("blank inputs reject and synthetic fixture separately marked",()=>{
  assert.equal(E.blank().cash,null);assert.equal(E.blank().minimumLiving,null);assert.throws(()=>sim(E.blank()));assert.equal(sample.dataKind,"synthetic_example");
});
test("whole cash ledger, independent no-shock arithmetic",()=>{
  const d=sim(dry({cash:1500,incomes:[income(2000)],expenses:[row("expenses",{id:"e",monthly:1250})]}));
  assert.equal(d.rows.length,120);for(const r of d.rows){eq(r.cash,1500+750*r.month);eq(r.netWorth,r.cash);eq(r.cashResidual,0);eq(r.netResidual,0);}
  return d.summary.terminalNominal;
});
test("basic living floor plus medical and a one-off not capitalized into reserve",()=>{
  const d=sim(dry({cash:10000,minimumLiving:100,reserveMonths:2,expenses:[
    row("expenses",{id:"e",monthly:50}),row("expenses",{id:"medical",kind:"medical",monthly:20}),row("expenses",{id:"shock",kind:"emergency",monthly:300,from:1,to:1})]}));
  eq(d.rows[0].essential,420);eq(d.rows[0].reserve,240);eq(d.rows[1].essential,120);
});
test("zero rate and one-period annuity, equal-principal and bullet",()=>{
  for(const method of ["annuity","principal","bullet"]){const d=sim(dry({cash:2000,loans:[loan({months:1,method})]}));eq(d.rows[0].principal,1200);eq(d.rows[0].debt,0);eq(d.rows[0].interest,0);eq(d.rows[1].principal,0);}
  const d=sim(dry({cash:2000,loans:[loan()]}));for(let m=0;m<12;m++){eq(d.rows[m].principal,100);eq(d.rows[m].debt,1100-100*m);}
});
test("independent equal principal, bullet, and contractual custom last balloon",()=>{
  for(const method of ["principal","bullet"]){const d=sim(dry({cash:2000,loans:[loan({annualRate:.12,method})]}));eq(d.rows[0].interest,12);eq(d.rows[0].principal,method==="bullet"?0:100);eq(d.rows[11].principal,method==="bullet"?1200:100);eq(d.rows[11].debt,0);}
  const d=sim(dry({cash:2000,loans:[loan({payment:80})]}));eq(d.rows[10].principal,80);eq(d.rows[11].principal,320);
});
test("recurring and one-off income rows, independent job loss and linear return",()=>{
  const h=dry({incomes:[income(100,{jobStart:2,jobMonths:2,recoveryMonths:2,returnFraction:.8}),income(25,{id:"j",kind:"business",every:2})]});
  const d=sim(h);assert.deepEqual(d.rows.slice(0,5).map(r=>r.income),[125,0,25,40,105]);
  const s={id:"joint",name:"特定月",paths:[E.path("unemploymentMonths",1,3,1,"j")]};eq(sim(h,undefined,s).rows[2].income,0);
  const d2=sim(dry({incomes:[income(100,{jobStart:1,jobMonths:1,returnFraction:1.2})]}));eq(d2.rows[1].income,120);
});
test("floating rate only reprices as the contract prescribes; fixed rate unchanged",()=>{
  const s={id:"s",name:"rate",paths:[E.path("loanRateDelta",.12,2,2)]};
  const d=sim(dry({cash:10000,loans:[loan({annualRate:.12,method:"bullet",rateType:"floating",resetFirst:3,resetEvery:3})]}),undefined,s);
  assert.deepEqual(d.rows.slice(0,6).map(r=>r.interest),[12,12,24,24,24,12]);
  const f=sim(dry({cash:10000,loans:[loan({annualRate:.12,method:"bullet"})]}),undefined,s);eq(f.rows[2].interest,12);
});
test("prepayment lowers payment or shortens term and does not double charge",()=>{
  const h=dry({cash:2000,loans:[loan()]});
  const run=mode=>sim(h,act({kind:"prepay",loan:"l",mode,month:1,amount:200}));
  const d=run("recast"),t=run("shorten");
  eq(d.rows[0].cash,1700);eq(d.rows[0].debt,900);eq(d.rows[1].principal,900/11);
  eq(t.rows[1].principal,100);eq(t.rows[9].debt,0);eq(t.rows[10].principal,0);
  assert.equal(t.byLoan.l.find(x=>x.prepay).end,10);
});
test("prepay minimum, mandatory reserve and explicit early termination fee",()=>{
  const a=act({kind:"prepay",loan:"l",mode:"recast",month:1,amount:200});
  const no=sim(dry({cash:3000,loans:[loan({prepayMin:300})]}),a);assert.equal(no.summary.blocked.length,1);eq(no.rows[0].prepaid,0);
  const r=sim(dry({cash:450,reserveMonths:3,minimumLiving:100,loans:[loan()]}),a);assert.equal(r.summary.blocked.length,1);eq(r.rows[0].prepaid,0);
  const ok=sim(dry({cash:2000,loans:[loan({settlementFee:20,prepayFee:.01})]}),act({kind:"prepay",loan:"l",month:1,mode:"full"}));
  eq(ok.rows[0].prepaid,1100);eq(ok.rows[0].prepayFees,31);eq(ok.rows[0].cash,769);
});
test("negative equity sale requires top-up, and prior discharge may require gross prefunding",()=>{
  const household=(cash,transferWithLien)=>dry({cash,properties:[home()],loans:[loan({collateral:"p",principal:100,method:"bullet",transferWithLien})]});
  const no=sim(household(19,true),listed());eq(no.rows[0].property,100);eq(no.rows[0].debt,100);eq(no.summary.blocked[0].need,1);
  const yes=sim(household(20,true),listed());eq(yes.rows[0].cash,0);eq(yes.rows[0].debt,0);eq(yes.rows[0].property,0);eq(yes.summary.saleNet,-20);eq(yes.rows[0].principal,0);
  const pref=sim(household(20,false),listed());eq(pref.summary.blocked[0].need,80);eq(pref.rows[0].debt,100);
});
test("economic sale closes once after lag, removes rent and settles every lien once",()=>{
  const h=dry({cash:100,properties:[home({use:"let",rent:10,saleLag:2,saleValue:200,closingFee:4,saleFee:.02})],
    loans:[loan({collateral:"p",principal:50,method:"bullet",annualRate:.12,transferWithLien:true}),loan({id:"l2",collateral:"p",principal:20,method:"bullet",transferWithLien:true})]});
  const d=sim(h,listed());assert.deepEqual(d.rows.slice(0,4).map(r=>r.rent),[10,10,0,0]);eq(d.rows[2].saleGross,200);eq(d.rows[2].closingPrincipal,70);
  eq(d.rows[2].closingInterest,.5);eq(d.rows[2].principal,0);eq(d.rows[2].saleFees,8);eq(d.rows[2].cash,240.5);eq(d.rows[3].saleGross,0);
});
test("vacancy, alternative housing/transport and locked/unmarketable assets",()=>{
  const r=sim(dry({properties:[home({use:"let",vacancy:1,rent:100})]}));eq(r.rows[0].rent,0);
  const h=dry({properties:[home({use:"occupied",replacementAllowed:false})]});assert.equal(sim(h,listed()).summary.blocked.length,1);
  const car=row("vehicles",{id:"p",value:200,saleValue:160,carry:10,necessary:true,replacementAllowed:true,replacementMonthly:7});
  const d=sim(dry({vehicles:[car]}),listed());eq(d.rows[0].replacement,7);eq(d.rows[0].carry,0);eq(d.rows[0].cash,153);
  assert.equal(sim(dry({properties:[home({lock:10})]}),listed()).summary.blocked.length,1);
  assert.equal(sim(dry({properties:[home({canSell:false})]}),listed()).summary.blocked.length,1);
});
test("financial settlement and one-time loss, deposit maturity and pledged/restricted use",()=>{
  const h=dry({financial:[sec({fee:.02,settle:2})]}),a=act({kind:"liquidate",asset:"f",month:1,mode:"all"});
  const s={id:"s",name:"loss",paths:[E.path("financialShock",-.5)]},d=sim(h,a,s);
  eq(d.rows[0].cash,0);eq(d.rows[0].receivables,49);eq(d.rows[1].receivables,49);eq(d.rows[2].cash,49);eq(d.rows[2].receivables,0);
  const held=sim(h,undefined,s);eq(held.rows[0].financial,50);eq(held.rows[1].financial,50);eq(held.rows[1].cash,0);
  const deposit=sim(dry({financial:[sec({kind:"deposit",maturity:3,settle:1})]}));eq(deposit.rows[1].financial,100);eq(deposit.rows[2].receivables,100);eq(deposit.rows[3].cash,100);
  assert.equal(sim(dry({financial:[sec({restriction:"restricted"})]}),a).summary.blocked.length,1);
  const pledge=sim(dry({cash:2000,financial:[sec({restriction:"pledged"})],loans:[loan({collateral:"f",kind:"margin"})]}),a);eq(pledge.rows[0].financial,100);assert.equal(pledge.summary.blocked.length,1);
});
test("staged security sale, total return without duplicated dividends",()=>{
  const h=dry({financial:[sec({annualReturn:.12})]}),d=sim(h);eq(d.rows[11].financial,112);eq(d.rows[11].cash,0);
  const r=sim(dry({financial:[sec()]}),act({kind:"liquidate",asset:"f",month:1,mode:"stages"}));assert.deepEqual(r.events.filter(e=>e.type==="trade").map(e=>e.month),[1,4,7,10]);eq(r.rows[9].cash,100);eq(r.rows[9].financial,0);
});
test("cash exhaustion leaves principal and unpaid interest; pending receipts cannot fund today",()=>{
  const h=dry({cash:5,minimumLiving:4,financial:[sec({settle:1})],loans:[loan({principal:120,annualRate:.12,months:1})]});
  const d=sim(h,act({kind:"liquidate",asset:"f",mode:"all",month:1})),r=d.rows[0];
  assert.equal(d.rows.length,1);eq(r.cash,0);eq(r.interest,1);eq(r.debt,120);eq(r.arrears,.2);eq(r.unpaid,120.2);eq(r.receivables,100);
  assert.equal(r.netWorth,null);assert.equal(d.summary.points[120],null);assert.equal(d.summary.terminalReal,null);eq(r.netResidual,0);
});
test("unfunded voluntary consumption stops the planned path without inventing payable debt",()=>{
  const h=dry({cash:100,expenses:[row("expenses",{id:"optional",kind:"discretionary",monthly:150})]});
  const r=sim(h);eq(r.summary.failureBreakdown.unfundedDiscretionary,50);eq(r.summary.failureBreakdown.missedDebtService,0);eq(r.rows[0].arrears,0);eq(r.rows[0].netResidual,0);
});
test("guarantee call and debts appear at the specified month",()=>{
  const d=sim(dry({cash:2000,loans:[loan({kind:"guarantee",start:3,method:"bullet"})]}));eq(d.rows[1].debt,0);eq(d.rows[2].debt,1200);eq(d.rows[2].netResidual,0);
});
test("small actual policy set, no feasible candidate, no terminal/regret ranking",()=>{
  const d=E.assess(dry({cash:1,minimumLiving:2}),[flat]);eq(d.coverage.evaluated,1);eq(d.commonCount,0);assert.equal(d.winners.robust,null);
  assert.equal(d.winners.leastGap,"S000");assert.equal(d.results[0].regret,null);eq(d.results[0].funding,1);
});
test("input intervals must have explicit center or use an endpoint; scenario units and overlaps checked",()=>{
  assert.throws(()=>sim(dry({cash:{low:1,high:3}})));
  eq(sim(dry({rangeCase:"low",cash:{low:1,high:3}})).rows[0].cash,1);
  eq(sim(dry({rangeCase:"high",cash:{low:1,high:3}})).rows[0].cash,3);
  const p=E.path("rentFactor",.8);assert.throws(()=>E.validateScenario({id:"x",name:"s",paths:[p,p]}));
  assert.throws(()=>E.validateScenario({id:"x",name:"s",paths:[{...p,unit:"%"}]}));
});
test("reverse thresholds are reruns, not a score, rent-sale equality and cash prepayment bound",()=>{
  const h=dry({incomes:[income(100)],minimumLiving:90,properties:[home({value:1000,saleValue:1000})]});
  const b=E.reverse(h,flat);eq(b.grid.wage.boundary.value,11);eq(b.grid.wage.boundary.previousSafe,10);eq(b.grid.job.boundary.value,1);
  eq(b.breakEven.grossMonthlyThreshold,0);eq(b.breakEven.saleNet,1000);assert.equal(b.grid.delay.applicable,false);
  const pre=E.reverse(dry({cash:1200,loans:[loan()]}),flat).affordablePrepay;eq(pre.largestTested,1100);eq(pre.liquidityCeiling,1100);
});
test("unconfirmed loan permissions, windows and fees suppress optional actions but preserve contract",()=>{
  const raw={id:"L",name:"单列合同",kind:"consumer",principal:10000,annualRate:.1,months:12};
  for(const terms of [{},{canPrepay:true,prepayFrom:1,allowRecast:true,allowShorten:true},{prepayFee:0,settlementFee:0}]){
    const h=dry({cash:20000,loans:[{...raw,...terms}]}),a=E.assess(h,[flat],100);
    assert.equal(a.commonCount,1);assert.equal(a.coverage.evaluated,1);assert.ok(a.coverage.exclusions.some(e=>e.reason.includes("未确认")));
    assert.equal(sim(h,act({kind:"prepay",loan:"L",month:1,mode:"full"})).summary.blocked.length,1);
  }
  const explicit=dry({cash:20000,loans:[{...raw,...knownTerms.loans}]});
  assert.ok(E.assess(explicit,[flat],100).results.some(r=>r.feasible&&r.strategy.actions.some(a=>a.mode==="full")));
  const partialOnly={...knownTerms.loans,allowRecast:null,allowShorten:null};assert.equal(E.enumerate(E.prepare(dry({cash:20000,loans:[{...raw,...partialOnly}]}),[flat]).h,100).strategies.length,2);
});
test("unknown asset release, fees, wait and mortgage fees are never imputed to allow a sale",()=>{
  const full=home({value:500,saleValue:400});
  for(const key of ["canSell","closingFee","saleFee","saleLag","lock","saleValue"]){
    const partial={...full};delete partial[key];const h=dry({cash:1000,properties:[partial]});
    assert.equal(E.assess(h,[flat],100).coverage.evaluated,1);const d=sim(h,listed());assert.equal(d.summary.blocked.length,1);eq(d.rows[0].property,500);
  }
  const withoutWait={...full,saleLag:null}, reverseUnknown=E.reverse(dry({cash:2,minimumLiving:1,properties:[withoutWait]}),flat,listed());
  assert.equal(reverseUnknown.grid.delay.firstBlocked,0);assert.equal(reverseUnknown.grid.delay.boundary.failureMonth,3);
  for(const key of ["fee","settle","unlock","restriction"]){
    const partial=sec();delete partial[key];const h=dry({financial:[partial]});assert.equal(E.assess(h,[flat],100).coverage.evaluated,1);
    assert.equal(sim(h,act({kind:"liquidate",asset:"f",month:1,mode:"all"})).summary.blocked.length,1);
  }
  for(const key of ["prepayFee","settlementFee","transferWithLien"]){
    const lien=loan({collateral:"p",transferWithLien:true});delete lien[key];
    const z=sim(dry({cash:1000,properties:[full],loans:[lien]}),listed());eq(z.rows[0].saleGross,0);assert.ok(z.summary.blocked[0].reason.includes("未确认"));
  }
});
test("same-month approved pledged liquidation retires margin once, including transaction and contract charges",()=>{
  const instrument=sec({value:3000,restriction:"pledged"}),leverage=loan({principal:1000,annualRate:0,method:"bullet",collateral:"f",kind:"margin",transferWithLien:true});
  const sold=act({kind:"liquidate",asset:"f",mode:"all",month:1});
  let d=sim(dry({minimumLiving:10,financial:[instrument],loans:[leverage]}),sold);
  eq(d.rows[0].cash,1990);eq(d.rows[0].closingPrincipal,1000);eq(d.rows[0].debt,0);eq(d.rows[0].financial,0);eq(d.summary.supportMonths,120);
  d=sim(dry({minimumLiving:10,financial:[{...instrument,fee:.02}],loans:[{...leverage,annualRate:.12,prepayFee:.01,settlementFee:25,monthlyFee:7}]}),sold);
  eq(d.rows[0].cash,1878);eq(d.rows[0].closingInterest,10);eq(d.rows[0].releaseFees,35);eq(d.rows[0].securityTradeFees,60);eq(d.rows[0].netResidual,0);
  for(const denied of [{canPrepay:false},{transferWithLien:false},{prepayFee:null},{settlementFee:null},{prepayFrom:3}]){
    const r=sim(dry({minimumLiving:10,financial:[instrument],loans:[{...leverage,...denied}]}),sold);
    assert.equal(r.summary.firstFailure,1);eq(r.rows[0].financial,3000);eq(r.rows[0].debt,1000);assert.equal(r.summary.blocked.length,1);
  }
});
test("pledged delayed closing, locked quote and top-up are reconciled at cash settlement",()=>{
  const asset=sec({value:3000,restriction:"pledged",settle:2}),debt=loan({principal:1000,method:"bullet",collateral:"f",kind:"margin",transferWithLien:true});
  const sold=act({kind:"liquidate",asset:"f",mode:"all",month:1});
  const h=dry({cash:25,minimumLiving:10,financial:[asset],loans:[debt]});
  const d=sim(h,sold,{id:"s",name:"valuation",paths:[E.path("financialShock",-.5,2)]});
  assert.deepEqual(d.rows.slice(0,3).map(r=>r.cash),[15,5,1995]);assert.deepEqual(d.rows.slice(0,3).map(r=>r.financial),[3000,1500,0]);
  eq(d.rows[1].receivables,0);eq(d.rows[2].securityReceipts,3000);eq(d.rows[2].closingPrincipal,1000);assert.equal(d.summary.blocked.length,0);
  const urgent=sim({...h,cash:0},sold);eq(urgent.summary.firstFailure,1);eq(urgent.rows[0].securityReceipts,0);eq(urgent.rows[0].debt,1000);
  for(const cash of [313,314]){
    const r=sim(dry({cash,financial:[{...asset,value:700,fee:.02,settle:0}],loans:[debt]}),sold);
    if(cash===313){eq(r.summary.blocked[0].need,1);eq(r.rows[0].financial,700);eq(r.rows[0].debt,1000);}
    else{eq(r.rows[0].cash,0);eq(r.rows[0].financial,0);eq(r.rows[0].debt,0);}
  }
});
test("candidate amounts include current received wage after living cost and contractual installment",()=>{
  const h=dry({cash:0,minimumLiving:100,incomes:[income(1000)],loans:[loan({principal:5000,months:10,prepayMin:100})]});
  const study=E.assess(h,[flat],100),candidate=study.results.find(r=>r.strategy.actions.some(a=>a.mode==="recast"&&a.amount===200));
  assert.ok(candidate&&candidate.feasible);eq(E.inspect(study,candidate.strategy.id,"flat").rows[0].cash,200);
});
test("demo common feasible set, deterministic unique policies, regret and residuals",()=>{
  const a=E.assess(sample,scenarios,500),again=E.enumerate(a.prepared.h,500);
  assert.deepEqual(again.strategies,a.results.map(r=>r.strategy));eq(new Set(again.strategies.map(s=>JSON.stringify(s.actions))).size,500);eq(a.results[0].strategy.actions.length,0);
  const common=a.results.filter(r=>r.feasible),failed=a.results.filter(r=>r.gap>0);assert.ok(common.length>=100);assert.ok(a.coverage.distinctFeasibleMonthlyTrajectories>=100);assert.ok(a.shortlist.length>=10&&a.shortlist.length<=20);
  for(const r of a.results)for(const v of Object.values(r.outcomes)){assert.ok(v.maxCashResidual<.00001);assert.ok(v.maxNetResidual<.00001);if(!v.completed)assert.equal(v.terminalReal,null);}
  for(const r of common){const regret=Math.max(...scenarios.map(s=>Math.max(...common.map(z=>z.outcomes[s.id].terminalReal))-r.outcomes[s.id].terminalReal));eq(r.regret,regret);}
  assert.equal(a.results[0].outcomes.severe.firstFailure,101);
  const initial=sim({...sample,cash:180000},undefined,scenarios.find(s=>s.id==="severe"));assert.equal(initial.summary.firstFailure,26);
  fs.writeFileSync(path.join(__dirname,"legacy_cash_stress.json"),JSON.stringify({dataKind:"synthetic_example",parent:"synthetic_household.json",override:{cash:180000},scenario:"severe",strategy:"S000",firstFailure:initial.summary.firstFailure,firstUnpaid:initial.summary.worstGap,matched280kFirstFailure:a.results[0].outcomes.severe.firstFailure},null,2)+"\n");
  const compact={inputKind:sample.dataKind,coverage:a.coverage,common:a.commonCount,distinctFeasibleMonthlyTrajectories:a.coverage.distinctFeasibleMonthlyTrajectories,distinctMonthlyTrajectories:a.coverage.distinctMonthlyTrajectories,pareto:common.filter(r=>r.pareto).length,shortlist:a.shortlist,winners:a.winners,atLeastOneCashFailure:failed.length,
    perScenario:Object.fromEntries(scenarios.map(s=>[s.id,{feasible:a.results.filter(r=>r.outcomes[s.id].feasible).length,cashFailed:a.results.filter(r=>!r.outcomes[s.id].completed).length}]))};
  fs.writeFileSync(path.join(__dirname,"sample_summary.json"),JSON.stringify(compact,null,2)+"\n");
  const lines=["inputKind,strategy,scenario,commonFeasible,trajectory,feasible,firstFailure,unpaid,minCash120,finalReal,maxRegret,pareto,blocked,actions"];
  const field=v=>v==null?"":typeof v==="number"?Number(v.toFixed(6)):typeof v==="boolean"?String(v):'"'+String(v).replace(/"/g,'""')+'"';
  for(const r of a.results)for(const s of scenarios){const o=r.outcomes[s.id];lines.push([sample.dataKind,r.strategy.id,s.id,r.feasible,r.trajectory,o.feasible,o.firstFailure,o.worstGap,o.minCash120,o.terminalReal,r.regret,r.pareto,JSON.stringify(o.blocked),JSON.stringify(r.strategy.actions)].map(field).join(","));}
  fs.writeFileSync(path.join(__dirname,"synthetic_strategy_results.csv"),lines.join("\n")+"\n");
  const d=E.inspect(a,"S000","severe");fs.writeFileSync(path.join(__dirname,"sample_baseline_severe_months.json"),JSON.stringify(d.rows)+"\n");
  return compact;
});
const actual={node:process.version,checks:tests.length,failures:errors.length,tests,errors};
fs.writeFileSync(path.join(__dirname,"checks.json"),JSON.stringify(actual,null,2)+"\n");
console.log(JSON.stringify({checks:tests.length,failures:errors},null,2));if(errors.length)process.exitCode=1;
