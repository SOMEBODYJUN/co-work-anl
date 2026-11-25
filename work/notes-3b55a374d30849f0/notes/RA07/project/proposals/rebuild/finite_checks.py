from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json
out={'scope':'作者有限例子/代数检验；不证明无限基数、一般测度定理或视觉识读。','checks':[]}
def add(name,inputs,result,ok):
 assert ok,name
 out['checks'].append({'name':name,'inputs':inputs,'result':result,'passed':ok})
rows=[]
for N in [1,2,4,8]:
 L=sum(F(i,N)*F(1,N) for i in range(N));U=sum(F(i,N)*F(1,N) for i in range(1,N+1))
 assert U-L==F(1,N)
 rows.append({'N':N,'L':str(L),'U':str(U),'gap':str(U-L)})
add('f(x)=x的均匀Darboux和',{'interval':'[0,1]','partitions':[1,2,4,8]},rows,rows[0]['U']=='1' and rows[0]['L']=='0')
intervals=[(F(0),F(1))];rows=[]
for n in range(7):
 total=sum(b-a for a,b in intervals)
 assert len(intervals)==2**n and total==F(2,3)**n
 rows.append({'n':n,'count':len(intervals),'total_length':str(total)})
 intervals=[piece for a,b in intervals for piece in ((a,a+(b-a)/3),(b-(b-a)/3,b))]
add('Cantor有限阶段长度',{'initial':'[0,1]','operation':'各段删去中间三分之一','n_max':6},rows,True)
U=set(range(3));sets=[set(i for i in U if (mask>>i)&1) for mask in range(8)]
wrong=0;correct=0;parts=0
for A,V in product(sets,repeat=2):
 wrong+=A|V==A|(A-V)
 correct+=A|V==A|(V-A)
for A,B,T in product(sets,repeat=3):
 D=[T&A-(B),T&A&B,T&B-A,T-A-B]
 assert set.union(*D)==T
 assert all(not(D[i]&D[j]) for i in range(4) for j in range(i+1,4))
 assert D[0]|D[1]|D[2]==T&(A|B)
 parts+=1
add('原错差集式及正确式穷举',{'universe':[0,1,2],'pairs':64},{'wrong_formula_equal_cases':wrong,'correct_formula_equal_cases':correct,'counterexample':{'A':[],'V':[0],'A_union_V':[0],'A_union_A_minus_V':[]}},correct==64 and wrong<64)
add('三圆四块分解穷举',{'universe':[0,1,2],'triples':512},{'all_partition_identities_hold':parts},parts==512)
rows=[{'N':N,'sum':str(sum(F(1,2**k) for k in range(1,N+1))),'remainder':str(F(1,2**N))} for N in [1,2,3,10]]
add('epsilon分配的几何级数',{'terms':'1/2^k, k=1..N'},rows,all(F(r['sum'])+F(r['remainder'])==1 for r in rows))
add('Riesz球半径常数',{'R':'1','center_scale':'1/2','unit_separation_strictly_greater_than':'1/2','ball_radius':'1/8'},{'center_separation_lower_threshold':str(F(1,2)*F(1,2)),'two_radii':str(2*F(1,8)),'containing_radius_bound':str(F(1,2)+F(1,8))},F(1,4)==2*F(1,8) and F(5,8)<1)
p=Path(__file__).parent/'finite-check-input-output.json';p.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'checks':len(out['checks']),'all_passed':all(x['passed'] for x in out['checks']),'output':str(p)},ensure_ascii=False))
