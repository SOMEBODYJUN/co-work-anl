#!/usr/bin/env python3
from __future__ import annotations
import hashlib, json
from fractions import Fraction
from pathlib import Path

ROOT=Path(__file__).parent

def F(x): return Fraction(str(x))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()

checks=[]
# Distorted group joint-slot input/output fixtures.
d=json.loads((ROOT/'distorted_group_joint_slot_cases.json').read_text())
assert d['seed']==2984106 and len(d['cases'])==16
for ci,c in enumerate(d['cases']):
    inp=c['input']; out=c['output']; groups=inp['groups']
    assert len(out['private_assignment'])==len(groups), (ci,'group count')
    home=[Fraction(0) for _ in groups]; sink=[Fraction(0) for _ in range(inp['sinks'])]
    # Macro home slots contribute their machine-dependent processing time.
    for mi,slot in enumerate(out['macro_home_slot']):
        h=slot[0]; assert isinstance(h,int) and 0 <= h < len(groups), (ci,mi,'bad macro home')
        mt=inp['macros'][mi]; assert str(h) in mt, (ci,mi,h,'macro not eligible')
        home[h] += F(mt[str(h)])
    for gi,(g,asg) in enumerate(zip(groups,out['private_assignment'])):
        ws=g['w']; assert len(asg)==len(ws), (ci,gi,'assignment length')
        h=Fraction(0)
        for ji,(kind,target) in enumerate(asg):
            if kind=='h':
                assert isinstance(target,int) and target>=0, (ci,gi,ji,'bad home')
                h += F(ws[ji])
            elif kind=='z':
                assert str(target) in [str(s) for s in g.get('E',[])], (ci,gi,ji,'sink not eligible')
                pmap=g.get('p',{}); vals=pmap.get(str(target),pmap.get(target,[]))
                assert len(vals)==len(ws), (ci,gi,ji,'p length')
                sink[target] += F(vals[ji])
            else:
                raise AssertionError((ci,gi,ji,'bad kind',kind))
        home[gi] += h
    assert [F(x) for x in out['home_loads']]==home, (ci,'home load mismatch',home,out['home_loads'])
    assert [F(x) for x in out['sink_loads']]==sink, (ci,'sink load mismatch',sink,out['sink_loads'])
    assert len(out['macro_home_slot'])==len(inp['macros']), (ci,'macro output count')
    assert len(out['token_loads'])==inp['sinks'] and len(out['demand'])==len(groups)
checks.append({'name':'distorted_group_joint_slot_cases','cases':len(d['cases']),'seed':d['seed'],'verified':'all private assignment target legality and exact home/sink load sums'})

# Exception-arity sharp family.
d=json.loads((ROOT/'dual_rail_exception_arity_sharp_certificates.json').read_text())
cs=d['certificates']; assert d['scope'].startswith('A1..8') and d['status']=='pass' and len(cs)==8
for cert in cs:
    A=cert['A']; m=cert['machines']; jobs=cert['original_jobs']; sigma=cert['sigma']; loads=cert['actual_machine_loads']
    assert m==4*A+4 and len(jobs)==6*A+3 and len(sigma)==len(jobs)==6*A+3 and len(loads)==m
    calc=[Fraction(0) for _ in range(m)]
    for j,(job,mi) in enumerate(zip(jobs,sigma)):
        assert str(mi) in job, (A,j,mi)
        calc[mi]+=F(job[str(mi)])
    assert calc==[F(x) for x in loads], (A,'loads')
    optimum=Fraction(A+1,A)
    assert F(cert['actual_makespan'])==optimum==F(cert['proved_optimum'])==max(calc), (A,'optimum')
checks.append({'name':'dual_rail_exception_arity_sharp_certificates','A_range':[1,8],'verified':'all 8 sigma assignments legal, exact machine loads and makespan=(A+1)/A'})

# Full-cube A=3 certificate and duplicate certificate.
d=json.loads((ROOT/'dual_rail_fullcube_A3_actual_certificate.json').read_text())
assert d['status']=='constructed' and d['instance']['A']==3 and d['instance']['d']==5
assert d['exact_value_formula']=={'B':3,'rail_capacity':2,'total_removed_ports':7,'value':'9/8'}
for label,cert in [('hand',d['A3_hand_certificate']),('certificate',d['certificate'])]:
    jobs=d['instance']['jobs']; sigma=cert['sigma']; loads=cert['actual_machine_loads']
    assert len(jobs)==165 and len(sigma)==165 and len(loads)==42, (label,'lengths')
    calc=[Fraction(0) for _ in range(42)]
    for j,(job,mi) in enumerate(zip(jobs,sigma)):
        assert str(mi) in job['eligible'], (label,j,mi)
        calc[mi]+=F(job['eligible'][str(mi)])
    assert calc==[F(x) for x in loads], (label,'loads')
    assert max(calc)==F(cert['actual_makespan'])==Fraction(9,8), (label,'makespan')
checks.append({'name':'dual_rail_fullcube_A3_actual_certificate','A':3,'machines':42,'jobs':165,'verified':'both supplied sigma certificates legal with exact loads and makespan 9/8; formula candidates include minimum B=3'})

manifest={
 'batch':'dual-rail-input-certificates-20261031',
 'source_commits':['68fad804ec5946cb296f77dc5b336308a66abf12','aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c'],
 'source_ids':{'distorted_group_joint_slot_cases':'b083c8d4196a16c48a20','dual_rail_exception_arity_sharp_certificates':'0d323a2d8638ce87fc76','dual_rail_fullcube_A3_actual_certificate':'c364b9a5b3af1dd211c5'},
 'source_sha256':{p.name:sha(p) for p in ROOT.glob('*.json') if p.name!='validation.json'},
 'checks':checks,
 'scope':'exact source-input preservation and independent Fraction consistency checks; no general UM theorem inferred'
}
(ROOT/'validation.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(manifest,ensure_ascii=False,indent=2))
