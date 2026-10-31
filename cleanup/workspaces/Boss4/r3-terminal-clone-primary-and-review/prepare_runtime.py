"""Local-only runtime assembly and explicitly derived inputs; no source fetching."""
from pathlib import Path
import hashlib,json

S=Path(__file__).resolve().parents[4]
E=S/'archives/customer-attraction/tools/evidence/terminal-clone-primary-and-review'
CF=S.parent/'r3-full-tree-milp-candidate-audits-primary'
CE=CF/'archives/customer-attraction/tools/evidence/full-tree-milp-candidate-audits-primary'
SUB=Path('research/workspaces/customer-attraction/R-18e993ca519949aba29e030d3d7b15b3')
def write(p,b):
    p.parent.mkdir(parents=True,exist_ok=True)
    if p.exists():assert p.read_bytes()==b,p
    else:p.write_bytes(b)
def js(p,x):write(p,(json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode())
primary=json.loads((E/'primary-manifest.json').read_text())['sources']
cf_sources=json.loads((CE/'source-manifest.json').read_text())
if isinstance(cf_sources,dict):cf_sources=cf_sources['sources']
aud=next(r for r in cf_sources if r['id']=='8542015b808290c371cf')
deps=json.loads((CE/'runtime-manifest.json').read_text())['sources']
runtime=[]
for r in [aud,*deps]:
    path=r['path'];source=CE/'original'/path;b=source.read_bytes()
    assert len(b)==r['size'] and hashlib.sha256(b).hexdigest()==r['sha256']
    write(E/'original'/path,b);write(E/'replay-tree'/path,b)
    runtime.append({**r,'role':'same-SHA-CF-runtime-code-not-primary',
       'local_origin':str(source),'saved_path':str((E/'original'/path).relative_to(S)),
       'verified_before_execution':True})
for r in primary:
    if r['path'].endswith(('.py','terminal_exact_audit.json')):
        write(E/'replay-tree'/r['path'],(S/r['saved_path']).read_bytes())
raw=json.loads((E/'original'/SUB/'next_boss/terminal_exact_audit.json').read_text())
derived=[]
for i,report in enumerate(raw):
    rec=report['records'][0];inst=rec['instance']
    value={'parameters':{'players':inst['players'],'topics':len(inst['topics']),
            'player':rec['normalized_player'],'objective':'terminal'},
           'results':[{'portfolio':rec['portfolio'],'actions':rec['strategy']['actions']}]}
    path=SUB/'next_boss'/('derived_terminal_fixed_graph_'+str(i)+'.json')
    data=(json.dumps(value,indent=2)+'\n').encode();write(E/'derived-inputs'/path.name,data);write(E/'replay-tree'/path,data)
    derived.append({'path':str(path),'size':len(data),'sha256':hashlib.sha256(data).hexdigest(),
       'source_primary_id':'c3b51b85f6e91bfcadc2','source_sha256':next(x['sha256'] for x in primary if x['id']=='c3b51b85f6e91bfcadc2'),
       'source_pointer':f'/{i}/records/0','role':'new-derived-fixed-graph-input-not-historical-MIP',
       'copied_fields':['instance.players','len(instance.topics)','normalized_player','portfolio','strategy.actions'],
       'explicit_new_field':'parameters.objective=terminal',
       'omitted_historical_material':'No original terminal MIP JSON was supplied here; no old numerical types/status/limit/timing/bound reconstructed.'})
js(E/'runtime-manifest.json',{'runtime_code_dependencies':6,'runtime_dependency_bytes':sum(r['size'] for r in runtime),'sources':runtime})
js(E/'derived-inputs/manifest.json',{'inputs':derived,'historical_terminal_MIP_inputs_replayed':False,'all_fields_read_before_run':True})
print(json.dumps({'runtime_code_dependencies':len(runtime),'bytes':sum(r['size'] for r in runtime),'derived_inputs':len(derived)}))
