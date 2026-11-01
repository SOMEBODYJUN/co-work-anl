"""Static check of the preserved empty data report and shared evidence only."""
import ast
from collections import Counter
from fractions import Fraction as F
from hashlib import sha256
import json
from pathlib import Path
import re

HERE=Path(__file__).resolve().parent
REPO=HERE.parents[4]
BODY=REPO/'archives/customer-attraction/state/计算/回复子菜单查询的空切面报告--计算.md'
RECEIPT=REPO/'cleanup/workspaces/Boss7/receipts-round12/a11f2102ef9c4b9e2cc7.json'

def rec(path):
    b=path.read_bytes();return {'path':str(path.relative_to(REPO)),'bytes':len(b),'sha256':sha256(b).hexdigest()}

def check_bound(r):
    p=REPO/r.get('stored_path',r.get('path'));b=p.read_bytes()
    assert len(b)==r.get('size',r.get('bytes')) and sha256(b).hexdigest()==r['sha256'],p

def main():
    assert __debug__
    manifest=json.loads((HERE/'source-manifest.json').read_bytes())
    for key in ('primary','shared_exact_input','shared_generator','shared_current_helper_report'):check_bound(manifest[key])
    for key in ('prior_evidence_bound_not_rerun','formal_interfaces_compared'):
        for item in manifest[key]:check_bound(item)
    raw=json.loads((HERE/'original/tail_reply_subset_cuts.json').read_bytes())
    interpretation=json.loads((HERE/'data-interpretation.json').read_bytes())
    assert interpretation['report']==raw
    assert len(raw)==6 and raw['selected']==[] and raw['best_float']==[0,None]
    assert raw['source_sha256']==manifest['shared_exact_input']['sha256']
    assert F(raw['source_W'])==F(interpretation['point_metadata']['W'])
    domain=json.loads((HERE/'planned-domain.json').read_bytes())
    keys={(r['source_i_zero_based'],r['member'],tuple(r['orb']),r['query']) for r in domain['domain']}
    assert len(domain['domain'])==len(keys)==interpretation['static_domain_count']==96
    assert Counter(r['source_i_zero_based'] for r in domain['domain'])=={1:24,2:24,3:24,4:24}
    for row in domain['domain']:
        assert row['actual_player_one_based']==row['source_i_zero_based']+1
        assert row['remaining_true_tail_players']==5-row['source_i_zero_based']
        assert row['ordered_edges']==(6 if row['orb'][1] else 30)
        assert row['reply_label']==('R' if row['member']==0 else 'Z')
        assert row['status']=='static planned loop key; not a recorded successful LP, tested price, or cut'
    helper=json.loads((REPO/manifest['shared_current_helper_report']['path']).read_bytes())
    assert helper['point_sha256']==raw['source_sha256'] and helper['source_sha256']==manifest['shared_generator']['sha256']
    assert helper['status']=='PASS_FINITE_EXACT_ORIGINAL_HELPER_CONTRACTS'
    assert helper['main_calls']==helper['discover_calls']==helper['linprog_calls']==0
    prices={tuple(x) for x in helper['multiplier_probes']}
    assert prices=={('0','0'),('1/3','2/5'),('7/5','3/2')}
    sampled=helper['sampled_rows']
    seen={(r['i'],r['member'],tuple(r['orb']),r['q'],r['alpha'],r['gamma']) for r in sampled}
    expected={(*k,*price) for k in keys for price in prices}
    assert len(sampled)==288 and seen==expected
    assert all(F(r['slack'])>0 for r in sampled)
    assert helper['exact_coefficient_equalities']==288*1905==548640
    assert helper['explicit_tuple_comparison_checks']==14336 and helper['fallback_repeated_query_checks']==520
    for path in HERE.rglob('*.py'):ast.parse(path.read_bytes())
    json_files=0
    for path in HERE.rglob('*.json'):
        if path.name=='selfcheck.json':continue
        json.loads(path.read_bytes());json_files+=1
    receipt=json.loads(RECEIPT.read_bytes())
    assert receipt['id']=='a11f2102ef9c4b9e2cc7' and receipt['disposition']=='integrated'
    assert all(receipt[k] for k in ('full_file_reviewed','related_material_checked','unique_content_accounted_for'))
    for target in receipt['targets']:
        if target.endswith('/selfcheck.json'):continue
        assert (REPO/target).is_file(),target
    links=[]
    for path in (BODY,HERE/'README.md'):
        for target in re.findall(r'\]\(([^)]+)\)',path.read_text()):
            if '://' in target or target.startswith('#'):continue
            dest=(path.parent/target.split('#')[0]).resolve()
            assert dest.is_file(),(path,target)
            links.append(str(dest.relative_to(REPO)))
    inventory=[rec(p) for p in sorted(HERE.rglob('*')) if p.is_file() and p.name!='selfcheck.json']
    out={'status':'PASS','scope':'static stored-file, source binding, complete saved helper-record interpretation and link/receipt check; no original entrypoint/helper/LP or new mathematical probe','primary_id':receipt['id'],'body':rec(BODY),'receipt':rec(RECEIPT),'evidence_file_inventory':inventory,'json_files_parsed_excluding_selfcheck':json_files,'links_checked':len(links),'primary_fields':6,'saved_cut_records':0,'static_structures':96,'shared_fixed_price_records_read':288,'shared_fixed_price_rows_all_positive':True,'data_task_original_or_helper_or_LP_calls':0,'new_calls_by_this_selfcheck':0}
    print(json.dumps(out,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
