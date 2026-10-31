from pathlib import Path
import hashlib,json,subprocess,sys
ROOT=Path(__file__).parent; SRC=ROOT/'source'; REP=ROOT/'replay'; checks=[]
def ck(n,ok,d=''):
 checks.append({'name':n,'passed':bool(ok),'detail':d})
 if not ok: raise AssertionError(n+': '+d)
exp={'two_player_closure_certificate.py':('97d54543c818784dc7a5',2007,'2e3f72236cfd39272abc1e16a22a29a4937a12fed924019459d50b078896b02b'),'two_player_full_closure_certificate.py':('2c9be9ee6595c5f0531d',2013,'275a8ca2938ba0b6e6949b404f0f0408a79383507709ae550340abc24a32f5c7'),'whole_gap_cone_walk.py':('01e00a94dcb2d744c30b',3601,'7fcfa829eb2237212558fc117c23841ff969f2453a363e41ce22aa63f3bb595c')}
for n,(sid,size,sha) in exp.items():
 b=(SRC/n).read_bytes(); ck('source:'+sid,len(b)==size and hashlib.sha256(b).hexdigest()==sha,f'{n} {len(b)} {hashlib.sha256(b).hexdigest()}')
 r=subprocess.run([sys.executable,'-m','py_compile',str(SRC/n)],capture_output=True,text=True); ck('compile:'+n,r.returncode==0,r.stderr)
for n in ['closure-d2.stdout','full-d2.stdout','full-residual-d2.stdout']:
 t=(REP/n).read_text(); ck('lp:'+n,'infeasible' in t and (REP/n.replace('.stdout','.stderr')).read_text()=='',t.strip())
g=(REP/'gap-smoke.stdout').read_text(); ck('probe-smoke','done' in g and "'best': 0.0" in g and (REP/'gap-smoke.stderr').read_text()=='',g.strip()); g6=(REP/'gap-q6k3-t3.stdout').read_text(); ck('probe-q6k3-smoke','done' in g6 and "'best': 0.0" in g6 and (REP/'gap-q6k3-t3.stderr').read_text()=='',g6.strip())
# Do not treat solver infeasibility or no-hit as a theorem.
ck('scope-boundary',True,'all runs are finite fixed templates or five-trial floating discovery')
out={'passed':True,'checks':checks,'scope':'finite template infeasibility and finite floating no-hit; no legal CAG or six-player theorem','lp_runs':['closure depth 2 whole','full depth 2 whole','full depth 2 residual'],'probe':['q=4,k=2,trials=5,seed=640130,best=0.0','q=6,k=3,trials=3,seed=640130,best=0.0']}
(ROOT/'validation.json').write_text(json.dumps(out,indent=2)+'\n'); print(json.dumps(out,indent=2))
