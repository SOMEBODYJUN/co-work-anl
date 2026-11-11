#!/usr/bin/env python3
"""751 exact point-free row descriptors and a single-state coefficient oracle."""
from fractions import Fraction as F
from hashlib import sha256
from pathlib import Path
import importlib.util
import json
import sys

sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
BASE_DIR=HERE.parent/'actual_source2_opt_requery'
BASE_KERNEL=BASE_DIR/'symbolic_coefficients.py'
BASE_KERNEL_SHA='3b8a00fa72b2b15678656f7f2f21f18610ab2f1586d850b080a1d61235e4a205'
C30_PATH=HERE.parent/'main_thirty_index_strengthening/requery30_envelopes.json'
C30_SHA='14ef732b35d0f859113daf92c8dda1f08330413682b057c69a57543a41a360bc'
assert sha256(BASE_KERNEL.read_bytes()).hexdigest()==BASE_KERNEL_SHA
assert sha256(C30_PATH.read_bytes()).hexdigest()==C30_SHA
_spec=importlib.util.spec_from_file_location('_frozen_source2_243',BASE_KERNEL)
base=importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(base)
C30=json.loads(C30_PATH.read_text())
assert len(C30)==128 and [entry['h'] for entry in C30]==list(range(128))
QUERIES=base.QUERIES[:]

def source25_cost(prefix,n,forcing,terminal,atom,q,tail):
    """Chosen exact union-weak cost for ONE ordered T/Q descriptor pair."""
    assert n in (1,2,3) and 0<=prefix<=5-n
    D=prefix+n+1
    A=F(n+1,2)+F(24,D);B=F(1,prefix+1);C=F(n,(prefix+1)*D)
    if forcing=='Omean' and terminal=='Omean':
        return F(atom['o'],6)*(A+B)
    if forcing=='Omean':
        query=base.value(terminal,atom,q,tail)
        return B*query+F(atom['o'],6)*(A-C*query)
    force=base.value(forcing,atom,q,tail)
    if terminal=='Omean':
        return A*force+F(atom['o'],6)*(B-C*force)
    query=base.value(terminal,atom,q,tail)
    return A*force+B*query-C*force*query

def c30_index(atom,q,tail):
    bits=[atom['a'][0],q,*tail,atom['o']]
    return int(''.join(map(str,bits)),2)

def coefficient(row,atom,q,tail):
    """Return original, unscaled A_R(v,q,tail) in A_R nu <= b_R(z,K)."""
    base.validate_state(atom,q,tail)
    if row['family'] not in ('NESTED_SOURCE25','NESTED_C30'):
        return base.coefficient(row,atom,q,tail)
    full=[atom['a'][0],q,*tail];total=sum(full)
    if row['family']=='NESTED_SOURCE25':
        i=row['source'];n=6-i
        assert i in (3,4,5)
        payoff=F(full[i-1],total) if total else F(0)
        return source25_cost(sum(full[:i-1]),n,*row['queries'],atom,q,tail)-25*payoff
    h=c30_index(atom,q,tail);entry=C30[h]
    assert entry['bits']==full+[atom['o']]
    wallet=F(126000*full[2]+65719*full[3]+4962*full[5],total) if total else F(0)
    value=F(entry['m30'])-wallet
    assert value==-F(entry['cut'])
    return value

def rhs_form(row):
    if row['family']=='NESTED_SOURCE25':return {'K':str(F(7-row['source'],2))}
    if row['family']=='NESTED_C30':return {}
    return base.rhs_form(row)

def base_atom_coefficient(row,atom):
    if row['family'] in ('NESTED_SOURCE25','NESTED_C30'):return F(0)
    return base.base_atom_coefficient(row,atom)

def base_K_coefficient(row):
    if row['family']=='NESTED_SOURCE25':return F(7-row['source'],2)
    if row['family']=='NESTED_C30':return F(0)
    return base.base_K_coefficient(row)

def catalogue():
    rows=base.catalogue()
    for i in (3,4,5):
        for forcing in QUERIES:
            for terminal in QUERIES:
                if forcing==terminal=='Omean':average='mean_mean_inner30'
                elif forcing=='Omean':average='meanT_pureQ_inner6'
                elif terminal=='Omean':average='pureT_meanQ_inner6'
                else:average='pure_same_outer_index'
                rows.append({'index':len(rows),
                    'name':f'NESTED_SOURCE25_j{i}|{forcing}|{terminal}',
                    'family':'NESTED_SOURCE25','source':i,'queries':[forcing,terminal],
                    'true_prefix':['A1','Q','R3','R4'][:i-1],
                    'remaining_inner_tail_count':6-i,'inner_averaging':average,
                    'rhs':{'K':str(F(7-i,2))},'suggested_positive_numerical_divisor':'25',
                    'inner_size_cap_weights':{'middle_each':'1/2','terminal':'1'},
                    'emitted_coefficients':'unscaled','own_Q_extension':False})
    rows.append({'index':len(rows),'name':'NESTED_C30|A1|Q',
        'family':'NESTED_C30','queries':[],'true_history':['A1','Q'],
        'source_payoffs':[3,4,6],'inner_averaging':'projected_true_C30_with_inner30',
        'h_bits':['a1','q','r3','r4','r5','r6','o'],
        'rhs':{},'suggested_positive_numerical_divisor':'126000',
        'emitted_coefficients':'unscaled','own_Q_extension':False})
    assert len(rows)==751
    return rows

def fixed_dimensions(s):
    assert isinstance(s,int) and 0<=s<=256
    return {'nu_columns':32*s,'mass_equations':s,'q_moment_rows':2*s,
            'genuine_rows':751,'raw_inequalities':751+2*s}

def moment_envelope(a0,a1,o):return base.moment_envelope(a0,a1,o)

if __name__=='__main__':
    from collections import Counter
    rows=catalogue()
    print(json.dumps({'status':'SYMBOLIC_UNBOUND','genuine_rows':751,
        'optimizer_calls':0,'matrix_constructed':False,
        'family_counts':dict(Counter(r['family'] for r in rows))},indent=2))
