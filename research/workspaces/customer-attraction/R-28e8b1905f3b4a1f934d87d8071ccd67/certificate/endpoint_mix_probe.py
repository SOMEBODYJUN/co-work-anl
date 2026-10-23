"""A bounded diagnostic of the unrestricted true one-deviation endpoint mixture.
The endpoints contain m players, including the deviator. It is not an m-1
opponent kernel and no positive finite result is a universal claim.
"""
import json
import sys
from fractions import Fraction as F
from pathlib import Path
import numpy as np
from scipy.optimize import linprog
ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT))
from customer_attraction import Instance, StrategyCertificate, verify_certificate


def solve(inst, actions):
    path=[]
    for i in range(inst.players): path.append(actions[tuple(path)])
    W=inst.welfare(inst.counts(path))
    ends={}
    for i in range(inst.players):
        for a in range(inst.topic_count):
            z=path[:i]+[a]
            while len(z)<inst.players: z.append(actions[tuple(z)])
            ends[(i,a)]=tuple(z)
    z_unique=sorted(set(ends.values()))
    mat=[]
    for z in z_unique:
        c=inst.counts(z)
        mat.append([sum((F(t.multiplicity,1+sum(c[b] for b in t.topics)) for t in inst.customers if a in t.topics),F(0)) for a in range(inst.topic_count)])
    A=np.array(mat,dtype=float)
    # max_p min_z A_z p, with simplex p.
    obj=np.r_[np.zeros(inst.topic_count),-1.]
    lp=linprog(obj,A_ub=np.c_[-A,np.ones(len(z_unique))], b_ub=np.zeros(len(z_unique)), A_eq=[np.r_[np.ones(inst.topic_count),0]],b_eq=[1],bounds=[(0,None)]*inst.topic_count+[(None,None)],method='highs')
    if not lp.success: raise RuntimeError(lp.message)
    return {'path':path,'welfare':W,'players':inst.players,'endpoints':len(z_unique),'value':-lp.fun,'budget':W/inst.players,'gap':-lp.fun-W/inst.players,'query':lp.x[:-1].tolist(),'terminal_matrix':[[str(v) for v in row] for row in mat],'terminals':[list(z) for z in z_unique]}


def main():
    out=[]
    for ep in sorted((ROOT/'examples/customer_attraction').glob('*.json')):
        cp=ROOT/'evidence/certificates/customer_attraction'/ep.name
        if not cp.exists(): continue
        try:
            inst=Instance.from_dict(json.loads(ep.read_text()))
            cert=StrategyCertificate.from_dict(json.loads(cp.read_text()))
            report=verify_certificate(inst,cert)
            report.assert_valid()
            r=solve(inst,cert.actions)
            r['instance']=str(ep.relative_to(ROOT)); r['certificate']=str(cp.relative_to(ROOT))
            out.append(r)
            print(ep.name,round(r['gap'],10),r['value'],r['budget'])
        except (KeyError,ValueError,TypeError,AssertionError) as e:
            print('SKIP',ep.name,str(e))
    (Path(__file__).with_suffix('.json')).write_text(json.dumps(out,indent=2)+'\n')

if __name__=='__main__': main()
