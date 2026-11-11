#!/usr/bin/env python3
"""Nine targeted one-query weight LPs and six true common-G two-query LPs.

LPs only propose globally nonnegative weights.  Exact full-domain envelopes
and full original-column vectors, including zero-mass states, decide acceptance.
"""
from __future__ import annotations
import argparse
from collections import defaultdict
from fractions import Fraction as F
from functools import lru_cache
import gzip
import hashlib
from itertools import product
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
import numpy as np
from scipy.optimize import linprog

HERE = Path(__file__).resolve().parent
RUN = HERE.parent
sys.path.insert(0, str(RUN/'cross_branch_math'))
import new_theme_early_projections as base
import observed_first_branch_requery as observed
import discover_projection_weights as old_finder
from prepare_priority_cuts import canon, vector_sha, literal_audit


def ratio(a, denominator):
    if not a:
        return F()
    assert denominator > 0
    return F(a, denominator)


@lru_cache(None)
def two_query_candidates(source, case):
    p, ell, t, q1, q2 = case
    n = 5-source
    assert source in range(5) and all(q in (0,1) for q in (t,q1,q2))
    out = []
    for s, g in product(range(n), (0,1)):
        z = p+t+s+g
        denominator = p+t+s+1
        out.append((ratio(t,z),
                    (F(s,ell+1),F(g,ell+1),F(s),F(g),
                     ratio(q1,denominator)-ratio(g,z),
                     ratio(q2,denominator)-ratio(g,z))))
    assert len(out) == 2*n
    return tuple(out)


@lru_cache(None)
def two_query_min(source, case, parameters):
    assert len(parameters) == 6 and min(parameters) >= 0
    return min(constant+sum((a*w for a,w in zip(coeff,parameters)),F())
               for constant,coeff in two_query_candidates(source,case))


def two_query_cases(spec, column, actual):
    source = spec['actual_source_zero_based']
    t = base.feature(column,actual,spec['forced'])
    queries = tuple(base.feature(column,actual,name) for name in spec['queries'])
    assert all(q in (0,1) for q in queries)
    # Forced Y averaging would be a mixture of complete pure-forcing rows;
    # no fractional t is substituted into an integer load denominator.
    return tuple(((sum(actual[:source]),sum(actual[:5]),bit,*map(int,queries)),prob)
                 for bit,prob in ((0,1-t),(1,t)) if prob)


def two_query_row(spec, parameters, columns, hist, family):
    source = spec['actual_source_zero_based']
    am,al,bm,bl,_,_ = parameters
    last_price,capacity = (4-source)*am+al,(4-source)*bm+bl
    row = {0:capacity} if capacity else {}
    for index in family[spec['family']]:
        column = columns[index]
        actual = tuple(map(int,hist[column['hist_column']]['actual_bits']))
        count = sum(actual)
        cost = sum((prob*two_query_min(source,case,parameters)
                    for case,prob in two_query_cases(spec,column,actual)),F())
        coefficient = ratio(actual[source],count)+last_price*ratio(actual[5],count)-cost
        if coefficient:
            row[index] = coefficient
    return row


def discover_two(spec, columns, hist, weights, profits, family):
    source = spec['actual_source_zero_based']
    masses = defaultdict(F)
    for index in family[spec['family']]:
        if not weights[index]:
            continue
        column = columns[index]
        actual = tuple(map(int,hist[column['hist_column']]['actual_bits']))
        for case,prob in two_query_cases(spec,column,actual):
            masses[case] += weights[index]*prob
    cases = sorted(masses)
    objective = list(map(float,((4-source)*profits[5],profits[5],(4-source)*weights[0],weights[0],F(),F())))
    objective += [-float(masses[c]) for c in cases]
    inequalities, rhs = [],[]
    for ci,case in enumerate(cases):
        for constant,coeff in two_query_candidates(source,case):
            row = [-float(v) for v in coeff]+[0.]*len(cases)
            row[6+ci] = 1.
            inequalities.append(row); rhs.append(float(constant))
    inequalities.append([1.]*6+[0.]*len(cases));rhs.append(32.)
    result = linprog(objective,A_ub=np.asarray(inequalities),b_ub=rhs,
                     bounds=[(0,None)]*6+[(None,None)]*len(cases),method='highs',
                     options={'primal_feasibility_tolerance':1e-9,'dual_feasibility_tolerance':1e-9})
    report = dict(spec,success=bool(result.success),status=str(result.message),
                  parameter_names=['alpha_middle','alpha_last','beta_middle','beta_last','mu_1','mu_2'],
                  positive_visible_states=len(cases),inequalities=len(inequalities),weight_budget=32)
    if not result.success:
        return report
    parameters = tuple(max(F(),F(float(v)).limit_denominator(1000000)) for v in result.x[:6])
    row = two_query_row(spec,parameters,columns,hist,family)
    exact = sum((v*weights[i] for i,v in row.items()),F())
    am,al,bm,bl,mu1,mu2 = parameters
    direct = profits[source]+((4-source)*am+al)*profits[5]+((4-source)*bm+bl)*weights[0]
    direct -= sum((mass*two_query_min(source,case,parameters) for case,mass in masses.items()),F())
    assert direct == exact
    report.update(parameters=list(map(str,parameters)),
                  float_slack=float(result.fun)+float(profits[source]),
                  exact_slack=str(exact),exact_slack_float=float(exact),
                  accepted_negative=exact<0,both_queries_positive=mu1>0 and mu2>0,
                  source_IC_weight='1',
                  coefficients=[[i,str(v)] for i,v in canon(row)])
    return report


def two_query_literal_audit(source, parameters):
    """All actual signatures, binary T/Q1/Q2 and literal successor bits."""
    n = 5-source
    am,al,bm,bl,mu1,mu2 = parameters
    checks = 0
    table = []
    for actual in product((0,1),repeat=6):
        p,ell = sum(actual[:source]),sum(actual[:5])
        for t,q1,q2 in product((0,1),repeat=3):
            values = []
            for successors in product((0,1),repeat=n):
                g = successors[-1];s = sum(successors[:-1]);z = p+t+s+g
                value = ratio(t,z)
                value += sum((am*F(f,ell+1)+bm*f for f in successors[:-1]),F())
                value += al*F(g,ell+1)+bl*g
                value += mu1*(F(q1,p+t+s+1)-ratio(g,z))
                value += mu2*(F(q2,p+t+s+1)-ratio(g,z))
                values.append(value);checks += 1
            minimum = min(values)
            assert minimum == two_query_min(source,(p,ell,t,q1,q2),parameters)
            table.append({'actual':''.join(map(str,actual)),'t':t,'q1':q1,'q2':q2,'minimum':str(minimum)})
    return {'complete_actual_signatures':64,'visible_cases':len(table),
            'literal_hidden_candidates_checked':checks,'integer_n':n,
            'all_literal_and_count_minima_equal':True,'table':table}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--point',type=Path,default=RUN/'zz_closure_lp/augmented_lp_exact.json')
    ap.add_argument('--matrix',type=Path,default=RUN/'zz_closure_lp/exact_matrix.json.gz')
    ap.add_argument('--output',type=Path,default=HERE/'targeted_weights_13931.json')
    args = ap.parse_args()
    raw = args.point.read_bytes();point = json.loads(raw)
    columns,hist,weights,profits,family,_ = base.topology(point)
    matrix = json.loads(gzip.decompress(args.matrix.read_bytes()))
    assert [{k:v for k,v in c.items() if k!='weight'} for c in columns] == matrix['columns']
    baseline = {canon(row):name for row,name in zip(matrix['rows'],matrix['row_names'])}
    priority_path = HERE/'priority_six_cuts_13931.json'
    priority = json.loads(priority_path.read_text())
    priority_vectors = {canon(r['coefficients']):r['name'] for r in priority['selected_rows']}
    specs = []
    for mechanism,seed,source,fam,t,q in (
        ('portfolio',2,1,'M1','H3','H1'),('portfolio',3,1,'M1','H1','H3'),('portfolio',2,1,'M1','H3','H2'),
        ('requery',0,3,'B2','H2','H3'),('requery',0,3,'B3','H1','H2'),('requery',0,3,'B4','H0','H1')):
        params = (base.PORTFOLIO if mechanism=='portfolio' else base.REQUERY)[seed]
        spec = {'mechanism':mechanism,'actual_source_zero_based':source,'family':fam,'forced':t,'query':q,'parameters':list(map(str,params))}
        row = base.row_coefficients(spec,columns,hist,family)
        seed_value = sum((v*weights[i] for i,v in row),F())
        specs.append(dict(spec,seed_parameters=list(map(str,params)),seed_slack=str(seed_value)))
    seen_observed = set()
    for r in sorted(observed.build(point),key=lambda r:F(r['slack'])):
        key = r['family'],r['query']
        if key in seen_observed:
            continue
        seen_observed.add(key)
        specs.append(dict(r,mechanism='observed-first',forced=None,seed_parameters=r['parameters'],seed_slack=r['slack']))
        if len(seen_observed) == 3:
            break
    one = []
    for index,spec in enumerate(specs):
        report = old_finder.discover(spec,columns,hist,weights,profits,family,32)
        report['name'] = f'targeted-one-query:{index}:{spec["mechanism"]}:{spec["family"]}:{spec.get("forced")}:{spec["query"]}'
        one.append(report)
        print(json.dumps({k:v for k,v in report.items() if k!='coefficients'}),flush=True)
    two = []
    for index,(forced,queries) in enumerate((('H3',('H1','H2')),('H3',('H1','A6')),('H3',('H1','H4')),
                                            ('H1',('H3','H2')),('H1',('H3','A6')),('H1',('H3','H4')))):
        spec = {'name':f'targeted-two-query:{index}:M1:{forced}:{queries[0]}:{queries[1]}',
                'mechanism':'portfolio-two-query','actual_source_zero_based':1,
                'family':'M1','forced':forced,'queries':list(queries)}
        report = discover_two(spec,columns,hist,weights,profits,family)
        two.append(report)
        print(json.dumps({k:v for k,v in report.items() if k!='coefficients'}),flush=True)
    seen = {}; unique_negative = []; audits = {}
    for report in one+two:
        if 'coefficients' not in report:
            continue
        vector = canon(report['coefficients'])
        report['vector_sha256'] = vector_sha(vector)
        report['baseline_match'] = baseline.get(vector)
        report['priority_pack_match'] = priority_vectors.get(vector)
        report['duplicate_of'] = seen.get(vector)
        if vector not in seen:
            seen[vector] = report['name']
            if report['accepted_negative']:
                assert report['baseline_match'] is None
                unique_negative.append(report['name'])
        if report['mechanism'] == 'portfolio-two-query':
            parameters = tuple(map(F,report['parameters']))
            audit_key = 'two:' + ','.join(report['parameters'])
            if audit_key not in audits:
                audits[audit_key] = two_query_literal_audit(report['actual_source_zero_based'],parameters)
            report['full_domain_audit_key'] = audit_key
    out = {'scope':'Nine targeted one-query LPs and six common-G two-query LPs in compact weight section; exact accepted rows only, not full parameter closure',
           'source':str(args.point.resolve()),'source_sha256':hashlib.sha256(raw).hexdigest(),
           'matrix':str(args.matrix.resolve()),'matrix_sha256':hashlib.sha256(args.matrix.read_bytes()).hexdigest(),
           'columns':len(columns),'original_columns':4849,
           'one_query_LP_count':len(one),'two_query_LP_count':len(two),
           'weight_section':'All non-source weights nonnegative with total at most 32; requery alpha in [0,1]. This is a discovery section, not a universal weight bound.',
           'one_query_negative_records':sum(r.get('accepted_negative',False) for r in one),
           'two_query_negative_records':sum(r.get('accepted_negative',False) for r in two),
           'two_positive_query_weight_records':sum(r.get('both_queries_positive',False) for r in two),
           'distinct_negative_vectors':len(unique_negative),'distinct_negative_names':unique_negative,
           'all_accepted_negative_vectors_already_in_priority_pack':all(r.get('priority_pack_match') for r in one+two if r.get('accepted_negative')),
           'one_query':one,'two_query':two,'full_domain_audits':audits,
           'source_theorem':'customer-attraction/shared-true-terminal-reply-query-portfolio-and-reweighted-requery'}
    args.output.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k not in ('one_query','two_query','full_domain_audits')}),flush=True)


if __name__ == '__main__':
    main()
