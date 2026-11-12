#!/usr/bin/env python3
"""Exact later-source anchor cells; no optimizer and no global data access.

Coordinates are (tau_(i+1), ..., tau_5, lambda).  Every real local
state and every closed-window occurrence is retained before proportional
halfspace grouping.  This program obtains vertices by boundary intersections.
"""
from fractions import Fraction as F
from itertools import product, combinations
from functools import reduce
from math import gcd, lcm
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
WS = "research/workspaces/six-boss1-20261111"
SOURCE_PATHS = [
    "archives/customer-attraction/state/定义/共同目录完整历史模型--定义.md",
    WS + "/all_source_minimal_cap_safe/proof.md",
    WS + "/ordered_minimal_cap/proof.md",
    WS + "/source2_lambda_strip/proof.md",
    WS + "/source2_lambda_strip/freeze_manifest.json",
    WS + "/all_source_minimal_cap_safe/parameter_domains.json",
    WS + "/all_source_minimal_cap_safe/exact_family.json",
    WS + "/ordered_minimal_cap/parameter_domains.json",
    WS + "/ordered_minimal_cap/exact_family.json",
]
EXPECTED_STRIP = "a3f42d72be4ebecd15f8f74315103ae90bb940d4031fa712211219e2c75f96a4"


def dump(name, data):
    (HERE / name).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")


def string_vector(x):
    return [str(v) for v in x]


def pin_sources():
    out = []
    for rel in SOURCE_PATHS:
        data = (ROOT / rel).read_bytes()
        item = dict(repository_relative_path=rel, sha256=hashlib.sha256(data).hexdigest(), bytes=len(data))
        if rel.endswith("source2_lambda_strip/freeze_manifest.json"):
            assert item["sha256"] == EXPECTED_STRIP
        out.append(item)
    return out


def rank(rows):
    if not rows:
        return 0
    a = [list(map(F, row)) for row in rows]
    nr, nc, r = len(a), len(a[0]), 0
    for c in range(nc):
        pivot = next((k for k in range(r, nr) if a[k][c]), None)
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        v = a[r][c]
        a[r] = [x / v for x in a[r]]
        for k in range(r + 1, nr):
            if a[k][c]:
                z = a[k][c]
                a[k] = [x - z * y for x, y in zip(a[k], a[r])]
        r += 1
        if r == nr:
            break
    return r


def solve_boundaries(forms, d):
    a = [[*h[1:], -h[0]] for h in forms]
    for c in range(d):
        pivot = next((k for k in range(c, d) if a[k][c]), None)
        if pivot is None:
            return None
        a[c], a[pivot] = a[pivot], a[c]
        z = a[c][c]
        a[c] = [v / z for v in a[c]]
        for r in range(d):
            if r != c and a[r][c]:
                z = a[r][c]
                a[r] = [x - z * y for x, y in zip(a[r], a[c])]
    return tuple(a[k][-1] for k in range(d))


def value(h, x):
    return h[0] + sum((a * b for a, b in zip(h[1:], x)), F(0))


def affine(fn, dim):
    zero = [F(0)] * dim
    const = fn(zero)
    return tuple([const] + [fn([F(k == j) for k in range(dim)]) - const for j in range(dim)])


def primitive(form):
    den = lcm(*(x.denominator for x in form))
    ints = [int(x * den) for x in form]
    div = reduce(gcd, (abs(x) for x in ints), 0)
    if not div:
        return tuple(ints), F(0)
    return tuple(x // div for x in ints), F(div, den)


def weights(i, q0, x):
    js = list(range(i + 1, 6))
    tau = dict(zip(js, x[:-1]))
    beta = {j: q0 / 2 + tau[j] + sum((q0 * tau[k] / ((7-k)*(8-k)) for k in js if k > j), F(0)) for j in js}
    return tau, beta, x[-1] + sum(tau.values(), F(0)), F(1) + sum(beta.values(), F(0))


def actual_cost(i, q0, x, p, t, q, r):
    tau, beta, a, _ = weights(i, q0, x)
    js = list(tau)
    z, load = r[-1], p + t + sum(r)
    actual = (a * t - z - sum((tau[j] * r[k] for k, j in enumerate(js)), F(0))) / load if load else F(0)
    caps = sum((beta[j] * r[k] for k, j in enumerate(js)), F(0)) + z
    query = q / (p + t + sum(r[:-1]) + 1)
    query += sum((tau[j] * q / (p + t + sum(r[:k]) + 7 - j) for k, j in enumerate(js)), F(0))
    return actual + caps + query


def w(lam, D):
    return min(lam / (D - 1), F(1) + (lam - 1) / D)


def anchor(i, q0, x, p):
    _, beta, _, _ = weights(i, q0, x)
    return sum(beta.values(), F(0)) + w(x[-1], p + 7 - i)


def make_cell(i, q0, lo, hi):
    js = list(range(i + 1, 6))
    d = len(js) + 1
    cid = f"I{i}_Q{q0.denominator}_L{lo}_{hi}"
    midpoint = F(lo + hi, 2)
    raw = []
    for p in range(i):
        D = p + 7 - i
        az = int(midpoint > (D - 1) ** 2)
        for r in product((0, 1), repeat=6-i):
            missing = [j for j, present in zip(js, r[:-1]) if not present]
            def remainder(x, p=p, r=r, D=D, az=az):
                _, beta, _, _ = weights(i, q0, x)
                wa = x[-1] / (D - 1) if az == 0 else F(1) + (x[-1] - 1) / D
                return actual_cost(i, q0, x, p, 1, F(0), r) - sum(beta.values(), F(0)) - wa
            form = affine(remainder, d)
            raw.append(dict(id=f"{cid}_P{p}_R{''.join(map(str,r))}", kind="true_t1_q0_state", p=p, D=D, missing_sources=missing,
                            tail=list(r), terminal=r[-1], anchor_terminal_on_window_interior=az, form=string_vector(form)))
    for k, j in enumerate(js):
        f = [F(0)] * (d+1)
        f[k+1] = F(1)
        raw.append(dict(id=f"{cid}_TAU{j}_NONNEG", kind="nonnegative_internal_SAFE_weight", form=string_vector(f)))
    for tag, constant, slope in [("LOW", -lo, 1), ("HIGH", hi, -1)]:
        f = [F(constant)] + [F(0)] * (d-1) + [F(slope)]
        raw.append(dict(id=f"{cid}_WINDOW_{tag}", kind="closed_research_window", form=string_vector(f)))
    grouped = {}
    for row in raw:
        h = tuple(map(F, row["form"]))
        key, scale = primitive(h)
        row["primitive_form"] = list(key)
        row["positive_scale_to_primitive"] = str(scale)
        grouped.setdefault(key, []).append(row["id"])
    groups = []
    for k, (prim, rawids) in enumerate(sorted(grouped.items())):
        groups.append(dict(id=f"{cid}_H{k:03}", primitive_form=list(prim), raw_ids=rawids,
                           is_identically_zero=not any(prim), is_constant=not any(prim[1:])))
    nonconstant = [g for g in groups if not g["is_constant"]]
    forms = [tuple(map(F, g["primitive_form"])) for g in nonconstant]
    assert all(g["primitive_form"][0] >= 0 for g in groups if g["is_constant"])
    vertices = set()
    checked = 0
    for ix in combinations(range(len(forms)), d):
        checked += 1
        x = solve_boundaries([forms[k] for k in ix], d)
        if x is not None and all(value(h, x) >= 0 for h in forms):
            vertices.add(x)
    verts = sorted(vertices)
    assert verts and rank([[x[k]-verts[0][k] for k in range(d)] for x in verts[1:]]) == d
    vrows = []
    for k, x in enumerate(verts):
        active = [g["id"] for g, h in zip(nonconstant, forms) if value(h, x) == 0]
        active_basis = next(c for c in combinations(active, d) if rank([forms[[g["id"] for g in nonconstant].index(g)][1:] for g in c]) == d)
        lam = x[-1]
        vrows.append(dict(id=f"{cid}_V{k:03}", coordinates=string_vector(x), lambda_value=str(lam),
                          active_primitive_halfspaces=active, active_independent_basis=list(active_basis),
                          all_query_zero_attaining_tails={str(p): [list(r) for r in product((0,1), repeat=6-i)
                              if actual_cost(i,q0,x,p,1,F(0),r) == anchor(i,q0,x,p)] for p in range(i)},
                          old_16_25_parameter=lam >= 16))
    facets, witnesses = [], []
    for g, h in zip(nonconstant, forms):
        ids = [k for k, x in enumerate(verts) if value(h, x) == 0]
        ar = rank([[verts[k][j]-verts[ids[0]][j] for j in range(d)] for k in ids[1:]]) if ids else -1
        g["support_vertex_ids"] = [vrows[k]["id"] for k in ids]
        g["support_affine_rank"] = ar
        g["is_facet"] = ar == d - 1
        if g["is_facet"]:
            facets.append(dict(g))
    for g in facets:
        h = tuple(map(F, g["primitive_form"]))
        faceverts = [verts[k] for k, v in enumerate(vrows) if v["id"] in g["support_vertex_ids"]]
        center = tuple(sum((x[j] for x in faceverts), F(0))/len(faceverts) for j in range(d))
        direction = tuple(-v for v in h[1:])
        steps = [F(1)]
        for other in facets:
            if other["id"] == g["id"]:
                continue
            oh = tuple(map(F, other["primitive_form"]))
            slack, derivative = value(oh, center), sum((a*b for a,b in zip(oh[1:],direction)),F(0))
            assert slack > 0
            if derivative < 0:
                steps.append(slack/(-2*derivative))
        step = min(steps)
        point = tuple(a+step*b for a,b in zip(center,direction))
        assert value(h, point) < 0
        witnesses.append(dict(cell=cid, facet_id=g["id"], point=string_vector(point), violated_slack=str(value(h,point)),
                              other_facet_slacks={o["id"]:str(value(tuple(map(F,o["primitive_form"])),point)) for o in facets if o["id"]!=g["id"]},
                              raw_sources=g["raw_ids"]))
    # All nonfacet constraints are directly checked at all complete vertices.
    for row in raw:
        assert all(value(tuple(map(F,row["form"])),x)>=0 for x in verts)
    ub = (F(4,5)-q0/2)/F(4,5)
    assert all(all(F(0)<=t<=ub for t in x[:-1]) and lo<=x[-1]<=hi for x in verts)
    cell = dict(id=cid, source=i, q0=str(q0), coordinate_order=[f"tau{j}" for j in js]+["lambda"],
                dimension=d, window=[str(lo),str(hi)], D_values=list(range(7-i,7)),
                bounded_box_tau_upper=str(ub), raw_constraint_count=len(raw), raw_real_state_count=i*2**(6-i),
                primitive_halfspace_count=len(groups), nonconstant_halfspace_count=len(nonconstant),
                facet_count=len(facets), vertex_count=len(verts), complete_boundary_combinations=checked,
                halfspaces=groups, facets=facets, vertices=vrows,
                strict_interior_point=string_vector(tuple(sum((x[j] for x in verts),F(0))/len(verts) for j in range(d))),
                old_window=lo==16, old_parameter_substitution="s=25-lambda" if lo==16 else None)
    return cell, raw, witnesses


def main():
    pins = pin_sources()
    dump("source_pins.json", pins)
    inputs = dict(sources=[3,4,5], q0=["1/6","1/5"], lambda_window=["0","25"],
                  windows={"3":[[0,9],[9,16],[16,25]],"4":[[0,4],[4,9],[9,16],[16,25]],"5":[[0,1],[1,4],[4,9],[9,16],[16,25]]},
                  coordinate_order="tau in increasing true source index, then lambda",
                  inequality_convention="constant plus coefficients dot coordinates >= 0",
                  zero_load_actual_share="0", raw_window_and_vertex_duplicates="retain all", optimizer_calls=0,
                  global_LP_inputs_points_faces_read=False, current_3056_plan_modified=False)
    dump("inputs.json",inputs)
    cells, states, witnesses = [], [], []
    for i in inputs["sources"]:
        for q0 in map(F, inputs["q0"]):
            for lo,hi in inputs["windows"][str(i)]:
                c, s, wits = make_cell(i,q0,lo,hi)
                cells.append(c); states.extend(s); witnesses.extend(wits)
                print(c["id"],"facets",c["facet_count"],"vertices",c["vertex_count"],flush=True)
    occurrences = {}
    for c in cells:
        for v in c["vertices"]:
            key=(c["source"],c["q0"],tuple(v["coordinates"]))
            occurrences.setdefault(key,[]).append(dict(cell=c["id"],vertex_id=v["id"]))
    dump("parameter_domains.json",dict(schema="later-source-complete-anchor-cells/v1",cells=cells,
         complete_from_all_real_state_halfspaces=True, retained_closed_window_occurrences=True,optimizer_calls=0))
    dump("state_halfspaces.json",dict(halfspace_convention=inputs["inequality_convention"],raw=states))
    dump("necessary_facet_witnesses.json",witnesses)
    dump("parameter_occurrences.json",[dict(source=k[0],q0=k[1],coordinates=list(k[2]),occurrences=v) for k,v in occurrences.items()])
    summary=dict(status="PASS",cells=len(cells),raw_real_states=sum(c["raw_real_state_count"] for c in cells),
                 raw_constraints=len(states),primitive_groups=sum(c["primitive_halfspace_count"] for c in cells),
                 facets=sum(c["facet_count"] for c in cells),vertex_occurrences=sum(c["vertex_count"] for c in cells),
                 unique_parameters=len(occurrences),all_boundary_combinations=sum(c["complete_boundary_combinations"] for c in cells),
                 old_window_vertex_occurrences=sum(c["vertex_count"] for c in cells if c["old_window"]),
                 sources_unchanged=pin_sources()==pins,optimizer_calls=0)
    assert summary["sources_unchanged"]
    dump("geometry_generator_output.json",summary)
    print(json.dumps(summary,ensure_ascii=False),flush=True)


if __name__ == "__main__":
    main()
