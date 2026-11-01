"""Static package consistency only; no original or independent audit rerun."""
import ast
from collections import Counter
from fractions import Fraction as F
from hashlib import sha256
import json
from pathlib import Path
import re

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[4]
BODY=ROOT/'archives/customer-attraction/state/计算/背景菜单的有限证书--计算.md'
RECEIPT=ROOT/'cleanup/workspaces/Boss7/receipts-round13/b9595537628e7f8219f5.json'
PEER=HERE.parent/'background-menu-certificate-program'

def fp(p):
    b=p.read_bytes()
    return {'path':str(p.relative_to(ROOT)),'bytes':len(b),'sha256':sha256(b).hexdigest()}

def read(p):
    return json.loads(p.read_bytes())

def main():
    assert __debug__
    manifest=read(HERE/'source-manifest.json')
    bound=manifest['bound_files']
    for record in bound:
        assert fp(ROOT/record['path'])==record
    cert=read(HERE/'original/background_menu_certificate.json')
    exact=read(HERE/'exact-audit.json')
    ledger=read(HERE/'case-ledger.json')
    assert cert==exact['certificate_fields']
    assert cert=={'success':True,'labels':'ABTSQRHV','slacks':{'floor_B':'1/2','floor_H':'1','last_B_A_T':'1','last_B_A_S':'1'},'cases':384,'minimum':'0'}
    assert ledger['labels']==cert['labels']
    names=exact['ordered_slack_names'];weights=list(map(F,exact['multipliers']))
    assert names==ledger['ordered_slack_names'] and len(names)==len(weights)==39
    assert all(x>=0 for x in weights) and sum(weights)==F(7,2)
    assert [i for i,x in enumerate(weights) if x]==exact['active_column_indices']==[4,9,12,13]
    cases=ledger['cases'];assert len(cases)==exact['rows']==384
    signs=Counter(); kinds=Counter()
    for i,row in enumerate(cases):
        assert row['index']==i and len(row['bits'])==8 and set(row['bits'])<=set('01')
        assert (row['bits'][6]=='0')==(row['case']=='fresh')
        coeff=list(map(F,row['all_39_scaled_IC_coefficients']))
        assert len(coeff)==39 and all(c.denominator==1 for c in coeff)
        assert sum(c*w for c,w in zip(coeff,weights))==F(row['weighted_IC_coefficient'])
        assert F(row['scaled_target'])-F(row['weighted_IC_coefficient'])==F(row['remainder'])==F(row['closed_form'])>=0
        assert row['four_active_IC_coefficients']=={n:str(coeff[names.index(n)]) for n in cert['slacks']}
        signs[row['case'],'zero' if F(row['remainder'])==0 else 'positive']+=1
        kinds[row['case']]+=1
    assert dict(kinds)=={'fresh':128,'p1':128,'slope':128}
    assert {k:{sign:signs[k,sign] for sign in ('zero','positive')} for k in kinds}==exact['by_case']
    assert sum(v for (k,s),v in signs.items() if s=='zero')==exact['zero_remainders']==80
    assert sum(v for (k,s),v in signs.items() if s=='positive')==exact['positive_remainders']==304
    covered=[]
    for group in exact['effective_residual_classes']:
        ids=group['full_case_indices'];assert len(ids)==8
        covered.extend(ids)
        for i in ids:
            row=cases[i]
            assert row['case']==group['case'] and list(map(int,row['bits'][:4]))==group['ABTS']
            assert row['remainder']==group['remainder']
    assert len(exact['effective_residual_classes'])==48 and sorted(covered)==list(range(384))
    assert exact['exact_IC_coefficients_reconstructed']==384*39==14976
    assert exact['original_entrypoint_calls']==exact['original_helper_calls']==exact['LP_calls']==0
    event=read(PEER/'replay/execution.json')
    assert event['returncode']==0 and event['original_entry_calls']==event['linprog_calls_in_original_main']==1
    assert event['other_original_entry_calls']==0 and event['new_output_matches_frozen_bytes'] is True
    assert event['source_before']==event['source_after']
    assert {k:fp(PEER/'original/background_menu_certificate.py')[k] for k in ('bytes','sha256')}==event['source_before']
    original=(HERE/'original/background_menu_certificate.json').read_bytes()
    assert original==(PEER/'replay/background_menu_certificate.json').read_bytes()==(PEER/'replay/stdout.txt').read_bytes()
    assert (PEER/'replay/stderr.txt').read_bytes()==b''
    for filename,record in event['files'].items():
        assert {k:fp(PEER/'replay'/filename)[k] for k in ('bytes','sha256')}==record
    receipt=read(RECEIPT)
    assert receipt['id']=='b9595537628e7f8219f5' and receipt['disposition']=='integrated'
    assert all(receipt[k] is True for k in ('full_file_reviewed','related_material_checked','unique_content_accounted_for'))
    for target in receipt['targets']:
        assert (ROOT/target).is_file() or ROOT/target==HERE/'self-check.json'
    links=[]
    for doc in (BODY,HERE/'README.md'):
        for link in re.findall(r'\]\(([^)]+)\)',doc.read_text()):
            if link.startswith(('https:','http:','#','source:')):continue
            target=(doc.parent/link.split('#',1)[0]).resolve()
            assert target.is_file() or target==HERE/'self-check.json',(doc,link)
            links.append({'from':str(doc.relative_to(ROOT)),'link':link,'target':str(target.relative_to(ROOT))})
    python_files=[HERE/'audit_certificate.py',HERE/'check_package.py',PEER/'original/background_menu_certificate.py']
    for path in python_files:ast.parse(path.read_bytes())
    json_files=sorted(HERE.rglob('*.json'))
    for path in json_files:read(path)
    inventory=sorted(p for p in HERE.rglob('*') if p.is_file() and p.name!='self-check.json')+[BODY,RECEIPT]
    report={'status':'PASS_STATIC_PACKAGE_CHECK','scope':'saved record consistency, source fingerprints, local links and receipt; no original or independent mathematics rerun',
      'bound_files_checked':len(bound),'preserved_case_rows_checked':384,'saved_IC_entries_checked':14976,'effective_groups_checked':48,
      'shared_original_main_events':1,'shared_original_LP_events':1,'original_main_calls_in_this_check':0,'original_helper_calls_in_this_check':0,'independent_audit_calls_in_this_check':0,'LP_calls_in_this_check':0,
      'python_AST_files':len(python_files),'json_files_parsed':len(json_files),'receipt_targets':len(receipt['targets']),'local_links_checked':len(links),
      'links':links,'files':[fp(p) for p in inventory],
      'raw_related_markdown_links':'Preserved frozen workspace README links are original source-relative paths, not claimed to be live cleaned-object links.'}
    print(json.dumps(report,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
