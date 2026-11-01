#!/usr/bin/env python3
"""Independent labeled-index integer reconstruction of the new five-row cut.

Does not import the author's generator or old indexed generators. Reconstructs
all 448 projected coefficients from all complete labeled-word histograms.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
from hashlib import sha256
import json,math
import numpy as np

HERE=Path(__file__).resolve().parent
PARENT=HERE.parent/'parent'
ROOT=next(p for p in HERE.parents if (p/'work.py').exists())
WEIGHTS=(83667573,9398368,1172672,2396329,3365058)

def comp(n,k):
    if k==1:yield (n,);return
    for first in range(n+1):
      for rest in comp(n-first,k-1):yield (first,)+rest

def words(d):
    pats=list(product((0,1),repeat=2));out=[]
    for h0 in comp(6-d,4):
      for h1 in comp(d,4):
        row=[]
        for t,h in [(0,h0),(1,h1)]:
          for (b,c),n in zip(pats,h):row.extend([(t,b,c)]*n)
        assert len(row)==6 and sum(z[0] for z in row)==d
        out.append(row)
    return np.array(out,dtype=np.int64)

def reciprocal(den):
    assert np.all((den>=1)&(den<=30))
    assert np.all(60%den==0)
    return 60//den

def main():
    author_path=PARENT/'fourth_indexed_projection.json'
    author=json.loads(author_path.read_text())
    expect={(r['actual_bits'],r['d']):int(r['coefficient']) for r in author['coefficients']}
    assert tuple(author['integer_weights'])==WEIGHTS and author['K_coefficient']==0
    arrays=[words(d) for d in range(7)]
    assert [len(e) for e in arrays]==[84,224,350,400,350,224,84]
    assert sum(map(len,arrays))==1716
    got={};cases=0
    for p in range(4):
      for d,e in enumerate(arrays):
        n=len(e);t=e[:,:,0];b=e[:,:,1];c=e[:,:,2]
        den=p+t+b+c
        safe=np.maximum(den,1)
        own_t=t*reciprocal(safe);own_b=b*reciprocal(safe);own_c=c*reciprocal(safe)
        tail_H=own_b+own_c+b*reciprocal((p+t+1)*(p+t+2))
        sb=np.zeros(n,dtype=np.int64);sc=sb.copy();sp=sb.copy()
        for i in range(6):
          for j in range(6):
            sc+=own_c[:,i]-c[:,j]*reciprocal(p+t[:,i]+b[:,i]+1)
            if i!=j:
              sb+=own_c[:,i]-b[:,j]*reciprocal(p+t[:,i]+b[:,i]+1)
              sp+=tail_H[:,i]-(b[:,j]+c[:,j])*reciprocal(p+t[:,i]+1)+b[:,j]*c[:,j]*reciprocal((p+t[:,i]+1)*(p+t[:,i]+2))
        fixed_branches=WEIGHTS[2]*sb+WEIGHTS[3]*sc+WEIGHTS[4]*sp
        for a in product((0,1),repeat=6):
          if sum(a[:3])!=p:continue
          s=sum(a);pa=p+a[3]
          u4=F(a[3],s) if a[3] else F()
          actual_H=(F(a[4]+a[5],s) if a[4]+a[5] else F())+F(a[4],(pa+1)*(pa+2))
          source=int(360*u4)-own_t.sum(axis=1)
          fixedpair=np.full(n,int(360*actual_H),dtype=np.int64)
          for j in range(6):
            fixedpair-=(b[:,j]+c[:,j])*reciprocal(np.full(n,pa+1))
            fixedpair+=b[:,j]*c[:,j]*reciprocal(np.full(n,(pa+1)*(pa+2)))
          value=WEIGHTS[0]*source+WEIGHTS[1]*fixedpair+fixed_branches
          key=(''.join(map(str,a)),d)
          got[key]=int(max(value));assert got[key]==expect[key],(key,got[key],expect[key])
          cases+=n
    assert len(got)==448 and cases==64*1716
    point_path=ROOT/'research/workspaces/customer-attraction/R-d1fe1e0c444e40d68b6813bf88db8fba/parent/joint_system.json'
    point=json.loads(point_path.read_text())['certificate']
    sep=sum(F(z['weight'])*got[z['actual_bits'],z['d']] for z in point['support'])
    assert sep<0 and str(sep)==author['exact_separation']
    report={'status':'independent full coefficient reconstruction passed; necessary cut, not half theorem',
      'all_actual_types':64,'histograms':1716,'labeled_index_coefficient_cases':cases,
      'projected_coefficients_checked':448,'scale':60,'integer_weights':WEIGHTS,
      'K_coefficient':0,'exact_separation':str(sep),'normalized_separation':str(sep/(60*WEIGHTS[0])),
      'author_report_sha256':sha256(author_path.read_bytes()).hexdigest(),
      'input_point_sha256':sha256(point_path.read_bytes()).hexdigest()}
    HERE.joinpath('review_fourth_projection.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()
