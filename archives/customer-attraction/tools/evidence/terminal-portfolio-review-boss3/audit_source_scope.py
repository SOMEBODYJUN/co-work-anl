"""Static source/report scope and expression identity, no audit rerun/import."""
from pathlib import Path
import ast
import hashlib
import json

HERE=Path(__file__).resolve().parent


def main():
    code=HERE/'original/47bc029a1cfc7f55f5d5/review_terminal_portfolio.py'
    author=HERE/'related/terminal_portfolio_cuts.py'
    report=json.loads((HERE/'original/f98a6bd9fd91fe44896e/review_terminal_portfolio.json').read_text())
    tree=ast.parse(code.read_text());at=ast.parse(author.read_text())
    params=next(x for x in tree.body if isinstance(x,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='params' for t in x.targets))
    qs=next(x for x in tree.body if isinstance(x,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='qs' for t in x.targets))
    assert isinstance(params.value,ast.List) and len(params.value.elts)==3
    assert isinstance(qs.value,ast.BinOp) and isinstance(qs.value.left,ast.List)
    onehot_indices=ast.literal_eval(qs.value.right.generators[0].iter)
    assert onehot_indices==(0,5,7,11,12)
    query_patterns=len(qs.value.left.elts)+len(onehot_indices)
    assert query_patterns==8
    p_loop=next(n for n in ast.walk(tree) if isinstance(n,ast.For) and isinstance(n.target,ast.Name) and n.target.id=='p')
    ell_loop=next(n for n in ast.walk(tree) if isinstance(n,ast.For) and isinstance(n.target,ast.Name) and n.target.id=='ell')
    assert ast.unparse(p_loop.iter)=='range(6 - n)' and ast.unparse(ell_loop.iter)=='range(p, 6)'
    compressed=next(n.value for n in ast.walk(tree) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='compressed' for t in n.targets))
    psi=next(n for n in at.body if isinstance(n,ast.FunctionDef) and n.name=='psi')
    author_return=next(n.value for n in psi.body if isinstance(n,ast.Return))
    same=ast.dump(compressed,include_attributes=False)==ast.dump(author_return,include_attributes=False)
    assert same
    counts=[]
    for n in range(1,6):
        pairs=sum(6-p for p in range(6-n))
        minima=pairs*2*query_patterns*len(params.value.elts)
        identities=minima*2**n
        actual_pairs=(6-n)*(n+1)
        counts.append(dict(n_followers=n,source_actual=6-n,p_values=list(range(6-n)),
            checked_p_ell_pairs=pairs,actual_prefix_compatible_p_ell_pairs=actual_pairs,
            extra_checked_p_ell_pairs=pairs-actual_pairs,minimum_checks=minima,identity_checks=identities))
    assert sum(c['minimum_checks'] for c in counts)==report['exact_minimum_checks']==3360
    assert sum(c['identity_checks'] for c in counts)==report['exact_identity_checks']==28800
    imports=[]
    for n in tree.body:
        if isinstance(n,ast.Import):imports.extend(x.name for x in n.names)
        if isinstance(n,ast.ImportFrom):imports.append(n.module)
    assert set(imports)=={'fractions','itertools','json','pathlib'}
    source_calls=[n.func.attr for n in ast.walk(tree) if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute)]
    assert 'write_text' in source_calls and not {'read_text','read_bytes'}&set(source_calls)
    assert [n.name for n in tree.body if isinstance(n,ast.FunctionDef)]==['share']
    assert not any(isinstance(n,ast.If) for n in tree.body)
    out=dict(scope='AST reading and integer loop-count derivation only; not a second mathematical audit run',
        historical_audit_sha256=hashlib.sha256(code.read_bytes()).hexdigest(),
        frozen_report_sha256=hashlib.sha256((HERE/'original/f98a6bd9fd91fe44896e/review_terminal_portfolio.json').read_bytes()).hexdigest(),
        current_author_comparison_sha256=hashlib.sha256(author.read_bytes()).hexdigest(),
        compressed_minimum_expression_AST_equal_to_current_author_psi=True,
        minimum_expression=ast.unparse(compressed),standard_library_imports=imports,
        author_code_import_or_execution_in_historical_audit=False,
        author_version_hash_binding_in_old_report=False,
        historical_audit_reads_any_input_file=False,
        top_level_execution_on_import=True,query_vector_length=13,parameter_patterns=3,query_bit_patterns=8,
        parameters_source=ast.unparse(params.value),query_patterns_source=ast.unparse(qs.value),
        counts_by_followers=counts,total_checked_p_ell_pairs=sum(c['checked_p_ell_pairs'] for c in counts),
        total_actual_prefix_compatible_p_ell_pairs=sum(c['actual_prefix_compatible_p_ell_pairs'] for c in counts),
        exact_minimum_checks=3360,exact_identity_checks=28800,
        not_executed_or_tested=['author qvec or row','16-query third-index averages','orbit count and K-column readout','1905 vectors','5083/5112 whole graph','SPE or exact LP optimum'],
        source_program_execution_count_for_this_static_check=0)
    print(json.dumps(out,ensure_ascii=False,indent=2))


if __name__=='__main__':
    main()
