from fractions import Fraction
from itertools import product,combinations_with_replacement
import json,hashlib,sys
p=6;masks=list(range(1,1<<p));rho=(1,4,4,4,5,4)
def u(a,b,i,B):
    return Fraction(1,int(B>>a&1)+int(B>>b&1)) if ((B>>(a,b)[i])&1) else Fraction(0)
def cov(a,b,B):return int(bool(B>>a&1 or B>>b&1))
rows=[];labels=[]
for a,b in product(range(p),repeat=2):rows.append([2*(u(a,rho[a],1,B)-u(a,b,1,B)) for B in masks]);labels.append(('response',a,b))
for b in range(p):rows.append([2*(u(0,1,0,B)-u(b,rho[b],0,B)) for B in masks]);labels.append(('root',b))
rows.append([cov(2,3,B)*(1-cov(0,1,B))-cov(0,1,B) for B in masks]);labels.append(('cover-gap',))
for a,b in combinations_with_replacement(range(p),2):
 if (a,b)==(2,3):continue
 rows.append([cov(2,3,B)-cov(a,b,B) for B in masks]);labels.append(('omit',a,b))
y={('response',0,2):Fraction(18),('response',0,3):Fraction(18),('response',0,4):Fraction(4),('response',3,2):Fraction(2),('root',1):Fraction(4),('root',2):Fraction(4),('root',3):Fraction(6),('cover-gap',):Fraction(27),('omit',1,2):Fraction(22),('omit',1,3):Fraction(22)}
vec=[]
for j,B in enumerate(masks):
 col=sum(y.get(labels[i],0)*rows[i][j] for i in range(len(rows)))
 vec.append(col)
assert all(c<=1 for c in vec),(max(vec),[(B,c) for B,c in zip(masks,vec) if c>1])
print('dual objective',sum(y.get(labels[i],0)*(0 if i<42 else 1) for i in range(len(rows))))
print('max column',max(vec),'min slack',min(Fraction(1)-c for c in vec),'tight',sum(c==1 for c in vec))
print('column slacks',json.dumps({str(B):str(Fraction(1)-c) for B,c in zip(masks,vec)},sort_keys=True))
# exact primal candidate from source run
w={1:10,2:13,4:8,8:8,20:5,24:5,36:5,40:5,49:6,50:4,54:1,58:1}
assert sum(w.values())==71
sl=[sum(Fraction(w.get(B,0))*rows[i][j] for j,B in enumerate(masks))-(0 if i<42 else 1) for i in range(len(rows))]
assert all(s>=0 for s in sl),(min(sl),[(labels[i],s) for i,s in enumerate(sl) if s<0])
print('primal objective',sum(w.values()),'min slack',min(sl),'tight',sum(s==0 for s in sl))
obj={'source_sha256':hashlib.sha256(open('cleanup/workspaces/Boss7/current-batch/36628191e3d12eec94ce/source.py','rb').read()).hexdigest(),'rho':rho,'weights':w,'objective':sum(w.values()),'dual':[{"label":list(k),"multiplier":str(v)} for k,v in y.items()],'dual_objective':str(sum(y.get(labels[i],0)*(0 if i<42 else 1) for i in range(len(rows)))),'dual_column_max':str(max(vec)),'dual_column_min_slack':str(min(Fraction(1)-c for c in vec)),'dual_column_slacks':{str(B):str(Fraction(1)-c) for B,c in zip(masks,vec)},'primal_row_slacks':[{"label":list(labels[i]),"slack":str(s)} for i,s in enumerate(sl)],'source_ids':['36628191e3d12eec94ce'],'python':'3.12','note':'exact Fraction replay of constraints; dual proves LP lower bound 71 and primal integer witness attains it'}
json.dump(obj,open('cleanup/workspaces/Boss7/current-batch/36628191e3d12eec94ce/dual_certificate.json','w'),ensure_ascii=False,indent=2);open('cleanup/workspaces/Boss7/current-batch/36628191e3d12eec94ce/dual_certificate.json','a').write('\n')
