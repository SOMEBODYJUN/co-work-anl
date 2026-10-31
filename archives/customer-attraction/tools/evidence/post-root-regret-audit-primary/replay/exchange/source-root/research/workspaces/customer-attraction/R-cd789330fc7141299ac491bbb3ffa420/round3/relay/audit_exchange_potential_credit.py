"""Definition-level audit of the all-input exchange-potential components.

Checks arbitrary incidence patterns (a superset of legal histories), and
checks the cross-rollout identity on one frozen full SPE input. No solver
or other author audit is imported. No new instance or local positive theorem.
"""
from fractions import Fraction as F
from itertools import permutations
from math import factorial
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
WORKSPACE = HERE.parent.parent


def H(c):
    return sum((F(1, j) for j in range(1, c+1)), F())


def beta(a, c):
    assert a >= 1 and c >= 1
    return F(factorial(a-1)*factorial(c-1), factorial(a+c-1))


def phi_x(A, B):
    a, c = A.bit_count(), B.bit_count()
    if not a:
        return H(c)
    return F() if A & B else -beta(a, c+1)


def owner_x(owner, B):
    c = B.bit_count()
    return F(1) if (B >> owner) & 1 else F(c, c+1)


def pattern_audit():
    marginal_checks = leaf_checks = prefix_checks = 0
    for m in range(1, 8):
        for A in range(1 << m):
            for B in range(1 << m):
                c = B.bit_count()
                rebate_sum = F()
                for i in range(m):
                    if not (B >> i) & 1:
                        continue
                    marginal = phi_x(A, B)-phi_x(A, B & ~(1 << i))
                    assert 0 <= marginal <= F(1, c)
                    if not A:
                        assert marginal == F(1, c)
                    rebate_sum += F(1, c)-marginal
                    marginal_checks += 1
                assert 0 <= rebate_sum <= int(bool(A and c))
                leaf_checks += 1
                if A:
                    owner = (A & -A).bit_length()-1
                    mod_sum = F()
                    for i in range(m):
                        if (B >> i) & 1:
                            marginal = owner_x(owner, B)-owner_x(owner, B & ~(1 << i))
                            assert 0 <= marginal <= F(1, c)
                            mod_sum += marginal
                    expected = F() if c == 0 else (F(1, c) if (B >> owner) & 1 else F(1, c+1))
                    assert mod_sum == expected
            if not A:
                continue
            a = A.bit_count()
            owner = (A & -A).bit_length()-1
            max_beta_sum = max_owner_sum = F()
            for i in range(m):
                if not (A >> i) & 1:
                    continue
                anchor = A & ((1 << i)-1)
                worst_beta = worst_owner = F()
                for future in range(1 << (m-i-1)):
                    B = anchor | (1 << i) | (future << (i+1))
                    c = B.bit_count()
                    beta_margin = phi_x(A, B)-phi_x(A, B & ~(1 << i))
                    own_margin = owner_x(owner, B)-owner_x(owner, B & ~(1 << i))
                    rb, ro = F(1, c)-beta_margin, F(1, c)-own_margin
                    worst_beta, worst_owner = max(worst_beta, rb), max(worst_owner, ro)
                    prefix_checks += 1
                max_beta_sum += worst_beta
                max_owner_sum += worst_owner
            assert max_beta_sum <= H(a-1) <= a-1
            assert max_owner_sum <= H(a)-1 <= a-1
            if a == 1:
                assert max_beta_sum == max_owner_sum == 0
    return dict(marginal_checks=marginal_checks, same_leaf_checks=leaf_checks,
                all_future_prefix_incidence_checks=prefix_checks)


def rollout_audit():
    source = WORKSPACE / 'round2/global/pi_fixed_cone_counterexample.json'
    data = json.loads(source.read_text())
    customers = [(frozenset(row['topics']), int(row['multiplicity'])) for row in data['instance']['customers']]
    policy = {tuple(row['history']): row['action'] for row in data['strategy']['actions']}
    m = 3

    def terminal(h):
        while len(h) < m:
            h += (policy[h],)
        return h

    def utility(topic, B):
        return sum((F(w, sum(a in C for a in B if a is not None)) for C, w in customers if topic in C), F())

    T = (1, 2, 4)
    # Customers are stored as types; optimal membership/owner are type-level.
    rows = []
    for pi in permutations(T):
        def pot(B):
            total = F()
            for C, w in customers:
                opt_slots = [i for i, a in enumerate(pi) if a in C]
                c = sum(a in C for a in B if a is not None)
                if not opt_slots:
                    total += w*H(c)
                else:
                    owner = opt_slots[0]
                    s = B[owner] is not None and B[owner] in C
                    total += w*(F(1) if s else F(c, c+1))
            return total
        optimum = sum(w for C, w in customers if any(a in C for a in pi))
        assert optimum == 324
        Z = terminal(())
        query_credit = IC = prior_credit = debt = F()
        for i in range(m):
            h = pi[:i]
            before, after = terminal(h), terminal(h+(pi[i],))
            u, d = utility(before[i], before), utility(pi[i], after)
            gap = u-d
            assert gap >= 0
            before_removed = before[:i]+(None,)+before[i+1:]
            after_removed = after[:i]+(None,)+after[i+1:]
            ell_before = pot(before)-pot(before_removed)
            ell_after = pot(after)-pot(after_removed)
            e, r = u-ell_before, d-ell_after
            D = pot(after_removed)-pot(before_removed)
            assert pot(after)-pot(before) == e-r-gap+D
            assert e >= 0 and r >= 0
            query_credit += r
            IC += gap
            prior_credit += e
            debt += D
        assert optimum-pot(Z)+query_credit+IC == prior_credit+debt
        # The exact prior-leaf joint credit is checked separately from cross-leaf e.
        old_mod = old_rebate = F()
        for i in range(m):
            removed = Z[:i]+(None,)+Z[i+1:]
            ell = pot(Z)-pot(removed)
            old_mod += ell
            old_rebate += utility(Z[i], Z)-ell
        I = sum(w for C, w in customers if any(a in C for a in pi) and any(a in C for a in Z))
        assert old_rebate <= I
        rows.append(dict(pi=list(pi), initial_potential=str(pot(Z)), query_credit=str(query_credit),
                         IC_slack=str(IC), cross_leaf_credit=str(prior_credit),
                         deletion_potential_difference=str(debt), actual_leaf_credit=str(old_rebate),
                         actual_I=I))
    return rows


def main():
    result = dict(status='PASS', pattern_checks=pattern_audit(), rollout_checks=rollout_audit(),
                  scope='All-input component formula audit; the written proof, not enumeration, carries the universal claims.',
                  limitation='No cross-rollout payment bound, matching flow bound or HALF proof is inferred.')
    with (HERE / 'exchange_potential_credit_audit.json').open('x') as f:
        json.dump(result, f, indent=2)
        f.write('\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
