"""Independent exact review of ae1632 CAG input; never writes source assets.

Uses frozen integer customer types and every ordered policy record. No author,
solver, or packet replay code is imported. Affine pairs represent c + k*J.
"""
from fractions import Fraction as Q
from itertools import product, combinations_with_replacement
from collections import Counter, defaultdict
from pathlib import Path
import hashlib
import json

ROOT = next(p for p in Path(__file__).resolve().parents if (p / 'work.py').is_file() and (p / 'archives/customer-attraction').is_dir())
BASE = ROOT / 'archives/customer-attraction/tools/evidence/local-potential-exclusion-complete-certificates-primary/original'
PATH3 = BASE / 'attack/potential_tax/esm_exact_obstruction.json'
PATH6 = BASE / 'attack/potential_tax/six_esm_embedding.json'
d3, d6 = [json.loads(p.read_text()) for p in (PATH3, PATH6)]
old = [(frozenset(t['topics']), t['multiplicity']) for t in d3['customers']]
assert sum(w for _, w in old) == 621 and len(old) == 11
assert d6['instance']['customers'] == d3['customers'] + [{'topics': [5], 'multiplicity': 510}]
print('INPUT_SHA', *(hashlib.sha256(p.read_bytes()).hexdigest() for p in (PATH3, PATH6)))

def label(t):
    return ''.join('ABCDEF'[a] for a in t) or 'empty'

def counts(t, n):
    return tuple(t.count(a) for a in range(n))

def read_policy(d, n, m):
    q = {}
    for row in d['strategy']:
        h, a = tuple(row['history']), row['action']
        assert h not in q and all(0 <= t < n for t in h) and 0 <= a < n
        q[h] = a
    expected = {h for k in range(m) for h in product(range(n), repeat=k)}
    assert set(q) == expected
    return q

def completion(q, n, m):
    end = {h:h for h in product(range(n), repeat=m)}
    for k in reversed(range(m)):
        for h in product(range(n), repeat=k):
            end[h] = end[h + (q[h],)]
    return end

def utilities(c):
    result = []
    for a in range(len(c)):
        constant = sum((Q(w, sum(c[t] for t in B)) for B,w in old if a in B and sum(c[t] for t in B)), Q(0))
        result.append((constant, Q(1,c[5]) if a == 5 and c[5] else Q(0)))
    return result

def check(q,n,m, frozen_rows=None):
    end = completion(q,n,m)
    cache = {c:utilities(c) for c in {counts(t,n) for t in product(range(n),repeat=m)}}
    lower, upper = None,None
    lower_rows,upper_rows = [],[]
    slopes = Counter()
    rows = {}
    min510 = None
    for k in range(m):
        for h in product(range(n),repeat=k):
            prescribed = end[h]
            v0,v1 = cache[counts(prescribed,n)][q[h]]
            for a in range(n):
                deviated = end[h+(a,)]
                w0,w1 = cache[counts(deviated,n)][a]
                b,s = v0-w0,v1-w1
                slopes[(s>0)-(s<0)] += 1
                record=(h,a,prescribed,deviated,b,s)
                rows[h,a]=record
                value=b+510*s
                min510=value if min510 is None else min(min510,value)
                if s==0:
                    assert b>=0,record
                elif s>0:
                    x=-b/s
                    if lower is None or x>lower: lower,lower_rows=x,[record]
                    elif x==lower: lower_rows.append(record)
                else:
                    x=-b/s
                    if upper is None or x<upper: upper,upper_rows=x,[record]
                    elif x==upper: upper_rows.append(record)
    assert min510>=0
    if frozen_rows is not None:
        assert len(frozen_rows)==len(rows)
        seen=set()
        for row in frozen_rows:
            key=tuple(row['history']),row['action']
            assert key not in seen
            seen.add(key)
            h,a,p,z,b,s=rows[key]
            assert list(p)==row['actual_terminal'] and list(z)==row['deviation_terminal']
            assert b==Q(row['slack']) and s==0
    print('POLICY',n,m,'nodes',len(q),'comparisons',len(rows),'cache',len(cache),'slopes',dict(slopes),'interval',lower,upper,'binding',len(lower_rows),len(upper_rows),'min@510',min510,'actual',label(end[()]))
    for name,items in [('LOWER',lower_rows),('UPPER',upper_rows)]:
        if items:
            h,a,p,z,b,s=items[0]
            print(name,label(h),'choose','ABCDEF'[q[h]],'deviate','ABCDEF'[a],label(p),label(z),'slack',b,s)
    return end,rows

q3=read_policy(d3,5,3)
assert q3[()]==d3['root_action']
assert [q3[(a,)] for a in range(5)]==d3['second_actions']
assert [[q3[(a,b)] for b in range(5)] for a in range(5)]==d3['last_actions']
e3,r3=check(q3,5,3,d3['IC_rows'])
q6=read_policy(d6,6,6)
e6,r6=check(q6,6,6)
qr=dict(q6)
for h,a in q3.items(): qr[(5,5,5)+h]=a
changed=[h for h in q6 if qr[h]!=q6[h]]
assert len(changed)==7
er,rr=check(qr,6,6)
print('RESTORE_CHANGES',[(label(h),'ABCDEF'[q6[h]],'ABCDEF'[qr[h]]) for h in changed])
print('COMPLETION_CHANGES',sum(e6[h]!=er[h] for h in q6),'IC_LEAFPAIR_CHANGES',sum(r6[k][2:4]!=rr[k][2:4] for k in r6))
print('RESTORE_OLD_MIN_PAYOFF',min(utilities(counts(e3[h],5))[q3[h]][0] for h in q3))
print('NEW_F_BRANCH_COUNTS',dict(Counter(e6[(5,5,5)+h+(5,)].count(5) for h in q3)))
print('ANCESTOR_COMPLETIONS',[(label(h),label(e6[h]),label(er[h])) for h in [(),(5,),(5,5),(5,5,5)]])
for h,a in [((0,3,3),1),((0,0,3,5,5),5)]:
    rec=r6[h,a];print('BOUNDARY',label(h),'action','ABCDEF'[a],'slack508',rec[4]+508*rec[5],'slack517',rec[4]+517*rec[5])

def affine_potential(prefix, tail, j):
    def contribution(B,w):
        b=sum(a in B for a in prefix)
        c=sum(a in B for a in tail)
        return w*sum((Q(1,t) for t in range(b+1,b+c+1)),Q(0))
    return sum((contribution(B,w) for B,w in old),Q(0))+contribution({5},j)

def maximal(prefix, r, j, required=(), n=6):
    valid=[]
    need=Counter(required)
    for t in combinations_with_replacement(range(n),r):
        if not (need-Counter(t)):
            valid.append((affine_potential(prefix,t,j),t))
    v=max(p for p,t in valid)
    return v,[t for p,t in valid if p==v]

def safe(prefix, a, r, j):
    return sum((Q(w,sum(t in B for t in prefix)+r) for B,w in old if a in B),Q(0))+(Q(j,prefix.count(5)+r) if a==5 else Q(0))

def arrival(prefix,a,j):
    return safe(prefix,a,1,j)

for name,q,end,n,m in [('three',q3,e3,5,3),('frozen',q6,e6,6,6),('restored',qr,er,6,6)]:
    ts=[Q(0)] if n==5 else [Q(1017,2),Q(509),Q(510),Q(516)]
    for j in ts:
        path=end[()]
        cp=counts(path,n)
        u=[sum(x*y for x,y in zip(utilities(cp)[a],(1,j))) for a in path]
        margins=[]; taxes=[];loss=[]
        for i,a in enumerate(path):
            b=path[:i];r=m-i
            p,_=maximal(b,r,j,n=n)
            forced,_=maximal(b,r,j,(a,),n)
            ss=safe(b,a,r,j)
            margins.append(u[i]-ss-(p-forced));taxes.append(arrival(b,a,j)-ss);loss.append(p-forced)
        pairs=[]
        for i in range(m-1):
            b=path[:i];r=m-i
            p,_=maximal(b,r,j,n=n)
            forced,_=maximal(b,r,j,path[i:i+2],n)
            pairloss=p-forced
            assert pairloss==loss[i]+loss[i+1]
            pairs.append(margins[i]+margins[i+1])
        rootp,maximizers=maximal((),m,j,n=n)
        remainder=[sum(margins[i:]) for i in range(m)]
        assert sum(u)+sum(taxes)-rootp==sum(margins)
        print('PATH',name,'J',j,'u',*[str(x) for x in u],'margins',*[str(x) for x in margins],'pair',*[str(x) for x in pairs],'D',*[str(x) for x in remainder],'W,C,P,D',sum(u),sum(taxes),rootp,sum(margins),'max',list(map(label,maximizers)))
        if j==510 or n==5:
            prefix=() if n==5 else (5,5,5)
            p,_=maximal(prefix,3,j,n=n);forced,_=maximal(prefix,3,j,(0,),n)
            s=safe(prefix,0,3,j);u0=Q(166)
            for a in range(n):
                leaf=end[prefix+(a,)];tail=leaf[len(prefix):]
                utility=utilities(counts(leaf,n))[a]
                d=utility[0]+j*utility[1]
                ga=arrival(prefix+tail[1:],0,j)
                ell=p-affine_potential(prefix,tail,j)
                gamma=u0-d
                rhs=ell-gamma-(ga-s)
                gap=forced-affine_potential(prefix,(0,)+tail[1:],j)
                assert rhs==(p-forced-(u0-s))+gap
                print('MENU',name,'ABCDEF'[a],label(tail),'ell',ell,'Gamma',gamma,'g-s',ga-s,'M_rhs',rhs,'restricted_gap',gap)

print('OLD_P0..6',[str(maximal((),r,Q(0),n=5)[0]) for r in range(7)])
assert maximal((),3,Q(0),n=5)[1]==[tuple(x) for x in d3['all_P3_maximizers']]
assert maximal((),3,Q(0),(0,),5)[1]==[tuple(x) for x in d3['all_P3_A_maximizers']]
# Every static comparison is affine in J at a fixed actual prefix. Equality
# to the claimed bound at both endpoints proves the bound throughout the
# interval, since this loop explicitly enumerates every legal multiset.
for j in [Q(1017,2),Q(516)]:
    path=(5,5,5,0,1,2)
    expected_p=[801+11*j/6,801+5*j/6,801+j/3,Q(801),Q(394),Q(190)]
    expected_f=expected_p[:3]+[Q(754),Q(394),Q(190)]
    for i,a in enumerate(path):
        prefix=path[:i];r=6-i
        assert maximal(prefix,r,j)[0]==expected_p[i]
        assert maximal(prefix,r,j,(a,))[0]==expected_f[i]
        # One common attaining multiset at both endpoints (hence everywhere).
        witness=(1,2,3)+(5,)*(3-i) if i<3 else [(1,2,3),(1,2),(2,)][i-3]
        forced_witness=witness if i!=3 else (0,1,2)
        assert affine_potential(prefix,witness,j)==expected_p[i]
        assert affine_potential(prefix,forced_witness,j)==expected_f[i]
    print('STATIC_ALL_CANDIDATES_ENDPOINT_PASS',j)
for name,prefix,n,j in [('three',(),5,Q(0)),('sixFFF',(5,5,5),6,Q(510))]:
    ordered=[(affine_potential(prefix,t,j),t) for t in product(range(n),repeat=3)]
    assert max(v for v,t in ordered)==801
    assert max(v for v,t in ordered if 0 in t)==754
    print('ORDERED_STATIC_PASS',name,len(ordered))
print('ALL_ASSERTIONS_PASSED')
