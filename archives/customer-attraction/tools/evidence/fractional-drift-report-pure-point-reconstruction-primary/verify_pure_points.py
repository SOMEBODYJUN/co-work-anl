"""Current exact finite reconstruction; no original script imports or numerical solver."""
from pathlib import Path
from fractions import Fraction
import hashlib,json
ROOT=Path(__file__).resolve().parent
EXPECTED={'fractional_drift_n3k5.json':'7a3b805fb10627452b0dbd3080b90ec9db4e61bb04e8911ef53e7d5c72c173fb','fractional_drift_n4k6.json':'a954564facfdfc00ff417a1c4921ee5be29aa601ee935815f7aeec2a5d763ea9'}
rows=[]
for name,sha in EXPECTED.items():
    paths=list((ROOT/'source-root').rglob(name));assert len(paths)==1
    data=paths[0].read_bytes();assert hashlib.sha256(data).hexdigest()==sha
    x=json.loads(data);assert len(x['bank'])==20 and all(z==x['bank'][0] for z in x['bank']) and x['best'] not in x['bank']
    for label,z in [('best',x['best']),('bank[0..19]',x['bank'][0])]:
        n,k,w,a=z['n'],z['k'],z['weights'],z['action']
        assert n>=2 and len(w)==2**k-1 and all(type(v) is int and v>=0 for v in w) and w[-1]==0
        assert len(z['terminal'])==k and z['terminal']==[n if j==a else 0 for j in range(k)]
        cols=[tuple(bool(mask>>j&1) for mask,v in enumerate(w,1) if v) for j in range(k)]
        assert len(set(cols))==k
        sizes=[sum(v for mask,v in enumerate(w,1) if mask>>j&1) for j in range(k)]
        inter=[sum(v for mask,v in enumerate(w,1) if mask>>j&1 and mask>>a&1) for j in range(k)]
        pure=[Fraction(inter[j],n)+sizes[j]-inter[j] for j in range(k)]
        bound=Fraction(sizes[a],n);assert max(pure)==bound
        utility=sum((Fraction(v,sum(z['terminal'][j] for j in range(k) if mask>>j&1)) for mask,v in enumerate(w,1) if mask>>a&1),Fraction())
        assert utility==bound
        debt=utility+(n-1)*bound-n*bound;assert debt==0
        rows.append({'file':name,'record':label,'root_and_child_value':str(bound),'utility':str(utility),'debt':str(debt),'all_pure_query_values':[str(t) for t in pure]})
print(json.dumps({'status':'PASS_FINITE_EXACT_RECONSTRUCTION_ONLY','distinct_models':4,'all_original_program_entries':0,'SPE_check_claimed':False,'rows':rows},ensure_ascii=False,indent=2))
