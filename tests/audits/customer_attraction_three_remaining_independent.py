"""Independent symbolic review using polynomial exact division and raw slacks.
No import of the candidate manuscript, candidate audit, or CAG solver.
"""
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path
import argparse
import hashlib
import platform
import subprocess

D = (6, 11, 6, 1)  # (p+1)(p+2)(p+3), increasing coefficients

def add(*items):
    return tuple(sum(item[i] if i < len(item) else 0 for item in items) for i in range(4))

def times(k, item):
    return tuple(k*x for x in item)

def divide(offsets):
    coefficients = [F(x) for x in D]
    # Exact division by each monic factor p+offset, descending synthetic division.
    for offset in offsets:
        quotient = [F(0)] * (len(coefficients)-1)
        quotient[-1] = coefficients[-1]
        for i in range(len(quotient)-2, -1, -1):
            quotient[i] = coefficients[i+1] - offset * quotient[i+1]
        if coefficients[0] != offset * quotient[0]:
            raise ValueError((offsets, coefficients))
        coefficients = quotient
    return tuple(coefficients)

def fraction(numerator, *offsets):
    return (F(0),) if not numerator else times(numerator, divide(offsets))

def unit(own, *others):
    return fraction(own, own + sum(others))

def raw_customer(a,b,c,q,r,ts,ls):
    alpha,beta,gamma = unit(a,b,c),unit(b,a,c),unit(c,a,b)
    kq = add(times(3,alpha),times(-3,fraction(q,3)))
    kr = add(times(3,alpha),times(-3,fraction(r,3)))
    p = add(*(add(gamma,times(-1,unit(t,a,b))) for t in ts))
    z = add(*(add(gamma,times(-1,unit(l,a,b))) for l in ls))
    s = add(*(add(beta,times(-1,unit(t,a,l))) for t,l in zip(ts,ls)))
    v = add(*(add(unit(ls[i],a,ts[i]), times(-1,unit(ls[j],a,ts[i])))
              for i in range(3) for j in range(3) if i != j))
    f = add(alpha,times(-1,unit(c,q,r)))
    j = add(*(add(unit(r,c,q),times(-1,unit(t,c,q))) for t in ts))
    g = add(times(2,kq),times(3,kr),times(17,p),times(2,z),times(12,s),times(4,v),times(14,f),j)
    actual_n = a+b+c
    opt_n = sum(ts)
    target = add(times(50,fraction(actual_n,actual_n)),times(-30,fraction(opt_n,opt_n)))
    return add(target,times(-1,g))

states={}
for bits in product(range(2),repeat=11):
    a,b,c,q,r=bits[:5];ts,ls=bits[5:8],bits[8:11]
    coefficients=raw_customer(a,b,c,q,r,ts,ls)
    if coefficients[3] or any(x<0 for x in coefficients):
        raise ValueError((bits,coefficients))
    key=(a,b,c,q,r,sum(ts),sum(ls))
    if key in states and states[key]!=coefficients:
        raise ValueError(('membership-pairing failed to cancel',key,states[key],coefficients))
    states[key]=coefficients
if len(states)!=512:raise ValueError(len(states))
minima = tuple(min(row[i] for row in states.values()) for i in range(3))
zero_polynomials=sum(not any(row) for row in states.values())
report={'claim_review':'three_remaining_arbitrary_fixed_background',
        'method':'symbolic exact polynomial division applied directly to eight SPE slack families',
        'raw_membership_cases':2048,'distinct_aggregate_cases':len(states),
        'degree_at_most_two':True,'all_coefficients_nonnegative':True,
        'coefficient_minima':[str(x) for x in minima],
        'zero_polynomial_cases':zero_polynomials,
        'K_root_deviation_review':'legal common-catalog action, denominator never exceeds fixed background plus 3',
        'target':'maximum remaining-three total profit, not total union coverage',
        'all_rational_nonnegative_backgrounds_covered_algebraically':True}
root = Path(__file__).resolve().parents[2]
report.update(python_version=platform.python_version(),
              base_commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip(),
              source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              replay_commands=['python3 tests/audits/customer_attraction_three_remaining_independent.py'],
              randomness='none; all binary membership patterns enumerated')
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--output',type=Path)
args = parser.parse_args()
if args.output:
    if args.output.exists(): raise FileExistsError('refusing to overwrite frozen evidence')
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
