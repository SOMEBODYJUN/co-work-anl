#!/usr/bin/env python3
"""Independent literal audit of the point-free early shared-X layer.

No generator imports, optimization packages, numerical point files, or writes
outside this audit directory.  All arithmetic is fractions.Fraction.
"""

from collections import Counter
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations_with_replacement, product
from pathlib import Path
import gzip
import json


HERE = Path(__file__).resolve().parent
LAYER = HERE.parent
WORK = LAYER.parent
REPO = WORK.parents[2]


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def read(path):
    with gzip.open(path, "rt") if path.suffix == ".gz" else path.open() as f:
        return json.load(f)


def direct_share(member, other_load):
    """A literal unit customer's share with its own membership included."""
    return F(1, other_load + 1) if member else F(0)


def pair_share(left, right, background):
    return F(1, background + left + right) if left else F(0)


def tax(left, right, background):
    return F(left * right, (background + 1) * (background + 2))


def fprice(member, background):
    return F(member, background + 1)


def literal_tp(background, z, t, left, right):
    return (pair_share(z, t, background) + pair_share(t, z, background)
            + tax(z, z, background) - fprice(left, background)
            - fprice(right, background) + tax(left, right, background))


def universal_budget_audit():
    """Rebuild coefficients from original membership/terminal-payoff formulas."""
    counts = Counter()
    full_domains = []
    for i in range(1, 5):
        r, m = 7 - i, 5 - i
        bvalues, pvalues, last_backgrounds = set(), set(), set()
        for a in product((0, 1), repeat=6):
            b, actual_p = sum(a[:i - 1]), sum(a[:4])
            assert actual_p == b + sum(a[i - 1:4])
            actual_u = direct_share(a[i - 1], sum(a) - a[i - 1])
            bvalues.add(b)
            pvalues.add(actual_p)
            for bits in product((0, 1), repeat=m + 2):
                x, *tail = bits
                ys, t = tuple(tail[:-1]), tail[-1]
                z = ys[-1]
                prefix = b + x + sum(ys[:-1])
                last_backgrounds.add(prefix)
                forced_payoff = direct_share(x, b + sum(ys) + t)
                assert forced_payoff == F(x, b + 1 + sum(ys) + t)
                assert actual_u - forced_payoff == actual_u - F(x, b + 1 + sum(ys) + t)
                counts["source_actual_and_hidden_client_types"] += 1
                terminal_payoff = direct_share(t, b + x + sum(ys))
                assert terminal_payoff == pair_share(t, z, prefix)
                for q in (0, 1):
                    br_literal = terminal_payoff - direct_share(q, b + x + sum(ys))
                    assert br_literal == F(t - q, b + x + sum(ys) + 1)
                    counts["terminal_br_literal_cases"] += 1
                    d = prefix + 1
                    common = F(z, d + t) + F(t, d + z) + F(z, d * (d + 1))
                    expected = (
                        common - F(q + x, d) + F(q * x, d * (d + 1)),
                        common - F(2 * q, d) + F(q, d * (d + 1)),
                        common - F(2 * x, d) + F(x, d * (d + 1)),
                    )
                    literal = (
                        literal_tp(prefix, z, t, q, x),
                        literal_tp(prefix, z, t, q, q),
                        literal_tp(prefix, z, t, x, x),
                    )
                    assert literal == expected
                    counts["tail_pair_literal_coefficients"] += 3
                for member in ys + (t,):
                    assert F(member, actual_p + 1 + x) == (
                        fprice(member, actual_p) - tax(member, x, actual_p))
                    counts["actual_cap_hidden_state_coefficients"] += 1
                # Every 6-index membership pattern is audited below separately;
                # here these selected counts exercise endpoints and fractions.
                for number in range(7):
                    q = F(number, 6)
                    literal_br = sum((terminal_payoff - direct_share(int(k < number),
                                          b + x + sum(ys)) for k in range(6)), F()) / 6
                    assert literal_br == (t - q) / F(b + x + sum(ys) + 1)
                    literal_qx = sum((literal_tp(prefix, z, t, int(k < number), x)
                                     for k in range(6)), F()) / 6
                    literal_qq = sum((literal_tp(prefix, z, t, int(k < number), int(k < number))
                                     for k in range(6)), F()) / 6
                    assert literal_qx == common - (q + x) / d + q*x / (d*(d+1))
                    assert literal_qq == common - 2*q / d + q / (d*(d+1))
                    counts["mean_terminal_and_pair_coefficient_cases"] += 3
        assert bvalues == set(range(i))
        assert pvalues == set(range(5))
        assert last_backgrounds == set(range(5))
        full_domains.append({"source": i, "remaining_players": r, "middles": m,
                             "actual_bits": 64, "tail_bit_states": 2 ** (m + 2),
                             "actual_prefix_load_domain": sorted(bvalues),
                             "actual_P_domain": sorted(pvalues),
                             "last_two_prefix_load_domain": sorted(last_backgrounds)})

    # A SAFE row is derived at its *own* original actual source, with arbitrary
    # true continuation after that source chooses the queried legal label.
    # These future bits are independent of the forced-X branch bits above.
    minimum_safe_remainder = None
    for actual_source in range(1, 7):
        remaining = 7 - actual_source
        for b in range(actual_source):
            for member in (0, 1):
                for followers in product((0, 1), repeat=remaining - 1):
                    true_deviation = direct_share(member, b + sum(followers))
                    floor = F(member, b + remaining)
                    remainder = true_deviation - floor
                    assert remainder >= 0
                    if minimum_safe_remainder is None or remainder < minimum_safe_remainder:
                        minimum_safe_remainder = remainder
                    if actual_source == 6:
                        assert true_deviation == floor
                    counts["SAFE_true_deviation_states_all_six_sources"] += 1

    # Three true IC terms plus one pointwise nonnegative self-tax difference.
    # No sign is asserted for individual-customer IC contributions.
    minimum_self_tax = None
    for background in range(5):
        for z, t, left, right, reply in product((0, 1), repeat=5):
            penultimate = pair_share(z, t, background)
            terminal = pair_share(t, z, background)
            ic1 = penultimate - pair_share(left, reply, background)
            ic2 = pair_share(reply, left, background) - pair_share(right, left, background)
            ic3 = terminal - pair_share(reply, z, background)
            nonnegative = tax(z, z, background) - tax(z, reply, background)
            assert nonnegative == F(z*(1-reply), (background+1)*(background+2)) >= 0
            assert literal_tp(background, z, t, left, right) == ic1 + ic2 + ic3 + nonnegative
            if minimum_self_tax is None or nonnegative < minimum_self_tax:
                minimum_self_tax = nonnegative
            counts["PAIR_three_IC_plus_nonnegative_literal_states"] += 1

    # Old MX and RC use TWO IC terms and one global maximum-price inequality.
    # Their source is always the actual length-four history, so P=0,...,4.
    for actual_p in range(5):
        for a5, a6, x, q, other, reply in product((0, 1), repeat=6):
            actual_u5 = pair_share(a5, a6, actual_p)
            max_budget = fprice(x, actual_p) - fprice(reply, actual_p)
            mx_target = actual_u5 - pair_share(q, x, actual_p)
            mx_paid = (actual_u5 - pair_share(x, reply, actual_p)
                       + pair_share(reply, x, actual_p) - pair_share(q, x, actual_p)
                       + max_budget)
            assert mx_target == mx_paid
            rc_target = (actual_u5 + fprice(x, actual_p) - fprice(q, actual_p)
                         - fprice(other, actual_p) + tax(q, other, actual_p))
            rc_paid = (actual_u5 - pair_share(q, reply, actual_p)
                       + pair_share(reply, q, actual_p) - pair_share(other, q, actual_p)
                       + max_budget)
            assert rc_target == rc_paid
            counts["MX_two_IC_plus_MAX_literal_states"] += 1
            counts["RC_two_IC_plus_MAX_literal_states"] += 1

    # Genuine six-index average: expand each q_i, keeping the diagonal i=i.
    # This is exact before any histogram compression.
    for background in range(5):
        for z, t, x in product((0, 1), repeat=3):
            for indexed_bits in product((0, 1), repeat=6):
                q = F(sum(indexed_bits), 6)
                avg_qx = sum((literal_tp(background, z, t, qj, x)
                              for qj in indexed_bits), F()) / 6
                avg_qq = sum((literal_tp(background, z, t, qj, qj)
                              for qj in indexed_bits), F()) / 6
                d = background + 1
                common = pair_share(z, t, background) + pair_share(t, z, background) + tax(z, z, background)
                assert avg_qx == common - (q+x)/d + q*x/(d*(d+1))
                assert avg_qq == common - 2*q/d + q/(d*(d+1))
                counts["all_six_index_average_patterns"] += 1

    assert counts["source_actual_and_hidden_client_types"] == 7680
    assert counts["SAFE_true_deviation_states_all_six_sources"] == 240
    assert counts["PAIR_three_IC_plus_nonnegative_literal_states"] == 160
    return {"status": "PASS", "counts": dict(sorted(counts.items())),
            "complete_domains": full_domains,
            "minimum_SAFE_local_remainder": str(minimum_safe_remainder),
            "minimum_PAIR_self_tax_remainder": str(minimum_self_tax),
            "global_IC_and_MAX_budgets_not_assumed_pointwise_nonnegative": True,
            "indexed_diagonal_uses_mean_q_not_mean_q_squared": True,
            "optimizer_calls": 0}


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()


def sparse(vector):
    return [[column, str(value)] for column, value in sorted(vector.items()) if value]


def add(vector, column, value):
    if value:
        vector[column] = vector.get(column, F()) + value
        if not vector[column]:
            del vector[column]


def descriptor_inputs():
    path = WORK / "early_x_anchor_queries/columns_21021.json.gz"
    columns = read(path)
    assert len(columns) == 21021 and columns[0] == {"kind": "K"}
    assert all("weight" not in descriptor for descriptor in columns)
    hist = {column: descriptor for column, descriptor in enumerate(columns)
            if descriptor["kind"] == "hist"}
    xcolumns = {descriptor["hist_column"]: column
                for column, descriptor in enumerate(columns)
                if descriptor["kind"] == "common-X-mass"}
    assert len(hist) == 16 and set(xcolumns) == set(hist)
    assert sorted(xcolumns.values()) == list(range(20585, 20601))
    for record in hist.values():
        assert sum(record["hist"]) == 6 and len(record["actual_bits"]) == 6
        assert len(record["hist"]) == 8
    return columns, hist, xcolumns, {"path": str(path.relative_to(REPO)), "sha256": digest(path)}


def independent_expected_layer():
    """Build independently from literal labels, without importing any builder.

    Existing income/F/K contributions use old columns.  Every query term uses
    the source's hidden state columns.  Indexed families are expanded into six
    literal labels before summing; no mean-square expression occurs here.
    """
    old_columns, hist, xcolumns, inputs = descriptor_inputs()
    known = [("A", j) for j in range(6)] + [("indexed", slot) for slot in range(3)]
    states, by_source, columns = {}, {}, []
    for source in range(1, 5):
        middles = 5 - source
        local = []
        for h in hist:
            for bits in product((0, 1), repeat=middles + 2):
                column = 21021 + len(columns)
                state = {"source": source, "hist": h, "x": bits[0],
                         "ys": tuple(bits[1:-1]), "t": bits[-1], "column": column}
                states[source, h, *bits] = column
                columns.append(state)
                local.append(state)
        by_source[source] = local
    assert len(columns) == 1920

    actual = {h: tuple(map(int, descriptor["actual_bits"])) for h, descriptor in hist.items()}
    literal_words = {h: tuple(word for word, multiplicity in
                             zip(product((0, 1), repeat=3), descriptor["hist"])
                             for _ in range(multiplicity)) for h, descriptor in hist.items()}
    incomes = {source: {h: direct_share(a[source - 1], sum(a) - a[source - 1])
                        for h, a in actual.items() if a[source - 1]}
               for source in range(1, 7)}
    price_x = {xcolumns[h]: F(1, sum(a[:4]) + 1) for h, a in actual.items()}

    def sample_bits(query, state):
        family, index = query
        if family == "A":
            return (actual[state["hist"]][index],)
        if family == "indexed":
            return tuple(word[index] for word in literal_words[state["hist"]])
        if family == "Y":
            return (state["ys"][index],)
        if family == "Tnew":
            return (state["t"],)
        assert query == ("X", 0)
        return (state["x"],)

    def income_seed(source):
        return dict(incomes[source])

    def row_from_clients(name, family, source, seed, coefficient):
        row = dict(seed)
        for state in by_source[source]:
            a = actual[state["hist"]]
            add(row, state["column"], coefficient(state, a))
        return {"name": name, "family": family, "source": source, "row": sparse(row), "rhs": "0"}

    rows, equalities = [], []
    for source in range(1, 5):
        middles = 5 - source
        new_queries = [("Y", position) for position in range(middles)] + [("Tnew", 0)]
        terminal_queries = [("X", 0)] + known + [("Y", position) for position in range(middles)]
        pair_queries = known + [("Y", position) for position in range(middles)]
        rows.append(row_from_clients(["source_IC", source], "source_IC", source, income_seed(source),
                    lambda state, a: -direct_share(state["x"], sum(a[:source-1]) + sum(state["ys"]) + state["t"])))
        for query in new_queries:
            for actual_source in range(1, 7):
                rows.append(row_from_clients(["actual_SAFE", source, query, actual_source], "actual_SAFE", source,
                            income_seed(actual_source),
                            lambda state, a, query=query, actual_source=actual_source:
                                -F(sample_bits(query, state)[0], sum(a[:actual_source-1])+7-actual_source)))
            rows.append(row_from_clients(["MAX", source, query], "MAX", source, price_x,
                        lambda state, a, query=query: -fprice(sample_bits(query, state)[0], sum(a[:4]))))
            rows.append(row_from_clients(["capacity", source, query], "capacity", source, {0:F(1)},
                        lambda state, a, query=query: -F(sample_bits(query, state)[0])))
            rows.append(row_from_clients(["actual_cap", source, query], "actual_cap", source, income_seed(5),
                        lambda state, a, query=query: -pair_share(sample_bits(query, state)[0], state["x"], sum(a[:4]))))
        for query in terminal_queries:
            def terminal(state, a, query=query):
                background = sum(a[:source-1]) + state["x"] + sum(state["ys"])
                bits = sample_bits(query, state)
                return (sum((direct_share(state["t"], background) - direct_share(qj, background)
                             for qj in bits), F()) / len(bits))
            rows.append(row_from_clients(["terminal_BR", source, query], "terminal_BR", source, {}, terminal))
        for query in pair_queries:
            for right in ("X", "diagonal"):
                def pair(state, a, query=query, right=right):
                    background = sum(a[:source-1]) + state["x"] + sum(state["ys"][:-1])
                    bits = sample_bits(query, state)
                    return sum((literal_tp(background, state["ys"][-1], state["t"],
                                           qj, state["x"] if right == "X" else qj)
                                for qj in bits), F()) / len(bits)
                rows.append(row_from_clients(["TP", source, query, right], "TP", source, {}, pair))
        rows.append(row_from_clients(["TP", source, "X", "X"], "TP", source, {},
                    lambda state, a: literal_tp(sum(a[:source-1])+state["x"]+sum(state["ys"][:-1]),
                                               state["ys"][-1], state["t"], state["x"], state["x"])))

        rc_seed = income_seed(5)
        for column, value in price_x.items():
            add(rc_seed, column, value)
        for left, right in combinations_with_replacement(new_queries, 2):
            def rc_same(state, a, left=left, right=right):
                p = sum(a[:4])
                q, r = sample_bits(left, state)[0], sample_bits(right, state)[0]
                return -fprice(q, p)-fprice(r, p)+tax(q, r, p)
            rows.append(row_from_clients(["RC_same_branch", source, left, right], "RC_same_branch", source,
                                         rc_seed, rc_same))
        for left in new_queries:
            for right in known:
                def rc_known(state, a, left=left, right=right):
                    p = sum(a[:4])
                    q = sample_bits(left, state)[0]
                    bits = sample_bits(right, state)
                    return sum((-fprice(q, p)-fprice(r, p)+tax(q, r, p) for r in bits), F()) / len(bits)
                rows.append(row_from_clients(["RC_known_query", source, left, right], "RC_known_query", source,
                                             rc_seed, rc_known))
        for h in hist:
            for x in (0, 1):
                row = {xcolumns[h]: F(-1) if x else F(1)}
                if not x:
                    row[h] = F(-1)
                for state in by_source[source]:
                    if state["hist"] == h and state["x"] == x:
                        row[state["column"]] = F(1)
                equalities.append({"name": ["mass", source, h, x], "row": sparse(row), "rhs":"0"})

    assert len(rows) == 436 and len(equalities) == 128
    expected_counts = {"source_IC":4, "actual_SAFE":84, "MAX":14, "capacity":14,
                       "actual_cap":14, "terminal_BR":50, "TP":96,
                       "RC_same_branch":34, "RC_known_query":126}
    assert dict(Counter(row["family"] for row in rows)) == expected_counts
    signatures = Counter(canonical(row["row"]) for row in rows)
    eqsignatures = Counter(canonical(row["row"]) for row in equalities)
    return {"columns":columns, "rows":rows, "equalities":equalities,
            "summary":{"status":"INDEPENDENT_EXPECTED_LAYER_BUILT", "new_columns":len(columns),
                       "raw_inequalities":len(rows), "unique_exact_row_vectors":len(signatures),
                       "raw_equalities":len(equalities), "unique_exact_equality_vectors":len(eqsignatures),
                       "raw_nonzeros":sum(len(row["row"]) for row in rows),
                       "equality_nonzeros":sum(len(row["row"]) for row in equalities),
                       "row_families":expected_counts, "input":inputs,
                       "ordered_independent_rows_sha256":sha256(canonical(rows)).hexdigest(),
                       "unordered_row_vector_multiset_sha256":sha256(canonical(sorted(
                           [row["row"] for row in rows], key=lambda row:canonical(row)))).hexdigest()}}


def audit_packet(expected):
    packet_path = LAYER / "symbolic_append.json.gz"
    contract_path = LAYER / "base_coordinate_contract.json"
    full_columns_path = LAYER / "columns_22941.json.gz"
    template_path = LAYER / "fixed_point_feasibility_template.json.gz"
    release_path = LAYER / "main_point_release_template.json"
    packet, contract, full_columns, template, release = map(
        read, (packet_path, contract_path, full_columns_path, template_path, release_path))
    old_columns, hist, xcolumns, _ = descriptor_inputs()
    assert packet["schema"] == "early-shared-X-joint-symbolic-append/v1"
    assert packet["old_columns"] == 21021 and packet["total_columns"] == 22941
    assert packet["base_contract"] == contract == template["base_contract"]
    assert len(full_columns) == 22941 and full_columns[21021:] == packet["new_columns"]
    assert len(packet["new_columns"]) == 1920
    assert packet["all_new_columns_nonnegative"] is True
    assert packet["optimizer_calls"] == 0 and packet["fixed_point_values_loaded"] is False
    assert full_columns[:20601] == old_columns[:20601]
    for old, final in zip(old_columns[20601:], full_columns[20601:21021]):
        assert {key:final[key] for key in old} == old
        assert set(final) - set(old) == {"semantic_upgrade"}
        assert final["semantic_upgrade"]["canonical_min_permitted"] is False
    assert sha256(canonical(old_columns)).hexdigest() == contract["old_full_descriptors_sha256"]
    assert sha256(canonical(full_columns[:21021])).hexdigest() == contract["base_descriptors_sha256"]
    assert contract["base_matrix_sha256"] == "1b4a4e544e5b9eeea1fa64b3849a9d4cc532b997a5ad972ce33df81c224551e7"
    base_matrix = REPO / contract["base_matrix_path"]
    assert digest(base_matrix) == contract["base_matrix_sha256"]
    assert contract["base_rows"] == 23676 and contract["base_columns"] == 21021
    assert contract["base_nonzeros"] == 3313758 and contract["all_base_columns_nonnegative"] is True
    assert contract["K_column"] == 0
    assert set(contract["zero_histograms_retained"]) == {1,59,366,449,524,574}
    for source in range(1, 7):
        actual_income = {h:direct_share(int(record["actual_bits"][source-1]),
                                       sum(map(int,record["actual_bits"]))-int(record["actual_bits"][source-1]))
                         for h,record in hist.items()}
        assert contract["actual_income_rows"][str(source)] == sparse(actual_income)
    assert contract["F_X_row"] == sparse({xcolumns[h]:F(1,sum(map(int,record["actual_bits"][:4]))+1)
                                         for h,record in hist.items()})
    assert contract["existing_normalization"] == {"row":[[h,"1"] for h in hist],"rhs":"1"}
    for record in contract["histograms"]:
        h = record["hist_column"]
        descriptor = hist[h]
        a = tuple(map(int,descriptor["actual_bits"]))
        words = tuple(word for word,count in zip(product((0,1),repeat=3),descriptor["hist"])
                      for _ in range(count))
        assert record["actual_bits"] == descriptor["actual_bits"]
        assert record["d"] == descriptor["d"] and record["hist"] == descriptor["hist"]
        assert record["X_column"] == xcolumns[h]
        assert record["P"] == sum(a[:4]) and record["actual_total_load"] == sum(a)
        assert record["actual_backgrounds"] == [sum(a[:j]) for j in range(6)]
        assert record["literal_words"] == [list(word) for word in words]
        assert record["indexed_membership_counts"] == {
            kind:sum(word[slot] for word in words) for slot,kind in enumerate(("T","B","C"))}

    # Independently generated complete column order, including zero histograms.
    for state, descriptor in zip(expected["columns"], packet["new_columns"]):
        assert descriptor["kind"] == "early-common-X-hidden-tail"
        source = state["source"]
        assert descriptor["source_player"] == source
        assert descriptor["remaining_players"] == 7-source
        assert descriptor["hist_column"] == state["hist"]
        assert descriptor["X_column"] == xcolumns[state["hist"]]
        assert descriptor["X_bit"] == state["x"]
        assert descriptor["middle_bits"] == list(state["ys"])
        assert descriptor["terminal_bit"] == state["t"]
        assert descriptor["tail_bits"] == list(state["ys"])+[state["t"]]
        assert state["column"] == 21021+packet["new_columns"].index(descriptor)

    def query_name(query, source):
        kind = query["kind"]
        if kind == "X":
            return ("X",0)
        if kind == "actual":
            assert 1 <= query["player"] <= 6
            return ("A",query["player"]-1)
        if kind == "indexed-average":
            family = query["family"]
            assert family in ("T","B","C")
            assert query["members"] == [f"{family}{j}" for j in range(1,7)]
            assert query["weights"] == ["1/6"]*6 and query["not_a_pure_action"] is True
            return ("indexed",("T","B","C").index(family))
        assert kind == "new-tail"
        assert query["source_player"] == source
        m = 5-source
        position = query["tail_index"]
        assert 0 <= position <= m
        assert query["player"] == source+position+1
        assert query["name"] == (f"Y{position+1}_at_source{source}" if position<m else f"T_at_source{source}")
        return ("Y",position) if position<m else ("Tnew",0)

    branches = {branch["source_player"]:branch for branch in packet["branches"]}
    assert set(branches) == {1,2,3,4}
    for source,branch in branches.items():
        m = 5-source
        oldprefix = [f"A{j}" for j in range(1,source)]
        middle_names = [f"Y{k}_at_source{source}" for k in range(1,m+1)]
        assert branch["source_history"] == oldprefix
        assert branch["forced_X_history"] == oldprefix+["X"]
        assert branch["terminal_history"] == oldprefix+["X"]+middle_names
        assert branch["last_two_prefix"] == oldprefix+["X"]+middle_names[:-1]
        assert len(branch["terminal_history"]) == 5 and len(branch["last_two_prefix"]) == 4
        assert branch["hidden_columns"] == 16*2**(m+2)
        assert [query_name(query,source) for query in branch["ordered_tail_labels"]] == (
            [("Y",position) for position in range(m)]+[("Tnew",0)])

    expected_by_name = {canonical(row["name"]):row for row in expected["rows"]}
    assert len(expected_by_name) == 436
    raw = packet["raw_inequality_provenance"]
    unique = packet["inequalities"]
    mapping = packet["raw_to_unique_inequality"]
    assert len(raw) == len(mapping) == 436 and len(unique) == 436
    assert [row["id"] for row in unique] == list(range(436))
    independent_to_packet = {}
    family_counts, provenance_checks = Counter(), Counter()
    for raw_id, provenance in enumerate(raw):
        assert provenance["raw_id"] == raw_id
        source, family = provenance["branch_source_player"], provenance["family"]
        assert source in branches
        evidence = provenance["provenance"]
        if family == "source-IC":
            name = ["source_IC",source]
            assert evidence["history"] == branches[source]["source_history"]
            assert evidence["frozen_actual_tail"] is False and evidence["forced_label"] == "X"
        elif family == "actual-source-SAFE":
            query = query_name(provenance["query"],source)
            actual_source = provenance["actual_source_player"]
            name = ["actual_SAFE",source,query,actual_source]
            assert evidence["history"] == [f"A{j}" for j in range(1,actual_source)]
            assert evidence["frozen_forced_X_tail"] is False
            assert evidence["actual_terminal_IC_when_j6"] == (actual_source == 6)
        elif family in ("same-P-MAX","catalog-capacity","actual-MX-cap"):
            normalized = {"same-P-MAX":"MAX","catalog-capacity":"capacity","actual-MX-cap":"actual_cap"}[family]
            name = [normalized,source,query_name(provenance["query"],source)]
            if family != "catalog-capacity":
                assert evidence["history"] == ["A1","A2","A3","A4"]
            if family == "actual-MX-cap":
                assert evidence["not_a_forced_branch_income"] is True
                assert evidence["maximum_background"] == "actual first-four P"
        elif family == "branch-terminal-BR":
            name = ["terminal_BR",source,query_name(provenance["query"],source)]
            assert evidence["history"] == branches[source]["terminal_history"]
            assert evidence["uses_actual_u6"] is False
            assert evidence["average_is_literal_query_average"] == (provenance["query"]["kind"]=="indexed-average")
        elif family == "branch-true-PAIR":
            left = query_name(provenance["query_left"],source)
            right = query_name(provenance["query_right"],source)
            mode = provenance["mode"]
            if mode == "X,X":
                assert left == right == ("X",0)
                name = ["TP",source,"X","X"]
            elif mode == "Q,X":
                assert right == ("X",0)
                name = ["TP",source,left,"X"]
            else:
                assert mode == "Q,Q" and left == right
                name = ["TP",source,left,"diagonal"]
            assert evidence["history"] == branches[source]["last_two_prefix"]
            assert evidence["uses_actual_u5_or_u6"] is False
            assert evidence["diagonal_average_is_q_not_q_squared"] is True
            assert evidence["last_payment_pointwise_nonnegative"] == "z*(1-j_Q)/(d*(d+1))"
        else:
            assert family == "actual-RC"
            left = query_name(provenance["query_left"],source)
            right = query_name(provenance["query_right"],source)
            same = provenance["pair_class"] == "new-tail-unordered"
            name = ["RC_same_branch" if same else "RC_known_query",source,left,right]
            assert evidence["history"] == ["A1","A2","A3","A4"]
            assert evidence["cross_branch_unknown_intersections"] is False
            assert evidence["not_a_branch_PAIR_wallet"] is True
            assert evidence["maximum_background"] == "actual first-four P"
        key = canonical(name)
        assert key in expected_by_name, name
        expected_row = expected_by_name[key]
        unique_id = mapping[raw_id]
        assert unique_id == provenance["unique_row_id"]
        actual_row = unique[unique_id]
        assert actual_row["row"] == expected_row["row"], (name, "coefficient mismatch")
        assert actual_row["rhs"] == "0" and actual_row["sense"] == ">="
        assert raw_id in actual_row["provenance_raw_row_ids"]
        assert key not in independent_to_packet
        independent_to_packet[key] = unique_id
        family_counts[expected_row["family"]] += 1
        provenance_checks[family] += 1
    assert set(independent_to_packet) == set(expected_by_name)
    assert dict(family_counts) == expected["summary"]["row_families"]
    vectors = Counter(canonical(row["row"]) for row in unique)
    assert vectors == Counter(canonical(row["row"]) for row in expected["rows"])
    assert max(vectors.values()) == 1
    for unique_id,row in enumerate(unique):
        assert row["provenance_raw_row_ids"] == [raw_id for raw_id,target in enumerate(mapping) if target==unique_id]

    assert len(packet["equalities"]) == 128
    for actual, independent in zip(packet["equalities"], expected["equalities"]):
        assert actual["row"] == independent["row"]
        assert actual["rhs"] == "0" and actual["sense"] == "="
        assert actual["name"][1:] == independent["name"][1:]
        source,h,x = actual["name"][1:]
        assert actual["provenance"]["source_player"] == source
        assert actual["provenance"]["hist_column"] == h
        assert actual["provenance"]["X_bit"] == x
        assert actual["provenance"]["shared_X_column"] == xcolumns[h]
    assert sum(len(row["row"]) for row in unique) == 163957
    assert sum(len(row["row"]) for row in packet["equalities"]) == 2112

    # The fixed-point template is checked symbolically, without filling it.
    assert template["schema"] == "early-shared-X-fixed-point-template/v1"
    assert template["status"] == "UNFILLED_AWAIT_MAIN_NEXT_23676_EXACT_POINT"
    assert template["hidden_columns"] == packet["new_columns"]
    assert template["hidden_column_count"] == 1920
    assert template["hidden_lower_bounds"] == ["0"]*1920
    assert template["objective"] is None and template["optimizer_authorization"] is False
    assert template["point_binding"]["old_vector"] is None
    assert template["point_binding"]["main_release_reference"] is None
    assert template["point_binding"]["exact_point_sha256"] is None
    assert len(template["rows"]) == 564
    for fixed,row in zip(template["rows"], unique+packet["equalities"]):
        expected_hidden = [[column-21021,value] for column,value in row["row"] if column>=21021]
        expected_rhs = [[column,str(-F(value))] for column,value in row["row"] if column<21021]
        assert fixed["hidden_coefficients"] == expected_hidden
        assert fixed["rhs_old_linear_form"] == expected_rhs
        assert fixed["rhs_constant"] == "0"
        assert fixed["id"] == row["id"] and fixed["sense"] == row["sense"]
    assert release["old_vector"] is None and release["exact_point_sha256"] is None
    assert release["main_release_reference"] is None and release["required_old_vector_length"] == 21021
    assert release["no_point_is_authorized_or_loaded"] is True

    files = [packet_path,contract_path,full_columns_path,template_path,release_path]
    return {"status":"PASS", "matched_raw_rows":436, "matched_unique_rows":436,
            "matched_mass_equalities":128, "matched_hidden_columns":1920,
            "checked_inequality_nonzero_coefficients":163957,
            "checked_equality_nonzero_coefficients":2112,
            "exact_row_vector_multiset_equal":True,
            "all_raw_rows_have_correct_source_provenance":True,
            "all_old_column_descriptors_preserved":True,
            "base_matrix_bytes_unchanged_at_pinned_SHA":True,
            "template_rows_split_symbolically":564,
            "template_is_unfilled_no_point_loaded":True,
            "indexed_queries_never_read_as_pure_fractional_actions":True,
            "families":dict(family_counts), "source_provenance_counts":dict(provenance_checks),
            "audited_inputs":[{"path":str(path.relative_to(REPO)),"sha256":digest(path)} for path in files],
            "optimizer_calls":0}


if __name__ == "__main__":
    expected = independent_expected_layer()
    result = {"universal_budget_audit": universal_budget_audit(),
              "independent_expected_layer":expected["summary"],
              "matrix_audit":audit_packet(expected)}
    (HERE / "independent_verification.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
