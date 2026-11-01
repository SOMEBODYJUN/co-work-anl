"""Exact reconstruction of three frozen cut packs on their named input points.

The independent path enumerates literal ordered indices and literal successor
bits. A second path extracts only the frozen pure row functions with AST; it
does not import their discovery modules, execute a CLI, or call an optimizer.
The old points are inputs for these rows, not newly verified complete matrices.
"""
from collections import Counter, defaultdict
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
from pathlib import Path
from types import SimpleNamespace
import ast
import hashlib
import json
import platform
import time

HERE = Path(__file__).resolve().parent
BASE = Path("research/workspaces/customer-attraction/R-5662d5cb0e5845a980ed10a3b3224cb1")
R3 = HERE / "original" / BASE / "research_3"
R5 = HERE / "original" / BASE / "research_5"
WORDS = tuple(product((0, 1), repeat=3))
ORBITS = ((0, 0), (1, 0), (1, 1))


def pay(numerator, denominator):
    return F(numerator, denominator) if numerator else F(0)


def extract(path, names, env):
    tree = ast.parse(path.read_text())
    nodes = [node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name in names]
    assert {node.name for node in nodes} == set(names)
    exec(compile(ast.Module(body=nodes, type_ignores=[]), str(path), "exec"), env)
    return env


def original_rows():
    common = {"F": F, "product": product, "lru_cache": lru_cache}
    oqenv = extract(R3 / "old_query_reply_cuts.py", {"groups"}, {**common, "PAT": WORDS, "GS": ORBITS})
    oq = SimpleNamespace(PAT=WORDS, GS=ORBITS, groups=oqenv["groups"])
    pcenv = extract(R3 / "terminal_portfolio_cuts.py", {"qvec", "share", "psi", "row"}, {**common, "oq": oq, "PAT": WORDS})
    pc = SimpleNamespace(qvec=pcenv["qvec"])
    rqenv = extract(R3 / "early_reply_requery_cuts.py", {"share", "candidates", "psi", "row"}, {**common, "oq": oq, "pc": pc})
    return {"portfolio": pcenv["row"], "requery": rqenv["row"]}


def literal_queries(actual, indexed_words, left, right, forced):
    others = [j for j in range(6) if j not in {left, right}]
    assert len(others) in (4, 5)
    return (tuple(actual) + indexed_words[left] + indexed_words[right] + (forced,)
            + tuple(sum(F(indexed_words[j][q]) for j in others) / len(others) for q in range(3)))


@lru_cache(None)
def portfolio_min(i, prefix, actual_last_load, forced, queries, prices, weights):
    am, al, bm, bl = prices
    total_query_weight = sum(weights)
    quoted = sum(weight * query for weight, query in zip(weights, queries))
    candidates = []
    for successors in product((0, 1), repeat=5-i):
        last = successors[-1]
        middle = sum(successors[:-1])
        total = prefix + forced + sum(successors)
        value = (pay(forced, total) - total_query_weight * pay(last, total)
                 + F(am * middle + al * last, actual_last_load + 1)
                 + bm * middle + bl * last
                 + F(quoted, prefix + forced + middle + 1))
        candidates.append(value)
    return min(candidates)


@lru_cache(None)
def requery_min(i, prefix, actual_last_load, forced, query, parameters):
    a, cross, jprice, vprice, capacity, mu = parameters
    candidates = []
    successor_count = 5 - i
    for first in product((0, 1), repeat=successor_count):
        b, c = first[-2:]
        z1 = prefix + forced + sum(first)
        for second in product((0, 1), repeat=successor_count):
            j, v = second[-2:]
            z2 = prefix + c + sum(second)
            # Seven literal IC/price/capacity rows, with the same first-branch
            # terminal C also used as the second branch's forced topic.
            value = (a * pay(forced, z1) - mu * pay(c, z1)
                     + (1-a) * pay(c, z2) - cross * pay(v, z2)
                     + cross * F(b, prefix+c+sum(second[:-1])+1)
                     + F(jprice*j + vprice*v, actual_last_load+1)
                     + capacity*v + F(mu*query, prefix+forced+sum(first[:-1])+1))
            candidates.append(value)
    return min(candidates)


def validate_cut(kind, cut):
    assert cut["i"] in range(4 if kind == "requery" else 5)
    assert cut["member"] in (0, 1) and tuple(cut["orb"]) in ORBITS
    if kind == "portfolio":
        prices = tuple(F(cut.get(key, "0")) for key in ("alpha_middle", "alpha_last", "beta_middle", "beta_last"))
        weights = tuple(map(F, cut["mu"]))
        assert len(weights) in (13, 16) and min(prices + weights) >= 0
        return prices, weights
    parameters = tuple(map(F, cut["parameters"]))
    assert len(parameters) == 6 and 0 <= parameters[0] <= 1 and min(parameters[1:]) >= 0
    assert cut["query"] in range(16)
    return parameters


def independent_row(columns, kind, cut):
    decoded = validate_cut(kind, cut)
    i = cut["i"]
    family, diagonal = cut["orb"]
    member = cut["member"]
    row = [F(0)] * len(columns)
    assert columns[0]["kind"] == "K"
    if kind == "portfolio":
        prices, weights = decoded
        am, al, bm, bl = prices
        row[0] = (4-i) * bm + bl
        last_budget = (4-i) * am + al
    else:
        parameters = decoded
        row[0] = parameters[4]
        last_budget = parameters[2] + parameters[3]
    blocks = []
    current = None
    for index, column in enumerate(columns):
        if column["kind"] == "hist":
            current = {"index": index, "data": column, "joint": []}
            blocks.append(current)
        elif column["kind"] == "joint-reply":
            assert current is not None
            current["joint"].append((index, column))
    assert len(blocks) == 16
    old_hist_ids = set()
    for block in blocks:
        column = block["data"]
        actual = tuple(map(int, column["actual_bits"]))
        assert len(actual) == 6 and set(actual) <= {0, 1}
        histogram = column["hist"]
        assert len(histogram) == 8 and sum(histogram) == 6 and all(isinstance(x, int) and x >= 0 for x in histogram)
        words = tuple(word for word, count in zip(WORDS, histogram) for _ in range(count))
        assert sum(word[0] for word in words) == column["d"]
        old_ids = {entry["hist_column_old"] for _, entry in block["joint"]}
        assert len(old_ids) == 1 and not old_ids & old_hist_ids
        old_hist_ids |= old_ids
        pairs = [(a, b) for a in range(6) for b in range(6) if (a == b) == bool(diagonal)]
        ct = len(pairs)
        assert ct == (6 if diagonal else 30)
        differences = defaultdict(F)
        groups = Counter()
        baseline = F(0)
        for left, right in pairs:
            values = []
            for forced in (0, 1):
                queries = literal_queries(actual, words, left, right, forced)
                if kind == "portfolio":
                    value = portfolio_min(i, sum(actual[:i]), sum(actual[:5]), forced, queries, prices, weights)
                else:
                    value = requery_min(i, sum(actual[:i]), sum(actual[:5]), forced, queries[cut["query"]], parameters)
                values.append(value)
            group = (family, diagonal, words[left], words[right])
            groups[group] += 1
            baseline += values[0] / ct
            differences[group] += (values[1]-values[0]) / ct
        row[block["index"]] = pay(actual[i], sum(actual)) + last_budget * pay(actual[5], sum(actual)) - baseline
        for index, entry in block["joint"]:
            ff, dd, wi, wj = entry["group"]
            if (ff, dd) != (family, diagonal):
                continue
            group = (ff, dd, tuple(wi), tuple(wj))
            assert group in groups
            assert entry["state"] in ([0, 1], [1, 0], [1, 1])
            if entry["state"][member]:
                row[index] = -differences[group]
    return row


def row_hash(row):
    return hashlib.sha256(json.dumps(list(map(str, row)), separators=(",", ":")).encode()).hexdigest()


def main():
    start = time.time()
    manifest = json.loads((HERE / "source-manifest.json").read_text())
    for entry in manifest:
        assert hashlib.sha256((HERE / entry["evidence_path"]).read_bytes()).hexdigest() == entry["sha256"]
    original = original_rows()
    packs = [
        ("early_reply_requery_master_all_queries.json", "selected", "requery"),
        ("capacity_master_price_cuts.json", "selected", "portfolio"),
        ("coupled_pending_cuts.json", "portfolio", "portfolio"),
        ("coupled_pending_cuts.json", "requery", "requery"),
    ]
    reports = []
    coordinates = 0
    sparse_rows = []
    for filename, field, kind in packs:
        pack = json.loads((R3 / filename).read_text())
        point_path = HERE / "original" / pack["source"]
        raw_point = point_path.read_bytes()
        point = json.loads(raw_point)
        columns = point["columns"]
        weights = [F(column["weight"]) for column in columns]
        assert min(weights) >= 0
        if "source_sha256" in pack:
            assert hashlib.sha256(raw_point).hexdigest() == pack["source_sha256"]
            assert F(point["W"]) == F(pack["source_W"])
        if "LPs" in pack:
            assert pack["LPs"] == 4*2*3*16 == 384
            assert pack["parameter_bounds"] == "a in [0,1], other five in [0,1000]"
        values = []
        hashes = defaultdict(list)
        for number, item in enumerate(pack[field]):
            cut = item["cut"]
            row = independent_row(columns, kind, cut)
            author_row = original[kind](columns, cut)
            assert row == author_row, (filename, field, number)
            coordinates += len(row)
            slack = sum(coefficient * weight for coefficient, weight in zip(row, weights))
            assert slack == F(item["slack"]) < 0, (filename, field, number, slack, item["slack"])
            if kind == "portfolio" and len(cut["mu"]) == 13:
                extended = dict(cut, mu=cut["mu"] + ["0", "0", "0"])
                assert row == original[kind](columns, extended)
            fingerprint = row_hash(row)
            hashes[fingerprint].append(number+1)
            values.append({"number": number+1, "cut": cut, "slack": str(slack), "row_sha256": fingerprint,
                           "nonzero_coefficients": sum(value != 0 for value in row)})
            sparse_rows.append({"pack": filename, "field": field, "number": number+1, "length": len(row),
                                "row_sha256": fingerprint, "nonzero": [[index, str(value)] for index, value in enumerate(row) if value]})
        reports.append({"pack": filename, "field": field, "kind": kind, "scope": pack["scope"],
                        "source": pack["source"], "point_sha256": hashlib.sha256(raw_point).hexdigest(),
                        "point_columns": len(columns), "point_W": point["W"], "saved_matrix_rows": point["verified_rows"],
                        "records": len(values), "distinct_rows_on_this_coordinate_domain": len(hashes),
                        "duplicate_record_groups": [group for group in hashes.values() if len(group)>1],
                        "all_saved_negative_slacks_equal": True, "rows": values})
    assert sum(report["records"] for report in reports) == 27
    assert coordinates == 52075
    result = {"status": "passed", "python": platform.python_version(), "seconds": time.time()-start,
              "record_count": 27, "coordinate_comparisons": coordinates, "original_pure_row_calls": 27,
              "additional_zero_extension_row_calls": 11, "original_CLI_calls": 0, "discovery_LP_calls": 0,
              "whole_saved_matrix_replays": 0, "portfolio_cache": str(portfolio_min.cache_info()),
              "requery_cache": str(requery_min.cache_info()), "reports": reports}
    out = HERE / "runs"
    out.mkdir(exist_ok=True)
    (out / "all-sparse-row-coefficients.json").write_text(json.dumps(sparse_rows, ensure_ascii=False, indent=2) + "\n")
    (out / "exact-cut-audit.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({key: value for key, value in result.items() if key != "reports"}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
