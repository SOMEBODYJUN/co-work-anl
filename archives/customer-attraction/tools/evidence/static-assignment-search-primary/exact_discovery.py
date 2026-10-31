"""Exact saved auxiliary witness replay; no optimizer/canonical game import."""
import argparse
import hashlib
import itertools
import json
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--root',type=Path,default=Path(__file__).resolve().parent);p.add_argument('--output',type=Path,required=True);args=p.parse_args()
source=args.root/'original/research/workspaces/customer-attraction/R-105f776c3e6d4a22bb7c380c5df8edc7/dynamic_exchange/probe_disjoint_assignment.json'
z=json.loads(source.read_text());F={frozenset(map(int,k.split(','))):v for k,v in z['F'].items()};P=tuple(range(6));second={int(k):v for k,v in z['second'].items()};last={tuple(map(int,k.split(','))):v for k,v in z['last'].items()}
assert set(F)=={frozenset(s) for k in (2,3) for s in itertools.combinations(P,k)}
assert all(type(v) is int and -10<=v<=10 for v in F.values())
assert set(second)==set(P) and all(second[a]!=a and second[a] in P for a in P)
assert set(last)==set(itertools.permutations(P,2)) and all(c in P and c not in h for h,c in last.items())
def f(s):return F.get(frozenset(s),0)
def finish(h):
 h=tuple(h)
 while len(h)<3:h+=(0 if not h else second[h[0]] if len(h)==1 else last[h],)
 return h
def pay(h,i):return f(h)-f(h[:i]+h[i+1:])
comparisons=[];histories=[]
for d in range(3):
 for h in itertools.permutations(P,d):
  histories.append(h);path=finish(h)
  for a in P:
   if a in h:continue
   dev=finish(h+(a,));slack=pay(path,d)-pay(dev,d);assert slack>=0;comparisons.append({'history':h,'action':a,'obey_path':path,'deviation_path':dev,'slack':slack})
actual=finish(());assert actual==(0,3,4)
u=tuple(pay(actual,i) for i in range(3));assert u==(-1,0,0)
assert (f((0,3,4)),f((0,4)),f((0,3)),f((3,4)))==(0,0,0,1)
def welfare(s):return 3*f(s)-sum(f(t) for t in itertools.combinations(s,2))
coverage=[{'support':s,'signed_welfare':welfare(s)} for s in itertools.combinations(P,3)];v=max(x['signed_welfare'] for x in coverage);opt=[x['support'] for x in coverage if x['signed_welfare']==v];assert opt==[(1,2,5)]
assign=[{'permutation':p,'signed_cost':sum(f(actual[:i]+(a,)+actual[i+1:])-f(actual[:i]+actual[i+1:]) for i,a in enumerate(p))} for p in itertools.permutations((1,2,5))];assert min(x['signed_cost'] for x in assign)>=0
report={'status':'exact saved auxiliary discovery witness replay; not full CAG or MILP optimality certificate','source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'all_F_count':len(F),'nonzero_F_count':sum(v!=0 for v in F.values()),'F_l1':sum(abs(v) for v in F.values()),'fresh_histories':len(histories),'fresh_action_checks_including_self':len(comparisons),'min_IC_slack':min(c['slack'] for c in comparisons),'actual':actual,'actual_signed_utilities':u,'actual_signed_welfare':sum(u),'target_signed_welfare':v,'unique_target':opt,'all_twenty_supports':coverage,'all_six_assignments':assign,'all_156_IC_checks':comparisons,'no_new_MILP_execution':True}
args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'status':'PASS','fresh_histories':len(histories),'fresh_action_checks':len(comparisons),'target':opt,'min_static_cost':min(x['signed_cost'] for x in assign)}))
