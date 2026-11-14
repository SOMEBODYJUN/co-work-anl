"""Read-only Fraction audit of the 5112, 5277 and 5692 frozen CAG points.

Run with the repository path as the only optional argument. The script reads
frozen JSON and extracts only pure archived row-building functions. It does
not invoke a matrix build, original entry point, or optimizer.
"""
import ast
from collections import Counter
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
import json
from pathlib import Path
import sys
from types import SimpleNamespace


ROOT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
BASE = ROOT / 'archives/customer-attraction/tools/evidence'
DEP = (
    BASE / 'combined-branch-master-program/dependencies/research/workspaces'
    / 'customer-attraction/R-5662d5cb0e5845a980ed10a3b3224cb1'
)
POINTS = {
    5112: BASE / 'terminal-capacity-refinement-boss3/original/2ac41f3470c74caa54b1/terminal_capacity_refinement_exact.json',
    5277: BASE / 'coupled-latest-menu-check-boss3/original/coupled_latest_exact.json',
    5692: BASE / 'b-family-menu-prices-boss3/original/research_2/all_menu_prices_exact.json',
}
PAT = tuple(product(range(2), repeat=3))
GS = ((0, 0), (1, 0), (1, 1))


def load(path, names, **extra):
    tree = ast.parse(path.read_text())
    statements = [
        node for node in tree.body
        if isinstance(node, ast.FunctionDef) and node.name in names
        or isinstance(node, ast.Assign) and names.intersection(
            target.id for target in node.targets if isinstance(target, ast.Name)
        )
    ]
    ns = {'F': F, 'product': product, 'lru_cache': lru_cache, 'PAT': PAT, 'GS': GS, **extra}
    exec(compile(ast.Module(body=statements, type_ignores=[]), str(path), 'exec'), ns)
    return SimpleNamespace(**ns)


def read(path):
    return json.loads(path.read_text())


def share(numerator, denominator):
    return F(numerator, denominator) if numerator else F()


def family4_coefficient(a, hist, q, r):
    """12 source IC + 2 cross[4] + 2 cross[8] + 3 cross[9]."""
    p, b = sum(a[:3]), a[5]
    load = p + b
    mean_b = sum(F(count * wi[1], 6) for count, wi in zip(hist, PAT))
    old_c = sum(
        F(count, 6) * share(wi[2], p + sum(wi)) for count, wi in zip(hist, PAT)
    )
    floor_c = sum(
        F(count, 6 * (p + wi[0] + wi[1] + 1)) for count, wi in zip(hist, PAT)
    )
    return (
        12 * share(a[3], sum(a)) + 5 * old_c
        + share(-12 * b + 2 * r, load + q + r)
        - 2 * mean_b / (load + q + 1) - (2 * q + 3 * r) * floor_c
    )


def family3_envelope(histograms, capacity, branch, families):
    weights = (670, 9, 1, 4, 76, 32, 100, 105)
    total = weights[3] * capacity
    for col, mass in histograms:
        a = tuple(map(int, col['actual_bits']))
        h = col['hist']
        local = []
        for hidden, ell in product(product(range(2), repeat=3), (0, 6)):
            names, primitive = branch.branch_rows(a + (0,), (2, 5), hidden, col['d'], ell)
            assert names[:3] == ['IC', 'M', 'Z']
            cross = families.cross(a, h, hidden, 3)
            state = [
                *primitive[:3], primitive[names.index('CAP:hidden:3')],
                *(cross[i] for i in (8, 12, 13, 14)),
            ]
            local.append(sum(x * y for x, y in zip(weights, state)))
        total += mass * max(local)
    return total


def main():
    points = {n: read(path) for n, path in POINTS.items()}
    original = points[5112]['columns']
    assert len(original) == 1905
    oq = load(DEP / 'research_3/old_query_reply_cuts.py', {'groups'})
    pc = load(DEP / 'research_3/terminal_portfolio_cuts.py', {'qvec', 'share', 'psi', 'row'}, oq=oq)
    requery = load(
        DEP / 'research_3/early_reply_requery_cuts.py', {'share', 'candidates', 'psi', 'row'},
        oq=oq, pc=pc,
    )
    nested = load(
        DEP / 'research_5/nested_reply_projection.py', {'NAMES', 'NI', 'share', 'raw', 'coeff', 'row'},
    )
    share_source = load(
        BASE / 'combined-branch-master-program/dependencies/customer_attraction/priced_hidden_reply.py',
        {'_rational', '_inputs', '_share', 'projected_by_count'}, Fraction=F,
    )
    continuous = load(
        DEP / 'research_3/continuous_old_query_cuts.py', {'psi', 'row'},
        projected_by_count=share_source.projected_by_count, oq=oq,
    )
    tail = load(
        DEP / 'research_2/tail3_B_projection.py', {'safe', 'raw', 'coeff', 'table', 'WEIGHTS'},
    ).table()
    early_b = read(DEP / 'research_2/early_B_projection_certificate.json')['rows']
    early64 = read(DEP / 'research_3/continuous_old_query_cuts.json')['selected']
    local = read(DEP / 'research_5/joint_local_v2_cuts.json')
    coupled = BASE / 'b-family-menu-prices-boss3/replay/research_2'
    branch = load(coupled / 'max_branch_lp.py', {'qf', 'menus', 'branch_rows'})
    minimal = load(
        coupled / 'coupled_B_branch_master.py', {'cross_rows'}, share=share, nr=SimpleNamespace(PAT=PAT),
    )
    families = load(
        coupled / 'coupled_B_families_master.py', {'cross'}, share=share, nr=SimpleNamespace(PAT=PAT),
    )
    archived_slacks = read(BASE / 'coupled-latest-menu-check-boss3/replay/local-eighteen-slacks.json')
    for n, point in points.items():
        columns = point['columns'][:1905]
        assert [
            {key: value for key, value in col.items() if key != 'weight'} for col in columns
        ] == [{key: value for key, value in col.items() if key != 'weight'} for col in original]
        weights = [F(col['weight']) for col in columns]

        def dot(row):
            return sum(c * w for c, w in zip(row, weights))

        hists = [(col, w) for col, w in zip(columns, weights) if col['kind'] == 'hist']
        slacks64 = [dot(continuous.row(columns, entry['cut'])) for entry in early64]
        vals68 = slacks64 + [sum(w * tail[(c['actual_bits'], c['d'])] for c, w in hists)]
        for entry in early_b:
            table = {(cell['actual_bits'], cell['d']): F(cell['psi']) for cell in entry['table']}
            vals68.append(F(entry['kappa']) * weights[0] + sum(
                w * table[(c['actual_bits'], c['d'])] for c, w in hists
            ))
        print('early and tail extra:', *vals68[64:])
        assert len(vals68) == 68 and min(slacks64) > 0
        if n == 5112:
            assert [v > 0 for v in vals68[64:]] == [True, False, False, True]
        else:
            assert min(vals68) >= 0
        print(n, 'min of early 64 =', min(slacks64))
        local_values = {}
        for key, module in [('nested', nested), ('requery', requery), ('portfolio', pc)]:
            local_values[key] = [dot(module.row(columns, entry)) for entry in local[key]]
            print(n, key, Counter((v > 0) - (v < 0) for v in local_values[key]))
            for idx, value in enumerate(local_values[key], 1):
                print(idx, value)
        if n == 5277:
            for key, saved in zip(('nested', 'requery', 'portfolio'), archived_slacks.values()):
                assert local_values[key] == [F(item['slack']) for item in saved['rows']]

        total = F()
        for c, w in hists:
            a = tuple(map(int, c['actual_bits']))
            hist = c['hist']
            scores = []
            for q, r in product(range(2), repeat=2):
                expected = family4_coefficient(a, hist, q, r)
                cross = minimal.cross_rows(a, hist, q, r)
                assert cross == families.cross(a, hist, (q, r), 4)
                for ell in (0, 6):
                    names, values = branch.branch_rows(a + (0,), (3, 5), (q, r), c['d'], ell)
                    assert names[0] == 'IC'
                    assert expected == 12 * values[0] + 2 * cross[4] + 2 * cross[8] + 3 * cross[9]
                scores.append(expected)
            total += w * max(scores)
            if n == 5112 and w:
                print('Source 4 hist', c['actual_bits'], hist, 'mass', w, 'max', max(scores))
        print(n, 'source 4 common lift envelope =', total)
        if n == 5112:
            assert total == -F(
                245604769923895081791133830617787185909,
                74005516513845927910387062892579257793420,
            )

        source3 = family3_envelope(hists, weights[0], branch, families)
        print(n, 'source 3 lift envelope =', source3)
        if n == 5277:
            assert source3 == -F(
                1505595416077174278327675259267902161027078757,
                735576345002473658294053882445594433882234368,
            )
        elif n == 5692:
            assert source3 >= 0


if __name__ == '__main__':
    main()
