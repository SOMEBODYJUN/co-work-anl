"""Static package validation; never imports or executes the mathematical source."""
import ast
from hashlib import sha256
import json
from pathlib import Path
import re

HERE=Path(__file__).resolve().parent
REPO=HERE.parents[4]
BODY=REPO/'archives/customer-attraction/state/程序/背景菜单的有限证书程序--程序.md'
RECEIPT=REPO/'cleanup/workspaces/Boss7/receipts-round13/d46bde33a0a22e62434e.json'
def digest(p):return sha256(p.read_bytes()).hexdigest()

def main():
    manifest=json.loads((HERE/'artifact-manifest.json').read_text())
    for row in manifest['files']:
        path=REPO/row['path']
        assert path.stat().st_size==row['bytes'] and digest(path)==row['sha256'],str(path)
    files=list(HERE.rglob('*'))+[BODY,RECEIPT]
    syntax=[];jsons=[];links=[]
    for path in files:
        if not path.is_file():continue
        if path.suffix=='.py':ast.parse(path.read_bytes());syntax.append(str(path.relative_to(REPO)))
        if path.suffix=='.json':json.loads(path.read_bytes());jsons.append(str(path.relative_to(REPO)))
        if path.suffix=='.md':
            for link in re.findall(r'\]\(([^)]+)\)',path.read_text()):
                if link.startswith(('http:','https:','#')):continue
                dest=(path.parent/link.split('#',1)[0]).resolve()
                assert dest.exists(),(str(path),link)
                links.append({'from':str(path.relative_to(REPO)),'target':str(dest.relative_to(REPO))})
    primary=json.loads((HERE/'source-manifest.json').read_text())['sources'][0]
    src=HERE/primary['preserved_path']
    assert digest(src)==primary['source']['sha256']=='06a392ce682cbc6429fe34ca5806398bb0cbdc2dd67e0c20908816d57e0c5db0'
    event=json.loads((HERE/'replay/execution.json').read_text())
    assert event['returncode']==0 and event['original_entry_calls']==event['linprog_calls_in_original_main']==1
    assert event['source_before']==event['source_after'] and event['new_output_matches_frozen_bytes']
    for name,record in event['files'].items():
        p=HERE/'replay'/name
        assert p.stat().st_size==record['bytes'] and digest(p)==record['sha256']
    assert (HERE/'replay/background_menu_certificate.json').read_bytes()==(HERE/'replay/stdout.txt').read_bytes()
    shared=HERE.parent/'background-menu-certificate-data'
    assert (shared/'original/background_menu_certificate.json').read_bytes()==(HERE/'replay/background_menu_certificate.json').read_bytes()
    report=json.loads((shared/'exact-audit.json').read_text())
    assert report['rows']==384 and report['exact_IC_coefficients_reconstructed']==14976
    assert report['zero_remainders']==80 and report['positive_remainders']==304
    assert report['original_entrypoint_calls']==report['original_helper_calls']==report['LP_calls']==0
    receipt=json.loads(RECEIPT.read_text())
    assert receipt['id']=='d46bde33a0a22e62434e' and receipt['disposition']=='integrated'
    for key in ('full_file_reviewed','related_material_checked','unique_content_accounted_for'):assert receipt[key] is True
    for target in receipt['targets']:assert (REPO/target).is_file(),target
    result={'status':'PASS_STATIC_PACKAGE','bound_files':len(manifest['files']),'json_parsed':len(jsons),'python_ast_parsed':len(syntax),'markdown_links':len(links),'receipt_targets':len(receipt['targets']),'new_math_execution':False,'shared_audit_sha256':digest(shared/'exact-audit.json'),'checked_links':links}
    (HERE/'self-check.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='checked_links'},indent=2))
if __name__=='__main__':main()
