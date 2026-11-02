#!/usr/bin/env python3
"""Static preservation/output/table/link check; no mathematical kernels run.

This only reads saved source and output data. No utilities or equilibria are
recomputed, and no preserved source is imported.
"""
from pathlib import Path
from argparse import ArgumentParser
import gzip,hashlib,json,re

HERE=Path(__file__).resolve().parent

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    ap=ArgumentParser(description=__doc__);ap.add_argument('--repo',required=True);a=ap.parse_args();repo=Path(a.repo).resolve()
    m=json.loads((HERE/'manifest.json').read_text())
    assert len(m['sources'])==14 and sum(x['size'] for x in m['sources'])==274970
    for x in m['sources']:
        p=HERE/x['package_path'];assert p.stat().st_size==x['size'] and sha(p)==x['sha256'],x['id']
    for x in m['related']:
        p=HERE/x['package_path'];assert p.stat().st_size==x['size'] and sha(p)==x['sha256']
    for x in m['reused_related_sources']:
        p=repo/x['archive_path'];assert p.stat().st_size==x['size'] and sha(p)==x['sha256']
    receipts=json.loads((HERE/'receipts.json').read_text());assert len(receipts)==14
    assert {x['id'] for x in receipts}=={x['id'] for x in m['sources']}
    assert all(x['full_file_reviewed'] and x['related_material_checked'] and x['unique_content_accounted_for'] for x in receipts)
    event=json.loads((HERE/'review-001/execution-record.json').read_text())
    assert event['original_affine_entrypoint_calls']==1 and event['new_fixed_definition_entrypoint_calls']==1
    assert event['original_discovery_or_LP_entrypoint_calls']==0 and event['original_canonical_solver_calls']==0 and event['original_verify_certificate_calls']==0
    for x in event['events']:
        assert x['exit_code']==0 and x['stderr_bytes']==0
        assert sha(HERE/'review-001'/(x['label']+'.stdout'))==x['stdout_sha256']
        assert sha(HERE/'review-001'/(x['label']+'.stderr'))==x['stderr_sha256']
    assert (HERE/'original/boss/audit_affine_obstruction.json').read_bytes()==(HERE/'review-001/affine-runtime/audit_affine_obstruction.json').read_bytes()
    assert (HERE/'original/boss/audit_affine_obstruction.py').read_bytes()==(HERE/'review-001/affine-runtime/audit_affine_obstruction.py').read_bytes()
    r=json.loads((HERE/'review-001/definitions/report.json').read_text())
    cases=[r['literal_canonical'],*r['saved_cone_graphs']]
    for x in cases:
        data=gzip.decompress((HERE/'review-001/definitions'/(x['label']+'-all-IC.csv.gz')).read_bytes())
        assert hashlib.sha256(data).hexdigest()==x['all_IC_csv_sha256']
        assert len(data.splitlines())-1==x['comparisons_including_self']
        assert not x['negative_comparisons']
    state=HERE.parents[2]/'state'
    counter=state/'反例/五人均匀实际删位静态核的三十一客户反例--反例.md'
    text=counter.read_text()
    table={():1}
    for depth,prefix,actions in re.findall(r'^\| ([1-4]) \| (∅|[0-5]+) \| ([0-5]{6}) \|$',text,re.M):
        p=() if prefix=='∅' else tuple(map(int,prefix));assert len(p)==int(depth)-1
        for action,chosen in enumerate(actions):
            h=p+(action,);assert h not in table;table[h]=int(chosen)
    original=json.loads((HERE/'original/boss/uniform_deletion_failure_certificate.json').read_text())
    literal={tuple(x['history']):x['action'] for x in original['actions']}
    assert table==literal and len(table)==1555
    program=state/'程序/均匀删位核的三类发现器与原保存图--程序.md'
    saved_rows=re.findall(r'^\| ([56]),([35]) \| ([0-9]+),([0-9]+) \| ([0-5]+) \| ([0-5]) \| ([0-9.e+-]+) \| ([0-9]+) \| ([0-9]+) \|$',program.read_text(),re.M)
    assert len(saved_rows)==40
    affine=state/'障碍/四人父门槛筛选的仿射包络严格损失--障碍.md'
    affine_rows=re.findall(r'^\| ([0-3]{4}) \| ([0-9/]+) \| ([0-3, ]+) \|$',affine.read_text(),re.M)
    assert len(affine_rows)==35
    for q,t,outs in affine_rows:
        row=next(x for x in r['affine_independent_count_menus']['all_nonterminal_menus'] if ''.join(map(str,x['q']))==q)
        assert t==row['threshold'] and outs==', '.join(''.join(map(str,o)) for o in row['outcomes'])
    base=HERE.parents[4];links=[]
    for prose in [counter,affine,program,HERE/'README.md']:
        for target in re.findall(r'\]\(([^)]+)\)',prose.read_text()):
            if '://' in target or target.startswith('#'):continue
            target=target.split('#',1)[0];dest=(prose.parent/target).resolve()
            if not dest.is_file():assert (repo/dest.relative_to(base)).is_file(),(str(prose),target)
            links.append(target)
    report=dict(scope='static-delivery-reconciliation-only',primary_originals=14,primary_bytes=274970,related_source_interfaces=3,
                receipt_count=14,literal_action_table_entries=1555,displayed_cone_records=40,displayed_affine_nonterminal_rows=35,
                exact_saved_output_IC_rows=sum(x['comparisons_including_self'] for x in cases),local_prose_links=len(links),
                original_affine_report_byte_identical=True,all_source_and_output_hashes_match=True,
                mathematical_kernel_invocations_from_this_script=0)
    (HERE/'reconciliation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))

if __name__=='__main__':main()
