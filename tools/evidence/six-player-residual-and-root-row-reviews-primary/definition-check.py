from fractions import Fraction as F
from itertools import product
import json

def enc(x):
 if isinstance(x,F):return str(x)
 if isinstance(x,dict):return {k:enc(v) for k,v in x.items()}
 if isinstance(x,(list,tuple)):return [enc(v) for v in x]
 return x

BASE={'P0':('T','A','B','C','D','E'),'P1':('T','E','F','G','H','I'),'P2':('T','A','E','J','K1','L'),'P3':('T','A','B','E','M','N')}
FIRST={'P0':1,'P1':2,'P2':3,'P3':4,'QI':2,'QL':3,'QD':3}
EDGES=[('P0','P1',1,'P0',5),('P0','P2',2,'P0',5),('P0','P3',3,'P0',5)]
def graph(mode):
 paths=dict(BASE);edges=list(EDGES)
 if mode=='QI':paths['QI']=('T','I','U','V','W','X');edges.append(('P0','QI',1,'P1',5))
 if mode=='QL':paths['QL']=('T','A','L','U','V','W');edges.append(('P0','QL',2,'P2',5))
 if mode=='QD':paths['QD']=('T','E','D','U','V','W');edges.append(('P1','QD',2,'P0',4))
 if mode=='JOINT':
  paths['QL']=('T','A','L','U','V','W');paths['QD']=('T','E','D','X','Y','Z')
  edges += [('P0','QL',2,'P2',5),('P1','QD',2,'P0',4)]
 for src,dst,i,labelpath,labeli in edges:
  assert paths[src][:i]==paths[dst][:i] and paths[dst][i]==paths[labelpath][labeli]
  assert i>=FIRST[src] and FIRST[dst]==i+1
 labels=sorted({x for p in paths.values() for x in p});k=len(labels)
 for name,p in paths.items():
  assert len(p)==6 and FIRST[name]<=4
  for i in range(FIRST[name],6):
   assert 6-i==1+len(p[i+1:]) # Safety denominator b+(current+future).
 genuine=sum(6-FIRST[name] for name in paths)
 rawrows=(k-1)+len(edges)+genuine*k+2*len(paths)
 return dict(name=mode,paths=paths,copy_edges=edges,first_genuine={name:FIRST[name] for name in paths},labels=k,literal_coefficient_types=2**k,safety_positions=genuine,explicit_unmerged_all_label_rows=rawrows,semantic_contract_only=True)

def main():
 gs=[graph(m) for m in ['BASE','QI','QL','QD','JOINT']]
 assert [g['labels'] for g in gs]==[15,19,18,18,21]
 assert [g['literal_coefficient_types'] for g in gs]==[32768,524288,262144,262144,2097152]
 assert gs[0]['explicit_unmerged_all_label_rows']==235
 assert sum(g['literal_coefficient_types'] for g in gs[:4])==1081344
 products={}
 for tau,expect in [(F(9,2),F(2122129,4782969)),(F(6),F(2352949,6718464))]:
  val=F(1)
  for r in range(1,7):val*=1-F(1,r)/tau
  val=1-val;assert val==expect and val<F(1,2);products[str(tau)]=val
 K=F(1999677999176384741339804233494917,8688875233423373354548736090657824)
 r=F(12304576977669022252980566479245,271527351044480417329648002833057)
 rows={'BASE':(F(62599453,5000000000),F(1431698969,10000000000)),'QI':(F(31340849,2500000000),F(286274429,2000000000)),'QL':(F(62825167,5000000000),F(286165527,2000000000)),'QD':(F(31363073,2500000000),F(71556517,500000000)),'JOINT':(F(31473521,2500000000),F(1430288409,10000000000))}
 residuals={name:r-a-b*K for name,(a,b) in rows.items()};assert all(x<0 for x in residuals.values())
 assert residuals['JOINT']==-F(16529619602329293769924215629617055430269,86888752334233733545487360906578240000000000)
 W=F(11563846740120540563650285979166203,24234087715908087797320314905948740);assert 0<W<F(1,2)
 # Counts of independent d,ell versus feasible (d,ell,h) membership summaries.
 triples=[(d,l,h) for d,l,h in product(range(7),repeat=3) if max(0,d+l-6)<=h<=min(d,l)]
 assert len(triples)==84
 contain=sum(1 for e in product([0,1],repeat=4) for a in [0,1] if not a or e[2]==e[3]==1)
 three=sum(1 for e in product([0,1],repeat=4) for a in [0,1] if not a or sum(e)>=3)
 counts=dict(two_early_independent=contain*2*49,two_early_with_h=contain*2*84,threefold_independent=three*2*49,threefold_with_h=three*2*84)
 assert counts==dict(two_early_independent=1960,two_early_with_h=3360,threefold_independent=2058,threefold_with_h=3528)
 return dict(status='PASS-fixed-contracts-counts-and-scalar-arithmetic-only',new_definition_check_runs=1,original_program_entries=0,old_full_audits_repeated=0,graphs=gs,baseline_old_row_count=235,old_merged_domain_count=1081344,prefix_products=products,given_old_point=dict(O=1,K=K,r=r,row_residuals=residuals),given_augmented_point=dict(O=1,W=W,half_gap=2*W-1),conditional_certificate_domain_counts=counts,coefficient_domain_residuals_verified=False,certificate_nu_inputs_available=False,tau6_Farkas_weights_verified=False,augmented_3894_constraints_verified=False,full_SPE_verified=False,scope='literalgraphsourcecontractsandgivenrationalnumbers;notreplayofwholecoefficientauditsorfeasibilityorSPE')

if __name__=='__main__':print(json.dumps(enc(main()),ensure_ascii=False,indent=2))
