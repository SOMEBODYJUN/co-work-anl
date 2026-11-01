from fractions import Fraction
from itertools import product
import hashlib, json
from pathlib import Path
source=Path(__file__).with_name('source.py')
p=5
masks=list(range(1,1<<p))
rho=(1,2,1,2,0)
actual=(4,0)
comparison=(1,3)
weights={2:Fraction(1,2),5:Fraction(1,2),8:Fraction(1,2),16:Fraction(1,2)}
def u(path,i,B):
    if not (B>>path[i])&1:
        return Fraction(0)
    return Fraction(1, sum((B>>a)&1 for a in path))
def out(first): return (first,rho[first])
rows=[]
row_names=[]
for a in range(p):
    for b in range(p):
        rows.append([u(out(a),1,B)-u((a,b),1,B) for B in masks])
        row_names.append({'player':1,'root_first':a,'deviation_second':b,'kind':'reply'})
for b in range(p):
    rows.append([u(actual,0,B)-u(out(b),0,B) for B in masks])
    row_names.append({'player':0,'actual':actual,'deviation_first':b,'kind':'root'})
slacks=[]
for name,row in zip(row_names,rows):
    value=sum(coef*weights.get(B,0) for B,coef in zip(masks,row))
    slacks.append({'row':name,'slack':str(value)})
C={B:int(any((B>>a)&1 for a in actual)) for B in masks}
R={B:int((not any((B>>a)&1 for a in actual)) and any((B>>a)&1 for a in comparison)) for B in masks}
W=sum(Fraction(C[B])*weights.get(B,0) for B in masks)
Rval=sum(Fraction(R[B])*weights.get(B,0) for B in masks)
assert W==1 and Rval==1 and min(Fraction(s['slack']) for s in slacks)>=0
ns_res=None
try:
    import runpy
    ns=runpy.run_path(str(source))
    ns_res=ns.get('res')
except Exception:
    ns_res=None
if ns_res is None:
    class Dummy: success=False; fun=float('nan'); message='not available'
    ns_res=Dummy()
out={
 'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
 'source_size':source.stat().st_size,
 'weights':{str(k):str(v) for k,v in weights.items()},
 'support_sets':{str(k):[i for i in range(p) if k>>i&1] for k in weights},
 'rows':len(rows),'minimum_spe_slack':str(min(Fraction(s['slack']) for s in slacks)),
 'zero_slack_rows':[s['row'] for s in slacks if s['slack']=='0'],
 'W':str(W),'R':str(Rval),'residual_C_minus_R':str(W-Rval),
 'actual_path':list(actual),'reply':list(rho),'comparison':list(comparison),
 'objective_support':{'C':{str(k):C[k] for k in weights},'R':{str(k):R[k] for k in weights}},
 'solver_float': {'success': bool(ns_res.success), 'objective_max': str(-float(ns_res.fun)), 'message': str(ns_res.message)},
 'source_output':json.loads(Path(__file__).with_name('run.json').read_text()),
}
Path(__file__).with_name('audit_exact.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(out,ensure_ascii=False,indent=2))
