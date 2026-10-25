"""Exact arithmetic for the author weighted root-saturation proof candidate."""
from fractions import Fraction as F
from pathlib import Path
import json

WEIGHTS=[(F(0),F(0),F(0),F(1)),(F(0),F(0),F(1,7),F(6,7)),
         (F(0),F(14,203),F(27,203),F(162,203)),
         (F(28,637),F(42,637),F(81,637),F(486,637))]
PAIRS=[(F(80),F(71,5)),(F(70),F(423,35)),
       (F(1920,29),F(11393,1015)),(F(5840,91),F(2627,245))]

def run():
    records=[];ts=(4,3,2,1)
    for lam,pair in zip(WEIGHTS,PAIRS):
        assert sum(lam)==1 and min(lam)>=0
        c=sum(t*x for t,x in zip(ts,lam))
        aa=[F(3,4)*ts[j]*lam[j]+sum(lam[i]/(ts[i]+1) for i in range(j+1,4)) for j in range(4)]
        a=max(aa);B=5*c+100*a;C=20*a+c/5-1
        assert (B,C)==pair and C>0
        records.append({'lambda':list(map(str,lam)),'a_j':list(map(str,aa)),
                        'a':str(a),'c':str(c),'B':str(B),'C':str(C)})
    result={'status':'passed','scope':__doc__,'records':records}
    Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':run()
