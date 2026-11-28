// Reproduce the old release candidate's counterexamples from a preserved Git object.
'use strict';
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const crypto = require('node:crypto');
const {execFileSync} = require('node:child_process');
const assert = require('node:assert/strict');

const root = path.resolve(__dirname, '../../../../..');
const inputFile = path.join(__dirname, 'pre_repair_cases.json');
const input = JSON.parse(fs.readFileSync(inputFile, 'utf8'));
const htmlFile = 'work/boss 1/formal/calculator.html';
const html = execFileSync('git', ['show', input.as_tested + ':' + htmlFile], {cwd:root});
const sha = b => crypto.createHash('sha256').update(b).digest('hex');
assert.equal(sha(html), input.html_sha256);
const scripts = [...html.toString('utf8').matchAll(/<script>([\s\S]*?)<\/script>/g)];
assert.equal(scripts.length, 2);
const context = vm.createContext({});
vm.runInContext(scripts[0][1], context);
const E = context.HouseholdEngine;
const h = {...E.blank(), ...input.wage_household, expenses:[{id:'medical', name:'一次性试算', kind:'medical', monthly:0}]};
const p = input.wage_path;
const targetCases = input.targets.map(target => {
  const scenario = {id:'stress',name:'收入减半',paths:[E.path(p.key,p.value,p.start,p.duration,target.id)]};
  const assessment = E.assess(h,[scenario],100);
  const outcome = assessment.results[0].outcomes.stress;
  return {
    target:target.id, meaning:target.meaning, acceptedWithoutError:true, feasibleRules:assessment.commonCount,
    firstFailure:outcome.firstFailure, firstMonthCash:outcome.firstCash,
    fundingGap:outcome.worstGap, terminal:outcome.terminalReal
  };
});
const quiet = {id:'quiet',name:'原合同',paths:[]};
const loanHousehold = {...E.blank(), ...input.contract_household};
const assessed = E.assess(loanHousehold,[quiet],100);
const policies = assessed.results.map(r => ({
  id:r.strategy.id, mode:r.strategy.actions[0]?.mode || 'baseline',
  feasible:r.feasible, extraPrincipal:r.outcomes.quiet.prepaid,
  endingRealWealth:r.outcomes.quiet.terminalReal
}));
const direct = E.simulate(loanHousehold,quiet,{id:'explicit',actions:[{kind:'prepay',loan:'loan',mode:'shorten',month:1,amount:1001}]});
const reverse = E.reverse(loanHousehold,quiet,E.baseStrategy(),{loanId:'loan'});
assert.equal(targetCases[0].firstFailure,1);
assert.equal(targetCases[0].fundingGap,200);
assert.equal(targetCases[0].terminal,null);
for(const r of targetCases.slice(1)){
  assert.equal(r.feasibleRules,1);
  assert.equal(r.terminal,36000);
}
assert.equal(policies.length,6);
assert.equal(policies.filter(r=>r.feasible&&r.extraPrincipal>1000).length,5);
assert.equal(assessed.winners.wealth,policies.find(r=>r.mode==='full').id);
assert.equal(direct.summary.prepaid,1001);
console.log(JSON.stringify({
  scope:'Synthetic negative controls on the immutable pre-repair HTML. Node VM; no real browser.',
  reviewer:'/root/release_audit',frozenCommit:input.as_tested,htmlSha256:sha(html),
  engineSha256:sha(scripts[0][1]),casesSha256:sha(fs.readFileSync(inputFile)),scriptSha256:sha(fs.readFileSync(__filename)),
  node:process.version, targetCases, policies, winners:assessed.winners,
  overQuotaDirect:{principal:direct.summary.prepaid, feasible:direct.summary.feasible},
  largestTestedEarlyPayment:reverse.affordablePrepay.largestTested
},null,2));
