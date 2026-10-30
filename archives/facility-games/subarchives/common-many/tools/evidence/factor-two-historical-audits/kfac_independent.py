"""Independent exact small-instance attack on the arbitrary-k factor-two witness.

This enumerates site-uniform lexicographic ties and every pure client NE at
each actual labeled deviation. It does not import the delivered constructor.
Finite coverage is evidence, not the universal theorem.
"""

from itertools import product
from random import Random
from fractions import Fraction
import json

rng=Random(2123)

def occupied_assignments(layout, menus):
    occ=tuple(sorted(set(layout)))
    choices=[tuple(t for t in occ if t in menu) for menu in menus]
    for js in product(*[x or (None,) for x in choices]):
        yield js

def lex_witnesses(k,m,weights,menus):
    best=None; witnesses=[]
    for layout in product(range(m),repeat=k):
        counts=[layout.count(t) for t in range(m)]
        for ass in occupied_assignments(layout,menus):
            masses=[sum(w for w,t0 in zip(weights,ass) if t0==t) for t in range(m)]
            v=tuple(sorted((Fraction(masses[t],counts[t]) for t in layout)))
            if best is None or v>best:
                best=v; witnesses=[(layout,ass,masses,counts)]
            elif v==best:
                witnesses.append((layout,ass,masses,counts))
    return best,witnesses

def min_pure_ne_deviator(layout,weights,menus,f):
    choices=[tuple(j for j,t in enumerate(layout) if t in menu) for menu in menus]
    best=None
    for ass in product(*[x or (None,) for x in choices]):
        loads=[sum(w for w,a in zip(weights,ass) if a==j) for j in range(len(layout))]
        if all(a is None or all(j==a or loads[a]<=loads[j]+w for j in choices[i]) for i,(a,w) in enumerate(zip(ass,weights))):
            val=loads[f]
            if best is None or val<best: best=val
    assert best is not None
    return best

cases=0; deviations=0; maxratio=Fraction(0); macro=0; singleton=0
for m,k,n in [(2,2,3),(3,3,4),(3,4,4),(4,4,5)]:
  for _ in range(175):
    weights=[rng.choice((1,2,3,5,8,13,21)) for i in range(n)]
    menus=[frozenset(t for t in range(m) if rng.randrange(2)) for i in range(n)]
    if not any(menus): continue
    best,witnesses=lex_witnesses(k,m,weights,menus)
    for layout,ass,masses,counts in witnesses[:min(len(witnesses),3)]:
      cases+=1
      for f in range(k):
        a=Fraction(masses[layout[f]],counts[layout[f]])
        assert a>0
        for r in range(m):
          if r==layout[f]:continue
          t=list(layout); t[f]=r
          b=min_pure_ne_deviator(t,weights,menus,f)
          assert b<=2*a, (m,k,n,weights,menus,layout,ass,f,r,a,b)
          deviations+=1
          maxratio=max(maxratio,Fraction(b)/a)
          singleton+=int(counts[layout[f]]==1)
          macro+=sum(w>2*a for w in weights)
print(json.dumps(dict(schema_version=1,seed=2123,cases=cases,deviations=deviations,
                      max_pure_ratio=str(maxratio),singleton_deviations=singleton,
                      macro_opportunities=macro,limitations=[
                          "Finite exact check only; no universal proof or mixed-NE optimum claim."
                      ]),indent=2))
