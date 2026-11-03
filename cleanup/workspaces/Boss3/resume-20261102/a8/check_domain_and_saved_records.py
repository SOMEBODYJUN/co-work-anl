"""Static domain/record check only. Never import/execute original programs or scan inputs."""
from pathlib import Path
import ast,json,hashlib,math,re,difflib,yaml
R=Path.cwd();E=R/'archives/customer-attraction/tools/evidence/copy-tax-domain-correction-resumed-boss3';W=R/'cleanup/workspaces/Boss3/resume-20261102/a8'
M=json.loads((E/'source-manifest.json').read_text());saved=json.loads((E/'saved-record-manifest.json').read_text());by={Path(x['path']).name:R/x['evidence_path'] for x in M}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
for x in M:
 p=R/x['evidence_path'];assert p.stat().st_size==x['size'] and sha(p)==x['sha256'];assert sha(R/x['copied_from'])==x['sha256']
for x in saved:
 p=R/x['evidence_path'];assert p.stat().st_size==x['size'] and sha(p)==x['sha256'];assert sha(R/x['from'])==x['sha256']
tree=ast.parse(by['exhaust_copy_tax_three_topics.py'].read_text());func=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='run_case')
assignment=next(n for n in func.body if isinstance(n,ast.Assign) and isinstance(n.targets[0],ast.Name) and n.targets[0].id=='types')
assert ast.dump(assignment.value)==ast.dump(ast.parse('tuple(product((0,1),repeat=topics))[1:]',mode='eval').body)
main=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='main');calls=[ast.unparse(n) for n in ast.walk(main) if isinstance(n,ast.Call)]
assert 'run_case(m, 3, 2)' in calls and 'run_case(6, 4, 1)' in calls and 'range(2, 7)' in calls
j=json.loads(by['copy_tax_three_topics_exact.json'].read_text());out=next(R/x['evidence_path'] for x in saved if x['from'].endswith('runs/exhaust_copy_tax_three_topics.stdout'));err=next(R/x['evidence_path'] for x in saved if x['from'].endswith('runs/exhaust_copy_tax_three_topics.stderr'))
assert json.loads(out.read_text())==j and err.read_bytes()==b''
rows=[]
for m,t,mult in [(m,3,2) for m in range(2,7)]+[(6,4,1)]:
 rec=next(x for x in j['results'] if x['m']==m and x['catalog_size']==t);types=2**t-1;scale=math.lcm(*range(1,m+1));assert rec['checked_instances']==(mult+1)**types-1
 assert rec['multiplicity_domain']==f'each of {types} nonempty interest types has count 0..{mult}; all-zero omitted'
 assert rec['scale']==scale and rec['status']=='NO_REFUTATION_IN_ENUMERATED_UNIVERSE' and rec['largest_gap_scaled']==0
 assert rec['maximum_count_states']==math.comb(m+t,t) and rec['maximum_root_terminal_counts']==math.comb(m+t-1,t-1)
 rows.append(dict(rec,interest_type_count=types,domain_formula=f'{mult+1}^{types}-1'))
r286=json.loads(by['counterexample_search_m6.json'].read_text());assert r286['p4_single_pair']['instances']==3**10-1 and r286['p4_single_pair']['minimum_ratio']=='8/11';assert r286['p3']['instances']==4**7-1
at=ast.parse(by['counterexample_search_m6.py'].read_text());assert 'masks = [1, 2, 4, 8, 3, 5, 9, 6, 10, 12]' in ast.unparse(at)
fail=next(R/x['evidence_path'] for x in saved if x['from'].endswith('runs/counterexample_search_m6.stderr'));assert "ModuleNotFoundError: No module named 'customer_attraction_search'" in fail.read_text()
ad=json.loads(by['exhaustive_k4_binary.json'].read_text());ast.parse(by['exhaustive_k4_binary.py'].read_text());assert ad['instances']==2**15-1 and ad['minimum_welfare_ratio']=='6/7';assert ad['script_sha256']==sha(by['exhaustive_k4_binary.py'])
before_after=json.loads((W/'formal-before-after.json').read_text());diffs=[];links=0
for x in before_after:
 old=R/x['before_path'];p=R/x['path'];assert sha(old)==x['before_sha256'];x['after_sha256']=sha(p)
 text=p.read_text();meta=yaml.safe_load(text.split('---',2)[1]);assert all(k in meta for k in ['id','kind','type_tag','title','status','summary','source_refs'])
 for target in re.findall(r'\[[^\]\n]+\]\(([^)\n]+)\)',text):
  if '://' in target or target.startswith('#'):continue
  assert (p.parent/target.split('#')[0]).resolve().exists(),target;links+=1
 diffs.append(''.join(difflib.unified_diff(old.read_text().splitlines(True),text.splitlines(True),fromfile='before/'+x['path'],tofile='after/'+x['path'],n=0)))
save(W/'formal-before-after.json',before_after);(W/'formal-changes.patch').write_text('\n'.join(diffs))
result={'passed':True,'domain_saved_record_checker_runs':1,'frozen_sources_size_SHA':len(M),'historical_records_size_SHA':len(saved),'R291_source_types_expression':ast.unparse(assignment.value),'R291_main_domain_calls':['run_case(m,3,2) for m in range(2,7)','run_case(6,4,1)'],'R291_all_six_results_checked':rows,'R291_stdout_JSON_equal':True,'R291_stderr_empty':True,'R291_historical_exit_evidence':'old README says exit0 and already-done program receipt says actual run; no separate argv/time/codeSHA execution receipt saved','R286_domain':'10 singleton/pair types count0..2 =>59048; welfare/OPT objective; old reproduction ModuleNotFoundError','R_ad571_domain':'15 all-nonempty binary types =>32767; welfare/OPT objective; minimum6/7; frozen script hash matches report','hypothetical_10_type_binary_not_original_main':2**10-1,'formal_YAML_files':2,'formal_local_links_checked':links,'original_scans_or_original_program_runs':0,'new_SPE_or_LP_or_BI_runs':0,'new_source_completions':0,'new_claim_or_done':0,'limitations':'Static AST/domain arithmetic and saved-output identity only; does not independently rerun all-SPE DP or exhaustive candidate/half scans.'}
save(W/'domain-and-record-check.json',result);save(E/'domain-and-record-check.json',result)
print(json.dumps({k:v for k,v in result.items() if k!='R291_all_six_results_checked'},ensure_ascii=False))
