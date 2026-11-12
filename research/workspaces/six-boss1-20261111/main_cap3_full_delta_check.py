"""Main independently checks all true affine states, full cells and weak corners."""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
from hashlib import sha256
import json

W=Path(__file__).resolve().parent
P=W/'source2_cap3_full_delta'
source=P/'exact_envelopes_2d.json'
assert sha256(source.read_bytes()).hexdigest()=='4d8fa86da04256ebd60855ae6fcd90baf76741f9c702de8d390cd5c11199e46f'
data=json.loads(source.read_text());b=F(5977,6912);v=F(43,48)
tails=list(product((0,1),repeat=4))
names=[''.join(map(str,r)) for r in tails]
def cost(p,t,q,r,s,q0,d,h):
    r3,r4,r5,z=r;x=b-d;y=v+d;n=p+t+sum(r)
    share=lambda m:F(m,n) if n else F(0)
    beta=[q0*(F(1,2)+x/12+y/6)-h,q0/2+x+q0*y/6,q0/2+y]
    return ((25+x+y-s)*share(t)+sum(B*m for B,m in zip(beta,r[:3]))+z
            -share(z)-x*share(r4)-y*share(r5)
            +q/F(p+t+r3+r4+r5+1)+x*q/F(p+t+r3+3)+y*q/F(p+t+r3+r4+2))
def minimum(p,t,q,s,q0,d,h):
    values=[cost(p,t,q,r,s,q0,d,h) for r in tails]
    m=min(values);return m,[names[i] for i,x in enumerate(values) if x==m]
counts=dict(state_affine_coefficients=0,exact_halfplanes=0,vertex_tail_values=0,
            complete_vertex_weak_sets=0,cell_corner_state_differences=0,
            full_h_difference_identities=0,ordered_multiplicity_comparisons=0)
isolated=[]
for sl in data['slices']:
    s,q0=F(sl['s']),F(sl['q0']);conditions=sl['conditions'];verts=sl['vertices']
    B=lambda d:q0*(F(1,2)+(b-d)/12+(v+d)/6)
    H=lambda d:q0*(F(1,3)+(b-d)/30+(v+d)/12)
    levels=lambda d:[F(0),H(d),B(d)] if q0==F(1,6) else [F(0),(10-b+d)/300,H(d),B(d)]
    points={a['id']:tuple(map(F,a['point'])) for a in verts}
    ds=sorted({pt[0] for pt in points.values()})
    assert ds[0]==0 and ds[-1]==b
    assert set(points.values())=={(d,h) for d in ds for h in levels(d)}
    expected_cells=set()
    for l,u in zip(ds,ds[1:]):
        low,up=levels(l),levels(u)
        for k in range(len(low)-1):expected_cells.add(tuple(sorted([(l,low[k]),(u,up[k]),(u,up[k+1]),(l,low[k+1])])))
    actual_cells={tuple(sorted(points[i] for i in cell['vertices'])) for cell in sl['cells']}
    assert actual_cells==expected_cells and len(actual_cells)==len(sl['cells'])
    coeffs={}
    for cond in conditions:
        p,t,q=cond['p'],cond['t'],F(cond['q']);rows=[]
        for r,state in zip(tails,cond['states']):
            base=cost(p,t,q,r,s,q0,F(0),F(0))
            coeff=(base,(cost(p,t,q,r,s,q0,b,F(0))-base)/b,-F(r[0]))
            assert tuple(map(F,state['affine']))==coeff
            rows.append(coeff);counts['state_affine_coefficients']+=3
            if state['weak_region_dimension']==0:
                assert state['tail']=='0100' and state['weak_region_vertices']==[[str(b),'0']]
                isolated.append((sl['id'],cond['key']))
        coeffs[cond['key']]=rows
        domain=[(0,-1,0),(-b,1,0),(0,0,-1),(-B(0),-(B(b)-B(0))/b,1)]
        for i,state in enumerate(cond['states']):
            required=domain+[tuple(a-z for a,z in zip(rows[i],other)) for j,other in enumerate(rows) if i!=j]
            assert [tuple(map(F,c)) for c in state['constraints']]==required
            counts['exact_halfplanes']+=len(required)
    for vertex in verts:
        d,h=map(F,vertex['point']);vals={}
        for cond in conditions:
            p,t,q=cond['p'],cond['t'],F(cond['q']);m,weak=minimum(p,t,q,s,q0,d,h)
            got=vertex['conditions'][cond['key']]
            assert F(got['value'])==m and got['tails']==weak
            counts['vertex_tail_values']+=16;counts['complete_vertex_weak_sets']+=1
            mbase=minimum(p,t,q,s,q0,d,F(0))[0]
            diff=(h if t else F(0) if q==0 else h if p==0 or q>=F(3,5)
                  else max(F(0),h-H(d)) if q==q0 else max(F(0),h-(10-b+d)/300))
            assert mbase-m==diff
            counts['full_h_difference_identities']+=1
            vals[p,t,q]=m
        if sl['mode']=='ordered':
            for p in (0,1):
                fs=[F(0)]+[((6-k)*vals[p,0,F(k,5)] if k<6 else 0)/6+k*vals[p,1,F(k-1,5)]/6 for k in range(1,7)]
                for k in range(1,6):assert fs[k+1]-fs[k]>=F(8567,82944);counts['ordered_multiplicity_comparisons']+=1
    for cell in sl['cells']:
        for cond in conditions:
            chosen=tuple(map(F,cell['conditions'][cond['key']]['affine']))
            assert chosen in coeffs[cond['key']]
            for i in cell['vertices']:
                d,h=points[i];value=chosen[0]+chosen[1]*d+chosen[2]*h
                for a in coeffs[cond['key']]:
                    assert a[0]+a[1]*d+a[2]*h>=value
                    counts['cell_corner_state_differences']+=1
assert len(isolated)==9
out={'status':'PASS_MAIN_COMPLETE_CAP3_TWO_PARAMETER_TRUE_STATE_AND_CELL_CHECK',
     'source_sha256':sha256(source.read_bytes()).hexdigest(),'proof_personally_read_complete':True,
     'slices':6,'full_state_planes':1536,'complete_cells':150,'complete_vertices':225,
     'isolated_weak_points':isolated,'checks':counts,'optimizer_calls':0,
     'scope':'Full stated two-parameter true-cost family. No LP point, cone nonredundancy, SPE construction or half conclusion.'}
dest=W/'main_cap3_full_delta_check.json';assert not dest.exists()
dest.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps(out,ensure_ascii=False))
