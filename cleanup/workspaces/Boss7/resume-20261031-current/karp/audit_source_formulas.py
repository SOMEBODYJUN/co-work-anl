"""Finite recomputations of specifically identified printed formulas, not a proof of the paper."""
from itertools import product
from pathlib import Path
import json, hashlib
base=Path(__file__).resolve().parent
out={"scope":"Finite exact recomputations of three printed-formula defects. General corrected proofs are in the literature object, not established by these checks.","checks":[]}
# SAT's displayed row coefficients become the wrong problem if read as equalities.
assign=list(product((0,1), repeat=2))
sat=[x for x in assign if x[0] and x[1] and (x[0] or x[1])]
wrong_ip=[x for x in assign if x[0]==1 and x[1]==1 and x[0]+x[1]==1]
assert sat==[(1,1)] and not wrong_ip
out['checks'].append({"name":"SAT displayed clause rows require slack for equality IP","formula":[[1],[2],[1,2]],"SAT_witnesses":sat,"displayed_rows_if_equalities_witnesses":wrong_ip})
# Original weighted-cut threshold has the square inside the sum.
c=[1,2]; C=sum(c)
partition=[x for x in assign if sum(a*b for a,b in zip(c,x))*2==C]
cut=max(sum(c[i]*c[j] for i in range(2) for j in range(i+1,2) if x[i]!=x[j]) for x in assign)
printed=(sum(v*v for v in c)+3)//4
corrected=(C*C+3)//4
assert not partition and cut>=printed and cut<corrected
out['checks'].append({"name":"Partition-to-weighted-MaxCut printed threshold fails","c":c,"partition":False,"max_cut":cut,"printed_threshold":printed,"corrected_threshold":corrected})
# Original undirected zero-incidence Steiner graph bypasses a root-to-set edge.
sets=[{'a','b'},{'b','c'}]; universe={'a','b','c'}
exact=[]
for x in assign:
 chosen=[s for s,t in zip(sets,x) if t]
 if all(sum(u in s for s in chosen)==1 for u in universe):exact.append(x)
edges=[('r','s1',2),('s1','a',0),('s1','b',0),('b','s2',0),('s2','c',0)]
verts={v for e in edges for v in e[:2]}; reached={'r'}
while True:
 new=reached|{v for u,v,w in edges if u in reached}|{u for u,v,w in edges if v in reached}
 if new==reached:break
 reached=new
assert not exact and len(edges)==len(verts)-1 and reached==verts and sum(w for _,_,w in edges)==2
out['checks'].append({"name":"ExactCover-to-Steiner printed graph admits a false YES","universe":sorted(universe),"sets":[sorted(s) for s in sets],"exact_covers":exact,"Steiner_tree_edges":edges,"tree_cost":2,"budget":3,"all_terminals_reached":True})
out['script_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
(base/'source-formula-audit.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({"checks":len(out['checks']),"assertions":"passed","scope":out['scope']},ensure_ascii=False))
