"""Materialize only declared frozen bytes. No mathematical function executes."""
from pathlib import Path
import argparse,json,hashlib,shutil
E=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--runtime',type=Path,required=True);a=p.parse_args();repo=a.repo.resolve();runtime=a.runtime.resolve();runtime.mkdir(parents=True,exist_ok=False)
 stage=next((p for p in E.parents if p.name=='deliverables'),None) or repo
 copied={}
 for z in json.loads((E/'source-manifest.json').read_text()):
  source=stage/z['preserved_repo_path']
  if not source.exists():source=repo/z['preserved_repo_path']
  assert source.stat().st_size==z['size'] and sha(source)==z['sha256'];target=runtime/z['path'];target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(source,target);copied[z['path']]={'sha256':z['sha256'],'role':'A10 primary'}
 for z in json.loads((E/'runtime-dependencies.json').read_text())['prior_25_file_closure']:
  source=repo/z['repo_path'];assert sha(source)==z['sha256'];target=runtime/z['path']
  if target.exists():assert sha(target)==z['sha256']
  else:target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(source,target)
  copied.setdefault(z['path'],{'sha256':z['sha256'],'role':'related prior dependency'})
 for rel,z in copied.items():assert sha(runtime/rel)==z['sha256']
 (runtime/'work.py').write_text('# Inert path-discovery marker only; no controller or stub module.\n')
 report={'copied':copied,'unique_frozen_files':len(copied),'prior_declared_closure':25,'mathematical_functions_executed':0,'marker':'work.py is comment-only and never executed'}
 (runtime/'runtime-preparation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k!='copied'}))
if __name__=='__main__':main()
