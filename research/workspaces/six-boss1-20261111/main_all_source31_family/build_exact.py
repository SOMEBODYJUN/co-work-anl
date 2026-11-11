"""All five real sources, seven visible legal queries and six-menu means.

The 31-fold same-branch argument is an instance of the registered portfolio
theorem. This builds all 320 full-domain rows without running an optimizer.
"""
from pathlib import Path
from itertools import product
from fractions import Fraction as F
from hashlib import sha256
import json

HERE=Path(__file__).resolve().parent
WS=HERE.parent


def share(n,d):return F(n,d) if d else F(0)


def main():
    minima=[]; states=[]
    for i in range(1,6):
        n=6-i
        for p in range(i):
            for t,q in product((0,1),repeat=2):
                m=n*t+F(30*t,p+n+1)+F(q,p+1+n*t)
                values=[]
                for tails in product((0,1),repeat=n):
                    z=tails[-1]; s=sum(tails[:-1])
                    val=share(31*t-z,p+t+s+z)+s+z+F(q,p+t+s+1)
                    assert val>=m
                    values.append(val)
                    states.append({'i':i,'p':p,'t':t,'q':q,'tails':list(tails),'cost':str(val),'residual':str(val-m)})
                assert min(values)==m
                minima.append({'i':i,'p':p,'t':t,'q':q,'minimum':str(m)})

    # All64 menu membership strings, every source and compatible prefix count.
    averaged=[]
    for i in range(1,6):
        n=6-i
        for p in range(i):
            for menu in product((0,1),repeat=6):
                d,o=sum(menu),int(any(menu))
                for q in (0,1):
                    literal=sum((n*t+F(30*t,p+n+1)+F(q,p+1+n*t) for t in menu),F(0))/6
                    guaranteed=F(q,p+1)+F(o,6)*(n+F(30,p+n+1)-F(n*q,(p+1)*(p+n+1)))
                    assert literal>=guaranteed
                literal=sum((n*menu[k]+F(30*menu[k],p+n+1)+F(menu[l],p+1+n*menu[k])
                             for k in range(6) for l in range(6) if k!=l),F(0))/30
                formula=F(d,6)*(n+F(30,p+n+1)+F(1,p+1))-F(n*d*(d-1),30*(p+1)*(p+n+1))
                guaranteed=o*(F(n,6)+F(5,p+n+1)+F(1,6*(p+1)))
                assert literal==formula>=guaranteed
                averaged.append({'i':i,'p':p,'menu':list(menu),'mean_mean30_residual':str(formula-guaranteed)})

    inp=WS/'universal_union_wallet_v4/exact_input.json'
    assert sha256(inp.read_bytes()).hexdigest()=='b520abb0565c6df7ae4192971bf90d712ddf92a4304f3ce51710cd9b2617b8f5'
    g=json.loads(inp.read_text()); rows=[]
    for i in range(1,6):
        n=6-i
        for T in range(8):
            for Q in range(8):
                coeff={}
                for atom in g['atom_columns']:
                    a,x,o=atom['a'],atom['x'],atom['o']; legal=a+[x]
                    p=sum(a[:i-1]); u=share(a[i-1],sum(a))
                    if T<7:
                        t=legal[T]; q=F(legal[Q]) if Q<7 else F(o,6)
                        cost=n*t+F(30*t,p+n+1)+F(q,p+1+n*t)
                    elif Q<7:
                        q=legal[Q]
                        cost=F(q,p+1)+F(o,6)*(n+F(30,p+n+1)-F(n*q,(p+1)*(p+n+1)))
                    else:
                        cost=o*(F(n,6)+F(5,p+n+1)+F(1,6*(p+1)))
                    coeff[str(atom['index'])]=str(31*u-cost)
                coeff['256']=str(n)
                rows.append({'name':f'PORTFOLIO31_i{i}_T{T+1}_Q{Q+1}','family':'ALL_SOURCE_PORTFOLIO31',
                             'source':i,'T':T+1,'Q':Q+1,'a':coeff,'rhs':'0','numerical_divisor':'31',
                             'menu_mean_mean_rule':'30 ordered distinct indices' if T==Q==7 else None})
    assert len(rows)==320 and all(len(r['a'])==257 for r in rows)
    known=json.loads((WS/'main_thirty_index_strengthening/SOURCE2_MAXSIZE_31.json').read_text())
    same=next(r for r in rows if r['source']==2 and r['T']==6 and r['Q']==7)
    assert same['a']==known['a']
    cp=WS/'universal_union_wallet_v4/exact_certificate.json'
    assert sha256(cp.read_bytes()).hexdigest()=='290f90feba9bf7ec8232e16e59f02b7f4e05dc41413f14510592c3d16ef28819'
    point=json.loads(cp.read_text())['primal']; evaluations=[]
    for r in rows:
        value=sum((F(v)*F(point.get(j,0)) for j,v in r['a'].items()),F(0))
        evaluations.append({'name':r['name'],'value':str(value),'decimal':float(value)})
    evaluations.sort(key=lambda r:F(r['value']))
    result={'status':'PASS_LITERAL_FIVE_SOURCES_AND_MENU_AVERAGES','optimizer_calls':0,
            'scope':'Actual source i=1..5, arbitrary legal T,Q; seven visible legal labels A1..A6,X and six legal comparison menu averages.',
            'state_count':len(states),'minimum_count':len(minima),'menu_count':len(averaged),'rows':rows,
            'v4_certificate_sha256':sha256(cp.read_bytes()).hexdigest(),'v4_evaluations':evaluations,
            'negative_v4_rows':sum(F(r['value'])<0 for r in evaluations),'all_minima':minima}
    for name,data in [('exact_family.json',result),('literal_states.json',states),('menu_checks.json',averaged)]:
        (HERE/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'status':result['status'],'states':len(states),'rows':len(rows),
                      'negative_v4_rows':result['negative_v4_rows'],'worst_v4':evaluations[:8],
                      'family_sha256':sha256((HERE/'exact_family.json').read_bytes()).hexdigest()},ensure_ascii=False,indent=2))


if __name__=='__main__':main()
