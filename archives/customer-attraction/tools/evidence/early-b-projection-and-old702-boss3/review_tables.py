"""Informed independent exact audit from uncancelled S/Z/V menu identities.

No historical program is imported; no LP or SPE solver is called.  All 1,344
table cells and the exact visible marginal of the selected old point are read.
"""
from fractions import Fraction as Q
from itertools import product
from collections import defaultdict
from pathlib import Path
import hashlib
import json
import time

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
CERT = HERE / "original/519adddb8a5e5058acc5/early_B_projection_certificate.json"
POINT = REPO / "archives/customer-attraction/tools/evidence/full156-tail-parent-report/original/research_5/combined_branch_master_exact.json"
WEIGHTS = {
    2: dict(F=771984, G=6492, L1=20517, L2=36285, CAP3=44168, CAP4=44610, H=5256, E=7186),
    3: dict(F=11958, G=172, CAP1=180, CAP2=1169, CAP3=1214, E=188),
    4: dict(F=89632, G=2576, L1=11205, L2=11557, CAP1=6311, CAP2=6899, E=2832),
}


def share(bit, count):
    return Q(bit, count) if bit else Q()


def main():
    started = time.monotonic()
    cert = json.loads(CERT.read_text())
    point_hash = hashlib.sha256(POINT.read_bytes()).hexdigest()
    assert set(cert) == {"status", "point_path", "point_sha256", "rows"}
    assert cert["status"] == "EXACT_VALID_NECESSARY_PROJECTIONS_SEPARATING_SELECTED_5108_POINT_ONLY"
    assert point_hash == cert["point_sha256"] == "d1aeba67e20c8d8fc7ff38cd6566ac05c3771731f586584e5c6f1dfe233472a8"
    point = json.loads(POINT.read_text())
    masses, hist_count, K = defaultdict(Q), 0, Q()
    for col in point["columns"]:
        if col["kind"] == "hist":
            bits = col["actual_bits"]
            assert len(bits) == 6 and set(bits) <= {"0", "1"}
            assert 0 <= col["d"] <= 6 and Q(col["weight"]) >= 0
            assert len(col["hist"]) == 8 and sum(col["hist"]) == 6
            assert sum(col["hist"][4:]) == col["d"]
            masses[bits, col["d"]] += Q(col["weight"])
            hist_count += 1
        elif col["kind"] == "K":
            K += Q(col["weight"])
    assert hist_count == 16 and K >= 0
    O = sum((v for (_, d), v in masses.items() if d), Q())
    W = sum((v for (a, _), v in masses.items() if "1" in a), Q())
    assert O == Q(point["O"]) == 1 and W == Q(point["W"])
    reports = []
    total_states = total_h_states = 0
    assert [r["source"] for r in cert["rows"]] == [2, 3, 4]
    for record in cert["rows"]:
        assert set(record) == {"source", "weights", "kappa", "coefficient_domain", "point_value", "point_value_decimal", "table"}
        source = record["source"]
        weights = WEIGHTS[source]
        assert record["weights"] == weights and min(weights.values()) > 0
        kappa = sum(w for name, w in weights.items() if name.startswith("CAP"))
        assert record["kappa"] == kappa
        assert record["coefficient_domain"] == dict(actual_bit_patterns=64, d_values=7,
            hidden_bit_patterns=2 ** (6-source), ell_values=7, full_ell_matches_endpoints=True)
        calculated = []
        state_count = h_count = 0
        for actual in product(range(2), repeat=6):
            bits = "".join(map(str, actual))
            actual_total = sum(actual)
            actual_pay = [share(a, actual_total) for a in actual]
            for d in range(7):
                maximum = endpoint_maximum = None
                for hidden in product(range(2), repeat=6-source):
                    terminal = actual[:source-1] + (actual[5],) + hidden
                    size = sum(terminal)
                    p = sum(terminal[:4])
                    x, y = terminal[4:]
                    vx, vy = share(x, size), share(y, size)
                    D = (p+1) * (p+2)
                    for ell in range(7):
                        Z = 6*vy-Q(ell, p+x+1)
                        G = 6*vx-Q(d, p+1)+Q(d*ell, 6*D)+Z/12
                        for overlap in range(max(0, d+ell-6), min(d, ell)+1):
                            S = 6*vx-Q(d, p+1)+Q(overlap, D)
                            V = Q(d*ell-6*overlap, D)
                            assert S+Z/12+V/6 == G
                            h_count += 1
                        parts = {"F": actual_pay[source-1]-share(actual[5], size),
                                 "G": G, "E": 6*vy-Q(d, p+x+1)}
                        for j, bit in enumerate(hidden, 1):
                            parts[f"CAP{j}"] = -Q(bit)
                            parts[f"L{j}"] = actual_pay[5]-Q(bit, 1+sum(actual[:5]))
                        if source == 2:
                            parts["H"] = share(hidden[1], size)-Q(hidden[3], 3+actual[0]+actual[5]+hidden[0])
                        value = sum((w*parts[name] for name, w in weights.items()), Q())
                        maximum = value if maximum is None else max(maximum, value)
                        if ell in (0, 6):
                            endpoint_maximum = value if endpoint_maximum is None else max(endpoint_maximum, value)
                        state_count += 1
                assert maximum == endpoint_maximum
                calculated.append(dict(actual_bits=bits, d=d, psi=str(maximum)))
        assert len(calculated) == 448 and calculated == record["table"]
        lookup = {(c["actual_bits"], c["d"]): Q(c["psi"]) for c in calculated}
        contributions = [{"actual_bits": a, "d": d, "mass": str(mass),
                          "psi": str(lookup[a,d]), "contribution": str(mass*lookup[a,d])}
                         for (a,d),mass in masses.items() if mass]
        value = sum((lookup[key]*mass for key,mass in masses.items()), Q()) + kappa*K
        assert value == Q(record["point_value"]) < 0
        assert float(value) == record["point_value_decimal"]
        reports.append(dict(source=source, kappa=kappa, coefficient_cells_equal=448,
            full_hidden_states=state_count, uncancelled_menu_overlap_states=h_count,
            minimum_table_coefficient=str(min(lookup.values())),
            maximum_table_coefficient=str(max(lookup.values())), point_value=str(value),
            positive_marginal_contributions=contributions, K_contribution=str(kappa*K)))
        total_states += state_count
        total_h_states += h_count
    assert total_states == 87808 and total_h_states == 150528
    out = dict(scope="complete local coefficient-domain and selected-point marginal check; no full graph or SPE verification",
        certificate_sha256=hashlib.sha256(CERT.read_bytes()).hexdigest(), point_sha256=point_hash,
        visible_cells_equal=1344, full_hidden_states=total_states,
        uncancelled_menu_overlap_states=total_h_states, hist_records_read=hist_count,
        positive_aggregated_actual_marginals=sum(v>0 for v in masses.values()),
        K=str(K), O=str(O), W=str(W), rows=reports,
        elapsed_seconds=time.monotonic()-started)
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
