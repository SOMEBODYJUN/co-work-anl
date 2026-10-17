"""Independent exact checks for a finite-cover configuration-LP realization.
No optimizer result is treated as a general proof. Base all 2**7 orientations
are enumerated exactly; the 6-cover is checked by its explicit true schedule.
"""
from fractions import Fraction as F
from itertools import product
import json

machines=['A','B','a','b']
jobs=['c']+[f'{s}{j}' for s in 'AB' for j in range(3)]
p={('A','c'):F(1),('B','c'):F(1)}
for root,terminal in [('A','a'),('B','b')]:
    for j in range(3):
        job=f'{root}{j}'
        p[root,job]=F(1,3)
        p[terminal,job]=F(1)
choices={j:[i for i in machines if (i,j) in p] for j in jobs}

def loads(sigma):
    out={i:F(0) for i in machines}
    for j,i in sigma.items():out[i]+=p[i,j]
    return out

base=[]
for row in product(*(choices[j] for j in jobs)):
    sigma=dict(zip(jobs,row)); ls=loads(sigma)
    base.append((max(ls.values()),sigma))
opt=min(x[0] for x in base)
assert opt==F(5,3)

# Six machine copies. First three root copies use all three small jobs;
# the next three each use c together with one small job.
q=6
configs={i:[] for i in machines}
for root,terminal in [('A','a'),('B','b')]:
    configs[root]=[tuple(f'{root}{j}' for j in range(3)) for _ in range(3)]
    configs[root]+=[('c',f'{root}{j}') for j in range(3)]
    configs[terminal]=[(f'{root}{j}',) for j in range(3) for _ in range(2)]
assert all(len(cs)==q for cs in configs.values())
T=F(4,3)
assert max(sum((p[i,j] for j in C),F(0)) for i in machines for C in configs[i])==T

# Assign distinct job-copy labels to all selected incidence sockets, then
# extend each partial incidence permutation lexicographically.
selected={j:[] for j in jobs}
for i in machines:
    for b,C in enumerate(configs[i]):
        for j in C:selected[j].append((i,b))
assert all(len(v)==q for v in selected.values())
perms={}; lift_sigma={}
for j in jobs:
    for label,(i,b) in enumerate(selected[j]):
        perms.setdefault((i,j),{})[label]=b
        lift_sigma[j,label]=(i,b)
    for i in choices[j]:
        partial=perms.setdefault((i,j),{})
        domain_missing=sorted(set(range(q))-set(partial))
        range_missing=sorted(set(range(q))-set(partial.values()))
        partial.update(zip(domain_missing,range_missing))
        assert sorted(partial)==list(range(q))
        assert sorted(partial.values())==list(range(q))
ll={(i,b):F(0) for i in machines for b in range(q)}
projected={i:{} for i in machines}
for (j,a),(i,b) in lift_sigma.items():
    assert perms[i,j][a]==b
    ll[i,b]+=p[i,j]
for i in machines:
    for b in range(q):
        S=tuple(sorted(j for (j,a),dest in lift_sigma.items() if dest==(i,b)))
        projected[i][S]=projected[i].get(S,F(0))+F(1,q)
    assert sum(projected[i].values())==1
for j in jobs:
    assert sum(v for i in machines for S,v in projected[i].items() if j in S)==1
assert max(ll.values())==T

# Check *every* base schedule lifts to this cover preserving every base
# machine's load at *each* clone, including overloaded schedules.
for C,sigma in base:
    ls=loads(sigma)
    liftload={(i,b):F(0) for i in machines for b in range(q)}
    for j in jobs:
        i=sigma[j]
        for a in range(q):liftload[i,perms[i,j][a]]+=p[i,j]
    assert all(liftload[i,b]==ls[i] for i in machines for b in range(q))

# Degenerate cases: no jobs, all-zero jobs and one-available-machine jobs.
def realize(p,machines,jobs,configs,q):
    for i in machines:assert len(configs[i])==q
    slots={j:[] for j in jobs}
    for i in machines:
        for b,C in enumerate(configs[i]):
            assert len(C)==len(set(C))
            for j in C:
                assert (i,j) in p
                slots[j].append((i,b))
    assert all(len(slots[j])==q for j in jobs)
    # Existence proof only needs this exact incidence counting identity.
    return max([sum((p[i,j] for j in C),F(0)) for i in machines for C in configs[i]] or [F(0)])
assert realize({},['z'],[],{'z':[(),()]},2)==0
assert realize({('z','j'):F(0)},['z'],['j'],{'z':[('j',),('j',)]},2)==0
assert realize({('z','j'):F(7,5)},['z'],['j'],{'z':[('j',)]},1)==F(7,5)

# Exact sanity checks for the partial-permutation construction in the
# high-girth-cover lemma. We do not enumerate the generated finite group.
def reduced_append(w,letter):
    return w[:-1] if w and w[-1]==-letter else w+(letter,)

def reduced_words(d,g):
    B={()}; frontier={()}
    for depth in range(g):
        new={w+(letter,) for w in frontier for letter in range(-d,d+1)
             if letter and (not w or w[-1]!=-letter)}
        B.update(new); frontier=new
    return B

word_checks=0
for d,g in [(1,g) for g in range(1,11)]+[(2,g) for g in range(1,5)]+[(3,g) for g in range(1,4)]:
    B=reduced_words(d,g)
    alphabet={}
    for letter in range(1,d+1):
        h={w:reduced_append(w,letter) for w in B
           if len(reduced_append(w,letter))<=g}
        assert len(set(h.values()))==len(h)
        h.update(zip(sorted(B-set(h)),sorted(B-set(h.values()))))
        assert set(h)==B and set(h.values())==B
        alphabet[letter]=h
        alphabet[-letter]={v:k for k,v in h.items()}
    for w in B-{()}:
        image=()
        for letter in w:image=alphabet[letter][image]
        assert image==w and image!=()
        word_checks+=1

out={
 'base':{'machines':len(machines),'jobs':len(jobs),'all_assignments_checked':len(base),'OPT':str(opt),'configuration_threshold_proved_in_note':'4/3'},
 'cover':{'q':q,'machines':len(machines)*q,'jobs':len(jobs)*q,'checked_schedule_load':str(max(ll.values())),'all_base_schedule_lifts_checked':len(base)},
 'high_girth_partial_permutation_words_checked':word_checks,
 'degenerates':['empty jobs','zero processing time','one finite machine'],
 'scope':'Exact finite certificate and enumeration; no graph-cover hardness conclusion.'
}
print(json.dumps(out,indent=2))
