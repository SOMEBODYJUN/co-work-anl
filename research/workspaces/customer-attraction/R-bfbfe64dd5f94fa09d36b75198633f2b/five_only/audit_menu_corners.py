"""Exact-integer check of shared-menu corner pricing; no game search."""
from itertools import product
from random import Random
from pathlib import Path
import numpy as np,json

def audit():
    rng=Random(516);checks=0
    for d in range(6):
        domain=[(h+v,h) for h in range(d+1) for v in range(6-d)]
        corners=[(0,0),(d,d),(5-d,0),(5,d)]
        for _ in range(6):
            E=np.array([rng.randrange(-5,6) for _ in range(3)],dtype=np.int64)
            H=np.array([rng.randrange(-5,6) for _ in range(3)],dtype=np.int64)
            base=np.array([[rng.randrange(-9,10) for _ in range(16)] for _ in range(4)],dtype=np.int64)
            CE=np.array([[[rng.randrange(-4,5) for _ in range(3)] for _ in range(16)] for _ in range(4)],dtype=np.int64)
            def maximum(choices):
                pairs=np.array(list(product(choices,repeat=3)),dtype=np.int64)
                ell=pairs[:,:,0];hh=pairs[:,:,1];score=ell@E+hh@H
                for s in range(4):score+=np.max(base[s,None,:]+ell@CE[s].T,axis=1)
                return int(np.max(score))
            assert maximum(domain)==maximum(corners);checks+=1
    return {'scope':'Exact integer regression of shared-menu corner maximization; mathematical validity is convexity, not sampling','seed':516,'numpy':np.__version__,'checks':checks,'status':'passed'}
if __name__=='__main__':
    out=audit();Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
