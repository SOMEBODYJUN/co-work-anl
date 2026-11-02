#!/usr/bin/env python3
"""Static packaging check only; no game payoff, BI, LP, random or project calls."""
import argparse,hashlib,json,re
from datetime import datetime,timezone
from pathlib import Path

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--repo',required=True,type=Path);args=ap.parse_args()
    repo=args.repo.resolve();package=Path(__file__).resolve().parent
    stage=next((p for p in package.parents if p.name=='deliverables'),repo)
    manifest=json.loads((package/'manifest.json').read_text());related=json.loads((package/'related-manifest.json').read_text())
    receipts=json.loads((package/'receipts.json').read_text())
    assert len(manifest['sources'])==manifest['primary_count']==len(receipts)==13
    assert sum(r['size'] for r in manifest['sources'])==manifest['primary_bytes']==570479
    assert len(related)==2 and sum(r['size'] for r in related)==6365
    assert {r['id'] for r in receipts}=={r['id'] for r in manifest['sources']}
    checked=[]
    for row in manifest['sources']+related:
        p=package/row['package_path'];assert p.stat().st_size==row['size'] and sha(p)==row['sha256']
        assert len(row['sources'])==2 and all(len(s['commit'])==40 and s['path']==row['path'] for s in row['sources'])
        checked.append({'id':row['id'],'sha256':row['sha256'],'size':row['size']})
    for row in receipts:
        assert all(row[k] is True for k in ('full_file_reviewed','related_material_checked','unique_content_accounted_for'))
        assert row['disposition'] in ('integrated','duplicate')
        assert all(row[k] for k in ('read_note','comparison_note','decision_note','targets'))
        assert all((stage/t).is_file() or (repo/t).is_file() for t in row['targets'])
    assert sum(row['disposition']=='duplicate' for row in receipts)==1
    run=package/'new-fixed-audit-001';event=json.loads((run/'execution-record.json').read_text())
    assert event['exit_code']==0 and event['new_fixed_audit_process_calls']==1
    assert event['stdout_bytes']==(run/'stdout.txt').stat().st_size==8373 and event['stderr_bytes']==0
    assert (run/'stderr.txt').read_bytes()==b''
    assert event['script_sha256']==sha(package/'audit_fixed_records.py')
    assert event['stdout_sha256']==sha(run/'stdout.txt') and event['stderr_sha256']==sha(run/'stderr.txt')
    assert all(event[k]==0 for k in ('original_CLI_calls','project_solver_or_verifier_calls','LP_calls','random_calls','original_five_generated_random_checks_replayed','p4_twelve_client_game_rechecks','template_audit_rechecks'))
    summary=json.loads((run/'data/summary.json').read_text());assert summary==json.loads((run/'stdout.txt').read_text())
    assert summary['all_checks_passed'] is True and summary['policy_records']==180
    assert summary['one_interest_records']==177 and summary['mixed_interest_records']==3
    states=comparisons=0
    for name in ['bg_s2r2k6','bg_s6r2k7','bg_s2r3k6']:
        raw=json.loads((package/f'original/early_price/{name}.json').read_text())
        fixed=json.loads((run/f'data/{name}-exact-policies.json').read_text())
        assert len(raw['records'])==len(fixed['records'])==60
        for old,new in zip(raw['records'],fixed['records']):
            assert old['trial']==new['trial'] and old['iteration']==new['iteration']
            assert old['background']==new['background'] and old['root']==new['root'] and old['target_action']==new['target_action']
            assert [(r['counts'],r['action']) for r in old['actions']]==[(r['counts'],r['action']) for r in new['all_node_payoffs']]
            assert new['count_policy_states']==len(new['all_node_payoffs'])
            assert all(len(r['all_true_query_payoffs'])==len(old['root']) for r in new['all_node_payoffs'])
            assert new['saved_query_strong_gap']=='0'
            states+=new['count_policy_states'];comparisons+=new['comparisons_including_self']
    assert states==2580 and comparisons==15960
    full=json.loads((run/'data/fullset-four-fixed-points.json').read_text())
    assert len(full)==4 and [r['trial'] for r in full]==[0,2,3,6]
    assert [r['saved_query_strong_gap_exact'] for r in full]==['-32','-419/15','-25','0']
    assert all(r['price_optimality_certified'] is False for r in full)
    bg=json.loads((run/'data/allbg-nine-fixed-points-and-new-suffixes.json').read_text())
    assert len(bg)==9 and sum(r['new_suffix_policy']['ordered_nodes'] for r in bg)==37
    assert sum(r['new_suffix_policy']['comparisons_including_self'] for r in bg)==259
    assert all(len(r['new_suffix_policy']['all_nodes'])==r['new_suffix_policy']['ordered_nodes'] for r in bg)
    reuse=json.loads((package/'comparison-and-reuse.json').read_text())
    for row in reuse['full_read_mature_objects']:
        p=repo/row['path'];assert p.stat().st_size==row['size'] and sha(p)==row['sha256']
    assert (repo/reuse['p4_reused_context']).read_bytes()==(package/'original/global/strict_static_bridge_compressed_p4.json').read_bytes()
    assert sha(repo/reuse['p4_reused_exact_evidence'])==reuse['p4_reused_exact_evidence_sha256']
    pages=[stage/'archives/customer-attraction/state/程序/固定合法背景价格锥的交替接口与一百八十份保存策略--程序.md',
           stage/'archives/customer-attraction/state/计算/整数全集价格探针与全前缀机会预算的十三个保存点--计算.md',
           stage/'archives/customer-attraction/state/资源/早期价格原审计与严格四标签压缩点的来源合同--资源.md']
    links=[]
    for page in pages+[package/'README.md']:
        text=page.read_text()
        if page in pages:assert text.startswith('---\nid: ') and '\nsource_refs:\n' in text and re.search(r'source:[0-9a-f]{40}:research/',text)
        for link in re.findall(r'\]\(([^)]+)\)',text):
            if re.match(r'[a-zA-Z][a-zA-Z0-9+.-]*:',link) or link.startswith('#'):continue
            target=(page.parent/link.split('#',1)[0]).resolve()
            if target.is_file():kind='stage-or-current-repository'
            else:
                rel=target.relative_to(stage);assert (repo/rel).is_file(),(str(page),link)
                kind='inherited-repository'
            links.append({'page':str(page.relative_to(stage)),'link':link,'resolved':kind})
    out={'identity':'Boss3','checked_at_utc':datetime.now(timezone.utc).isoformat(),
         'scope':'static hashes, receipts, existing event/output, preserved-policy provenance and output shape, mature reuse and links only; no mathematical execution',
         'source_checks':checked,'primary_receipts':13,'duplicate_receipts':1,'formal_pages':3,
         'policy_records':180,'count_policy_states':states,'stored_comparisons_including_self':comparisons,
         'integer_saved_records':13,'new_suffix_policy_files':9,'links':links,
         'mature_comparison_hashes':12,'p4_exact_context_bytes_same':True,
         'mathematical_reexecutions_in_this_check':0,'all_checks_passed':True}
    (package/'self-check.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'ok':True,'primary_sources':13,'related_sources':2,'receipts':13,'formal_pages':3,'links':len(links),'mathematical_reexecutions':0}))

if __name__=='__main__':main()
