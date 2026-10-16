#!/usr/bin/env python3
"""Exact star-CONFIG transfer and contracted sparse-family audit.

Fraction only; deterministic exhaustive probes on the stated expanded input.
No general configuration LP solver; stdout does not overwrite frozen evidence.
"""
from collections import defaultdict
from fractions import Fraction as F
from pathlib import Path
from itertools import combinations
import hashlib
import importlib.util
import json
import argparse
import sys

ROOT = Path(__file__).resolve().parents[3]
spec = importlib.util.spec_from_file_location(
    "sparse_base", ROOT / "tests/audits/unrelated_machines/sparse_conditioned_configuration.py")
base = importlib.util.module_from_spec(spec)
spec.loader.exec_module(base)


def add(row, weight, items):
    if weight:
        row[frozenset(items)] += weight


def normalized(cert):
    return {i: dict((frozenset(S), w) for S, w in row.items() if w)
            for i, row in cert.items()}


def record(costs, machines, v, T, e):
    """Check a full-neighborhood minimal star and build its exact replacement."""
    group = frozenset(j for j, c in costs.items() if v in c)
    total = sum(costs[j][v] for j in group)
    assert total > T and all(total-costs[j][v] <= T for j in group)
    assert e not in costs
    exterior = sorted(set().union(*(set(costs[j]) for j in group))-{v}, key=repr)
    mins = {i: min((costs[j][i], j) for j in group if i in costs[j]) for i in exterior}
    assert mins
    return dict(v=v, group=group, e=e, exterior=exterior,
                replacement={i: pair[0] for i, pair in mins.items()},
                argmin={i: pair[1] for i, pair in mins.items()},
                local={j: costs[j][v] for j in group})


def contract_matrix(costs, machines, rec):
    for j in rec['group']:
        del costs[j]
    costs[rec['e']] = rec['replacement'].copy()
    machines.remove(rec['v'])


def forward(cert, rec, force=None):
    """Mutate an explicit point; at most one old column splits globally."""
    group, e = rec['group'], rec['e']
    occupancy = sum(w for i in rec['exterior'] for S, w in cert[i].items()
                    if S & group)
    assert occupancy >= 1, 'external configuration occupancy below one'
    need = F(1)
    split = 0
    priority = force[1] if force is not None and force[0] in group else None
    order = ([priority]+[i for i in rec['exterior'] if i != priority]
             if priority is not None else rec['exterior'])
    for i in order:
        row = defaultdict(F)
        for S, w in cert[i].items():
            overlap = S & group
            take = min(w, need) if overlap else F(0)
            residual = S-group
            add(row, take, residual | {e})
            add(row, w-take, residual)
            need -= take
            split += 0 < take < w
        cert[i] = dict(row)
    assert need == 0 and split <= 1
    del cert[rec['v']]
    return split


def reverse(cert, rec):
    group, e = rec['group'], rec['e']
    local = defaultdict(F)
    for i in rec['exterior']:
        row = defaultdict(F)
        for S, w in cert[i].items():
            if e in S:
                j = rec['argmin'][i]
                add(row, w, (S-{e}) | {j})
                add(local, w, group-{j})
            else:
                add(row, w, S)
        cert[i] = dict(row)
    cert[rec['v']] = dict(local)


def verify(costs, machines, cert, T, force=None):
    assert set(cert) == set(machines)
    cover = defaultdict(F)
    forced = F(0)
    support = 0
    for i, row in cert.items():
        assert sum(row.values()) == 1
        for S, w in row.items():
            assert w > 0
            load = sum(costs[j][i] for j in S)
            assert load <= T
            assert sum(costs[j][i] > T/2 for j in S) <= 1
            for j in S:
                cover[j] += w
            if force is not None and i == force[1] and force[0] in S:
                forced += w
            support += 1
    assert set(cover) == set(costs) and all(q == 1 for q in cover.values())
    if force is not None:
        assert forced == 1
    return support


def triggers(costs, machines, T):
    out = []
    for i in machines:
        times = [c[i] for c in costs.values() if i in c]
        total = sum(times)
        if total > T and all(total-p <= T for p in times):
            out.append(i)
    return out


def contracted_family(k=3, export=None):
    s0, M, H, gamma = base.parameters(k)
    P = base.instance(k, H, gamma)
    original_costs = {j: rec['costs'].copy() for j, rec in enumerate(P['jobs'])}
    costs = {j: c.copy() for j, c in original_costs.items()}
    machines = list(P['machines'])
    T = 1+F(1, k)
    records = []
    for terms, _ in P['groups'].values():
        for v in (terms[0], terms[-1]):
            rec = record(costs, machines, v, T, max(costs)+1)
            # Strong instance-level condition, independent of a particular y.
            for i in rec['exterior']:
                eligible = [j for j in rec['group'] if i in costs[j]]
                assert len(eligible) == 1
            contract_matrix(costs, machines, rec)
            records.append(rec)
    assert not triggers(costs, machines, T)
    counts = defaultdict(int)
    max_support = max_original = max_splits = 0
    sample, sample_force, sample_sink = None, None, F(-1)
    for j, c in costs.items():
        for i in c:
            source = (j, i)
            for rec in reversed(records):
                if source[0] == rec['e']:
                    source = (rec['argmin'][source[1]], source[1])
            old, _ = base.certificate(P, source)
            cert = {}
            for v, row in old.items():
                merged = defaultdict(F)
                for w, S in row:
                    add(merged, w, S)
                cert[v] = dict(merged)
            before = verify(original_costs, P['machines'], cert, T, source)
            tracked, splits = source, 0
            for rec in records:
                splits += forward(cert, rec, tracked)
                if tracked[0] in rec['group']:
                    tracked = (rec['e'], tracked[1])
            assert tracked == (j, i)
            after = verify(costs, machines, cert, T, (j, i))
            assert after <= before+len(records)
            max_support = max(max_support, after)
            max_original = max(max_original, before)
            max_splits = max(max_splits, splits)
            counts['all_final_edges'] += 1
            if j >= len(P['jobs']):
                counts['replacement_edges'] += 1
            sink = max(sum(costs[a][('z',)] for a in S) for S in cert[('z',)])
            if sink > sample_sink:
                sample_sink, sample_force = sink, (j, i)
                sample = {v: row.copy() for v, row in cert.items()}
            # One complete reverse chain checks all recovered capacities/coverage.
            if counts['all_final_edges'] == 1:
                for rec in reversed(records):
                    reverse(cert, rec)
                verify(original_costs, P['machines'], cert, T)
    frozen = json.loads((ROOT / 'evidence/certificates/unrelated_machines/sparse_conditioned_configuration_witness.json').read_text())
    assignment = dict(enumerate(frozen['integer_upper_assignment']))
    labels = P['machines']
    assignment = {j: labels[i] for j, i in assignment.items()}
    # The frozen example is k=3,H=5 and uses the same deterministic generator.
    assert k == 3 and H == 5
    for rec in records:
        candidates = [j for j in rec['group'] if assignment[j] != rec['v']]
        assert candidates
        a = min(candidates)
        dest = assignment[a]
        for j in rec['group']:
            del assignment[j]
        assignment[rec['e']] = dest
    loads = defaultdict(F)
    for j, i in assignment.items():
        loads[i] += costs[j][i]
    assert max(loads.values()) <= 2-F(1, k)
    if export is not None:
        export = Path(export)
        export.mkdir(parents=True, exist_ok=True)
        machine_id = {v: i for i, v in enumerate(machines)}
        job_id = {j: q for q, j in enumerate(costs)}
        payload = dict(k=k, H=H, gamma=str(gamma), threshold=str(T),
                       machines=machines,
                       jobs=[dict(source_job_id=j, eligible=[[machine_id[i], str(p)] for i, p in c.items()])
                             for j, c in costs.items()])
        witness = dict(forced_job=job_id[sample_force[0]], forced_machine=machine_id[sample_force[1]],
                       configuration_point=[dict(machine=machine_id[i], configurations=[dict(weight=str(w), jobs=sorted(job_id[j] for j in S)) for S, w in row.items()]) for i, row in sample.items()],
                       integer_upper_assignment=[machine_id[assignment[j]] for j in costs],
                       integer_upper_makespan=str(max(loads.values())), maximum_sink_configuration=str(sample_sink))
        for filename, data in [('contracted_sparse_configuration_input.json', payload),
                               ('contracted_sparse_configuration_witness.json', witness)]:
            dest = export / filename
            assert not dest.exists(), 'export must not overwrite an artifact'
            dest.write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n')
    return dict(k=k, H=H, gamma=str(gamma), threshold=str(T),
                original_machines=len(P['machines']), original_jobs=len(P['jobs']),
                contractions=len(records), machines=len(machines), jobs=len(costs),
                final_triggers=0, maximum_job_degree=max(map(len, costs.values())),
                probe_counts=dict(counts), max_original_support=max_original,
                max_final_support=max_support, max_actual_splits=max_splits,
                integer_upper=str(max(loads.values())),
                input_sha256=hashlib.sha256((ROOT/'examples/unrelated_machines/sparse_conditioned_configuration_input.json').read_bytes()).hexdigest())


def small_transfer():
    # Zero outside edge, nonuniform probabilities, and a genuine global split.
    costs = {0: {0: F(1), 1: F(0)}, 1: {0: F(1), 2: F(1)}}
    cert = {0: {frozenset({0}): F(1, 3), frozenset({1}): F(1, 3), frozenset(): F(1, 3)},
            1: {frozenset({0}): F(2, 3), frozenset(): F(1, 3)},
            2: {frozenset({1}): F(2, 3), frozenset(): F(1, 3)}}
    rec = record(costs, [0, 1, 2], 0, F(1), 2)
    before = verify(costs, [0, 1, 2], cert, F(1))
    split = forward(cert, rec)
    assert split == 1
    reduced = {j: c.copy() for j, c in costs.items()}
    machines = [0, 1, 2]
    contract_matrix(reduced, machines, rec)
    after = verify(reduced, machines, cert, F(1))
    assert after <= before+1
    reverse(cert, rec)
    verify(costs, [0, 1, 2], cert, F(1))
    # All threshold-zero inputs have no contraction trigger; empty jobs included.
    assert triggers({}, [0], F(0)) == []
    assert triggers({0: {0: F(0)}}, [0], F(0)) == []
    # Explicit failure of the certificate-relative exclusivity condition.
    bad = {0: {frozenset({0}): F(1, 2), frozenset({1}): F(1, 2)},
           1: {frozenset({0, 1}): F(1, 2), frozenset(): F(1, 2)}}
    badcost = {0: {0: F(1), 1: F(1, 2)}, 1: {0: F(1), 1: F(1, 2)}}
    verify(badcost, [0, 1], bad, F(1))
    badrec = record(badcost, [0, 1], 0, F(1), 2)
    try:
        forward(bad, badrec)
    except AssertionError as err:
        assert 'occupancy' in str(err)
    else:
        raise AssertionError('missing assumption accepted')
    # The forced machine must precede other eligible machines in the selection.
    control = {0: {frozenset({0}): F(1, 2), frozenset(): F(1, 2)},
               1: {frozenset({0}): F(1, 2), frozenset(): F(1, 2)},
               2: {frozenset({1}): F(1)}}
    verify(costs, [0, 1, 2], control, F(1), (1, 2))
    forward(control, rec, (1, 2))
    verify(reduced, machines, control, F(1), (2, 2))
    return dict(zero_and_empty=True, rational_roundtrip=True, forced_machine_priority=True,
                missing_exclusivity_rejected=True, actual_global_splits=split)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--export-dir')
    args = parser.parse_args()
    print(json.dumps(dict(arithmetic='fractions.Fraction', python=sys.version.split()[0],
                         code_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                         small=small_transfer(), expanded=contracted_family(export=args.export_dir)), indent=2))
