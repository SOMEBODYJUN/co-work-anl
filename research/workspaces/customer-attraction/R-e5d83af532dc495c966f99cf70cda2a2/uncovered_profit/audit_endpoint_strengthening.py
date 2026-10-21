"""Independent exact corner/table checks; general argument is in the note."""
from fractions import Fraction as F
from pathlib import Path
import json

def audit():
    checked=0;minimum=F(100);max_E_ratio=F(0)
    for p in range(81):
        for a in (0,1):
            for b in (0,1):
                f=F(p,p+a+b) if p else F(0)
                e=F(p-1,2*(p+1)*(p+2)) if a and b and p>=2 else F(0)
                cap=F(p,p+1) if p else F(a,4)
                assert cap-F(a,2*(p+2))<=f+e
                for tau in (F(1),F(5,4),F(3,2),F(2),F(7,2),F(5),F(11),F(100)):
                    for d in (F(0),F(1),tau):
                        for ell in (F(0),tau):
                            r=min(F(1),d)-d/(p+1)-ell/(2*tau*(p+a+1))+d*ell/(tau*(p+1)*(p+2))
                            slack=f+e-r+F(a,2*(p+2))
                            assert cap>=r
                            assert slack>=0
                            minimum=min(minimum,slack);checked+=1
                if e:
                    ratio=e/F(1,p+2);max_E_ratio=max(max_E_ratio,ratio)
                    for m in range(p+2,101):
                        assert ratio<=F(m-3,2*(m-1))
    return {'status':'exact finite audit passed; general proof separate','corner_cases':checked,'minimum_slack':str(minimum),'p_range':[0,80],'tau_values':['1','5/4','3/2','2','7/2','5','11','100'],'max_E_over_A_share_in_grid':str(max_E_ratio)}

if __name__=='__main__':
    result=audit();Path(__file__).with_name('endpoint_strengthening_audit.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
