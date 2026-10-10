#!/usr/bin/env python3
"""Independent standard-library exact check of all joint-budget coefficients."""
from fractions import Fraction as F
from itertools import combinations_with_replacement
from pathlib import Path
import argparse, hashlib, json


def restricted_growth(length, labels=6):
    if length == 0:
        yield ()
        return
    def visit(prefix, high):
        if len(prefix) == length:
            yield tuple(prefix)
            return
        for label in range(min(high+1, labels-1)+1):
            yield from visit(prefix+[label], max(high, label))
    yield from visit([0], 0)


def customer_rows(n, incidence, true_players):
    """Coefficients of nonnegative SPE slacks, from raw unit-customer equal sharing."""
    count = true_players.bit_count()
    pay = [F(int(true_players >> t & 1), count) if count else F(0) for t in range(n)]
    bits = incidence.bit_count()
    mixed = []
    for t in range(n):
        if incidence == 63:
            floor = F(1, n)
        elif bits == 1:
            floor = F(1, 2*n)
        else:
            floor = F(1, 3*n-2*t) if t < n-1 else F(n+1, n*(n+5))
        mixed.append(pay[t]-floor)
    prior = (true_players & ((1 << (n-1))-1)).bit_count()
    last = [pay[-1]-F(int(incidence >> j & 1), prior+1) for j in range(6)]
    prefix = (true_players & ((1 << (n-2))-1)).bit_count()
    suffix = pay[-2]+pay[-1]
    tax = F(int(true_players >> (n-2) & 1), (prefix+1)*(prefix+2))
    pair_rows = []
    for first, second in combinations_with_replacement(range(6), 2):
        covers = int(incidence >> first & 1)+int(incidence >> second & 1)
        comparison = F(covers, prefix+covers) if covers else F(0)
        pair_rows.append(suffix+tax-comparison)
    return mixed+last+pair_rows


def all_true_subsets(eligible, last_required, n):
    subset = eligible
    while True:
        if bool(subset >> (n-1) & 1) == last_required:
            yield subset
        if subset == 0:
            break
        subset = (subset-1) & eligible


def universal_multipliers(n):
    return ([F(35,48) if t < n-2 else F(0) for t in range(n)]
            +[F(0) if j == 0 else F(1,8) for j in range(6)]
            +[F(5,48) if first == 0 and second != 0
              else F(1,96) if first != second and first != 0 else F(0)
              for first, second in combinations_with_replacement(range(6),2)])


def compressed_residual(n, other_incidence_count, last_incidence, prior_count, penultimate):
    k, f, p, d = other_incidence_count, last_incidence, prior_count, penultimate
    m = k+f
    assert 1 <= m <= 6
    if m == 6:
        floor_sum = F(n-2, n)
    elif m == 1:
        floor_sum = F(n-2, 2*n)
    else:
        floor_sum = sum((F(1, 3*n-2*t) for t in range(n-2)), F(0))
    denominator = p+d+f
    share = F(35*p+30*d+60*f, 48*denominator) if denominator else F(0)
    last_comparison = F(k, 8*(p+d+1))
    pair_with_last = F(k, p+1) if not f else F(5-k, p+1)+F(2*k,p+2)
    pair_without_last = F(k*(5-k), p+1)+F(k*(k-1), p+2)
    return (F(int(denominator > 0))-F(1,2)+F(35,48)*floor_sum
            +last_comparison+F(5,48)*pair_with_last+F(1,96)*pair_without_last
            -share-F(5*d,8*(p+1)*(p+2)))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--certificates', type=Path, default=Path(__file__).resolve().parents[2]/'evidence/certificates/customer_attraction/six_maxima_joint_bound.json')
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    package = json.loads(args.certificates.read_text())
    expected_names = (['mixed:'+str(t) for t in range(5)]
                      +['lastBR:'+str(j) for j in range(6)]
                      +['twoTax:'+str(a)+str(b) for a,b in combinations_with_replacement(range(6),2)])
    assert package['row_order_n5'] == expected_names
    certificates = package['n5_certificates']
    assert len(certificates) == 52
    assert {tuple(item['route']) for item in certificates} == set(restricted_growth(5))
    assert len({tuple(item['route']) for item in certificates}) == 52
    scale = package['n5_common_denominator']
    assert scale == 10000
    total_columns = 0
    n5_min = None
    certificate_counts = []
    for item in certificates:
        route = item['route']
        numerator = item['multipliers_numerator']
        assert len(numerator) == 32
        assert all(isinstance(number,int) and number >= 0 for number in numerator)
        multiplier = [F(number,scale) for number in numerator]
        minimum, columns = None, 0
        for incidence in range(1,64):
            eligible = sum(1 << t for t,j in enumerate(route) if incidence >> j & 1)
            required = bool(incidence >> route[-1] & 1)
            for true in all_true_subsets(eligible,required,5):
                rows = customer_rows(5,incidence,true)
                residual = F(int(true != 0))-F(1,2)-sum((weight*row for weight,row in zip(multiplier,rows)),F(0))
                assert residual >= 0,(route,incidence,true,residual)
                minimum = residual if minimum is None else min(minimum,residual)
                columns += 1
        assert columns == item['column_count']
        assert minimum == F(item['minimum_residual'])
        total_columns += columns
        n5_min = minimum if n5_min is None else min(n5_min,minimum)
        certificate_counts.append(columns)
    universal = {}
    compressed_checks = 0
    for n, expected_min in [(6,F(1,72)),(7,F(1,32)),(8,F(23393,532224))]:
        multiplier = universal_multipliers(n)
        minimum, columns, compressed_min = None,0,None
        for incidence in range(1,64):
            required = bool(incidence & 1)
            eligible = ((1 << (n-1))-1)+((1 << (n-1)) if required else 0)
            for true in all_true_subsets(eligible,required,n):
                rows = customer_rows(n,incidence,true)
                residual = F(int(true != 0))-F(1,2)-sum((weight*row for weight,row in zip(multiplier,rows)),F(0))
                p = (true & ((1 << (n-2))-1)).bit_count()
                d = int(true >> (n-2) & 1)
                compressed = compressed_residual(n,(incidence >> 1).bit_count(),int(required),p,d)
                assert residual == compressed,(n,incidence,true,residual,compressed)
                assert residual >= 0
                minimum = residual if minimum is None else min(minimum,residual)
                columns += 1
        for f in (0,1):
            for k in range(6):
                if k+f == 0:continue
                for p in range(n-1):
                    for d in (0,1):
                        residue = compressed_residual(n,k,f,p,d)
                        assert residue >= 0
                        compressed_min = residue if compressed_min is None else min(compressed_min,residue)
                        compressed_checks += 1
        assert minimum == expected_min == compressed_min
        assert columns == 63*(1 << (n-1))
        universal[n] = {'literal_columns':columns,'minimum_residual':str(minimum),'coverage_fraction_lower':str(F(1,2)+minimum)}
    # The private floor used above follows the published suffix envelope for every n>=5.
    private_checks = 0
    for n in range(5,101):
        raw = [F(n+t,2*(t+1)*(3*n-2*t)) for t in range(n-1)]+[F(1,n+5)]
        envelope = [min(raw[t:]) for t in range(n)]
        assert all(value >= F(1,2*n) for value in envelope)
        shared = [F(1,3*n-2*t) for t in range(n-1)]+[F(n+1,n*(n+5))]
        assert all(first <= second for first,second in zip(shared,shared[1:]))
        private_checks += n
    report = {'status':'passed','scope':'All52 complete five-player routing classes and all true customer memberships; a broader path-free true-membership domain for six/seven/eight players. Coefficients of exact nonnegative SPE slacks only.','n5_routes':52,'n5_column_inequalities':total_columns,'n5_row_count':32,'n5_minimum_residual':str(n5_min),'n5_column_counts':certificate_counts,'universal':universal,'compressed_universal_cases':compressed_checks,'private_envelope_points':private_checks,'certificate_sha256':hashlib.sha256(args.certificates.read_bytes()).hexdigest(),'audit_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'proof_sha256':hashlib.sha256((Path(__file__).resolve().parents[2]/'research/current/customer_attraction/six_maxima_joint_bound.md').read_bytes()).hexdigest(),'claim_id':'CA-SIX-MAXIMA-HALF'}
    print(json.dumps(report,indent=2))
    if args.output:
        assert not args.output.exists(),'Frozen output exists; choose a new destination.'
        args.output.write_text(json.dumps(report,indent=2)+'\n')

if __name__ == '__main__':
    main()
