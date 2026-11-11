"""Main independent four-state projection replay for the six genuine budgets."""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
from hashlib import sha256
import json

HERE=Path(__file__).resolve().parent
def main():
    base=HERE/'universal_true_x_tail';cp=base/'exact_certificate.json'
    assert sha256(cp.read_bytes()).hexdigest()=='467d2b0f7415c8b51cce1aebe0a5784ece6da31822ce6630b767ab001883837e'
    ip=base/'exact_input.json.gz'
    assert sha256(ip.read_bytes()).hexdigest()=='367ab0932172ce10e459bdf390121d0a5ad825a1475b30e5bb5ae6105b797375'
    cert=json.loads(cp.read_text());cut=cert['universal_cut']
    orig=HERE/'universal_union_wallet_lp'
    inp=json.loads((orig/'exact_input.json').read_text())
    primal=json.loads((orig/'exact_certificate.json').read_text())
    point={int(k):F(v) for k,v in primal['primal'].items()}
    vals=[];positive=0;zero=0
    for atom in inp['atom_columns']:
        a=atom['a'];x=atom['x'];o=atom['o'];j=atom['index']
        b=sum(a[:3]);D=b+a[3]+1;d=b+x+1;q=F(o,6)
        psi=[]
        for y,t in product((0,1),repeat=2):
            branch_wallet=F(y,d+t)+F(t,d+y)+F(y,d*(d+1))
            p=4096*F(x,b+1+y+t)+800*F(y,D)+71*t+384*(q-t)/F(d+y)
            p+=512*((a[5]+q)/F(d)-a[5]*q/F(d*(d+1))-branch_wallet)
            p+=900*((t+q)/F(D)-t*q/F(D*(D+1)))
            psi.append(p)
        m=min(psi)
        res=[p-m for p in psi]
        assert min(res)>=0
        positive+=sum(r>0 for r in res);zero+=sum(r==0 for r in res)
        c=sum(a)
        u4=F(a[3],c) if c else F(0)
        u5=F(a[4],c) if c else F(0)
        coef=4096*u4+900*u5+1700*F(x,D)-m
        assert coef==F(cut['cut_z'].get(str(j),'0'))
        vals.append({'index':j,'minimum':str(m),'coefficient':str(coef),'four_values':[str(p) for p in psi]})
    assert F(cut['cut_K'])==71
    value=sum((F(v['coefficient'])*point.get(v['index'],F(0)) for v in vals),F(0))+71*point[256]
    assert value==F(cert['fixed_projection_cut_value'])==F(-128742478797765148513379,2572043380472564711298)
    out={'status':'PASS','scope':'Main literal six-budget four-state universal projection replay',
         'input_sha256':sha256(ip.read_bytes()).hexdigest(),'certificate_sha256':sha256(cp.read_bytes()).hexdigest(),
         'universal_types':256,'four_state_count':1024,'positive_residuals':positive,'zero_residuals':zero,
         'cut_K':'71','fixed_point_value':str(value),'released_to_universal_wallet_v2':True,'types':vals}
    print(json.dumps(out,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
