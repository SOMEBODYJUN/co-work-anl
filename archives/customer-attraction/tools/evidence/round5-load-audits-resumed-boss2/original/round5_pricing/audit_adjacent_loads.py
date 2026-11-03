"""Exact independent audit: adjacent-load joint law from two marginals."""
from itertools import product
from pathlib import Path
import json
from audit_load_signature import comp

def reconstruct(a,b):
    xprev=0;out=[]
    for c,ac in enumerate(a):
        x=ac+xprev-b[c]
        if not 0<=x<=ac:return None
        out.extend((ac-x,x));xprev=x
    return tuple(out) if b[-1]==xprev else None

def run():
    histchecks=pairchecks=0;records=[]
    for m,q in product(range(2,7),range(6)):
        realized={}
        for h in comp(q,2*(m-1)):
            a=tuple(h[2*c]+h[2*c+1] for c in range(m-1));b=[0]*m
            for c in range(m-1):b[c]+=h[2*c];b[c+1]+=h[2*c+1]
            b=tuple(b);assert reconstruct(a,b)==h
            key=(a,b)
            if key in realized:assert realized[key]==h
            realized[key]=h;histchecks+=1
        n=0
        if q<=3:
            for a,b in product(comp(q,m-1),comp(q,m)):
                rec=reconstruct(a,b);assert (rec is not None)==((a,b) in realized)
                if rec is not None:assert rec==realized[a,b]
                n+=1;pairchecks+=1
        records.append({'m':m,'q':q,'unique_joint_laws':len(realized),'all_marginal_pair_checks':n})
    report={'scope':'Adjacent-load representation only; no welfare theorem','client_histogram_checks':histchecks,'all_marginal_pair_checks':pairchecks,'all_exact':True,'records':records}
    Path(__file__).with_suffix('.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k!='records'},indent=2))
if __name__=='__main__':run()
