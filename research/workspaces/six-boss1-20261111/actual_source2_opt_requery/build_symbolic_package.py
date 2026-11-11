#!/usr/bin/env python3
"""Write point-free catalog/schema and a small exact sample, never an LP."""
from collections import Counter
from hashlib import sha256
from pathlib import Path
import json
import sys

sys.dont_write_bytecode = True
from symbolic_coefficients import (ACTUAL, OLD, NEW, QUERIES, TAILS, catalogue,
    coefficient, base_atom_coefficient, base_K_coefficient)

HERE = Path(__file__).resolve().parent
WS = HERE.parent
ROOT = HERE.parents[3]

def digest(path):
    return sha256(path.read_bytes()).hexdigest()

def save(name, value):
    (HERE / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')

def sample_states():
    # Twelve deliberately chosen states; this is NOT full-domain validation.
    raw = [
        ('all_zero', '000000', 0, 0, 0, '0000'),
        ('all_one', '111111', 1, 1, 1, '1111'),
        ('outside_O_forced_zero_q1', '000000', 0, 0, 1, '0000'),
        ('old_A2_distinct_own_Q', '010000', 0, 1, 0, '0000'),
        ('own_Q_distinct_old_A2', '000000', 0, 1, 1, '0000'),
        ('actual_P_three_new_P_zero', '011100', 1, 1, 0, '0000'),
        ('actual_P_zero_new_P_three', '000000', 1, 1, 1, '1100'),
        ('outside_O_all_tail', '100001', 1, 0, 0, '1111'),
        ('zero_total_positive_O', '001100', 1, 1, 0, '0000'),
        ('last_two_overlap', '101010', 0, 1, 1, '0011'),
        ('tail3_only', '000010', 1, 1, 0, '1000'),
        ('tail4_only', '100100', 0, 1, 1, '0100'),
    ]
    return [{'id':n, 'atom':{'a':[int(t) for t in a], 'x':x, 'o':o},
             'q':q, 'tail':[int(t) for t in tail]} for n,a,x,o,q,tail in raw]

def main():
    rows = catalogue()
    counts = dict(Counter(row['family'] for row in rows))
    save('row_catalogue.json', {
        'status':'SYMBOLIC_UNBOUND', 'convention':'A_R nu <= b_R(z,K)',
        'genuine_rows':243, 'core_rows':235, 'own_Q_additions':8,
        'family_counts':counts, 'query_descriptors':QUERIES,
        'old_roles':OLD, 'new_roles':NEW, 'rows':rows,
    })
    save('main_point_release_template.json', {
        'status':'UNBOUND_AWAITING_MAIN_RELEASE',
        'point_version':None, 'exact_input_path':None, 'exact_input_sha256':None,
        'primal_certificate_path':None, 'primal_certificate_sha256':None,
        'baseline_row_catalogue_path':None, 'baseline_row_catalogue_sha256':None,
        'baseline_old36_actual_RC_version':None,
        'baseline_Omean_Omean_averaging':None,
        'common_X_semantics':None, 'K':None, 'O':None,
        'all256_masses':None, 'positive_support':None,
        'positive_support_size':None, 'phase_I_authorization':None,
        'source_history':'actual ordered (A1)',
        'required_common_X_semantics':'ONE catalog-wide f_P maximizer at actual P=A1+A2+A3+A4; not a naked-size maximizer',
    })
    save('symbolic_template.json', {
        'status':'SYMBOLIC_UNBOUND', 'run':'six-boss1-20261111', 'boss':'Boss1',
        'point_release':'main_point_release_template.json',
        'state':{'old_bits':['a1','a2','a3','a4','a5','a6','x','o'],
                 'new_bits':['q','r3','r4','r5','r6'],
                 'new_true_tuple':['a1','q','r3','r4','r5','r6'],
                 'old_full_domain_size':256,'new_states_per_old_type':32,
                 'eventual_projection_state_count':8192,
                 'bit_order':'lexicographic tuples, leftmost most significant; all-zero retained'},
        'dimensions_at_positive_support_s':{
            'nonnegative_columns':'32*s', 'mass_equations':'s',
            'q_moment_inequalities':'2*s', 'genuine_inequalities':243,
            'raw_inequalities':'243+2*s'},
        'moment_rows':{
            'lower_A':'-q','lower_rhs':'-o*z/6','lower_slack':'sum(q*nu)-o*z/6',
            'upper_A':'q','upper_rhs':'o*z','upper_slack':'o*z-sum(q*nu)'},
        'mass_equation':'sum_{q,tail} nu[v,q,tail] = z[v]',
        'fixed_input':None,'fixed_matrix':None,'fixed_rhs':None,
        'full8192_matrix':None,'certificate':None,'projection_weights':None,
        'optimizer_calls':0,'matrix_constructed':False,
        'construction_scope':'catalogue and single-state coefficient oracle only',
    })
    save('audit_interface.json', {
        'status':'SYMBOLIC_UNBOUND', 'kernel':'symbolic_coefficients.py',
        'catalogue':'row_catalogue.json','samples':'literal_samples.json',
        'row_direction':'A nu <= b; residual b-A nu >= 0',
        'entry_points':{
            'catalogue()':'243 raw row descriptors in fixed order',
            'coefficient(row,atom,q,tail)':'one exact Fraction A coefficient',
            'base_atom_coefficient(row,atom)':'one exact old-mass coefficient in b',
            'base_K_coefficient(row)':'one exact coefficient of K in b',
            'fixed_dimensions(s)':'32s, s, 2s, 243, 243+2s; no allocation',
            'moment_envelope(a0,a1,o)':'exact minimum and signed-row multiplier contract'},
        'expected_counts':counts,
        'pair_counts':{'new_pair_pure_pure':78,'new_pair_pure_mean':12,
                       'new_pair_mean_mean':1,'actual_RC_new_new':15,
                       'actual_RC_new_old':40,'actual_RC_pure_pure':50,
                       'actual_RC_pure_mean':5,'omitted_old_RC':36},
        'single_distinct30_row':'NEW_PAIR|Omean|Omean',
        'distinct30_mean_cost':'o/(3D), D=1+a1+q+r3+r4',
        'same_actual_P_families':['MAX','MX','ACTUAL_RC'],
        'known_redundancies':{'MX_and_RC_L_X_mod_mass':5,
                             'literal_duplicate':'NEW_PAIR|R5|R6 = NEW_SAFE_j5|R5',
                             'literal_zero_row':'NEW_SAFE_j6|R6'},
        'omitted_paid_row':'ACTUAL_SAFE_j2|Q is implied by IC_SOURCE2 plus q*(1/(a1+1+sum(tail))-1/(a1+5)) >= 0',
        'globalization':{
            'W':'sum(lambda_R*A_R)', 'a_q':'min over ALL16 tail states of W(v,q,tail)',
            'm_o0':'a0','m_o1':'min((5*a0+a1)/6,a1)',
            'lower_multiplier':'delta=max(a1-a0,0)',
            'upper_multiplier':'gamma=max(a0-a1,0)',
            'mass_multiplier':'a0, free sign',
            'residual':'W+(gamma-delta)*q-a0 = W-a_q >= 0',
            'cut':'sum(lambda_R*b_R)-sum_all256(m_v*z_v) >= 0',
            'all_state_count_required':8192},
        'excluded_claims':['fixed-point feasibility or infeasibility','LP optimum',
                           'global sharpness','complete SPE','half bound'],
    })
    samples = []
    for state in sample_states():
        atom,q,tail=state['atom'],state['q'],state['tail']
        samples.append({**state,'coefficients':[
            {'row':row['name'],'A':str(coefficient(row,atom,q,tail)),
             'b_atom':str(base_atom_coefficient(row,atom)),
             'b_K':str(base_K_coefficient(row))} for row in rows]})
    save('literal_samples.json',{
        'claim':'Twelve boundary states only, not an LP input or full8192 matrix',
        'state_count':len(samples),'rows_per_state':243,'states':samples})
    source_paths = [
        ROOT/'archives/customer-attraction/state/定义/共同目录完整历史模型--定义.md',
        ROOT/'archives/customer-attraction/state/引理/真实末回复的共同潜力上限与重叠参数端点--引理.md',
        ROOT/'archives/customer-attraction/state/引理/末两人重叠比较与任意索引聚合--引理.md',
        WS/'main_full_average_pair.md',
    ]
    # Protect all artifacts named in the four preceding frozen builder packages.
    for folder in ['universal_true_x_tail','maximal_root_tail_wallet',
                   'maximal_root_opt_requery','maximal_root_tail_wallet_v2']:
        package=WS/folder
        manifest_path=package/'freeze_manifest.json'
        manifest=json.loads(manifest_path.read_text())
        frozen=manifest.get('file_sha256',manifest.get('files',{}))
        if isinstance(frozen,dict):
            for name,expected in frozen.items():
                path=(package/name).resolve()
                expected=expected if isinstance(expected,str) else expected['sha256']
                assert digest(path)==expected, str(path)
                source_paths.append(path)
        source_paths.append(manifest_path)
        if (package/'SHA256SUMS').exists():source_paths.append(package/'SHA256SUMS')
    unique=sorted(set(p.resolve() for p in source_paths),key=str)
    save('frozen_sources_before.json',{
        'claim':'Read-only mathematical sources and earlier frozen builder artifacts',
        'source_count':len(unique),
        'file_sha256':{str(p.relative_to(ROOT)):digest(p) for p in unique}})
    print(json.dumps({'status':'SYMBOLIC_FILES_WRITTEN','genuine_rows':243,
        'sample_states':len(samples),'sample_coefficients':len(samples)*243,
        'protected_read_only_files':len(unique),'optimizer_calls':0,
        'matrix_constructed':False},indent=2))

if __name__=='__main__':main()
