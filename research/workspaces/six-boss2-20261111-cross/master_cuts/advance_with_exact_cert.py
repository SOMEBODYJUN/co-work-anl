#!/usr/bin/env python3
"""Run a reviewed new round through unchanged matrix engines and strict dual recovery.

Each attempt receives fresh log names. Existing exact points are never replaced.
"""
from pathlib import Path
import argparse,datetime,hashlib,json,os,platform,subprocess,sys,time
HERE=Path(__file__).resolve().parent
REPO=HERE.parents[3]

def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    stages=('prepare','solve','reconstruct','dual','verify')
    ap=argparse.ArgumentParser();ap.add_argument('config');ap.add_argument('--start',default='prepare',choices=stages);args=ap.parse_args();cp=Path(args.config).resolve();assert cp.is_relative_to(HERE)
    cfg=json.loads(cp.read_text());stem=cfg['stem'];start_index=stages.index(args.start)
    if start_index<=2:assert not (HERE/(stem+'_exact.json')).exists(),'Existing exact point must remain unchanged; use a new stem or resume at dual/verify.'
    reviews=[];basepoint=HERE/cfg['base_point'];base_sha=digest(basepoint)
    for rel in cfg.get('independent_review_reports',[]):
        p=REPO/rel;a=json.loads(p.read_text());assert a['status']=='PASS'
        ps=a.get('point_sha256',a.get('input_sha256'));assert ps==base_sha,(p,ps,base_sha)
        reviews.append({'path':rel,'sha256':digest(p),'input_point_sha256':ps,'pack_sha256':a['pack_sha256']})
    assert {r['pack_sha256'] for r in reviews}=={p['sha256'] for p in cfg['packs']}
    review_path=HERE/(stem+'_review_manifest.json')
    if not review_path.exists():review_path.write_text(json.dumps({'status':'PASS','reviews':reviews,'config_sha256':digest(cp)},indent=2)+'\n')
    started=time.time();stamp=datetime.datetime.now(datetime.timezone.utc).isoformat();records=[];success=False
    attempt=1
    while (HERE/(stem+f'_wrapper_attempt{attempt}.json')).exists():attempt+=1
    try:
        for stage in stages[start_index:]:
            command=([sys.executable,'-B',str(HERE/'scaled_dual.py'),str(cp)] if stage=='dual' else [sys.executable,'-B',str(HERE/'advance_master.py'),str(cp),stage])
            stdout=HERE/(stem+f'_{stage}_wrapper{attempt}.stdout.txt');stderr=HERE/(stem+f'_{stage}_wrapper{attempt}.stderr.txt')
            assert not stdout.exists() and not stderr.exists()
            print(json.dumps({'stage':stage,'event':'start','stem':stem}),flush=True);t=time.time()
            with stdout.open('w') as out,stderr.open('w') as err:result=subprocess.run(command,cwd=REPO,stdout=out,stderr=err)
            records.append({'stage':stage,'command':command,'exit_code':result.returncode,'elapsed_seconds':time.time()-t,'stdout':stdout.name,'stderr':stderr.name})
            print(json.dumps({'stage':stage,'event':'finish','exit_code':result.returncode,'seconds':time.time()-t}),flush=True)
            if result.returncode:raise SystemExit(result.returncode)
        success=True
    finally:
        report={'scope':'Execution wrapper only; exact mathematical certification is in the saved full primal/dual verifier report.','success':success,'command':[sys.executable,'-B',str(Path(__file__).resolve()),str(cp),'--start',args.start],'cwd':str(REPO),'started_utc':stamp,'elapsed_seconds':time.time()-started,'python':platform.python_version(),'script_sha256':digest(Path(__file__)),'config_sha256':digest(cp),'dependencies':{name:digest(HERE/name) for name in ('advance_master.py','scaled_dual.py','extend_master.py','merge_master.py')},'stages':records}
        (HERE/(stem+f'_wrapper_attempt{attempt}.json')).write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':main()
