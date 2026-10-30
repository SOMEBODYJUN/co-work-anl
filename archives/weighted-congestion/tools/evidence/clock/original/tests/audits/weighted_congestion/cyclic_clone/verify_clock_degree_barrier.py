"""Exact finite obstruction to degree-preserving anchored clock addition.
Only Python standard library. Costs are recomputed from literal incidences;
no solver output or compressed local-load formula enters the verification.
"""
from fractions import Fraction as F
from itertools import product,combinations
from hashlib import sha256
import json

WEIGHTS=[F(1),F(1,2),F(1,4),F(1,8)]
ALPHA=F(21,20)
BASE=[((0,0,1,1),F(1593928,421875)),((0,1,1,0),F(452978,421875)),((1,-1,-1,-1),F(23816,5859375)),((1,1,-1,-1),F(855968,17578125))]
BAD=(0,1,0,1)
DUALS=[(58,0,18,0,24),(70,0,10,10,10),(86,0,0,7,7),(44,0,28,0,28)]

SIMPLE_DUALS=[(3,0,0,0,1),(4,0,0,0,1),(3,0,1,0,1),(0,0,0,0,1)]

def costs(s,resources):
 result=[F() for _ in WEIGHTS]
 for degree,coefficient,actions in resources:
  users=[i for i,a in enumerate(actions) if a==s[i]]
  load=sum((WEIGHTS[i] for i in users),F())
  fee=coefficient*load**degree
  for i in users:result[i]+=fee
 return result

def flip(s,i):
 a=list(s);a[i]=1-a[i];return tuple(a)

def gain(s,i,resources):return costs(s,resources)[i]-ALPHA*costs(flip(s,i),resources)[i]

def main():
 base=[]
 for signature,coefficient in BASE:
  for side in (0,1):
   actions=tuple(-1 if x==0 else side if x==1 else 1-side for x in signature)
   base.append((3,coefficient,actions))
 cycle=[(0,0,0,0)]
 for step in range(8):cycle.append(flip(cycle[-1],step%4))
 cycle_gains=[gain(s,step%4,base)for step,s in enumerate(cycle[:-1])]
 assert all(x>0 for x in cycle_gains)
 assert cycle_gains[:4]==cycle_gains[4:]
 bad_pairs=[(costs(BAD,base)[i],costs(flip(BAD,i),base)[i])for i in range(4)]
 assert all(old<new for old,new in bad_pairs)
 columns=[base];labels=['base']
 for i,j in combinations(range(1,4),2):
  triple=(0,i,j);total=sum((WEIGHTS[k]for k in triple),F())
  for degree in range(4):
   res=[]
   for side in (0,1):
    acts=[-1]*4
    for k,p in zip(triple,(0,1,0)):acts[k]=side^p
    res.append((degree,1/total**degree,tuple(acts)))
   columns.append(res);labels.append({'triple':triple,'degree':degree})
 certificates=[]
 for i,dual in enumerate(DUALS):
  rows=[(cycle[j],j)for j in range(4)]+[(BAD,i)]
  G=[[gain(s,j,res)for res in columns]for s,j in rows]
  products=[sum((F(dual[k])*G[k][c]for k in range(5)),F())for c in range(len(columns))]
  assert all(x<0 for x in products)
  assert all(x>=0 for x in dual)and dual[-1]>0
  certificates.append({'off_player':i,'dual_integer_rows':list(dual),'dot_products':list(map(str,products)),'largest_dot_product':str(max(products))})
 simple_certificates=[]
 for i,dual in enumerate(SIMPLE_DUALS):
  rows=[(cycle[j],j)for j in range(4)]+[(BAD,i)]
  G=[[gain(s,j,res)for res in columns]for s,j in rows]
  products=[sum((F(dual[k])*G[k][c]for k in range(5)),F())for c in range(len(columns))]
  assert products[0]<0 and all(x<=0 for x in products[1:])
  simple_certificates.append({'off_player':i,'dual_integer_rows':list(dual),'dot_products':list(map(str,products)),'clock_max_by_triple':[str(max(products[1+4*j:5+4*j]))for j in range(3)]})
 # Every permitted resource pair and the base preserve simultaneous complement.
 for res in columns:
  for s in product((0,1),repeat=4):
   t=tuple(1-x for x in s)
   assert costs(s,res)==costs(t,res)
   for i in range(4):assert gain(s,i,res)==gain(t,i,res)
 out={'status':'all exact Fraction assertions passed','claim_scope':'This fixed base; anchor 0; complementary pair phase 010/101; same polynomial on both resources; independent nonnegative coefficients of degrees 0..3. No exclusion of higher degrees or other clocks.','alpha':str(ALPHA),'weights':list(map(str,WEIGHTS)),'base_pairs':[{'signature':sig,'x_cubed_coefficient':str(c)}for sig,c in BASE],'cycle_states':[''.join(map(str,s))for s in cycle],'cycle_gains':list(map(str,cycle_gains)),'off_state':''.join(map(str,BAD)),'off_state_cost_pairs':[[str(a),str(b)]for a,b in bad_pairs],'column_labels':labels,'certificates':certificates,'simple_certificates':simple_certificates,'dot_products_checked':sum(len(c['dot_products'])for c in certificates),'conclusion':'If original sweep edges 0 and 2 retain nonnegative alpha gain, every off-state gain at 0101 is strictly negative; 0101 and 1010 remain alpha-PNE.'}
 print(json.dumps(out,indent=2))

if __name__=='__main__':main()
