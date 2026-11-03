"""five_direct's true penultimate-query envelope on all five root paths.

The extra row is root-local, hence adds no cross-family pricing dimension.
This module imports its mathematical contract from five_direct's derivation.
"""
from fractions import Fraction as F
from pathlib import Path
import json, hashlib
import numpy as np
from cross_root_last import Universe as CrossUniverse, RTYPES

TAUS=tuple(sorted({F(d,q) for d in range(6) for q in range(1,6)}))
NAMES={tau:'Root:penultimate-truequery-envelope:'+str(tau) for tau in TAUS}

def coefficient(state,d,tau=F(1,2)):
    t,x,y,z,k=state;p=t+x+y;total=p+z+k
    share=(F(5*z,total) if z else F())+(tau*F(k,total) if k else F())
    return share-F(d,p+1)+max(F(),F(d,(p+1)*(p+2))-tau*F(1,p+z+1))

def row(atom,exact=True,tau=F(1,2)):
    d=sum(atom['root_hist'][16:])
    ans=sum((n*coefficient(state,d,tau) for n,state in zip(atom['root_hist'],RTYPES)),F())
    return ans if exact else float(ans)

class Universe(CrossUniverse):
    def __init__(self):
        super().__init__()
        for tau,name in NAMES.items():
            self.names.append(name);self.root_names.append(name);self.root_name_set.add(name)
            # The inherited discovery pricer is floating; the authoritative
            # coefficient function above remains exact Fraction arithmetic.
            table=np.asarray([[float(120*coefficient(t,d,tau)) for t in RTYPES] for d in range(6)])
            local=np.zeros(len(self.root_engine.rh))
            for d,ids in enumerate(self.root_engine.rids):local[ids]=self.root_engine.rh[ids]@table[d]
            self.root_engine.local[name]=local
        original=self.root_engine.root_score
        def root_score(bits,weights,integer=False):
            own=[(n,v) for n,v in weights if n in NAMES.values()]
            rest=[(n,v) for n,v in weights if n not in NAMES.values()]
            key,const,co,E,H=original(bits,rest,integer)
            for name,value in own:co[name]=co.get(name,0)+value
            return tuple(sorted((n,v) for n,v in co.items() if v)),const,co,E,H
        self.root_engine.root_score=root_score

    def atom_rows(self,atom,exact=True):
        rr=super().atom_rows(atom,exact)
        for tau,name in NAMES.items():rr[name]=row(atom,exact,tau)
        return rr

if __name__=='__main__':
    table={str(tau):{''.join(map(str,t)):[str(coefficient(t,d,tau)) for d in range(6)] for t in RTYPES} for tau in TAUS}
    report={'scope':'Exact local coefficient table of imported true penultimate-query envelope; no welfare theorem',
            'parameters':list(map(str,TAUS)),'row_count':len(TAUS),'states_per_row':192,'coefficients':table,
            'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    Path(__file__).with_suffix('.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='coefficients'},indent=2))
