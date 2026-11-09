"""Exact independent checks of the repeated-site construction on weighted three-site inputs."""
from fractions import Fraction
from itertools import product

SITES = range(3)

def menu(client, layout):
    return [j for j, site in enumerate(layout) if client[0] & (1 << site)]

def loads_of(clients, rows):
    return [sum(weight * row[j] for (_, weight), row in zip(clients, rows)) for j in SITES]

def exact_ne(clients, layout, rows):
    loads = loads_of(clients, rows)
    for client, row in zip(clients, rows):
        _, weight = client
        options = menu(client, layout)
        assert sum(row) == bool(options)
        costs = [weight + loads[j] - weight * row[j] for j in SITES]
        for j in SITES:
            if row[j]:
                assert j in options and costs[j] == min(costs[k] for k in options)
    return loads

def improve(clients, layout, assigned, capped_label=None, cap=None):
    while True:
        loads = [sum(w for (_, w), x in zip(clients, assigned) if x == j) for j in SITES]
        if capped_label is not None:
            assert loads[capped_label] <= cap
        for i, (client, src) in enumerate(zip(clients, assigned)):
            if src is None:
                assert not menu(client, layout)
                continue
            assert src in menu(client, layout)
            for dst in menu(client, layout):
                if loads[src] > loads[dst] + client[1]:
                    assigned[i] = dst
                    break
            else:
                continue
            break
        else:
            return exact_ne(clients, layout, [[int(x == j) for j in SITES] for x in assigned])

def verify(clients):
    covers = [sum(w for mask, w in clients if mask & (1 << j)) for j in SITES]
    A = max(SITES, key=covers.__getitem__)
    R = covers[A]
    outside = [sum(w for mask, w in clients if mask & (1 << j) and not mask & (1 << A)) for j in SITES]
    B = max(SITES, key=outside.__getitem__)
    low = 3 * outside[B] <= 2 * R
    active = (A, A, A if low else B)
    orbit = []
    for mask, _ in clients:
        on_a = mask & (1 << A)
        if on_a:
            orbit.append([Fraction(1, 3)] * 3 if low else [Fraction(1, 2), Fraction(1, 2), 0])
        else:
            orbit.append([0, 0, int(not low and bool(mask & (1 << B)))])
    baseline = exact_ne(clients, active, orbit)
    covered_a = [i for i, (mask, _) in enumerate(clients) if mask & (1 << A)]
    for f, dst in product(SITES, SITES):
        if dst == active[f]:
            continue
        target = tuple(dst if f == j else s for j, s in enumerate(active))
        cap = Fraction(2 * R, 3)
        if low:
            stationary = [j for j in SITES if j != f]
            for labels in product(stationary, repeat=len(covered_a)):
                seed = [f if mask & (1 << dst) else None for mask, _ in clients]
                for i, j in zip(covered_a, labels):
                    seed[i] = j
                boxes = [[w for (_, w), j in zip(clients, seed) if j == s] for s in stationary]
                if all(sum(box) <= cap or len(box) == 1 for box in boxes):
                    break
            else:
                raise AssertionError("Two-bin seed missing")
            continued = improve(clients, target, seed, f, cap)
        else:
            seed = [next(iter(menu(client, target)), None) for client in clients]
            continued = improve(clients, target, seed)
        assert continued[f] <= 2 * baseline[f]
    return low

low_count = 0
for atom_weights in product(range(3), repeat=7):
    clients = [(mask, w) for mask, w in enumerate(atom_weights, 1) if w]
    low_count += verify(clients)
print({"instances": 3**7, "low": low_count, "high": 3**7 - low_count})
