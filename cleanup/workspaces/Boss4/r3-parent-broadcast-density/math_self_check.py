"""Read-after-source mathematical checks, not another execution of either original audit."""
from pathlib import Path
from fractions import Fraction as F
import json
STAGE=Path(__file__).resolve().parents[4]
E=STAGE/'archives/customer-attraction/tools/evidence/parent-broadcast-density-primary'
parent=json.loads((E/'replay/parent-broadcast/captured-stdout-report.json').read_text())
inputs=json.loads((E/'fixture-input-index.json').read_text())['cases']
density_path=E/'replay/density-ledger/source-root/research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round5/dynamic/density_ledger_independent_audit.json'
density=json.loads(density_path.read_text())
assert parent['scalar_algebra_not_spe']['checks']==sum(n*4**(n-1) for n in range(1,7))==7737
assert parent['scalar_algebra_not_spe']['positive_cases']==sum(n*(4**(n-1)-3**(n-1)) for n in range(1,7))==5732
assert sum(len(r['all_original_policy_actions']) for r in inputs)==624
assert sum(r['complete_ic_checks'] for r in parent['cases'])==3641
subset_checks=0
for r in inputs:
 for a in r['all_original_policy_actions']:
  if any(a['action'] in t['topics'] and t.get('multiplicity',1)>0 for t in r['customer_types']):
   subset_checks+=2**(r['players']-len(a['history'])-1)
assert subset_checks==767
assert sum(r['all_positive_future_edges'] for r in parent['cases'])==18
assert all(r['fresh_positive_edges']==0 for r in parent['cases'])
for r in parent['cases']:
 for flow in r['flows'].values():assert F(flow['seed'])==F(flow['diagonal'])+F(flow['past_coupon'])==F(flow['signed_ledger'])
for r in density['reports']:
 M,H,T,C,L=map(F,(r['M'],r['H'],r['actual_return_T'],r['covariance_COV'],r['offhistory_slack_L']))
 assert F(r['diagonal_total'])==M-H
 assert F(r['K_incoming'])==M-H+T+C-L
 assert H>=0 and L>=0
raw=json.loads((E/'dependencies/examples/customer_attraction/portfolio_matching_failure.json').read_text())
types=[(set(t['topics']),t['multiplicity']) for t in raw['customers']]
def count(z,x):return sum(a in types[x][0] for a in z)
def pay(z,i):return sum((F(w,count(z,x)) for x,(likes,w) in enumerate(types) if z[i] in likes),F())
Z=(4,0);O=(1,3);old=(1,2);reset=(4,2);returned=(1,0);sourceD=(4,3)
R={x for x,(likes,_) in enumerate(types) if any(a in likes for a in O) and not any(a in likes for a in Z)}
owner={x:next(i for i,a in enumerate(O) if a in types[x][0]) for x in R}
sourceB={x for x in R if owner[x]==0};sourceDtypes={x for x in R if owner[x]==1}
Babs=sum((F(types[x][1],count(old,x)) for x in sourceB),F());Dabs=sum((F(types[x][1],count(sourceD,x)) for x in sourceDtypes),F())
incoming={x:F(1,count(old,x)) for x in sourceB if old[1] in types[x][0]}
full=[x for x,(likes,_) in enumerate(types) if reset[1] in likes]
D=pay(reset,1);v=pay(old,1);z=pay(returned,1);u=pay(Z,1)
a=sum((types[x][1]*f/count(reset,x) for x,f in incoming.items()),F());theta=a/D
J=sum((types[x][1]*f/count(old,x) for x,f in incoming.items()),F())
ef=sum((F(types[x][1],count(reset,x))/D*incoming.get(x,F()) for x in full),F())
er=sum((F(types[x][1],count(reset,x))/D*F(count(reset,x),count(old,x)) for x in full),F())
efr=sum((F(types[x][1],count(reset,x))/D*incoming.get(x,F())*F(count(reset,x),count(old,x)) for x in full),F())
C=-D*(efr-ef*er);T=theta*(u-z);L=theta*(v-z)
Ksrc=pay(Z,0)*Babs/pay(old,0)+u*Dabs/pay(sourceD,1);Kin=theta*u
HsrcB=sum((F(types[x][1],count(old,x)**2) for x in sourceB),F());HsrcD=sum((F(types[x][1],count(sourceD,x)**2) for x in sourceDtypes),F());Hin=sum((types[x][1]*f/count(reset,x)**2 for x,f in incoming.items()),F())
r=next(r for r in density['reports'] if r['case']=='portfolio_matching_failure')
for key,value in {'K_source':Ksrc,'K_incoming':Kin,'H':HsrcB+HsrcD+Hin,'diagonal_total':J,'actual_return_T':T,'covariance_COV':C,'offhistory_slack_L':L}.items():assert F(r[key])==value,(key,r[key],value)
assert (Babs,Dabs,a,theta,D,v,z,J,C,T,L)==tuple(map(F,('35/2','22','5/2','5/44','22','22','43/2','5/4','5/4','5/88','5/88')))
assert Ksrc+Kin-F(44)==F(29,38)
result={'scope':'Post-reading mathematical checks on saved input/report data only; neither original program was executed again.','parent_histories':624,'parent_IC_including_self':3641,'parent_scalar_checks':7737,'parent_scalar_positive':5732,'parent_fresh_future_subset_checks':subset_checks,'parent_local_all_positive_future_edges':18,'all_six_old_policies_have_zero_fresh_positive_edges':True,'three_density_global_identities':True,'portfolio_computed':{k:str(v) for k,v in {'source_B_absorbed':Babs,'source_D_absorbed':Dabs,'incoming_absorption':a,'theta':theta,'reset_D':D,'old_v':v,'return_z':z,'J':J,'E_mu_f':ef,'E_mu_r':er,'E_mu_fr':efr,'COV':C,'T':T,'L':L,'K_source':Ksrc,'K_incoming':Kin,'H':HsrcB+HsrcD+Hin,'K_minus_W':Ksrc+Kin-F(44)}.items()}}
Path(__file__).with_name('math-self-check-results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
