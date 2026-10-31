#!/usr/bin/env python3
"""Explicit small semantic counterexamples; does not rerun original entries."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib
import json
import sys


def load_definitions(root, ident):
    p=root/'original'/(ident+'.py')
    namespace={'__name__':'frozen_definitions_only','__file__':str(p)}
    exec(compile(p.read_text(),str(p),'exec'),namespace)
    return namespace


def typed_tree(q,K,edges):
    # Direct real typed-child choices; neither old zip oracle nor mu/nu formula.
    states=[]
    for x in range(q):
        options=[None]
        for xx,y,z in edges:
            if xx==x:
                options.extend([frozenset({('y',y)}),frozenset({('z',z)}),
                                frozenset({('y',y),('z',z)})])
        states.append(options)
    best=F(0);witness=None;tested=0
    for choices in product(*states):
        chosen=[s for s in choices if s is not None]
        if not chosen:continue
        tested+=1
        union=set().union(*chosen)
        if len(union)!=sum(map(len,chosen)):continue
        score=min(F(1),F(len(chosen),q),*(F(len(s),K) for s in chosen))
        if score>best:best=score;witness=choices
    return best,witness,tested


def js(x):
    if isinstance(x,F):return str(x)
    if isinstance(x,(set,frozenset)):return sorted([list(y) if isinstance(y,tuple) else y for y in x])
    if isinstance(x,tuple):return [js(z) for z in x]
    if isinstance(x,list):return [js(z) for z in x]
    if isinstance(x,dict):return {str(k):js(v) for k,v in x.items()}
    return x


def main():
    out=Path(sys.argv[1]);out.mkdir(parents=True,exist_ok=False)
    root=Path(__file__).resolve().parent
    three=load_definitions(root,'4f13d4de5870674ce284')
    bundle=load_definitions(root,'8af37296657f6ee6656d')
    single=load_definitions(root,'a68bbc33808220d4814e')
    quota=load_definitions(root,'11edfbeb430cb529a9a7')

    edges=[(0,0,0),(1,0,0),(2,0,0)]
    correct,witness,tested=typed_tree(3,2,edges)
    original=three['brute_b'](3,2,edges);closed=three['closed_form'](3,2,edges)
    mu=three['max_bipartite_mu'](3,edges);nu=three['max_3dm_nu'](3,edges)
    assert (mu,nu,original,closed,correct)==(2,1,F(1,3),F(1,2),F(1,2))
    defect={'q':3,'K':2,'triples':edges,'true_mu':mu,'true_nu':nu,'original_brute_b':original,
      'original_closed_form':closed,'independent_typed_tree_b':correct,'typed_tree_witness':witness,
      'independent_nonempty_state_choices_inspected':tested,
      'defect':'singleton z tuple is retagged y by zip; two distinct typed resources y0 and z0 become one y0',
      'analytic_identity_refuted':False,'original_full_entry_failed':False}

    edges=[(0,0,0),(0,1,1),(1,0,1),(1,1,0)]
    choices=[(x,frozenset({('y',y),('z',z)})) for x,y,z in edges]
    union=[set().union(*(S for xx,S in choices if xx==x)) for x in range(2)]
    proper=bundle['formula'](2,2,choices,2)
    actual,witness2,tested2=typed_tree(2,2,edges)
    collapsed=single['formula'](union,2,2)
    assert proper==actual==three['closed_form'](2,2,edges)==F(1,2)
    assert collapsed==single['treescore'](union,2,2)==1 and single['nu'](union,2)==2
    distinction={'q':2,'K':2,'triples':edges,'multi_label_bundle_b':proper,'independent_typed_tree_b':actual,
      'collapsed_single_A_per_choice_b':collapsed,'collapsed_A':union,'typed_witness':witness2,
      'independent_nonempty_state_choices_inspected':tested2,
      'meaning':'single-A model is a restriction with one allowed label per choice; union of arbitrary labels loses correlation'}
    sets=[{0},{1}]
    n=single['nu'](sets,1);score=single['formula'](sets,1,1)
    assert n==2 and score==single['treescore'](sets,1,1)==1
    free_q={'sets':sets,'N':2,'q':1,'K':1,'nu_K':n,'b_star':score,
      'correct_YES_criterion':'nu_K >= q; equality is not necessary when q independent of N'}

    profiles=[]
    for K in (2,3,4):
        q=3
        bundles=[(x,frozenset({('common',0)}|{('private',x,j) for j in range(K-1)})) for x in range(q)]
        # Independent resource DFS from the separately read bundle program,
        # rather than merely typing the synthetic profile into quota_value.
        nu={t:bundle['nu_t'](q,bundles,t) for t in range(1,K+1)}
        assert nu=={t:q if t<K else 1 for t in range(1,K+1)}
        assert quota['quota_value'](nu,q,K)==F(K-1,K)
        profiles.append({'q':q,'K':K,'actual_resource_DFS_nu':nu,'profile_value':quota['quota_value'](nu,q,K)})
    low_cases=sum((K+1)*(K//2) for K in range(2,30))
    counts={'bundle_q1_nonempty_resource_sets':3,'bundle_q1_edge_masks':8,'bundle_exhaustive_q1_K_instances':32,
      'bundle_stdout_hardcoded_exhaustive_label':'16*4 (incorrect)','bundle_random_instance_K_comparisons':6000,
      'bundle_fixed_floor_checks':9,
      'single_nonempty_3_resource_sets':7,'single_exhaustive_cases':3*4*(7+49+343),
      'single_random_cases':100,'single_empty_neighborhoods_tested_in_original_main':False,
      'three_q1_edge_masks':2,'three_q2_edge_masks':256,'three_exhaustive_instance_K_comparisons':(2+256)*5,
      'three_stdout_hardcoded_exhaustive_label':'256*5 (omits q1)','three_q3_sample_K_comparisons':602*4,
      'three_fixed_pool_checks':3,'three_perfect_family_checks':4*7,
      'quota_synthetic_profile_cases':7,'quota_pair_shift_low_t_cases':low_cases,
      'quota_tournament_cases':3,'quota_tournament_label_count':15,'quota_chosen_pair_disjoint_checks':34,
      'scope':'counts derived exactly from actual loop domains, not parsed as truthful from PASS strings'}
    assert counts['single_exhaustive_cases']==4788
    report={'status':'typed-oracle defect and model distinction reproduced with exact arithmetic',
      'diagnostic_runs':1,'original_entry_runs_in_this_diagnostic':0,'original_definition_only_loads':4,
      'diagnostic_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
      'three_dimensional_original_oracle_defect':defect,'multi_label_versus_single_neighborhood':distinction,
      'single_layer_free_q_boundary':free_q,'quota_synthetic_profile_small_actual_checks':profiles,
      'actual_loop_counts':counts,
      'limits':['explicit small counterexamples and three actual-profile checks only',
       'no source program mutated; no original audit entry rerun here',
       'no corrected broad production oracle, general proof replacement, UM algorithm or hardness claim']}
    (out/'report.json').write_text(json.dumps(js(report),ensure_ascii=False,indent=2)+'\n')
    (out/'command.json').write_text(json.dumps({'argv':sys.argv,'fresh_output_directory':str(out.resolve()),
      'definition_load_rule':"exec frozen source with __name__='frozen_definitions_only', so no __main__ entry",
      'new_math_program_runs':1,'original_main_entry_runs':0},ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'status':report['status'],'old_brute':'1/3','typed_brute':'1/2',
        'multi_label':'1/2','union_single_label':'1','quota_pair_cases':low_cases,'output':str(out.resolve())},ensure_ascii=False))

if __name__=='__main__':main()
