from fractions import Fraction as Q
from itertools import combinations_with_replacement
n=6;s=7
B=[Q(2,42-5*t) for t in range(n-1)]+[Q(7,72)];A=[Q(1,12)]*n
pairs=list(combinations_with_replacement(range(s),2))
lam=[Q(33,98),Q(17,26),Q(38,55),Q(57,82),Q(0),Q(0)]
lam += [Q(0),Q(5,51),Q(5,51),Q(5,51),Q(5,51),Q(5,51),Q(9,44)]
lam += [Q(0)]*len(pairs)
# T01..T05
for idx,(a,b) in enumerate(pairs):
 if a==0 and 1<=b<=5:lam[n+s+idx]=Q(5,47)
# root R0 appended
lam += [Q(29,92)]
assert len(lam)==6+7+28+1
minimum=None;arg=None;count=0;neg=[]
for I in range(1,1<<s):
 for E in range(32):
  # all selected-max singleton customers covered somewhere on the actual path
  if I.bit_count()==1 and I not in (1,64) and not E:continue
  final=int(bool(I&1));J=E|(final<<5);z=J.bit_count();share=[Q((J>>t)&1,z) if z else Q() for t in range(n)]; floor=A if I.bit_count()==1 else B
  rows=[share[t]-floor[t] for t in range(n)]
  rows += [share[-1]-Q((I>>j)&1,E.bit_count()+1) for j in range(s)]
  h=(E&15).bit_count();d=(E>>4)&1
  rows += [share[-2]+share[-1]-(Q(((I>>a)&1)+((I>>b)&1),h+((I>>a)&1)+((I>>b)&1)) if (((I>>a)&1)+((I>>b)&1)) else Q())+Q(d,(h+1)*(h+2)) for a,b in pairs]
  rows += [share[0]-Q(I&1,6)]
  target=Q(int(bool(J)))- (Q(0) if I==64 else Q(1,2))
  res=target-sum(x*y for x,y in zip(lam,rows))
  if res<0:neg.append((I,E,J,res))
  if minimum is None or res<minimum:minimum,arg=res,(I,E,J)
  count+=1
print('count',count,'minimum',minimum,'arg',arg,'neg',len(neg),neg[:3])
