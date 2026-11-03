"""Independent Fraction check of five-player weighted-max hinge elimination.

No optimizer, source implementation, or strategy evaluator is imported.
This checks the complete allowed coefficient domain and finite breakpoints;
node legitimacy is established in weighted_hinge_independent_review.md.
"""
from fractions import Fraction as F
from pathlib import Path
import json

def endpoints(k):
    L=4*(k-1);out={F(0),F(L-1)}
    for p in range(6-k):
        for d in range(6):
            z=F(L-1)-F((k-1)*d,5*(p+1))
            if z>=0:out.add(z)
    return sorted(out)
def direct(p,k,d,c,t,h):
    # Coefficient excluding the common 5L*u term: BNSopt+t*menu cap.
    L=4*(k-1)
    return -5*(L-1)*F(h,p+k)-F(h*d,p+k)-F((1-h)*d,p+1)+t*(5*F(h,p+k)-F(c,p+k))
def cut(p,k,d,c,t):
    L=4*(k-1)
    return -t*F(c,p+k)-F(d,p+1)+max(F(0),F((k-1)*d-5*(L-1-t)*(p+1),(p+1)*(p+k)))
def run():
    elimination=interpolation=tail=source=0;reports=[]
    for k in range(2,6):
        ee=endpoints(k)
        for p in range(6-k):
            for d in range(6):
                for c in range(6):
                    for t in ee:
                        assert cut(p,k,d,c,t)==max(direct(p,k,d,c,t,h) for h in (0,1));elimination+=1
                    for a,b in zip(ee,ee[1:]):
                        assert cut(p,k,d,c,(a+b)/2)==(cut(p,k,d,c,a)+cut(p,k,d,c,b))/2;interpolation+=1
                    assert cut(p,k,d,c,F(4*(k-1)))>=cut(p,k,d,c,F(4*(k-1)-1));tail+=1
            for z in range(k-1):
                assert F(1,p+z+1)>=F(1,p+1)-F(z,(p+1)*(p+2))>=F(1,p+1)-F(k*z,2*(p+k));source+=1
        reports.append({'k':k,'L':4*(k-1),'breakpoints':list(map(str,ee))})
    out={'status':'passed','scope':__doc__,'elimination_states':elimination,'interpolation_states':interpolation,'tail_states':tail,'source_query_states':source,'families':reports}
    Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':run()
