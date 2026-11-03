"""Read every primary JSON leaf; check saved arithmetic without solving any LP.

Native row builders are loaded in memory with ROOT explicitly redirected to the
preserved dependency. No native main runs and no original file is overwritten.
The sole dynamic-programming check uses the saved integer catalogue and stops
at the recorded first failed prefix; it does not enumerate a full root tree.
"""
from pathlib import Path
from fractions import Fraction as F
from collections import defaultdict
import ast, hashlib, itertools, json, math, sys
import numpy as np

HERE = Path(__file__).resolve().parent
ORIG = HERE / 'original'
INPUT = HERE / 'dependencies/five_player_indexed_bound.json'
out = {'scope': 'saved-data consistency, exact feedback identity and narrow exclusion; no LP optimization', 'json_files': {}}

def leaves(x):
    if isinstance(x, dict):
        return sum(leaves(k) + leaves(v) for k, v in x.items())
    if isinstance(x, list):
        return sum(map(leaves, x))
    if isinstance(x, float):
        assert math.isfinite(x)
    return 1

saved = {}
for p in sorted(ORIG.glob('*.json')):
    data = json.loads(p.read_text()); saved[p.name] = data
    out['json_files'][p.name] = {'bytes': p.stat().st_size, 'leaves_with_keys': leaves(data), 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()}

primal = json.loads(INPUT.read_text())['primal']
atoms = primal['atoms']; N = len(atoms); assert N == 64
r = [F(a['mass_numerator'], primal['denominator']) for a in atoms]
bits = [list(map(int, a['bits'])) for a in atoms]
assert all(sum(a['AB_hist'][4:]) == 1 for a in atoms)
u = [sum(rr * F(b[j], sum(b[:5])) for rr,b in zip(r,bits) if b[j]) for j in range(5)]

def load_functions(filename, names, ns):
    tree = ast.parse((ORIG / filename).read_text())
    nodes = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name in names]
    assert len(nodes) == len(names)
    exec(compile(ast.Module(body=nodes, type_ignores=[]), filename, 'exec'), ns)

class InputRoute:
    def __truediv__(self, ignored): return INPUT
ns = {'F': F, 'json': json, 'ROOT': InputRoute()}
load_functions('max_topic_security.py', ['build'], ns)
load_functions('universal_punisher.py', ['extra'], ns)

def check_float(A, b, c, record, xkey='x', dualkey='dual', E=None, f=None, upper=None):
    A=np.array(A,float); b=np.array(b,float); c=np.array(c,float)
    x=np.array(record[xkey],float); y=np.array(record[dualkey],float)
    lo=np.array(record['lower' if 'lower' in record else 'dual_lower'],float)
    hi=np.array(record['upper' if 'upper' in record else 'dual_upper'],float)
    assert A.shape == (len(b),len(x)) and len(y)==len(b) and len(lo)==len(x)==len(hi)
    upper=np.ones(len(x)) if upper is None else np.array(upper,float)
    eq = np.zeros(len(x)); eqobj=0.; eqviol=0.
    if E is not None:
        E=np.array(E,float); f=np.array(f,float); z=np.array(record['dual_eq'],float)
        assert E.shape==(len(f),len(x)) and len(z)==len(f)
        eq=E.T@z; eqobj=float(f@z); eqviol=float(np.max(abs(E@x-f)))
    bounds_violation=max(0.,float(-min(x[:-1] if math.isinf(upper[-1]) else x)),float(max((x-upper)[np.isfinite(upper)])))
    pviol=max(0.,float(max(A@x-b)),eqviol,bounds_violation)
    stat=float(max(abs(c-A.T@y-eq-lo-hi)))
    dobj=float(b@y)+eqobj+sum(v*w for v,w in zip(upper,hi) if math.isfinite(v))
    gap=float(c@x)-dobj
    assert pviol<1e-10 and stat<1e-10 and abs(gap)<1e-10, (pviol,stat,gap)
    assert min(lo)>-1e-10 and max(hi)<1e-10 and max(y)<1e-10
    return {'rows':len(b),'variables':len(x),'max_float_primal_violation':pviol,'max_float_stationarity_error':stat,'float_primal_dual_gap':gap,'objective':float(c@x)}

out['max_topic_saved'] = []
for last, rec in enumerate(saved['max_topic_security_proposal.json']):
    assert rec['last_reply'] == ('ABCDEUVWXY'[last] if last<10 else 'T0')
    if 'x' not in rec:
        assert 'infeasible' in rec['status'].lower()
        out['max_topic_saved'].append({'last_reply':rec['last_reply'],'status':'native saved infeasible; no Farkas certificate supplied'})
        continue
    *_, rows,rhs,names,own = ns['build'](last)
    check=check_float(rows,rhs,own,rec)
    assert abs(check['objective']-rec['minimum_T0_payoff_proposal'])<1e-12
    assert abs(float(u[3])-rec['onpath_D'])<1e-12
    assert abs(check['objective']-float(u[3])-rec['margin_proposal'])<1e-12
    out['max_topic_saved'].append({'last_reply':rec['last_reply'],**check})

out['universal_saved'] = []
exact = saved['universal_punisher_exact.json']
assert exact['fixed_bad_deviations']==['E','V','W','X','Y'] and exact['single_shared_reply']=='T0'
for last,(rec,cert) in enumerate(zip(saved['universal_punisher_proposal.json'],exact['fixed_last_reply_certificates'])):
    *_, rows,rhs,names,own = ns['extra'](last)
    assert rec['last_reply']==last and rec['names']==names and len(names)==38
    A=[row+[F(-1)] for row in rows]
    check=check_float(A,rhs,[0]*64+[1],rec,upper=[1]*64+[math.inf])
    assert rec['x'][-1]>=0 and abs(check['objective']-rec['minimum_common_violation'])<1e-12
    mu={name:F(value) for name,value in cert['multipliers'].items()}
    assert sum(mu.values())==1 and min(mu.values())>0
    aa=[sum(v*rows[names.index(name)][j] for name,v in mu.items()) for j in range(64)]
    bb=sum(v*rhs[names.index(name)] for name,v in mu.items())
    kappa=sum(min(F(0),v) for v in aa)-bb
    assert cert['last_reply']==('ABCDEUVWXY'[last] if last<10 else 'T0')
    assert [str(v) for v in aa]==cert['linear_coefficients'] and str(bb)==cert['weighted_rhs']
    assert kappa>0 and str(kappa)==cert['minimum_common_violation_at_least']
    assert float(kappa)==cert['minimum_common_violation_decimal']
    out['universal_saved'].append({'last_reply':cert['last_reply'], 'exact_kappa':str(kappa),**check})
fixed = sum(rr*F(b[7],sum(b[j] for j in (0,1,2,6))+1) for rr,b in zip(r,bits))
margin=fixed-u[3]
assert str(margin)==exact['other_T_last_reply_margin'] and float(margin)==exact['other_T_last_reply_margin_decimal']
out['other_T']={'fixed_W_after_V':str(fixed),'D':str(u[3]),'margin':str(margin)}

# Rebuild the best partition's 55 inequalities and 64 equalities independently.
best=saved['best_alignment_proposal.json']; joint=saved['joint_alignment_proposal.json']
pn={'itertools':itertools}; load_functions('joint_alignment.py',['partitions'],pn)
parts=list(pn['partitions'](5)); assert len(parts)==52 and [list(p) for p in parts]==[q['partition'] for q in joint['results']]
assert joint['partitions']==52 and joint['branches']==[4,6,7,8,9]
success=[q for q in joint['results'] if 'minimum_common_IC_violation' in q]
assert min(q['minimum_common_IC_violation'] for q in success)==joint['minimum_proposal']==best['delta']
assert best['partition']==[0]*5 and len(best['x'])==321
rows=[];rhs=[]
for j in range(5):
    for i in range(5):
        z=[F(0)]*321
        for k,(rr,b) in enumerate(zip(r,bits)): z[5*k+j]=rr/F(sum(b[:i])+5-i)
        rows.append(z);rhs.append(u[i])
for dev,j in zip(joint['branches'],best['partition']):
    load=[sum(b[i] for i in (0,1,2,dev)) for b in bits]
    g=[rr/F(ll+1) for rr,ll in zip(r,load)]
    fixedmax=max(sum(rr*F(b[t],ll+1) for rr,b,ll in zip(r,bits,load)) for t in range(10))
    z=[F(0)]*321
    for k,v in enumerate(g): z[5*k+j]=-v
    rows.append(z);rhs.append(-fixedmax)
    for ell in range(5):
        if ell==j: continue
        z=[F(0)]*321
        for k,v in enumerate(g):z[5*k+ell]=v;z[5*k+j]=-v
        rows.append(z);rhs.append(F(0))
    z=[F(0)]*321
    for k,(rr,b,ll) in enumerate(zip(r,bits,load)):
        if b[dev]:z[5*k+j]=-rr/F(ll*(ll+1))
    z[-1]=-1;rows.append(z)
    rhs.append(u[3]-sum(rr*F(b[dev],ll) for rr,b,ll in zip(r,bits,load) if b[dev]))
E=[]
for k in range(64):
    z=[F(0)]*321
    for j in range(5):z[5*k+j]=1
    E.append(z)
best_record={**best,'lower':best['dual_lower'],'upper':best['dual_upper'],'dual':best['dual_ub']}
# Delta has box [-2,2]; shift it to [0,4] for the generic checker.
shifted={**best_record,'x':best['x'][:-1]+[best['x'][-1]+2]}
shift_rhs=[b+2*row[-1] for row,b in zip(rows,rhs)]
out['joint_best']=check_float(rows,shift_rhs,[0]*320+[1],shifted,E=E,f=[1]*64,upper=[1]*320+[4])
out['joint_best']['original_objective']=best['delta']
out['joint_summary']={'partitions':52,'saved_success':len(success),'saved_infeasible':52-len(success),'negative_saved_objectives':sum(q['minimum_common_IC_violation']<0 for q in success)}

# Verify all integer catalogue rows by reproducing only the arithmetic lift.
ts=[F(best['x'][5*k]).limit_denominator(10**6) for k in range(64)]
coeff=[rr/F(sum(b[:4])+1) for rr,b in zip(r,bits)]
residual=sum(g*t for g,t in zip(coeff,ts))-u[4]
pivot=next(k for k,t in enumerate(ts) if F(1,10)<t<F(9,10))
ts[pivot]-=residual/coeff[pivot]
assert all(0<=t<=1 for t in ts) and sum(g*t for g,t in zip(coeff,ts))==u[4]
masses=defaultdict(F)
for k,a in enumerate(atoms):
    base=sum(int(v)<<i for i,v in enumerate(a['bits']))
    for member,prob in ((0,1-ts[k]),(1,ts[k])):
        if not prob:continue
        choices=list(itertools.combinations(range(1,5),1-member))
        for choice in choices:
            mask=base+sum(1<<(10+j) for j in choice)+(member<<10)
            masses[mask]+=r[k]*prob/len(choices)
den=math.lcm(*(v.denominator for v in masses.values()))
counts={m:int(v*den) for m,v in masses.items()};gg=math.gcd(*counts.values())
expected={'topics':list('ABCDEUVWXY')+['T'+str(i) for i in range(5)],'customers':[{'topics':[i for i in range(15) if m>>i&1],'multiplicity':n//gg} for m,n in sorted(counts.items())],'players':5}
assert expected==saved['aligned_catalog_instance.json']
out['realization']={'pivot_zero_based':pivot,'rational_repair':str(residual),'customer_types':len(counts),'unit_customers':sum(c['multiplicity'] for c in expected['customers']),'scale_relative_to_old_mass':str(F(den,gg)),'each_customer_in_exactly_one_T':True,'all_saved_integer_rows_reconstructed':True}

an={'F':F,'product':itertools.product}; load_functions('audit_feedback_identity.py',['u','P','audit'],an)
for key,k in [('FF',4),('FF5',5)]:
    assert an['audit'](k)==saved['audit_feedback_identity.json'][key]
out['feedback_identity']={key:saved['audit_feedback_identity.json'][key] for key in ('FF','FF5')}

sys.path.insert(0,str(HERE/'dependencies'))
from customer_attraction import Instance, ExactSPESolver
inst=Instance.from_dict(expected); solver=ExactSPESolver(inst); target=(1,)*5+(0,)*10
report=[]
for depth in range(4,-1,-1):
    prefix=tuple(int(j<depth) for j in range(15)); R=solver.outcomes(prefix)
    actual=inst.topic_payoff(depth,target);thr=solver.threshold(prefix)
    rec={'prefix':list(inst.topics[:depth]),'desired_tail_feasible':target in R,'threshold':str(thr),'on_path_payoff':str(actual),'margin':str(actual-thr),'number_outcomes':len(R),'forcing_deviations':[]}
    if target not in R:
        for j in range(15):
            child=tuple(v+int(ell==j) for ell,v in enumerate(prefix)); Q=solver.outcomes(child)
            minimum=min(inst.topic_payoff(j,q) for q in Q)
            if minimum>actual:rec['forcing_deviations'].append({'topic':inst.topics[j],'gain':str(minimum-actual),'minimum_reply_counts':list(min(q for q in Q if inst.topic_payoff(j,q)==minimum))})
    report.append(rec)
    if target not in R:break
assert report==saved['aligned_catalog_prefix_audit.json']
out['canonical_prefix_audit']={'saved_report_equal':True,'prefixes':[r['prefix'] for r in report],'root_not_run':True,'stats':str(solver.stats)}
(HERE/'inspection.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k!='json_files'},ensure_ascii=False,indent=2))
