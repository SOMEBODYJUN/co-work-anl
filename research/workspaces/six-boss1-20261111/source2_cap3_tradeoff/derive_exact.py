#!/usr/bin/env python3
"""COST-only exact derivation for the source-2 cap-3 tradeoff.

All arithmetic is Python-standard-library Fraction.  This program reads only
the two requested proof sources and the explicitly identified previous family;
it writes only beside itself.  It never reads an optimization input or result.
"""
from fractions import Fraction as F
from itertools import product, combinations
from pathlib import Path
import hashlib
import json
import traceback

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
OLD = HERE.parent / "source2_conditional_redistribution"
FORMAL = REPO / "archives/customer-attraction/state/引理/联合内部偏离的完整参数域与同菜单条件投影--引理.md"
TAILS = list(product((0, 1), repeat=4))
TYPES = list(product((0, 1), repeat=9))
TARGETS = [f"A{i}" for i in range(1, 7)] + ["X", "C"]
S_VALUES = [("s0", F(0)), ("sstar", F(61273, 6912)), ("s9", F(9))]
DELTA_VALUES = [("delta0", F(0)), ("deltaeps", F(1, 144))]


def js(v):
    if isinstance(v, F):
        return str(v)
    if isinstance(v, dict):
        return {str(k): js(x) for k, x in v.items()}
    if isinstance(v, (tuple, list)):
        return [js(x) for x in v]
    return v


def save(name, data):
    (HERE / name).write_text(json.dumps(js(data), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def tail_name(r):
    return "".join(map(str, r))


def weights(mode, delta, s, h=F(0)):
    q0 = F(1, 6 if mode == "pure" else 5)
    tau = [F(0), F(5977, 6912) - delta, F(43, 48) + delta]
    beta = [q0 / 2 + tau[j] + sum((q0 * tau[k] / ((4-k)*(5-k)) for k in range(j+1, 3)), F(0)) for j in range(3)]
    old_beta3 = beta[0]
    beta[0] -= h
    return dict(q0=q0, tau=tau, beta=beta, beta3_original=old_beta3,
                source_ic=25+sum(tau)-s, S=1+sum(beta))


def cost(w, p, t, q, r):
    load = p+t+sum(r)
    numerator = w["source_ic"]*t-r[3]-sum(w["tau"][j]*r[j] for j in range(3))
    assert load or not numerator
    return ((numerator/load if load else F(0))
            + sum(w["beta"][j]*r[j] for j in range(3)) + r[3]
            + q/(p+t+sum(r[:3])+1)
            + sum(w["tau"][j]*q/(p+t+sum(r[:j])+4-j) for j in range(3)))


def val(line, h):
    return line[0]+line[1]*h


def add_line(x, y):
    return (x[0]+y[0], x[1]+y[1])


def scale_line(x, k):
    return (k*x[0], k*x[1])


def min_at(lines, h):
    values = {r: val(line, h) for r, line in lines.items()}
    m = min(values.values())
    return m, [r for r in values if values[r] == m]


def envelope(lines, top):
    # Derive through ALL pair intersections; the checker uses half-intervals.
    crossings = {F(0), top}
    for x, y in combinations(lines.values(), 2):
        if x[1] != y[1]:
            h = (y[0]-x[0])/(x[1]-y[1])
            if 0 <= h <= top:
                crossings.add(h)
    candidate = sorted(crossings)
    at = {h: min_at(lines, h) for h in candidate}
    breaks = {F(0), top}
    for h, (_, active) in at.items():
        if len({lines[r][1] for r in active}) > 1:
            breaks.add(h)
    breaks = sorted(breaks)
    intervals = []
    for r, line in lines.items():
        active_points = [h for h in candidate if r in at[h][1]]
        dom = [min(active_points), max(active_points)] if active_points else None
        intervals.append(dict(tail=r, intercept=line[0], slope=line[1],
                              weak_minimum_interval=dom,
                              zero_length=bool(dom is not None and dom[0] == dom[1])))
    segments = []
    for lo, hi in zip(breaks, breaks[1:]):
        _, active = min_at(lines, (lo+hi)/2)
        line = lines[active[0]]
        assert all(lines[r] == line for r in active)
        differences = {r: [val(x, lo)-val(line, lo), val(x, hi)-val(line, hi)] for r, x in lines.items()}
        assert all(z >= 0 for pair in differences.values() for z in pair)
        segments.append(dict(lo=lo, hi=hi, minimum_affine=line,
                             open_active_tails=active, all_tail_endpoint_gaps=differences))
    endpoints = [dict(h=h, value=min_at(lines, h)[0], active_tails=min_at(lines, h)[1]) for h in breaks]
    group_min = [min(line[0] for r, line in lines.items() if int(r[0]) == bit) for bit in (0, 1)]
    group_active = [[r for r, line in lines.items() if int(r[0]) == bit and line[0] == group_min[bit]] for bit in (0, 1)]
    return dict(all_pair_candidate_count=len(candidate), breaks=breaks,
                group_min_at_zero=group_min, group_active_tails=group_active,
                kappa=max(F(0), group_min[1]-group_min[0]),
                tails=intervals, endpoints=endpoints, segments=segments)


def condition_key(p, t, n):
    return f"p{p}_t{t}_n{n}"


def make_conditions(mode, delta, s):
    w = weights(mode, delta, s)
    out = []
    for p, t in product((0, 1), repeat=2):
        ns = range(2) if mode == "pure" else (range(0, 6) if t == 0 else range(1, 7))
        for n in ns:
            q = F(n, 6) if mode == "pure" else F(n-t, 5)
            lines = {tail_name(r): (cost(w, p, t, q, r), -F(r[0])) for r in TAILS}
            env = envelope(lines, w["beta3_original"])
            out.append(dict(key=condition_key(p, t, n), p=p, t=t, n=n,
                            n_meaning="o" if mode == "pure" else "d", q=q, **env))
    return out


def condition_lines(condition):
    return {r["tail"]: (r["intercept"], r["slope"]) for r in condition["tails"]}


def active_line(condition, h):
    lines = condition_lines(condition)
    _, active = min_at(lines, h)
    return lines[active[0]]


def m_value(conditions, p, t, n, h):
    return min_at(condition_lines(conditions[condition_key(p, t, n)]), h)[0]


def multiplicities(conditions, breaks):
    # All six f_d are constructed first. No multiplicity is preselected.
    records = []
    extra_breaks = set()
    for lo, hi in zip(breaks, breaks[1:]):
        mid = (lo+hi)/2
        for p in (0, 1):
            f = {}
            for d in range(7):
                line = (F(0), F(0))
                if d < 6:
                    line = add_line(line, scale_line(active_line(conditions[condition_key(p, 0, d)], mid), F(6-d, 6)))
                if d > 0:
                    line = add_line(line, scale_line(active_line(conditions[condition_key(p, 1, d)], mid), F(d, 6)))
                f[d] = line
            pair_records = []
            for d, e in combinations(range(1, 7), 2):
                diff = (f[d][0]-f[e][0], f[d][1]-f[e][1])
                cross = None
                if diff[1]:
                    h = -diff[0]/diff[1]
                    if lo <= h <= hi:
                        cross = h
                        if lo < h < hi:
                            extra_breaks.add(h)
                elif diff[0] == 0:
                    cross = "whole_interval"
                pair_records.append(dict(d=d, e=e, difference_affine=diff,
                                         endpoint_values=[val(diff, lo), val(diff, hi)], intersection=cross))
            best = min(val(f[d], mid) for d in range(1, 7))
            act = [d for d in range(1, 7) if val(f[d], mid) == best]
            g = f[act[0]]
            records.append(dict(p=p, lo=lo, hi=hi, f_affines=f, all_pair_comparisons=pair_records,
                                G_affine=g, open_G_multiplicities=act,
                                all_G_endpoint_gaps={d:[val(f[d],lo)-val(g,lo),val(f[d],hi)-val(g,hi)] for d in range(1,7)}))
    return records, extra_breaks


def f_values(conditions, p, h):
    result = {}
    for d in range(7):
        value = F(0)
        if d < 6:
            value += F(6-d,6)*m_value(conditions,p,0,d,h)
        if d > 0:
            value += F(d,6)*m_value(conditions,p,1,d,h)
        result[d] = value
    return result


def row_values(slice_data, kind, target, h):
    mode, delta, s = slice_data["mode"], slice_data["delta"], slice_data["s"]
    w = weights(mode, delta, s, h)
    cond = {c["key"]: c for c in slice_data["conditions"]}
    is_c = kind == "C-only"
    mu = w["S"]-s/5 if is_c else F(0)
    if mode == "pure":
        mm = {(p,t,o):m_value(cond,p,t,o,h) for p,t,o in product((0,1),repeat=3)}
        tidx = TARGETS.index(target) if target in TARGETS else None
        if target == "C":
            tidx = 8
    else:
        gg = {p:min(v for d,v in f_values(cond,p,h).items() if d > 0) for p in (0,1)}
    values=[]
    for bits in TYPES:
        a6=bits[:6]
        actual=F(bits[1],sum(a6)) if sum(a6) else F(0)
        sub=mm[(bits[0],bits[tidx],bits[7])] if mode=="pure" else bits[7]*gg[bits[0]]
        values.append(w["source_ic"]*actual-sub+mu*bits[8])
    values.append(w["S"]-mu)
    return values


def row_metadata(slice_data, kind, target, h):
    w=weights(slice_data["mode"],slice_data["delta"],slice_data["s"],h)
    mu=w["S"]-slice_data["s"]/5 if kind=="C-only" else F(0)
    return dict(slice_id=slice_data["id"],mode=slice_data["mode"],row_kind=kind,target=target,
                source=2,delta=slice_data["delta"],s=slice_data["s"],h=h,
                q0=w["q0"],tau={str(j+3):v for j,v in enumerate(w["tau"])},
                beta_original={str(j+3):v+(h if j==0 else 0) for j,v in enumerate(w["beta"])},
                beta_actual={str(j+3):v for j,v in enumerate(w["beta"])},
                real_budget=dict(source_IC=w["source_ic"],intermediate_CAP={str(j+3):v for j,v in enumerate(w["beta"])},
                                 terminal_CAP=F(1),terminal_BR=F(1),internal_SAFE={str(j+3):v for j,v in enumerate(w["tau"])},
                                 outer_average=F(1,6) if slice_data["mode"]=="ordered" else None,
                                 inner_query_average=F(1,5) if slice_data["mode"]=="ordered" else F(1,6)),
                raw_K=w["S"],K=w["S"]-mu,free_EC=mu,equality_definition="E_C=sum_x c_x-K=0",
                numerical_divisor=F(25),column_count=513,
                customer_formula="a*actual_u2-m(p,t,o/6)+free_EC*c" if slice_data["mode"]=="pure" else "a*actual_u2-o*G(p)")


def make_slice(mode, dn, delta, sn, s):
    w = weights(mode, delta, s)
    conditions = make_conditions(mode,delta,s)
    common=sorted({b for c in conditions for b in c["breaks"]})
    index={c["key"]:c for c in conditions}
    multi=[]
    if mode=="ordered":
        multi,extra=multiplicities(index,common)
        if extra:
            common=sorted(set(common)|extra)
            multi,extra2=multiplicities(index,common)
            assert not extra2
    return dict(id=f"{mode}_{dn}_{sn}",mode=mode,delta=delta,s=s,q0=w["q0"],
                h_domain=[F(0),w["beta3_original"]],weights_at_zero=w,
                conditions=conditions,common_breaks=common,multiplicity_segments=multi,
                multiplicity_endpoints=[dict(h=h,p=p,f=f_values(index,p,h),
                                            G=min(f_values(index,p,h)[d] for d in range(1,7)),
                                            active_d=[d for d in range(1,7) if f_values(index,p,h)[d]==min(f_values(index,p,h)[e] for e in range(1,7))])
                                        for h in common for p in (0,1)] if mode=="ordered" else [])


def main():
    assert not (HERE/"freeze_manifest.json").exists(), "Frozen package: replay in a separate copy."
    input_files=[FORMAL,OLD/"proof.md",OLD/"exact_family.json",OLD/"epsilon_rows.json"]
    pins=[dict(path=str(p.relative_to(REPO)),sha256=digest(p),bytes=p.stat().st_size) for p in input_files]
    save("source_pins.json",dict(agent_id="/root/source2_cap3_tradeoff",run="six-boss1-20261111",files=pins,
                                 mandatory_full_reads=["formal lemma sections 2 and 8","source2_conditional_redistribution/proof.md"],
                                 forbidden_inputs_read=False))
    slices=[make_slice(mode,dn,delta,sn,s) for mode in ("pure","ordered") for dn,delta in DELTA_VALUES for sn,s in S_VALUES]
    save("exact_envelopes.json",dict(schema="source2-cap3-envelopes-v1",tail_order="r3,r4,r5,z",slices=slices))
    save("coordinate_contract.json",dict(customer_bits=[f"a{i}" for i in range(1,7)]+["x","o","c"],
                                        order="lexicographic with 0 before 1",customer_column_count=512,
                                        K_column=512,total_columns=513,inequality="dot(row.a,coordinates)>=0",
                                        actual_u2="a2/(a1+...+a6), with zero actual load giving zero",
                                        rows_keep_zero_types=True,rows_keep_repeated_sources=True,
                                        source_id="/root/source2_cap3_tradeoff",run="six-boss1-20261111"))
    rows=[]
    affine=[]
    for sl in slices:
        specs=[("general",t) for t in TARGETS]+[("C-only","C")] if sl["mode"]=="pure" else [("ordered",None)]
        for k,h in enumerate(sl["common_breaks"]):
            for kind,target in specs:
                row=dict(id=f"{sl['id']}_h{k}_{kind}_{target or 'menu'}",**row_metadata(sl,kind,target,h))
                row["a"]=row_values(sl,kind,target,h)
                rows.append(row)
        for k,(lo,hi) in enumerate(zip(sl["common_breaks"],sl["common_breaks"][1:])):
            for kind,target in specs:
                left=row_values(sl,kind,target,lo)
                right=row_values(sl,kind,target,hi)
                slope=[(r-l)/(hi-lo) for l,r in zip(left,right)]
                intercept=[l-lo*b for l,b in zip(left,slope)]
                affine.append(dict(id=f"{sl['id']}_segment{k}_{kind}_{target or 'menu'}",slice_id=sl["id"],
                                   row_kind=kind,target=target,lo=lo,hi=hi,intercept=intercept,slope=slope,
                                   left_row_id=f"{sl['id']}_h{k}_{kind}_{target or 'menu'}",
                                   right_row_id=f"{sl['id']}_h{k+1}_{kind}_{target or 'menu'}",
                                   interpolation="R(h)=((hi-h)*R(lo)+(h-lo)*R(hi))/(hi-lo)"))
    save("exact_family.json",dict(schema="source2-cap3-513-v1",rows=rows))
    save("affine_family.json",dict(schema="source2-cap3-affine-513-v1",rows=affine))
    # Explicit exact comparison with the specified predecessor only.
    previous=[]
    for name in ("exact_family.json","epsilon_rows.json"):
        raw=json.loads((OLD/name).read_text())
        rs=raw["rows"] if isinstance(raw,dict) else raw
        previous.extend((name,r) for r in rs)
    prior_index={tuple(F(x) for x in r["a"]):(name,r.get("id")) for name,r in previous}
    matches=[]
    for row in rows:
        hit=prior_index.get(tuple(row["a"]))
        matches.append(dict(row_id=row["id"],h=row["h"],exact_previous_match=hit))
    save("previous_exact_matches.json",dict(previous_rows=len(previous),comparisons=matches,
                                            matched_rows=sum(m["exact_previous_match"] is not None for m in matches),
                                            note="Literal full-column comparison only; it is not a cone-independence test."))
    stat=dict(slices=len(slices),conditions=sum(len(sl["conditions"]) for sl in slices),
              tail_affines=sum(16*len(sl["conditions"]) for sl in slices),
              zero_length_tail_intervals=sum(r["zero_length"] for sl in slices for c in sl["conditions"] for r in c["tails"]),
              endpoint_rows=len(rows),affine_rows=len(affine),
              distinct_endpoint_vectors=len({tuple(r["a"]) for r in rows}),
              per_slice=[dict(id=sl["id"],breaks=sl["common_breaks"],
                              endpoint_rows=len(sl["common_breaks"])*(9 if sl["mode"]=="pure" else 1),
                              multiplicity_pair_intersections=[p for seg in sl["multiplicity_segments"] for p in seg["all_pair_comparisons"] if p["intersection"] is not None]) for sl in slices])
    save("derivation_summary.json",stat)
    assert all(digest(REPO/p["path"])==p["sha256"] for p in pins)
    print(json.dumps(js(stat),ensure_ascii=False,indent=2))


if __name__=="__main__":
    try:
        main()
    except BaseException as e:
        path=HERE/"failure_log.json"
        old=json.loads(path.read_text()) if path.exists() else []
        old.append(dict(stage="derive_exact",type=type(e).__name__,message=str(e),traceback=traceback.format_exc()))
        save("failure_log.json",old)
        raise
