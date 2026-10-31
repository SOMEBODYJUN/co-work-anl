#!/usr/bin/env python3
"""Independent exact audit of subdivided two-tree configuration-gap certificates.

Every numeric model calculation uses integers or Fraction. Exhaustive orientation
enumeration is independent of the asserted optimum and LP certificate. This is a
finite audit, not a proof or an algorithm for the general scheduling problem.
"""
from collections import deque
from fractions import Fraction as F
from itertools import combinations, product
from pathlib import Path
import hashlib
import json
import platform


def build(k, length):
    if type(k) is not int or not 2 <= k <= 5 or type(length) is not int or not 2 <= length <= 8:
        raise ValueError("Expanded audit supports integer 2<=k<=5 and 2<=length<=8")
    h, alpha = 1, F(1, k - 1)
    while alpha < F(1, 2):
        h += 1
        alpha *= F(k, k - 1)
    edges, config = [], []

    def machine():
        config.append({})
        return len(config) - 1

    def edge(a, b, pa, pb):
        edges.append((a, b, F(pa), F(pb)))
        return len(edges) - 1

    def add(i, jobs, weight):
        jobs = tuple(sorted(jobs))
        if weight:
            config[i][jobs] = config[i].get(jobs, F(0)) + weight

    def tree(v, depth, incoming):
        children = []
        if depth == 1:
            c = machine()
            for _ in range(k):
                chain = [v] + [machine() for _ in range(length - 1)] + [c]
                jobs = []
                for t in range(length):
                    jobs.append(edge(chain[t], chain[t+1], F(1,k) if t == 0 else 1, 1))
                children.append(jobs[0])
                for t in range(1, length):
                    add(chain[t], (jobs[t-1],), F(1,k))
                    add(chain[t], (jobs[t],), F(k-1,k))
                add(c, (jobs[-1],), F(1,k))
            a = F(1, k - 1)
        else:
            for _ in range(k):
                u = machine()
                j = edge(v, u, F(1,k), 1)
                children.append(j)
                child_alpha = tree(u, depth - 1, j)
            a = child_alpha * F(k, k - 1)
        add(v, children, 1-a)
        for j in children:
            add(v, (incoming, j), a/k)
        return a

    roots = [machine(), machine()]
    big = edge(*roots, 1, 1)
    for v in roots:
        a = tree(v, h, big)
        old = config[v]
        config[v] = {}
        for jobs, w in old.items():
            if big in jobs:
                add(v, jobs, w / (2*a))
                add(v, tuple(j for j in jobs if j != big), w * (1 - 1/(2*a)))
            else:
                add(v, jobs, w)
    return {"k": k, "length": length, "height": h, "edges": edges,
            "config": config, "target": 1 + F(1,k)}


def certificate(instance):
    edges, config, target = instance["edges"], instance["config"], instance["target"]
    coverage = [F(0)] * len(edges)
    for i, choices in enumerate(config):
        assert sum(choices.values()) == 1
        for jobs, w in choices.items():
            assert w > 0
            assert len(jobs) == len(set(jobs))
            load = F(0)
            for j in jobs:
                a, b, pa, pb = edges[j]
                assert i in (a, b)
                load += pa if i == a else pb
                coverage[j] += w
            assert load <= target
    assert coverage == [F(1)] * len(edges)
    assert all(a != b for a, b, _, _ in edges)
    assert len({tuple(sorted((a,b))) for a,b,_,_ in edges}) == len(edges)


def girth(instance):
    """Independent breadth-first shortest-cycle oracle for simple graphs."""
    neighbors = [[] for _ in instance["config"]]
    for a,b,_,_ in instance["edges"]:
        neighbors[a].append(b)
        neighbors[b].append(a)
    best = None
    for s in range(len(neighbors)):
        dist, parent = {s:0}, {s:None}
        queue = deque([s])
        while queue:
            u = queue.popleft()
            if best is not None and 2*dist[u] >= best:
                continue
            for v in neighbors[u]:
                if v not in dist:
                    dist[v], parent[v] = dist[u]+1, u
                    queue.append(v)
                elif parent[u] != v and parent[v] != u:
                    candidate = dist[u]+dist[v]+1
                    best = candidate if best is None else min(best,candidate)
    return best


def exhaustive_optimum(instance):
    """Enumerate every complete orientation, using Gray-code incremental loads."""
    k, edges = instance["k"], instance["edges"]
    if len(edges) > 20:
        raise ValueError("Independent complete enumeration limited to <=20 jobs")
    scaled = [(a,b,int(pa*k),int(pb*k)) for a,b,pa,pb in edges]
    assert all(F(pa,k) == e[2] and F(pb,k) == e[3]
               for e,(_,_,pa,pb) in zip(edges,scaled))
    loads = [0] * len(instance["config"])
    for a,b,pa,pb in scaled:
        loads[a] += pa
    best, witness, old = max(loads), 0, 0
    count = 1 << len(edges)
    for code in range(1,count):
        gray = code ^ (code >> 1)
        flipped = gray ^ old
        j = flipped.bit_length()-1
        a,b,pa,pb = scaled[j]
        if gray & flipped:
            loads[a] -= pa
            loads[b] += pb
        else:
            loads[b] -= pb
            loads[a] += pa
        value = max(loads)
        if value < best:
            best, witness = value, gray
        old = gray
    # Reverse-check the winning orientation independently by summing from zero.
    verify = [F(0)] * len(instance["config"])
    for j,(a,b,pa,pb) in enumerate(edges):
        i,p = (b,pb) if witness & (1 << j) else (a,pa)
        verify[i] += p
    assert max(verify) == F(best,k)
    return {"orientations": count, "optimum": str(F(best,k)),
            "witness_bits": witness}


def explicit_witness(instance):
    """Route root task along one branch, then along one full terminal path."""
    edges = instance["edges"]
    outgoing = [[] for _ in instance["config"]]
    for j,(a,b,pa,pb) in enumerate(edges):
        if j:
            outgoing[a].append(j)
    # Original orientation gives each edge to its left endpoint. The special
    # root edge (job 0) remains at root 0. Propagate that one unit task downward.
    assignment = [a for a,b,pa,pb in edges]
    current, steps = edges[0][0], 0
    while outgoing[current]:
        j = outgoing[current][0]
        a,b,pa,pb = edges[j]
        assignment[j] = b
        current = b
        steps += 1
        assert steps <= len(edges)
    actual = [F(0)] * len(instance["config"])
    for i,(a,b,pa,pb) in zip(assignment,edges):
        assert i == a or i == b
        actual[i] += pa if i == a else pb
    bound = 2-F(1,instance["k"])
    assert max(actual) == bound
    return {"maximum_load":str(max(actual)),"rerouted_path_length":steps,
            "assignment_sha256":hashlib.sha256(json.dumps(assignment).encode()).hexdigest()}


def glue(instance, coalition):
    """Enumerate the exact tree-gluing distribution; preserve FULL config states.

    Each root chooses its original full machine configuration. Child states use
    that machine's original distribution, conditioned on the internal edge being
    absent/present opposite its parent. Disconnected components are independent.
    This routine requires induced forest and explicitly checks all marginals.
    """
    coalition = tuple(sorted(coalition))
    edges, config = instance["edges"], instance["config"]
    neighbors = {i:[] for i in coalition}
    for j,(a,b,_,_) in enumerate(edges):
        if a in neighbors and b in neighbors:
            neighbors[a].append((b,j))
            neighbors[b].append((a,j))
    order, relation, seen = [], {}, set()
    for root in coalition:
        if root in seen:
            continue
        relation[root] = None
        seen.add(root)
        queue = deque([root])
        while queue:
            i = queue.popleft()
            order.append(i)
            for child,j in neighbors[i]:
                if relation[i] is not None and child == relation[i][0]:
                    continue
                assert child not in seen, "The requested induced graph is not a forest"
                seen.add(child)
                relation[child] = i,j
                queue.append(child)
    states = [({},F(1))]
    for i in order:
        next_states = []
        for state, probability in states:
            candidates = config[i]
            if relation[i] is not None:
                parent,j = relation[i]
                required = j not in state[parent]
                candidates = {jobs:w for jobs,w in candidates.items() if (j in jobs) == required}
            mass = sum(candidates.values())
            assert mass > 0, "A positive-probability parent event requested zero-mass child event"
            for jobs,w in candidates.items():
                next_states.append((state | {i:jobs},probability*w/mass))
        states = next_states
    assert sum(w for _,w in states) == 1
    for i in coalition:
        marginals = {}
        for state,w in states:
            marginals[state[i]] = marginals.get(state[i],F(0)) + w
        assert marginals == config[i]
    for state,w in states:
        taken = set()
        for i in coalition:
            assert not taken.intersection(state[i])
            taken.update(state[i])
        for j,(a,b,_,_) in enumerate(edges):
            if a in neighbors and b in neighbors:
                assert (j in state[a]) + (j in state[b]) == 1
    return len(states)


def audit():
    results = []
    for k,length in [(2,2),(2,3),(3,2),(3,3),(4,2),(4,4),(5,2)]:
        instance = build(k,length)
        certificate(instance)
        g = girth(instance)
        assert g == 2*length
        record = {"k":k,"length":length,"height":instance["height"],
                  "machines":len(instance["config"]),"jobs":len(instance["edges"]),
                  "configuration_certificate":"exactly valid", "girth":g,
                  "target":str(instance["target"]),
                  "asserted_optimum":str(2-F(1,k)),
                  "ratio_lower_bound":str((2-F(1,k))/instance["target"]),
                  "explicit_schedule_witness":explicit_witness(instance)}
        if len(instance["edges"]) <= 20:
            record["independent_oracle"] = exhaustive_optimum(instance)
            assert record["independent_oracle"]["optimum"] == record["asserted_optimum"]
        results.append(record)
    # Test EVERY vertex coalition of size <=3 in the 4-girth case; ALL <=4 in
    # the 6-girth case. This includes disconnected and branching coalitions.
    coalition_results = []
    for k,length,rank in [(3,2,3),(3,3,4)]:
        instance = build(k,length)
        count, max_support = 0,0
        for r in range(rank+1):
            for coalition in combinations(range(len(instance["config"])),r):
                max_support = max(max_support,glue(instance,coalition))
                count += 1
        coalition_results.append({"k":k,"length":length,"maximum_coalition_size":rank,
                                  "all_coalitions_checked":count,
                                  "largest_joint_distribution_support":max_support,
                                  "full_machine_configuration_marginals":"exactly preserved"})
    # A cycle violates this routine's forest precondition. Rejection alone
    # asserts NOTHING about existence of some other joint distribution.
    instance = build(3,2)
    first_cycle = (0,2,3,4)
    try:
        glue(instance,first_cycle)
    except AssertionError as exc:
        assert "not a forest" in str(exc)
    else:
        raise AssertionError("Cycle precondition was not enforced")
    for left in (True, False):
        fixture = {"edges":[(0,1,F(0),F(0))],
                   "config":[{(0,):F(1)} if left else {():F(1)},
                             {():F(1)} if left else {(0,):F(1)}],
                   "target":F(0)}
        certificate(fixture)
        assert glue(fixture,(0,1)) == 1
        assert glue(fixture,()) == 1
    invalid = [(True,2),(1,2),(6,2),(2,True),(2,1),(2,9),(2,2.0)]
    for args in invalid:
        try:
            build(*args)
        except ValueError:
            pass
        else:
            raise AssertionError("Invalid expanded-generator argument accepted")
    return {"purpose":"finite independent Fraction audit; general claims require the proof",
            "boundary_fixtures":2,"invalid_arguments_rejected":len(invalid),
            "python":platform.python_version(),
            "code_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "instances":results,"coalition_checks":coalition_results,
            "cycle_precondition":"rejected as required","random_seed":None,
            "numeric_policy":"exact Fraction and integer arithmetic, no floating point"}


if __name__ == "__main__":
    print(json.dumps(audit(),ensure_ascii=False,indent=2))
