"""Add arbitrary-background rows to 437-row frozen 64-atom support.

Only a diagnostic on an already restricted support. Not full catalog completion,
not all allowed atom types, not a half-coverage proof or a game counterexample.
"""
from fractions import Fraction as F
import json
from pathlib import Path
import sys
import numpy as np
from scipy.optimize import linprog

HERE=Path(__file__).resolve().parent
ROOT=next(p for p in HERE.parents if (p/'customer_attraction/__init__.py').is_file())
ns={}
source=(ROOT/'tests/audits/customer_attraction_five_indexed.py').read_text()
exec(compile(source.split('from pathlib import Path')[0],'<canonical 437 row definitions>','exec'),ns)
data=json.loads((ROOT/'evidence/certificates/customer_attraction/five_player_indexed_bound.json').read_text())['primal']
atoms=data['atoms'];bits=[list(map(int,a['bits'])) for a in atoms]
cols=[ns['evaluate'](b,[a['AB_hist'],a['AE_hist'],a['second_hist']],a['menus_lh'],True) for a,b in zip(atoms,bits)]
names=list(cols[0]);rows=[[col[n] for col in cols] for n in names]
w=[F(bool(sum(b[:5]))) for b in bits]
o=[F(bool(any(a['AB_hist'][4:]))) for a in atoms]
for i in range(4):
    k=5-i
    for C in range(10):
        MC=k+max((sum(b[:i]) for b in bits if b[C]),default=0)
        coef=(k-1)*(MC-1)+F(k*k,2)
        for D in range(10):
            row=[]
            for b in bits:
                past=sum(b[:i]);load=sum(b[:5])
                u=F(b[i],load) if b[i] else F(0)
                s=F(b[C],past+k)
                f=F(b[D],past+k if b[C] else past+1)
                row.append(s+coef*(u-s)-f)
            rows.append(row);names.append(f'background_pair:i{i}:C{C}:D{D}')
# Every node on the other two fixed genuine suffix paths.
for family,path,start in [('second',[0,4,5,6,7],2),('third',[0,1,4,8,9],3)]:
    for i in range(start,4):
        k=5-i
        for C in range(10):
            MC=k+max((sum(b[z] for z in path[:i]) for b in bits if b[C]),default=0)
            coef=(k-1)*(MC-1)+F(k*k,2)
            for D in range(10):
                row=[]
                for b in bits:
                    past=sum(b[z] for z in path[:i]);load=sum(b[z] for z in path)
                    u=F(b[path[i]],load) if b[path[i]] else F(0)
                    s=F(b[C],past+k)
                    f=F(b[D],past+k if b[C] else past+1)
                    row.append(s+coef*(u-s)-f)
                rows.append(row);names.append(f'{family}_background:i{i}:C{C}:D{D}')

# Summed same-index AP rows in recorded indexed true suffixes.  Fixed labels
# retain their original membership on every index; local letters denote the
# indexed topic with the same current index, never a fixed Markov selector.
local_families=[('AB', 'AB_hist',3,2,2),('AE','AE_hist',3,2,2),
                ('S3','second_hist',4,1,3),('S4','second_hist',4,2,2)]
from itertools import product
for family,hist_key,width,chosen,k in local_families:
    keys=list(range(10))+list(range(10,10+width))
    cells=list(product((0,1),repeat=width))
    for C in keys:
        # Uniform upper bound over every supported type and indexed local cell.
        # A column-dependent M would be invalid: M_C is a maximum over clients.
        candidate_past=[]
        for atom,b in zip(atoms,bits):
            for n,cell in zip(atom[hist_key],cells):
                cb=b[C] if C<10 else cell[C-10]
                if not n or not cb:continue
                if family=='AB':past=b[0]+b[1]+cell[0]
                elif family=='AE':past=b[0]+b[4]+cell[0]
                else:past=b[0]+sum(cell[:chosen])
                candidate_past.append(past)
        MC=k+max(candidate_past,default=0)
        coef=(k-1)*(MC-1)+F(k*k,2)
        for D in keys:
            row=[]
            for atom,b in zip(atoms,bits):
                result=F(0)
                for n,cell in zip(atom[hist_key],cells):
                    if not n:continue
                    if family=='AB':prefix=b[0]+b[1];past=prefix+cell[0]
                    elif family=='AE':prefix=b[0]+b[4];past=prefix+cell[0]
                    else:prefix=b[0];past=prefix+sum(cell[:chosen])
                    # chosen is local cell coordinate: AB/AE x is coordinate1.
                    cidx=1 if family in ('AB','AE') else chosen
                    load=prefix+sum(cell)
                    u=F(cell[cidx],load) if cell[cidx] else F(0)
                    cb=b[C] if C<10 else cell[C-10]
                    db=b[D] if D<10 else cell[D-10]
                    s=F(cb,past+k);f=F(db,past+k if cb else past+1)
                    result+=n*(s+coef*(u-s)-f)
                row.append(result)
            rows.append(row);names.append(f'{family}_indexed_background:C{C}:D{D}')
res=linprog(-np.array(o,dtype=float),A_ub=-np.array(rows,dtype=float),b_ub=np.zeros(len(rows)),
            A_eq=np.array([w],dtype=float),b_eq=[1],bounds=(0,None),method='highs')
assert res.success,res.message
support=[i for i,x in enumerate(res.x) if x>1e-8]
active=[i for i,row in enumerate(rows) if abs(sum(float(v)*x for v,x in zip(row,res.x)))<1e-7]
basis={}
for rr,bb in [([w[j] for j in support],F(1))]+[([rows[i][j] for j in support],F(0)) for i in active]:
    for c,(br,bv) in sorted(basis.items()):
        if rr[c]:
            z=rr[c];rr=[x-z*y for x,y in zip(rr,br)];bb-=z*bv
    c=next((j for j,z in enumerate(rr) if z),None)
    if c is None:
        assert not bb
        continue
    z=rr[c];basis[c]=([x/z for x in rr],bb/z)
    if len(basis)==len(support):break
assert len(basis)==len(support)
x=[F(0)]*len(support)
for c,(rr,bb) in sorted(basis.items(),reverse=True):
    x[c]=bb-sum(rr[j]*x[j] for j in range(c+1,len(support)))
point=[F(0)]*len(atoms)
for j,z in zip(support,x):point[j]=z
assert all(z>=0 for z in point)
assert sum(z*y for z,y in zip(w,point))==1
slacks=[sum(z*y for z,y in zip(row,point)) for row in rows]
assert min(slacks)>=0
value=sum(z*y for z,y in zip(o,point))
old=[F(a['mass_numerator'],data['denominator']) for a in atoms]
oldslacks=[sum(z*y for z,y in zip(row,old)) for row in rows[437:]]
report={'scope':'v2 topic-specific M_C support upper bounds; 437 old rows plus written background rows only on frozen 64 atom support',
        'game_SPE_witness':False,'universal_bound':False,'exact_primal_verified':True,
        'old_row_count':437,'new_row_count':len(rows)-437,'float_value':float(-res.fun),
        'exact_primal_value':str(value),'exact_primal_point':[str(z) for z in point],
        'old_point_min_background_slack':str(min(oldslacks)),
        'old_point_most_violated':[names[437+j] for j,z in enumerate(oldslacks) if z==min(oldslacks)],
        'full_domain_dual_certificate':False}
(HERE/'background_rows_fixed_support_v2.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='exact_primal_point'},indent=2))
