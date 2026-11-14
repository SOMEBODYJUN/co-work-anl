import ast
import json
import math
from collections import Counter, defaultdict
from fractions import Fraction as Q
from functools import lru_cache
from hashlib import sha256
from itertools import combinations_with_replacement, product
from pathlib import Path

root = Path.cwd()
archive = root / 'archives/customer-attraction'
evidence = archive / 'tools/evidence'
menu_root = evidence / 'root-menu-four-boss3'
read = lambda path: json.loads(path.read_text())
old_path = next((menu_root / 'related').rglob('enhanced_2396_exact_obstruction.json'))
exact_path = next((menu_root / 'original').glob('667891e62cfa307ad184/*'))
float_path = next((menu_root / 'original').glob('92626fe69b07b30088e9/*'))
hist_path = evidence / 'global-indexed-reviews-boss3/related/root_full_hist_completion_exact.json'
hist_discovery_path = hist_path.with_name('root_full_hist_completion.json')
float_report = read(float_path)
exact_report = read(exact_path)
replay = read(menu_root / 'replay/original-return-observation.json')
review = read(menu_root / 'replay/input-contract-review.json')
old = read(old_path)['atom_masses']
assert len(old) == 38 and all(Q(a['mass']) > 0 for a in old)
assert exact_path.read_bytes() == (menu_root / 'replay/root_menu_completion_exact.json').read_bytes()
for row in read(menu_root / 'source-manifest.json'):
    copy = menu_root / 'original' / row['id'] / Path(row['path']).name
    assert copy.stat().st_size == row['size'] and sha256(copy.read_bytes()).hexdigest() == row['sha256']

labels = 'ABCDEUVWXY'
paths = {'actual': 'ABCDE', 'second': 'AEUVW', 'third': 'ABEXY'}
bitvectors = list(product(range(2), repeat=4))
menus = [(label, 1) for label in labels] + [('T', 5)] + [(f'L{i}', 5) for i in range(3)]
for tag, chars in [('AB', 'XY'), ('AE', 'XY'), ('S', 'UVW')]:
    menus.extend((f'{tag}:{c}', 5) for c in chars)
counts = []
for atom in old:
    bits = tuple(map(int, atom['bits']))
    assert len(bits) == 10 and all(bit in (0,1) for bit in bits)
    triples = tuple(product(range(2), repeat=3))
    histograms = [(atom['AB_hist'], triples), (atom['AE_hist'], triples), (atom['second_hist'], bitvectors)]
    assert all(len(hist) == len(types) and sum(hist) == 5 and all(type(n) is int and n >= 0 for n in hist) for hist, types in histograms)
    assert all(sum(hist[i] for i, mode in enumerate(types) if mode[0]) == 1 for hist, types in histograms)
    assert all(0 <= h <= 1 and 0 <= ell - h <= 4 for ell, h in atom['menus_lh'])
    row = list(bits) + [1] + [pair[0] for pair in atom['menus_lh']]
    for hist, types in histograms:
        for axis in range(1,len(types[0])):
            row.append(sum(m for m, mode in zip(hist, types) if mode[axis]))
    counts.append(row)

groups = [(i, t) for i in range(38) for t in range(2)]
cells = [(i, t, v) for i, t in groups for v in bitvectors]
assert float_report['groups'] == [list(group) for group in groups]
assert float_report['variables_spec'] == [[i, t, list(v)] for i, t, v in cells]
rows = [('root:exact-opt', ['root'])]
for j in range(4):
    rows.extend((f'rootreply:{j}:menu:{nm}', ['menu', j, nm]) for nm, _ in menus)
    rows.extend((f'rootreply:{j}:own:{pos}', ['own', j, pos]) for pos in range(5) if (j,pos) != (3,4))
for name, start in zip(paths, (0,2,3)):
    rows.extend((f'{name}:{j}:new-root-menu:{k}', ['reverse', name, j, k]) for j in range(start,5) for k in range(4))
for r in (4,3):
    rows.extend((f'root:r{r}:profit:'+''.join(labels[i] for i in ids), ['profit', r, list(ids)]) for ids in combinations_with_replacement(range(10), r))
rows.extend((f'root:r2:tax:{menus[i][0]}|{menus[j][0]}', ['tax', i, j]) for i,j in combinations_with_replacement(range(21), 2))
assert len(rows) == 1310 and len({row[0] for row in rows}) == 1310
assert float_report['row_names'] == [name for name, spec in rows]
assert float_report['row_specs'] == [spec for name, spec in rows]
assert review['all_14_top_level_float_fields_read'] == list(float_report)
assert review['row_families'] == dict(Counter(spec[0] for _, spec in rows))
assert all(math.isfinite(value) for field in ('point','dual_rows','dual_equalities') for value in float_report[field])
assert all(value >= 0 for field in ('point','dual_rows') for value in float_report[field])
assert review['float_margin'] == float_report['margin']
assert review['float_dual_rows_sum_as_exact_stored_binary_numbers'] == str(sum(map(Q,float_report['dual_rows'])))
assert review['positive_float_columns'] == [dict(index=i,variable=float_report['variables_spec'][i],value=x) for i,x in enumerate(float_report['point']) if x]
assert review['all_nonzero_float_inequality_multipliers'] == [dict(index=i,name=rows[i][0],value=x) for i,x in enumerate(float_report['dual_rows']) if x]
assert review['all_equality_multipliers'] == [dict(group=list(group),value=x) for group,x in zip(groups,float_report['dual_equalities'])]

original = {(a['atom'],a['t'],tuple(a['replies'])): Q(a['mass']) for a in exact_report['positive_refinements']}
assert len(original) == 92 and set(original) <= set(cells) and all(mass > 0 for mass in original.values())
vector = [Q(x).limit_denominator(10**9) for x in float_report['point']]
positive_groups = Counter()
for j,(i,t) in enumerate(groups):
    block = slice(16*j, 16*(j+1))
    block_mass = Q(old[i]['mass'])*(1 if t else 4)/5
    correction = block_mass - sum(vector[block])
    chosen = 16*j + vector[block].index(max(vector[block]))
    assert correction
    vector[chosen] += correction
    assert min(vector[block]) >= 0 and sum(vector[block]) == block_mass
    positive = sum(x > 0 for x in vector[block]); positive_groups[positive] += 1
    assert replay['all_76_exact_mass_groups'][j] == dict(atom=i, t=t, target_mass=str(block_mass),actual_mass=str(block_mass),positive_cells=positive,rounding_mass_correction=[dict(index=chosen,correction=str(correction))])
assert replay['positive_cell_distribution_per_group'] == {str(k): v for k,v in positive_groups.items()}
assert replay['groups_with_nonzero_mass_repair'] == 76
assert replay['full_recovered_vector'] == list(map(str, vector))
assert replay['positive_indices'] == [i for i,x in enumerate(vector) if x]
assert original == {cell: x for cell,x in zip(cells, vector) if x}

hist_report = read(hist_path)
hist_discovery = read(hist_discovery_path)
assert hist_discovery['row_names'][:1310] == float_report['row_names']
assert hist_discovery['row_specs'][:1310] == float_report['row_specs']
assert hist_discovery['row_specs'][1310:] == [['off', j, k] for j,k in product(range(4),repeat=2)]
projected = defaultdict(Q)
seen = set()
for rec in hist_report['positive_histograms']:
    i, histogram, mass = rec['atom'], rec['histogram'], Q(rec['mass'])
    key = (i,tuple((t, tuple(v), n) for t,v,n in histogram))
    assert key not in seen and mass > 0
    seen.add(key)
    assert sum(n for t,v,n in histogram) == 5 and sum(t*n for t,v,n in histogram) == 1
    assert len({(t,tuple(v)) for t,v,n in histogram}) == len(histogram)
    for t,v,n in histogram:
        cell = (i,t,tuple(v))
        assert cell in original or cell in cells
        assert type(n) is int and n > 0
        projected[cell] += mass*n/5
assert len(seen) == hist_report['positive_columns'] == 53
for point in (original, projected):
    for i,t in groups:
        assert sum(mass for (j,u,v),mass in point.items() if (i,t)==(j,u)) == Q(old[i]['mass'])*(1 if t else 4)/5

ratio = lambda n,d: Q(n,d) if n else Q()
menu_pos = {nm:i for i,(nm,s) in enumerate(menus)}
def score(spec, cell):
    i,t,v = cell
    bits = counts[i][:10]
    share = [ratio(b, t+sum(v)) for b in v]
    kind,*args = spec
    if kind == 'root':
        return ratio(bits[0],sum(bits[:5])) - ratio(t,t+sum(v))
    if kind in ('menu','own'):
        j,p = args
        if kind == 'menu':
            idx = menu_pos[p]; membership = Q(counts[i][idx],menus[idx][1])
        else:
            membership = (t,*v)[p]
        return share[j] - Q(membership,t+sum(v[:j])+4-j)
    if kind == 'reverse':
        name,j,k = args
        path = [bits[labels.index(c)] for c in paths[name]]
        return ratio(path[j],sum(path)) - ratio(v[k],sum(path[:j])+5-j)
    if kind == 'profit':
        r,ids = args
        beta = {3:Q(5,3),4:Q(1499,750)}[r]
        bg = t+sum(v[:4-r]); n = sum(bits[k] for k in ids)
        return beta*sum(share[4-r:]) - ratio(n,bg+n)
    i1,i2 = args
    x,y = (Q(counts[i][k],menus[k][1]) for k in (i1,i2))
    bg = t+sum(v[:2]); H = sum(share[2:]) + Q(v[2],(bg+1)*(bg+2))
    return H - (x+y)/(bg+1) + 2*x*y/((bg+1)*(bg+2))

def scores(point):
    return {name: sum(score(spec,c)*mass for c,mass in point.items()) for name,spec in rows}
exact_scores = scores(original)
projected_scores = scores(projected)
assert replay['all_1310_original_slacks'] == {k:str(v) for k,v in exact_scores.items()}
assert min(exact_scores.values()) == Q(exact_report['minimum_slack']) > 0
assert replay['minimum_slack_names'] == [k for k,v in exact_scores.items() if v == min(exact_scores.values())]
assert min(projected_scores.values()) > 0

full_names = hist_discovery['row_names']
off_scores = dict.fromkeys(full_names[1310:],Q())
for rec in hist_report['positive_histograms']:
    mass = Q(rec['mass'])
    ps = [(t,*v) for t,v,n in rec['histogram'] for _ in range(n)]
    for row, (j,k) in zip(full_names[1310:], product(range(4),repeat=2)):
        off_scores[row] += mass/5*sum(ratio(p[1+j],sum(p))-Q(other[k+1],sum(p[:j+1])+4-j)
                                     for i,p in enumerate(ps) for l,other in enumerate(ps) if l != i)
assert min(off_scores.values()) > 0
assert min(*projected_scores.values(),*off_scores.values()) == Q(hist_report['minimum_slack'])

fixed_counts = [[int(c) for c in atom['bits']] for atom in old]
old_exclusion = Q()
for i,atom in enumerate(old):
    p=sum(fixed_counts[i][j] for j in (0,1,4)); (_, _),(l1,h1),(l2,h2) = atom['menus_lh']
    old_exclusion += Q(atom['mass'])*(Q(l2-l1,p+1)-Q(h2-h1,(p+1)*(p+2)))
assert old_exclusion == -Q(33962942532321286037391724417608677893,2370629578513027021549656484975223155224)
print(json.dumps(dict(original_cells=len(original), original_group_size_distribution=dict(positive_groups),
 original_minimum=[k for k,v in exact_scores.items() if v == min(exact_scores.values())],
 projected_cells=len(projected), common_cells=len(original.keys() & projected.keys()),
 common_equal_masses=sum(original[k]==projected[k] for k in original.keys() & projected.keys()),
 projected_t_counts=dict(Counter(t for _,t,_ in projected)),
 projected_minimum=[(k,str(v)) for k,v in projected_scores.items() if v==min(projected_scores.values())],
 full_minimum=[(k,str(v)) for k,v in (projected_scores | off_scores).items() if v==Q(hist_report['minimum_slack'])],
 old_exclusion=str(old_exclusion)), ensure_ascii=False, indent=2))

# Isolate pure function definitions by AST. No frozen script top level, scan, or random loop is run.
def functions_from(path, names, namespace):
    parsed = ast.parse(path.read_text()); nodes = [n for n in parsed.body if isinstance(n,ast.FunctionDef) and n.name in names]
    assert {node.name for node in nodes} == names
    exec(compile(ast.Module(body=nodes,type_ignores=[]),str(path),'exec'),namespace)
    return namespace
private = evidence/'reviewed-local-private-search-and-singleton-residue-three-primary/source-root/intake/reviewed-local-20261029/raw'
ordered = functions_from(private/'search_disjoint_tmp.py', {'possible'}, {'Fraction':Q,'lru_cache':lru_cache})['possible']
integer_src = root/'tools/evidence/search-and-facility-site-primary/original/4a0a68157e801a180ce5/tests/audits/customer_attraction_search.py'
count = functions_from(integer_src, {'compositions','geometry','exact_outcomes','instance_record'}, {'lru_cache':lru_cache,'lcm':math.lcm,'Fraction':Q})

def exhaustive_two_players(values):
    k=len(values); terminals=set()
    for root_action in range(k):
        for last_policy in product(range(k),repeat=k):
            if any(Q(values[a], 1+(first==a)) < max(Q(values[b],1+(first==b)) for b in range(k)) for first,a in enumerate(last_policy)):
                continue
            if Q(values[root_action],1+(root_action==last_policy[root_action])) >= max(Q(values[a],1+(a==last_policy[a])) for a in range(k)):
                terminals.add((root_action,last_policy[root_action]))
    return terminals

for values,m in [((0,0,0,0),2),((1,1,1,1),2),((1,0,3,2),2),((4,1,1,1),4),((6,0,1,2),6),((6,1,1,1,1,1,1),6)]:
    k=len(values); all_seq=ordered(values,m)
    if m==2:
        assert all_seq == exhaustive_two_players(values)
    weights=[0]*((1<<k)-1)
    for a,v in enumerate(values): weights[(1<<a)-1]=v
    cnt=count['exact_outcomes'](k,m,tuple(weights))
    record=count['instance_record'](k,m,tuple(weights),cnt)
    assert {tuple(seq.count(a) for a in range(k)) for seq in all_seq} == {tuple(seq) for seq in record['all_spe_terminal_counts']}
    assert sum(sorted(values,reverse=True)[:m]) == record['opt_m']
    assert min(sum(values[a] for a in set(seq)) for seq in all_seq) == record['minimum_spe_welfare']
    assert 11 * record['minimum_spe_welfare'] >= 6 * record['opt_m'] if m==6 else (2*m-1)*record['minimum_spe_welfare'] >= m*record['opt_m']
    print(values, m, len(all_seq), len(record['all_spe_terminal_counts']), record['minimum_ratio'])

coupling = evidence/'root-coupling-six-boss3'
cert = read(coupling/'original/root_coupling_obstruction_exact.json')
lam = list(map(Q,cert['lambda'])); nu = list(map(Q,cert['nu']))
assert lam == [Q(0)]*15+[Q(1)] and sum(x != 0 for x in nu) == 30
assert len(nu) == len(original)
nu_cells = dict(zip(original, nu))
budget = sum(nu_cells[cell]*mass for cell,mass in original.items())
assert budget == Q(cert['positive_impossibility_budget']) > 0
counts_by_sign = Counter()
for i in range(38):
    choices = [[v for j,t,v in original if i == j and t == u] for u in range(2)]
    for zero_modes in combinations_with_replacement(choices[0],4):
        for one_mode in choices[1]:
            modes = [(0,*v) for v in zero_modes] + [(1,*one_mode)]
            val = sum(ratio(p[4],sum(p))-Q(other[4],sum(p[:4])+1)
                      for j,p in enumerate(modes) for k,other in enumerate(modes) if j != k)/5
            dual = sum(nu_cells[(i,p[0],p[1:])] for p in modes)/5
            slack = -(val+dual)
            assert slack >= 0
            counts_by_sign['positive' if slack else 'zero'] += 1
assert counts_by_sign == {'zero':72,'positive':24}
print('fixed92 complete Farkas', dict(counts_by_sign), str(budget))

values, k, m = (4,1,1,1),4,4
weights = tuple(values[mask.bit_length()-1] if mask.bit_count() == 1 else 0 for mask in range(1,1<<k))
model = count['exact_outcomes'](k,m,weights)
levels, leaves, leaf_ids, _, _, children = count['geometry'](k,m)
pay = model['payoffs']
sets = {q:{j} for j,q in enumerate(leaves)}
floors = {}
for level in reversed(levels[:-1]):
    for c in level:
        branches = [sets[cc] for cc in children[c]]
        floors[c] = tuple(min(pay[a][j] for j in branch) for a,branch in enumerate(branches))
        sets[c] = {j for a,branch in enumerate(branches) for j in branch if pay[a][j] >= max(floors[c])}
assert sets[(0,)*k] == model['outcome_ids']

def decode(h,c,j,forced,policy):
    if len(h)==m:
        assert c==leaves[j]
        return
    valid = [a for a,cc in enumerate(children[c]) if j in sets[cc] and pay[a][j]>=max(floors[c])]
    a = forced[0] if forced else valid[0]
    assert a in valid
    policy[h] = a
    for b,cc in enumerate(children[c]):
        if a == b:
            decode(h+(b,),cc,j,forced[1:],policy)
        else:
            bad_j = min(sets[cc],key=lambda item:pay[b][item])
            assert pay[b][bad_j] <= pay[a][j]
            decode(h+(b,),cc,bad_j,(),policy)

def realized(h,policy):
    while len(h)<m:
        h += (policy[h],)
    return leaf_ids[tuple(h.count(a) for a in range(k))]

ordered_paths = ordered(values,m)
for path in ordered_paths:
    j = leaf_ids[tuple(path.count(a) for a in range(k))]; policy={}
    decode((),(0,)*k,j,path,policy)
    assert set(policy) == {h for size in range(m) for h in product(range(k),repeat=size)}
    for h,a in policy.items():
        assert pay[a][realized(h+(a,),policy)] >= max(pay[b][realized(h+(b,),policy)] for b in range(k))
    h=()
    while len(h)<m:
        h += (policy[h],)
    assert h == path
print('four-label ordered certificate checks',len(model['outcome_ids']),len(ordered_paths),len(policy))
