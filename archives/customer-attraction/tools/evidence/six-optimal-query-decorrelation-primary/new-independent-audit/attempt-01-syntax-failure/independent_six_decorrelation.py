"""New definition-level reconstruction from the two supplied Markdown specifications.
No original audit program, report, canonical game model or solver is imported.
One entry point checks both explicit six-player policies; all shares use 60 units.
"""
from pathlib import Path
from functools import lru_cache
from itertools import product,combinations_with_replacement
from fractions import Fraction as F
from collections import Counter
import argparse,json,hashlib,platform

def digest(b):return hashlib.sha256(b).hexdigest()
def frac(x):return str(x)
def check_model(data,mode,out):
 m=6;prefix=(6,7,8)if mode=='actual-banks'else(6,6,6);topics=9 if mode=='actual-banks'else7
 types=[(sum(1<<a for a in row['topics']),row['multiplicity'])for row in data['customers']]
 if mode=='actual-banks':types +=[(1<<a,18)for a in(6,7,8)]
 units=tuple(mask for mask,w in types for _ in range(w));assert len(units)==(88 if mode=='actual-banks'else34)
 themes=[frozenset(x for x,mask in enumerate(units)if mask>>a&1)for a in range(topics)];assert len(set(themes))==topics
 def counts(path):return tuple(path.count(a)for a in range(topics))
 @lru_cache(None)
 def compressed_pay(c):
  result=[0]*topics
  for mask,w in types:
   load=sum(c[a]for a in range(topics)if mask>>a&1)
   if not load:continue
   assert 60%load==0
   for a in range(topics):
    if c[a]and mask>>a&1:result[a]+=w*(60//load)
  return tuple(result)
 @lru_cache(None)
 def expanded_pay(c):
  # Distinct unit clients and a separate evaluator for the saved-table replay.
  result=[0]*topics
  for mask in units:
   present=[a for a,n in enumerate(c)if n and mask>>a&1];load=sum(c[a]for a in present)
   if not load:continue
   assert 60%load==0
   for a in present:result[a]+=60//load
  return tuple(result)
 def oldlast(a,b):return min(set(range(3)if b<3 else range(3,6))-{a,b})
 def prescribed(h):
  if mode=='actual-banks'and len(h)<3 and h==prefix[:len(h)]:return prefix[len(h)]
  if h==prefix:return 0
  if len(h)==4 and h[:3]==prefix:
   a=h[3]
   if a<6:return 3 if a<3 else0
   if mode=='actual-banks':return 3
  if len(h)==5 and h[:3]==prefix:
   a,b=h[3:]
   if a<6 and b<6:return oldlast(a,b)
   if mode=='actual-banks'and a>=6 and b==3:return 4
  return None
 policy={};overrides=Counter();construction_nodes=0
 def build(h):
  nonlocal construction_nodes
  if len(h)==m:return h
  construction_nodes+=1;i=len(h);ends=[build(h+(a,))for a in range(topics)];values=[compressed_pay(counts(z))[z[i]]for z in ends];best=max(values);a=prescribed(h)
  if a is None:a=next(a for a,v in enumerate(values)if v==best)
  else:assert values[a]==best,('prescribed_action_not_best',mode,h,a,values);overrides[i]+=1
  policy[h]=a;return ends[a]
 actual=build(())
 def follow(h):
  while len(h)<m:h=h+(policy[h],)
  return h
 decision_histories=nonself=all_actions=strict=tied=0
 for length in range(m):
  for h in product(range(topics),repeat=length):
   decision_histories+=1;a=policy[h];z=follow(h);value=expanded_pay(counts(z))[z[length]]
   assert compressed_pay(counts(z))==expanded_pay(counts(z))
   for b in range(topics):
    all_actions+=1;v=follow(h+(b,));other=expanded_pay(counts(v))[v[length]];assert value>=other,('not_SPE',mode,h,b,z,v,value,other)
    if b!=a:
     nonself+=1;strict+=value>other;tied+=value==other
 assert decision_histories==len(policy)==construction_nodes==(66430 if mode=='actual-banks'else19608)
 assert nonself==(531440 if mode=='actual-banks'else117648)and nonself==strict+tied
 def cover(t):return sum(any(mask>>a&1 for a in t)for mask in units)
 actual_u=[F(expanded_pay(counts(actual))[a],60)for a in actual];W=cover(actual)
 policy_path=out/(mode+'.policy.json');policy_path.write_text(json.dumps({','.join(map(str,h)):a for h,a in sorted(policy.items(),key=lambda z:(len(z[0]),z[0]))},separators=(',',':'))+'\n')
 def U(a,competition):
  total=0
  for mask in units:
   if mask>>a&1:
    load=sum(bool(mask>>x&1)for x in prefix)+1+sum(bool(mask>>x&1)for x in competition);assert 60%load==0;total+=60//load
  return total
 def Phi(pair):
  ans=0
  for mask in units:
   b=sum(bool(mask>>a&1)for a in prefix);extra=sum(bool(mask>>a&1)for a in pair)
   for k in range(1,extra+1):assert 60%(b+k)==0;ans+=60//(b+k)
  return ans
 def query(t):
  n=len(t);Bs=[policy[prefix+(a,)]for a in t];Cs=[policy[prefix+(a,b)]for a,b in zip(t,Bs)];matrix=[];I=J=R=0;pair_checks=0
  for j,a in enumerate(t):
   row=[]
   for l,aa in enumerate(t):
    B,C=Bs[j],Cs[j];Bp,Cp=Bs[l],Cs[l];chat=policy[prefix+(a,Bp)];lhs=U(a,(B,C))-U(a,(Bp,Cp));ell1=U(B,(a,C))-U(Bp,(a,chat));ell2=U(chat,(a,Bp))-U(Cp,(a,Bp));ret=U(C,(a,))-U(chat,(a,));potential=Phi((Bp,Cp))-Phi((B,C));assert ell1>=0 and ell2>=0 and lhs==ell1+ell2+ret+potential
    I+=ell1;J+=ell2;R+=ret;pair_checks+=1;row.append(str(F(U(a,(Bp,Cp)),60)))
   matrix.append(row)
  D=sum(F(U(a,(b,c)),60*n)for a,b,c in zip(t,Bs,Cs));ind=sum((F(x)for row in matrix for x in row),F(0))/(n*n);I,J,R=[F(x,60*n*n)for x in(I,J,R)];assert D-ind==I+J+R
  return dict(tuple=list(t),support_size=len(set(t)),coverage=cover(t),real_successor_pairs=[list(x)for x in zip(Bs,Cs)],diagonal_mean=str(D),independent_mean=str(ind),Delta=str(D-ind),first_successor_IC=str(I),cross_last_IC=str(J),deleted_middle_return=str(R),cross_query_matrix=matrix,exact_pair_identity_checks=pair_checks)
 if mode=='actual-banks':
  candidates=list(combinations_with_replacement(range(topics),6));Cmax=max(map(cover,candidates));best=[t for t in candidates if cover(t)==Cmax];assert len(candidates)==3003 and Cmax==88 and best==[(0,2,5,6,7,8),(1,2,5,6,7,8),(2,3,5,6,7,8),(2,4,5,6,7,8)];queries=[query(t)for t in best]
  assert actual==(6,7,8,0,3,4)and W==86 and actual_u==[F(18)]*3+[F(29,3),F(67,6),F(67,6)]
  assert [q['Delta']for q in queries]==['-11/72','-11/72','-1/9','-1/9']and queries[0]['first_successor_IC']=='5/36'and queries[0]['cross_last_IC']=='0'and queries[0]['deleted_middle_return']=='-7/24'
 else:
  Cmax=len(units);candidates=list(combinations_with_replacement(range(topics),3));best=[t for t in candidates if cover(t)==Cmax];queries=[query((0,2,2,5,5,5)),query((0,1,2,3,4,5))]+[query(t)for t in best];assert actual==(2,5,0,1,3,4)and W==Cmax==34 and len(best)==4
  assert queries[0]['Delta']=='-3/8'and queries[0]['diagonal_mean']=='29/3'and queries[0]['independent_mean']=='241/24'and queries[0]['first_successor_IC']=='3/8'and queries[0]['cross_last_IC']=='0'and queries[0]['deleted_middle_return']=='-3/4'
  assert queries[1]['Delta']=='0'and queries[1]['first_successor_IC']=='5/12'and queries[1]['cross_last_IC']=='1/4'and queries[1]['deleted_middle_return']=='-2/3'and all(q['Delta']=='-5/18'for q in queries[2:])
 return dict(mode=mode,unit_customers=len(units),distinct_valid_themes=topics,players=m,exact_integer_share_scale=60,policy_construction='complete ordered tree backward induction, min-label best reply except explicitly prescribed Markdown nodes; every prescribed node equality checked',prescribed_node_counts_by_depth=dict(overrides),full_decision_histories=decision_histories,all_action_comparisons_including_self=all_actions,nonself_deviations=nonself,strictly_losing_deviations=strict,tied_deviations=tied,source_actual_path=list(actual),actual_payoffs=list(map(str,actual_u)),welfare=W,OPT6=Cmax,actual_prefix=list(prefix),prefix_is_on_actual_path=actual[:3]==prefix,optimal_benchmark_multisets_enumerated=len(candidates),optimal_benchmark_budget=6 if mode=='actual-banks'else3,all_optimal_multisets=[list(t)for t in best],queries=queries,full_policy_file=policy_path.name,full_policy_sha256=digest(policy_path.read_bytes()),full_policy_bytes=policy_path.stat().st_size,limits='Finite explicit policies only, not all policies; original programs/reports unavailable and not rerun; no half/ROW/general-SPE claim')
def main():
 p=argparse.ArgumentParser();p.add_argument('--input',type=Path,required=True);p.add_argument('--output-dir',type=Path,required=True);a=p.parse_args();raw=a.input.read_bytes();assert digest(raw)=='bc5202502faa778fae402da4d74a4da8971ffa30bd712423147555b6e15a437a';data=json.loads(raw);a.output_dir.mkdir(parents=True,exist_ok=True)
 cases=[check_model(data,mode,a.output_dir)for mode in['offpath-empty','actual-banks']];payload=dict(provenance='new informed definition-level audit reconstructed only from supplied Markdown and original34-client input; no original audit or canonical solver import',python=platform.python_version(),own_source_sha256=digest(Path(__file__).read_bytes()),input_sha256=digest(raw),source_CLI_original_executions=0,new_independent_audit_processes=1,cases=cases,total_full_decision_histories=sum(x['full_decision_histories']for x in cases),total_nonself_deviations=sum(x['nonself_deviations']for x in cases),status='all exact definition-level checks passed');path=a.output_dir/'independent-audit.payload.json';path.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'status':payload['status'],'histories':payload['total_full_decision_histories'],'nonself':payload['total_nonself_deviations'],'cases':[{k:x[k]for k in['mode','source_actual_path','welfare','OPT6','full_decision_histories','nonself_deviations']}for x in cases]},ensure_ascii=False))
if __name__=='__main__':main()
