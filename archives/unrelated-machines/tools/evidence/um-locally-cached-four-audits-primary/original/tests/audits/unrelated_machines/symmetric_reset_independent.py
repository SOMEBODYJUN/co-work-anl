#!/usr/bin/env python3
"""对称真实最优分布的单机 fallback 重置：独立一二阶审计。

This audit was reconstructed from the exact question, without reading another
agent's derivation. It does not import a repository audit or theorem formula.
The original distribution is uniform over all assignments with exactly q jobs
per machine. Fixing C means overriding and removing these jobs, NOT conditioning
on the event that they originally occupy the removed machine.

The universal proof is separate. This program checks all count-vector orbits
for small q, all literal types for larger q, and directly enumerates the original
balanced assignments for q=1,2 to verify conditional means from pushforward.
"""
from fractions import Fraction as F
from itertools import combinations
from math import factorial
from pathlib import Path
import hashlib
import json
import platform


def compositions(total, parts, bound=None):
    if parts == 1:
        if total >= 0 and (bound is None or total <= bound):
            yield (total,)
        return
    hi = total if bound is None else min(total, bound)
    for first in range(hi + 1):
        for rest in compositions(total - first, parts - 1, bound):
            yield (first,) + rest


def conditional_mean(q, c, counts, job_fallback, literal_target, checked_machine):
    """Return mean, P(literal), mean|literal, mean|not literal, exactly.

    The deleted machine is labelled 2q-1. A selected residual job a has fallback
    h. Event X'_{t,a}=1 has preimages {t} or {t,deleted}. For a different job b,
    conditional old occupancy at a label l is (q-1)/(N-1) if a originally has l,
    and q/(N-1) otherwise. This pairwise sampling identity alone is used here.
    """
    m, n = 2 * q, 2 * q * q
    r = n - c
    h, t, k = job_fallback, literal_target, checked_machine
    assert len(counts) == m - 1 and sum(counts) == r and counts[h] > 0
    fk = counts[k]
    d = 2 if h == t else 1
    mean = F(r + fk, m)
    # A's own final occupancy in checked machine is exactly 1[k==t].
    same_job = int(k == t)
    # Remaining jobs have one ordinary k-choice, plus f_k-1[h==k]
    # deleted-machine choices routed to k.
    other_fallback = fk - int(h == k)
    true_mean = F(same_job) + F(q * (r - 1 + other_fallback), n - 1)
    true_mean -= F((r - 1) * int(k == t) + other_fallback * int(h == t),
                   d * (n - 1))
    p = F(d, m)
    false_mean = None if p == 1 else (mean - p * true_mean) / (1 - p)
    return mean, p, true_mean, false_mean


def check_count_vector(q, c, counts):
    records = []
    for h, count in enumerate(counts):
        if not count:
            continue
        for t in range(2 * q - 1):
            for k in range(2 * q - 1):
                a = conditional_mean(q, c, counts, h, t, k)
                records.append((h, t, k, a))
    return records


def lower_boundary(q, c, counts):
    """A true fallback literal must violate count q for q>=2,c<2q."""
    assert q >= 2 and c < 2 * q
    k = max(range(len(counts)), key=lambda z: counts[z])
    assert counts[k] >= q
    mean, p, plus, minus = conditional_mean(q, c, counts, k, k, k)
    n, r = 2 * q * q, 2 * q * q - c
    reconstructed = 1 + F(2 * q - 1, 2) * F(r + counts[k] - 2, n - 1)
    assert plus == reconstructed
    assert plus > q
    assert plus - q >= F(q - 1, 2 * (n - 1))
    return plus - q


def upper_boundary(q, counts):
    """At c=2q, every count vector with f_k<=q passes every literal."""
    c, n, r = 2 * q, 2 * q * q, 2 * q * q - 2 * q
    assert q >= 2 and max(counts) <= q and sum(counts) == r
    records = check_count_vector(q, c, counts)
    for h, t, k, (mean, p, plus, minus) in records:
        assert mean <= q and plus <= q and minus <= q
        d, fk = (2 if h == t else 1), counts[k]
        # Reconstruct the exact false-literal inequality independently.
        assert minus == F(r + fk - d * plus, 2 * q - d)
        if d == 1:
            assert q - c + fk <= 0 <= plus
        else:
            assert plus >= F(fk, 2)
            if k != t:
                difference = F(q * ((r - 1) - (q - 1) * fk), n - 1)
                assert plus - F(fk, 2) == difference > 0
            else:
                assert plus - F(fk, 2) >= F(q * (q * q - 1), n - 1) > 0
    return len(records)


def balanced_assignments(q):
    m, n = 2 * q, 2 * q * q
    a = [-1] * n
    def rec(machine, remaining):
        if machine == m - 1:
            assert len(remaining) == q
            for j in remaining:
                a[j] = machine
            yield tuple(a)
            return
        for block in combinations(remaining, q):
            chosen = set(block)
            for j in block:
                a[j] = machine
            yield from rec(machine + 1, tuple(j for j in remaining if j not in chosen))
    yield from rec(0, tuple(range(n)))


def direct_pushforward(q, c, fallbacks):
    m, n = 2 * q, 2 * q * q
    removed = m - 1
    residual = tuple(range(c, n))
    assert len(fallbacks) == len(residual)
    counts = tuple(fallbacks.count(k) for k in range(m - 1))
    count_samples = []
    for old in balanced_assignments(q):
        final = tuple(fallbacks[z] if old[j] == removed else old[j]
                      for z, j in enumerate(residual))
        loads = tuple(final.count(k) for k in range(m - 1))
        count_samples.append((final, loads))
    expected_number = factorial(n) // factorial(q) ** m
    assert len(count_samples) == expected_number
    for z, h in enumerate(fallbacks):
        for t in range(m - 1):
            yes = [loads for final, loads in count_samples if final[z] == t]
            no = [loads for final, loads in count_samples if final[z] != t]
            for k in range(m - 1):
                mean, p, plus, minus = conditional_mean(q, c, counts, h, t, k)
                assert mean == F(sum(load[k] for _, load in count_samples), expected_number)
                assert p == F(len(yes), expected_number)
                assert plus == F(sum(load[k] for load in yes), len(yes))
                if no:
                    assert minus == F(sum(load[k] for load in no), len(no))
                else:
                    assert minus is None
    return dict(q=q, c=c, fallbacks=fallbacks, assignments_enumerated=expected_number)


def construct_recoupling(q):
    """Keep the c=q pushforward base x' and replace only its second moments.

    There are 2q-1 remaining machines, q jobs in each fallback group, and
    r=(2q-1)q residual jobs. Entries of x' are 2/(2q) at the fallback and
    1/(2q) elsewhere. Greedily split these integer units into q unit slots per
    machine. The resulting bipartite job/slot multigraph is 2q-regular.
    Repeated deterministic augmenting-path matching gives 2q perfect matchings.
    Their uniform distribution has the exact unchanged x' and every state has
    exactly q jobs per remaining machine.
    """
    assert q >= 2
    m, machine_count = 2 * q, 2 * q - 1
    r = machine_count * q
    fallbacks = tuple(k for k in range(machine_count) for _ in range(q))
    target_units = [[1 + int(fallbacks[j] == k) for k in range(machine_count)]
                    for j in range(r)]
    assert all(sum(row) == m for row in target_units)
    assert all(sum(target_units[j][k] for j in range(r)) == q*m
               for k in range(machine_count))
    # Each integer unit denotes probability 1/m. Slots are indexed k*q+s.
    multiplicity = [[0] * r for _ in range(r)]
    for k in range(machine_count):
        slot, used = 0, 0
        for j in range(r):
            remaining = target_units[j][k]
            while remaining:
                take = min(remaining, m - used)
                multiplicity[j][k*q+slot] += take
                remaining -= take
                used += take
                if used == m:
                    slot += 1
                    used = 0
        assert slot == q and used == 0
    assert all(sum(row) == m for row in multiplicity)
    assert all(sum(multiplicity[j][s] for j in range(r)) == m for s in range(r))
    states = []
    for stage in range(m):
        slot_to_job = [-1] * r
        def augment(job, seen):
            for slot in range(r):
                if not multiplicity[job][slot] or slot in seen:
                    continue
                seen.add(slot)
                previous = slot_to_job[slot]
                if previous == -1 or augment(previous, seen):
                    slot_to_job[slot] = job
                    return True
            return False
        for j in range(r):
            assert augment(j, set()), (q, stage, j)
        job_to_slot = [-1] * r
        for slot, j in enumerate(slot_to_job):
            assert j >= 0 and job_to_slot[j] == -1
            job_to_slot[j] = slot
            multiplicity[j][slot] -= 1
        state = tuple(slot // q for slot in job_to_slot)
        assert all(state.count(k) == q for k in range(machine_count))
        states.append(state)
        remaining_degree = m-stage-1
        assert all(sum(row) == remaining_degree for row in multiplicity)
        assert all(sum(multiplicity[j][s] for j in range(r)) == remaining_degree
                   for s in range(r))
    assert all(not any(row) for row in multiplicity)
    # Exact one-job marginals and two-job joint probabilities from the new
    # distribution. Include diagonal variables, not just distinct jobs.
    marginal = {(j,k): F(sum(state[j] == k for state in states), m)
                for j in range(r) for k in range(machine_count)}
    assert all(marginal[j,k] == F(target_units[j][k],m)
               for j in range(r) for k in range(machine_count))
    joint = {(j,k,a,t): F(sum(state[j] == k and state[a] == t for state in states),m)
             for j in range(r) for k in range(machine_count)
             for a in range(r) for t in range(machine_count)}
    assert all(joint[j,k,a,t] == joint[a,t,j,k]
               for j,k,a,t in joint)
    literal_checks = 0
    for a in range(r):
        for t in range(machine_count):
            yes = [state for state in states if state[a] == t]
            no = [state for state in states if state[a] != t]
            assert yes and no
            for k in range(machine_count):
                # Reconstruct conditional row capacity from second moments.
                plus_numerator = sum(joint[j,k,a,t] for j in range(r))
                minus_numerator = sum(marginal[j,k]-joint[j,k,a,t] for j in range(r))
                assert plus_numerator/marginal[a,t] == q
                assert minus_numerator/(1-marginal[a,t]) == q
                literal_checks += 2
    old_plus = conditional_mean(q,q,(q,)*machine_count,0,0,0)[2]
    assert old_plus-q == F(q*(q-1),2*q*q-1)>0
    return dict(q=q, c=q, fallback_counts=[q]*machine_count,
                decomposition_states=m, each_state_count_per_machine=q,
                exact_unchanged_marginals=True,
                original_pushforward_conditional_excess=str(old_plus-q),
                recoupled_true_and_false_literal_checks=literal_checks,
                recoupled_joint_entries=len(joint),
                schedules=[list(state) for state in states])


def main():
    lower, upper = [], []
    # Full fallback functions reduce to their count vector, a's fallback h,
    # literal target t, and checked machine k by exchangeability.
    for q in (2, 3):
        for c in range(2 * q):
            gaps = [lower_boundary(q, c, counts)
                    for counts in compositions(2 * q * q - c, 2 * q - 1)]
            lower.append(dict(q=q, c=c, count_vectors=len(gaps),
                              minimum_certified_excess=str(min(gaps))))
        cases = [upper_boundary(q, counts)
                 for counts in compositions(2 * q * q - 2 * q, 2 * q - 1, q)]
        upper.append(dict(q=q, c=2*q, count_vectors=len(cases), literal_machine_checks=sum(cases)))
    # All local categories, including impossible categories, are safely bounded
    # by the same symbolic inequalities for every 2<=q<=64. This avoids treating
    # an exponentially large family of complete count vectors as an oracle.
    scalar_checks = 0
    for q in range(2, 65):
        n, c, r = 2*q*q, 2*q, 2*q*q-2*q
        for f in range(q + 1):
            # double-preimage literal; checked machine equal/different
            vals = [1 + F(2*q-1, 2)*F(r+f-2, n-1)] if f else []
            vals += [F(q*(r-1), n-1) + F(2*q-1, 2)*F(f, n-1)]
            for plus in vals:
                mean=F(r+f,2*q);minus=F(r+f-2*plus,2*q-2)
                assert mean<=q and plus<=q and minus<=q and plus>=F(f,2)
                scalar_checks += 1
            # single-preimage literal; checked machine is literal target,
            # fallback target, or neither. Some impossible categories included.
            vals = [1+F((q-1)*(r-1)+q*f,n-1), F(q*(r+f-1),n-1)]
            if f:
                vals += [F(q*(r+f-2),n-1)]
            for plus in vals:
                mean=F(r+f,2*q);minus=F(r+f-plus,2*q-1)
                assert mean<=q and plus<=q and minus<=q
                scalar_checks += 1
        # Sharp lower witness's least possible local excess.
        plus = 1+F(2*q-1,2)*F((n-2*q+1)+q-2,n-1)
        assert plus-q == F(q-1,2*(n-1))>0
    direct = [direct_pushforward(1,0,[0,0]), direct_pushforward(1,1,[0]),
              direct_pushforward(2,2,[0,0,1,1,2,2]),
              direct_pushforward(2,3,[0,0,1,1,2]),
              direct_pushforward(2,4,[0,0,1,1])]
    recouplings = [construct_recoupling(q) for q in (2,3)]
    source = Path(__file__)
    return dict(
        scope="fixed original uniform true-optimum distribution, single-job fallback pushforward only",
        claim="for q>=2 minimal c admitting all capacity literals is 2q; q=1 minimal c is 1",
        python=platform.python_version(), source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
        lower_count_vector_audits=lower, upper_count_vector_audits=upper,
        scalar_q_range=[2,64], scalar_checks=scalar_checks, direct_pushforward_audits=direct,
        same_base_recoupling_audits=recouplings,
        limitations=["finite audits supplement the separate universal proof",
                     "no obstruction to selecting new residual moments or changing other old choices"])


if __name__ == '__main__':
    print(json.dumps(main(), ensure_ascii=False, indent=2))
