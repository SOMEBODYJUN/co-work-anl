"""Only saved rational matrices/budget fields and record shapes; no model payoff/IC/LP."""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
import json,sys,hashlib
manifest_path,model_manifest_path,outpath=map(Path,sys.argv[1:]);manifest=json.loads(manifest_path.read_text());primary=manifest['rows']
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
before={x['id']:sha(Path(x['local_path'])) for x in primary};models={Path(x['path']).name:json.loads(Path(x['local_path']).read_text()) for x in json.loads(model_manifest_path.read_text())}
report=json.loads(Path(primary[1]['local_path']).read_text());exact=json.loads(Path(primary[3]['local_path']).read_text());checks=[]
for s in report['summaries']:
 w=s['worst'];g=models[s['name']];n=g['players'];k=len(g['topics']);b=w['prefix'];z=w['terminal'];C=w['coefficient']
 assert len(b)==len(z)==k and all(type(x) is int and x>=0 for x in b+z) and sum(b) in (0,1) and sum(z)==n and all(x<=y for x,y in zip(b,z))
 assert C==n+(n-sum(b))-1
 deleted=[a for a in range(k) if z[a]>b[a]];assert w['deleted']==deleted
 cols=[[F(x) for x in col] for col in w['query_prices']];a=list(map(F,w['ancestor_reserves']));lam=list(map(F,w['lambda']));rho=list(map(F,w['dual_rho']));B=F(w['actual_ancestor_profit'])
 assert len(cols)==len(a)==len(lam)==len(deleted) and all(len(col)==k for col in cols) and len(rho)==k
 assert min(lam)>=0 and sum(lam)==1 and min(rho)>=0 and sum(rho)==C and all(0<=x<=B for x in a)
 t=max(sum((lam[j]*cols[j][q] for j in range(len(cols))),F()) for q in range(k))
 upper=C*t+sum((lam[j]*a[j] for j in range(len(cols))),F())
 lower=min(a[j]+sum((rho[q]*cols[j][q] for q in range(k)),F()) for j in range(len(cols)))
 assert lower==F(w['lower']) and upper==F(w['upper']) and lower<=upper
 assert F(w['gap_lower'])==lower-2*w['W'] and F(w['gap_upper'])==upper-2*w['W'] and w['OPT_k'] is None
 checks.append(dict(name=s['name'],cases=s['cases'],displayed_matrix_columns=len(cols),displayed_query_coordinates=sum(map(len,cols)),stored_primal_dual_domains_legal=True,stored_upper_and_lower_reconstructed=True,stored_bounds_match=(lower==upper),stored_query_cap=str(t),stored_gap=str(lower-2*w['W']),ancestor_reserve_domain_legal=True,game_matrix_or_SPE_recomputed=False))
assert len(checks)==19 and sum(x['cases'] for x in checks)==716 and report['strict_failures']==[]
labels=exact['topics'];policy={tuple(x['history']):x['action'] for x in exact['policy']};histories=[h for d in range(exact['players']) for h in product(labels,repeat=d)]
assert len(policy)==len(exact['policy'])==43 and set(policy)==set(histories) and all(a in labels for a in policy.values())
assert exact['positive_depth_nodes']==42 and exact['comparisons_including_self']==252 and exact['min_slack']=='0'
assert sum(x['count'] for x in exact['types'])==exact['unit_customers']==14
assert sum(map(F,exact['actual_payoffs']))==exact['W']==9 and exact['half_margin']==2*exact['W']-exact['OPT_3']==4
assert all(F(col[2])==max(map(F,col))==F(exact['restricted_query_value'])==5 for col in exact['deletion_query_vectors'])
assert F(exact['J'])==exact['coefficient']*F(exact['restricted_query_value'])==20 and F(exact['violation'])==F(exact['J'])-2*exact['W']==2
assert F(exact['nonactual_budget'])==exact['coefficient']*max(map(F,exact['nonactual_query_vector']))==16 and F(exact['ancestor_reserve'])==0
assert max(map(F,exact['root_deviation_payoffs']))>F(exact['actual_payoffs'][0])==0
after={x['id']:sha(Path(x['local_path'])) for x in primary};assert before==after=={x['id']:x['sha256'] for x in primary}
out=dict(status='pass',scope='new stored-matrix rational dot products/primal-dual domain and bound equality/budget fields/43-node policy shapes only; no original entry/import/game-query/SPE/IC/LP/OPT evaluation',primary_sha256_before=before,primary_sha256_after=after,summary_records=len(checks),reported_cases=sum(x['cases'] for x in checks),unreported_cases=716-19,saved_worst_rows_only=True,matrix_columns=sum(x['displayed_matrix_columns'] for x in checks),query_coordinates=sum(x['displayed_query_coordinates'] for x in checks),all19_saved_bounds_match=all(x['stored_bounds_match'] for x in checks),exact_report_fields=len(exact),exact_policy_actions=43,exact_policy_positive_depth_nodes=42,checks=checks)
outpath.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps(out,ensure_ascii=False,indent=2))
