from fractions import Fraction
from itertools import combinations_with_replacement, product
from pathlib import Path
import hashlib, json

BASE = Path(__file__).resolve().parent

def plan(p, t):
    q = len(p)
    if not q:
        return 0, set(), 'a'
    if sum(p) <= t:
        return q, set(), 'b'
    big = {j for j, v in enumerate(p) if 2*v > t}
    if q <= 3:
        return q-1, big, 'c'
    if sum(p[1:]) > t:
        return 2, big, 'd'
    if p[0] + p[1] > t:
        return 3, {0, 1}, 'e'
    return 3, big, 'f'

def allowed(p, t, chosen):
    d, big, _ = plan(p, t)
    return len(chosen) <= d and len(set(chosen) & big) <= 1

rows = subsets = 0
for t in range(1, 21):
    for q in range(5):
        for inc in combinations_with_replacement(range(1,t+1), q):
            p = tuple(reversed(inc))
            rows += 1
            for mask in range(1 << q):
                chosen = [j for j in range(q) if (mask >> j) & 1]
                load = sum(p[j] for j in chosen)
                a = allowed(p,t,chosen)
                subsets += 1
                assert load > t or a, (t,p,chosen,'lost legal configuration')
                ratio = Fraction(1) if q <= 2 else Fraction(3,2) if q == 3 else Fraction(5,3)
                assert not a or load <= ratio*t, (t,p,chosen,'load bound')
                assert q > 2 or a == (load <= t), (t,p,chosen,'ell2 equivalence')

# Every row is indexed by task label. None denotes an unavailable endpoint.
def schedules(matrix, t=None):
    n = len(matrix[0]); m = len(matrix)
    eligible = [[i for i in range(m) if matrix[i][j] is not None] for j in range(n)]
    for assignment in product(*eligible):
        if t is not None:
            ok = True
            for i, row in enumerate(matrix):
                order = sorted([j for j,v in enumerate(row) if v is not None and v <= t], key=lambda j: (-row[j], j))
                chosen = [k for k,j in enumerate(order) if assignment[j] == i]
                if any(assignment[j] == i and j not in order for j in range(n)) or not allowed([row[j] for j in order],t,chosen):
                    ok = False; break
            if not ok:
                continue
        load = max(sum(matrix[i][j] for j in range(n) if assignment[j] == i) for i in range(m))
        yield assignment,load

inverse = [[6,5,1],[None,None,1]]
nonmonotone = [[10,5,4,3],[None,None,1,None],[None,None,None,1]]
assert min(load for _,load in schedules(inverse)) == 11
assert list(schedules(inverse,10))
assert min(load for _,load in schedules(nonmonotone)) == 15
assert list(schedules(nonmonotone,10))
assert not list(schedules(nonmonotone,12))
assert list(schedules(nonmonotone,15))
l = 0; h = sum(v for row in nonmonotone for v in row if v is not None)
trace=[]
while h > l+1:
    mid = (l+h)//2
    success = bool(list(schedules(nonmonotone,mid)))
    trace.append({'T':mid,'success':success})
    if success: h=mid
    else: l=mid
assert h == 15
result={
    'local_rows':rows,'local_subsets':subsets,'T_range':[1,20],
    'checks':['every legal threshold configuration survives the machine plan','all allowed rows satisfy the 1/3/2/5/3 load bounds','ell2 allowed family equals threshold configuration family'],
    'inverse_example':{'matrix':inverse,'T':10,'OPT':11,'full_flow':True},
    'nonmonotone_example':{'matrix':nonmonotone,'OPT':15,'T10_full_flow':True,'T12_full_flow':False,'T15_full_flow':True,'binary_trace':trace,'binary_final':h},
    'note':'Exact finite verification supplements but does not replace the analytic proof.',
    'source_pdf_sha256':hashlib.sha256(Path('archives/unrelated-machines/tools/evidence/registration-Boss5-0111-literature/bounded-job-assignments.pdf').read_bytes()).hexdigest()
}
(BASE/'verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(result,ensure_ascii=False))
