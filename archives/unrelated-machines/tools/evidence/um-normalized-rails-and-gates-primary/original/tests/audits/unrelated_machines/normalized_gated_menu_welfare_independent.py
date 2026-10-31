"""Independent finite certificate and enumeration checks against the frozen menu audit."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
from collections import defaultdict
import hashlib, json, random, subprocess, sys

ROOT=Path(__file__).resolve().parents[3]
import argparse
parser=argparse.ArgumentParser()
parser.add_argument('--output',type=Path,required=True)
args=parser.parse_args()
if args.output.exists():parser.error('refusing to overwrite frozen output')
TARGET=ROOT/'tests/audits/unrelated_machines/normalized_gated_menu_welfare.py'
EXPECTED='31aeb2b57bbf78e0f980f552bd5985e4f0a15b57f98f93f46be1296a19b156f6'
raw=TARGET.read_bytes()
assert hashlib.sha256(raw).hexdigest()==EXPECTED
DATA=ROOT/'evidence/runs/unrelated_machines/normalized_gated_menu_welfare_audit.json'
data=json.loads(DATA.read_text())
assert data['code_sha256']==EXPECTED

def frac(a):
    if isinstance(a,list):return [frac(x) for x in a]
    return F(a)

def feasible(menu,z,x):
    for g,ss in enumerate(menu):
        assert sum(z[g])==1 and all(v>=0 for v in z[g])
        for s,state in enumerate(ss):
            assert min(state)>=0 and sum(state)==1
            for u,p in enumerate(state):
                assert 0<=x[g][s][u]<=z[g][s]
                assert p or not x[g][s][u]
    for u in range(len(menu[0][0])):
        assert sum(x[g][s][u] for g,ss in enumerate(menu) for s in range(len(ss)))<=1

def value(menu,x):
    return sum(p*x[g][s][u] for g,ss in enumerate(menu) for s,state in enumerate(ss) for u,p in enumerate(state))

def semantic_dual(menu,cert):
    # Decode minimization dual as welfare prices a_(g,s,u), b_u, eta_g.
    pv=frac(cert['exact_primal']);du=frac(cert['exact_dual_ub']);de=frac(cert['exact_dual_eq'])
    n=len(menu);m=len(menu[0][0]);keys=[(g,s,u) for g,ss in enumerate(menu) for s,state in enumerate(ss) for u,p in enumerate(state) if p]
    sc=sum(map(len,menu));assert len(pv)==sc+len(keys) and len(du)==len(keys)+m and len(de)==n
    z=[];k=0
    for ss in menu:z.append(pv[k:k+len(ss)]);k+=len(ss)
    x=[[[F(0)]*m for _ in ss] for ss in menu]
    for edge,q in zip(keys,pv[sc:]):g,s,u=edge;x[g][s][u]=q
    feasible(menu,z,x)
    a={edge:-q for edge,q in zip(keys,du[:len(keys)])}
    b=[-q for q in du[len(keys):]];eta=[-q for q in de]
    assert min(a.values(),default=F(0))>=0 and min(b)>=0
    for (g,s,u),q in a.items():assert q+b[u]>=menu[g][s][u]
    for g,ss in enumerate(menu):
        for s in range(len(ss)):assert eta[g]>=sum(q for (gg,ss_,u),q in a.items() if gg==g and ss_==s)
    pval=value(menu,x);dval=sum(b)+sum(eta)
    assert pval==dval==F(cert['objective'])
    return z,x,pval

certificates=0
for row in data['general_cases']:
    menu=frac(row['menu']);z,x,val=semantic_dual(menu,row['lp_certificate'])
    assert z==frac(row['z']) and x==frac(row['x'])
    certificates+=1
for row in data['coin_cases']:
    menu=frac(row['menu']);_,_,val=semantic_dual(menu,row['optimal_lp_certificate'])
    z,x=frac(row['z']),frac(row['x']);feasible(menu,z,x)
    assert value(menu,x)==val==1
    certificates+=1

# Do not import the file: compile/exec creates no __pycache__ in the repo.
ns={'__name__':'scratch_reviewed_module','__file__':str(TARGET)}
exec(compile(raw,str(TARGET),'exec'),ns)
expect_calls=0
def independently_enumerated_expectation(menu,z,x,states,bits):
    global expect_calls
    expect_calls+=1
    total=F(0)
    for u in range(len(menu[0][0])):
        all_outcomes=[]
        for g,ss in enumerate(menu):
            group=[]
            for s,state in enumerate(ss):
                ps=z[g][s] if states[g] is None else F(s==states[g])
                if not ps:continue
                p=state[u]
                if not p:group.append((F(0),ps));continue
                if (g,u) in bits:
                    group.append((p if bits[g,u] else F(0),ps))
                else:
                    coin=x[g][s][u]/z[g][s]
                    if coin:group.append((p,ps*coin))
                    if coin!=1:group.append((F(0),ps*(1-coin)))
            assert sum(prob for v,prob in group)==1
            all_outcomes.append(group)
        for outcome in product(*all_outcomes):
            probability=F(1)
            for v,prob in outcome:probability*=prob
            total+=max(v for v,prob in outcome)*probability
    return total

ns['expected_max_sum']=independently_enumerated_expectation
rounds=0
for section in ['support_cases','general_cases','coin_cases','large_denominator_cases']:
    for row in data[section]:
        menu=frac(row['menu']);z=frac(row.get('z',row.get('lambda')))
        x=frac(row['x']) if 'x' in row else [[[z[g][s] if p else F(0) for p in state] for s,state in enumerate(ss)] for g,ss in enumerate(menu)]
        feasible(menu,z,x)
        out=ns['round_welfare'](menu,z,x,support=section=='support_cases')
        wanted=F(row.get('output_welfare',row.get('welfare')))
        assert out['welfare']==wanted
        if 'initial_expectation' in row:assert out['initial_expectation']==F(row['initial_expectation'])
        # Independent all-job peak calculation; all zero jobs count as jobs.
        if section=='support_cases':
            H=[g for g,v in enumerate(out['values']) if v>=F(3,8)]
            expected_peak,_=ns['gate_schedule'](menu,out,(F(3,8),H))
        else:
            _,H=ns['balanced'](out['values']);expected_peak,_=ns['gate_schedule'](menu,out)
        H=set(H);n=len(menu);loads={('R',):F(1)}
        job_count=1
        for g,ss in enumerate(menu):
            loads['X',g]=F(1)
            if g not in H:loads['R',]+=F(1,n)
            job_count+=2
            for s,state in enumerate(ss):
                loads['M',g,s]=F(g in H and s==out['states'][g])
                for u,p in enumerate(state):
                    job_count+=1
                    exports=g in H and s==out['states'][g] and p and u in out['bundles'][g]
                    if exports:loads['Q',u]=loads.get(('Q',u),F(0))+1
                    else:loads['M',g,s]+=p
        assert job_count==1+2*n+sum(len(ss)*len(menu[0][0]) for ss in menu)
        assert max(loads.values())==expected_peak==F(row['peak'])
        assert all(v<=1 for k,v in loads.items() if k[0]=='Q')
        rounds+=1

def independent_resource_opt(menu):
    n=len(menu);m=len(menu[0][0]);beta=F(0);welfare=F(0)
    for owners in product(range(-1,n),repeat=m):
        vals=[max(sum(state[u] for u,g_ in enumerate(owners) if g_==g) for state in ss) for g,ss in enumerate(menu)]
        welfare=max(welfare,sum(vals));vals.sort(reverse=True)
        beta=max(beta,max(min(F(k,n),vals[k-1]) for k in range(1,n+1)))
    return welfare,beta,(n+1)**m

def independent_job_lists(menu,gated=True):
    n=len(menu);m=len(menu[0][0]);jobs=[]
    if gated:jobs.append({('root',):F(1)})
    for g,ss in enumerate(menu):
        if gated:jobs.append({('root',):F(1,n),('gate',g):F(1)})
        selector={('private',g,s):F(1) for s in range(len(ss))}
        if gated:selector['gate',g]=F(1)
        jobs.append(selector)
        for s,state in enumerate(ss):
            for u,p in enumerate(state):jobs.append({('private',g,s):p,('resource',u):F(1)})
    return jobs

def independent_full_um_enumeration(menu,gated=True):
    jobs=independent_job_lists(menu,gated);best=None;count=0
    for choices in product(*(list(job.items()) for job in jobs)):
        loads=defaultdict(F)
        for machine,p in choices:loads[machine]+=p
        peak=max(loads.values());best=peak if best is None else min(best,peak);count+=1
    return best,count

# Regenerate only the deterministic input stream; independent matrix/enumeration below.
rng=random.Random(20261018)
for k in range(36):ns['feasible_support_example'](rng,1+k%4,1+k%4+k%3,1+k%3)
for k in range(72):ns['random_menu'](rng,1+k%3,1+(k//3)%5,1+(k//15)%3)
full_counts=[]
for k,row in enumerate(data['brute_um_cases']):
    menu=ns['random_menu'](rng,1+k%2,1+(k//2)%2,1+(k//4)%2)
    _,beta,allocs=independent_resource_opt(menu)
    optimum,completions=independent_full_um_enumeration(menu)
    assert beta==F(row['beta_opt']) and optimum==F(row['um_opt'])==2-beta
    assert allocs==row['resource_allocations']
    full_counts.append(completions)

control=[[[F(1)]],[[F(1)]]]
flat,flat_count=independent_full_um_enumeration(control,False)
gated,gated_count=independent_full_um_enumeration(control,True)
assert (flat,flat_count,gated,gated_count)==(F(2),4,F(3,2),64)
assert F(data['flat_negative_control']['flat_opt'])==flat
assert F(data['flat_negative_control']['gated_opt'])==gated
assert len(data['large_denominator_cases'])==2
for row in data['large_denominator_cases']:
    menu=frac(row['menu']);z,x=frac(row['z']),frac(row['x'])
    welfare,beta,_=independent_resource_opt(menu)
    # LP upper bound one follows from the identical normalized rows of each
    # fixture: weighted resource capacity (two groups), or group norm (n=1).
    assert value(menu,x)==welfare==1
    assert beta==F(row['beta_opt'])

path=DATA
before=hashlib.sha256(path.read_bytes()).hexdigest()
run=subprocess.run([sys.executable,str(TARGET),'--output',str(path)],capture_output=True,text=True)
assert run.returncode==2 and 'refusing to overwrite frozen output' in run.stderr
assert hashlib.sha256(path.read_bytes()).hexdigest()==before
assert hashlib.sha256(TARGET.read_bytes()).hexdigest()==EXPECTED
result={'code_sha256':EXPECTED,'semantic_primal_dual_certificates':certificates,
        'all_rounding_cases_with_independent_outcome_expectation':rounds,
        'independent_expectation_calls':expect_calls,'all_jobs_load_rechecks':rounds,
        'independently_complete_um_instances':len(full_counts),
        'complete_legal_schedule_counts':full_counts,'total_complete_schedules':sum(full_counts),
        'negative_control':{'flat_opt':str(flat),'flat_assignments':flat_count,'gated_opt':str(gated),'gated_assignments':gated_count},
        'large_denominator_fixtures':2,'existing_output_rejected_exit':run.returncode,
        'existing_output_sha256_unchanged':before,'scope':'Replay of the named frozen data; not a general solver'}
with args.output.open('x') as stream:
    stream.write(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
