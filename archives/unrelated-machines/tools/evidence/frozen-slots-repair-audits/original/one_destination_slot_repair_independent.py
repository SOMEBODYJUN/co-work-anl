"""Independent task-identity enumeration for the one-destination lemma.

Does not import the constructor audit. Recursion enforces original-owner
destination consistency while placing separately labeled original small jobs.
"""
from collections import Counter
from fractions import Fraction as F
import json


def enumerate_identities(m):
    owners = [0] * (m - 1) + [i for i in range(1, m) for _ in range(m)]
    hist = {False: Counter(), True: Counter()}
    witness = {}
    for big_dest in range(m):
        moves_big = big_dest != 0
        target = [0 if i == big_dest else m + 1 for i in range(m)]
        used = [0] * m
        # owner 0's already-moved big reserves its only permitted destination.
        reserved = [None] * m
        if moves_big:
            reserved[0] = big_dest
        current = []

        def visit(j, distance):
            if j == len(owners):
                if used == target:
                    total_distance = distance + int(moves_big)
                    hist[moves_big][total_distance] += 1
                    witness.setdefault((moves_big, total_distance), (big_dest, tuple(current)))
                return
            source = owners[j]
            for destination in range(m):
                if used[destination] >= target[destination]:
                    continue
                moved = destination != source
                if moved and reserved[source] is not None and reserved[source] != destination:
                    continue
                old = reserved[source]
                if moved:
                    reserved[source] = destination
                used[destination] += 1
                current.append(destination)
                visit(j + 1, distance + int(moved))
                current.pop()
                used[destination] -= 1
                reserved[source] = old

        visit(0, 0)
    assert min(hist[False]) == m * (m - 1) // 2
    assert min(hist[True]) == m * (m + 1) // 2
    assert len(hist[True]) == 1
    return {
        "m": m,
        "big_stays_hamming_histogram": dict(sorted(hist[False].items())),
        "big_moves_hamming_histogram": dict(sorted(hist[True].items())),
        "big_stays_count": sum(hist[False].values()),
        "big_moves_count": sum(hist[True].values()),
    }


def lifted_chain(m, move_big):
    """Build final owners using only the original tasks in each source inventory."""
    old = [0] * m + [v for v in range(1, m) for _ in range(m)]
    final = old.copy()
    if not move_big:
        order = list(range(m))
        for k, source in enumerate(order[:-1]):
            destination = order[k + 1]
            count = m - 1 - k
            original_small_ids = [j for j in range(1, m * m) if old[j] == source]
            for j in original_small_ids[:count]:
                final[j] = destination
    else:
        final[0] = 1
        order = [1] + list(range(2, m)) + [0]
        for k, source in enumerate(order[:-1]):
            destination = order[k + 1]
            count = m - k
            original_small_ids = [j for j in range(1, m * m) if old[j] == source]
            for j in original_small_ids[:count]:
                final[j] = destination
    big_dest = final[0]
    small_counts = Counter(final[1:])
    assert small_counts[big_dest] == 0
    assert all(small_counts[v] == m + 1 for v in range(m) if v != big_dest)
    for source in range(m):
        destinations = {final[j] for j in range(m * m) if old[j] == source and final[j] != source}
        assert len(destinations) <= 1
    distance = sum(x != y for x, y in zip(old, final))
    assert distance == m * (m + (1 if move_big else -1)) // 2
    return distance


def sequential_batches(m):
    """Recompute genuine loads after each batch of original-owner small jobs."""
    original = [0] * m + [v for v in range(1, m) for _ in range(m)]
    current = original.copy()

    def real_loads():
        out = [F(0) for _ in range(m)]
        for j, destination in enumerate(current):
            out[destination] += F(1) if j == 0 else F(1, m + 1)
        return out

    before = max(real_loads())
    assert before == F(2 * m, m + 1)
    maxima = [str(before)]
    batches = []
    for t in range(1, m):
        source, destination = t - 1, t
        # Select IDs from the initial inventory, never from received tasks.
        original_ids = [j for j in range(1, m * m) if original[j] == source]
        selected = original_ids[:m - t]
        assert len(selected) == m - t
        assert all(current[j] == source for j in selected)
        for j in selected:
            current[j] = destination
        actual = real_loads()
        expected = [F(1)] + [F(1) if v < t else F(2 * m - t, m + 1) if v == t else F(m, m + 1) for v in range(1, m)]
        assert actual == expected
        after = max(actual)
        assert after == F(2 * m - t, m + 1)
        assert before - after == F(1, m + 1)
        assert after < before
        assert current[0] == 0
        for owner in range(m):
            assert len({current[j] for j in range(m * m) if original[j] == owner and current[j] != owner}) <= 1
        distance = sum(x != y for x, y in zip(original, current))
        assert distance == t * m - t * (t + 1) // 2
        batches.append({"t": t, "source": source, "destination": destination,
                        "original_small_moved": len(selected),
                        "actual_loads": list(map(str, actual)),
                        "makespan": str(after), "hamming_so_far": distance})
        maxima.append(str(after))
        before = after
    assert before == 1
    assert sum(x != y for x, y in zip(original, current)) == m * (m - 1) // 2
    return {"m": m, "makespans_including_initial": maxima, "batches": batches}


def run():
    identities = [enumerate_identities(m) for m in (2, 3)]
    constructions = []
    for m in range(2, 41):
        constructions.append({"m": m, "big_stays": lifted_chain(m, False), "big_moves": lifted_chain(m, True)})
    sequential = [sequential_batches(m) for m in range(2, 41)]
    # Explicit attack against the false statement that every big-stays repair is a path.
    # job 0 big; jobs 1,2 initially A; 3,4,5 initially B; 6,7,8 initially C.
    old = [0, 0, 0, 1, 1, 1, 2, 2, 2]
    final = [0, 1, 1, 2, 2, 2, 1, 1, 2]
    distance = sum(x != y for x, y in zip(old, final))
    assert distance == 7
    assert Counter(final[1:]) == Counter({1: 4, 2: 4})
    for source in range(3):
        assert len({final[j] for j in range(9) if old[j] == source and final[j] != source}) <= 1
    return {
        "independent_identity_enumeration": identities,
        "identity_preserving_chain_constructions": constructions,
        "sequential_batch_real_load_checks": sequential,
        "cycle_counterexample": {"m": 3, "old": old, "final": final, "hamming": distance},
        "limits": "finite verification; general lower bound is the prefix-cut proof in the independent review",
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
