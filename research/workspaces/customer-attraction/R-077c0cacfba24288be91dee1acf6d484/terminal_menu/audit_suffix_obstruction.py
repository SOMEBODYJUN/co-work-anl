"""Independent exact audit of bounded_suffix_security_obstruction.md."""

from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path


def size(k, m, topic):
    return m-k if topic == 0 else k+1


def policy(m, history):
    return next(q for q in range(1, m+1) if q not in history)


def rollout(k, m, suffix_prefix):
    out = list(suffix_prefix)
    while len(out) < k:
        out.append(policy(m, out))
    return out


def utility(k, m, topic, suffix):
    count = suffix.count(topic) + (m-k if topic == 0 else 0)
    return F(size(k, m, topic), count)


def audit_case(k, m, enumerate_tail=False):
    n, L = m-k, k+1
    assert k >= 1 and m >= 2*k+1
    welfare = n+k*L
    optimum = n+(m-1)*L
    assert welfare == m+k*k
    assert optimum == (k+2)*m-2*k-1
    assert optimum-2*welfare == k*(m-2*k-2)-1
    security_rows = 0
    for i in range(1, n+1):
        for topic in range(m+1):
            previous = i-1 if topic == 0 else 0
            sec = F(size(k, m, topic), previous+m-i+1)
            assert F(1) >= sec, (k, m, i, topic, sec)
            security_rows += 1
    tail_histories = tail_rows = 0
    if enumerate_tail:
        for t in range(k):
            for hist in product(range(m+1), repeat=t):
                prescribed = policy(m, hist)
                actual = rollout(k, m, hist+(prescribed,))
                pay = utility(k, m, prescribed, actual)
                assert pay == L
                for alternative in range(m+1):
                    changed = rollout(k, m, hist+(alternative,))
                    devpay = utility(k, m, alternative, changed)
                    assert pay >= devpay, (k, m, hist, alternative, pay, devpay)
                    tail_rows += 1
                tail_histories += 1
    # Explicit missing real early comparison: player n switches from E to Q_1.
    changed_tail = [1]
    while len(changed_tail) < k+1:
        changed_tail.append(policy(m, changed_tail))
    assert F(L, changed_tail.count(1)) > F(1)
    return {
        "k": k, "m": m, "W": welfare, "OPT": optimum,
        "OPT_minus_2W": optimum-2*welfare,
        "security_rows": security_rows,
        "tail_histories": tail_histories, "tail_deviation_rows": tail_rows,
    }


def main():
    grid = []
    for k in range(1, 16):
        for m in range(2*k+1, 2*k+42):
            grid.append(audit_case(k, m))
    tails = [audit_case(2, 9, True), audit_case(3, 10, True)]
    report = {
        "claim": "TM-BOUNDED-SUFFIX-SECURITY-OBSTRUCTION-v1",
        "status": "exact finite audit; general theorem is analytic",
        "grid_cases": len(grid),
        "grid_security_rows": sum(r["security_rows"] for r in grid),
        "enumerated_tails": tails,
        "not_SPE_counterexample": "early real deviation from E to a fresh Q is profitable",
    }
    target = Path(__file__).with_name("suffix_obstruction_audit.json")
    target.write_text(json.dumps(report, indent=2)+"\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
