#!/usr/bin/env python3
"""JSON-only replay using literal true-budget shares and minimization.

Does not import/execute the builders, other project programs, or any solver.
Recomputes every new column from true budgets at all hidden tail choices.
"""
from fractions import Fraction as F
from itertools import product, combinations
from pathlib import Path
import hashlib
import json

OUT = Path(__file__).resolve().parent
REPO = OUT.parents[3]
WS = OUT.parent

def read(name):
    return json.loads((OUT / name).read_text())

def dump(name, obj):
    (OUT / name).write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n')

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def rowrank(vectors):
    basis = {}
    for vec in vectors:
        row = list(vec)
        for k in sorted(basis):
            q = row[k]
            if q:
                row = [a-q*b for a,b in zip(row,basis[k])]
        pivot = next((k for k,x in enumerate(row) if x), None)
        if pivot is not None:
            q = row[pivot]
            basis[pivot] = [x/q for x in row]
    return len(basis)

def literal_wallet(i, p, t, o, tails, theta, s):
    """Construct each client's genuine payoff and query share separately."""
    prefix = [1]*p + [0]*(i-1-p)
    six_actions = prefix + [t] + list(tails)
    load = sum(six_actions)
    shares = [F(bit, load) if bit else F(0) for bit in six_actions]
    alpha = F(25) + sum(theta.values()) - s
    cost = alpha*shares[i-1]
    cap_K = F(0)
    for player in range(i+1,7):
        weight = F(1) if player==6 else F(1,2)
        cost += weight*six_actions[player-1]
        cap_K += weight
    # For union weakening use an actual singleton membership menu when o=1.
    menu = [o,0,0,0,0,0]
    terminal_query = sum(F(bit, 1+sum(six_actions[:5])) for bit in menu)/6
    cost += terminal_query - shares[5]
    for player, weight in theta.items():
        max_query_load = sum(six_actions[:player-1]) + 1 + (6-player)
        safe_query = sum(F(bit, max_query_load) for bit in menu)/6
        cost += weight*(safe_query-shares[player-1])
    return cost, cap_K, alpha

def solve_all_facets(facets, dimension):
    """Independent exact vertex recovery via augmented-row elimination."""
    points = set()
    for selected in combinations(facets, dimension):
        a = [list(map(F, f['coefficients'])) + [-F(f['constant'])] for f in selected]
        good = True
        for col in range(dimension):
            pivot = next((r for r in range(col,dimension) if a[r][col]), None)
            if pivot is None:
                good = False
                break
            a[col], a[pivot] = a[pivot], a[col]
            divisor = a[col][col]
            a[col] = [x/divisor for x in a[col]]
            for r in range(dimension):
                if r != col:
                    multiplier = a[r][col]
                    a[r] = [x-multiplier*y for x,y in zip(a[r],a[col])]
        if good:
            point = tuple(a[k][-1] for k in range(dimension))
            if all(F(f['constant'])+sum(F(x)*y for x,y in zip(f['coefficients'],point))>=0 for f in facets):
                points.add(point)
    return points

def main():
    guard = read('source_manifest.json')
    for group in ('source_sha256', 'prior_frozen_artifact_sha256'):
        for p,h in guard[group].items():
            assert sha(REPO/p) == h, p
    family = read('exact_family.json')
    coordinates = read('coordinate_contract.json')
    domains = read('parameter_polytopes.json')['sources']
    stored_states = {(x['vertex'],x['state']):x for x in read('hidden_state_checks.json')}
    stored_mins = {(x['vertex'],x['p'],x['t'],x['o']):x for x in read('minimum_tables.json')}
    state_spaces = {x['name']:x for x in read('state_halfspaces.json')}
    minima, vertexmap, local_stats, vertex_set_checks = {}, {}, [], []
    hidden_count = 0
    for domain in domains:
        i, dim = domain['source'], domain['dimension']
        listed = {tuple(map(F,v['theta']+[v['s']])) for v in domain['vertices']}
        assert solve_all_facets(domain['facets'], dim) == listed
        # Every displayed halfspace is an actual facet, not merely a redundant label.
        for facet in domain['facets']:
            c, co = F(facet['constant']), list(map(F,facet['coefficients']))
            face = [v for v in listed if c+sum(a*b for a,b in zip(co,v))==0]
            assert face
            rank = rowrank([[x-y for x,y in zip(v,face[0])] for v in face[1:]])
            assert rank == dim-1, (i,facet['name'],rank)
            vertex_set_checks.append({'source':i,'facet':facet['name'],'facet_dimension':rank})
        for vertex in domain['vertices']:
            vid = vertex['id']
            theta = {j:F(w) for j,w in zip(range(i+1,6),vertex['theta'])}
            s = F(vertex['s'])
            a = F(25)+sum(theta.values())-s
            assert str(a)==vertex['a'] and a>0
            vertexmap[vid] = (i,theta,s,a)
            for p in range(i):
                for t,o in product((0,1),repeat=2):
                    tail_values = {}
                    for tails in product((0,1),repeat=6-i):
                        value, capK, alpha = literal_wallet(i,p,t,o,tails,theta,s)
                        assert capK == F(7-i,2) and alpha == a
                        tail_values[tails] = value
                    least = min(tail_values.values())
                    minima[(vid,p,t,o)] = least
                    record = stored_mins[(vid,p,t,o)]
                    all_ties = [list(tails) for tails,val in tail_values.items() if val==least]
                    assert F(record['minimum'])==least
                    assert record['all_attaining_tails']==all_ties
                    for tails,value in tail_values.items():
                        sid = f'I{i}_p{p}_t{t}_o{o}_r' + ''.join(map(str,tails))
                        saved = stored_states[(vid,sid)]
                        assert F(saved['cost'])==value and F(saved['target'])==least
                        assert F(saved['residual'])==value-least >= 0
                        half = state_spaces[sid]
                        params = list(theta.values())+[s]
                        assert F(half['constant'])+sum(F(q)*v for q,v in zip(half['coefficients_theta_then_s'],params)) == value-least
                        hidden_count += 1
            local_stats.append({'vertex':vid,'source':i,'genuine_source_IC':str(a),'tail_K_payment':str(F(7-i,2))})
    assert hidden_count==8064 and len(minima)==444
    # Reconstruct each full customer type without borrowing old-income expressions.
    atoms = []
    for k in range(512):
        bits = tuple((k>>(8-j))&1 for j in range(9))
        atoms.append(bits)
        saved = coordinates['atom_columns'][k]
        assert tuple(saved['a'])+(saved['x'],saved['o'],saved['c']) == bits
        assert saved['index']==k and saved['old_index']==k//2
    assert coordinates['K_column']==512 and coordinates['variables']==513
    assert family['raw_row_count']==len(family['rows'])==536
    expected_pairs = {(v['id'],role) for d in domains for v in d['vertices'] for role in [f'A{j}' for j in range(1,7)]+['X','C']}
    observed_pairs = set()
    column_count = 0
    reports = []
    for row in family['rows']:
        vid, role = row['vertex_id'],row['T']
        assert (vid,role) not in observed_pairs
        observed_pairs.add((vid,role))
        i,theta,s,a = vertexmap[vid]
        assert row['source']==i and F(row['source_IC_weight'])==a and F(row['s'])==s
        assert {int(k):F(v) for k,v in row['theta_by_true_source'].items()}==theta
        assert F(row['middle_cap_weight'])==F(1,2) and F(row['terminal_cap_weight'])==1
        assert F(row['terminal_BR_average_weight'])==1 and row['numerical_divisor']=='25'
        assert row['rhs']=='0' and row['uses_C_size_equality'] is False
        assert set(row['a'])=={str(k) for k in range(513)}
        for k,bits in enumerate(atoms):
            actual_actions = bits[:6]
            p = sum(actual_actions[:i-1])
            if role=='X':
                t=bits[6]
            elif role=='C':
                t=bits[8]
            else:
                t=actual_actions[int(role[1:])-1]
            o=bits[7]
            own_actual_share = F(1,sum(actual_actions)) if actual_actions[i-1] else F(0)
            expected = a*own_actual_share - minima[(vid,p,t,o)]
            assert F(row['a'][str(k)])==expected,(row['name'],k)
            column_count+=1
        assert F(row['a']['512'])==F(7-i,2)==F(row['K_weight'])
        column_count+=1
        reports.append({'row':row['name'],'verified_columns':513,'actual_source':i,'forced_role':role,'raw_K_weight':row['a']['512'],'status':'PASS'})
    assert observed_pairs==expected_pairs and column_count==274968
    # Independent C-size equality sign: new - old = (s/5 - 5/2)(|C|-K).
    old = json.loads((WS/'source2_joint_internal_safe/sixteen_reweighted_vertex_family.json').read_text())
    old_by_parameter = {(tuple(map(F,r['theta3_theta4_theta5'])),F(r['s'])):r for r in old}
    comparisons = []
    for row in family['rows']:
        if row['source']==2 and row['T']=='C':
            _,theta,s,a = vertexmap[row['vertex_id']]
            parent = old_by_parameter[(tuple(theta.values()),s)]
            multiplier = s/5-F(5,2)
            residuals=[]
            for k in range(513):
                equality = F(atoms[k][8]) if k<512 else F(-1)
                residual = F(row['a'][str(k)])-F(parent['a'].get(str(k),'0'))-multiplier*equality
                assert residual==0
                residuals.append(str(residual))
            comparisons.append({'new':row['name'],'old':parent['name'],'equality':'E_C=|C|-K','identity':'new = old + multiplier * E_C','multiplier':str(multiplier),'all_513_residuals':residuals})
    assert len(comparisons)==16
    dump('source2_C_endpoint_comparison.json',{'status':'PASS','parent_family_sha256':sha(WS/'source2_joint_internal_safe/sixteen_reweighted_vertex_family.json'),'compared_rows':16,'checked_columns':8208,'comparisons':comparisons})
    dump('literal_row_checks.json',reports)
    dump('literal_domain_checks.json',{'status':'PASS','all_vertices_reenumerated':67,'all_facets_have_full_codimension_one':vertex_set_checks,'hidden_state_checks':hidden_count,'minimum_tables_and_all_ties':444,'source_weights':local_stats})
    result={'status':'PASS','exact_family_sha256':sha(OUT/'exact_family.json'),'raw_rows':536,'columns':513,'all_literal_coefficient_checks':column_count,'independent_true_wallet_hidden_checks':hidden_count,'exact_minimum_tables_with_all_attainers':444,'source2_C_comparison_rows':16,'source2_C_comparison_columns':8208,'prior_frozen_artifacts_unchanged':len(guard['prior_frozen_artifact_sha256']),'source_bindings_unchanged':len(guard['source_sha256']),'optimizer_calls':0,'other_project_code_executed_or_imported':False,'fixed_point_bound':False,'global_optimality_or_SPE_sharpness_claimed':False}
    for group in ('source_sha256','prior_frozen_artifact_sha256'):
        for p,h in guard[group].items(): assert sha(REPO/p)==h,p
    dump('literal_checker_output.json',result)
    print(json.dumps(result))

if __name__=='__main__':
    main()
