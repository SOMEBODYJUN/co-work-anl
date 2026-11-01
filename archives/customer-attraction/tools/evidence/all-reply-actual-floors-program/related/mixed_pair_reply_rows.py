"""Actual strongPAIR between every indexed new R/Z and old legal themes."""
from fractions import Fraction as F
from itertools import product
import old_query_reply_cuts as oq
KEYS=tuple((m,f,d,q) for m,(f,d),q in product(range(2),oq.GS,range(12)))
def query(q,a,wi,wj):return a[q] if q<6 else (tuple(wi)+tuple(wj))[q-6]
def rows(cols):
 out=[[F()]*len(cols) for _ in KEYS];hi=None
 for j,c in enumerate(cols):
  if c['kind']=='hist':
   hi=c;a=tuple(map(int,c['actual_bits']));whole=sum(a);pa=sum(a[:4]);D=(pa+1)*(pa+2)
   H=(F(a[4]+a[5],whole) if whole else F())+F(a[4],D);gs=oq.groups(c['hist'])
   for rr,(member,f,diag,qi) in zip(out,KEYS):
    v=(6 if diag else 30)*H
    for (ff,dd,wi,wj),count in gs.items():
     if (ff,dd)==(f,diag):v-=F(count*query(qi,a,wi,wj),pa+1)
    rr[j]=v
  elif c['kind']=='joint-reply':
   f,d,wi,wj=c['group'];ni=hi['hist'][oq.PAT.index(tuple(wi))];nj=hi['hist'][oq.PAT.index(tuple(wj))];count=ni if d else ni*nj-(ni if wi==wj else 0)
   a=tuple(map(int,hi['actual_bits']));pa=sum(a[:4]);D=(pa+1)*(pa+2)
   for rr,(member,ff,dd,qi) in zip(out,KEYS):
    if (ff,dd)==(f,d) and c['state'][member]:rr[j]=-count*(F(1,pa+1)-F(query(qi,a,wi,wj),D))
 return out
if __name__=='__main__':
 from pathlib import Path
 import json,sys
 point=json.loads(Path(sys.argv[1]).read_text());ys=[F(c['weight']) for c in point['columns']];s=[sum(x*y for x,y in zip(r,ys)) for r in rows(point['columns'])]
 print({'negative_rows':sum(v<0 for v in s),'minimum_slack':str(min(s)),'min_key':KEYS[s.index(min(s))]})
