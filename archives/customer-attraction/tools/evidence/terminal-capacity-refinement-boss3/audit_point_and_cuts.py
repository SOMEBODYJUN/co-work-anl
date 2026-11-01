"""Independent exact reading and structural audit of the saved 1905-column point.

This does not import the original graph builder, solve an LP, or certify all
5112 rows. Full metadata and all weights are read, not only nonzero support.
"""
from argparse import ArgumentParser
from collections import Counter
from fractions import Fraction as F
from itertools import combinations, product
from pathlib import Path
import hashlib
import json
import sys
import ast
from functools import lru_cache
from types import SimpleNamespace

HERE = Path(__file__).resolve().parent
SOURCE = None
REPO = None
SHA = '0bf850f2489986a56cc2847cfdae0a1f8d86fe1b069a425cad5d40fa253e91ee'
PAT = tuple(product((0, 1), repeat=3))


def group(raw):
    f, d, wi, wj = raw
    assert f in (0, 1) and d in (0, 1) and (f or not d)
    assert tuple(wi) in PAT and tuple(wj) in PAT
    return f, d, tuple(wi), tuple(wj)


def multiplicity(g, hist):
    _, diag, wi, wj = g
    ni, nj = hist[PAT.index(wi)], hist[PAT.index(wj)]
    return ni if diag else ni * nj - (ni if wi == wj else 0)


def audit_capacity_rows(cols, weights, hist, K):
    """Reconstruct each full vector from literal follower bits and index pairs."""
    raw_cuts = json.loads((HERE/'original/504b5c22ca1331dc9ef5/terminal_capacity_refinement_cuts.json').read_text())
    assert set(raw_cuts) == {'scope', 'cuts'} and len(raw_cuts['cuts']) == 29
    gs = ((0, 0), (1, 0), (1, 1))
    old_group_path = REPO/'archives/customer-attraction/tools/evidence/combined-branch-master-program/dependencies/research/workspaces/customer-attraction/R-5662d5cb0e5845a980ed10a3b3224cb1/research_3/old_query_reply_cuts.py'
    group_tree = ast.parse(old_group_path.read_text())
    defs = [x for x in group_tree.body if isinstance(x, ast.FunctionDef) and x.name == 'groups']
    group_ns = dict(PAT=PAT, GS=gs, product=product)
    exec(compile(ast.Module(body=defs,type_ignores=[]),str(old_group_path),'exec'),group_ns)
    source_code = HERE/'related/terminal_portfolio_cuts.py'
    source_tree = ast.parse(source_code.read_text())
    defs = [x for x in source_tree.body if isinstance(x, ast.FunctionDef) and x.name in {'qvec','share','psi','row'}]
    assert len(defs) == 4
    author = dict(F=F, product=product, lru_cache=lru_cache,
                  oq=SimpleNamespace(groups=group_ns['groups']), PAT=PAT)
    exec(compile(ast.Module(body=defs,type_ignores=[]),str(source_code),'exec'),author)
    joint_columns = {}
    hc = None
    for ci,c in enumerate(cols):
        if c['kind']=='hist': hc=ci
        if c['kind']=='joint-reply': joint_columns[ci]=(hc,group(c['group']),tuple(c['state']))

    def fraction_share(n,d):
        return F(n,d) if n else F()

    @lru_cache(None)
    def literal_minimum(n,p,ell,t,qs,am,al,bm,bl,mus):
        M=sum(mus,F());Q=sum((m*q for m,q in zip(mus,qs)),F())
        values=[]
        for followers in product((0,1),repeat=n):
            g=followers[-1]
            z=p+t+sum(followers)
            price=sum(((bl if j==n-1 else bm)+(al if j==n-1 else am)/F(ell+1))*bit
                      for j,bit in enumerate(followers))
            values.append(fraction_share(t-M*g,z)+price+Q/F(p+t+sum(followers[:-1])+1))
        return min(values)

    def queries(a,words,i,j,t,length):
        q=tuple(a)+tuple(words[i])+tuple(words[j])+(t,)
        if length==16:
            remaining=[k for k in range(6) if k not in {i,j}]
            q+=tuple(F(sum(words[k][b] for k in remaining),len(remaining)) for b in range(3))
        return q

    matrices=[];records=[]
    for cut in raw_cuts['cuts']:
        assert set(cut)=={'i','member','orb','alpha_middle','alpha_last','beta_middle','beta_last','mu'}
        i,member=cut['i'],cut['member'];f,diag=cut['orb'];n=5-i;ct=6 if diag else 30
        assert i in range(5) and member in (0,1) and (f,diag) in gs
        am,al=F(cut['alpha_middle']),F(cut['alpha_last']);bm=F(cut.get('beta_middle','0'));bl=F(cut.get('beta_last','0'))
        mus=tuple(map(F,cut['mu']))
        assert len(mus)==13 and min((am,al,bm,bl,*mus))>=0
        assert sum(m>0 for m in mus) in (1,2)
        alpha=(n-1)*am+al;beta=(n-1)*bm+bl
        vector=[F()]*len(cols);vector[0]=beta;differences={}
        for hc,h in hist.items():
            c=h['column'];a=tuple(map(int,c['actual_bits']));p=sum(a[:i]);ell=sum(a[:5])
            words=tuple(w for count,w in zip(c['hist'],PAT) for _ in range(count))
            edge_values={};baseline=F();edge_count=0
            for left,right in product(range(6),repeat=2):
                if not f and left==right:continue
                if int(left==right)!=diag:continue
                g=(f,diag,words[left],words[right])
                z=[]
                for t in (0,1):
                    qs=queries(a,words,left,right,t,len(mus))
                    z.append(literal_minimum(n,p,ell,t,qs,am,al,bm,bl,mus))
                if g in edge_values:assert edge_values[g]==z
                edge_values[g]=z;baseline+=z[0]/ct;edge_count+=1
            assert edge_count==ct
            vector[hc]=fraction_share(a[i],sum(a))+alpha*fraction_share(a[5],sum(a))-baseline
            for g,z in edge_values.items():differences[hc,g]=-F(multiplicity(g,c['hist']),ct)*(z[1]-z[0])
        for ci,(hc,g,state) in joint_columns.items():
            if g[:2]==(f,diag) and state[member]:vector[ci]=differences[hc,g]
        original=author['row'](cols,cut)
        assert original==vector
        padded={**cut,'mu':cut['mu']+['0','0','0']}
        assert author['row'](cols,padded)==vector
        value=sum((x*y for x,y in zip(vector,weights)),F())
        assert value>=0 and beta>0
        matrices.append(vector)
        records.append(dict(source_actual=i+1,member='Z' if member else 'R',orb=cut['orb'],
            alpha_middle=str(am),alpha_last=str(al),total_actual_last_price=str(alpha),
            total_capacity_price=str(beta),positive_queries=[{'query_index':j,'weight':str(m)} for j,m in enumerate(mus) if m],beta_middle=str(bm),beta_last=str(bl),
            exact_slack=str(value),all_1905_coefficients_equal_to_original=True,
            zero_padding_13_to_16_preserves_all_coefficients=True))
    prior_points={
      'portfolio_5083':'archives/customer-attraction/tools/evidence/terminal-portfolio-refinement-boss3/original/7f3e20e49ad37edc1d64/terminal_portfolio_refinement_exact.json',
      'continuous_5075':'archives/customer-attraction/tools/evidence/continuous-query-refinement-program/related/continuous_refinement_exact.json',
      'combined_5108':'archives/customer-attraction/tools/evidence/full156-tail-parent-report/original/research_5/combined_branch_master_exact.json'}
    prior={}
    for label,path in prior_points.items():
        q=json.loads((REPO/path).read_text());old=q['columns'];assert len(old)==len(cols)
        assert all({k:v for k,v in c.items() if k!='weight'}=={k:v for k,v in d.items() if k!='weight'} for c,d in zip(cols,old))
        ow=[F(c['weight']) for c in old]
        changing=[i for i,(x,y) in enumerate(zip(weights,ow)) if x!=y]
        kind_differences=Counter(cols[i]['kind'] for i in changing)
        same_hist=all(weights[i]==ow[i] for i,c in enumerate(cols) if c['kind']=='hist')
        prior[label]=dict(source_path=path,source_sha256=hashlib.sha256((REPO/path).read_bytes()).hexdigest(),
            nonweight_descriptors_all_equal=True,K_equal=K==ow[0],all_hist_masses_equal=same_hist,
            W_equal=F(q['W'])==sum((h['mass'] for h in hist.values() if '1' in h['column']['actual_bits']),F()),
            different_weight_coordinates=len(changing),different_coordinates_by_kind=dict(kind_differences),
            twenty_nine_exact_slacks=[str(sum((x*y for x,y in zip(row,ow)),F())) for row in matrices])
    old_eight=json.loads((HERE/'related/terminal_portfolio_refinement_cuts.json').read_text())['cuts']
    old_eight_values=[str(sum((x*y for x,y in zip(author['row'](cols,c),weights)),F())) for c in old_eight]
    assert all(F(x)>=0 for x in old_eight_values)
    stats=dict(single_positive_mu=sum(len(c['positive_queries'])==1 for c in records),two_positive_mu=sum(len(c['positive_queries'])==2 for c in records),beta_middle_positive=sum(F(c['beta_middle'])>0 for c in records),beta_last_positive=sum(F(c['beta_last'])>0 for c in records))
    return dict(capacity_cuts=records,capacity_feature_counts=stats,prior_eight_current_slacks=old_eight_values,coefficient_comparisons_to_original=29*len(cols),
        coefficient_comparisons_for_zero_padding=29*len(cols),
        independent_hidden_domain='literal 2^n follower memberships, not the author count-compressed psi',
        original_functions_used_for_comparison_only=['qvec','share','psi','row','old_query_reply_cuts.groups'],
        discovery_LP_calls=0,full_graph_builds=0,prior_point_comparisons=prior)


def run():
    if sys.flags.optimize:
        raise RuntimeError('Assertions must be enabled')
    raw = SOURCE.read_bytes()
    assert len(raw) == 819848 and hashlib.sha256(raw).hexdigest() == SHA
    p = json.loads(raw)
    assert set(p) == {'scope', 'base_rows', 'first_raw_rows', 'additional_index_class_rows',
                      'O', 'W', 'strict_half_gap', 'verified_rows', 'minimum_slack',
                      'positive_columns', 'terminal_portfolio_cut_rows', 'columns'}
    assert (p['base_rows'], p['first_raw_rows'], p['additional_index_class_rows'],
            p['verified_rows'], p['minimum_slack']) == (5083, 37, 100, 5112, '0')
    assert p['terminal_portfolio_cut_rows'] == 29
    cols = p['columns']
    assert len(cols) == 1905 and cols[0]['kind'] == 'K'
    assert all(isinstance(c['weight'], str) for c in cols)
    weights = [F(c['weight']) for c in cols]
    assert min(weights) >= 0 and sum(w > 0 for w in weights) == p['positive_columns'] == 194
    assert set(cols[0]) == {'kind', 'weight'}
    k = weights[0]
    hist = {}
    hi = None
    kind_counts = Counter()
    positive_counts = Counter()
    for i, c in enumerate(cols):
        kind_counts[c['kind']] += 1
        positive_counts[c['kind']] += weights[i] > 0
        if c['kind'] == 'hist':
            assert set(c) == {'kind', 'actual_bits', 'd', 'hist', 'weight'}
            assert len(c['actual_bits']) == 6 and set(c['actual_bits']) <= {'0', '1'}
            assert len(c['hist']) == 8 and all(isinstance(n, int) and n >= 0 for n in c['hist'])
            assert sum(c['hist']) == 6
            assert c['d'] == sum(n*w[0] for n, w in zip(c['hist'], PAT)) == 1
            hi = i
            hist[i] = {'column': c, 'mass': weights[i], 'states': {}, 'old_id': None}
        elif c['kind'] == 'joint-reply':
            assert set(c) == {'kind', 'hist_column_old', 'group', 'state', 'weight'}
            assert hi is not None and len(hist) <= 16
            h = hist[hi]
            if h['old_id'] is None:
                h['old_id'] = c['hist_column_old']
            assert h['old_id'] == c['hist_column_old']
            g, st = group(c['group']), tuple(c['state'])
            assert st in {(0, 1), (1, 0), (1, 1)}
            states = h['states'].setdefault(g, {})
            assert st not in states
            states[st] = weights[i]
        else:
            assert c['kind'] in ('K', 'overlap')
    assert kind_counts == {'K': 1, 'hist': 16, 'joint-reply': 582, 'overlap': 1306}
    implicit = []
    expected_old_hist_column = 1
    for h in hist.values():
        assert h['old_id'] == expected_old_hist_column
        expected_old_hist_column += 1 + len(h['states'])
        words = tuple(word for n, word in zip(h['column']['hist'], PAT) for _ in range(n))
        expected = {(f, int(i == j), words[i], words[j])
                    for f, i, j in product(range(2), range(6), range(6)) if f or i != j}
        assert set(h['states']) == expected
        h['R'], h['Z'] = {}, {}
        for g, st in h['states'].items():
            assert set(st) == {(0, 1), (1, 0), (1, 1)}
            q00 = h['mass'] - sum(st.values())
            assert q00 >= 0
            implicit.append(q00)
            h['R'][g] = st[1, 0] + st[1, 1]
            h['Z'][g] = st[0, 1] + st[1, 1]
        assert sum(multiplicity(g, h['column']['hist']) for g in expected) == 66
    assert len(implicit) == 194
    overlaps, overlap_slacks = {}, []
    literal_intersection_obstructions = []
    for i, c in enumerate(cols):
        if c['kind'] != 'overlap':
            continue
        assert set(c) == {'kind', 'hist_column', 'groups', 'weight'}
        hc = c['hist_column']
        assert hc in hist and len(c['groups']) == 2
        g1, g2 = map(group, c['groups'])
        assert g1 != g2 and g1 in hist[hc]['R'] and g2 in hist[hc]['R']
        key = hc, frozenset((g1, g2))
        assert key not in overlaps
        overlaps[key] = weights[i]
        lower = max(F(), hist[hc]['R'][g1] + hist[hc]['R'][g2] - hist[hc]['mass'])
        if weights[i] < lower:
            literal_intersection_obstructions.append({
                'column': i, 'hist_column': hc, 'hist_mass': str(hist[hc]['mass']),
                'groups': c['groups'], 'R_masses': [str(hist[hc]['R'][g1]), str(hist[hc]['R'][g2])],
                'saved_overlap': str(weights[i]), 'frechet_lower_bound': str(lower),
                'lower_minus_saved': str(lower-weights[i])})
        for g in (g1, g2):
            slack = hist[hc]['R'][g] - weights[i]
            assert slack >= 0
            overlap_slacks.append(slack)
    expected_pairs = {(hc, frozenset(gs)) for hc, h in hist.items()
                      for gs in combinations(h['states'], 2)}
    assert set(overlaps) == expected_pairs and len(overlap_slacks) == 2612
    total = sum((h['mass'] for h in hist.values()), F())
    welfare = sum((h['mass'] for h in hist.values() if '1' in h['column']['actual_bits']), F())
    assert total == F(p['O']) == 1 and welfare == F(p['W'])
    assert 1 - 2*welfare == F(p['strict_half_gap']) > 0
    profits = [sum((h['mass']*F(int(h['column']['actual_bits'][j]),
                                   sum(map(int, h['column']['actual_bits'])))
                    for h in hist.values() if '1' in h['column']['actual_bits']), F())
               for j in range(6)]
    assert sum(profits) == welfare
    capacities = []
    for family, diag in ((0, 0), (1, 0), (1, 1)):
        count = 6 if diag else 30
        for reply in ('R', 'Z'):
            amount = sum((multiplicity(g, h['column']['hist'])*v
                          for h in hist.values() for g, v in h[reply].items()
                          if g[:2] == (family, diag)), F())
            slack = count*k - amount
            assert slack >= 0
            capacities.append({'reply': reply, 'family': family, 'diagonal': diag,
                               'indexed_themes': count, 'total_theme_mass': str(amount),
                               'capacity_slack': str(slack)})
    old_floors = []
    for word_bit, name in ((1, 'B'), (2, 'C')):
        for j in range(6):
            price = sum((h['mass'] * sum(n*w[word_bit] for n, w in zip(h['column']['hist'], PAT))
                         / (sum(map(int, h['column']['actual_bits'][:j]))+6-j)
                         for h in hist.values()), F())
            slack = 6*profits[j]-price
            assert slack >= 0
            old_floors.append({'reply': name, 'actual_player': j+1, 'slack': str(slack)})
    new_floors = []
    for family, diag in ((0, 0), (1, 0), (1, 1)):
        count = 6 if diag else 30
        for reply in ('R', 'Z'):
            for j in range(6):
                price = sum((multiplicity(g, h['column']['hist'])*v
                             / (sum(map(int, h['column']['actual_bits'][:j]))+6-j)
                             for h in hist.values() for g, v in h[reply].items()
                             if g[:2] == (family, diag)), F())
                slack = count*profits[j]-price
                assert slack >= 0
                new_floors.append({'reply': reply, 'family': family, 'diagonal': diag,
                                   'actual_player': j+1, 'slack': str(slack)})
    saturation = Counter()
    for (hc, pair), value in overlaps.items():
        a, b = pair
        top = min(hist[hc]['R'][a], hist[hc]['R'][b])
        saturation['equal_to_minimum_R_marginal'] += int(value == top)
        saturation['strictly_below_minimum_R_marginal'] += int(value < top)
    summary = []
    for hc, h in hist.items():
        summary.append({'hist_column': hc, 'hist_column_old': h['old_id'],
                        'actual_bits': h['column']['actual_bits'], 'hist': h['column']['hist'],
                        'mass': str(h['mass']), 'groups': len(h['states']),
                        'positive_joint_states': sum(v > 0 for s in h['states'].values() for v in s.values())})
    example = next((x for x in literal_intersection_obstructions if x['R_masses'] == [x['hist_mass']]*2 and F(x['saved_overlap']) == 0), None)
    extra = audit_capacity_rows(cols, weights, hist, k)
    return {'status': 'PASS_EXACT_RELAXED_STRUCTURE_AND_REPLY_FLOORS',
            'scope': 'All 1905 column records; nonnegativity, all 194 implicit 00 masses, 2612 overlap upper bounds, six split R/Z capacities, twelve actual B/C safety floors, 36 actual R/Z safety floors, norm and welfare. Not original all-5112-row replay.',
            'source_sha256': SHA, 'source_bytes': len(raw), 'python_version': sys.version,
            'audit_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'top_level_metadata': {key: value for key, value in p.items() if key != 'columns'},
            'column_counts': dict(kind_counts), 'positive_counts': dict(positive_counts),
            'histograms': summary, 'minimum_implicit_00': str(min(implicit)),
            'overlap_upper_bounds_checked': len(overlap_slacks),
            'minimum_overlap_upper_slack': str(min(overlap_slacks)),
            'normalization_O': str(total), 'actual_W': str(welfare),
            'strict_half_gap': str(1-2*welfare), 'six_actual_payoffs': list(map(str, profits)),
            'K': str(k), 'split_capacities': capacities, 'actual_BC_safety_floors': old_floors,
            'actual_RZ_safety_floors': new_floors, 'overlap_saturation_counts': dict(saturation),
            'literal_intersection_diagnostic': {
                'scope': 'These are auxiliary relaxed overlaps, not all literal intersections of the given R marginals. This does not rule out replacing overlaps by minima or a different complete-game realization.',
                'frechet_lower_violations': len(literal_intersection_obstructions),
                'simple_example': example, 'all_violations': literal_intersection_obstructions},
            'capacity_row_and_prior_point_audit': extra,
            'reused_independent_implementation': 'continuous-refinement-necessary-point/audit_point.py; source identity and metadata adapted; independent literal-hidden-state 29-row construction and prior-point comparison added',
            'not_certified': ['all original 5112 inequalities', 'exact optimality',
                              'a complete-history SPE', 'six-half counterexample']}


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--repo', type=Path, required=True)
    args = parser.parse_args()
    SOURCE = args.source
    REPO = args.repo
    report = run()
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in {'histograms','split_capacities','actual_BC_safety_floors','actual_RZ_safety_floors','literal_intersection_diagnostic'}},ensure_ascii=False,indent=2))
