"""Constructive target-counterexample probe by adding admissible topics.

Floating discovery only. The actual six actions/customer masses are preserved.
Every added topic respects all six actual safe quotes. At a selected bad
penultimate deviation it can be a new last reply blocking the deviator to u5.
Closure of the LAST TWO players would still not certify the first four.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import combinations
from math import comb
import argparse,json
import numpy as np
from scipy.optimize import linprog


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--steps',type=int,default=20);args=parser.parse_args()
    root=Path(__file__).parent
    data=json.loads((root/'potential_menu_joint_private.json').read_text())
    bits=[];mass=[]
    for (mask,d,ell,h),value in data['positive_types']:
        for subset in combinations(range(6),d):
            t=sum(1<<i for i in subset)
            reply=0 if ell==0 else (t if (ell,h)==(d,d) else (63^t if (ell,h)==(6-d,0) else 63))
            bits.append([(mask>>i)&1 for i in range(6)]+[(t>>i)&1 for i in range(6)]+[(reply>>i)&1 for i in range(6)])
            mass.append(float(F(value)/comb(6,d)))
    bits=np.array(bits,dtype=np.int16);mass=np.array(mass)
    c=bits[:,:6].sum(axis=1)
    u=np.array([sum(mass*bits[:,j]/np.maximum(c,1)) for j in range(6)])
    records=[];closed=False
    for step in range(args.steps):
        p=bits[:,:4].sum(axis=1); count=bits.shape[1]
        worst=[];responders=[];theta=[]
        for action in range(count):
            t=bits[:,action]
            last=(mass/(p+t+1))@bits
            best=max(last);eligible=np.flatnonzero(last>=best-1e-9)
            source=(mass*t/(p+1+bits[:,eligible].T)).sum(axis=1)
            chosen=int(eligible[np.argmin(source)])
            worst.append(float(min(source)));responders.append(chosen);theta.append(best)
        gap=np.array(worst)-u[4]
        action=int(np.argmax(gap));record={'step':step,'topics':count,'types':len(mass),'bad_action':action,'deviation_gap':float(gap[action])}
        if max(gap)<=1e-7:
            record['status']='floating_penultimate_full_menu_closed';closed=True;records.append(record);break
        t=bits[:,action];source0=float(sum(mass*t/(p+1)))
        block=t/((p+1)*(p+2));lastprofit=1/(p+t+1)
        prices=[1/(bits[:,:j].sum(axis=1)+6-j) for j in range(6)]
        answer=linprog(prices[-1],A_ub=np.array([-lastprofit,-block]+prices),
                       b_ub=[-theta[action],-(source0-u[4])]+u.tolist(),
                       bounds=list(zip(np.zeros(len(mass)),mass)),method='highs')
        record['LP_status']=answer.message
        if not answer.success:
            record['status']='greedy_completion_blocked_float';records.append(record);break
        record['new_actual_last_quote']=float(answer.fun)
        selected=np.minimum(np.maximum(answer.x,0),mass)
        nextbits=[];nextmass=[]
        for row,weight,taken in zip(bits,mass,selected):
            if weight-taken>1e-11:
                nextbits.append(np.append(row,0));nextmass.append(weight-taken)
            if taken>1e-11:
                nextbits.append(np.append(row,1));nextmass.append(taken)
        bits=np.array(nextbits,dtype=np.int16);mass=np.array(nextmass)
        records.append(record);print(json.dumps(record),flush=True)
    output={'scope':'floating admissible-catalog completion probe; NOT complete SPE',
            'closed_penultimate_float':closed,'records':records,'actual_payoffs':u.tolist(),
            'bits':bits.tolist(),'masses':mass.tolist()}
    (root/'catalog_completion_probe.json').write_text(json.dumps(output,indent=2)+'\n')
    print('TAIL_CLOSED',closed,'topics',bits.shape[1],'types',len(mass),flush=True)


if __name__=='__main__':main()
