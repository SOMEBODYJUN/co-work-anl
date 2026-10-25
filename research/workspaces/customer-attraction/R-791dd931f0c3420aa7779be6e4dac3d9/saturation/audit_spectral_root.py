"""Independent exact reconstruction of maximal-root certificate residual spectra.

No author evaluator or LP/SPE solver is imported. Every permitted 5-bit branch
membership and optimum-index multiplicity 0..5 is checked. New universal rows
retain the minimum exact residual conditional on optimum multiplicity.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json,hashlib
HERE=Path(__file__).resolve().parent
CERTS=[
 ('old','80','71/5',{'s1':'1/2','s2':'1/2','s3':'1/2','s4':'5','last-opt':'1'}),
 ('O-envelope','89090/1753','29147/3506',{'s1':'8089/3506','s2':'9673/3506','s3':'9475/3506','s4':'4475/1753','third-last':'3960/1753','last-opt':'565/1753','two-O':'1188/1753'}),
 ('pair-envelope','50200/1753','4851/1753',{'s1':'43609/21036','s2':'9673/3506','s3':'9475/3506','s4':'4475/1753','third-last':'3960/1753','last-opt':'565/1753','two-pairs':'297/1753'}),
 ('third-source-A','3070/59','1009/118',{'s1':'279/118','s2':'1/2','s3':'345/118','s4':'185/59','last-opt':'15/59','two-O':'44/59'}),
 ('third-source-B','1800/59','187/59',{'s1':'1/2','s2':'279/118','s3':'345/118','s4':'185/59','last-opt':'15/59','two-O':'44/59'}),
 ('third-source-C','1665/59','613/236',{'s1':'1/2','s2':'1/2','s3':'345/118','s4':'185/59','last-opt':'15/59','two-O':'44/59'}),
 ('pair-envelope-2','678285/23888','64639/23888',{'s1':'73631/35832','s2':'65269/23888','s3':'16155/5972','s4':'61145/23888','third-last':'53325/23888','last-opt':'480/1493','two-pairs':'1013/5972'})]
def q(n,d):return F(n,d) if n else F(0)
def direct_rows(b,d):
    c,a2,a3,a4,a5=b;load=sum(b);u=[q(t,load) for t in b];p=c+a2+a3
    H=u[3]+u[4]+q(a4,(p+1)*(p+2))
    r={f's{i}':F(c-b[i]) for i in range(1,5)}
    r['third-last']=u[2]-q(a5,c+a2+3)
    r['last-opt']=5*u[4]-q(d,p+a4+1)
    r['two-O']=F(5,2)*H+q(p,p+1)-int(d>0)
    r['two-pairs']=10*H-q(d*(5-d),p+1)-q(d*(d-1),p+2)
    return r,u[0]

def main():
    records=[]
    for tag,B,C,weights in CERTS:
        B,C=F(B),F(C);weights={n:F(v) for n,v in weights.items()};assert min(weights.values())>=0
        residual={}
        for b in product((0,1),repeat=5):
            for d in range(6):
                rows,V=direct_rows(b,d)
                residual[b,d]=B*V-C*b[0]-int(d>0)-sum(weights[n]*rows[n] for n in weights)
        assert min(residual.values())>=0
        conditional=[[min(v for (b,dd),v in residual.items() if b[0]==c and dd==d) for d in range(6)] for c in range(2)]
        e=[min(conditional[c][d] for c in range(2)) for d in range(6)]
        if tag.startswith('third-source'):assert e==[F(3,59)*max(0,d-1) for d in range(6)]
        if tag=='old':assert e==[F(max(0,d-1),5) for d in range(6)]
        if tag=='O-envelope':assert e==[F(113,1753)*max(0,d-1) for d in range(6)]
        if tag in ('pair-envelope','pair-envelope-2'):
            alpha=F(297,35060) if tag=='pair-envelope' else F(1013,119440)
            assert e==[F(max(0,d-1),5)+alpha*max(0,d-1)*(4-d) for d in range(6)]
        exact=[(b,d,v-e[d]) for (b,d),v in residual.items()]
        assert min(v for b,d,v in exact)>=0
        records.append({'name':tag,'B':str(B),'C':str(C),'multipliers':{n:str(v) for n,v in weights.items()},'conditional_c_d':[[str(v) for v in row] for row in conditional],'e_d':list(map(str,e)),'minimum_enhanced_residual':str(min(v for b,d,v in exact)),'enhanced_zero_types':sum(v==0 for b,d,v in exact),'checked_types':len(residual)})
    ans={'status':'passed-independent-coefficient-reconstruction','scope':__doc__,'new_statement':'For d_x=number of optimal five indices covering x, OPT_5 + sum_x e(d_x) <= B*u1 - C*K; K=max topic size.','records':records}
    HERE.joinpath('audit_spectral_root.json').write_text(json.dumps(ans,indent=2)+'\n')
    print(json.dumps(ans,indent=2))
if __name__=='__main__':main()
