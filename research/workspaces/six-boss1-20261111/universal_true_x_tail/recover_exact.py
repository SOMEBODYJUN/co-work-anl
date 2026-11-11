#!/usr/bin/env python3
"""Rational Farkas extraction and ALL-256-type elimination; no optimizer."""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
from functools import reduce
from math import lcm,gcd
import json,gzip,hashlib
from build_input import coefficient,basecoef,dump

H=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    inp=json.loads(gzip.decompress((H/'exact_input.json.gz').read_bytes()))
    raw=json.loads((H/'discovery_output.json').read_text())
    assert raw['success'] and raw['fun']>0 and raw['optimizer_calls']==1
    assert raw['input_sha256']==sha(H/'exact_input.json.gz')
    rows=inp['inequalities'];atoms=inp['all_base_atoms']
    normalized={r['name']:F(-w).limit_denominator(1000000) for r,w in zip(rows,raw['ineqlin']['marginals']) if -w>1e-10}
    assert all(v>0 for v in normalized.values())
    common=lcm(*(w.denominator for w in normalized.values()))
    ints={r:int(w*common) for r,w in normalized.items()}
    common_gcd=reduce(gcd,ints.values());weights={r:w//common_gcd for r,w in ints.items()}
    by_source={i:[r for r in rows if r['source']==i and r['name'] in weights] for i in range(1,5)}
    minima=[];minmap={};residual_lines=['source\tatom\ttail\tweighted_A\tminimum\tresidual'];state_count=0
    for i in range(1,5):
        for atom in atoms:
            state_values=[]
            for tail in product((0,1),repeat=6-i):
                val=sum((weights[r['name']]*coefficient(r,atom,tail) for r in by_source[i]),F(0))
                state_values.append((tail,val))
            minval=min(v for s,v in state_values);minmap[i,atom['index']]=minval
            minima.append({'source':i,'atom':atom['index'],'minimum':str(minval),'minimizing_tail_codes':[k for k,(s,v) in enumerate(state_values) if v==minval]})
            for tail,v in state_values:
                residual=v-minval;assert residual>=0;state_count+=1
                residual_lines.append(f'{i}\t{atom["index"]}\t{"".join(map(str,tail))}\t{v}\t{minval}\t{residual}')
    dump(H/'universal_minima.json.gz',minima)
    with (H/'universal_state_residuals.tsv.gz').open('wb') as f:
        with gzip.GzipFile(fileobj=f,mode='wb',mtime=0,filename='') as gz:gz.write(('\n'.join(residual_lines)+'\n').encode())
    chosen=[r for r in rows if r['name'] in weights]
    base_K=sum(weights[r['name']]*F(r['base_K']) for r in chosen)
    cut={}
    table=['atom\ta1a2a3a4a5a6\tx\to\tbase\tminsum\tcut_coefficient']
    for atom in atoms:
        base=sum((weights[r['name']]*basecoef(r,atom) for r in chosen),F(0))
        m=sum(minmap[i,atom['index']] for i in range(1,5));val=base-m
        cut[str(atom['index'])]=str(val)
        table.append(f'{atom["index"]}\t{"".join(map(str,atom["a"]))}\t{atom["x"]}\t{atom["o"]}\t{base}\t{m}\t{val}')
    (H/'universal_cut_256.tsv').write_text('\n'.join(table)+'\n')
    masses={int(k):F(v) for k,v in inp['fixed_positive_mass'].items()};K=F(inp['fixed_K'])
    weighted_rhs=sum((weights[r['name']]*F(r['rhs']) for r in chosen),F(0))
    min_rhs=sum((minmap[i,v]*masses[v] for i in range(1,5) for v in masses),F(0))
    value=weighted_rhs-min_rhs
    assert value<0
    cut_value=sum((F(cut[str(v)])*m for v,m in masses.items()),F(0))+base_K*K
    assert value==cut_value
    fixed_residuals={}
    for col in inp['columns']:
        Acol=sum((weights[r['name']]*F(r['a'].get(str(col['index']),'0')) for r in chosen),F(0))
        residual=Acol-minmap[col['source'],col['atom']]
        assert residual>=0
        fixed_residuals[str(col['index'])]=str(residual)
    sum_weights=sum(weights.values());bound=-value/sum_weights
    fixed_multipliers={f'MASS_i{i}_v{v}':str(minmap[i,v]) for i in range(1,5) for v in masses}
    exact={'status':'EXACT_INFEASIBLE','claim':'The released universal 217-row point has no completion of this necessary four-forced-X true-tail system. This is not half and not a full-SPE counterexample.',
           'input_sha256':sha(H/'exact_input.json.gz'),'discovery_sha256':sha(H/'discovery_output.json'),
           'row_weights':weights,'positive_row_weights':len(weights),'weight_sum':sum_weights,
           'nonzero_branch_sources':sorted(i for i in by_source if by_source[i]),
           'fixed_mass_lower_multipliers':fixed_multipliers,
           'fixed_nonnegative_residual_columns':fixed_residuals,
           'fixed_weighted_rhs':str(weighted_rhs),'fixed_weighted_mass_lower_bound':str(min_rhs),
           'fixed_projection_cut_value':str(value),'fixed_projection_cut_value_decimal':float(value),
           'normalized_phase_I_lower_bound':str(bound),'normalized_phase_I_lower_bound_decimal':float(bound),
           'universal_cut':{'convention':'sum cut_z[v]*z[v]+cut_K*K >= 0', 'cut_z':cut,'cut_K':str(base_K),
                            'minima_sha256':sha(H/'universal_minima.json.gz'),'state_residuals_sha256':sha(H/'universal_state_residuals.tsv.gz'),
                            'all_types':256,'source_type_minima':len(minima),'tail_states':state_count,
                            'rule':'m_i(v)=min_s sum lambda_r A_r(i,v,s), including every zero-support/o=0/zero-client type.'},
           'optimizer_calls':1,'exact_arithmetic_only_after_discovery':True}
    dump(H/'exact_certificate.json',exact)
    print(json.dumps({k:exact[k] for k in ['status','row_weights','weight_sum','nonzero_branch_sources','fixed_projection_cut_value','fixed_projection_cut_value_decimal','normalized_phase_I_lower_bound','normalized_phase_I_lower_bound_decimal']},indent=2))
if __name__=='__main__':main()
