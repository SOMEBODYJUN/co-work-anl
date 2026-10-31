#!/usr/bin/env python3
"""稀释终端阻塞器：配置证书、逐边LST探针和安全星匹配的精确审计。

Reusable audit code; no repository mutations. Fraction throughout. This tests
finite expanded instances; the general family proof is separate.
"""
from fractions import Fraction as F
from itertools import product
import argparse
import json
import platform
import hashlib
from pathlib import Path

SOURCE_SHA256 = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()


def height(k):
    if type(k) is not int or k < 2:
        raise ValueError("integer k >= 2 required")
    h, a = 1, F(1, k-1)
    while a < F(1, 2):
        h, a = h+1, a*F(k, k-1)
    return h, a


def instance(k):
    if not 2 <= k <= 4:
        raise ValueError("expanded materialization limited to k=2,3,4")
    h, alpha = height(k)
    N, T = k*(k-1), 1+F(1,k)
    edges, roles, configs, gadgets = [], [], [], []
    def node():
        configs.append([])
        return len(configs)-1
    def edge(times, role):
        edges.append(times)
        roles.append(role)
        return len(edges)-1
    roots = [node(), node()]
    bridge = edge({roots[0]:F(1), roots[1]:F(1)}, ("bridge",))
    down = {bridge: roots[0]}
    def subtree(root, depth, incoming):
        if depth == 1:
            terminals = [node() for _ in range(N)]
            ordinary = []
            for t in terminals[:k]:
                j = edge({root:F(1,k), t:F(1)}, ("ordinary", depth))
                ordinary.append(j)
                down[j] = t
            blockers = [edge({t:F(1) for t in terminals}, ("blocker",))
                        for _ in range(N-1)]
            a = F(1,k-1)
            for q, t in enumerate(terminals):
                ordinary_mass = F(1,k) if q < k else F(0)
                choices = []
                if q < k:
                    choices.append((ordinary_mass,(ordinary[q],)))
                choices += [((1-ordinary_mass)/(N-1),(b,)) for b in blockers]
                configs[t] = choices
            gadgets.append({"parent":root,"terminals":terminals,
                            "ordinary":ordinary,"blockers":blockers})
            children = ordinary
        else:
            children = []
            for _ in range(k):
                child = node()
                j = edge({root:F(1,k), child:F(1)}, ("tree", depth))
                down[j] = child
                children.append(j)
                child_a = subtree(child,depth-1,j)
            a = child_a*F(k,k-1)
        configs[root] = [(1-a,tuple(children))] + [
            (a/k,(incoming,j)) for j in children]
        return a
    for root in roots:
        a = subtree(root,h,bridge)
        thinned = []
        for w, jobs in configs[root]:
            if bridge in jobs:
                thinned += [(w/(2*a),jobs),
                            (w*(1-1/(2*a)),tuple(j for j in jobs if j != bridge))]
            else:
                thinned.append((w,jobs))
        configs[root] = [(w,s) for w,s in thinned if w]
    return {"k":k,"h":h,"N":N,"T":T,"edges":edges,
            "roles":roles,"configs":configs,"gadgets":gadgets,
            "down":down,"roots":roots,"bridge":bridge,"alpha":alpha}


def check_config(d):
    cover = [F(0)]*len(d["edges"])
    columns = 0
    for i, choices in enumerate(d["configs"]):
        assert sum(w for w,s in choices) == 1
        for w,s in choices:
            assert w >= 0 and len(set(s)) == len(s)
            assert sum(d["edges"][j][i] for j in s) <= d["T"]
            for j in s:
                cover[j] += w
            columns += 1
    assert all(c == 1 for c in cover)
    return columns


def probe_certificate(d, jfix, ifix):
    """Explicit pruned-LST point with x[ifix,jfix]=1, all forced edge types."""
    if ifix not in d["edges"][jfix]:
        raise ValueError("forced edge unavailable")
    normal = dict(d["down"])
    if jfix in normal:
        normal[jfix] = ifix
    else:
        # The only forced non-normal jobs are blockers. If needed, displace
        # the ordinary terminal job to its small parent endpoint.
        for g in d["gadgets"]:
            if jfix in g["blockers"]:
                for j in g["ordinary"]:
                    if normal[j] == ifix:
                        normal[j] = g["parent"]
                break
    x = {j:{i:F(1)} for j,i in normal.items()}
    for g in d["gadgets"]:
        fixed_here = jfix in g["blockers"]
        used = {t:F(0) for t in g["terminals"]}
        for j in g["ordinary"]:
            i = normal[j]
            if i in used:
                used[i] += d["edges"][j][i]
        if fixed_here:
            used[ifix] += 1
            x[jfix] = {ifix:F(1)}
        residual = {t:d["T"]-used[t] for t in used}
        assert all(v >= 0 for v in residual.values())
        others = [j for j in g["blockers"] if j != jfix or not fixed_here]
        total_capacity = sum(residual.values())
        assert total_capacity >= len(others)
        if others:
            for j in others:
                x[j] = {t:v/total_capacity for t,v in residual.items() if v}
    return x


def check_lst(d,x,jfix,ifix):
    assert set(x) == set(range(len(d["edges"])))
    loads = [F(0)]*len(d["configs"])
    for j, row in x.items():
        assert sum(row.values()) == 1
        for i,v in row.items():
            assert v >= 0 and i in d["edges"][j]
            assert d["edges"][j][i] <= d["T"]
            loads[i] += d["edges"][j][i]*v
    assert x[jfix] == {ifix:F(1)}
    assert all(load <= d["T"] for load in loads)
    return max(loads)


def star_matching_certificate(d,i,jfix):
    """The safe heavy-alternative star filter is zero-loss on this family."""
    forced = [j for j,e in enumerate(d["edges"]) if j != jfix and i in e
              and all(p > d["T"]/2 for r,p in e.items() if r != i)]
    owner = {}
    def augment(j, seen):
        for r in d["edges"][j]:
            if r == i or r in seen:
                continue
            seen.add(r)
            if r not in owner or augment(owner[r],seen):
                owner[r] = j
                return True
        return False
    assert all(augment(j,set()) for j in forced)
    matching = {j:r for r,j in owner.items()}
    assert len(matching) == len(forced)
    assert len(set(matching.values())) == len(forced)
    assert all(r != i and r in d["edges"][j] for j,r in matching.items())
    # All forced jobs can leave simultaneously according to this necessary
    # condition, so max-weight matching weight equals the full star weight.
    W = sum(d["edges"][j][i] for j in forced)
    LB = d["edges"][jfix][i] + sum(d["edges"][j][i] for j in forced)-W
    assert LB <= d["T"]
    return len(forced)


def representatives(d):
    seen, result = set(), []
    selected = {t for g in d["gadgets"] for t in g["terminals"][:d["k"]]}
    for j,e in enumerate(d["edges"]):
        for i,p in e.items():
            role = d["roles"][j]
            if role[0] == "bridge":
                key = ("bridge",d["roots"].index(i))
            elif role[0] == "blocker":
                key = ("blocker",i in selected)
            else:
                key = role+(p == 1,)
            if key not in seen:
                result.append((j,i,key))
                seen.add(key)
    return result


def brute_optimum(d):
    best = None
    count = 0
    for choices in product(*(tuple(e) for e in d["edges"])):
        load = [F(0)]*len(d["configs"])
        for j,i in enumerate(choices):
            load[i] += d["edges"][j][i]
        value = max(load)
        best = value if best is None else min(best,value)
        count += 1
    return best,count


def optimal_schedule(d):
    """Construct the path schedule; verifier recomputes actual sparse loads."""
    sigma = {d["bridge"]:d["roots"][0]}
    for j,e in enumerate(d["edges"]):
        if d["roles"][j][0] in ("tree","ordinary"):
            sigma[j] = min(e,key=e.get)
    current = d["roots"][0]
    while True:
        outgoing = [j for j,e in enumerate(d["edges"])
                    if d["roles"][j][0] in ("tree","ordinary")
                    and e.get(current) == F(1,d["k"])]
        if not outgoing:
            break
        j = outgoing[0]
        current = next(i for i in d["edges"][j] if i != current)
        sigma[j] = current
    for g in d["gadgets"]:
        occupied = {sigma[j] for j in g["ordinary"] if sigma[j] in g["terminals"]}
        free = [t for t in g["terminals"] if t not in occupied]
        assert len(free) >= len(g["blockers"])
        for j,t in zip(g["blockers"],free):
            sigma[j] = t
    assert set(sigma) == set(range(len(d["edges"])))
    load = [F(0)]*len(d["configs"])
    for j,i in sigma.items():
        assert i in d["edges"][j]
        load[i] += d["edges"][j][i]
    assert max(load) == 2-F(1,d["k"])
    return sigma,max(load)


def audit(all_k4=False):
    results = []
    for k in (2,3,4):
        d = instance(k)
        columns = check_config(d)
        sigma, schedule_value = optimal_schedule(d)
        probes = [(j,i,("all",)) for j,e in enumerate(d["edges"]) for i in e]
        if k == 4 and not all_k4:
            probes = representatives(d)
        for j,i,key in probes:
            check_lst(d,probe_certificate(d,j,i),j,i)
        matching_edges = 0
        for j,e in enumerate(d["edges"]):
            for i in e:
                star_matching_certificate(d,i,j)
                matching_edges += 1
        row = {"k":k,"height":d["h"],"N":d["N"],
               "machines":len(d["configs"]),"jobs":len(d["edges"]),
               "eligible_edges":sum(map(len,d["edges"])),
               "T":str(d["T"]),"config_columns":columns,
               "lst_probes_checked":len(probes),
               "lst_probe_scope":"all edges" if k < 4 or all_k4 else "symmetry representatives",
               "representative_classes":[list(key) for j,i,key in probes] if k == 4 and not all_k4 else None,
               "star_matching_edges_checked":matching_edges,
               "analytic_optimum":str(2-F(1,k)),
               "constructed_schedule_value":str(schedule_value),
               "ratio":str((2-F(1,k))/d["T"])}
        if k == 2:
            optimum,count = brute_optimum(d)
            assert optimum == 2-F(1,k)
            row.update(exhaustive_optimum=str(optimum),exhaustive_assignments=count)
        results.append(row)
    return {"title":"稀释终端阻塞器的精确有限核验", "python":platform.python_version(),
            "arithmetic":"fractions.Fraction, exact", "seed":None,
            "code_sha256":SOURCE_SHA256,
            "results":results,
            "limitations":["Finite checks do not prove the general family theorem.",
                            "No approximation algorithm or complexity hardness result is claimed.",
                            "This defeats independent per-edge LST probes, not conditioned configuration-LP probes."]}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--all-k4",action="store_true")
    args = parser.parse_args()
    print(json.dumps(audit(args.all_k4),ensure_ascii=False,indent=2))
