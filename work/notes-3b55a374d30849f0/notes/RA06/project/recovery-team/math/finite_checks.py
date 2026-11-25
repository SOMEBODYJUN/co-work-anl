"""Small independent checks for RA06 math recovery.
No OCR/ledger mutation.  Run with Python 3.12.
"""
from itertools import product
from fractions import Fraction


def is_topology(fam, n):
    """fam is a set of bitmasks denoting subsets of an n-element set."""
    full=(1<<n)-1
    if 0 not in fam or full not in fam: return False
    # finite test: arbitrary unions reduce to unions of all subfamilies;
    # closure under binary unions implies this, but check all for clarity.
    fs=list(fam)
    for r in range(len(fs)+1):
        # no need enumerate all combinations for n<=3 used here
        pass
    for A in fs:
        for B in fs:
            if (A|B) not in fam or (A&B) not in fam: return False
    # all unions of finite families (binary closure already enough)
    return True


def count_topologies(n):
    num_subsets=1<<n
    count=0
    examples=[]
    for fam_mask in range(1<<num_subsets):
        fam={s for s in range(num_subsets) if fam_mask>>s & 1}
        if is_topology(fam,n):
            count+=1
            if len(examples)<2: examples.append(sorted(fam))
    return count, examples


def cube_tests():
    # Candidate endpoint/exponent interpretations for a bounded subset M of R^n.
    n=2; a=3
    M={(0,0),(2,-1)}
    canonical=all(-a <= z <= a for x in M for z in x)
    M_counter={(n+1,0)}
    fixed_n_endpoint=all(-a <= z <= n for x in M_counter for z in x)
    # a cardinal exponent c is not a finite Cartesian product in R^n; report type failure.
    return canonical, fixed_n_endpoint


def maximal_interval_test():
    # U=(0,1) union (2,3); component (0,1) has endpoints outside U.
    U=lambda x: (0<x<1) or (2<x<3)
    eps=Fraction(1,100)
    left,right=Fraction(0),Fraction(1)
    interior=all(U(Fraction(i,100)) for i in range(1,100))
    endpoints_out=(not U(left)) and (not U(right))
    # no extension by eps on either side remains in U
    no_left_extension=not U(left-eps)
    no_right_extension=not U(right+eps)
    return interior,endpoints_out,no_left_extension,no_right_extension


def closure_decomposition_counterexample():
    # One-point discrete metric X={a}, E=X. E is clopen, so boundary=empty and E'=empty.
    E={0}; interior=E; boundary=set(); derived=set()
    interior_identity=(E == interior | boundary)
    derived_identity=(E == derived | boundary)
    return interior_identity, derived_identity

if __name__ == '__main__':
    counts={n:count_topologies(n)[0] for n in (1,2,3)}
    print('topology_counts_n1_n2_n3', counts)
    print('cube_canonical, fixed_endpoint_n', cube_tests())
    print('maximal_interval', maximal_interval_test())
    print('closure_decomposition_interior, derived', closure_decomposition_counterexample())
