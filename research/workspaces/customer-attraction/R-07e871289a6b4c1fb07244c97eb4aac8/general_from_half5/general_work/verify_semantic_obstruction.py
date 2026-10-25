"""Independent Fraction evaluation of the semantic necessary rows, without NPZ."""
import itertools,json,sys
from fractions import Fraction as F
from pathlib import Path
base=Path(__file__).parent;m=int(sys.argv[1])
raw=json.loads((base/f'cone{m}_exact_obstruction.json').read_text())
y={int(k):F(v) for k,v in raw['duals'].items()}
states=list(itertools.product(range(2),repeat=m+1));ns=len(states)
x=[y.get(j,F()) for j in range(ns)];K=y.get(ns,F());at=ns+1
def fr(a,b):return F(a,b) if a else F()
def u(a,j):return fr(a[j],sum(a))
def safe(a,j,q):return u(a,j)-fr(q,sum(a[:j])+m-j)
def hp(a):
    b=sum(a[:-2]);return u(a,m-2)+u(a,m-1)+fr(a[-2],(b+1)*(b+2))
def ev(fun):return sum((n*fun(st[:-1],st[-1]) for n,st in zip(x,states)),F())
rows={}
for i in range(m):
    rows[f'cap:A{i}']=K-ev(lambda a,o:a[i])
    for q in range(m):rows[f'actual:{i}:safe:A{q}']=ev(lambda a,o:safe(a,i,a[q]))
    rows[f'actual:{i}:safe:O']=ev(lambda a,o:m*u(a,i)-fr(o,sum(a[:i])+m-i))
rows['root:K']=m*ev(lambda a,o:u(a,0))-K
rows['actual:pairO']=ev(lambda a,o:F(m,2)*hp(a)-fr(o,sum(a[:-2])+1))
for i in range(m-1):
    zz=[]
    for st,n in zip(states,x):
        total=F()
        for h in itertools.product(range(2),repeat=m-i-1):
            mass=y.get(at,F());at+=1;total+=mass
            if mass:zz.append((st[:-1],st[-1],h,mass))
        assert total==n,(i,st,total,n)
    def evb(fun):return sum((n*fun(a,o,h) for a,o,h,n in zz),F())
    def p(a,h):return a[:i]+(a[-1],)+h
    rows[f'b{i}:copy']=evb(lambda a,o,h:u(a,i)-u(p(a,h),i))
    for j in range(i+1,m):
        rows[f'b{i}:cap:H{j}']=K-evb(lambda a,o,h:p(a,h)[j])
        for q in range(m):rows[f'b{i}:true:{j}:safe:A{q}']=evb(lambda a,o,h:safe(p(a,h),j,a[q]))
        for q in range(i+1,m):rows[f'b{i}:true:{j}:safe:H{q}']=evb(lambda a,o,h:safe(p(a,h),j,p(a,h)[q]))
        rows[f'b{i}:true:{j}:safe:O']=evb(lambda a,o,h:m*u(p(a,h),j)-fr(o,sum(p(a,h)[:j])+m-j))
        for g in range(m):rows[f'b{i}:global:{g}:H{j}']=evb(lambda a,o,h:u(a,g)-fr(p(a,h)[j],sum(a[:g])+m-g))
    if i<=m-3:
        rows[f'b{i}:pairO']=evb(lambda a,o,h:F(m,2)*hp(p(a,h))-fr(o,sum(p(a,h)[:-2])+1))
        for q in range(m):
            for r in range(q,m):
                rows[f'b{i}:pair:A{q}:A{r}']=evb(lambda a,o,h:hp(p(a,h))-
                    fr(a[q]+a[r],sum(p(a,h)[:-2])+1)+fr(a[q]*a[r],(sum(p(a,h)[:-2])+1)*(sum(p(a,h)[:-2])+2)))
assert at==max(y)+1 or at>max(y)
assert all(v>=0 for v in rows.values()),{k:str(v) for k,v in rows.items() if v<0}
W=ev(lambda a,o:int(any(a)));O=ev(lambda a,o:o)
assert W==1 and O==F(raw['ratio']) and O>2
out={'m':m,'status':'exact_semantic_template_obstruction','W':str(W),'O':str(O),'K':str(K),
     'gap':str(O-2*W),'rows_checked':len(rows),'minimum_necessary_row':str(min(rows.values())),
     'actual_profiles':{'%s:%d'%(''.join(map(str,st[:-1])),st[-1]):str(n) for st,n in zip(states,x) if n}}
(base/f'cone{m}_semantic_report.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
