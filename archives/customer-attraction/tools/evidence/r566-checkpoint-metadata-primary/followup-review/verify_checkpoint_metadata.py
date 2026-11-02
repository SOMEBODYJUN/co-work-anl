"""Independent metadata/transcription comparison; no mathematical entrypoint run.

Reads only the explicitly supplied workspace/repository roots, writes only OUT.
Do not interpret success as 174 members read, a historical run recreated, a
second row implementation, an LP optimum or a complete SPE certificate.
"""
from pathlib import Path
from collections import defaultdict
from fractions import Fraction
import ast
import hashlib
import json
import re

import argparse
HERE = Path(__file__).resolve().parent
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--repo', type=Path, default=next(p for p in HERE.parents if (p/'cleanup/inventory.jsonl').exists()))
parser.add_argument('--work', type=Path, default=HERE)
parser.add_argument('--out', type=Path, default=HERE/'reproduced')
args=parser.parse_args()
REPO=args.repo.resolve()
WORK=args.work.resolve()
OUT=args.out.resolve()
OUT.mkdir(parents=True,exist_ok=True)
EVID = REPO / 'archives/customer-attraction/tools/evidence'
OLD = EVID / 'r566-checkpoint-metadata-primary'
SOURCES = {r['id']: r for r in json.loads((WORK/'manifest.json').read_text())}
NAMES = {'3913485fc9b9d5810df5':'checkpoint_manifest.json', 'c6b117b9e8fd491d2d98':'checkpoint_verification.json'}

def read(p): return json.loads(p.read_text())
def fp(p):
    b=p.read_bytes()
    return {'path':str(p), 'bytes':len(b), 'sha256':hashlib.sha256(b).hexdigest()}

identity=[]
for sid,name in NAMES.items():
    p=WORK/'sources'/f'{sid}-{name}'
    expected=SOURCES[sid]
    saved=next(r for r in read(OLD/'source-manifest.json') if r['id']==sid)
    f=fp(p)
    check={'id':sid, 'actual':f,
      'matches_source_size_sha':(f['bytes'],f['sha256'])==(expected['size'],expected['sha256']),
      'formal_original_byte_equal':p.read_bytes()==(OLD/'original'/name).read_bytes(),
      'formal_source_manifest_identity_equal':all(expected[k]==saved[k] for k in ('id','blob','mode','path','size','sha256','sources')),
      'preserved_path_correct':saved['preserved_path']==f'original/{name}'}
    assert all(v for k,v in check.items() if k not in ('id','actual'))
    identity.append(check)

manifest=read(WORK/'sources/3913485fc9b9d5810df5-checkpoint_manifest.json')
verification=read(WORK/'sources/c6b117b9e8fd491d2d98-checkpoint_verification.json')
by_path=defaultdict(list)
for line in (REPO/'cleanup/inventory.jsonl').read_text().splitlines():
    r=json.loads(line);by_path[r['path']].append(r)
old_comparison=read(OLD/'manifest-inventory-comparison.json')
rows=[]
for i,item in enumerate(manifest['files']):
    versions=by_path[item['path']]
    matches=[r for r in versions if (r['sha256'],r['size'])==(item['sha256'],item['bytes'])]
    other=[r for r in versions if r not in matches]
    normalized={'path':item['path'],'manifest_sha256':item['sha256'],'manifest_bytes':item['bytes'],
       'frozen_matching_ids':[r['id'] for r in matches],'other_frozen_ids':[r['id'] for r in other]}
    assert normalized==old_comparison[i]
    rows.append({'index':i,**normalized,'frozen_versions':[{k:r[k] for k in ('id','sha256','size','sources')} for r in versions]})
assert len(old_comparison)==len(rows)
prefix=manifest['files'][0]['path'].rsplit('/',1)[0]+'/'
by_name={r['path'].removeprefix(prefix):r for r in manifest['files']}
resource=REPO/'archives/customer-attraction/state/资源/R5662研究checkpoint的版本清单与有限复核--资源.md'
doc=resource.read_text()
table=[(int(a),b,int(c)) for a,b,c in re.findall(r'^\|(\d+)\|`([^`]+)`\|(\d+)\|$',doc,re.M)]
assert table==[(i,r['path'].removeprefix(prefix),r['bytes']) for i,r in enumerate(manifest['files'])]
blocks=[json.loads(s) for s in re.findall(r'```json\n(.*?)\n```',doc,re.S)]
assert blocks[0]==verification

bindings={
 'research_2/B_menu_prices_master.py': EVID/'b-family-menu-prices-boss3/original/research_2/B_menu_prices_master.py',
 'research_3/refine_terminal_portfolio.py': EVID/'terminal-capacity-refinement-boss3/related/refine_terminal_portfolio.py',
 'research_5/coupled_latest_master.py': EVID/'coupled-latest-menu-check-boss3/original/coupled_latest_master.py',
 'research_4/verify_minimum_reply_commutation.py': EVID/'minimum-reply-commutation-program/original/verify_minimum_reply_commutation.py',
 'research_1/audit_B_menu_actual_prices.py': WORK/'sources/59a90ea11a2df684017e-audit_B_menu_actual_prices.py',
}
code_bindings=[]
for name,path in bindings.items():
    f=fp(path);row=by_name[name]
    assert (f['bytes'],f['sha256'])==(row['bytes'],row['sha256'])
    code_bindings.append({'manifest_relative_path':name,'actual':f,'same_manifest_size_sha':True})

menu_stdout=(EVID/'b-family-menu-prices-boss3/replay/verify-stdout.txt').read_text().splitlines()
menu=ast.literal_eval(menu_stdout[-1])
capacity=ast.literal_eval((EVID/'terminal-capacity-refinement-boss3/runs/original.stdout').read_text())
latest=read(EVID/'coupled-latest-menu-check-boss3/replay/latest/summary.json')
comm=read(EVID/'minimum-reply-commutation-program/rerun/stdout.txt')
checks=verification['checks']
assert menu['rows']==checks[0]['rows'] and menu['minimum_slack']==checks[0]['minimum_slack']
assert re.search(r'^built 5692 rows 4849 columns ',menu_stdout[0])
assert capacity['rows']==checks[1]['rows'] and capacity['min_slack']==checks[1]['minimum_slack']
assert latest['rows']==checks[2]['rows'] and latest['columns']==checks[2]['columns'] and latest['minimum_slack']==checks[2]['minimum_slack']
assert comm['all_two_player_policies']==checks[3]['complete_two_tail_policies'] and comm['SPE_tail_policies']==checks[3]['SPE_policies'] and comm['strict_gap']==checks[3]['strict_gap']
assert (fp(EVID/'minimum-reply-commutation-program/rerun/stdout.txt')['bytes'],fp(EVID/'minimum-reply-commutation-program/rerun/stdout.txt')['sha256'])==(by_name['research_4/minimum_reply_commutation_report.json']['bytes'],by_name['research_4/minimum_reply_commutation_report.json']['sha256'])
# A six-term scalar identity; not the proof of the incidence-budget interface.
endpoint=sum(Fraction(1)/(6+(Fraction(149,50)-1)*r) for r in range(1,7))
assert str(endpoint)==verification['peer_author_replays']['incidence_tau_endpoint']

summary={'scope':'metadata/transcription/existing-output and six-term scalar identity only; zero research imports, entrypoint runs, matrix reconstructions, LPs, potential or SPE enumerations',
 'source_checks':identity,
 'manifest':{'entries':len(rows),'unique_paths':len(set(r['path'] for r in rows)),'declared_bytes':sum(r['manifest_bytes'] for r in rows),
 'same_frozen_path_size_sha':sum(bool(r['frozen_matching_ids']) for r in rows),'known_other_version':sum(not r['frozen_matching_ids'] and bool(r['other_frozen_ids']) for r in rows),
 'missing_inventory_path':sum(not r['frozen_versions'] for r in rows),'all_existing_comparison_rows_exact':True,'all_resource_table_rows_exact':True,
 'scope':manifest['scope'],'snapshot_commit':manifest['snapshot_commit'],'note':manifest['note'],'lists_itself':'checkpoint_manifest.json' in by_name,
 'all_member_paths_in_actor_workspace':all(r['path'].startswith(prefix) for r in manifest['files']),
 'link_checker_outside_manifest':'research/check_active_research.py' not in [r['path'] for r in manifest['files']]},
 'verification_full_JSON_transcription_exact':True,
 'historical_verification_all_fields':verification,
 'five_saved_code_versions_match_manifest':code_bindings,
 'later_stored_reports_compared':{'5692':menu,'5112':capacity,'5277':{k:latest[k] for k in ('source_point_sha256','rows','columns','minimum_slack','scope')},
 'commutation':comm,'commutation_stdout_matches_manifest_report_size_SHA':True,
 '5277_later_event_uses_original_builder_not_master_main':True,
 'old_vs_later_events_are_not_identical_historical_execution_claims':True},
 'scalar_only':{'incidence_tau': '149/50','six_term_sum':str(endpoint),'excess_over_half':str(endpoint-Fraction(1,2))},
 'unverified_historical_execution_details':['old 502-link execution identity/transcript','old git diff --check transcript/base','old own-file curation copy and exact dependency staging','peer mixed_singleton all-seven report underlying run','peer 3904-column underlying run']}
(OUT/'manifest-comparison.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
(OUT/'evidence-check.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:summary[k] for k in ('scope','manifest','verification_full_JSON_transcription_exact','scalar_only')},ensure_ascii=False,indent=2))
