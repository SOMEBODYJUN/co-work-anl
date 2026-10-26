"""Independent exhaustive integer check of sparse six-branch elimination."""
from pathlib import Path
import sys,json
import numpy as np
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
import joint_copy_price as p

def run():
    rng=np.random.default_rng(560364)
    edges=[('B','D3'),('B','C'),('C','E'),('B','D'),('D','E'),('D2','E'),('C','D2'),('D3','E')]
    edges=[tuple(x for x in p.ORDER if x in e) for e in edges]
    un={s:rng.integers(-7,8,size=(6,64,len(p.c.STATES[s]))) for s in p.ORDER}
    pairs={e:rng.integers(-7,8,size=tuple(len(p.c.STATES[s]) for s in e)) for e in edges}
    values,records=p.maxjoint(un,pairs);checks=[]
    dom=tuple(len(p.c.STATES[s]) for s in p.ORDER)
    for d,m in [(0,0),(1,27),(5,63)]:
        arr=np.zeros(dom,dtype=np.int64)
        for s,a in un.items():
            shape=tuple(len(p.c.STATES[t]) if t==s else 1 for t in p.ORDER);arr+=a[d,m].reshape(shape)
        for e,a in pairs.items():
            shape=tuple(len(p.c.STATES[t]) if t in e else 1 for t in p.ORDER);arr+=a.reshape(shape)
        target=int(arr.max());assert values[d,m]==target
        rec=p.recover(records,d,m);indices=tuple(p.c.STATES[s].index(tuple(rec[s])) for s in p.ORDER)
        assert arr[indices]==target
        checks.append({'d':d,'menu':m,'maximum_integer':target,'recovered_value_integer':int(arr[indices])})
    out={'status':'passed','scope':__doc__,'independent_exhaustive_states_per_case':int(np.prod(dom)),'checks':checks}
    (HERE/'audit_joint_factor.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':run()
