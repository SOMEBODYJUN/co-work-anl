"""Source/link/structure and saved-scalar selfcheck; no game, solver, or LP run."""
from pathlib import Path
from fractions import Fraction as F
import hashlib,json,re
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[4]
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def check():
 m=read(HERE/'source-manifest.json');source_checks=[]
 assert len(m['sources'])==m['primary_source_count']==4
 assert sum(s['size'] for s in m['sources'])==m['primary_bytes']==25329
 assert len({s['preserved_as'] for s in m['sources']})==4
 for s in m['sources']:
  p=ROOT/s['preserved_as'];b=p.read_bytes()
  assert p.suffix=='.md' and len(b)==s['size'] and sha(p)==s['sha256']
  assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==s['blob']
  source_checks.append(dict(id=s['id'],size=len(b),sha256=s['sha256'],git_blob_matches=True))
 assert len(list((HERE/'original').rglob('README.md')))==3
 assert not list((HERE/'original').rglob('*.py'))
 comparisons=read(HERE/'comparison-and-relationships.json')['comparisons'];assert len(comparisons)==16
 for c in comparisons:
  p=ROOT/c['preserved_as'];assert p.stat().st_size==c['size'] and sha(p)==c['sha256'] and c['full_file_read'] is True
 scalars=read(HERE/'saved-scalar-binding.json');h,v,u,P,PO=[F(scalars[k]) for k in ('h','v','u','P','P_O')]
 assert u-(v-P)==F(scalars['F'])==F(21,4)
 assert max(v-u,F(0))==F(scalars['required_positive_price'])==F(21,2)
 gap=max(v-u-PO,F(0));assert gap==F(scalars['outside_O_price_lower_bound'])==F(3,4)
 assert h/v*gap==F(scalars['outside_O_flow_lower_bound'])==F(35,978)
 assert scalars['context']==[5,0] and scalars['m']==scalars['current_role_one_based']==3
 assert scalars['source_reported_histories']==43 and scalars['source_reported_comparisons_including_self']==258 and scalars['current_replay_calls']==0
 boundary=read(HERE/'execution-boundary.json')
 assert boundary['primary_sources_all_markdown'] is True
 assert all(boundary[k]==0 for k in ('current_original_entry_calls','current_source_imports','current_source_function_calls','current_SPE_BI_LP_discovery_calls'))
 objects=list((ROOT/'archives/customer-attraction/state').rglob('*.md'));assert len(objects)==4
 object_checks=[]
 for p in objects:
  txt=p.read_text();front=txt.split('---',2)[1]
  for field in ('id:','kind:','type_tag:','title:','status:','truth_status:','review_level:','scope:','summary:','source_refs:'):assert field in front
  object_checks.append(dict(path=str(p.relative_to(ROOT)),frontmatter_fields_present=True))
 known={c['path'] for c in comparisons};missing=[];controls=[]
 for p in ROOT.rglob('*.md'):
  if 'original' in p.relative_to(ROOT).parts or 'comparison' in p.relative_to(ROOT).parts:continue
  b=p.read_bytes()
  if any(x<32 and x not in (9,10,13) for x in b):controls.append(str(p.relative_to(ROOT)))
  for link in re.findall(r'\]\(([^)]+)\)',b.decode()):
   if '://' in link or link.startswith('#'):continue
   q=(p.parent/link.split('#')[0]).resolve()
   try:rel=str(q.relative_to(ROOT))
   except ValueError:missing.append([str(p.relative_to(ROOT)),link]);continue
   if not q.exists() and q!=HERE/'verification.json' and rel not in known:missing.append([str(p.relative_to(ROOT)),link])
 assert not missing and not controls
 for row in m['payload']:
  p=ROOT/row['path'];assert p.stat().st_size==row['size'] and sha(p)==row['sha256']
 return dict(all_pass=True,source_fingerprints=source_checks,full_comparison_snapshots=len(comparisons),original_markdown_sources=4,distinct_README_paths=3,objects=object_checks,saved_scalar_equalities_checked=['F=u-(v-P)','required=(v-u)+','outsideO_gap=required-PO','outsideO_flow=(h/v)*gap'],scalar_source_is_historical_not_new_replay=True,payload_files_checked=len(m['payload']),missing_links=missing,control_character_files=controls,new_original_entry_import_source_function_SPE_BI_LP_discovery_calls=0,method='byte fingerprints, frontmatter, preserved snapshot identity, links, control characters, and four saved Fraction scalar identities only; no game reconstruction or parameter tests')
if __name__=='__main__':
 d=check();(HERE/'verification.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:v for k,v in d.items() if k not in ('source_fingerprints','objects')},ensure_ascii=False))
