#!/usr/bin/env python3
"""Boss1 full-delta cap3: exact two-dimensional COST geometry, no matrices/LP.

Agent /root/source2_cap3_tradeoff.  Writes only beside this script.  The two
frozen source proofs are read for provenance; no previous cache is imported.
"""
from fractions import Fraction as F
from itertools import product
from math import gcd, lcm
from pathlib import Path
import argparse
import hashlib
import json
import traceback

HERE=Path(__file__).resolve().parent
DEFAULT_REPO=Path("/workspace/scratch/b0fef5ec503f/co-work-anl-boss1")
b=F(5977,6912)
v=F(43,48)
TAILS=tuple(product((0,1),repeat=4))
S_VALUES=(("s0",F(0)),("sstar",F(61273,6912)),("s9",F(9)))


def serial(x):
    if isinstance(x,F): return str(x)
    if isinstance(x,dict): return {str(k):serial(vv) for k,vv in x.items()}
    if isinstance(x,(tuple,list)): return [serial(vv) for vv in x]
    return x


def save(name,obj):
    (HERE/name).write_text(json.dumps(serial(obj),ensure_ascii=False,indent=2)+"\n",encoding="utf-8")


def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()


def parameters(mode,s,delta,h):
    q0=F(1,6 if mode=="pure" else 5)
    x,y=b-delta,v+delta
    B=q0*(F(1,2)+x/12+y/6)
    return dict(q0=q0,tau=(F(0),x,y),caps=(B-h,q0/2+x+q0*y/6,q0/2+y),
                B=B,S=1+B-h+q0+x+y+q0*y/6,a=25+x+y-s)


def cost(mode,s,p,t,q,r,delta,h):
    w=parameters(mode,s,delta,h)
    r3,r4,r5,z=r
    L=p+t+r3+r4+r5+z
    N=w["a"]*t-z-w["tau"][1]*r4-w["tau"][2]*r5
    assert L or not N
    return ((N/L if L else F(0))+sum(w["caps"][j]*r[j] for j in range(3))+z
            +q/(p+t+r3+r4+r5+1)+w["tau"][1]*q/(p+t+r3+3)
            +w["tau"][2]*q/(p+t+r3+r4+2))


def ev(plane,point): return plane[0]+plane[1]*point[0]+plane[2]*point[1]
def sub(x,y): return tuple(xx-yy for xx,yy in zip(x,y))
def add(x,y): return tuple(xx+yy for xx,yy in zip(x,y))
def scale(x,w): return tuple(w*xx for xx in x)
def cross(o,a,c): return (a[0]-o[0])*(c[1]-o[1])-(a[1]-o[1])*(c[0]-o[0])


def normalize(poly):
    pts=[]
    for x in poly:
        if not pts or pts[-1]!=x: pts.append(tuple(x))
    if len(pts)>1 and pts[0]==pts[-1]: pts.pop()
    if len(pts)<=1: return pts
    if all(cross(pts[0],pts[1],x)==0 for x in pts[2:]):
        return sorted(set(pts))[::max(1,len(set(pts))-1)]
    changed=True
    while changed:
        changed=False
        for i in range(len(pts)):
            if cross(pts[i-1],pts[i],pts[(i+1)%len(pts)])==0:
                del pts[i]
                changed=True
                break
    if sum(pts[i][0]*pts[(i+1)%len(pts)][1]-pts[(i+1)%len(pts)][0]*pts[i][1] for i in range(len(pts)))<0:
        pts.reverse()
    k=pts.index(min(pts))
    return pts[k:]+pts[:k]


def dim(poly):
    if not poly: return -1
    if len(poly)==1: return 0
    return 1 if len(poly)==2 else 2


def clip(poly,plane):
    if not poly: return []
    if len(poly)==1: return poly if ev(plane,poly[0])<=0 else []
    out=[]
    for A,C in zip(poly,poly[1:]+poly[:1]):
        fa,fc=ev(plane,A),ev(plane,C)
        if fa<=0: out.append(A)
        if (fa<0<fc) or (fc<0<fa):
            w=fa/(fa-fc)
            out.append((A[0]+w*(C[0]-A[0]),A[1]+w*(C[1]-A[1])))
        elif fa>0 and fc==0:
            out.append(C)
    return normalize(out)


def canonical_line(plane):
    if plane[1]==0 and plane[2]==0: return None
    den=lcm(*(z.denominator for z in plane))
    ns=[int(z*den) for z in plane]
    g=gcd(gcd(abs(ns[0]),abs(ns[1])),abs(ns[2]))
    ns=[n//g for n in ns]
    if next(n for n in ns if n)!=abs(next(n for n in ns if n)):
        ns=[-n for n in ns]
    return tuple(ns)


def through(A,C):
    return canonical_line((A[0]*C[1]-C[0]*A[1],A[1]-C[1],C[0]-A[0]))


def centroid(poly):
    return (sum((x[0] for x in poly),F(0))/len(poly),sum((x[1] for x in poly),F(0))/len(poly))


def at_condition(condition,point):
    vals={r["tail"]:ev(r["affine"],point) for r in condition["states"]}
    m=min(vals.values())
    active=[name for name,z in vals.items() if z==m]
    selected=next(r["affine"] for r in condition["states"] if r["tail"]==active[0])
    return dict(value=m,tails=active,affine=selected)


def condition_key(p,t,n): return f"p{p}_t{t}_n{n}"


def make_conditions(mode,s,domain,domain_constraints):
    result=[]
    for p,t in product((0,1),repeat=2):
        ns=range(2) if mode=="pure" else range(t,6+t)
        for n in ns:
            q=F(n,6) if mode=="pure" else F(n-t,5)
            planes={}
            for r in TAILS:
                zero=cost(mode,s,p,t,q,r,F(0),F(0))
                dx=(cost(mode,s,p,t,q,r,b,F(0))-zero)/b
                dh=-F(r[0])
                planes["".join(map(str,r))]=(zero,dx,dh)
            states=[]
            for name,plane in planes.items():
                constraints=list(domain_constraints)+[sub(plane,other) for other_name,other in planes.items() if other_name!=name]
                poly=list(domain)
                for constraint in constraints[4:]:
                    poly=clip(poly,constraint)
                states.append(dict(tail=name,affine=plane,weak_region_dimension=dim(poly),
                                   weak_region_vertices=poly,constraints=constraints))
            result.append(dict(key=condition_key(p,t,n),p=p,t=t,n=n,
                               n_means="o" if mode=="pure" else "d",q=q,states=states))
    return result


def multiplicity_affines(conditions,point):
    index={c["key"]:c for c in conditions}
    out={}
    for p in (0,1):
        f={}
        for d in range(7):
            line=(F(0),F(0),F(0))
            if d<6:
                line=add(line,scale(at_condition(index[condition_key(p,0,d)],point)["affine"],F(6-d,6)))
            if d>0:
                line=add(line,scale(at_condition(index[condition_key(p,1,d)],point)["affine"],F(d,6)))
            f[d]=line
        m=min(ev(f[d],point) for d in range(1,7))
        active=[d for d in range(1,7) if ev(f[d],point)==m]
        out[p]=dict(f=f,G=f[active[0]],active_d=active)
    return out


def make_slice(mode,sname,s):
    w0=parameters(mode,s,F(0),F(0))
    wb=parameters(mode,s,b,F(0))
    B0=w0["B"]
    Bd=(wb["B"]-B0)/b
    domain=normalize([(F(0),F(0)),(b,F(0)),(b,wb["B"]),(F(0),B0)])
    constraints=[(F(0),F(-1),F(0)),(-b,F(1),F(0)),(F(0),F(0),F(-1)),(-B0,-Bd,F(1))]
    conditions=make_conditions(mode,s,domain,constraints)
    domain_lines={canonical_line(x) for x in constraints}
    all_lines=set()
    for c in conditions:
        for r in c["states"]:
            poly=r["weak_region_vertices"]
            if len(poly)>=2:
                for A,C in zip(poly,poly[1:]+poly[:1]):
                    if A!=C: all_lines.add(through(A,C))
    internal=sorted(all_lines-domain_lines)
    cells=[domain]
    for line in internal:
        next_cells=[]
        for poly in cells:
            values=[ev(line,point) for point in poly]
            if min(values)<0<max(values):
                left=clip(poly,line)
                right=clip(poly,tuple(-x for x in line))
                assert dim(left)==dim(right)==2
                next_cells.extend([left,right])
            else:
                next_cells.append(poly)
        cells=next_cells
    cells=sorted(cells,key=lambda z:tuple(z))
    points=sorted({pt for poly in cells for pt in poly})
    point_ids={pt:i for i,pt in enumerate(points)}
    edges=sorted({tuple(sorted((A,C))) for poly in cells for A,C in zip(poly,poly[1:]+poly[:1])})
    vertices=[]
    edge_records=[]
    cell_records=[]
    for i,point in enumerate(points):
        vertices.append(dict(id=i,point=point,conditions={c["key"]:at_condition(c,point) for c in conditions},
                             multiplicities=multiplicity_affines(conditions,point) if mode=="ordered" else None))
    for i,edge in enumerate(edges):
        mid=centroid(edge)
        edge_records.append(dict(id=i,vertices=[point_ids[pt] for pt in edge],interior_point=mid,
                                 conditions={c["key"]:at_condition(c,mid) for c in conditions}))
    for i,poly in enumerate(cells):
        mid=centroid(poly)
        condition_values={c["key"]:at_condition(c,mid) for c in conditions}
        for c in conditions:
            selected=condition_values[c["key"]]["affine"]
            assert all(ev(sub(r["affine"],selected),pt)>=0 for r in c["states"] for pt in poly)
        cell_records.append(dict(id=i,vertices=[point_ids[pt] for pt in poly],interior_point=mid,
                                 conditions=condition_values,
                                 multiplicities=multiplicity_affines(conditions,mid) if mode=="ordered" else None))
    assert len(points)-len(edges)+len(cells)==1
    assert all(pt in point_ids for c in conditions for r in c["states"] for pt in r["weak_region_vertices"])
    return dict(id=f"{mode}_{sname}",mode=mode,s=s,q0=w0["q0"],domain_vertices=domain,
                domain_constraints=constraints,B_affine=(B0,Bd),conditions=conditions,
                internal_boundary_lines=internal,vertices=vertices,edges=edge_records,cells=cell_records)


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--source-repo",type=Path,default=DEFAULT_REPO)
    args=parser.parse_args()
    assert not (HERE/"freeze_manifest.json").exists(),"Frozen: replay in a separate copy."
    rel=Path("research/workspaces/six-boss1-20261111")
    sources=[rel/"source2_cap3_tradeoff/proof.md",rel/"source2_conditional_redistribution/proof.md"]
    pins=[]
    for source in sources:
        path=args.source_repo/source
        path.read_text(encoding="utf-8")
        pins.append(dict(path=str(source),bytes=path.stat().st_size,sha256=digest(path)))
    save("source_pins.json",dict(run="six-boss1-20261111",boss="Boss1",agent_id="/root/source2_cap3_tradeoff",
                                 source_repo=str(args.source_repo),files=pins,source_access="read-only",
                                 frozen_predecessor_modified=False,candidate_inputs_read=0,optimization_calls=0))
    slices=[]
    for mode in ("pure","ordered"):
        for sname,s in S_VALUES:
            sl=make_slice(mode,sname,s)
            slices.append(sl)
            print(sl["id"],"conditions",len(sl["conditions"]),"cells",len(sl["cells"]),"edges",len(sl["edges"]),"vertices",len(sl["vertices"]),flush=True)
    save("exact_envelopes_2d.json",dict(schema="source2-cap3-full-delta-2d-v1",variables=["delta","h"],
                                      affine_order=["constant","delta","h"],tail_order="r3,r4,r5,z",
                                      b=b,slices=slices,matrices_materialized=False))
    dims={k:sum(r["weak_region_dimension"]==k for sl in slices for c in sl["conditions"] for r in c["states"]) for k in (-1,0,1,2)}
    summary=dict(slices=len(slices),conditions=sum(len(sl["conditions"]) for sl in slices),
                 tail_planes=sum(16*len(sl["conditions"]) for sl in slices),weak_region_dimensions=dims,
                 cells=sum(len(sl["cells"]) for sl in slices),edges=sum(len(sl["edges"]) for sl in slices),
                 vertices=sum(len(sl["vertices"]) for sl in slices),
                 per_slice=[dict(id=sl["id"],cells=len(sl["cells"]),edges=len(sl["edges"]),vertices=len(sl["vertices"]),
                                 vertical_cuts=sorted({pt["point"][0] for pt in sl["vertices"]}),
                                 internal_boundary_lines=sl["internal_boundary_lines"]) for sl in slices],
                 potential_full_condition_endpoint_rows=sum(len(sl["vertices"])*(9 if sl["mode"]=="pure" else 1) for sl in slices),
                 matrices_materialized=False)
    save("derivation_summary.json",summary)
    assert all(digest(args.source_repo/r["path"])==r["sha256"] for r in pins)
    print(json.dumps(serial(summary),ensure_ascii=False,indent=2))


if __name__=="__main__":
    try:
        main()
    except BaseException as e:
        file=HERE/"failure_log.json"
        log=json.loads(file.read_text()) if file.exists() else []
        log.append(dict(stage="derive_2d",type=type(e).__name__,message=str(e),traceback=traceback.format_exc()))
        save("failure_log.json",log)
        raise
