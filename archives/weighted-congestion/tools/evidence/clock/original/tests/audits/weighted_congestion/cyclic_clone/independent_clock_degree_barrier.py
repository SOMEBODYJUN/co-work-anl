"""Exact independent certificate for cubic anchor-clock sweep retention.

All mathematical inputs are the literals below. Standard library only.
Print JSON by default; --output NEW_PATH writes exclusively and never overwrites.
"""
from argparse import ArgumentParser
from fractions import Fraction as F
from hashlib import sha256
from itertools import product
from pathlib import Path
import json
import platform
import sys


WEIGHTS=(F(1),F(1,2),F(1,4),F(1,8))
ALPHA=F(21,20)
BASE=(((0,0,1,1),F(1593928,421875)),
      ((0,1,1,0),F(452978,421875)),
      ((1,-1,-1,-1),F(23816,5859375)),
      ((1,1,-1,-1),F(855968,17578125)))
TRIPLES=((0,1,2),(0,1,3),(0,2,3))
DEGREES=tuple(range(4))
SWEEP=((0,0,0,0),(1,0,0,0),(1,1,0,0),(1,1,1,0),
       (1,1,1,1),(0,1,1,1),(0,0,1,1),(0,0,0,1))
TARGETS=((0,1,0,1),(1,0,1,0))
# Independent simple witnesses, found before reading the author certificates.
# Entries multiply sweep margins M0,M1,M2,M3; target coefficient is one.
INDEPENDENT_DUALS=((3,0,0,0),(4,0,0,0),(3,0,1,0),(0,0,0,0))
AUTHOR_DUALS=((58,0,18,0,24),(70,0,10,10,10),
              (86,0,0,7,7),(44,0,28,0,28))
AUTHOR_SOURCE_SHA256='575dbf4fe1ad0b533d188d54e1ad32aad5f143a1e3f1828d524e22d2f33547b2'
AUTHOR_CODE_SHA256='508c37f6cbdb76d77ac995215011dae7860080e2f2ed6c8c399fa5ab76d23e2b'


def flip(state,i):
    changed=list(state);changed[i]^=1
    return tuple(changed)


def phase(signature,state,i):
    return state[i] if signature[i]==1 else 1-state[i]


def literal_pair_costs(signature,degree,coefficient,state):
    """Build both actual resource user sets and recompute their true loads."""
    costs=[F(0)]*4
    for side in (0,1):
        users=[i for i in range(4) if signature[i] and phase(signature,state,i)==side]
        load=sum((WEIGHTS[i] for i in users),F(0))
        if not users:
            continue  # no cost is paid by anybody; avoid a gratuitous 0**0
        fee=coefficient*load**degree
        for i in users:costs[i]+=fee
    return costs


def costs(game,state):
    return [sum((literal_pair_costs(sig,p,a,state)[i] for sig,p,a in game),F(0))
            for i in range(4)]


def margin(game,state,i):
    return costs(game,state)[i]-ALPHA*costs(game,flip(state,i))[i]


def clock_signature(triple):
    sig=[0]*4
    for i,sign in zip(triple,(1,-1,1)):sig[i]=sign
    return tuple(sig)


def strings(values):
    return [str(v) for v in values]


def run():
    base=tuple((sig,3,a) for sig,a in BASE)
    columns=tuple(((clock_signature(triple),degree,F(1)),)
                  for triple in TRIPLES for degree in DEGREES)
    cycle_margins=[margin(base,s,j%4) for j,s in enumerate(SWEEP)]
    assert all(v>0 for v in cycle_margins)
    assert cycle_margins[:4]==cycle_margins[4:]
    b=cycle_margins[:4]
    target_base=[margin(base,TARGETS[0],i) for i in range(4)]
    target_cost_pairs=[]
    for target in TARGETS:
        pairs=[(costs(base,target)[i],costs(base,flip(target,i))[i]) for i in range(4)]
        assert all(old<new for old,new in pairs)
        target_cost_pairs.append([[str(old),str(new)] for old,new in pairs])
    matrix=[[margin(game,s,j) for game in columns] for j,s in enumerate(SWEEP[:4])]
    target_matrix=[[margin(game,TARGETS[0],i) for game in columns] for i in range(4)]
    certificates=[]
    for i,mu in enumerate(INDEPENDENT_DUALS):
        residuals=[target_matrix[i][c]+sum((F(mu[j])*matrix[j][c] for j in range(4)),F(0))
                   for c in range(12)]
        assert all(v<=0 for v in residuals)
        bound=target_base[i]+sum((F(mu[j])*b[j] for j in range(4)),F(0))
        assert bound<0
        assert all(v>=0 for v in mu) and mu[1]==mu[3]==0
        certificates.append({'player':i,'sweep_dual':list(mu),
                             'column_residuals':strings(residuals),
                             'scaled_base_strict_upper_bound':str(bound)})
    author_certificates=[]
    for i,u in enumerate(AUTHOR_DUALS):
        products=[sum((F(u[j])*b[j] for j in range(4)),F(0))+u[4]*target_base[i]]
        for c,(triple,degree) in enumerate((t,p) for t in TRIPLES for p in DEGREES):
            total=sum((WEIGHTS[j] for j in triple),F(0))
            raw=sum((F(u[j])*matrix[j][c] for j in range(4)),F(0))+u[4]*target_matrix[i][c]
            products.append(raw/total**degree)
        assert all(v<0 for v in products)
        author_certificates.append({'player':i,'author_dual':list(u),
                                    'normalized_dot_products':strings(products)})
    complement_checks=0
    for game in (base,)+columns:
        for state in product((0,1),repeat=4):
            comp=tuple(1-x for x in state)
            assert costs(game,state)==costs(game,comp)
            for i in range(4):
                assert margin(game,state,i)==margin(game,comp,i)
                complement_checks+=1
    # Integer row table uses a common scale valid for all dyadic loads and degrees 0..3.
    scale=10240
    integer_rows={}
    for name,row in [('M0',matrix[0]),('M2',matrix[2])]+[(f'T{i}',row) for i,row in enumerate(target_matrix)]:
        scaled=[scale*v for v in row]
        assert all(v.denominator==1 for v in scaled)
        integer_rows[name]=[v.numerator for v in scaled]
    literal_inputs={
        'weights':strings(WEIGHTS),'alpha':str(ALPHA),
        'base_pairs':[{'signature':list(sig),'cubic_coefficient':str(a)} for sig,a in BASE],
        'clock_triples':[list(t) for t in TRIPLES],'clock_literal_pattern':[0,1,0],
        'degrees':list(DEGREES),'sweep_states':[list(s) for s in SWEEP],
        'sweep_movers':[j%4 for j in range(8)],'target_states':[list(s) for s in TARGETS],
        'independent_duals':[list(u) for u in INDEPENDENT_DUALS],
        'author_duals':[list(u) for u in AUTHOR_DUALS]}
    canonical=json.dumps(literal_inputs,sort_keys=True,separators=(',',':')).encode()
    return {'status':'all exact Fraction checks passed',
            'scope':'fixed positive rescalings of this base; anchor0; equal-phase clock pairs; arbitrary nonnegative real coefficients degree<=3',
            'stronger_hypothesis':'only total sweep margins M0>=0 and M2>=0 are required',
            'conclusion':'0101 and 1010 have all four alpha margins strictly negative',
            'environment':{'python_version':platform.python_version(),'implementation':platform.python_implementation()},
            'invocation':{'python_executable':sys.executable,'argv':sys.argv},
            'script_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),
            'literal_inputs_sha256':sha256(canonical).hexdigest(),'literal_inputs':literal_inputs,
            'reviewed_author_source_sha256':AUTHOR_SOURCE_SHA256,'reviewed_author_code_sha256':AUTHOR_CODE_SHA256,
            'base_cycle_margins':strings(cycle_margins),'base_target_margins':strings(target_base),
            'base_target_cost_pairs':target_cost_pairs,
            'raw_x_power_columns':[[list(t),p] for t in TRIPLES for p in DEGREES],
            'cycle_matrix':[[str(v) for v in row] for row in matrix],
            'target_matrix':[[str(v) for v in row] for row in target_matrix],
            'integer_row_common_scale':scale,'integer_rows':integer_rows,
            'independent_certificates':certificates,'independent_nonpositive_column_checks':48,
            'author_certificates':author_certificates,'author_strict_dot_product_checks':52,
            'complement_margin_checks':complement_checks,
            'numeric_arithmetic':'fractions.Fraction only; no solver; no random input'}


def main():
    parser=ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,help='New JSON path; creation is exclusive.')
    args=parser.parse_args()
    result=run()
    rendered=json.dumps(result,indent=2,ensure_ascii=False)+'\n'
    if args.output is None:
        sys.stdout.write(rendered)
    else:
        with args.output.open('x',encoding='utf-8') as handle:handle.write(rendered)


if __name__=='__main__':main()
