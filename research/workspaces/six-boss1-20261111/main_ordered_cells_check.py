"""Main rebuilds all cell halfspaces and vertices, then every181x513 coefficient."""
from fractions import Fraction as F
from itertools import combinations,product
from pathlib import Path
from hashlib import sha256
import json

W=Path(__file__).resolve().parent;P=W/'all_source_ordered_menu_cells'
def load(p):return json.loads(p.read_text())
def dot(a,b):return sum((x*y for x,y in zip(a,b)),F(0))
def solve(rows):
    n=len(rows);m=[[F(x) for x in v]+[-F(c)] for c,v in rows]
    for col in range(n):
        pivot=next((r for r in range(col,n) if m[r][col]),None)
        if pivot is None:return None
        m[col],m[pivot]=m[pivot],m[col];d=m[col][col]
        m[col]=[v/d for v in m[col]]
        for r in range(n):
            if r!=col and m[r][col]:
                d=m[r][col];m[r]=[v-d*b for v,b in zip(m[r],m[col])]
    return tuple(m[r][-1] for r in range(n))
def loss(i,q):
    return max([F(0)]+[q[j-i-1]+sum((q[h-i-1]/(5*(7-h)*(8-h)) for h in range(j+1,6)),F(0))-F(2,5) for j in range(i+1,6)])
def g(i,p,q):
    s=q[-1];n=6-i;ci=F(n+1,2)
    return (ci+F(24,p+n+1)+F(1,p+1)-s/min(p+n+1,5)+sum((q[j-i-1]/(p+7-j) for j in range(i+1,6)),F(0)))/6-(F(5,6)*loss(i,q) if p==0 else 0)

def main():
    out=W/'main_ordered_cells_check.json';assert not out.exists()
    assert sha256((P/'exact_family.json').read_bytes()).hexdigest()=='f1bca409d9927f9721764a327f1fcd52a18c38f0968d9c240fa20288aa95eac3'
    geom=load(P/'parameter_cells.json');family=load(P/'exact_family.json')
    vertex_by_id={};results=[];attempts=0;incidences=0
    for source in geom['sources']:
        i=source['source'];m=5-i;dim=m+1
        planes=[]
        for k,j in enumerate(range(i+1,6)):
            v=[F(0)]*dim;v[k]=1;planes.append((F(0),tuple(v)))
            v=[F(0)]*dim;v[k]=-1
            for h in range(j+1,6):v[h-i-1]=-F(1,6*(7-h)*(8-h))
            planes.append((F(5,12),tuple(v)))
        v=[F(0)]*dim;v[-1]=1;planes.append((F(0),tuple(v)))
        if i==1:
            for k in range(m):
                v=[F(0)]*dim;v[k]=5;v[-1]=-1;planes.append((F(15),tuple(v)))
        else:
            v=[F(0)]*dim;v[-1]=-1;planes.append((F(9),tuple(v)))
        ell={0:(F(0),tuple([F(0)]*dim))}
        for k,j in enumerate(range(i+1,6)):
            v=[F(0)]*dim;v[k]=1
            for h in range(j+1,6):v[h-i-1]=F(1,5*(7-h)*(8-h))
            ell[j]=(F(-2,5),tuple(v))
        known={v['id']:tuple(map(F,v['parameters'])) for v in source['vertices']}
        source_vertices=set();cell_results=[]
        for cell in source['cells']:
            active=cell['active_term'];c,v=ell[active]
            cuts=planes+[(c-d,tuple(x-y for x,y in zip(v,w))) for k,(d,w) in ell.items() if k!=active]
            vv=set()
            for chosen in combinations(cuts,dim):
                attempts+=1;q=solve(chosen)
                if q is not None and all(c+dot(v,q)>=0 for c,v in cuts):vv.add(q)
            expected={known[key] for key in cell['vertex_ids']};assert vv==expected,(i,active,len(vv),len(expected))
            source_vertices|=vv;incidences+=len(vv)
            cell_results.append({'active':active,'vertices':len(vv)})
        assert source_vertices==set(known.values())
        for key,q in known.items():vertex_by_id[key]=(i,q)
        results.append({'source':i,'cells':cell_results,'unique_vertices':len(source_vertices)})
        print('source',i,'complete',len(source_vertices),flush=True)
    assert attempts==32448 and incidences==369 and len(vertex_by_id)==181
    atoms=list(product((0,1),repeat=9));checked=0
    row_by_id={}
    for row in family['rows']:
        i,q=vertex_by_id[row['cell_vertex_id']];a=25+sum(q[:-1])-q[-1];ci=F(7-i,2)
        assert a==F(row['source_IC_weight']) and a>0
        assert loss(i,q)==F(row['loss_L']) and F(row['numerical_divisor'])==25
        for p in range(i):assert g(i,p,q)==F(row['G_by_prefix_load'][str(p)])
        for h,bits in enumerate(atoms):
            actual=bits[:6];p=sum(actual[:i-1]);o=bits[7]
            u=F(actual[i-1],sum(actual)) if sum(actual) else F(0)
            assert F(row['a'].get(str(h),'0'))==a*u-o*g(i,p,q)
            checked+=1
        assert F(row['a']['512'])==ci;checked+=1
        row_by_id[row['cell_vertex_id']]=row
    old=load(W/'all_source_joint_reweighted_safe/parameter_polytopes.json')['sources']
    old_by_id={v['id']:(s['source'],tuple(map(F,v['theta']))+(F(v['s']),)) for s in old for v in s['vertices']}
    strict=0
    for rec in load(P/'old_vertex_interpolations.json')['records']:
        i,q=vertex_by_id[rec['cell_vertex_id']]
        weights=[(F(r['weight']),old_by_id[r['old_vertex_id']][1]) for r in rec['old_vertex_weights']]
        assert all(w>=0 for w,v in weights) and sum(w for w,v in weights)==1
        assert all(sum(w*v[k] for w,v in weights)==q[k] for k in range(len(q)))
        gap=sum(w*loss(i,v) for w,v in weights)-loss(i,q)
        assert gap==F(rec['Jensen_gap'])>=0
        assert (gap==0)==rec['is_original_vertex'];strict+=gap>0
        # The full row Jensen difference follows independently at each prefix and actual membership.
        for p in range(i):
            assert g(i,p,q)-sum(w*g(i,p,v) for w,v in weights)==(F(5,6)*gap if p==0 else 0)
    assert strict==114 and checked==92853
    r={'status':'PASS_MAIN_COMPLETE181_CELL_GEOMETRY_AND_ALL513_COLUMNS','optimizer_calls':0,
       'source_results':results,'all_boundary_intersections':attempts,'all_cell_vertex_incidences':incidences,
       'full_coefficients':checked,'strict_old_vertex_Jensen_gaps':strict,
       'source_proof_read_sha256':sha256((P/'proof.md').read_bytes()).hexdigest(),
       'source_family_sha256':sha256((P/'exact_family.json').read_bytes()).hexdigest(),
       'source_manifest_sha256':sha256((P/'freeze_manifest.json').read_bytes()).hexdigest(),
       'scope':'Main personally read continuous source proof and finite-generation proof, reconstructed every cell and its complete rational vertex set, and derived every coefficient. Complete finite representation of specified family only.'}
    out.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n');print(json.dumps(r,ensure_ascii=False))

if __name__=='__main__':main()
