"""One original supported-branch run and one explicitly truncated ZZ prefix.

The 1083 old raw and 2806 bound rows are NOT executed here. The old-schema
dependency is stored losslessly gzipped; original bytes are restored only into
an isolated scratch layout. All execution scope and stdio are recorded.
"""
from pathlib import Path
from itertools import product
from fractions import Fraction as F
import argparse, datetime, gzip, hashlib, json, runpy, shutil, subprocess, sys, time

MARKER='# Check all preceding raw rows using their frozen exact definitions.'
ATOM_REL='archives/customer-attraction/tools/evidence/ra241-oracle-cross-pair-primary/related-original/research/workspaces/customer-attraction/R-a8ee6fdb155c47da95540775b4a6a2db/closure/joint_atoms_exact.json'

def fp(p):return {'size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}

def supported(base, runtime):
    folder=runtime/'supported';folder.mkdir(parents=True)
    src=base/'original/verify_supported_branch.py';script=folder/src.name;shutil.copyfile(src,script)
    ns=runpy.run_path(str(script),run_name='scoped_original_supported_branch')
    checks={}
    for file in ('supported_branch_audit.json','supported_branch_six_full_policy.json'):
        actual=folder/file;old=base/'original'/file
        assert actual.read_bytes()==old.read_bytes()
        checks[file]={'byte_identical':True,'original':fp(old),'new_output':fp(actual)}
    raw=json.loads((base/'original/supported_branch_six_full_policy.json').read_text())
    entries=raw['policy'];policy={tuple(e['history']):e['action']for e in entries}
    expected={h for depth in range(raw['m'])for h in product(range(raw['p']),repeat=depth)}
    assert len(policy)==len(entries)==1365 and set(policy)==expected
    assert all(type(a)is int and 0<=a<4 for a in policy.values())
    assert raw['clients']==[[0],[0,1],[1,2],[3],[3],[3]]
    assert policy[(3,3,3,0,1)]==0 and policy[(3,3,3,1,0)]==1
    compact={str(depth):''.join(str(policy[h])for h in product(range(4),repeat=depth))for depth in range(6)}
    result={'scope':'one unmodified original top-level construction/audit, then one separate complete-key inventory check',
            'original_top_level_runs':1,'new_complete_key_inventory_checks':1,
            'outputs':checks,'complete_ordered_keys':1365,'all_actions_legal':True,
            'policy_compact_lexicographic_by_depth':compact,
            'same_count_different_history_reply':{'33301':0,'33310':1},
            'forced_nodes':len(ns['forced']),
            'root_outcome_count_scope':'E uses16 forced action nodes; its one root count is NOT the unconstrained game SPE outcome set',
            'restricted_root_outcome_counts':[list(q)for q in sorted(ns['E'](()))],
            'audit_report':json.loads((folder/'supported_branch_audit.json').read_text()),
            'source':fp(src)}
    (base/'replay/supported-byte-and-key-review.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'unmodified_supported_runs':1,'two_output_files_byte_identical':True,'key_inventory':1365,'forced_nodes':len(ns['forced'])}),flush=True)

def zzprefix(base, runtime, repo):
    root=runtime/'zz-layout';work=root/'research/workspaces/customer-attraction/R-a8ee6fdb155c47da95540775b4a6a2db';attack=work/'attack';closure=work/'closure'
    attack.mkdir(parents=True);closure.mkdir()
    # The original prefix only tests this marker's existence; it is never run.
    (root/'work.py').write_text('# inert ancestor-location marker; never executed\n')
    src=base/'original/review_joint_atoms_independent.py';script=attack/src.name;shutil.copyfile(src,script)
    atomsrc=repo/ATOM_REL;assert fp(atomsrc)['sha256']=='b4c40bc9ab35ea5ba162d84e5f8020af54e66f9c167af11bbc07acf2185998a4'
    shutil.copyfile(atomsrc,closure/'joint_atoms_exact.json')
    schema=closure/'joint_atoms_old_schema.json';schema.write_bytes(gzip.decompress((base/'dependencies/joint_atoms_old_schema.json.gz').read_bytes()))
    assert fp(schema)['sha256']=='50a8645a1b365e21b94ce601e4ce40fa3b44a2743735ec639e70ead44c0cefd4'
    source=src.read_text();assert source.count(MARKER)==1;prefix=source.split(MARKER)[0]
    ns={'__file__':str(script),'__name__':'explicitly_truncated_ZZ_review_prefix'}
    exec(compile(prefix,str(script)+' [prefix only]','exec'),ns)
    old=json.loads((base/'original/closure_independent_review.json').read_text())
    rows=[{'f':f,'g':g,'partition':list(p),'literal_label_pairs':ns['paircounts'][f,g,p],'value':str(ns['zz'][f,g,p])}for f,g,p in ns['ROWS']]
    assert rows==old['ZZ_rows'] and len(rows)==60 and min(ns['zz'].values())>=0
    checked={'atoms':len(ns['d']['atoms']),'histograms':len(ns['histmass']),
             'reply_labels_per_atom':len(ns['labels']),'literal_pair_comparisons':ns['paircomparisons'],
             'denominator_identity_checks':ns['semantic_polynomial_matches'],
             'four_state_bounds_checked':ns['fourbounds'],
             'RR_upper_bounds_checked_including_diagonal_and_both_orders':ns['rrbounds'],
             'minimum_implicit_00_mass':str(ns['minfour']),'minimum_RR_upper_slack':str(ns['minrr']),
             'matched_old_schema_columns':len(ns['generated']),
             'K':str(F(ns['d']['K'])),'O':str(ns['O']),'W':str(ns['W']),
             'strict_half_gap':str(1-2*ns['W'])}
    assert all(v==old[k] for k,v in checked.items())
    assert sum(x['literal_label_pairs']for x in rows)==66**2
    raw=ns['old']; assert len(raw['columns'])==1905
    assert sum(F(c['weight'])>0 for c in raw['columns'])==raw['positive_columns']==527
    result={'scope':'original prefix only; all60 ZZ and1905 column masses; no old-library build or row replay',
            'original_full_entry_runs':0,'original_prefix_executes':1,
            'cut_marker_exclusive':MARKER,'executed_line_count':len(prefix.splitlines()),
            'first_unexecuted_line':len(prefix.splitlines())+1,
            'executed_definition_and_assertion_scope':['imports and root/input location','groupkey, canon,15 partitions,66 labels,60 row definitions','all27 atoms positivity and binary/common-assignment checks','194 four-state implicit00 checks','5612 ordered/diagonal RR upper checks','117612 literal comparisons and denominator identities','all1905 reconstructed old-column mass equalities'],
            'not_executed':['sys.path insertion of SOURCE old library','import attractive_nested','at.build of old matrix','1083 preceding raw rows','2806 preceding bound rows','original final report write/print'],
            'checked_frozen_fields':checked,'new_ZZ_rows_all60_identical':True,'ZZ_rows':rows,
            'old_schema_positive_columns':527,
            'old_schema_top_level_fields_accounted_for':list(raw),
            'old_raw_bound_counts_only_inherited_from_source_report':{'raw':old['prior_raw_rows_shared_library_replayed'],'bound':old['prior_bound_rows_replayed']},
            'group_equality_is_chosen_witness_restriction_not_universal_constraint':True,
            'input_atom_source':{'path':ATOM_REL,**fp(atomsrc)},'schema_uncompressed':fp(schema),
            'schema_gzip':fp(base/'dependencies/joint_atoms_old_schema.json.gz'),
            'original_source':fp(src),'executed_prefix_sha256':hashlib.sha256(prefix.encode()).hexdigest(),
            'inert_root_marker_not_executed':True,'new_independent_third_implementation_claimed':False}
    (base/'replay/zz-prefix-review.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'prefix_only':True,'executed_lines':len(prefix.splitlines()),'checked':checked,'old_raw_replayed_here':0,'old_bounds_replayed_here':0}),flush=True)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--repo',required=True,type=Path);ap.add_argument('--runtime',required=True,type=Path);ap.add_argument('--worker',choices=['supported','zz-prefix']);a=ap.parse_args()
    base=Path(__file__).resolve().parent;out=base/'replay';out.mkdir(exist_ok=True)
    if a.worker:
        a.runtime.mkdir(parents=True,exist_ok=True)
        if a.worker=='supported':supported(base,a.runtime)
        else:zzprefix(base,a.runtime,a.repo.resolve())
        return
    if a.runtime.exists():raise SystemExit('refuse to overwrite an existing runtime; supply a fresh --runtime')
    a.runtime.mkdir(parents=True)
    events=[]
    for task in ('supported','zz-prefix'):
        cmd=[sys.executable,'-I',str(Path(__file__).resolve()),'--repo',str(a.repo.resolve()),'--runtime',str(a.runtime.resolve()),'--worker',task]
        started=datetime.datetime.now(datetime.timezone.utc).isoformat();t=time.monotonic();p=subprocess.run(cmd,capture_output=True,text=True)
        stdout=out/(task+'-stdout.txt');stderr=out/(task+'-stderr.txt');stdout.write_text(p.stdout);stderr.write_text(p.stderr)
        events.append({'task':task,'argv':cmd,'start_utc':started,'elapsed_seconds':time.monotonic()-t,'returncode':p.returncode,'stdout':fp(stdout),'stderr':fp(stderr),'driver':fp(Path(__file__))})
        (out/'execution-record.json').write_text(json.dumps(events,ensure_ascii=False,indent=2)+'\n')
        print(p.stdout,end='');print(p.stderr,end='',file=sys.stderr)
        if p.returncode:raise SystemExit(p.returncode)
    print(json.dumps(events,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
