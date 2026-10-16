#!/usr/bin/env python3
"""私有汇点族：真实OPT凸包边际的逐行偏差上界障碍。

Exact Fraction reconstruction plus an independent complete assignment oracle on
small instances. This script performs finite checks only; the accompanying note
contains the general argument. No floating point arithmetic or optimization
package is used. The exponentially enumerated test cases are explicitly listed.
"""
from fractions import Fraction as F
from itertools import product, combinations
from math import comb
from pathlib import Path
import hashlib, json, platform, sys


def family(k, r):
    assert isinstance(k, int) and isinstance(r, int) and k >= 1 and r >= 1
    # Machines 0..r-1 are H; r..2r-1 are Z. Jobs: B, then grouped jobs.
    jobs = [('B',)] + [('J', i, t) for i in range(r) for t in range(k)]
    proc = []
    for job in jobs:
        row = [None] * (2*r)
        if job[0] == 'B':
            for i in range(r): row[i] = F(1)
        else:
            _, i, _ = job
            row[i] = row[r+i] = F(1, k)
        proc.append(row)
    return jobs, proc


def actual_opt_schedules(k, r):
    # Explicit r assignments; this construction does not consult fractional x.
    return [[h] + [r+i if i == h else i for i in range(r) for _ in range(k)]
            for h in range(r)]


def loads(proc, assignment):
    out = [F(0)] * len(proc[0])
    for row, machine in zip(proc, assignment):
        assert row[machine] is not None
        out[machine] += row[machine]
    return out


def reconstruct(k, r):
    jobs, proc = family(k, r)
    opts = actual_opt_schedules(k, r)
    assert all(max(loads(proc, s)) == 1 for s in opts)
    x = [[F(0)]*(2*r) for _ in jobs]
    for assignment in opts:
        for j, i in enumerate(assignment): x[j][i] += F(1, r)
    assert all(sum(row) == 1 for row in x)
    masses = [sum(row[i] for row in x) for i in range(2*r)]
    fractional_loads = [sum(x[j][i] * proc[j][i]
                            for j in range(len(jobs)) if proc[j][i] is not None)
                        for i in range(2*r)]
    support_max = [max(proc[j][i] for j in range(len(jobs)) if x[j][i] > 0)
                   for i in range(2*r)]
    assert masses == [F(k)-F(k-1,r)]*r + [F(k,r)]*r
    assert fractional_loads == [F(1)]*r + [F(1,r)]*r
    assert support_max == [F(1)]*r + [F(1,k)]*r
    return proc, x, masses, fractional_loads, support_max


def ceilq(q): return -((-q.numerator)//q.denominator)
def floorq(q): return q.numerator//q.denominator


def direct_oracle(k, r, a=F(1), b=F(1)):
    # Enumerates every concrete assignment of all distinguishable small jobs.
    # Scaled integer units are 1/k, independently of Fraction reconstruction.
    count_cap_h = ceilq(F(k)-F(k-1,r))
    count_cap_z = ceilq(F(k,r))
    row_cap_h = (a+b)*k
    row_cap_z = a*F(k,r)+b
    best = best_count = best_row = None
    best_row_assignment = None
    examined = 0
    for choices in product((0,1), repeat=r*k):
        h_load = [0]*r
        z_load = [0]*r
        h_count = [0]*r
        z_count = [0]*r
        for pos, to_sink in enumerate(choices):
            i = pos//k
            if to_sink:
                z_load[i] += 1; z_count[i] += 1
            else:
                h_load[i] += 1; h_count[i] += 1
        for h in range(r):
            examined += 1
            makespan = max(h_load[i]+(k if i == h else 0) for i in range(r))
            makespan = max(makespan, max(z_load))
            best = makespan if best is None else min(best, makespan)
            if all(h_count[i]+(1 if i == h else 0) <= count_cap_h for i in range(r)) and max(z_count) <= count_cap_z:
                best_count = makespan if best_count is None else min(best_count, makespan)
            if all(h_load[i]+(k if i == h else 0) <= row_cap_h for i in range(r)) and max(z_load) <= row_cap_z:
                if best_row is None or makespan < best_row:
                    best_row, best_row_assignment = makespan, (h, choices)
    q = min(k, floorq(a*F(k,r)+b))
    if k >= 2 and r >= k:
        assert best == k
        assert best_count == 2*k-1
    if a+b >= 2 and 0 <= q <= k:
        assert best_row == max(k,2*k-q)
        h, choices = best_row_assignment
        witness = [h]+[r+(pos//k) if v else pos//k for pos,v in enumerate(choices)]
        proc, *_ = reconstruct(k,r)
        assert max(loads(proc,witness)) == F(best_row,k)
    return {'k':k,'r':r,'concrete_assignments':examined,
            'OPT':str(F(best,k)),
            'best_with_ceil_count_caps':None if best_count is None else str(F(best_count,k)),
            'a':str(a),'b':str(b),'sink_integer_cap':q,
            'best_with_row_discrepancy_caps':None if best_row is None else str(F(best_row,k))}


def symbolic_checks():
    out=[]
    for k in (2,3,4,8,16,32,64,128):
        r=k*k
        # For a=b=1, r>k gives q=1 exactly.
        q=floorq(F(k,r)+1)
        assert q==1
        lower=F(2*k-q,k)
        assert lower==2-F(1,k)
        # Explicit attainment: one small job goes to each sink.
        hload=1+F(k-1,k)
        zload=F(1,k)
        assert hload<=2 and zload<=F(1,r)+F(1,k)
        # A (2-eps)-schedule needs >=ceil(eps*k) small jobs on B's sink.
        eps=F(1,4)
        needed=ceilq(eps*k)
        assert 1+F(k-needed,k)<=2-eps
        if needed:
            assert 1+F(k-(needed-1),k)>2-eps
        out.append({'k':k,'r':r,'row_cap_lower':str(lower),
                    'quarter_improvement_requires_sink_jobs':needed,
                    'ratio_sink_load_to_fractional_plus_max':str((F(needed,k))/(F(1,r)+F(1,k)))})
    # All fixed nonnegative rational a,b are finite examples, not the universal proof.
    for a,b in ((F(0),F(2)),(F(1),F(1)),(F(3,2),F(3,2)),(F(17),F(5,2))):
        for k in (2,5,23,100):
            r=k*k
            q=min(k,floorq(a*F(k,r)+b))
            if a+b>=2:
                assert F(2*k-q,k)<=a+b
                assert F(q,k)<=a*F(1,r)+b*F(1,k)
    return out


def independent_distribution(k, r):
    distribution = {}
    for bits in product((0,1),repeat=k*r):
        masks = tuple(sum(bits[i*k+t] << t for t in range(k)) for i in range(r))
        ones = sum(bits)
        probability = F(1,r)**ones * F(r-1,r)**(k*r-ones) / r
        for h in range(r):
            if probability:
                distribution[h,masks] = probability
    return distribution


def sharp_nc_distribution(k, r, collision_size=2):
    """Exact marginal-preserving distribution saturating the pair budget.

    At B's home send either one or collision_size jobs to its private sink;
    distribute the remaining sink jobs as singletons on other groups.
    """
    q = collision_size
    assert 2 <= q <= k and r >= k
    collision_probability = F(comb(k,2),r*comb(q,2))
    assert collision_probability <= 1
    distribution = {}
    for h in range(r):
        others = tuple(i for i in range(r) if i != h)
        for active_count, type_weight in ((1,1-collision_probability),(q,collision_probability)):
            if not type_weight: continue
            number_other_groups = k-active_count
            atom_weight = type_weight / (r*comb(r-1,number_other_groups)
                            *comb(k,active_count)*k**number_other_groups)
            for other_groups in combinations(others,number_other_groups):
                for active_jobs in combinations(range(k),active_count):
                    for other_jobs in product(range(k),repeat=number_other_groups):
                        masks = [0]*r
                        masks[h] = sum(1<<t for t in active_jobs)
                        for i,t in zip(other_groups,other_jobs): masks[i]=1<<t
                        key=h,tuple(masks)
                        distribution[key]=distribution.get(key,F(0))+atom_weight
    return distribution


def audit_distribution(k, r, distribution, kind, collision_size=None):
    assert sum(distribution.values()) == 1
    bmarg=[F(0)]*r
    smarg=[[F(0)]*k for _ in range(r)]
    pair=[{tu:F(0) for tu in combinations(range(k),2)} for _ in range(r)]
    expected=F(0)
    total_expected_pairs=F(0)
    good_tail=F(0)
    for (h,masks),weight in distribution.items():
        bmarg[h]+=weight
        counts=[mask.bit_count() for mask in masks]
        # Independent direct makespan computation, in units 1/k.
        direct=max(max(k-counts[i]+(k if i==h else 0) for i in range(r)),max(counts))
        assert F(direct,k)==2-F(counts[h],k)
        expected+=weight*F(direct,k)
        total_expected_pairs+=weight*sum(comb(c,2) for c in counts)
        assert max(counts)<=1+sum(comb(c,2) for c in counts)
        if collision_size and counts[h]>=collision_size: good_tail+=weight
        for i,mask in enumerate(masks):
            for t in range(k):
                if mask>>t&1:smarg[i][t]+=weight
            for t,u in pair[i]:
                if (mask>>t&1) and (mask>>u&1): pair[i][t,u]+=weight
    assert bmarg==[F(1,r)]*r
    assert smarg==[[F(1,r)]*k for _ in range(r)]
    assert all(v<=F(1,r*r) for row in pair for v in row.values())
    lower=2-F(1,k)-F(k-1,2*r)
    assert expected>=lower
    if kind=='independent': assert expected==2-F(1,r)
    if kind=='sharp_nc' and collision_size==2: assert expected==lower
    if kind=='sharp_nc':
        q=collision_size
        bound=F(k*(k-1),r*q*(q-1))
        assert good_tail==bound
    return {'k':k,'r':r,'kind':kind,'collision_size':collision_size,
            'positive_atoms':len(distribution),
            'all_job_and_B_marginals_exact':True,'same_sink_pair_negative_correlation':True,
            'expected_makespan':str(expected),'universal_NC_lower':str(lower),
            'total_expected_sink_pairs':str(total_expected_pairs),
            'pair_budget':str(F(k*(k-1),2*r)),
            'tail_probability_at_collision_size':str(good_tail) if collision_size else None}


def main():
    reconstructed=[]
    for k,r in ((1,1),(1,3),(2,2),(2,4),(3,3),(3,4),(4,4),(4,16)):
        reconstruct(k,r)
        reconstructed.append([k,r])
    # The k=1 cases test construction boundaries and are not asymptotic claims.
    finite=[direct_oracle(k,r) for k,r in ((1,1),(1,3),(2,2),(2,4),(3,3),(3,4),(4,4))]
    finite += [direct_oracle(2,3,F(0),F(2)), direct_oracle(2,3,F(1,2),F(1,2))]
    distribution_checks=[]
    for k,r in ((2,2),(2,4),(3,3),(3,4)):
        distribution_checks.append(audit_distribution(k,r,independent_distribution(k,r),'independent'))
    for k,r in ((2,2),(2,4),(3,3),(3,9),(4,6)):
        distribution_checks.append(audit_distribution(k,r,sharp_nc_distribution(k,r),'sharp_nc',2))
    distribution_checks.append(audit_distribution(4,6,sharp_nc_distribution(4,6,3),'sharp_nc',3))
    result={'purpose':'finite exact audit; not a proof of the general claim',
            'arithmetic':'Fraction plus independently scaled integer enumeration',
            'python':sys.version,'platform':platform.platform(),
            'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'reconstructed_parameters':reconstructed,
            'complete_assignment_oracles':finite,
            'exact_probability_distributions':distribution_checks,
            'symbolic_parameter_checks':symbolic_checks(),
            'limits':'Full concrete enumeration only on listed small cases; no general algorithm or novelty certification.'}
    print(json.dumps(result,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
