"""Parent's independent seven-row projection reconstruction (known weights).

No author code or output imported.  Exact original IC/tax row contributions
are constructed explicitly, then all hidden bits are eliminated.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json

expected = [list(map(F,(0,960,1220,1480,1740,2000))),
            list(map(F,(0,"1665/4","2745/4","3785/4","4825/4","5865/4"))),
            list(map(F,(0,320,524,728,932,1136)))]
table=[]; states=[]
for p in range(3):
    row=[]
    for d in range(6):
        vals=[]
        for h,q,r in product((0,1),repeat=3):
            total=p+h+q+r
            div=lambda a: F(a,total) if a else F(0)
            VH,VQ,VR=map(div,(h,q,r))
            b=p+h
            # Remove common 17040*u + 1085*1_M - 2679*j/(p+3).
            G = -17040*VH
            G += 9000*F(h-q,p+3)+10080*F(h-r,p+3)
            G += 600*(5*VR-F(d,p+h+q+1))
            G -= 1085*h
            G += 360*(5*(VQ+VR+F(q,(b+1)*(b+2)))
                      -F(5*r+d-2*r*d,b+1)-F(2*r*d,b+2))
            G += 2679*F(5*h,p+3)
            assert -expected[p][d]-G>=0
            vals.append(G)
            states.append({"p":p,"d":d,"hidden":[h,q,r],
                           "residue":str(-expected[p][d]-G)})
        value=-max(vals)
        assert value==expected[p][d]
        row.append(str(value))
    table.append(row)
report={"status":"PASS","states":len(states),"F":table,
        "review":"parent independent reconstruction with known seven weights; not blind",
        "scope":"arbitrary genuine third-position history, any bare maximum M, any two five-topic menus",
        "residues":states,"limitation":"Necessary auxiliary inequality; no HALF5 certificate."}
Path(__file__).with_suffix('.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='residues'}))
