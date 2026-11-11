"""Main 25-IC, half-priced middle capacities, true terminal BR; zero LP calls."""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
from hashlib import sha256
import json

HERE=Path(__file__).resolve().parent
WS=HERE.parent


def share(n,d):return F(n,d) if d else F(0)


def main():
    states=[];mins=[];menus=[]
    for i in range(1,6):
        n=6-i;c=F(n+1,2)
        for p in range(i):
            D=p+n+1
            for t,q in product((0,1),repeat=2):
                minimum=c*t+F(24*t,D)+F(q,p+1+n*t)
                vals=[]
                for tails in product((0,1),repeat=n):
                    s,z=sum(tails[:-1]),tails[-1]
                    value=share(25*t-z,p+t+s+z)+F(s,2)+z+F(q,p+t+s+1)
                    assert value>=minimum;vals.append(value)
                    states.append({'i':i,'p':p,'t':t,'q':q,'tails':list(tails),'cost':str(value),'residual':str(value-minimum)})
                assert min(vals)==minimum
                mins.append({'i':i,'p':p,'t':t,'q':q,'minimum':str(minimum)})
            for menu in product((0,1),repeat=6):
                d,o=sum(menu),int(any(menu))
                for q in (0,1):
                    literal=sum((c*t+F(24*t,D)+F(q,p+1+n*t) for t in menu),F(0))/6
                    guarantee=F(q,p+1)+F(o,6)*(c+F(24,D)-F(n*q,(p+1)*D))
                    assert literal>=guarantee
                for t in (0,1):
                    literal=sum((c*t+F(24*t,D)+F(q,p+1+n*t) for q in menu),F(0))/6
                    guarantee=c*t+F(24*t,D)+F(o,6*(p+1+n*t))
                    assert literal>=guarantee
                literal=sum((c*menu[k]+F(24*menu[k],D)+F(menu[l],p+1+n*menu[k])
                             for k in range(6) for l in range(6) if k!=l),F(0))/30
                formula=F(d,6)*(c+F(24,D)+F(1,p+1))-F(n*d*(d-1),30*(p+1)*D)
                guarantee=o*(c/6+F(4,D)+F(1,6*(p+1)))
                assert literal==formula>=guarantee
                menus.append({'i':i,'p':p,'menu':list(menu),'literal_mean30':str(literal),'residual':str(literal-guarantee)})
    ip=WS/'universal_union_wallet_v5/exact_input.json';cp=WS/'universal_union_wallet_v5/exact_certificate.json'
    assert sha256(ip.read_bytes()).hexdigest()=='3b2065e702c5590d50ebc8acd5ea30337e82db2a84585f87040acd36e91db553'
    assert sha256(cp.read_bytes()).hexdigest()=='5e5a2377ed780f4a9c9f58ca8703fc5a473d41ea1945a654aa0ee6c0efa0deda'
    inp,cert=json.loads(ip.read_text()),json.loads(cp.read_text())
    old=json.loads((WS/'main_all_source31_family/exact_family.json').read_text())
    oldrows={r['name']:r for r in old['rows']};rows=[];checks=0
    for i in range(1,6):
        n=6-i;c=F(n+1,2)
        for T in range(8):
            for Q in range(8):
                a={};prior=oldrows[f'PORTFOLIO31_i{i}_T{T+1}_Q{Q+1}']
                for atom in inp['atom_columns']:
                    bits,x,o=atom['a'],atom['x'],atom['o'];legal=bits+[x]
                    p=sum(bits[:i-1]);D=p+n+1;u=share(bits[i-1],sum(bits))
                    tv=F(legal[T]) if T<7 else F(o,6)
                    if T<7:
                        q=F(legal[Q]) if Q<7 else F(o,6)
                        cost=c*tv+F(24*tv,D)+F(q,p+1+n*tv)
                    elif Q<7:
                        q=legal[Q]
                        cost=F(q,p+1)+F(o,6)*(c+F(24,D)-F(n*q,(p+1)*D))
                    else:cost=o*(c/6+F(4,D)+F(1,6*(p+1)))
                    j=str(atom['index']);a[j]=str(25*u-cost)
                    safe=u-F(tv,D);cap=-tv
                    assert F(prior['a'][j])-F(a[j])==6*safe+F(n-1,2)*cap
                    checks+=1
                a['256']=str(c)
                assert F(prior['a']['256'])-c==F(n-1,2);checks+=1
                rows.append({'name':f'PORTFOLIO25_i{i}_T{T+1}_Q{Q+1}','family':'ALL_SOURCE_PORTFOLIO25',
                             'source':i,'T':T+1,'Q':Q+1,'a':a,'rhs':'0','numerical_divisor':'25'})
    assert checks==82240
    point=cert['primal'];values=[]
    for row in rows:
        value=sum((F(v)*F(point.get(j,0)) for j,v in row['a'].items()),F(0))
        values.append({'name':row['name'],'value':str(value),'decimal':float(value)})
    values.sort(key=lambda r:F(r['value']))
    out={'status':'PASS_MAIN_LITERAL_25_FAMILY_AND_EXACT31_DOMINANCE','optimizer_calls':0,
         'source_certificate_sha256':sha256(cp.read_bytes()).hexdigest(),'states':len(states),'minima':mins,
         'menu_states':len(menus),'rows':rows,'dominance_columns_checked':checks,
         'dominance':'R31=R25+6 SAFE_i(T)+(n-1)/2 CAP(T); menu T uses theta=o/6 and CAP=K-O/6.',
         'v5_evaluations':values,'negative_v5_rows':sum(F(r['value'])<0 for r in values),
         'not_claimed':['unique hidden minimizer','SPE realization','half coverage','next cone optimum']}
    for name,data in [('exact_family.json',out),('literal_states.json',states),('menu_checks.json',menus)]:
        (HERE/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'status':out['status'],'states':len(states),'rows':len(rows),
                     'negative_v5_rows':out['negative_v5_rows'],'worst':values[:6],
                     'family_sha256':sha256((HERE/'exact_family.json').read_bytes()).hexdigest()},ensure_ascii=False,indent=2))


if __name__=='__main__':main()
