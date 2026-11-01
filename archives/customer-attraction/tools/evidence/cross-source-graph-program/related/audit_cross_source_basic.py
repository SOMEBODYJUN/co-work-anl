"""Independent review of research_5's 12 actual floors and 2 old capacities.

This does not review the old 3945 rows, 960 projected rows, or SPE realizability.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
import importlib.util,json,sys
HERE=Path(__file__).resolve().parent
SRC=HERE.parent/'research_5'
sys.path.insert(0,str(SRC))
spec=importlib.util.spec_from_file_location('reviewed_cross_source_graph',SRC/'cross_source_graph.py')
cross=importlib.util.module_from_spec(spec);spec.loader.exec_module(cross)

patterns=tuple(product((0,1),repeat=3))
cols=[{'kind':'K'}]
for a in product((0,1),repeat=6):
    for nb,nc in product(range(7),repeat=2):
        hist=[0]*8
        for j in range(6):
            word=(0,int(j<nb),int(j<nc));hist[patterns.index(word)]+=1
        cols.append({'kind':'hist','actual_bits':''.join(map(str,a)),'d':0,'hist':hist})
# Review only the freshly added basic rows; no inherited build is called.
cross.sb.build=lambda:(cols,[],[],[],[])
sys.argv=['independent-basic-review']
_,names,rows,_,_=cross.build()
assert len(names)==14
checked=0
for name,row in zip(names,rows):
    for j,c in enumerate(cols):
        if c['kind']=='K':
            expected=F(6) if name.startswith('old-capacity:') else F()
        else:
            actual=tuple(map(int,c['actual_bits']));whole=sum(actual)
            # Independently reconstruct actual current payoff and six queries.
            queried=[sum(n*w[q] for n,w in zip(c['hist'],patterns)) for q in (1,2)]
            if name.startswith('actual-floor:'):
                i,q=map(int,name.split('(',1)[1].rstrip(')').split(','))
                own=F(actual[i],whole) if actual[i] else F()
                old_load=sum(actual[:i]);players_left=6-i
                expected=6*own-F(queried[q-1],old_load+players_left)
            else:
                q=int(name.rsplit(':',1)[1]);expected=-F(queried[q-1])
        assert row[j]==expected,(name,j,row[j],expected)
        checked+=1
# Check these same formulas on the author's preceding exact graph point.
point=json.loads((SRC/'split_basic_exact.json').read_text())
oldslacks={n:F() for n in names}
for c in point['columns']:
    mass=F(c['weight'])
    if c['kind']=='K':
        for n in names:
            if n.startswith('old-capacity:'):oldslacks[n]+=6*mass
    elif c['kind']=='hist':
        a=tuple(map(int,c['actual_bits']));whole=sum(a)
        for q in (1,2):
            count=sum(n*w[q] for n,w in zip(c['hist'],patterns))
            oldslacks['old-capacity:'+str(q)]-=mass*count
            for i in range(6):
                own=F(a[i],whole) if a[i] else F()
                n='actual-floor:'+str((i,q))
                oldslacks[n]+=mass*(6*own-F(count,sum(a[:i])+6-i))
print(json.dumps({'scope':'14 basic row coefficients only; no projected or inherited graph review',
    'coefficient_comparisons':checked,'types_including_K':len(cols),
    'old_point_negative_rows':{n:str(v) for n,v in oldslacks.items() if v<0}},indent=2))
