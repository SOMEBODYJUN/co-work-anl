"""Exact extraction from one bounded-congestion DAG certificate.

The standard interfaces validate/extract/find_certificate/min_certificate
are bit-polynomial.
The main audit is finite and does not decide the general certificate-search
problem.  Stdlib only; inputs are integers or fractions.Fraction, never float.
Default output is JSON to stdout and does not overwrite frozen evidence.
"""
from collections import deque
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib
import json
import platform


def _structure(n, edges, k, K, W, root):
    """Validate just the original graph and the supplied support."""
    if type(n) is not int or n < 1:
        raise ValueError('vertex count')
    if type(root) is not int or not 0 <= root < n:
        raise ValueError('root')
    if type(K) is not int or K < 1:
        raise ValueError('K must be a positive integer')
    if len(k) != n or any(type(a) is not int or a < 0 for a in k):
        raise ValueError('nonnegative integer demands')
    normalized_edges = []
    out = [[] for _ in range(n)]
    indegree = [0] * n
    for edge in edges:
        if not isinstance(edge, (tuple, list)) or len(edge) != 2:
            raise ValueError('edge format')
        u, v = edge
        if (type(u) is not int or type(v) is not int or
                not 0 <= u < n or not 0 <= v < n or u == v):
            raise ValueError('edge endpoints')
        normalized_edges.append((u, v))
        out[u].append(v)
        indegree[v] += 1
    if len(normalized_edges) != len(set(normalized_edges)):
        raise ValueError('parallel edges')
    if indegree[root]:
        raise ValueError('root must have indegree zero')
    if any(k[v] == 0 and out[v] for v in range(n)):
        raise ValueError('zero-demand vertices must be terminals')
    queue = deque(v for v in range(n) if indegree[v] == 0)
    topological_count = 0
    while queue:
        v = queue.popleft()
        topological_count += 1
        for w in out[v]:
            indegree[w] -= 1
            if indegree[w] == 0:
                queue.append(w)
    if topological_count != n:
        raise ValueError('graph must be acyclic')
    chosen = list(W)
    if any(type(v) is not int or not 0 <= v < n for v in chosen):
        raise ValueError('support vertices')
    if len(chosen) != len(set(chosen)) or root not in chosen:
        raise ValueError('support must contain root and have no duplicates')
    support = set(chosen)
    allowed = sorted((u, v) for u, v in normalized_edges
                     if u in support and v in support)
    return {'n': n, 'edges': allowed, 'k': list(k), 'K': K,
            'W': sorted(support), 'root': root,
            'high': {v for v in support if k[v] >= K},
            'low': {v for v in support if 0 < k[v] < K},
            'terminals': {v for v in support if k[v] == 0}}


def validate(n, edges, k, K, W, flow, root=0):
    """Validate the graph and the complete, non-circular flow certificate.

    W is a supplied root-containing vertex subset.  Unlisted flow edges have
    value zero.  On W, high vertices have k[v] >= K, low vertices have
    0 < k[v] < K, and terminals have k[v] == 0.  Every nonroot inflow is at
    most K.  High outflow is at least k[v].  Nonroot low vertices conserve
    flow.  A low root has outflow at least K.  K is a positive INTEGER.

    Positive-demand vertices outside W are unconstrained by the certificate;
    the original graph, including all such vertices, must still be a DAG.
    """
    structure = _structure(n, edges, k, K, W, root)
    support = set(structure['W'])
    allowed = structure['edges']
    allowed_set = set(allowed)
    if not hasattr(flow, 'items'):
        raise ValueError('flow must map original edges to exact values')
    exact = {}
    incoming = [F(0) for _ in range(n)]
    outgoing = [F(0) for _ in range(n)]
    for edge, value in flow.items():
        if edge not in allowed_set:
            raise ValueError('flow edge is not in the supported graph')
        if type(value) is not int and not isinstance(value, F):
            raise ValueError('flow values must be integers or Fraction')
        value = F(value)
        if value < 0:
            raise ValueError('negative flow')
        exact[edge] = value
        u, v = edge
        outgoing[u] += value
        incoming[v] += value
    high, low = structure['high'], structure['low']
    for v in support:
        if v != root and incoming[v] > K:
            raise ValueError('vertex congestion exceeds K')
        if v in high and outgoing[v] < k[v]:
            raise ValueError('high vertex has insufficient supply')
        if v in low:
            if v == root:
                if outgoing[v] < K:
                    raise ValueError('low root must supply at least K')
            elif incoming[v] != outgoing[v]:
                raise ValueError('low corridor fails flow conservation')
    q = {v: k[v] // K for v in high}
    if root in low:
        q[root] = 1
    supported_outdegree = {v: 0 for v in support}
    for u, v in allowed:
        supported_outdegree[u] += 1
    # These follow from the checked certificate: every original edge carries
    # at most K, because its head is nonroot and has inflow at most K.
    if any(q[v] > supported_outdegree[v] for v in q):
        raise AssertionError('certificate contradicts source capacity bound')
    if sum(q.values()) > len(allowed):
        raise AssertionError('certificate contradicts total capacity bound')
    structure.update({'flow': exact, 'q': q})
    return structure


class _IntegralFlow:
    """Edmonds-Karp with exact integers; O(V E^2) arithmetic operations.

    In extraction the stronger bound of <= |E_original| augmentations holds.
    In certificate search, use the shortest-augmenting-path bound instead:
    capacities may be huge binary integers and flow-value bounds would not
    establish bit-polynomial running time.
    """
    def __init__(self, n):
        self.adj = [[] for _ in range(n)]
        self.arcs = []

    def add(self, u, v, capacity):
        index = len(self.arcs)
        self.arcs.extend([[u, v, capacity, capacity], [v, u, 0, 0]])
        self.adj[u].append(index)
        self.adj[v].append(index + 1)
        return index

    def used(self, index):
        return self.arcs[index][3] - self.arcs[index][2]

    def solve(self, source, sink):
        value = 0
        augmentations = 0
        while True:
            parent = [None] * len(self.adj)
            parent[source] = -1
            queue = deque([source])
            while queue and parent[sink] is None:
                u = queue.popleft()
                for index in self.adj[u]:
                    _, v, residual, _ = self.arcs[index]
                    if residual and parent[v] is None:
                        parent[v] = index
                        queue.append(v)
            if parent[sink] is None:
                return value, augmentations
            delta = None
            v = sink
            while v != source:
                index = parent[v]
                capacity = self.arcs[index][2]
                delta = capacity if delta is None else min(delta, capacity)
                v = self.arcs[index][0]
            v = sink
            while v != source:
                index = parent[v]
                self.arcs[index][2] -= delta
                self.arcs[index ^ 1][2] += delta
                v = self.arcs[index][0]
            value += delta
            augmentations += 1


def find_certificate(n, edges, k, K, W, root=0):
    """Find this contract's certificate for FIXED W,K, or return None.

    This is one integer maximum flow with binary capacities.  BFS residual
    augmentations are Edmonds-Karp: shortest residual distances never
    decrease, and each directed residual arc can be critical O(V) times.
    Hence O(V E) augmentations and O(V E^2) arithmetic operations, independent
    of the numerical flow value.  All integers have polynomial bit length.
    The function does not choose W or promise a bounded K on general inputs.
    """
    structure = _structure(n, edges, k, K, W, root)
    source, sink = 2 * n, 2 * n + 1
    network = _IntegralFlow(2 * n + 2)
    source_arcs = {}
    required = 0
    for v in structure['W']:
        vin, vout = 2 * v, 2 * v + 1
        supply = k[v] if v in structure['high'] else K if v == root and k[v] else 0
        if supply:
            source_arcs[v] = network.add(source, vout, supply)
            required += supply
        if v in structure['high'] or v in structure['terminals']:
            network.add(vin, sink, K)
        elif v != root:
            network.add(vin, vout, K)
    original_arcs = {}
    for u, v in structure['edges']:
        original_arcs[(u, v)] = network.add(2 * u + 1, 2 * v, K)
    value, _ = network.solve(source, sink)
    if value != required:
        return None
    if any(network.used(index) != network.arcs[index][3]
           for index in source_arcs.values()):
        raise AssertionError('max-flow value did not saturate every source')
    f = {edge: network.used(index) for edge, index in original_arcs.items()
         if network.used(index)}
    validate(n, structure['edges'], k, K, structure['W'], f, root)
    return f


def min_certificate(n, edges, k, W, root=0):
    """Find the least feasible positive INTEGER K for fixed W, or None.

    Feasibility is monotone in K, even though the high/low partition changes.
    For K1 <= K2 normalize an old certificate as g=f/K1, then process the DAG
    topologically, keeping each new edge weight <= its old g weight.  A new
    high vertex sends exactly k/K2; a new nonroot low vertex sends its new
    incoming amount; a new low root sends 1.  Each requested amount fits:
    an old high has outgoing >=1 >= incoming, and an old low conserves flow.
    Multiplying the new weights by K2 gives the new certificate.

    U=1+max(k[v]:v in W) makes every positive vertex low.  The upper instance
    is feasible iff root has a supported path to a terminal (including the
    length-zero path for a terminal root).  This function verifies it by the
    actual finder, then uses O(log U) finder calls.  A terminal root does not
    imply K=1: high vertices elsewhere in W still carry source obligations.
    """
    structure = _structure(n, edges, k, 1, W, root)
    fixed_edges, fixed_W = structure['edges'], structure['W']
    upper = 1 + max(k[v] for v in fixed_W)
    witness = find_certificate(n, fixed_edges, k, upper, fixed_W, root)
    if witness is None:
        return None
    lower = 1
    while lower < upper:
        middle = (lower + upper) // 2
        candidate = find_certificate(n, fixed_edges, k, middle, fixed_W, root)
        if candidate is None:
            lower = middle + 1
        else:
            upper, witness = middle, candidate
    validate(n, fixed_edges, k, lower, fixed_W, witness, root)
    return lower, witness


def extract(n, edges, k, K, W, flow, root=0):
    """Return actual original edges of a rooted arborescence of score >=
    1/(2K-1), after one integral maximum flow.  No demand-sized loops.
    """
    cert = validate(n, edges, k, K, W, flow, root)
    if k[root] == 0:
        return []
    source, sink = 2 * n, 2 * n + 1
    network = _IntegralFlow(2 * n + 2)
    source_arcs = {}
    for v in cert['W']:
        vin, vout = 2 * v, 2 * v + 1
        if v in cert['q']:
            source_arcs[v] = network.add(source, vout, cert['q'][v])
        if v in cert['high'] or v in cert['terminals']:
            network.add(vin, sink, 1)
        elif v != root:
            network.add(vin, vout, 1)
    original_arcs = {}
    for u, v in cert['edges']:
        original_arcs[(u, v)] = network.add(2 * u + 1, 2 * v, 1)
    value, augmentations = network.solve(source, sink)
    required = sum(cert['q'].values())
    if value != required or any(network.used(index) != cert['q'][v]
                                for v, index in source_arcs.items()):
        raise AssertionError('valid certificate failed to saturate every source')
    if augmentations > required or required > len(cert['edges']):
        raise AssertionError('augmentation bound')
    selected = [edge for edge, index in original_arcs.items()
                if network.used(index)]
    out = [[] for _ in range(n)]
    incoming = [0] * n
    for u, v in selected:
        out[u].append(v)
        incoming[v] += 1
    if incoming[root] or any(x > 1 for x in incoming):
        raise AssertionError('integer flow reused a vertex')
    reached = {root}
    queue = deque([root])
    while queue:
        v = queue.popleft()
        for w in out[v]:
            if w in reached:
                raise AssertionError('integer flow produced a cycle/reused child')
            reached.add(w)
            queue.append(w)
    result = sorted((u, v) for u, v in selected if u in reached)
    alpha = F(1, 2 * K - 1)
    for v in reached:
        if k[v] and F(len(out[v]), k[v]) < alpha:
            raise AssertionError('output degree ratio')
    return result


def _score(n, tree, k, root):
    """Small, separate tree verifier used only by the finite audit."""
    if len(tree) != len(set(tree)):
        raise AssertionError('duplicate tree edge')
    deg = [0] * n
    indeg = [0] * n
    for u, v in tree:
        deg[u] += 1
        indeg[v] += 1
    if indeg[root] or any(d > 1 for d in indeg):
        raise AssertionError('tree indegrees')
    reached = {root}
    for _ in range(n):
        reached |= {v for u, v in tree if u in reached}
    if any(u not in reached or v not in reached for u, v in tree):
        raise AssertionError('disconnected tree')
    if len(tree) != len(reached) - 1:
        raise AssertionError('tree edge count')
    return min([F(1)] + [F(deg[v], k[v]) for v in reached if k[v]])


def sharp_family(K):
    """Explicit rational certificate with exact tree optimum 1/(2K-1).

    K >= 2.  Layers have sizes a[0]=1 and
    a[l+1]=ceil((2K-1)*a[l]/K), and consecutive layers are complete
    bipartite.  The last layer has 2**d-1 terminals, where
    d=ceil(log2(K))+1, so a binary tree of depth d cannot fit.
    This audit-family generator takes time polynomial in its explicit output
    size, not in log(K); it is not one of the bit-polynomial solver interfaces.
    """
    if type(K) is not int or K < 2:
        raise ValueError('sharp family requires integer K >= 2')
    positive_demand = 2 * K - 1
    depth = (K - 1).bit_length() + 1
    sizes = [1]
    for _ in range(depth):
        sizes.append((positive_demand * sizes[-1] + K - 1) // K)
    layers = []
    n = 0
    for size in sizes:
        layers.append(list(range(n, n + size)))
        n += size
    edges = [(u, v) for left, right in zip(layers, layers[1:])
             for u in left for v in right]
    f = {(u, v): F(positive_demand, len(right))
         for left, right in zip(layers, layers[1:])
         for u in left for v in right}
    k = [positive_demand] * (n - sizes[-1]) + [0] * sizes[-1]
    assert sizes[-1] == 2 ** depth - (2 ** (depth - 1) // K)
    assert sizes[-1] == 2 ** depth - 1
    return (n, edges, k, K, list(range(n)), f, 0), sizes


def main():
    checked = accepted = 0
    expected_feasibility = {}
    for n in range(1, 4):
        possible = [(u, v) for u in range(n) for v in range(u + 1, n)]
        for mask in product([0, 1], repeat=len(possible)):
            edges = [e for e, bit in zip(possible, mask) if bit]
            for k in product(range(4), repeat=n):
                if any(k[u] == 0 for u, v in edges):
                    continue
                for wbits in product([0, 1], repeat=n - 1):
                    W = [0] + [v for v, bit in zip(range(1, n), wbits) if bit]
                    allowed = [e for e in edges if e[0] in W and e[1] in W]
                    for K in range(1, 4):
                        key = (n, tuple(edges), tuple(k), K, tuple(W))
                        expected_feasibility[key] = False
                        for values in product(range(K + 1), repeat=len(allowed)):
                            checked += 1
                            f = dict(zip(allowed, values))
                            try:
                                validate(n, edges, k, K, W, f)
                            except ValueError:
                                continue
                            tree = extract(n, edges, k, K, W, f)
                            assert set(tree) <= set(edges)
                            assert _score(n, tree, k, 0) >= F(1, 2 * K - 1)
                            accepted += 1
                            expected_feasibility[key] = True
    finder_feasible = 0
    feasibility_by_support = {}
    for key, expected in expected_feasibility.items():
        n, edges, k, K, W = key
        f = find_certificate(n, edges, k, K, W)
        assert (f is not None) == expected
        group = (n, edges, k, W)
        feasibility_by_support.setdefault(group, {})[K] = expected
        if f is not None:
            finder_feasible += 1
            tree = extract(n, edges, k, K, W, f)
            assert _score(n, tree, k, 0) >= F(1, 2 * K - 1)
    minimum_feasible = 0
    for group, outcomes in feasibility_by_support.items():
        n, edges, k, W = group
        finite = [outcomes[K] for K in sorted(outcomes)]
        assert finite == sorted(finite)
        minimum = min_certificate(n, edges, k, W)
        upper = 1 + max(k[v] for v in W)
        # Our bounded oracle stops at K=3.  At the only remaining upper K=4,
        # all k<=3 are low; existence is exactly a root-to-terminal path.
        reached = {0}
        for _ in range(n):
            reached |= {v for u, v in edges if u in reached and u in W and v in W}
        terminal_reachable = any(k[v] == 0 for v in reached)
        expected_min = next((K for K in sorted(outcomes) if outcomes[K]),
                            upper if terminal_reachable else None)
        assert (None if minimum is None else minimum[0]) == expected_min
        if minimum is not None:
            minimum_feasible += 1
            K, f = minimum
            validate(n, edges, k, K, W, f)
    special = [
        (5, [(0, 1), (0, 2), (1, 3), (2, 3), (2, 4)],
         [3, 1, 1, 0, 0], 2, [0, 1, 2, 3, 4],
         {(0, 1): F(3, 2), (0, 2): F(3, 2), (1, 3): F(3, 2),
          (2, 3): F(1, 2), (2, 4): 1}, 0),
        (6, [(0, 1), (0, 2), (1, 3), (2, 3), (2, 5), (3, 4)],
         [3, 1, 1, 1, 0, 0], 2, list(range(6)),
         {(0, 1): 1, (0, 2): 2, (1, 3): 1, (2, 3): 1,
          (2, 5): 1, (3, 4): 2}, 0),
        (4, [(3, 2), (2, 1), (1, 0)], [0, 1, 1, 1], 2,
         [0, 1, 2, 3], {(3, 2): 2, (2, 1): 2, (1, 0): 2}, 3),
        (3, [(2, 0), (2, 1)], [0, 0, 5], 3, [0, 1, 2],
         {(2, 0): 3, (2, 1): 2}, 2),
        (3, [(0, 1)], [1, 0, 10 ** 100], 2, [0, 1], {(0, 1): 2}, 0),
        (3, [(2, 0), (2, 1)], [0, 0, 2 * 10 ** 100 - 1],
         10 ** 100, [0, 1, 2], {(2, 0): 10 ** 100,
                                  (2, 1): 10 ** 100 - 1}, 2),
        (1, [], [0], 10 ** 100, [0], {}, 0),
    ]
    rows = []
    for case in special:
        n, edges, k, K, W, f, root = case
        tree = extract(*case)
        score = _score(n, tree, k, root)
        assert score >= F(1, 2 * K - 1)
        found = find_certificate(n, edges, k, K, W, root)
        assert found is not None
        recovered_tree = extract(n, edges, k, K, W, found, root)
        assert _score(n, recovered_tree, k, root) >= F(1, 2 * K - 1)
        rows.append({'n': n, 'edges': edges, 'demands': k, 'K': K,
                     'W': W, 'root': root,
                     'flow': [{'edge': e, 'value': str(a)} for e, a in f.items()],
                     'tree': tree, 'score': str(score),
                     'guarantee': str(F(1, 2 * K - 1))})
    # A long low-demand corridor incurs the same guarantee, independent of depth.
    depth = 1000
    chain = [(v, v + 1) for v in range(depth)]
    tree = extract(depth + 1, chain, [1] * depth + [0], 2,
                   list(range(depth + 1)), {e: 2 for e in chain})
    assert tree == chain
    huge_K = 10 ** 100
    assert find_certificate(2, [(0, 1)], [1, 0], huge_K, [0, 1]) == {(0, 1): huge_K}
    assert find_certificate(2, [(0, 1)], [2 * huge_K, 0], huge_K, [0, 1]) is None
    assert find_certificate(2, [], [huge_K, 0], huge_K, [0, 1]) is None
    assert min_certificate(2, [(0, 1)], [huge_K, 0], [0, 1])[0] == huge_K
    assert min_certificate(2, [], [0, huge_K], [0, 1])[0] == huge_K + 1
    assert min_certificate(2, [], [huge_K, 0], [0, 1]) is None
    assert min_certificate(1, [], [0], [0]) == (1, {})
    sharp_rows = []
    for K in range(2, 17):
        case, sizes = sharp_family(K)
        tree = extract(*case)
        n, edges, k, _, _, _, root = case
        score = _score(n, tree, k, root)
        assert score == F(1, 2 * K - 1)
        found = find_certificate(n, edges, k, K, case[4])
        assert found is not None
        assert _score(n, extract(n, edges, k, K, case[4], found), k, root) == score
        oracle_maximum = None
        if K == 2:
            oracle_maximum = F(0)
            for mask in product([0, 1], repeat=len(edges)):
                candidate = [e for e, bit in zip(edges, mask) if bit]
                try:
                    candidate_score = _score(n, candidate, k, root)
                except AssertionError:
                    continue
                oracle_maximum = max(oracle_maximum, candidate_score)
            assert oracle_maximum == score
        sharp_rows.append({'K': K, 'layer_sizes': sizes,
                           'vertices': n, 'edges': len(edges),
                           'terminal_capacity': sizes[-1],
                           'binary_tree_terminals_required': 2 ** (len(sizes) - 1),
                           'extracted_score': str(score),
                           'edge_subset_oracle_optimum':
                           None if oracle_maximum is None else str(oracle_maximum)})
    bad = [
        (1, [], [1], 0, [0], {}, 0),
        (1, [], [0], True, [0], {}, 0),
        (1, [], [0], F(3, 2), [0], {}, 0),
        (2, [(0, 1)], [1, 0], 2, [0, 1], {(0, 1): 1}, 0),
        (2, [(0, 1)], [1, 0], 2, [0, 1], {(0, 1): 2.0}, 0),
        (2, [(0, 1)], [1, 0], 2, [0, 1], {(0, 1): -1}, 0),
        (2, [(0, 1)], [3, 0], 2, [0, 1], {(0, 1): 2}, 0),
        (2, [(0, 1)], [3, 0], 2, [0, 1], {(0, 1): 3}, 0),
        (3, [(0, 1), (1, 2)], [1, 1, 0], 2, [0, 1, 2],
         {(0, 1): 2, (1, 2): 1}, 0),
        (2, [(0, 1)], [1, 0], 2, [1], {}, 0),
        (2, [(0, 1)], [1, 0], 2, [0, 0, 1], {}, 0),
        (2, [(0, 1)], [1, 0], 2, [0], {(0, 1): 2}, 0),
        (2, [(0, 1), (0, 1)], [1, 0], 2, [0, 1], {}, 0),
        (2, [(0, 1), (1, 0)], [1, 1], 2, [0, 1], {}, 0),
        (2, [(0, 1)], [0, 0], 2, [0, 1], {}, 0),
        (2, [(0, 1)], [1, 0], 2, [0, 1], {}, 1),
        (1, [], [True], 1, [0], {}, 0),
        (2, [(0, 1)], [1, 0], 2, [0, 1], {(0, 1): 2}, True),
        (3, [(0, 1)], [1, 0, 10 ** 100], 2, [0, 1, 2], {(0, 1): 2}, 0),
    ]
    for case in bad:
        try:
            validate(*case)
        except ValueError:
            pass
        else:
            raise AssertionError('invalid certificate accepted: ' + repr(case))
    # Integer K is substantive: the same floor bound is false at K=6/5,k=2.
    rational_K = F(6, 5)
    assert F(2 // rational_K, 2) == F(1, 2) < 1 / (2 * rational_K - 1)
    print(json.dumps({
        'title': '有向需求树共同拥塞证书的一次整数流精确审计',
        'python': platform.python_version(),
        'precision': 'integers / fractions.Fraction; exact',
        'seed': None,
        'code_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'enumerated_certificate_assignments': checked,
        'accepted_certificates_extracted': accepted,
        'fixed_support_search_instances': len(expected_feasibility),
        'fixed_support_search_feasible': finder_feasible,
        'fixed_support_search_oracle': 'exhaustive integer edge flows in 0..K for n<=3',
        'minimum_congestion_support_instances': len(feasibility_by_support),
        'minimum_congestion_feasible_supports': minimum_feasible,
        'monotonicity_checked_K': [1, 2, 3],
        'special_cases': rows,
        'low_corridor_depth_checked': depth,
        'sharp_family_cases': sharp_rows,
        'invalid_cases_rejected': len(bad),
        'limits': ('Finite certificate enumeration only. The theorem is conditional '
                   'on the explicit certificate; no general support-selection or '
                   'constant-K search theorem, no UM-TARGET-v1 algorithm.')
    }, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
