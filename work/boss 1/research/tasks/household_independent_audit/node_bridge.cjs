/* Stand-alone audit adapter. This file calls the public API and captures the actual observable ledger. */
'use strict';
const fs=require('node:fs'), crypt=require('node:crypto'), path=require('node:path');
const productPath=path.resolve(process.argv[2]);
function reviewedAPI(){
  if(!productPath.endsWith('.html'))return require(productPath);
  const page=fs.readFileSync(productPath,'utf8');
  const scripts=[...page.matchAll(/<script\b[^>]*>([\s\S]*?)<\/script>/gi)].map(m=>m[1]);
  const inline=scripts.find(body=>body.includes('root.HouseholdEngine = factory()'));
  if(!inline)throw Error('Cannot locate the packaged monthly ledger');
  const vm=require('node:vm'),browserGlobal=vm.createContext({});
  new vm.Script(inline,{filename:'packaged-engine.js'}).runInContext(browserGlobal);
  return browserGlobal.HouseholdEngine;
}
const E=reviewedAPI();
const digest=value=>crypt.createHash('sha256').update(JSON.stringify(value)).digest('hex');
const identity=(row)=>row.map(v=>typeof v==='number' ? Math.round(v*100) : v);
const inputs=JSON.parse(fs.readFileSync(0,'utf8'));
const output={};
for(const r of inputs) {
  try {
    if(r.op==='blank'){output[r.id]=E.blank();continue;}
    if(r.op==='reverse'){output[r.id]=E.reverse(r.household,r.scenarios[0],r.strategy);continue;}
    if(r.op==='simulate'){output[r.id]=E.simulate(r.household,r.scenarios[0],r.strategy);continue;}
    if(r.op!=='assess')throw Error('Unknown audit operation');
    const t=E.assess(r.household,r.scenarios,r.limit||100), ranks={};
    for(const k of ['cash','debt','wealth','regret'])ranks[k]=E.rank(t.results,k).map(x=>x.strategy.id);
    const all=t.results.map(x=>{
      const summaries={};
      for(const p of r.scenarios){
        const s=x.outcomes[p.id],full=E.inspect(t,x.strategy.id,p.id),a=full.rows;
        const vals=a.map(m=>identity([m.cash,m.debt,m.financial,m.property,m.vehicle,m.rent,m.receivables,m.netWorth,m.unpaid,m.prepaid,m.saleGross,m.discretionary]));
        const valid=a.every((m,i)=>m.month===i+1&&m.cash>=-1e-7&&m.debt>=-1e-7)&&a.length===(s.firstFailure||120)&&s.terminalReal===full.summary.terminalReal;
        summaries[p.id]={valid,rows:a.length,hash:digest(vals),completed:s.completed,feasible:s.feasible,firstFailure:s.firstFailure,terminalReal:s.terminalReal,terminalNominal:s.terminalNominal,minCash120:s.minCash120,interest:s.interestTotal,rentNet:s.rentNet,saleNet:s.saleNet,peakDsr:s.peakDsr,peakDsrInfinite:s.peakDsrInfinite,blocked:s.blocked};
      }
      return {id:x.strategy.id,trajectory:x.trajectory,actions:x.strategy.actions,feasible:x.feasible,regret:x.regret,recoveryCost:x.recoveryCost,pareto:x.pareto,worstWealth:x.worstWealth,minCash:x.minCash,funding:x.funding,support:x.support,scenarios:summaries};
    });
    output[r.id]={coverage:t.coverage,winners:t.winners,commonCount:t.commonCount,shortlist:t.shortlist,best:t.best,all,ranks};
  }catch(e){output[r.id]={error:e.message};}
}
process.stdout.write(JSON.stringify(output));
