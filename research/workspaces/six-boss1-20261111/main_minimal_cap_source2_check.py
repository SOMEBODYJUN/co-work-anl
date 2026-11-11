"""Main independently derives minimal-cap full tau domain and complete C-only rows."""
from pathlib import Path
from fractions import Fraction as F
from itertools import combinations,product
from hashlib import sha256
import json

W=Path(__file__).resolve().parent;P=W/'source2_minimal_cap_safe'
theta=(F(0),F(0),F(0))
def solve(rows):
    m=[[F(v) for v in a]+[-F(b)] for b,a in rows]
    for k in range(4):
        pivot=next((r for r in range(k,4) if m[r][k]),None)
        if pivot is None:return None
        m[k],m[pivot]=m[pivot],m[k];div=m[k][k];m[k]=[v/div for v in m[k]]
        for r in range(4):
            if r!=k and m[r][k]:
                c=m[r][k];m[r]=[a-c*b for a,b in zip(m[r],m[k])]
    return tuple(r[-1] for r in m)
def load(p):return json.loads(p.read_text())
def main():
    out=W/'main_minimal_cap_source2_check.json';assert not out.exists()
    planes=[]
    for k in range(4):
        a=[F(0)]*4;a[k]=F(1);planes.append((F(0),tuple(a)))
    planes.append((F(9),(F(0),F(0),F(0),F(-1))))
    for k,j in enumerate(range(3,6)):
        for own,b,scoef in [(F(4,5),F(43,60),F(0)),(F(3,4),F(67,60),F(-1,20))]:
            a=[F(0)]*4;a[k]=-own;a[3]=scoef
            for h in range(j+1,6):a[h-3]=-F(1,6*(7-h)*(8-h))
            planes.append((b,tuple(a)))
    vv=set()
    for rows in combinations(planes,4):
        q=solve(rows)
        if q is not None and all(b+sum(a*t for a,t in zip(v,q))>=0 for b,v in planes):vv.add(q)
    param=load(P/'parameter_polytope.json')
    by={r['id']:tuple(map(F,r['tau3_tau4_tau5']))+(F(r['s']),) for r in param['vertices']}
    assert vv==set(by.values()) and len(vv)==28
    checks=0;minimum=0;cols=0;face_values=[]
    atoms=list(product((0,1),repeat=9))
    face=load(W/'visible_maximum_joint_v4_solve/optimal_face.json')
    coords={r['column']:[F(r['constant'])]+list(map(F,r['parameter_coefficients'])) for r in face['coordinates']}
    for row in load(P/'exact_family.json')['rows']:
        e=by[row['vertex_id']][:3];s=by[row['vertex_id']][3]
        tau=tuple(theta[k]+e[k] for k in range(3))
        gamma=tuple(e[k]+sum((e[h-3]/(6*(7-h)*(8-h)) for h in range(k+4,6)),F(0)) for k in range(3))
        beta=tuple(F(1,12)+v for v in gamma);a=25+sum(tau)-s;H=1+sum(beta)
        assert a==F(row['source_IC_weight']) and H==F(row['true_tail_K_weight'])
        for p,c,o in product((0,1),repeat=3):
            anchor=H*c+F(24*c,p+5)-s*c/5+F(o,6*(p+4*c+1))
            anchor+=sum(tau[j-3]*F(o,6*(p+(j-2)*c+7-j)) for j in range(3,6))
            values=[]
            for t in product((0,1),repeat=4):
                L=p+c+sum(t)
                v=(a*c-t[3]-sum(tau[k]*t[k] for k in range(3)))/L if L else F(0)
                v+=sum(beta[k]*t[k] for k in range(3))+t[3]+F(o,6*(p+c+sum(t[:3])+1))
                v+=sum(tau[j-3]*F(o,6*(p+c+sum(t[:j-3])+7-j)) for j in range(3,6))
                assert v>=anchor;checks+=1;values.append(v)
            assert min(values)==anchor;minimum+=1
        for h,bits in enumerate(atoms):
            actual=bits[:6];p,c,o=actual[0],bits[8],bits[7]
            u2=F(actual[1],sum(actual)) if sum(actual) else F(0)
            want=a*u2-F(24*c,p+5)-F(o,6*(p+4*c+1))
            want-=sum(tau[j-3]*F(o,6*(p+(j-2)*c+7-j)) for j in range(3,6))
            assert F(row['a'].get(str(h),'0'))==want;cols+=1
        assert F(row['a']['512'])==s/5;cols+=1
        values=[sum((F(row['a'].get(str(h),'0'))*v[k] for h,v in coords.items()),F(0)) for k in range(8)]
        assert all(v==0 for v in values[1:])
        face_values.append({'vertex_id':row['vertex_id'],'whole_face_value':str(values[0]),'strict_negative':values[0]<0})
    assert checks==3584 and minimum==224 and cols==14364
    r={'status':'PASS_MAIN_MINIMAL_CAP_SOURCE2_COMPLETE_DOMAIN28_TRUE_COSTS_AND_COLUMNS','optimizer_calls':0,
       'facet_count':11,'vertices':28,'boundary_intersections':330,'hidden_state_checks':checks,'conditional_minima':minimum,'full_row_coefficients':cols,
       'whole1586_face_values':face_values,'strictly_negative_whole_face_rows':sum(v['strict_negative'] for v in face_values),
       'proof_read_sha256':sha256((P/'proof.md').read_bytes()).hexdigest(),'family_sha256':sha256((P/'exact_family.json').read_bytes()).hexdigest(),
       'manifest_sha256':sha256((P/'freeze_manifest.json').read_bytes()).hexdigest(),
       'scope':'Arbitrary nonnegative tau, minimal beta>=1/12, complete11-facet/28-vertex domain. C-only free equality multiplier may be negative; all true budget weights remain nonnegative. Full1586 diagnostics only after whole certificate review; no optimizer.'}
    out.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:v for k,v in r.items() if k!='whole1586_face_values'},ensure_ascii=False))
if __name__=='__main__':main()
