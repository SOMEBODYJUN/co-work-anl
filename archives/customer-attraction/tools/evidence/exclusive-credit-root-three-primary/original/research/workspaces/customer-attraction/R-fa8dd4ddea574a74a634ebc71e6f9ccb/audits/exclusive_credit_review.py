"""Independent root check using the pre-existing canonical definition verifier."""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json
import sys

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT))
from customer_attraction import Instance, StrategyCertificate, verify_certificate


def main():
    base = Path(__file__).resolve().parent.parent / 'global_proof'
    ip = base / 'exclusive_credit_four_instance.json'
    cp = base / 'exclusive_credit_four_certificate.json'
    instance = Instance.from_dict(json.loads(ip.read_text()))
    cert = StrategyCertificate.from_dict(json.loads(cp.read_text()))
    report = verify_certificate(instance, cert)
    report.assert_valid()
    path = report.terminal_history
    assert path == (0, 0, 1, 2)
    customers = [frozenset(c.topics) for c in instance.customers
                 for _ in range(c.multiplicity)]
    sets = [frozenset(i for i, c in enumerate(customers) if a in c)
            for a in range(4)]
    assert len(set(sets)) == 4
    loads = [sum(a in c for a in path) for c in customers]
    utilities = [sum((F(1, n) for c, n in zip(customers, loads) if a in c), F(0))
                 for a in path]
    queries = [sum((F(1, n+1) for c, n in zip(customers, loads) if a in c), F(0))
               for a in range(4)]
    credit = sum((F(1, 2) for c, n in zip(customers, loads) if path[0] in c and n == 1), F(0))
    welfare = sum(n > 0 for n in loads)
    G = sum((F(1, n+1) for n in loads if n), F(0))
    maximum = max(queries)
    assert utilities == [F(13,4), F(13,4), F(17,4), F(21,4)]
    assert queries == [F(71,30), F(11,5), F(16,5), F(37,10)]
    assert credit == 0
    assert utilities[0] + credit - maximum == -F(9,20)
    assert welfare == instance.optimal_welfare() == 16
    assert welfare + G - 4*maximum == F(106,15)
    print(json.dumps({
        'status': 'independent canonical SPE and root arithmetic check passed',
        'unit_customers': len(customers),
        'distinct_coverage_sets': len(set(sets)),
        'ordered_histories': report.checked_histories,
        'nontrivial_deviations': report.checked_deviations,
        'actual_path': path,
        'utilities': list(map(str, utilities)),
        'queries': list(map(str, queries)),
        'exclusive_credit': str(credit),
        'local_gap': str(utilities[0] + credit - maximum),
        'global_credit_gap': str(welfare + G - 4*maximum),
        'W': welfare, 'OPT': instance.optimal_welfare(),
        'instance_sha256': hashlib.sha256(ip.read_bytes()).hexdigest(),
        'certificate_sha256': hashlib.sha256(cp.read_bytes()).hexdigest(),
        'scope': 'local exclusive-credit induction is false; global bridge and half remain open',
    }, indent=2))


if __name__ == '__main__':
    main()
