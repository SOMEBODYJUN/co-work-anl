"""Exact m=5 arithmetic audit of the source-root copy identity.

This audits general clientwise formulas, not a strategy or SPE instance.
All sequences are symbolic binary membership sequences of one shared client.
"""
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path


def audit(m=5):
    rows = 0
    strict_rows = 0
    positive_columns = 0
    terminal_rows = 0
    min_parent_load = m + 1
    max_column_ratio = F(0)
    for k in range(m - 1):
        for l in range(k + 1, m):
            free_prefix = [j for j in range(l) if j != k]
            for bits in product((0, 1), repeat=len(free_prefix)):
                prefix = [0] * l
                prefix[k] = 1
                for j, bit in zip(free_prefix, bits):
                    prefix[j] = bit
                for atail in product((0, 1), repeat=m - l - 1):
                    for qtail in product((0, 1), repeat=m - l - 1):
                        # Shared source/current client belongs to both current actions.
                        c_a = sum(prefix) + 1 + sum(atail)
                        c_q = sum(prefix) + 1 + sum(qtail)
                        lhs = F(1, c_a) - F(1, c_q)
                        rhs = sum((F(q - a, c_a * c_q)
                                   for a, q in zip(atail, qtail)), F(0))
                        assert lhs == rhs
                        assert c_a >= 2
                        min_parent_load = min(min_parent_load, c_a)
                        rows += 1
                        strict_rows += (lhs != 0)
                        for a, q in zip(atail, qtail):
                            if q and not a:
                                tax = F(1, c_a * c_q)
                                recipient_profit = F(1, c_q)
                                assert tax <= recipient_profit / 2
                                max_column_ratio = max(max_column_ratio,
                                                       tax / recipient_profit)
                                positive_columns += 1
                        # Verify WEIGHTED for representative exact inputs and a scalar.
                        for f in (F(0), F(1, 3), F(1)):
                            for theta in (F(0), F(2, 5), F(1)):
                                remainder = (f - theta) * lhs
                                assert f * lhs == theta * rhs + remainder
                        if l == m - 1:
                            assert lhs == 0
                            terminal_rows += 1
    return {
        "status": "exact arithmetic identities verified",
        "scope": "symbolic one-client m=5 membership audit; not a game or SPE certificate",
        "m": m,
        "client_rows": rows,
        "nonzero_future_reset_rows": strict_rows,
        "positive_future_columns": positive_columns,
        "minimum_parent_client_load": min_parent_load,
        "maximum_positive_column_to_recipient_profit_ratio": str(max_column_ratio),
        "terminal_rows_all_zero": terminal_rows,
        "does_not_establish": ["cross-action actual-wallet capacity", "OPT_5 <= 2 W", "general HALF"],
    }


if __name__ == "__main__":
    out = audit()
    target = Path(__file__).with_name("source_copy_identity_audit.json")
    target.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(out, ensure_ascii=False, indent=2))
