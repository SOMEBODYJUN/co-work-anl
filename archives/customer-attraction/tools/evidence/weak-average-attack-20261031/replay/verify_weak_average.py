from __future__ import annotations
from pathlib import Path
from math import comb, isfinite
import hashlib, json
BASE=Path(__file__).resolve().parents[1]
frozen=(BASE/'source/weak_average_attack.frozen.json').read_bytes()
replayed=(BASE/'replay/root/research/workspaces/customer-attraction/R-29b83efed6b045678e3b7ee11dffb7b3/strategic_relay/weak_average_attack.json').read_bytes()
assert frozen==replayed
report=json.loads(frozen)
assert report['candidate'].startswith('For each complete SPE')
expected={
 'root_tax':(4,6,259,1295,126,1.0,(0,1,1,1)),
 'actual_B':(4,6,259,1295,126,1.0,(0,2,2,2)),
 'individual_security':(3,6,43,215,56,1.5579710144927537,(1,4,5)),
 'portfolio_matching':(2,5,6,24,15,1.0,(0,3)),
}
checks=[]
for c in report['cases']:
 name=c['case']; n,k,h,r,p,g,T=expected[name]
 assert c['histories']==h and c['true_rows']==r and c['portfolios']==p
 assert c['portfolio']==list(T) and isfinite(c['best_gap']) and c['best_gap']>=0
 assert h==sum(k**ell for ell in range(n))
 assert r==h*(k-1)
 assert p==comb(k+n-1,n)
 assert len(c['weights'])==(1<<k)-1
 checks.append({'case':name,'histories':h,'true_rows':r,'portfolios':p,'best_gap':c['best_gap'],'best_portfolio':list(T),'nonnegative_gap':True})
# ensure no negative candidate was recorded in any case
assert all(c['best_gap']>=-1e-7 for c in report['cases'])
manifest={'status':'PASS','scope':'finite fixed-policy cone LP diagnostics; no universal SPE claim','byte_identical':True,'cases':checks,'negative_gap_observed':False,'formula_checks':'history and portfolio counts verified exactly','source_sha256':hashlib.sha256((BASE/'source/attack_weak_average.py').read_bytes()).hexdigest(),'frozen_sha256':hashlib.sha256(frozen).hexdigest()}
print(json.dumps(manifest,indent=2))
(BASE/'replay/verification.json').write_text(json.dumps(manifest,indent=2)+'\n')
