#!/usr/bin/env python3
"""Independent literal COST and all-boundary-pairs verification; no imports
from the generator or previous project code, and no optimization routines.
"""
from fractions import Fraction as Q
from itertools import product, combinations
from functools import lru_cache
from math import gcd, lcm
from pathlib import Path
import hashlib
import json
import traceback

P=Path(__file__).resolve().parent
BDELTA=Q(5977,6912)
V=Q(43,48)
THETA=BDELTA+V
TAILS=tuple(product((0,1),repeat=4))
COUNTS={}


def count(key,n=1): COUNTS[key]=COUNTS.get(key,0)+n


def save(name,obj):
    def ser(z):
        if isinstance(z,Q): return str(z)
        if isinstance(z,dict): return {str(k):ser(v) for k,v in z.items()}
        if isinstance(z,(tuple,list)): return [ser(v) for v in z]
        return z
    (P/name).write_text(json.dumps(ser(obj),ensure_ascii=False,indent=2)+"\n",encoding="utf-8")


def coefficients(mode,s,delta,h):
    q0=Q(1,6) if mode=="pure" else Q(1,5)
    x,y=BDELTA-delta,V+delta
    B=q0/2+q0*x/12+q0*y/6
    return 25+THETA-s,B-h,q0/2+x+q0*y/6,q0/2+y,x,y,B,q0


@lru_cache(None)
def literal(mode,s,p,t,q,r,delta,h):
    a,b3,b4,b5,x,y,B,q0=coefficients(mode,s,delta,h)
    r3,r4,r5,z=r
    L=p+t+r3+r4+r5+z
    share=lambda member: Q(member,L) if L else Q(0)
    income=a*share(t)-x*share(r4)-y*share(r5)-share(z)
    caps=b3*r3+b4*r4+b5*r5+z
    end=q/Q(p+t+r3+r4+r5+1)
    safe4=x*q/Q(p+t+r3+3)
    safe5=y*q/Q(p+t+r3+r4+2)
    return income+caps+end+safe4+safe5


def ev(line,point): return line[0]+line[1]*point[0]+line[2]*point[1]
def sub(a,b): return tuple(x-y for x,y in zip(a,b))


def integers(line):
    den=lcm(*(x.denominator for x in line))
    ns=tuple(int(x*den) for x in line)
    g=gcd(gcd(abs(ns[0]),abs(ns[1])),abs(ns[2]))
    return tuple(n//g for n in ns) if g else ns


def in_halfspace(line,point):
    a,c,e=line
    dn,dd=point[0].numerator,point[0].denominator
    hn,hd=point[1].numerator,point[1].denominator
    return a*dd*hd+c*dn*hd+e*hn*dd<=0


def convex_hull(points):
    pts=sorted(set(points))
    if len(pts)<=1: return pts
    def cross(a,b,c): return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
    lower=[]
    for x in pts:
        while len(lower)>=2 and cross(lower[-2],lower[-1],x)<=0: lower.pop()
        lower.append(x)
    upper=[]
    for x in reversed(pts):
        while len(upper)>=2 and cross(upper[-2],upper[-1],x)<=0: upper.pop()
        upper.append(x)
    return lower[:-1]+upper[:-1]


def region_from_boundary_pairs(inequalities):
    ints=set(integers(line) for line in inequalities)
    if any(c==e==0 and a>0 for a,c,e in ints): return []
    ints=sorted(line for line in ints if line[1] or line[2])
    points=set()
    for (a,c,e),(aa,cc,ee) in combinations(ints,2):
        determinant=c*ee-cc*e
        count("boundary_pairs_examined")
        if not determinant: continue
        point=(Q(e*aa-a*ee,determinant),Q(a*cc-c*aa,determinant))
        if all(in_halfspace(line,point) for line in ints): points.add(point)
    return convex_hull(points)


def dimension(poly): return -1 if not poly else 0 if len(poly)==1 else 1 if len(poly)==2 else 2


def minimum(lines,point):
    values={tail:ev(line,point) for tail,line in lines.items()}
    m=min(values.values())
    return m,tuple(tail for tail,value in values.items() if value==m)


def plane_for(mode,s,p,t,q,r):
    z=literal(mode,s,p,t,q,r,Q(0),Q(0))
    d=(literal(mode,s,p,t,q,r,BDELTA,Q(0))-z)/BDELTA
    cap=coefficients(mode,s,Q(0),Q(0))[6]
    h=(literal(mode,s,p,t,q,r,Q(0),cap)-z)/cap
    return z,d,h


def h_level(mode,delta,n):
    q0=Q(1,6) if mode=="pure" else Q(1,5)
    x,y=BDELTA-delta,V+delta
    B=q0*(Q(1,2)+x/12+y/6)
    H1=q0*(Q(1,3)+x/30+y/12)
    if mode=="pure": return (Q(0),H1,B)[n]
    H2=q0*(Q(1,6)-x/60)
    return (Q(0),H2,H1,B)[n]


def old_L(delta,s,p,o):
    if p:
        return max(Q(0),4*delta/5-Q(o,180))
    y=V+delta
    return max(Q(0),(s-Q(61273,6912))/20-13*delta/18-Q(o)*(1+y)/120,
               3*delta/4+s/20-Q(427,960)-Q(o,120))


def E(mode,delta,p,q):
    q0=Q(1,6) if mode=="pure" else Q(1,5)
    x,y=BDELTA-delta,V+delta
    return q0/2+x*Q(p+1,p+2)+q0*y/6-q/Q((p+2)*(p+3))-y*q/Q((p+3)*(p+4))


def f_values(index,point,p):
    out={}
    for d in range(7):
        value=Q(0)
        if d<6: value+=Q(6-d,6)*minimum(index[(p,0,d)],point)[0]
        if d>0: value+=Q(d,6)*minimum(index[(p,1,d)],point)[0]
        out[d]=value
    return out


def main():
    assert not (P/"freeze_manifest.json").exists(),"Frozen: replay separately."
    package=json.loads((P/"exact_envelopes_2d.json").read_text())
    regions=[]
    certs=[]
    multiplicity=[]
    formulas=[]
    total_dimensions={-1:0,0:0,1:0,2:0}
    for sl in package["slices"]:
        mode,s=sl["mode"],Q(sl["s"])
        domain=[tuple(Q(x) for x in line) for line in sl["domain_constraints"]]
        corners=[tuple(Q(x) for x in point) for point in sl["domain_vertices"]]
        for delta,h in corners:
            a,b3,b4,b5,x,y,B,q0=coefficients(mode,s,delta,h)
            assert a>=Q(122761,6912)>0 and all(z>=0 for z in (b3,b4,b5,x,y))
            assert B<=Q(6581,41472)<Q(1,2)
            count("budget_corner_checks")
            # Independent exact checks of the reusable analytic eliminations.
            for p in (0,1):
                for q in (Q(0),Q(1)):
                    for r3,r4,r5 in product((0,1),repeat=3):
                        load=p+r3+r4+r5
                        if load:
                            with_z=literal(mode,s,p,0,q,(r3,r4,r5,1),delta,h)
                            without_z=literal(mode,s,p,0,q,(r3,r4,r5,0),delta,h)
                            A=x*r4+y*r5
                            assert with_z-without_z==Q(load,load+1)+A/Q(load*(load+1))>0
                            count("analytic_terminal_removal_checks")
                    for r3,r4 in product((0,1),repeat=2):
                        load=p+r3+r4
                        if load:
                            added=literal(mode,s,p,0,q,(r3,r4,1,0),delta,h)-literal(mode,s,p,0,q,(r3,r4,0,0),delta,h)
                            assert added==q0/2+y*Q(load,load+1)+x*r4/Q(load*(load+1))-q/Q((load+1)*(load+2))
                            assert added>=Q(35,96)>0
                            count("analytic_fifth_member_removal_checks")
                    for r4,r5,z in product((0,1),repeat=3):
                        added=literal(mode,s,p,1,q,(1,r4,r5,z),delta,h)-literal(mode,s,p,1,q,(0,r4,r5,z),delta,h)
                        assert added<=Q(6581,41472)-Q(1,2)<0
                        count("analytic_third_member_insertion_checks")
                    for before,after,strict in (((1,0,0,0),(1,0,0,1),True),
                                                ((1,0,1,0),(1,0,1,1),False),
                                                ((1,1,0,0),(1,1,0,1),True)):
                        change=literal(mode,s,p,1,q,after,delta,h)-literal(mode,s,p,1,q,before,delta,h)
                        assert change<0 if strict else change<=0
                        count("analytic_t1_terminal_insertion_checks")
                    change=literal(mode,s,p,1,q,(1,1,0,1),delta,h)-literal(mode,s,p,1,q,(1,0,0,1),delta,h)
                    assert change<=-Q(151,9216)<0
                    count("analytic_t1_fourth_member_insertion_checks")
        index={}
        all_x={Q(0),BDELTA}
        all_weak_vertices=set()
        for c in sl["conditions"]:
            p,t,n,q=c["p"],c["t"],c["n"],Q(c["q"])
            assert q==(Q(n,6) if mode=="pure" else Q(n-t,5))
            if mode=="ordered": assert (t==0 and 0<=n<=5) or (t==1 and 1<=n<=6)
            lines={"".join(map(str,r)):plane_for(mode,s,p,t,q,r) for r in TAILS}
            index[(p,t,n)]=lines
            for r,raw in zip(TAILS,c["states"]):
                name="".join(map(str,r))
                assert raw["tail"]==name
                line=lines[name]
                assert line==tuple(Q(z) for z in raw["affine"]) and line[2]==-r[0]
                for point in corners:
                    assert ev(line,point)==literal(mode,s,p,t,q,r,*point)
                    count("literal_domain_corner_tail_checks")
                inequalities=domain+[sub(line,other) for tail,other in lines.items() if tail!=name]
                assert inequalities==[tuple(Q(x) for x in pp) for pp in raw["constraints"]]
                independent=region_from_boundary_pairs(inequalities)
                expected=[tuple(Q(x) for x in point) for point in raw["weak_region_vertices"]]
                assert set(independent)==set(expected)
                assert dimension(independent)==raw["weak_region_dimension"]
                total_dimensions[dimension(independent)]+=1
                all_weak_vertices.update(independent)
                all_x.update(pt[0] for pt in independent)
                regions.append(dict(slice=sl["id"],condition=c["key"],tail=name,
                                    dimension=dimension(independent),vertices=independent))
                count("independently_reconstructed_tail_planes")
        # Independently build the full common complex as an exact affine grid.
        xs=sorted(all_x)
        bands=2 if mode=="pure" else 3
        wanted_points={(delta,h_level(mode,delta,k)) for delta in xs for k in range(bands+1)}
        stored_points={tuple(Q(z) for z in point["point"]) for point in sl["vertices"]}
        assert wanted_points==stored_points and all_weak_vertices<=wanted_points
        wanted_cells=[]
        for left,right in zip(xs,xs[1:]):
            for k in range(bands):
                wanted_cells.append(frozenset(((left,h_level(mode,left,k)),(right,h_level(mode,right,k)),
                                              (right,h_level(mode,right,k+1)),(left,h_level(mode,left,k+1)))))
        points_by_id={point["id"]:tuple(Q(z) for z in point["point"]) for point in sl["vertices"]}
        stored_cells=[frozenset(points_by_id[i] for i in cell["vertices"]) for cell in sl["cells"]]
        assert set(wanted_cells)==set(stored_cells) and len(wanted_cells)==len(stored_cells)
        assert len(sl["vertices"])-len(sl["edges"])+len(sl["cells"])==1
        count("independent_full_cells",len(wanted_cells))
        count("independent_complex_vertices",len(wanted_points))
        for point_record in sl["vertices"]:
            point=points_by_id[point_record["id"]]
            for c in sl["conditions"]:
                key=(c["p"],c["t"],c["n"])
                lines=index[key]
                m,weak=minimum(lines,point)
                saved=point_record["conditions"][c["key"]]
                assert Q(saved["value"])==m and tuple(saved["tails"])==weak
                for r in TAILS:
                    assert literal(mode,s,c["p"],c["t"],Q(c["q"]),r,*point)==ev(lines["".join(map(str,r))],point)
                    count("literal_all_complex_vertex_tail_checks")
                count("all_vertex_weak_sets")
        for edge in sl["edges"]:
            point=tuple(Q(z) for z in edge["interior_point"])
            ends=[points_by_id[i] for i in edge["vertices"]]
            assert point==tuple((ends[0][j]+ends[1][j])/2 for j in range(2))
            for c in sl["conditions"]:
                m,weak=minimum(index[(c["p"],c["t"],c["n"])],point)
                saved=edge["conditions"][c["key"]]
                assert Q(saved["value"])==m and tuple(saved["tails"])==weak
                count("all_open_edge_weak_sets")
        gap_min=None
        for cell in sl["cells"]:
            pts=[points_by_id[i] for i in cell["vertices"]]
            mid=tuple(Q(z) for z in cell["interior_point"])
            assert len(pts)==4 and mid==tuple(sum(pt[j] for pt in pts)/4 for j in range(2))
            for c in sl["conditions"]:
                p,t,n,q=c["p"],c["t"],c["n"],Q(c["q"])
                lines=index[(p,t,n)]
                m,weak=minimum(lines,mid)
                stored=cell["conditions"][c["key"]]
                selected=tuple(Q(z) for z in stored["affine"])
                assert Q(stored["value"])==m and tuple(stored["tails"])==weak
                assert ev(selected,mid)==m
                candidates=("1110","1111","1011","1101") if t else ("0000","1000","1100")
                assert any(lines[r]==selected for r in candidates)
                gaps={tail:[ev(sub(line,selected),point) for point in pts] for tail,line in lines.items()}
                assert all(g>=0 for values in gaps.values() for g in values)
                count("all_cell_corner_tail_gaps",16*len(pts))
                count("compact_candidate_affine_identities")
                certs.append(dict(slice=sl["id"],cell=cell["id"],condition=c["key"],
                                  vertex_ids=cell["vertices"],selected=selected,all_tail_vertex_gaps=gaps))
                # All h-shift formulas, using the TRUE h=0 lower envelope.
                for delta,h in pts+[mid]:
                    base=minimum(lines,(delta,Q(0)))[0]
                    actual=minimum(lines,(delta,h))[0]
                    if t:
                        loss=h
                    elif q==0:
                        loss=Q(0)
                    elif p==0:
                        loss=h
                    elif mode=="pure" or n==1:
                        H=h_level(mode,delta,1 if mode=="pure" else 2)
                        loss=max(Q(0),h-H)
                    elif n==2:
                        loss=max(Q(0),h-h_level(mode,delta,1))
                    else:
                        loss=h
                    assert base-actual==loss
                    count("all_condition_shift_formula_checks")
                    if mode=="pure":
                        a,b3,b4,b5,x,y,B,q0=coefficients(mode,s,delta,Q(0))
                        S=1+b3+b4+b5
                        anchor=t*(S+Q(24,p+5)-s/5)+Q(n,6)*(Q(1,p+4*t+1)+x/(p+2*t+3)+y/(p+3*t+2))
                        assert base==anchor-t*old_L(delta,s,p,n)
                        count("original_delta_losses_preserved")
                    else:
                        if not t:
                            assert ev(lines["1100"],(delta,h))-ev(lines["1000"],(delta,h))==E(mode,delta,p,q)
                            count("extra_1100_loss_identities")
            if mode=="ordered":
                for p in (0,1):
                    stored=cell["multiplicities"][str(p)]
                    ff={int(d):tuple(Q(x) for x in line) for d,line in stored["f"].items()}
                    assert stored["active_d"]==[1]
                    assert tuple(Q(x) for x in stored["G"])==ff[1]
                    for point in pts+[mid]:
                        fv=f_values(index,point,p)
                        assert fv[0]==0
                        for d in range(7):
                            assert ev(ff[d],point)==fv[d]
                            count("all_physical_multiplicity_affine_checks")
                        for d in range(1,6):
                            assert fv[d+1]-fv[d]>=Q(8567,82944)>0
                            count("strict_adjacent_multiplicity_checks")
                        for d in range(2,7):
                            assert fv[d]-fv[1]>=Q(d-1)*Q(146807,414720)>0
                            count("strict_d1_multiplicity_checks")
                        delta,h=point
                        H1=h_level(mode,delta,2)
                        g0=f_values(index,(delta,Q(0)),p)[1]
                        decrease=h if p==0 else h/6+Q(5,6)*max(Q(0),h-H1)
                        assert fv[1]==g0-decrease
                        count("ordered_G_shift_checks")
                    pairs=[]
                    for d,e in combinations(range(1,7),2):
                        diff=sub(ff[e],ff[d])
                        values=[ev(diff,point) for point in pts]
                        assert all(z>=Q(e-d)*Q(8567,82944)>0 for z in values)
                        gap_min=min(values) if gap_min is None else min(gap_min,min(values))
                        pairs.append(dict(d=d,e=e,difference=diff,vertex_values=values))
                        count("all_pair_cell_comparisons")
                    multiplicity.append(dict(slice=sl["id"],cell=cell["id"],p=p,pairs=pairs))
        # Check real indexed routing for every 64-menu at every complex vertex.
        if mode=="ordered":
            for point in stored_points:
                for p in (0,1):
                    fv=f_values(index,point,p)
                    for menu in product((0,1),repeat=6):
                        d=sum(menu)
                        avg=sum((minimum(index[(p,t,d)],point)[0] for t in menu),Q(0))/6
                        assert avg==fv[d]
                        count("all_indexed_menu_vertex_averages")
        # The pure row and C-only identities reduce to all eight local types.
        if mode=="pure":
            for delta,h in stored_points:
                H6=h_level(mode,delta,1)
                for p,t,o in product((0,1),repeat=3):
                    lines=index[(p,t,o)]
                    loss=minimum(lines,(delta,Q(0)))[0]-minimum(lines,(delta,h))[0]
                    expected=h*t+h*(1-t)*(1-p)*o+max(Q(0),h-H6)*(1-t)*p*o
                    assert loss==expected
                    C_remainder=loss-h*t
                    assert C_remainder==h*(1-t)*(1-p)*o+max(Q(0),h-H6)*(1-t)*p*o>=0
                    count("general_and_C_local_coefficient_identities")
                old=coefficients(mode,s,delta,Q(0))
                new=coefficients(mode,s,delta,h)
                S0=1+sum(old[1:4]);Sh=1+sum(new[1:4])
                assert new[0]==old[0] and Sh-S0==-h
                mu0=S0-s/5;muh=Sh-s/5
                assert muh-mu0==-h and Sh-muh==s/5
                count("IC_K_freeEC_identities")
        formulas.append(dict(slice=sl["id"],delta_cuts=xs,complex_cells=len(sl["cells"]),
                             complex_vertices=len(sl["vertices"]),minimum_all_pair_gap=gap_min,
                             general_T_shift="globally exact" if mode=="pure" else None,
                             C_only="globally redundant via nonnegative local masses" if mode=="pure" else None,
                             ordered_G_shift="globally exact" if mode=="ordered" else None))
        print(sl["id"],"independent geometry/corners/formulas PASS",flush=True)
    # Four precise failures of the old two-candidate t=0 formula.
    witnesses=[]
    for p,k in ((0,3),(0,4),(0,5),(1,5)):
        q=Q(k,5)
        e0=E("ordered",Q(0),p,q)
        eb=E("ordered",BDELTA,p,q)
        root=-e0*BDELTA/(eb-e0)
        assert 0<root<BDELTA and e0>0>eb
        values={"".join(map(str,r)):literal("ordered",Q(0),p,0,q,r,BDELTA,Q(0)) for r in TAILS}
        actual=min(values.values())
        old=min(values["0000"],values["1000"])
        assert actual==values["1100"]<old and actual-old==eb
        witnesses.append(dict(p=p,t=0,d=k,q=q,delta_threshold=root,delta=BDELTA,h=Q(0),
                              actual_tail="1100",actual=actual,old_two_candidate_value=old,
                              exact_gap=actual-old,E_affine=[e0,(eb-e0)/BDELTA]))
    assert [w["delta_threshold"] for w in witnesses]==[Q(28853,35712),Q(25517,36864),Q(22181,38016),Q(29975,35424)]
    # Exhaustive index exclusion is purely combinatorial, including duplicates.
    for menu in product((0,1),repeat=6):
        for k,t in enumerate(menu):
            assert Q(sum(menu)-t,5)==Q(sum(menu[j] for j in range(6) if j!=k),5)
            count("inner_five_index_identities")
    # One explicitly preserved old s=9 loss, independently from true shares.
    delta,h,s=Q(0),Q(0),Q(9)
    a,b3,b4,b5,x,y,B,q0=coefficients("pure",s,delta,h)
    old_anchor=1+b3+b4+b5+Q(24,5)-s/5
    true=min(literal("pure",s,0,1,Q(0),r,delta,h) for r in TAILS)
    assert old_anchor-true==Q(187,27648)
    pins=json.loads((P/"source_pins.json").read_text())
    root=Path(pins["source_repo"])
    assert all(hashlib.sha256((root/r["path"]).read_bytes()).hexdigest()==r["sha256"] for r in pins["files"])
    save("independent_weak_regions.json",regions)
    save("all_cell_corner_certificates.json",certs)
    save("multiplicity_cell_certificates.json",multiplicity)
    save("formula_audit.json",dict(slices=formulas,old_m0_two_candidates="false only in four listed ordered large-q conditions",
                                   full_m0_candidates=["0000","1000","1100"],
                                   full_m1_candidates=["1110","1111","1011","1101"],
                                   old_B_numeric_bound="59881/414720 does not cover the extended domain; replace by 6581/41472<1/2",
                                   pure_h_shift="globally exact",C_only_redundancy="globally exact",ordered_G_shift="globally exact",
                                   ordered_multiplicity_order="strict throughout: f1<f2<...<f6; f0=0",
                                   old_s9_delta0_loss=Q(187,27648),new_large_q_witnesses=witnesses))
    save("literal_checker_output.json",dict(status="PASS",counts=COUNTS,weak_region_dimensions=total_dimensions,
                                           source_pins_unchanged=True,optimization_calls=0,LP_points_read=0,
                                           matrices_materialized=False,columns_proved_by_local_identities=True))
    if not (P/"failure_log.json").exists(): save("failure_log.json",[])
    print(json.dumps(COUNTS,ensure_ascii=False,indent=2))


if __name__=="__main__":
    try:
        main()
    except BaseException as e:
        path=P/"failure_log.json"
        old=json.loads(path.read_text()) if path.exists() else []
        old.append(dict(stage="check_literal",type=type(e).__name__,message=str(e),traceback=traceback.format_exc()))
        save("failure_log.json",old)
        raise
