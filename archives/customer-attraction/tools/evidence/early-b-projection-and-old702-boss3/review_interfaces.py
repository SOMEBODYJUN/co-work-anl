"""Read-only AST and pure-function interface check; no historical main or LP.

Invoke with an optional repository root when this package is in external stage.
The 702-row count is the existing shared old_system contract, not a new replay.
"""
from pathlib import Path
from fractions import Fraction
import ast
import hashlib
import json
import sys

HERE = Path(__file__).resolve().parent
REPO = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else HERE.parents[4]


def main():
    family_path = HERE / "original/bb302c2f87c0e23a435a/old702_plus_B_families.py"
    combine_path = HERE / "original/6810944411e73238bda4/combine_old702.py"
    dependency = HERE / "related/max_branch_lp.py"
    family = ast.parse(family_path.read_text())
    solve = next(n for n in family.body if isinstance(n, ast.FunctionDef) and n.name == "solve")
    sources = ast.literal_eval(solve.args.defaults[0])
    assert sources == (0, 1, 2, 3)
    tree = ast.parse(dependency.read_text())
    pure = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name in {"qf", "menus", "branch_rows"}]
    assert len(pure) == 3
    ns = {"F": Fraction}
    exec(compile(ast.Module(body=pure, type_ignores=[]), str(dependency), "exec"), ns)
    families = []
    for source in sources:
        hidden_count = 5-source
        names, vals = ns["branch_rows"]((0,)*7, (source,5), (1,)*hidden_count, 0, 0)
        expected = 3+15*hidden_count+hidden_count**2
        cap_positions = [i for i,name in enumerate(names) if name.startswith("CAP:")]
        assert len(names) == len(vals) == expected and len(cap_positions) == hidden_count
        assert all(vals[i] == -1 for i in cap_positions)
        families.append(dict(actual_source=source+1, hidden_bits=hidden_count,
            endpoint_states=2**hidden_count*2, inequality_rows=len(names),
            common_K_capacity_rows=len(cap_positions)))
    nt = 64*7
    lift_rows = 702+sum(f["inequality_rows"] for f in families)
    equalities = 1+nt*len(families)
    variables = nt+1+nt*sum(f["endpoint_states"] for f in families)
    assert (lift_rows,equalities,variables) == (978,1793,54209)
    combine = ast.parse(combine_path.read_text())
    imported = [(n.module,[a.name for a in n.names]) for n in combine.body if isinstance(n,ast.ImportFrom)]
    assert ("tail3_B_projection",["table"]) in imported
    old_path = REPO / "archives/customer-attraction/tools/evidence/combined-branch-master-program/dependencies/research/workspaces/customer-attraction/R-c4f1ef099fad483c9f81283b61eb0b53/six_astra/new_reply_budget.py"
    old_tree = ast.parse(old_path.read_text())
    old_fn = next(n for n in old_tree.body if isinstance(n,ast.FunctionDef) and n.name == "old_system")
    assert any(isinstance(n,ast.Assert) and "702" in ast.unparse(n.test) for n in ast.walk(old_fn))
    report = dict(scope="default shape and CAP coefficient interface only; old generators and floating LPs not run",
        combine_old702=dict(inequality_rows=703,variables=449,new_row="old no-K actual-fourth psi / 204", normalization="comparison union = 1"),
        lifted_default=dict(inequality_rows=lift_rows,equality_rows=equalities,variables=variables,families=families),
        branch_functions_extracted_via_AST=["qf","menus","branch_rows"],representative_branch_calls=4,
        historical_main_executions=0,floating_LP_executions=0,
        original_hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (family_path,combine_path,dependency)},
        unsafe_custom_source_boundary="Zero-based source 4 makes the forced penultimate player the menu optimizer; the default 0..3 avoids that unsupported inference.")
    print(json.dumps(report,ensure_ascii=False,indent=2))


if __name__ == "__main__":
    main()
