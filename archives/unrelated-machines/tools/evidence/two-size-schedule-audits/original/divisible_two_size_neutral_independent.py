"""Independent labeled-job audit of the neutral macro balancing statement.

Does not import or call the author's count-state repair or audit.
All times are integer ticks; delta scaling is verified separately by Fraction.
"""
from fractions import Fraction
from itertools import product


def actual_loads(m, q, k, where):
    result = [0] * m
    for job, machine in enumerate(where):
        result[machine] += q if job < k else 1
    return result


def below_in_majorization(new, old):
    aa, bb = sorted(new, reverse=True), sorted(old, reverse=True)
    left = right = 0
    for a, b in zip(aa, bb):
        left += a
        right += b
        if left > right:
            return False
    return left == right


def labeled_balance(m, q, k, initial):
    where = list(initial)
    n_tiny = len(where) - k
    target = max(q * ((k + m - 1) // m),
                 (k * q + n_tiny + m - 1) // m)
    big_steps = little_steps = reversed_tinies = 0
    max_batch = 0
    while True:
        bigs = [[j for j in range(k) if where[j] == i] for i in range(m)]
        pairs = [(s, t) for s in range(m) for t in range(m)
                 if len(bigs[s]) >= len(bigs[t]) + 2]
        if not pairs:
            break
        s, t = pairs[0]
        old = actual_loads(m, q, k, where)
        old_composition = sum(len(row) ** 2 for row in bigs)
        dload = old[s] - old[t]
        chosen_tinies = []
        if dload < q:
            requested = q - dload
            available = [j for j in range(k, len(where)) if where[j] == t]
            assert 0 < requested <= len(available)
            chosen_tinies = available[:requested]
        where[bigs[s][0]] = t
        for job in chosen_tinies:
            where[job] = s
        new = actual_loads(m, q, k, where)
        assert below_in_majorization(new, old)
        if dload < q:
            assert new[s] == old[t] and new[t] == old[s]
        new_counts = [sum(where[j] == i for j in range(k)) for i in range(m)]
        assert sum(z * z for z in new_counts) <= old_composition - 2
        big_steps += 1
        reversed_tinies += len(chosen_tinies)
        max_batch = max(max_batch, 1 + len(chosen_tinies))
    moved_once = set()
    while True:
        old = actual_loads(m, q, k, where)
        excessive = [i for i in range(m) if old[i] > target]
        if not excessive:
            break
        deficient = [i for i in range(m) if old[i] < target]
        assert deficient
        s, t = excessive[0], deficient[0]
        job = next(j for j in range(k, len(where)) if where[j] == s)
        assert job not in moved_once
        moved_once.add(job)
        where[job] = t
        new = actual_loads(m, q, k, where)
        assert below_in_majorization(new, old)
        assert sorted(new) != sorted(old)
        little_steps += 1
    final = actual_loads(m, q, k, where)
    assert max(final) == target
    assert big_steps <= k * k // 2
    assert little_steps <= n_tiny
    return target, tuple(where), big_steps, little_steps, reversed_tinies, max_batch


def audit():
    states = parameters = macro_steps = tiny_steps = reverse_moves = 0
    largest_batch = 0
    for m, q, k, nt in product(range(1, 4), range(1, 6), range(4), range(5)):
        if k + nt > 6:
            continue
        assignments = list(product(range(m), repeat=k + nt))
        brute = min(max(actual_loads(m, q, k, a)) for a in assignments)
        parameters += 1
        for a in assignments:
            value, final, bs, ts, rs, support = labeled_balance(m, q, k, a)
            assert value == brute
            assert len(final) == k + nt
            states += 1
            macro_steps += bs
            tiny_steps += ts
            reverse_moves += rs
            largest_batch = max(largest_batch, support)
    # Huge binary Q with only explicit finitely many jobs: no numeric Q loop.
    huge_q = 2 ** 200 + 123
    delta = Fraction(7, 2 ** 120 + 3)
    value, final, *_ = labeled_balance(4, huge_q, 7, (0,) * 7 + (1,) * 5)
    assert max(delta * z for z in actual_loads(4, huge_q, 7, final)) == delta * value
    return dict(parameter_sets=parameters, labeled_initial_states=states,
                macro_steps=macro_steps, tiny_steps=tiny_steps,
                tiny_moves_inside_macro_batches=reverse_moves,
                largest_macro_batch_support=largest_batch,
                huge_Q_binary_bits=huge_q.bit_length(),
                includes_m_one_empty_jobs_Q_one=True)


if __name__ == '__main__':
    print(audit())
