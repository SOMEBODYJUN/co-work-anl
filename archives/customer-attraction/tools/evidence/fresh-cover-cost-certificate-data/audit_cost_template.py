"""Exact independent unit-share reconstruction and 8-support Farkas witness.

No original helper/import/main, LP, or complete-strategy search is called.
The 52-customer complete-SPE example is an already certified input; here only
its current six-label projection and 24 global slacks are recomputed.
"""
from argparse import ArgumentParser
from collections import defaultdict
from fractions import Fraction as F
from hashlib import sha256
from itertools import product
import json
from pathlib import Path

LABELS='ABTSQR'
LAST=[('B','A'),('Q','T'),('R','S')]
NAMES=['root_T_Q','root_S_R']+['floor_'+x for x in LABELS]+['old_cover']+['last_'+c+'_'+p+'_'+x for c,p in LAST for x in LABELS if x!=c]


def shares(bits,p,occupied,tau):
    D=(p+1)*(p+2)
    pay=lambda x,y:F(bits[x],p+1+bits[y])
    ua=pay('A','B')
    values=[ua-pay('T','Q'),ua-pay('S','R')]
    values += [ua-F(bits[x],p+2) for x in LABELS]
    values += [tau*ua-(F(1,p+2) if occupied else F())]
    values += [pay(c,prior)-pay(x,prior) for c,prior in LAST for x in LABELS if x!=c]
    a,b,t,s=(bits[x] for x in 'ABTS')
    target=pay('A','B')+pay('B','A') if occupied else F(2*int(a or b)-int(t or s))
    return [D*x for x in values],D*target


def literal_source_formula(bits,p,occupied,tau):
    # Direct transcription of the read source, compared against unit fractions.
    u=lambda a,b:bits[a]*(p+2-bits[b])
    a,b,t,s=(bits[x] for x in 'ABTS')
    row=[u('A','B')-u('T','Q'),u('A','B')-u('S','R')]
    row += [u('A','B')-bits[x]*(p+1) for x in LABELS]
    row += [tau*u('A','B')-(p+1 if occupied else 0)]
    row += [u(c,prior)-u(x,prior) for c,prior in LAST for x in LABELS if x!=c]
    rhs=(p+2)*(a+b)-2*a*b if occupied else 2*(2*(a+b-a*b)-(t+s-t*s))
    return list(map(F,row)),F(rhs)


def matrix(tau):
    records=[]
    for v in product((0,1),repeat=6):
        bits=dict(zip(LABELS,v));old=None
        for occupied,p,kind in [(False,0,'fresh'),(True,1,'old-p1'),(True,2,'old-slope')]:
            row,rhs=shares(bits,p,occupied,tau)
            lr,lb=literal_source_formula(bits,p,occupied,tau)
            assert row==lr and rhs==lb
            if kind=='old-slope':
                row=[x-y for x,y in zip(row,old[0])];rhs-=old[1]
            if kind=='old-p1':old=(row,rhs)
            assert all(x.denominator==1 for x in row+[rhs])
            records.append({'index':len(records),'bits':''.join(map(str,v)),'kind':kind,'coefficients':row,'target':rhs})
    assert len(records)==192 and len(NAMES)==24
    return records


def main():
    p=ArgumentParser();p.add_argument('--primary',type=Path,required=True);p.add_argument('--output-dir',type=Path,required=True);a=p.parse_args();a.output_dir.mkdir(exist_ok=True,parents=True)
    raw=a.primary.read_bytes();saved=json.loads(raw)
    assert len(raw)==148 and sha256(raw).hexdigest()=='390eed8d1f1755881dc5afff4d20e3c275ec9313950897450a44c72e5766755b'
    assert saved=={'tau':'2','success':False,'message':'The problem is infeasible. (HiGHS Status 8: model_status is Infeasible; primal_status is None)'}
    rows=matrix(F(2));rows1=matrix(F(1))
    # Original old labels are A,B,T,Q,R,S. Last replies after T and Q are S.
    source_types=[('A',10),('B',12),('T',5),('Q',5),('TR',2),('QR',2),('TS',2),('QS',2),('ARS',6),('BRS',6)]
    label_map={'A':'A','B':'B','T':'T','S':'Q','Q':'S','R':'S'}
    masses=defaultdict(int)
    for interests,n in source_types:
        occupied=bool(set(interests)&set('AB'))
        bits=''.join(str(int(label_map[x] in interests)) for x in LABELS)
        masses[bits,'old-p1' if occupied else 'fresh']+=n
    assert sum(masses.values())==52 and len(masses)==8
    y=[F()]*192;witness=[]
    for (bits,kind),n in sorted(masses.items()):
        idx=next(r['index'] for r in rows if r['bits']==bits and r['kind']==kind)
        load=1 if kind=='old-p1' else 0;D=(load+1)*(load+2)
        y[idx]=F(6*n,D);assert y[idx].denominator==1
        witness.append({'row':idx,'bits':bits,'kind':kind,'customers':n,'background_load':load,'D':D,'nonnegative_integer_weight':str(y[idx])})
    lhs=[sum(y[i]*r['coefficients'][j] for i,r in enumerate(rows)) for j in range(24)]
    rhs=sum(y[i]*r['target'] for i,r in enumerate(rows))
    assert min(lhs)>=0 and rhs==-6 and lhs[NAMES.index('old_cover')]==28
    ua=F();ub=F();cost=F();fresh_actual=0;fresh_compare=0
    for (vs,kind),n in masses.items():
        bits=dict(zip(LABELS,map(int,vs)));load=int(kind=='old-p1')
        ua+=n*F(bits['A'],load+1+bits['B']);ub+=n*F(bits['B'],load+1+bits['A'])
        if load:cost+=F(n,load+2)
        else:
            fresh_actual+=n*int(bits['A'] or bits['B']);fresh_compare+=n*int(bits['T'] or bits['S'])
    assert (ua,ub,cost,fresh_actual,fresh_compare)==(8,9,F(34,3),0,18)
    assert rhs==6*(ua+ub+fresh_actual-fresh_compare)
    # Same witness has old-cover pairing 48*tau-68. No other column changes.
    assert all(sum(y[i]*r['coefficients'][j] for i,r in enumerate(rows1))==v for j,v in enumerate(lhs) if NAMES[j]!='old_cover')
    assert sum(y[i]*r['coefficients'][8] for i,r in enumerate(rows1))==-20
    lam=[F()]*24
    for name,v in [('floor_B',F(1,2)),('old_cover',F(1)),('last_B_A_T',F(1)),('last_B_A_S',F(1))]:lam[NAMES.index(name)]=v
    residuals=[]
    for rec in rows1:
        bits=dict(zip(LABELS,map(int,rec['bits'])));aa,bb,t,ss=(bits[x] for x in 'ABTS')
        if rec['kind']=='fresh':symbolic=aa*((1-t)*(1-ss)+t*ss)+(1-aa)*(F(bb,2)+2*t*ss)
        elif rec['kind']=='old-p1':symbolic=(1-bb)*(2-F(3*aa,2))+(t+ss)*(3-aa)
        else:symbolic=1-F(aa+bb,2)+t+ss
        rest=rec['target']-sum(x*z for x,z in zip(rec['coefficients'],lam))
        assert rest==symbolic>=0;residuals.append({'row':rec['index'],'value':str(rest)})
    summary={'status':'PASS_EXACT_UNIT_SHARE_AND_FARKAS_AUDIT','primary_sha256':sha256(raw).hexdigest(),'all_primary_fields':saved,'labels':LABELS,'names':NAMES,'rows':192,'columns':24,'exact_coefficient_comparisons':192*24,'target_comparisons':192,'case_kinds':{'fresh':64,'old-p1':64,'old-slope':64},'original10_types':[{'interest_labels':k,'customers':n} for k,n in source_types],'label_map_to_existing52_example':label_map,'merged_types':8,'integer_farkas_support':witness,'pairing_24_columns':[{'name':name,'value':str(v),'global_slack':str(v/6)} for name,v in zip(NAMES,lhs)],'paired_target':str(rhs),'game_quantities':{'u_A':str(ua),'u_B':str(ub),'P':str(ua+ub),'Delta':fresh_actual,'comparison_fresh_union':fresh_compare,'C_old':str(cost),'tau2_old_budget_slack':str(2*ua-cost),'target':str(ua+ub+fresh_actual-fresh_compare)},'same_witness_tau_range':{'old_cover_pairing':'48*tau-68','valid_for':'tau >= 17/12','sharp_threshold_claimed':False},'tau1_certificate':{'nonzero_multipliers':{n:str(v) for n,v in zip(NAMES,lam) if v},'minimum_residual':str(min(F(x['value']) for x in residuals)),'zero_residuals':sum(F(x['value'])==0 for x in residuals),'positive_residuals':sum(F(x['value'])>0 for x in residuals),'complete_residuals':residuals,'source':'algebraic transfer from existing legal-H menu certificate; no tau1 LP run'},'full52_SPE_verification_repeated':False,'original_module_or_helper_calls':0,'LP_calls':0,'scope':'Exact impossibility of this tau2 nonnegative certificate template, with existing complete-SPE counterexample satisfying the extra budget; no half counterexample or exact best tau threshold.'}
    ledger=[{**rec,'coefficients':list(map(str,rec['coefficients'])),'target':str(rec['target'])} for rec in rows]
    (a.output_dir/'exact-audit.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
    (a.output_dir/'coefficient-rows.json').write_text(json.dumps({'tau':'2','names':NAMES,'records':ledger},ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:summary[k] for k in ['status','integer_farkas_support','pairing_24_columns','paired_target','game_quantities','same_witness_tau_range']},ensure_ascii=False,indent=2))


if __name__=='__main__':main()
