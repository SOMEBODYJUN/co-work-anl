"""Exact feasible >2 point for all 2408 rows, not an SPE certificate."""
from pathlib import Path
from fractions import Fraction as F
import json
from reopt_common_pivot import allrows
HERE=Path(__file__).parent


def main():
    report=json.loads((HERE/'reopt_common_pivot.json').read_text())
    atoms=report['atoms'];point=report['point'];cols=[allrows(a) for a in atoms]
    names=list(cols[0]);G=[[c[n] for c in cols] for n in names]
    w=[int(any(map(int,a['bits'][:5]))) for a in atoms]
    o=[int(any(a['AB_hist'][4:])) for a in atoms]
    support=[i for i,x in enumerate(point) if x>1e-8]
    active=[row for row in G if abs(sum(float(a)*b for a,b in zip(row,point)))<1e-7]
    basis={}
    for row,rhs in [(w,F(1))]+[(r,F()) for r in active]:
        v=[F(row[i]) for i in support]+[rhs]
        for pivot,b in sorted(basis.items()):
            z=v[pivot]
            if z:v=[a-z*c for a,c in zip(v,b)]
        pivot=next((i for i,x in enumerate(v[:-1]) if x),None)
        if pivot is None:
            assert not v[-1];continue
        z=v[pivot];basis[pivot]=[a/z for a in v]
        if len(basis)==len(support):break
    assert len(basis)==len(support)
    x=[F()]*len(support)
    for pivot,b in sorted(basis.items(),reverse=True):
        x[pivot]=b[-1]-sum(b[i]*x[i] for i in range(pivot+1,len(support)))
    mass=[F()]*len(atoms)
    for i,z in zip(support,x):mass[i]=z
    assert min(mass)>=0 and sum(a*b for a,b in zip(w,mass))==1
    slacks={n:sum(c[n]*z for c,z in zip(cols,mass)) for n in names}
    assert min(slacks.values())>=0
    objective=sum(a*b for a,b in zip(o,mass));assert objective>2
    out={'scope':'exact feasible point of the entire 2408-row necessary-condition system; finite support witnesses insufficiency, not full-domain optimality or SPE',
         'rows':len(names),'candidate_columns':len(atoms),'positive_atoms':sum(z>0 for z in mass),
         'W':'1','O':str(objective),'gap_above_two':str(objective-2),
         'all_rows_verified_exactly':True,'minimum_slack':str(min(slacks.values())),
         'zero_slacks':sum(z==0 for z in slacks.values()),
         'new_row_slacks':{n:str(z) for n,z in slacks.items() if n.startswith('common-pivot:')},
         'atom_masses':[{**a,'mass':str(z)} for a,z in zip(atoms,mass) if z]}
    (HERE/'common_pivot_2408_exact_obstruction.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k!='atom_masses'},indent=2))


if __name__=='__main__':main()
