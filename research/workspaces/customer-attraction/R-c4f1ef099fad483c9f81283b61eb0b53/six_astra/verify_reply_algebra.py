"""Independent Fraction checks of every local new-reply coefficient identity."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json
import new_reply_budget as n

def frac(q,d):return F(q,d) if q else F()

def main():
    cases=0
    for a in product((0,1),repeat=6):
        p=sum(a[:3]);ell=sum(a[:5]);s=sum(a)
        for fam,(t,b,c),y,r in product(range(2),n.PAT,range(2),range(2)):
            key=(fam,p,ell,t,b,y);off=5+fam*n.NF
            queries=(b,c,t,F(3,6),*a,F(2,6),F(4,6))
            vb=frac(b,p+t+b+c);vc=frac(c,p+t+b+c)
            vr=frac(r,p+t+y+r)
            direct=[vb-frac(y,p+t+y+r)]
            direct += [vr-frac(q,p+t+y+1) for q in queries]
            direct += [vc-frac(r,p+t+b+1),frac(a[5],s)-frac(r,ell+1),-F(r)]
            atzero=[vb-frac(y,p+t+y)]
            atzero += [-frac(q,p+t+y+1) for q in queries]
            atzero += [vc,frac(a[5],s),F()]
            reconstructed=[v+r*n.delta(key).get(off+j,F()) for j,v in enumerate(atzero)]
            assert direct==reconstructed,(a,fam,t,b,c,y,r)
            cases+=1
    hcases=0
    for d in range(7):
        for hist in n.fp.HISTS[d]:
            words=[z for z,c in zip(n.PAT,hist) for _ in range(c)]
            for fam in range(2):
                literal={};compressed={}
                for i,(t,b,c) in enumerate(words):
                    for j,(_,bj,cj) in enumerate(words):
                        if fam==0 and i==j:continue
                        key=(t,b,(bj,cj)[fam]);literal[key]=literal.get(key,0)+1
                for ni,wordi in zip(hist,n.PAT):
                    for nj,wordj in zip(hist,n.PAT):
                        count=ni*nj-(ni if fam==0 and wordi==wordj else 0)
                        if count:
                            t,b,c=wordi;_,bj,cj=wordj
                            key=(t,b,(bj,cj)[fam]);compressed[key]=compressed.get(key,0)+count
                assert literal==compressed
                hcases+=1
    report={'status':'exact local coefficient and full histogram multiplicity identities verified; not a welfare proof','local_cases':cases,'histogram_family_cases':hcases,'reply_coordinates':'family,p,ell,t_i,b_i,y_j','source_rows':n.WP}
    Path(__file__).with_suffix('.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='source_rows'},indent=2))

if __name__=='__main__':main()
