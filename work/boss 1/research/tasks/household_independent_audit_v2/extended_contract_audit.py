"""Independent additions for typed scenario targets and contractual prepayment capacity.

The Decimal reference ledger constructs due principal, interest, calendar reset,
actual paid extras and cash without calling the product or copying its code.
"""
import datetime as dt
from decimal import Decimal
import gzip
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True
import independent_numeric as base
from migration import explicit_terms

HERE = Path(__file__).resolve().parent
FORMAL = HERE.parents[2] / 'formal' / 'calculator.html'
requests = []
results = []


def add(name, household, paths=None, actions=(), op='simulate'):
    request = {'id': name, 'op': op, 'household': household,
               'scenarios': [base.scenario(name, paths)],
               'strategy': {'id': 'manual', 'actions': list(actions)}, 'limit': 100}
    requests.append(request)


def loan(principal=9000, rate=.12, months=10, **overrides):
    terms = explicit_terms(secured=bool(overrides.get('collateral')))
    terms.update(method='principal', prepayMax=420, prepayPeriodMax=600,
                 prepayPeriodMonths=3, prepayPeriodRemaining=2, prepayPeriodUsed=250)
    terms.update(overrides)
    return base.debt(principal, rate, months, **terms)


def extra(month, value, loan_id='L', mode='shorten'):
    action = {'kind': 'prepay', 'loan': loan_id, 'month': month, 'mode': mode}
    if mode != 'full':
        action['amount'] = value
    return action


def expect(name, value, expected, tolerance=1e-7):
    def compare(a,b):
        if isinstance(b, bool) or b is None:
            return a is b
        if isinstance(b, (int, float, Decimal)):
            return isinstance(a, (int,float)) and abs(float(a)-float(b))<=tolerance
        if isinstance(b, list):
            return isinstance(a, list) and len(a)==len(b) and all(compare(i,j) for i,j in zip(a,b))
        return a==b
    vals=lambda o:json.loads(json.dumps(o,default=float))
    results.append({'check':name,'pass':compare(value,expected),'observed':vals(value),'expected':vals(expected)})


# The targeted/wildcard pair overlaps deliberately. Income A and B have different
# bases, and the business receipts have a separate month-2 interruption.
family = base.household(cash=1000, incomes=[base.income('A',900),base.income('B',600),
                         base.income('Shop',240,kind='business')],properties=[base.home()])
for name, targeted in [('typed_valid','A'),('typed_typo','A0'),('typed_wrong','Shop')]:
    paths=[base.shock('wageFactor',.8,1,3),base.shock('wageFactor',.4,2,2,targeted),
           {'key':'businessFactor','mode':'level','value':.5,'target':'Shop','unit':'倍','start':2,
            'duration':1,'range':[.5,.5],'sourceId':'audit','assumption':'stress_test','editable':True}]
    add(name,family,paths)
for op in ['assess','reverse']:
    add('wrong_class_'+op,family,[base.shock('rentFactor',.4,2,2,'A')],op=op)
add('household_only_wrong',family,[base.shock('inflationAnnual',.1,1,12,'P')]);
missing=base.shock('wageFactor',.2);del missing['target'];add('missing_target',family,[missing]);
add('explicit_wildcard_empty_category',base.household(cash=727),[base.shock('wageFactor',.2,1,3)])

# Period 0 has two months remaining and 250 of its 600-yuan capacity is already used.
# The independent calendar below names the months in each contractual bucket.
calendar_terms=loan()
regular=base.household(cash=30000,loans=[calendar_terms]);schedule={1:220,2:130,3:420,4:180,5:1,6:250}
add('multi_period',regular,actions=[extra(m,amount) for m,amount in schedule.items()])
add('reverse_day1',regular,op='reverse')
add('cross_lender',base.household(cash=50000,loans=[loan(),loan(id='M',prepayMax=500,prepayPeriodUsed=100)]),
    actions=[extra(1,300),extra(1,450,'M'),extra(2,100),extra(2,50,'M')])
add('relative_start',base.household(cash=30000,loans=[loan(kind='guarantee',start=4)]),
    actions=[extra(4,250),extra(5,100),extra(6,420)])
add('cross_reset_reverse',base.household(cash=30000,loans=[loan(prepayFrom=4,prepayPeriodUsed=599.99)]),op='reverse')
add('capped_full_enumeration',base.household(cash=8000,loans=[loan(3000,0,6,prepayMax=700,
    prepayPeriodMax='unlimited',prepayPeriodMonths=None,prepayPeriodRemaining=None,prepayPeriodUsed=None)]),op='assess')
add('forbid_full_by_alias',base.household(cash=8000,loans=[loan(3000,0,6,allowFull=False,prepayMax='unlimited',
    prepayPeriodMax='unlimited',prepayPeriodMonths=None,prepayPeriodRemaining=None,prepayPeriodUsed=None)]),actions=[extra(5,500)])

for label,fee_basis,limit in [('extra','extra',1800),('balance','balance',1800),('one_cent_short','extra',1799.99)]:
    x=loan(2400,.12,4,kind='mortgage',collateral='P',transferWithLien=True,prepayMax=limit,prepayPeriodMax=2400,
           prepayPeriodUsed=600,prepayFee=.015,settlementFee=9,salePayoffFeeBase=fee_basis)
    f=base.household(cash=5000,properties=[base.home(3500,3400,saleFee=.02,closingFee=5)],loans=[x])
    add('sale_basis_'+label,f,actions=[base.sell()])
# Loan maturity falls beyond this sale in both examples. The contractual exception
# bypasses only voluntary limits; it still charges its independently specified fees.
for label,month in [('before',1),('on',2)]:
    x=loan(2400,0,4,kind='car',collateral='C',canPrepay=False,allowFull=False,transferWithLien=True,
           salePayoffRule='sale_exception',salePayoffFrom=2,salePayoffFee=.02,saleSettlementFee=11,salePayoffFeeBase='extra')
    f=base.household(cash=5000,vehicles=[base.car(value=3300,saleValue=3300,saleLag=0,necessary=False,carry=0)],loans=[x]);add('sale_exception_'+label,f,actions=[base.sell('C',month)])

# At contractual maturity a distinct confirmed administrative fee is payable
# exactly once; the ordinary prepayment prohibitions have no effect on due principal.
for tag,admin in [('included','in_asset_cost'),('additional',23),('unknown',None)]:
    item=loan(1200,0,2,kind='car',collateral='C',transferWithLien=True,canPrepay=False,allowFull=False,
              salePayoffRule='forbidden',saleMaturityReleaseFee=admin)
    c=base.car(value=1800,saleValue=1800,necessary=False,carry=0,saleLag=0,closingFee=18)
    add('natural_'+tag,base.household(cash=2500,vehicles=[c],loans=[item]),actions=[base.sell('C',2)])

# Quota is exhausted at the order date; an explicit contractual reset occurs at
# settlement month 3. The security price suffers a 50% shock while clearing so the
# 1st-month executable quote and 3rd-month legal capacity must be tested separately.
for tag,lag in [('before',1),('on',2)]:
    stock=base.security(3300,restriction='pledged',settle=lag,fee=.01)
    x=loan(1200,.12,12,kind='margin',method='bullet',collateral='F',transferWithLien=True,
           prepayMax=1200,prepayPeriodMax=1200,prepayPeriodUsed=1200)
    add('pledged_reset_'+tag,base.household(cash=1000,minimum=10,financial=[stock],loans=[x]),
        [base.shock('financialShock',-.5,2,1,'F')],[base.trade()])


def verify(out):
    rows=lambda id:out[id]['rows']
    values=lambda id,field,n:[r[field] for r in rows(id)[:n]]
    expect('specific wage overrides wildcard only for A; business path stays separate',
           values('typed_valid','income',4),[1440,960,1080,1740])
    for id,token in [('typed_typo','A0'),('typed_wrong','Shop'),('wrong_class_assess','A'),
                     ('wrong_class_reverse','A'),('household_only_wrong','P'),('missing_target','目标')]:
        msg=out[id].get('error','');expect('reject explicit invalid input '+id,bool(msg and token in msg and id in msg),True)
    expect('explicit global wildcard may target an empty household category',values('explicit_wildcard_empty_category','cash',2),[727,727])
    cash=Decimal('30000');balance=Decimal('9000');expected_cash=[];expected_debt=[];expected_interest=[];expected_extra=[]
    buckets=[([1,2],Decimal(350)),([3,4,5],Decimal(600)),([6,7,8],Decimal(600))];available=[left for months,left in buckets]
    accepted=[]
    for month in range(1,7):
        index=next(i for i,(months,_) in enumerate(buckets) if month in months)
        due_interest=balance/100;balance-=900;cash-=900+due_interest;amount=Decimal(schedule[month]);paid=Decimal(0)
        if amount<=min(Decimal(420),available[index],balance):
            cash-=amount;balance-=amount;available[index]-=amount;paid=amount;accepted.append([month,float(amount),float(available[index])])
        expected_extra.append(paid);expected_interest.append(due_interest);expected_cash.append(cash);expected_debt.append(balance)
    for field,ref in [('prepaid',expected_extra),('interest',expected_interest),('cash',expected_cash),('debt',expected_debt)]:
        expect('six month independent Decimal contract '+field,values('multi_period',field,6),ref)
    payments=lambda key,loan_id:[[r['month'],r['prepay'],r['remainingQuota']] for r in out[key]['byLoan'][loan_id] if 'prepay' in r]
    expect('consumed quota across three named calendar buckets',payments('multi_period','L'),accepted)
    expect('fifth month rejected without exhausting next interval',[r['month'] for r in out['multi_period']['summary']['blocked']],[5])
    expect('reverse cap is binding from historic usage and remaining component',out['reverse_day1']['affordablePrepay']['largestTested'],350)
    expect('first lender unused balance stays independent',payments('cross_lender','L'),[[1,300,50]])
    expect('second lender unused balance stays independent',payments('cross_lender','M'),[[1,450,50],[2,50,0]])
    expect('loan age, not household calendar origin, starts guarantee quota buckets',payments('relative_start','L'),[[4,250,100],[5,100,0],[6,420,180]])
    expect('cap after reset discards prior period use',out['cross_reset_reverse']['affordablePrepay']['largestTested'],420)
    runs=out['capped_full_enumeration']['all'];full=[a['month'] for r in runs if r['feasible'] for a in r['actions'] if a['mode']=='full'];expect('first possible voluntary full only after contractual outstanding balance falls within 700',sorted(set(full)),[5]);expect('no finite-cap feasible partial over 700',max(a.get('amount',0) for r in runs if r['feasible'] for a in r['actions'])<=700,True)
    expect('partial label cannot evade prohibition on clearing remaining 500',values('forbid_full_by_alias','prepaid',5),[0]*5)
    for tag,fee,end in [('extra',36,5867),('balance',45,5858)]:
        z=rows('sale_basis_'+tag)[0];expect('sale '+tag+' uses selected base and separate principal', [z['releaseFees'],z['closingPrincipal'],z['closingInterest'],z['saleFees'],z['cash'],z['debt']],[fee,2400,24,73,end,0]);entry=out['sale_basis_'+tag]['byLoan']['L'][0];expect('sale separates scheduled 600 and extra 1800 '+tag,[entry['scheduledPrincipal'],entry['earlyPrincipal']],[600,1800])
    z=rows('sale_basis_one_cent_short')[0];expect('one cent below extra balance prevents legal close while contractual debt is paid',[z['saleGross'],z['principal'],z['interest'],z['cash'],z['debt']],[0,600,24,4376,1800])
    expect('sale exception waits until explicitly contracted month',values('sale_exception_before','saleGross',2),[0,0]);z=rows('sale_exception_on')[1];expect('separate sale-only fee on 1200 extra plus 11 despite voluntary full prohibition',[z['closingPrincipal'],z['releaseFees'],z['cash'],z['debt']],[1800,35,5865,0])
    for tag,expectation in [('included',[1800,600,18,0,3082]),('additional',[1800,600,18,23,3059]),('unknown',[0,0,0,0,1300])]:
        z=rows('natural_'+tag)[1];expect('administrative charge only on natural-maturity asset closing '+tag,[z[k] for k in ('saleGross','closingPrincipal','saleFees','releaseFees','cash')],expectation)
    z=rows('pledged_reset_before')[1];expect('security settling before quota reset remains pledged at shocked price',[z['securityReceipts'],z['financial'],z['debt'],z['cash']],[0,1650,1200,956]);expect('no available sale proceeds in two months before settlement',values('pledged_reset_on','securityReceipts',2),[0,0]);z=rows('pledged_reset_on')[2];expect('quote locked at 3300 but 3rd-month release uses newly available 1200 quota',[z['securityReceipts'],z['closingPrincipal'],z['closingInterest'],z['financial'],z['debt'],z['cash']],[3267,1200,12,0,0,3001])


def main():
    frozen=base.sha(FORMAL.read_bytes()); (HERE/'extended_inputs.json').write_text(base.dump(requests))
    packed=base.run_engine(requests,FORMAL);module=base.run_engine(requests)
    assert base.sha(FORMAL.read_bytes())==frozen
    verify(packed);expect('formal inline and CommonJS agree on every extension',base.sha(base.canonical(packed)),base.sha(base.canonical(module)))
    raw=base.canonical(packed);(HERE/'extended_outputs.json.gz').write_bytes(gzip.compress(raw,mtime=0))
    report={'utc':dt.datetime.now(dt.timezone.utc).isoformat(),'reviewer':'/root/household_independent_audit','formalHTML':frozen,
            'engine':base.sha((base.AUTHOR/'engine.js').read_bytes()),'requests':len(requests),'checks':len(results),
            'passed':sum(r['pass'] for r in results),'failed':sum(not r['pass'] for r in results),
            'inputSHA256':base.sha((HERE/'extended_inputs.json').read_bytes()),'uncompressedOutputSHA256':base.sha(raw),
            'assertions':results};(HERE/'extended_report.json').write_text(base.dump(report));print(base.dump({k:v for k,v in report.items() if k!='assertions'}));print(base.dump([r for r in results if not r['pass']]));return bool(report['failed'])

if __name__=='__main__':sys.exit(main())
