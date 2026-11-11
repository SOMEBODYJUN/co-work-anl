"""Main's independent finite proof and full-column check; no optimization."""
from fractions import Fraction as F
from itertools import combinations, product
from pathlib import Path
import hashlib
import json

P=Path(__file__).resolve().parent
Q=P/'all_source_joint_reweighted_safe'
assert (Q/'freeze_manifest.json').exists(), 'Wait for final source freeze.'
source_names=['exact_family.json','parameter_polytopes.json','proof.md','freeze_manifest.json']
pins={name:hashlib.sha256((Q/name).read_bytes()).hexdigest() for name in source_names}
family=json.loads((Q/'exact_family.json').read_text())
polys=json.loads((Q/'parameter_polytopes.json').read_text())['sources']
assert family['raw_row_count']==536 and family['variables']==513

def solve(a,b):
    n=len(b)
    m=[[F(t) for t in row]+[F(rhs)] for row,rhs in zip(a,b)]
    for c in range(n):
        pivot=next((r for r in range(c,n) if m[r][c]),None)
        if pivot is None:return None
        m[c],m[pivot]=m[pivot],m[c]
        d=m[c][c];m[c]=[v/d for v in m[c]]
        for r in range(n):
            if r!=c and m[r][c]:
                t=m[r][c];m[r]=[x-t*y for x,y in zip(m[r],m[c])]
    return tuple(m[r][-1] for r in range(n))

def dot(a,b):return sum(x*y for x,y in zip(a,b))

results=[]
vertex_table={}
all_states=0
all_minima=0
for i in range(1,5):
    m=5-i
    dim=m+1
    planes=[]
    for k,j in enumerate(range(i+1,6)):
        v=[F(0)]*dim;v[k]=1;planes.append((F(0),tuple(v)))
        v=[F(0)]*dim;v[k]=-1
        for ell in range(j+1,6):v[ell-i-1]=-F(1,6*(7-ell)*(8-ell))
        planes.append((F(5,12),tuple(v)))
    v=[F(0)]*dim;v[-1]=1;planes.append((F(0),tuple(v)))
    if i==1:
        for k in range(m):
            v=[F(0)]*dim;v[k]=5;v[-1]=-1;planes.append((F(15),tuple(v)))
    else:
        v=[F(0)]*dim;v[-1]=-1;planes.append((F(9),tuple(v)))
    vertices=set()
    for selected in combinations(planes,dim):
        z=solve([b for c,b in selected],[-c for c,b in selected])
        if z is not None and all(c+dot(b,z)>=0 for c,b in planes):vertices.add(z)
    produced=next(d for d in polys if d['source']==i)
    expected={tuple(map(F,v['theta']))+(F(v['s']),) for v in produced['vertices']}
    assert vertices==expected
    assert len(vertices)==[39,16,8,4][i-1]
    state_count=0;min_count=0;zeros=0
    for v in produced['vertices']:
        theta=tuple(map(F,v['theta']));s=F(v['s']);a=25+sum(theta)-s
        assert a==F(v['a']) and a>0
        vertex_table[(i,v['id'])]=(theta,s,a)
        n=6-i;ci=F(n+1,2)
        for p in range(i):
            for t,o in product((0,1),repeat=2):
                wanted=ci*t+F(24*t,p+n+1)+F(o,6*(p+1+n*t))-s*F(t,min(p+n+1,5))
                wanted+=sum(theta[j-i-1]*F(o,6*(p+(j-i)*t+7-j)) for j in range(i+1,6))
                values=[]
                for tail in product((0,1),repeat=n):
                    load=p+t+sum(tail)
                    numerator=a*t-tail[-1]-sum(theta[k]*tail[k] for k in range(m))
                    value=numerator/load if load else F(0)
                    value+=F(sum(tail[:-1]),2)+tail[-1]+F(o,6*(p+t+sum(tail[:-1])+1))
                    value+=sum(theta[j-i-1]*F(o,6*(p+t+sum(tail[:j-i-1])+7-j)) for j in range(i+1,6))
                    assert value>=wanted,(i,v['id'],p,t,o,tail)
                    zeros+=value==wanted;values.append(value);state_count+=1
                assert min(values)==wanted
                min_count+=1
    all_states+=state_count;all_minima+=min_count
    results.append({'source':i,'facets_reconstructed':len(planes),'vertices':len(vertices),
                    'hidden_checks':state_count,'minima':min_count,'zero_states':zeros})
assert all_states==8064 and all_minima==444

atoms=list(product((0,1),repeat=9))
col_checks=0
for row in family['rows']:
    i,T=row['source'],row['T'];theta,s,a=vertex_table[(i,row['vertex_id'])]
    assert tuple(F(row['theta_by_true_source'][str(j)]) for j in range(i+1,6))==theta
    assert F(row['s'])==s and F(row['source_IC_weight'])==a
    assert F(row['numerical_divisor'])==25 and F(row['rhs'])==0
    assert row['uses_C_size_equality'] is False
    n=6-i;ci=F(n+1,2)
    for h,bits in enumerate(atoms):
        actual=bits[:6];p=sum(actual[:i-1]);o=bits[7]
        t=actual[int(T[1:])-1] if T.startswith('A') else bits[6 if T=='X' else 8]
        u=F(actual[i-1],sum(actual)) if sum(actual) else F(0)
        expected=a*u-ci*t-F(24*t,p+n+1)+s*F(t,min(p+n+1,5))-F(o,6*(p+1+n*t))
        expected-=sum(theta[j-i-1]*F(o,6*(p+(j-i)*t+7-j)) for j in range(i+1,6))
        assert F(row['a'].get(str(h),'0'))==expected,(row['name'],h)
        col_checks+=1
    assert F(row['a']['512'])==ci==F(row['K_weight']);col_checks+=1
assert col_checks==274968

old=json.loads((P/'source2_joint_internal_safe/sixteen_reweighted_vertex_family.json').read_text())
old_by_param={(tuple(map(F,r['theta3_theta4_theta5'])),F(r['s'])):r for r in old}
comparisons=0
for row in family['rows']:
    if row['source']!=2 or row['T']!='C':continue
    theta,s,a=vertex_table[(2,row['vertex_id'])]
    r=old_by_param[(theta,s)]
    for h in range(513):
        ec=atoms[h][8] if h<512 else -1
        expected=F(r['a'].get(str(h),'0'))+(s/5-F(5,2))*ec
        assert F(row['a'].get(str(h),'0'))==expected
        comparisons+=1
assert comparisons==8208
root=[(theta,s,a) for (i,ident),(theta,s,a) in vertex_table.items() if i==1]
assert max(v[1] for v in root)==F(1070,63)
assert min(v[2] for v in root)==F(605,63)
assert sum(v[1]==F(1070,63) for v in root)==1
assert sum(v[2]==F(605,63) for v in root)==1
assert pins=={name:hashlib.sha256((Q/name).read_bytes()).hexdigest() for name in source_names}
output={'owner':'Boss1/Main','status':'PASS','optimizer_calls':0,'proof_read_sha256':pins['proof.md'],
        'source_pins':pins,'source_domain_results':results,'total_hidden_checks':all_states,
        'total_minima':all_minima,'full536_column_checks':col_checks,'source2_C_comparison_columns':comparisons,
        'root_extremizer':{'theta_each':'25/63','s':'1070/63','a':'605/63','unique':True},
        'scope':'Direct true-budget proof read and independently reconstructed full domains, states and coefficients. No optimizer or SPE existence claim.'}
(P/'main_all_source_joint_check.json').write_text(json.dumps(output,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(output,ensure_ascii=False))
