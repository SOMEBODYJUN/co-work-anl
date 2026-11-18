"""Independent exact audit of the frozen B proof's finite certificate core.

The matrix is built column-first from customer membership and the six proved
necessary row families. It does not import the author's matrix builder for
derivation or certificate acceptance. An optional final differential comparison
then checks all coefficients and the author's read-only replay.
"""
from collections import Counter
from fractions import Fraction as Q
from itertools import combinations_with_replacement, permutations, product
from pathlib import Path
import hashlib
import importlib.util
import json
import sys
import time

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[5]
BASE = ROOT / 'research/workspaces/n6-boss3-20261118/informed-b'
OUT = Path(__file__).parent
FREEZE = ROOT / 'research/runs/n6-boss3-20261118/studio/freezes/boss3-B-math-v1/99258d5407253dff5506ea508350b730ba77013a88c7f75823a2a1b7a8514420.json'

def read(path):
    return json.loads(path.read_text())

started = time.perf_counter()
freeze = read(FREEZE)
ledger = []
for ref in freeze['content_refs']:
    data = (ROOT / ref['path']).read_bytes()
    actual = hashlib.sha256(data).hexdigest()
    assert actual == ref['sha256'], ref['path']
    ledger.append({**ref, 'actual_sha256': actual, 'bytes': len(data), 'match': True})

# Each directed edge is the ordered pair (fifth extra, sixth extra).
edges = [(a,b) for a in range(4) for b in range(4) if a != b]
def edge_id(a,b):
    assert a != b
    return 3*a + b - int(b > a)
assert all(edge_id(*edge) == i for i,edge in enumerate(edges))

multisets = list(combinations_with_replacement(range(12),4))
assert len(multisets) == 1365
all_renamings = tuple(permutations(range(4)))
def rename(mode, pi):
    return tuple(edge_id(pi[edges[e][0]], pi[edges[e][1]]) for e in mode)
def graph_canonical(mode):
    # Unlabelled four-edge directed multigraph on the four unused extras.
    return min(tuple(sorted(rename(mode,pi))) for pi in all_renamings)
representatives = sorted({graph_canonical(mode) for mode in multisets})
assert len(representatives) == 69

mapping = read(BASE / 'B-1365-to-69-orbit-map.json')
assert mapping['pairs'] == [list(e) for e in edges]
assert mapping['representatives'] == [list(r) for r in representatives]
assert len(mapping['mapping']) == 1365
map_by_mode = {}
for mode, record in zip(multisets,mapping['mapping']):
    assert record['mode'] == list(mode)
    pi = tuple(record['extra_permutation'])
    order = tuple(record['anchor_order'])
    assert sorted(pi) == sorted(order) == list(range(4))
    moved = rename(mode,pi)
    target = tuple(moved[j] for j in order)
    assert target == graph_canonical(mode)
    assert representatives[record['representative']] == target
    map_by_mode[mode] = record['representative']

# This additionally covers the branch ordering that was quotiented out before
# the provided multiset map; all original four-branch assignments are visited.
raw_orbit_sizes = Counter()
for mode in product(range(12), repeat=4):
    sorted_mode = tuple(sorted(mode))
    assert sorted_mode in map_by_mode
    raw_orbit_sizes[map_by_mode[sorted_mode]] += 1
assert sum(raw_orbit_sizes.values()) == 12**4 == 20736
assert len(raw_orbit_sizes) == 69

# Independent integer-mask enumeration, in the frozen certificate column order:
# E is bit 4 and F0,...,F3 are bits 3,...,0. Outside/all-zero is omitted.
atoms = [(block,mask) for block in range(7) for mask in range(32)
         if block != 6 or mask != 0]
assert len(atoms) == 223
def bit(mask,number):
    return (mask >> (4-number)) & 1
def member(label,block,mask):
    if label < 4:  # four new anchors
        return int(block == label)
    return bit(mask,label-4)  # E,F0,F1,F2,F3
def share(n,denom):
    return Q(n,denom) if n else Q()

def independent_system(mode):
    columns = []
    for block,mask in atoms:
        coeff = [Q(bit(mask,k)) for k in range(5)]
        for j,edge in enumerate(mode):
            a,y = edges[edge]
            fa,fy = bit(mask,a+1),bit(mask,y+1)
            background = bit(mask,0) + int(block in (4,5)) + int(block == j)
            total = background + fa + fy
            u,v = share(fa,total),share(fy,total)
            w = share(int(block == j),total)
            coeff.extend((w,-u,-v))
            for label in range(9):
                q = member(label,block,mask)
                coeff.append(share(q,background+fa+q)-v)
            for label in range(9):
                q = member(label,block,mask)
                coeff.append(share(q,background+2)-u)
            for k in range(4):
                if k != j:
                    own_discount = Q(bit(mask,0)*int(block == k),2)
                    other_discount = sum((Q(bit(mask,0)*int(block == l),4)
                                          for l in range(4) if l not in (j,k)),Q())
                    coeff.append(-u-own_discount-other_discount)
            for t,q in product(range(4), repeat=2):
                mt,mq = bit(mask,t+1),bit(mask,q+1)
                immediate_t = share(mt,background+mt)
                terminal_query = share(mq,background+mt+mq)
                coeff.append(immediate_t+terminal_query-u)
        assert len(coeff) == 165
        columns.append(coeff)
    gamma = [Q()]*165
    for j in range(4):
        gamma[5+40*j] = Q(-1)
    columns.append(gamma)
    matrix = [list(v) for v in zip(*columns)]
    rhs = [Q(1)]*5
    for _ in range(4):
        rhs.extend([Q(),-Q(7,12),-Q(7,12)] + [Q()]*18 + [Q(-1)]*3 + [Q(1)]*16)
    equalities = [[Q(int(block == k)) for block,_ in atoms]+[Q()] for k in range(6)]
    assert len(matrix) == len(rhs) == 165 and len(columns) == 224
    return matrix,rhs,equalities

bundle = read(BASE / 'B-all-orbit-rational-certificates.json')
assert bundle['failures'] == []
assert len(bundle['certificates']) == len(bundle['float_results']) == 69
assert [tuple(c['mode']) for c in bundle['certificates']] == representatives
assert [tuple(c['mode']) for c in bundle['float_results']] == representatives

summaries = []
systems = []
for mode,cert in zip(representatives,bundle['certificates']):
    A,b,E = independent_system(mode)
    systems.append((A,b,E))
    entries = cert['inequality_dual']
    assert len({i for i,_ in entries}) == len(entries)
    assert all(type(i) is int and 0 <= i < 165 for i,_ in entries)
    multipliers = [(i,Q(v)) for i,v in entries]
    assert all(v <= 0 for _,v in multipliers)
    equality_dual = tuple(Q(v) for v in cert['equality_dual'])
    assert len(equality_dual) == 6
    residual = []
    for col in range(224):
        lhs = sum((v*A[i][col] for i,v in multipliers),Q())
        lhs += sum((e*row[col] for e,row in zip(equality_dual,E)),Q())
        reduced = Q(int(col == 223)) - lhs
        assert reduced >= 0,(mode,col,reduced)
        residual.append(reduced)
    bound = sum((v*b[i] for i,v in multipliers),Q()) + sum(equality_dual,Q())
    assert bound == Q(cert['bound']) and bound >= Q(1,2)
    summaries.append({'mode':list(mode), 'bound':str(bound),
                      'nonzero_dual_rows':len(entries),
                      'minimum_reduced_cost':str(min(residual)),
                      'zero_reduced_cost_columns':sum(x == 0 for x in residual)})
minimum = min(Q(s['bound']) for s in summaries)
assert minimum == Q(325,632)
frozen_replay = read(BASE / 'B-all-orbit-exact-replay.json')
assert frozen_replay['summaries'] == summaries
assert frozen_replay['minimum_dual_bound'] == str(minimum)

# Secondary differential check only after independent certificate acceptance.
spec = importlib.util.spec_from_file_location('author_B_readonly_verifier',BASE / 'verify_B_all_orbits.py')
author = importlib.util.module_from_spec(spec)
spec.loader.exec_module(author)
assert author.TYPES == [(block,tuple(bit(mask,k) for k in range(5))) for block,mask in atoms]
for mode,(A,b,E) in zip(representatives,systems):
    their_A,their_b,their_E,_ = author.build(mode)
    assert (A,b,E) == (their_A,their_b,their_E)
author_replay = author.verify()  # function is read-only; __main__ is not run
assert author_replay == frozen_replay

result = {
    'freeze_revision_pin':FREEZE.stem, 'hash_checks':ledger,
    'independent_builder':{
        'method':'Column-first characteristic membership algebra, integer masks, Fraction; no author imports for derivation or acceptance',
        'client_types':len(atoms), 'columns_per_mode':224,
        'inequalities_per_mode':165, 'equalities_per_mode':6,
        'independently_accepted_certificates':len(summaries),
        'independently_checked_dual_columns':69*224,
        'minimum_bound':str(minimum),
        'full_matrix_coefficients_equal_author_after_independent_acceptance':True,
    },
    'mode_coverage':{
        'ordered_distinct_extra_pairs':12,
        'original_ordered_four_branch_patterns':20736,
        'multisets':len(multisets), 'extra_renaming_orbits':len(representatives),
        'checked_mapping_records':len(map_by_mode),
        'all_original_ordered_patterns_covered':True,
        'raw_pattern_counts_by_representative':[raw_orbit_sizes[i] for i in range(69)],
    },
    'author_readonly_replay_matches_frozen_output':True,
    'summaries':summaries,
    'scope':'Exact rational necessary-model certificates for all B double-extra patterns. Mathematical SPE-to-row and symmetry validity are separately reviewed in review-B-math-v1.md; not an all-SPE enumeration or A/C/root-half theorem.',
    'elapsed_seconds':time.perf_counter()-started,
}
(OUT / 'independent-audit-results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ('hash_checks','summaries')},indent=2))
