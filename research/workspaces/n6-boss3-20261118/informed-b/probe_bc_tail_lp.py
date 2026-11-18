"""A necessary-condition relaxation for B/C three-player tails.
Not an original-model SPE test; arbitrary sets A,Y replace fixed catalogue labels.
"""
from itertools import product
from fractions import Fraction as F
import json
from pathlib import Path
import numpy as np
from scipy.optimize import linprog


def run(s,t):
    r=s-1
    types=[(block,e,a,y) for block in ('target','other','outside') for e,a,y in product((0,1),repeat=3)
           if block!='outside' or e or a or y]
    def row(fn):return np.array([float(fn(*v)) for v in types])
    def util(which,b,e,a,y):
        chosen={'A':a,'Y':y,'T':int(b=='target')}[which]
        return F(chosen,t*e+int(b=='target')+a+y) if chosen else F(0)
    UA=row(lambda *v:util('A',*v)); UY=row(lambda *v:util('Y',*v)); UT=row(lambda *v:util('T',*v))
    erow=row(lambda b,e,a,y:e)
    eother=row(lambda b,e,a,y:e*(b=='other'))
    etarget=row(lambda b,e,a,y:e*(b=='target'))
    Aeq=[row(lambda b,e,a,y:b=='target'),row(lambda b,e,a,y:b=='other')]
    beq=[1,r]
    Aub=[erow,etarget,row(lambda b,e,a,y:a),row(lambda b,e,a,y:y)]
    bub=[1,F(1,s),1,1]
    names=['E-size','target-E-at-most-average','A-size','Y-size']
    def ge(name,lhs,rhs=0):
        Aub.append(-lhs);bub.append(-rhs);names.append(name)
    ge('penultimate-anchor-deficit',UA+2*F(t,t+1)/r*eother,1)
    qothers=row(lambda b,e,a,y:F(1,t*e+a+1)/r if b=='other' else 0)
    ge('last-query-other-anchor-average',UY-qothers)
    qtarget=row(lambda b,e,a,y:F(1,t*e+a+2) if b=='target' else 0)
    ge('last-query-forced-anchor',UY-qtarget)
    qE=row(lambda b,e,a,y:F(e,t+int(b=='target')+a+1))
    ge('last-query-E',UY-qE)
    ge('last-universal-7/12',UY,F(7,12))
    qA=row(lambda b,e,a,y:F(a,t*e+int(b=='target')+a+1) if a else 0)
    ge('last-query-penultimate-action',UY-qA)
    z=linprog(UT,A_ub=np.array(Aub,dtype=float),b_ub=np.array(bub,dtype=float),
        A_eq=np.array(Aeq,dtype=float),b_eq=np.array(beq,dtype=float),bounds=(0,None),method='highs')
    return {'s':s,'t':t,'success':z.success,'objective':z.fun,
        'atoms':[{'type':list(v),'mass':float(x)} for v,x in zip(types,z.x) if x>1e-9],
        'rows':[{'name':n,'slack':float(v)} for n,v in zip(names,z.ineqlin.residual)],
        'scope':'Necessary relaxation only; no fixed shared catalogue actions, no complete SPE strategy.'}

if __name__=='__main__':
    print(json.dumps([run(4,1),run(5,2)],indent=2))
