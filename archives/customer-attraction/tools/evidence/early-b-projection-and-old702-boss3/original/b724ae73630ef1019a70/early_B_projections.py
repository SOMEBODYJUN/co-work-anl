"""Three exact projected actual-source->actual-last-B necessary rows.

Standard library only. Every follower is taken from the same original SPE.
CAP_H=K-|H| supplies a common scalar K; the table stores only customer terms.
The global necessary row is sum_x psi(actual_bits,d)+kappa*K >= 0.
"""
from fractions import Fraction as F
from itertools import product
from collections import defaultdict
from pathlib import Path
import hashlib,json

ROOT=Path(__file__).resolve().parents[5]
POINT_REL='research/workspaces/customer-attraction/R-5662d5cb0e5845a980ed10a3b3224cb1/research_5/combined_branch_master_exact.json'
SPECS=[
 {'source':2,'weights':{'F':771984,'G':6492,'L1':20517,'L2':36285,'CAP3':44168,'CAP4':44610,'H':5256,'E':7186}},
 {'source':3,'weights':{'F':11958,'G':172,'CAP1':180,'CAP2':1169,'CAP3':1214,'E':188}},
 {'source':4,'weights':{'F':89632,'G':2576,'L1':11205,'L2':11557,'CAP1':6311,'CAP2':6899,'E':2832}},
]
def share(bit,den):return F(bit,den) if bit else F(0)
def raw(actual,d,hidden,ell,source):
    i=source-1;b=actual[5];seq=actual[:i]+(b,)+hidden;den=sum(seq)
    p=sum(seq[:-2]);r,s=seq[-2:];c=sum(actual);u=[share(t,c) for t in actual]
    values={'F':u[i]-share(b,den),
       'G':6*share(r,den)+share(s,2*den)-F(d,p+1)-F(ell,12*(p+r+1))+F(d*ell,6*(p+1)*(p+2)),
       'E':6*share(s,den)-F(d,p+r+1)}
    for j,t in enumerate(hidden,1):
        values[f'CAP{j}']=-F(t)
        values[f'L{j}']=u[5]-F(t,1+sum(actual[:5]))
    if source==2:
        # Parent path: A1,B,Q1,Q2,Q3,Q4. True position4 Q2 -> Q4 floor.
        values['H']=share(hidden[1],den)-F(hidden[3],3+actual[0]+b+hidden[0])
    return values
def value(actual,d,hidden,ell,spec):
    rr=raw(actual,d,hidden,ell,spec['source'])
    return sum(w*rr[name] for name,w in spec['weights'].items())
def make_table(spec):
    nh=6-spec['source'];table={}
    for bits in product(range(2),repeat=6):
        for d in range(7):
            endpoint=max(value(bits,d,h,ell,spec) for h in product(range(2),repeat=nh) for ell in (0,6))
            full=max(value(bits,d,h,ell,spec) for h in product(range(2),repeat=nh) for ell in range(7))
            assert endpoint==full
            table[''.join(map(str,bits)),d]=full
    return table
def verify(export=False):
    path=ROOT/POINT_REL;j=json.loads(path.read_text());mass=defaultdict(F);K=F(0)
    for col in j['columns']:
        if col['kind']=='hist':mass[col['actual_bits'],col['d']]+=F(col['weight'])
        if col['kind']=='K':K+=F(col['weight'])
    rows=[]
    for spec in SPECS:
        table=make_table(spec);kappa=sum(w for name,w in spec['weights'].items() if name.startswith('CAP'))
        point_value=sum(table[t]*weight for t,weight in mass.items())+kappa*K
        assert point_value<0
        rows.append({**spec,'kappa':kappa,'coefficient_domain':{'actual_bit_patterns':64,'d_values':7,'hidden_bit_patterns':2**(6-spec['source']),'ell_values':7,'full_ell_matches_endpoints':True},'point_value':str(point_value),'point_value_decimal':float(point_value),'table':[{'actual_bits':bits,'d':d,'psi':str(v)} for (bits,d),v in table.items()]})
    out={'status':'EXACT_VALID_NECESSARY_PROJECTIONS_SEPARATING_SELECTED_5108_POINT_ONLY','point_path':POINT_REL,'point_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'rows':rows}
    if export:
        target=Path(__file__).with_name('early_B_projection_certificate.json')
        if target.exists():raise FileExistsError(target)
        target.write_text(json.dumps(out,indent=2)+'\n')
    return {**{k:v for k,v in out.items() if k!='rows'},'rows':[{k:v for k,v in row.items() if k!='table'} for row in rows]}
if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--export',action='store_true');a=p.parse_args()
    print(json.dumps(verify(a.export),indent=2))
