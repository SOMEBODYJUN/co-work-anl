"""Replay all fixed candidate rows exactly, check the source matrix and build its menu."""
import ast
import csv
import hashlib
from fractions import Fraction as F
from itertools import combinations_with_replacement, product
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
PREV = HERE.parents[1] / "n6-boss3-20261118" / "informed-a"
CAND = "A-two-response-rational-candidate.json"
PROBE = "probe_A_two_response.py"
PINS = {
    CAND: "80784538f0472beb93eff51d43747eab7761c978cc3478faacf046c6b0fe5618",
    PROBE: "b7f88636c137f2dae60507bcf6e8e8f2e9415a49d923976719ea9ee9c4806f48",
    "A-two-response-probe-output.json": "5b26e86598225725969a73d4b92694c0628938ae3042bf8fcd5241a4890f5cd9",
    "A-two-response-checkpoint-r1.md": "332b2da4283720e34fc779d03e04cfcad82169c6637a746efae2509e91164af5",
}
LABELS = tuple(f"T{k}" for k in range(6)) + tuple(f"F{k}" for k in range(5))
TYPES = [(b, v) for b in range(7) for v in product((0, 1), repeat=5) if b < 6 or any(v)]
PATTERN = ((0,1,2), (0,2,1), (1,3,4), (1,4,3))


def read_point():
    manifest = json.loads((PREV / "A-two-response-checkpoint-r1-manifest.json").read_text())
    for name, expected in PINS.items():
        assert hashlib.sha256((PREV / name).read_bytes()).hexdigest() == manifest[name] == expected
    point = json.loads((PREV / CAND).read_text())
    assert point["source_sha256"] == PINS["A-two-response-probe-output.json"]
    assert tuple(tuple(x) for x in point["pattern"]) == PATTERN
    k = point["candidate_integer_scale_K"]
    gamma = F(point["gamma"])
    assert k > 0 and gamma * k == F(point["candidate_gamma_in_integer_scale"])
    counts, masses = {}, {}
    for a in point["atoms"]:
        t = (a["block"], tuple(a["bits"]))
        assert t in TYPES and t not in masses
        m, n = F(a["mass"]), a["integer_count"]
        assert isinstance(n, int) and n > 0 and m == F(n, k)
        counts[t], masses[t] = n, m
    return point, k, gamma, counts, masses


def branches_coefficients(block, bits):
    """Return one coefficient per row for one unit atom in original row order."""
    covers = tuple(int(block == i) for i in range(6)) + bits
    for f, present in enumerate(bits):
        yield f"extra-cap-{f}", F(present), F(1)
    query_names = [str(k) for k in range(6)] + [str(("F", k)) for k in range(5)]
    for j, (e, a, y) in enumerate(PATTERN):
        prefix = covers[4] + covers[5] + covers[j]
        final = prefix + bits[e] + bits[a] + bits[y]
        name = f"branch{j}-"

        def actual(member):
            return F(member, final) if member else F(0)
        u4, u5, u6 = map(actual, (bits[e], bits[a], bits[y]))
        yield name+"force-at-most-gamma", actual(covers[j]), F(0)
        yield name+"fourth-clean-1/2", -u4, F(-1, 2)
        yield name+"fifth-7/12", -u5, F(-7, 12)
        yield name+"sixth-7/12", -u6, F(-7, 12)
        for label, member in zip(query_names, covers):
            yield name+"fourth-H-"+label, F(member, prefix+3)-u4, F(0)
        for label, member in zip(query_names, covers):
            yield name+"last-query-"+label, F(member, prefix+bits[e]+bits[a]+1)-u6, F(0)
        for label, member in zip(query_names, covers):
            yield name+"fifth-H-"+label, F(member, prefix+bits[e]+2)-u5, F(0)
        for t in range(4):
            if t != j:
                at_t = covers[t] * bits[e]
                other = sum(covers[l]*bits[e] for l in range(4) if l not in (j, t))
                yield name+f"fifth-anchor-deficit-{t}", -u5-F(at_t,2)-F(other,4), F(-1)
        for t, q in product(range(5), repeat=2):
            lead_alone = F(bits[t], prefix+bits[e]+1)
            last_query = F(bits[q], prefix+bits[e]+bits[t]+1)
            yield name+f"fifth-TQ-{t}-{q}", lead_alone+last_query-u5, F(1)


def legacy_exact_rows():
    """Extract only the pinned original matrix builder. Replace float by Fraction."""
    import numpy as np
    run = next(n for n in ast.parse((PREV/PROBE).read_text()).body
               if isinstance(n, ast.FunctionDef) and n.name == "run")
    stop = next(i for i, node in enumerate(run.body) if isinstance(node, ast.Assign)
                and isinstance(node.targets[0], ast.Name) and node.targets[0].id == "c")
    run.body = run.body[:stop] + [ast.parse("return names, rows, rhs, eq").body[0]]
    for node in ast.walk(run):
        if isinstance(node, ast.Constant) and type(node.value) is float:
            assert node.value.is_integer()
            node.value = int(node.value)

    class ExactArrays:
        array = staticmethod(lambda entries: np.array(entries, dtype=object))
        zeros = staticmethod(lambda n: np.zeros(n, dtype=object))
    env = {"np": ExactArrays, "TYPES": TYPES, "F": F, "product": product, "float": F}
    module = ast.fix_missing_locations(ast.Module(body=[run], type_ignores=[]))
    exec(compile(module, str(PREV/PROBE), "exec"), env)
    return env["run"](PATTERN)


def audit_rows(k, gamma, masses):
    cols = [list(branches_coefficients(*t)) for t in TYPES]
    names, rows, rhs, eq = legacy_exact_rows()
    assert len(cols) == 223 and len(names) == len(set(names)) == len(rows) == len(rhs) == 265
    assert len(eq) == 6 and all(len(row) == 224 for row in [*eq, *rows])
    fields = ["kind", "name", "lhs", "relation", "rhs", "slack", "slack_in_clients"]
    ledger, binding = [], []
    for i, (name, row, bound) in enumerate(zip(names, rows, rhs)):
        coeff = [col[i][1] for col in cols] + [-int(name.endswith("force-at-most-gamma"))]
        assert all(col[i][0] == name and col[i][2] == bound for col in cols)
        assert all(isinstance(y, (F, int)) and y == x for x,y in zip(coeff, row))
        left = sum(a*masses.get(t,0) for a,t in zip(coeff,TYPES)) + coeff[-1]*gamma
        slack = bound-left
        assert slack >= 0, (name, slack)
        if slack == 0:
            binding.append(name)
        ledger.append(["inequality", name, left, "<=", bound, slack, k*slack])
    for b, row in enumerate(eq):
        expected = [int(block == b) for block, _ in TYPES] + [0]
        assert expected == list(row)
        left = sum(masses.get(t,0) for t in TYPES if t[0] == b)
        assert left == 1
        ledger.append(["equality", f"anchor-mass-{b}", left, "=", 1, 0, 0])
    assert gamma >= 0 and all(masses.get(t,0) >= 0 for t in TYPES)
    previous = json.loads((PREV/"A-two-response-probe-output.json").read_text())["two_two_response"]
    assert binding == previous["active_rows"]
    with (HERE/"necessary-rows.csv").open("w", newline="") as f:
        writer=csv.writer(f, lineterminator="\n")
        writer.writerow(fields)
        writer.writerows(ledger)
    return {
        "types": len(TYPES), "columns_including_gamma": len(TYPES)+1,
        "nonnegative_coordinates_checked": len(TYPES)+1,
        "strictly_positive_atom_count": len(masses),
        "inequalities": len(rows), "anchor_equalities": len(eq),
        "exact_coefficients_compared_including_equalities": (len(rows)+len(eq))*(len(TYPES)+1),
        "exact_inequality_rhs_compared": len(rhs),
        "active_inequalities": len(binding),
        "min_inequality_slack": str(min(x[5] for x in ledger[:len(names)])),
        "min_positive_inequality_slack": str(min(x[5] for x in ledger[:len(names)] if x[5]>0)),
        "all_original_float_active_names_agree_with_exact_zero": True,
        "gamma": str(gamma), "K": k, "gamma_times_K": str(gamma*k),
        "strict_distance_below_half": str(F(1,2)-gamma),
    }


def build_menu(k, point, counts):
    """Disjoint intervals name the unit clients. Explicit finite sets audit unions."""
    intervals, covers = [], [0]*len(LABELS)
    n = 0
    for (block,bits), count in sorted(counts.items()):
        members = ([block] if block<6 else [])+[6+i for i,x in enumerate(bits) if x]
        clients = ((1<<count)-1)<<n
        intervals.append({"first":n,"end_exclusive":n+count,"labels":[LABELS[a] for a in members]})
        for a in members:
            covers[a] |= clients
        n += count
    assert len(set(covers)) == len(covers) and all(covers)
    assert all((a & b) == 0 for i,a in enumerate(covers[:6]) for b in covers[:i])
    sizes = [bits.bit_count() for bits in covers]
    assert sizes == [int(F(m)*k) for m in point["anchor_masses"]+point["extra_masses"]]
    assert max(sizes) == k and all(x == k for x in sizes[:6])
    opt, opt_multisets, checked = 0, [], 0
    for multiset in combinations_with_replacement(range(len(covers)), 6):
        u = 0
        for a in multiset:
            u |= covers[a]
        w = u.bit_count()
        if w > opt:
            opt, opt_multisets = w, []
        if w == opt:
            opt_multisets.append([LABELS[a] for a in multiset])
        checked += 1
    assert opt == 6*k == n and [*LABELS[:6]] in opt_multisets
    menu = {"schema":"Unit clients are IDs in [0,clients), each range is half-open.",
            "K":k,"clients":n,"label_order":LABELS,"sizes":dict(zip(LABELS,sizes)),
            "client_intervals":intervals,"OPT6":opt,
            "all_six_multisets_checked":checked,"all_optimal_multisets":opt_multisets}
    (HERE/"integer-menu.json").write_text(json.dumps(menu,ensure_ascii=False,indent=2)+"\n")
    return menu


def main():
    point,k,gamma,counts,masses = read_point()
    result = audit_rows(k,gamma,masses)
    menu = build_menu(k,point,counts)
    result.update({"input_sha256":PINS, "pattern":PATTERN,
                   "integer_menu_client_count":menu["clients"],
                   "menu_sizes":menu["sizes"], "OPT6":menu["OPT6"],
                   "opt_multisets_checked":menu["all_six_multisets_checked"],
                   "optimal_multiset_count":len(menu["all_optimal_multisets"])})
    (HERE/"candidate-audit.json").write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps(result,ensure_ascii=False,indent=2))


if __name__ == "__main__":
    main()
