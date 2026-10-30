"""Independent Fraction Gauss-Jordan reference for the price vertex enumerator.

This checks finite implementation instances, not the arbitrary-p proof, whose
independent reconstruction is in fractional_price_vertex_audit.md.
"""
from fractions import Fraction as F
from itertools import combinations,permutations
from pathlib import Path
import importlib.util,json,random,time
HERE=Path(__file__).resolve().parent
MODULE=HERE.parent/'credible/fractional_query_vertices.py'
spec=importlib.util.spec_from_file_location('reviewed_vertices',MODULE)
target=importlib.util.module_from_spec(spec);spec.loader.exec_module(target)

def reference_solve(rows):
    n=len(rows)
    if not n:return ()
    a=[[F(x) for x in row]+[F(1)] for row in rows]
    for j in range(n):
        piv=next((i for i in range(j,n) if a[i][j]),None)
        if piv is None:return None
        a[j],a[piv]=a[piv],a[j]
        d=a[j][j];a[j]=[x/d for x in a[j]]
        for i in range(n):
            if i!=j:
                f=a[i][j];a[i]=[x-f*y for x,y in zip(a[i],a[j])]
    return tuple(a[j][-1] for j in range(n))

def independent_vertices(p):
    out={(F(0),)*p}
    # Enumerate each actual positive coordinate support; no pattern sorting.
    for s in range(1,p+1):
        rows=[tuple((mask>>j)&1 for j in range(s)) for mask in range(1,1<<s)]
        positive=set()
        for selected in combinations(rows,s):
            z=reference_solve(selected)
            if z is not None and all(0<x<=1 for x in z):positive.add(z)
        for support in combinations(range(p),s):
            for z in positive:
                full=[F(0)]*p
                for j,x in zip(support,z):full[j]=x
                out.add(tuple(full))
    return out

def main():
    started=time.monotonic();total=0;singular=0;dimensions=[]
    for n in range(1,5):
        rows=[tuple((mask>>j)&1 for j in range(n)) for mask in range(1,1<<n)]
        checked=0
        for selected in combinations(rows,n):
            want=reference_solve(selected);got=target.solve_binary_ones(selected)
            assert want==got,(selected,want,got)
            checked+=1;singular+=want is None
        dimensions.append({'n':n,'exhaustive_nonempty_binary_row_subsets':checked});total+=checked
    rng=random.Random(748095)
    for n in range(2,10):
        # Include arbitrary row orders, duplicates, and empty rows to exercise
        # row pivoting/singular exits beyond the caller's row-combination class.
        for _ in range(200):
            selected=[tuple(rng.randrange(2) for _ in range(n)) for _ in range(n)]
            want=reference_solve(selected);got=target.solve_binary_ones(selected)
            assert want==got,(selected,want,got)
            total+=1;singular+=want is None
    counts=[]
    for p in range(5):
        vertices,patterns,stats=target.enumerate_vertices(p)
        reference=independent_vertices(p)
        assert set(vertices)==reference,(p,set(vertices)^reference)
        assert len(vertices)==len(set(vertices))
        counts.append({'p':p,'vertices':len(vertices),'patterns':len(patterns)})
    for p in [-1,True,1.5]:
        try:target.enumerate_vertices(p)
        except ValueError:pass
        else:raise AssertionError(('invalid p accepted',p))
    out={'scope':'finite independent exact implementation check, not universal theorem','method':'Fraction Gauss-Jordan versus integer Bareiss; independent support embedding versus sorted-pattern permutations','binary_systems_checked':total,'singular_systems':singular,'exhaustive_dimensions':dimensions,'vertex_counts':counts,'seconds':time.monotonic()-started,'passed':True}
    print(json.dumps(out,indent=2))
    (HERE/'fractional_price_vertex_implementation_audit.json').write_text(json.dumps(out,indent=2)+'\n')

if __name__=='__main__':main()
