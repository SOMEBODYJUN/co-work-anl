#!/usr/bin/env python3
"""Static byte, scalar, report and table reconciliation; no finite-domain audit.

This script never imports or executes any preserved mathematical implementation.
It does not enumerate COPY/binary/full-pricing types or recompute primal columns.
"""
from pathlib import Path
from fractions import Fraction as F
from argparse import ArgumentParser
import hashlib,json,re

HERE=Path(__file__).resolve().parent

def sha(b):
    return hashlib.sha256(b).hexdigest()

def main():
    parser=ArgumentParser(description=__doc__)
    parser.add_argument('--repo')
    parser.add_argument('--output',default=str(HERE/'reconciliation.json'))
    args=parser.parse_args()
    manifest=json.loads((HERE/'manifest.json').read_text())
    if args.repo:
        repo=Path(args.repo).resolve()
    else:
        repo=next(p for p in HERE.parents if all((p/d['archive_path']).is_file() for d in manifest['reused_dependencies']))
    fingerprints=[]
    bypath={}
    for item in manifest['sources']:
        p=HERE/item['package_path']; data=p.read_bytes()
        assert len(data)==item['size'] and sha(data)==item['sha256'],item['id']
        fingerprints.append(dict(id=item['id'],bytes=len(data),sha256=sha(data)))
        bypath[item['path']]=p
    assert len(fingerprints)==10 and sum(x['bytes'] for x in fingerprints)==55902
    cert=json.loads((HERE/'original/dual/exact_shared_root.json').read_text())
    L={k:int(v) for k,v in cert['integer_multipliers'].items()}
    B,D=int(cert['beta_numerator']),int(cert['common_denominator'])
    assert len(L)==61 and min(L.values())>0
    assert list(L)==list(cert['multipliers'])
    for n,l in L.items():
        assert F(l,D)==F(cert['multipliers'][n]),n
    beta=F(cert['dual_beta'])
    assert F(B,D)==beta and F(2)<beta<F(5043,2500)
    coefficient=lambda n: 1 if n.startswith('MAX:fixed:') else 78 if n.startswith('KRS:fixed:') else -88940 if n=='KCAP:4' else 0
    kres=-sum(l*coefficient(n) for n,l in L.items())
    assert kres==0==int(cert['K_dual_residual'])
    assert cert['minimum_scaled_integer_residual']=='0' and cert['full_pricing_nonnegative'] is True
    assert cert['negative_columns']==[] and cert['generated_columns']==2753
    first=json.loads((HERE/'original/dual/separate_shared_root_audit.json').read_text())
    second=json.loads((HERE/'original/countersearch/separate_shared_root_audit.json').read_text())
    differences=[k for k in first if first[k]!=second[k]]
    assert first.keys()==second.keys() and differences==['seconds']
    for report in (first,second):
        assert report['source_sha256']==sha((HERE/'original/dual/exact_shared_root.json').read_bytes())
        assert F(report['beta'])==beta and report['all_cases_nonnegative'] is True
        assert report['negative_cases']==[] and report['minimum_scaled_integer_residual']=='0'
        assert report['K_dual_residual']=='0' and report['K_dual_nonnegative'] is True
        assert report['conditional_cases']==6144 and report['zero_conditional_cases']==43
        assert report['positive_multipliers']==61 and report['score_contexts']==160
        assert report['fixed_masks']==1024 and report['shared_optimal_multiplicities']==6
        assert report['third_histograms']==792 and report['second_histograms']==15504
        assert report['menu_corners_per_family']==4 and report['uses_discovery_pricing_implementation'] is False
    math=json.loads((HERE/'original/countersearch/audit_shared_root_math.json').read_text())
    inputbindings=[]
    for item in manifest['reused_dependencies']:
        p=repo/item['archive_path'];data=p.read_bytes()
        assert len(data)==item['size'] and sha(data)==item['sha256']
        assert math['inputs_sha256'][item['frozen_path']]==sha(data)
        inputbindings.append(dict(path=item['archive_path'],bytes=len(data),sha256=sha(data)))
        if p.name=='root_shared_max_copy_cg.json':
            cg=json.loads(data)
            assert len(cg['atoms'])==2753
            assert len(cg['row_names'])==len(cg['K_column'])
            columns=dict(zip(cg['row_names'],cg['K_column']))
            for n in L:
                assert F(str(columns[n]))==coefficient(n),n
            assert cert['source_sha256']==sha(data)
    assert math['inputs_sha256'][cert_path:=next(p for p in bypath if p.endswith('/dual/exact_shared_root.json'))]==sha(bypath[cert_path].read_bytes())
    assert F(math['certificate_coefficients']['exact_beta'])==beta
    assert math['certificate_coefficients']['positive_multipliers']==61
    assert math['certificate_coefficients']['K_coefficient_residual']=='0'
    # Match the displayed complete integer table against the primary source.
    formal=HERE.parents[2]/'state/定理/五人共同最大主题的六十一行有理福利界--定理.md'
    table=dict(re.findall(r'^\| `([^`]+)` \| ([0-9]+) \|$',formal.read_text(),re.M))
    assert table==cert['integer_multipliers'] and len(table)==61
    receipt_path=HERE/'receipts.json'
    if receipt_path.exists():
        receipts=json.loads(receipt_path.read_text())
        assert {r['id'] for r in receipts}=={x['id'] for x in manifest['sources']}
        assert len(receipts)==10 and all(r['full_file_reviewed'] and r['related_material_checked'] and r['unique_content_accounted_for'] for r in receipts)
    # Check only this batch's formal/package prose, using the stage for new files
    # and the result repository for mature dependencies.
    package_root=HERE.parents[4]
    prose=[formal,formal.parent.parent/'审查/共同最大主题六十一行证书的原数学复核--审查.md',
           formal.parent.parent/'程序/共同最大主题证书恢复与两份定价报告--程序.md',HERE/'README.md']
    links=[]
    for prose_file in prose:
        for target in re.findall(r'\]\(([^)]+)\)',prose_file.read_text()):
            if '://' in target or target.startswith('#'):
                continue
            target=target.split('#',1)[0]
            local=(prose_file.parent/target).resolve()
            if not local.is_file():
                published=repo/local.relative_to(package_root)
                assert published.is_file(),(str(prose_file),target)
            links.append(target)
    report=dict(action='static-byte-scalar-report-and-table-reconciliation-only',
        primary_fingerprints=fingerprints,reused_dependency_bindings=inputbindings,
        positive_integer_multipliers=61,all_rational_multipliers_equal_integer_over_D=True,
        beta_equals_B_over_D=True,beta_strictly_between_two_and_5043_over_2500=True,
        common_K_residual=str(kres),active_K_columns_equal_original_CG=True,
        separate_report_only_different_fields=differences,
        displayed_full_integer_table_matches_primary=True,
        formal_and_package_prose_local_links_checked=len(links),
        original_scientific_entrypoint_calls=0,
        finite_domain_enumerations=0,
        primal_or_generated_column_replays=0)
    Path(args.output).write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ('primary_fingerprints','reused_dependency_bindings')},indent=2))

if __name__=='__main__':
    main()
