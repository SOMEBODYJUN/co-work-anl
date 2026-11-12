#!/usr/bin/env python3
"""Independent standard-library checker; imports no generator or project code."""
from fractions import Fraction as Q
from itertools import product, combinations
from functools import lru_cache
from pathlib import Path
import hashlib
import json
import traceback

P = Path(__file__).resolve().parent
TAILS = tuple(product((0,1),repeat=4))
CLIENTS = tuple(product((0,1),repeat=9))
COUNTS = {}


def count(name,n=1):
    COUNTS[name]=COUNTS.get(name,0)+n


def output(name,obj):
    def encode(x):
        if isinstance(x,Q): return str(x)
        if isinstance(x,dict): return {str(k):encode(v) for k,v in x.items()}
        if isinstance(x,(list,tuple)): return [encode(v) for v in x]
        return x
    (P/name).write_text(json.dumps(encode(obj),ensure_ascii=False,indent=2)+"\n",encoding="utf-8")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


@lru_cache(None)
def pars(mode,delta,s,h):
    q=Q(1,6) if mode=="pure" else Q(1,5)
    x=Q(5977,6912)-delta
    y=Q(43,48)+delta
    cap3=q/2+q*x/12+q*y/6-h
    cap4=q/2+x+q*y/6
    cap5=q/2+y
    ic=25+x+y-s
    return (ic,cap3,cap4,cap5,x,y,1+cap3+cap4+cap5)


@lru_cache(None)
def literal(mode,delta,s,h,p,t,q,r):
    # Separate individual shares, naked caps, and true-prefix query payments.
    a,b3,b4,b5,x,y,S=pars(mode,delta,s,h)
    r3,r4,r5,z=r
    load=p+t+r3+r4+r5+z
    share=lambda bit: Q(bit,load) if load else Q(0)
    source_payment=a*share(t)
    subtract_internal=x*share(r4)+y*share(r5)
    subtract_terminal=share(z)
    cap_payments=b3*r3+b4*r4+b5*r5+z
    last_query=q/(p+t+r3+r4+r5+1)
    fourth_query=x*q/(p+t+r3+3)
    fifth_query=y*q/(p+t+r3+r4+2)
    return source_payment-subtract_internal-subtract_terminal+cap_payments+last_query+fourth_query+fifth_query


@lru_cache(None)
def direct_min(mode,delta,s,h,p,t,q):
    vals=[literal(mode,delta,s,h,p,t,q,r) for r in TAILS]
    v=min(vals)
    return v,tuple("".join(map(str,r)) for r,u in zip(TAILS,vals) if u==v)


def half_interval(lines,key,top):
    ar,br=lines[key]
    lower,upper=Q(0),top
    for other,(av,bv) in lines.items():
        if other==key: continue
        da,db=ar-av,br-bv
        count("dominance_halfspace_comparisons")
        if db==0:
            if da>0: return None
        elif db>0:
            upper=min(upper,-da/db)
        else:
            lower=max(lower,-da/db)
    return None if lower>upper else [lower,upper]


def closed_phi(mode,delta,s,p,q):
    a,b3,b4,b5,x,y,S=pars(mode,delta,s,Q(0))
    return min(S-1+(25-s)/(p+4)+q*(1+x+y)/(p+5),
               S+(24-s)/(p+5)+q*(1+x+y)/(p+5),
               S-b4+(24+x-s)/(p+4)+q*((1+y)/(p+4)+x/(p+5)),
               S-b5+(24+y-s)/(p+4)+q*(Q(1,p+4)+(x+y)/(p+5)))


def closed_m(mode,delta,s,h,p,t,q):
    a,b3,b4,b5,x,y,S=pars(mode,delta,s,Q(0))
    if t:
        return closed_phi(mode,delta,s,p,q)-h
    zero=q*(Q(1,p+1)+x/(p+3)+y/(p+2))
    r3=b3-h+q*(Q(1,p+2)+x/(p+4)+y/(p+3))
    return min(zero,r3)


def H(mode,delta):
    q=Q(1,6) if mode=="pure" else Q(1,5)
    x=Q(5977,6912)-delta
    y=Q(43,48)+delta
    return q*(Q(1,3)+x/30+y/12)


@lru_cache(None)
def fd(mode,delta,s,h,p,d):
    assert mode=="ordered"
    ans=Q(0)
    if d<6:
        ans+=Q(6-d,6)*direct_min(mode,delta,s,h,p,0,Q(d,5))[0]
    if d>0:
        ans+=Q(d,6)*direct_min(mode,delta,s,h,p,1,Q(d-1,5))[0]
    return ans


@lru_cache(None)
def vec(mode,delta,s,h,kind,target):
    a,b3,b4,b5,x,y,S=pars(mode,delta,s,h)
    mu=S-s/5 if kind=="C-only" else Q(0)
    if mode=="pure":
        idx=int(target[1:])-1 if target.startswith("A") else 6 if target=="X" else 8
        mm={(p,t,o):direct_min(mode,delta,s,h,p,t,Q(o,6))[0] for p,t,o in product((0,1),repeat=3)}
    else:
        gg={p:min(fd(mode,delta,s,h,p,d) for d in range(1,7)) for p in (0,1)}
    out=[]
    for v in CLIENTS:
        share=Q(v[1],sum(v[:6])) if sum(v[:6]) else Q(0)
        query=mm[(v[0],v[idx],v[7])] if mode=="pure" else v[7]*gg[v[0]]
        out.append(a*share-query+mu*v[8])
    return tuple(out+[S-mu])


def assert_metadata(row,sl):
    mode,delta,s=sl["mode"],Q(sl["delta"]),Q(sl["s"])
    h=Q(row["h"])
    a,b3,b4,b5,x,y,S=pars(mode,delta,s,h)
    q0=Q(1,6) if mode=="pure" else Q(1,5)
    expected_beta={"3":b3,"4":b4,"5":b5}
    expected_tau={"3":Q(0),"4":x,"5":y}
    assert Q(row["q0"])==q0 and row["source"]==2 and row["column_count"]==513
    assert row["slice_id"]==sl["id"] and Q(row["delta"])==delta and Q(row["s"])==s
    assert {k:Q(v) for k,v in row["beta_actual"].items()}==expected_beta
    assert {k:Q(v) for k,v in row["beta_original"].items()}==dict(expected_beta,**{"3":b3+h})
    assert {k:Q(v) for k,v in row["tau"].items()}==expected_tau
    budget=row["real_budget"]
    assert Q(budget["source_IC"])==a
    assert {k:Q(v) for k,v in budget["intermediate_CAP"].items()}==expected_beta
    assert {k:Q(v) for k,v in budget["internal_SAFE"].items()}==expected_tau
    assert Q(budget["terminal_CAP"])==Q(budget["terminal_BR"])==1
    assert Q(budget["inner_query_average"])==q0
    assert budget["outer_average"] is None if mode=="pure" else Q(budget["outer_average"])==Q(1,6)
    mu=S-s/5 if row["row_kind"]=="C-only" else Q(0)
    assert Q(row["raw_K"])==S and Q(row["K"])==S-mu and Q(row["free_EC"])==mu
    assert Q(row["numerical_divisor"])==25
    assert a>0 and all(b>=0 for b in (b3,b4,b5,x,y))
    count("complete_row_metadata_records")


def tradeoff_vector(sl,kind,target,h):
    mode,delta,s=sl["mode"],Q(sl["delta"]),Q(sl["s"])
    hstar=H(mode,delta)
    pp=max(Q(0),h-hstar)
    out=[]
    if mode=="pure":
        idx=int(target[1:])-1 if target.startswith("A") else 6 if target=="X" else 8
        for v in CLIENTS:
            p,t,o=v[0],v[idx],v[7]
            gain=h*t+h*(1-t)*(1-p)*o+pp*(1-t)*p*o
            if kind=="C-only": gain-=h*v[8]
            out.append(gain)
        out.append(Q(0) if kind=="C-only" else -h)
    else:
        for v in CLIENTS:
            out.append(v[7]*(h*(1-v[0])+v[0]*(h/6+Q(5,6)*pp)))
        out.append(-h)
    return tuple(out)


def main():
    assert not (P/"freeze_manifest.json").exists(),"Frozen package: replay in a separate copy."
    env=json.loads((P/"exact_envelopes.json").read_text())
    slices={sl["id"]:sl for sl in env["slices"]}
    dom_report=[]
    weak_report=[]
    certificates=[]
    gap_report=[]
    for sl in slices.values():
        mode,delta,s=sl["mode"],Q(sl["delta"]),Q(sl["s"])
        top=pars(mode,delta,s,Q(0))[1]
        assert [Q(x) for x in sl["h_domain"]]==[Q(0),top]
        common=set([Q(0),top])
        independent={}
        for c in sl["conditions"]:
            p,t,n,q=c["p"],c["t"],c["n"],Q(c["q"])
            assert q==(Q(n,6) if mode=="pure" else Q(n-t,5))
            if mode=="ordered": assert (t==0 and 0<=n<=5) or (t==1 and 1<=n<=6)
            lines={}
            for raw,r in zip(c["tails"],TAILS):
                name="".join(map(str,r))
                assert raw["tail"]==name
                intercept=literal(mode,delta,s,Q(0),p,t,q,r)
                slope=literal(mode,delta,s,top,p,t,q,r)/top-intercept/top
                assert slope==-r[0]
                assert Q(raw["intercept"])==intercept and Q(raw["slope"])==slope
                lines[name]=(intercept,slope)
                for h in (Q(0),top/2,top):
                    assert literal(mode,delta,s,h,p,t,q,r)==intercept+slope*h
                    count("individual_share_affine_checks")
                count("tail_affines")
            expected_breaks={Q(0),top}
            tail_doms={}
            for raw in c["tails"]:
                name=raw["tail"]
                interval=half_interval(lines,name,top)
                got=None if raw["weak_minimum_interval"] is None else [Q(x) for x in raw["weak_minimum_interval"]]
                assert interval==got
                assert raw["zero_length"]==bool(interval is not None and interval[0]==interval[1])
                if interval is not None: expected_breaks.update(interval)
                tail_doms[name]=interval
                dom_report.append(dict(slice=sl["id"],condition=c["key"],tail=name,interval=interval))
            assert expected_breaks==set(Q(x) for x in c["breaks"])
            common.update(expected_breaks)
            independent[c["key"]]=(c,lines,tail_doms)
            U=min(a for name,(a,b) in lines.items() if name[0]=="0")
            V=min(a for name,(a,b) in lines.items() if name[0]=="1")
            assert [U,V]==[Q(x) for x in c["group_min_at_zero"]]
            assert Q(c["kappa"])==max(Q(0),V-U)
        assert sorted(common)==[Q(x) for x in sl["common_breaks"]]
        points=sorted(common)
        samples=sorted(common|{(l+u)/2 for l,u in zip(points,points[1:])})
        for key,(c,lines,tail_doms) in independent.items():
            p,t,q=c["p"],c["t"],Q(c["q"])
            for h in samples:
                m,weak=direct_min(mode,delta,s,h,p,t,q)
                derived=tuple(name for name,iv in tail_doms.items() if iv is not None and iv[0]<=h<=iv[1])
                assert weak==derived
                assert closed_m(mode,delta,s,h,p,t,q)==m
                for r in TAILS:
                    value=literal(mode,delta,s,h,p,t,q,r)
                    assert value>=m
                    count("global_sample_tail_comparisons")
                weak_report.append(dict(slice=sl["id"],condition=key,h=h,minimum=m,all_active_tails=weak))
                count("closed_condition_formula_checks")
            for lo,hi in zip(points,points[1:]):
                mid=(lo+hi)/2
                _,active=direct_min(mode,delta,s,mid,p,t,q)
                a,b=lines[active[0]]
                gaps={name:[aa+bb*lo-a-b*lo,aa+bb*hi-a-b*hi] for name,(aa,bb) in lines.items()}
                assert all(v>=0 for vv in gaps.values() for v in vv)
                count("all_segment_tail_endpoint_comparisons",32)
                certificates.append(dict(slice=sl["id"],condition=key,lo=lo,hi=hi,
                                         selected_affine=[a,b],all_active_tails=active,all_tail_gaps=gaps))
        # The six-query weakening is an exact identity for every real d.
        if mode=="pure":
            for h in points:
                a,b3,b4,b5,x,y,S=pars(mode,delta,s,h)
                for p,t in product((0,1),repeat=2):
                    for r in TAILS:
                        r3,r4,r5,z=r
                        slope=Q(1,p+t+r3+r4+r5+1)+x/Q(p+t+r3+3)+y/Q(p+t+r3+r4+2)
                        assert slope>0
                        for d in range(7):
                            o=int(d>0)
                            actual=literal(mode,delta,s,h,p,t,Q(d,6),r)
                            weakened=literal(mode,delta,s,h,p,t,Q(o,6),r)
                            assert actual-weakened==Q(d-o,6)*slope>=0
                            count("pure_true_query_weakening_identities")
        else:
            min_gap=None
            for seg in sl["multiplicity_segments"]:
                lo,hi=Q(seg["lo"]),Q(seg["hi"])
                p=seg["p"]
                f={int(d):tuple(Q(x) for x in v) for d,v in seg["f_affines"].items()}
                for d in range(7):
                    for h in (lo,(lo+hi)/2,hi):
                        assert f[d][0]+f[d][1]*h==fd(mode,delta,s,h,p,d)
                        count("multiplicity_affine_value_checks")
                assert f[0]==(Q(0),Q(0))
                for comp in seg["all_pair_comparisons"]:
                    d,e=comp["d"],comp["e"]
                    aa,bb=f[d][0]-f[e][0],f[d][1]-f[e][1]
                    assert [aa,bb]==[Q(x) for x in comp["difference_affine"]]
                    values=[aa+bb*lo,aa+bb*hi]
                    assert values==[Q(x) for x in comp["endpoint_values"]]
                    assert all(v<0 for v in values)
                    assert comp["intersection"] is None
                    if bb: assert not lo<=-aa/bb<=hi
                    count("all_multiplicity_pair_segment_checks")
                for d in range(2,7):
                    for h in (lo,hi):
                        gap=fd(mode,delta,s,h,p,d)-fd(mode,delta,s,h,p,1)
                        assert gap>=Q(d-1)*Q(146807,414720)>0
                        min_gap=gap if min_gap is None else min(min_gap,gap)
                        count("strict_G_endpoint_comparisons")
                assert seg["open_G_multiplicities"]==[1]
                assert tuple(Q(x) for x in seg["G_affine"])==f[1]
            gap_report.append(dict(slice=sl["id"],exact_minimum_f_d_minus_f_1=min_gap,
                                   universal_bound_per_d_minus_1=Q(146807,414720),all_pair_intersections=0))
            for h in samples:
                for p in (0,1):
                    assert fd(mode,delta,s,h,p,0)==0
                    g=min(fd(mode,delta,s,h,p,d) for d in range(1,7))
                    g0=fd(mode,delta,s,Q(0),p,1)
                    predicted=g0-h if p==0 else g0-h/6-Q(5,6)*max(Q(0),h-H(mode,delta))
                    assert g==fd(mode,delta,s,h,p,1)==predicted
                    for mask in product((0,1),repeat=6):
                        d=sum(mask)
                        average=sum((direct_min(mode,delta,s,h,p,t,Q(d-t,5))[0] for t in mask),Q(0))/6
                        assert average==fd(mode,delta,s,h,p,d)
                        count("all_64_menu_average_checks")
                    count("closed_G_formula_checks")
    # The inner-five routing identity is checked for all 64 indexed menus.
    for mask in product((0,1),repeat=6):
        d=sum(mask)
        for k,t in enumerate(mask):
            assert Q(sum(mask[l] for l in range(6) if l!=k),5)==Q(d-t,5)
            assert Q(0)<=Q(d-t,5)<=Q(1)
            count("all_indexed_inner_query_checks")
    rows=json.loads((P/"exact_family.json").read_text())["rows"]
    row_index={r["id"]:r for r in rows}
    row_report=[]
    tradeoffs=[]
    for row in rows:
        sl=slices[row["slice_id"]]
        mode,delta,s=sl["mode"],Q(sl["delta"]),Q(sl["s"])
        h=Q(row["h"])
        kind,target=row["row_kind"],row["target"]
        expected=vec(mode,delta,s,h,kind,target)
        got=tuple(Q(x) for x in row["a"])
        assert got==expected and len(got)==513
        assert_metadata(row,sl)
        count("endpoint_row_columns",513)
        baseline=vec(mode,delta,s,Q(0),kind,target)
        change=tradeoff_vector(sl,kind,target,h)
        assert tuple(v-b for v,b in zip(expected,baseline))==change
        count("tradeoff_endpoint_identity_columns",513)
        if kind=="C-only":
            assert all(v>=0 for v in change)
            general=vec(mode,delta,s,h,"general","C")
            mu=pars(mode,delta,s,h)[6]-s/5
            ec=tuple(Q(v[8]) for v in CLIENTS)+(Q(-1),)
            assert expected==tuple(v+mu*e for v,e in zip(general,ec))
            count("C_free_equality_columns",513)
        row_report.append(dict(id=row["id"],columns=513,status="PASS"))
        tradeoffs.append(dict(id=row["id"],h=h,status="PASS",C_only_nonnegative_remainder=kind=="C-only"))
    affine=json.loads((P/"affine_family.json").read_text())["rows"]
    for seg in affine:
        sl=slices[seg["slice_id"]]
        mode,delta,s=sl["mode"],Q(sl["delta"]),Q(sl["s"])
        lo,hi=Q(seg["lo"]),Q(seg["hi"])
        kind,target=seg["row_kind"],seg["target"]
        aa=tuple(Q(x) for x in seg["intercept"])
        bb=tuple(Q(x) for x in seg["slope"])
        left=vec(mode,delta,s,lo,kind,target)
        right=vec(mode,delta,s,hi,kind,target)
        expected_slope=tuple((r-l)/(hi-lo) for l,r in zip(left,right))
        assert bb==expected_slope and aa==tuple(l-lo*b for l,b in zip(left,bb))
        assert left==tuple(Q(x) for x in row_index[seg["left_row_id"]]["a"])
        assert right==tuple(Q(x) for x in row_index[seg["right_row_id"]]["a"])
        count("affine_row_coefficient_checks",1026)
        h=(lo+hi)/2
        expected=vec(mode,delta,s,h,kind,target)
        assert expected==tuple(a+b*h for a,b in zip(aa,bb))
        assert expected==tuple((l+r)/2 for l,r in zip(left,right))
        baseline=vec(mode,delta,s,Q(0),kind,target)
        change=tradeoff_vector(sl,kind,target,h)
        assert tuple(v-b for v,b in zip(expected,baseline))==change
        count("affine_row_midpoint_columns",513)
        count("tradeoff_segment_identity_columns",513)
        if kind=="C-only": assert all(v>=0 for v in change)
    ordered_extra=[]
    for sl in slices.values():
        if sl["mode"]!="ordered": continue
        delta,s=Q(sl["delta"]),Q(sl["s"])
        points=[Q(x) for x in sl["common_breaks"]]
        h2,h1=points[1:3]
        baseline=vec("ordered",delta,s,Q(0),"ordered",None)
        at_h1=vec("ordered",delta,s,h1,"ordered",None)
        at_h2=vec("ordered",delta,s,h2,"ordered",None)
        w=h2/h1
        assert at_h2==tuple((1-w)*x+w*y for x,y in zip(baseline,at_h1))
        count("ordered_extra_conditional_breakpoint_identity_columns",513)
        ordered_extra.append(dict(slice=sl["id"],h2=h2,h1=h1,weight_at_zero=1-w,
                                  weight_at_h1=w,columns=513,status="PASS"))
    # Independent literal matches against the specified predecessor package.
    old=P.parent/"source2_conditional_redistribution"
    prior=[]
    for name in ("exact_family.json","epsilon_rows.json"):
        raw=json.loads((old/name).read_text())
        prior.extend(raw["rows"] if isinstance(raw,dict) else raw)
    prior_vectors={tuple(Q(x) for x in r["a"]) for r in prior}
    matched=[r for r in rows if tuple(Q(x) for x in r["a"]) in prior_vectors]
    assert len(matched)==60 and all(Q(r["h"])==0 for r in matched)
    assert sum(Q(r["h"])==0 for r in rows)==60
    assert len({tuple(r["a"]) for r in rows})==186
    for r in rows:
        if Q(r["h"])>0 and r["row_kind"]!="C-only":
            old_min=Q(1528993,497664) if r["mode"]=="pure" else Q(1300021,414720)
            assert Q(r["K"])<old_min
            count("positive_endpoint_K_below_prior_continuous_family")
    source_pins=json.loads((P/"source_pins.json").read_text())
    repo=P.parents[3]
    for pin in source_pins["files"]:
        assert sha(repo/pin["path"])==pin["sha256"]
    output("literal_dominance_intervals.json",dom_report)
    output("literal_weak_tables.json",weak_report)
    output("literal_segment_certificates.json",certificates)
    output("literal_strict_G_comparisons.json",gap_report)
    output("literal_row_checks.json",row_report)
    output("ordered_internal_breakpoint_identities.json",ordered_extra)
    output("tradeoff_identity_checks.json",dict(identities=tradeoffs,
        C_only_formula="R_C_only(h)=R_C_only(0)+h*M(p=0,c=0,o=1)+[h-H6]+*M(p=1,c=0,o=1)",
        pure_general_formula="R_T(h)=R_T(0)+h*(|T|-K)+h*M(p=0,t=0,o=1)+[h-H6]+*M(p=1,t=0,o=1)",
        ordered_formula="R_ord(h)=R_ord(0)-h*K+h*M(p=0,o=1)+(h/6+5*[h-H5]+/6)*M(p=1,o=1)"))
    output("redundancy_review.json",dict(previous_exact_rows=183,matched_h0_rows=60,
        positive_h_rows=126,positive_h_C_only_rows=12,positive_h_general_rows=96,positive_h_ordered_rows=18,
        total_distinct_endpoint_vectors=186,
        C_only_all_continuous_rows="old same-parameter h=0 row plus an explicitly nonnegative customer-mass vector",
        general_and_ordered="all positive endpoint K coefficients lie strictly below the minimum K coefficient of the corresponding prior delta-continuous raw family; no literal row coincidence",
        limit="No claim of nonnegative-cone independence from every existing inequality; no optimization or candidate point was used."))
    output("literal_checker_output.json",dict(status="PASS",counts=COUNTS,
        checked_endpoint_rows=len(rows),checked_affine_rows=len(affine),
        zero_length_intervals=sum(iv["interval"] is not None and iv["interval"][0]==iv["interval"][1] for iv in dom_report),
        source_pins_unchanged=True,optimization_calls=0,candidate_inputs_read=0))
    if not (P/"failure_log.json").exists(): output("failure_log.json",[])
    print(json.dumps(COUNTS,ensure_ascii=False,indent=2))


if __name__=="__main__":
    try:
        main()
    except BaseException as e:
        log=P/"failure_log.json"
        entries=json.loads(log.read_text()) if log.exists() else []
        entries.append(dict(stage="check_literal",type=type(e).__name__,message=str(e),traceback=traceback.format_exc()))
        output("failure_log.json",entries)
        raise
