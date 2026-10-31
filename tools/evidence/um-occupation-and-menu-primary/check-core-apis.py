"""Hand-solvable exact API examples for original library, not a main/scheduler run."""
from pathlib import Path
from fractions import Fraction as F
import importlib.util,json,sys,hashlib
source=Path(sys.argv[1]);spec=importlib.util.spec_from_file_location('cg_original_core_only',source)
core=importlib.util.module_from_spec(spec);spec.loader.exec_module(core)
assert core.dot((F(1,3),F(2,3)),(3,3))==3
assert core.rank([[1,0,1],[0,1,1],[1,1,2]])==2
assert core.solve_square([[1,1],[1,-1]],[1,0])==(F(1,2),F(1,2))
assert core.solve_square([[1,1],[2,2]],[1,2]) is None
assert core.affine_rank([(0,0),(1,0),(0,1),(1,1)])==2
matching=core.max_matching([{0,1},{1,2}],{0,2})
assert len(matching)==2 and len({h for b,h in matching})==2
assert all(h in [{0,1},{1,2}][b] for b,h in matching)
cases=[]
for K in (1,2):
    groups=[]
    graph=[]
    for z in range(K):
        graph.append({2*z,2*z+1})
        for t in (0,1):
            cost=tuple(F(2) if j==z and t==0 else F(0) for j in range(K))
            groups.append([(0,tuple(F(0) for _ in range(K))),(1,cost)])
    offsets,rows,selections,points=core.prepare(groups,graph)
    assert len(points)==2**K
    y,count=core.projected_vertex(points,rows,[F(1)]*K,list(range(K)))
    assert y==tuple([F(1,2)]*(4*K))
    dp,db,support,mixed=core.face_dimensions(y,groups,graph,offsets,points)
    assert dp==db==K and mixed==2*K and all(s=={0,1} for s in support)
    assert dp==db+sum(len(s)-1 for s in support)-mixed
    assert [core.dot(row,y) for row in rows]==[F(1)]*K
    # A valid integer support selection can exceed the original side budget.
    first=tuple(1 if h%2==0 else 0 for h in range(2*K))
    assert first in selections
    point=points[selections.index(first)]
    assert [core.dot(row,point) for row in rows]==[F(2)]*K
    cases.append({'side_constraints':K,'homes':2*K,'integer_mode_points':len(points),'lex_projected_vertex':list(map(str,y)),'original_face_dimension':dp,'occupation_face_dimension':db,'mixed_homes':mixed,'non_singleton_homes':len(support),'candidate_extension_vertices_with_multiplicity':count,'side_costs_at_vertex':['1']*K,'one_valid_support_rounding_costs':['2']*K,'side_budget_not_promised_by_core':True})
offsets,rows,selections,points=core.prepare([],[])
assert selections==[()] and points==[()] and rows==()
assert core.projected_vertex(points,rows,[],[])[0]==()
assert core.face_dimensions((),[],[],offsets,points)==(0,0,[],0)
report={'status':'passed','arithmetic':'Fraction exact, hand-described polytopes','original_library_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'original_library_main_entries':0,'library_definition_imports':1,'new_api_probe_runs':1,'cases':cases,'zero_home_zero_macro_case':'passed','linear_algebra_rank2_and_singular_system':'passed','covering_matching_two_distinct_homes':'passed','limits':'Two constructed sharp2K projected vertices and empty/linear algebra API checks only; no full fixed-sink scheduler or arbitrary LP backend.'}
print(json.dumps(report,ensure_ascii=False,indent=2))
