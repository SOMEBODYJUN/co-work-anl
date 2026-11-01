"""One new entry: complete727 primal + finite conditional factorization.

Reuses unchanged437 direct evaluator FUNCTION PREFIX, never its original CLI.
Two previously checked single-O rows, objectives/domain and217matching result
are reused at the identical69 SHA; there is no new69 matching enumeration.
No full-universe dual or optimizer is run.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product,combinations_with_replacement,permutations
from collections import defaultdict
import ast,json,hashlib
E=Path(__file__).resolve().parent;OUT=E/'new-727-primal-and-signature-factorization.json'
if OUT.exists():raise SystemExit('Successful entry exists; do not rerun')
P=E/'original/research/workspaces/customer-attraction/R-c4732bee2f7b4e50a70568170e3334ae/round5_pricing/exact_optimum_primal_terminal_cross.json'
assert hashlib.sha256(P.read_bytes()).hexdigest()=='e2caa8f504da61dd41c6980671f2ce3d0c715f5d4dcce4b16dd656af25363acb'
data=json.loads(P.read_text());prior=json.loads((E/'reused-evidence/HG-selected69-success.json').read_text())
assert prior['status']=='passed' and prior['point727']['input_sha256']==hashlib.sha256(P.read_bytes()).hexdigest()
old=prior['point727'];atoms=data['atoms'];assert len(atoms)==len(old['atom_records'])==69
helper=E/'formal-comparison/archives/customer-attraction/tools/evidence/five-player-indexed/tests/audits/customer_attraction_five_indexed.py'
nodes=[]
for n in ast.parse(helper.read_text()).body:
    if isinstance(n,ast.ImportFrom) and n.module=='pathlib':break
    nodes.append(n)
ns={};exec(compile(ast.Module(body=nodes,type_ignores=[]),str(helper),'exec'),ns)
spec=[('AB','AB_hist',3,(0,1)),('AE','AE_hist',3,(0,4)),('Sbranch','second_hist',4,(0,))]
patterns=['all_equal','query_equal','first_branch','second_branch','all_distinct']
def f(n,d):return F(n,d) if n else F(0)
def pq(q,z,w,B,C,K):
    return [(1,z+w,z*w),(q-1,B-z+C-w,K-z*w),
            (q-1,(q-1)*z+C-w,z*(C-w)),(q-1,B-z+(q-1)*w,(B-z)*w),
            ((q-1)*(q-2),(q-2)*(B-z+C-w),(B-z)*(C-w)-(K-z*w))]
def expand(atom,s):return [x for x,n in zip(product((0,1),repeat=s[2]),atom[s[1]]) for _ in range(n)]
def two_source(atom,s):
    ss=expand(atom,s);fixed=sum(int(atom['bits'][k]) for k in s[3]);pp=[fixed+sum(x[:-2]) for x in ss]
    hh=[f(x[-2]+x[-1],p+x[-2]+x[-1])+F(x[-2],(p+1)*(p+2)) for p,x in zip(pp,ss)]
    return ss,pp,hh
def pair_rows(p,H,target,m,n):
    q=len(p);B=sum(x[m] for x in target);C=sum(x[n] for x in target);K=sum(x[m]*x[n] for x in target);out=[F(0)]*5
    for pp,hh,x in zip(p,H,target):
        for k,(nn,L,M) in enumerate(pq(q,x[m],x[n],B,C,K)):out[k]+=nn*hh-F(L,pp+1)+F(M,(pp+1)*(pp+2))
    return out
names=list(data['slacks']);assert len(names)==727
reused={'crossfinal:AB:Sbranch:2O':F(old['M_separate_upper']),'crossfinal:AB:Sbranch:3O':F(old['N_separate_upper'])}
totals={n:F(0) for n in names};mat=[];new_coefficients=reused_coefficients=0
for ai,atom in enumerate(atoms):
    rec=old['atom_records'][ai];assert rec['atom']==ai and rec['AB_hist']==atom['AB_hist'] and rec['second_hist']==atom['second_hist'] and F(rec['mass'])==F(atom['exact_mass'])
    mass=F(atom['exact_mass']);bits=tuple(map(int,atom['bits']));his=[atom[s[1]] for s in spec]
    rows=ns['evaluate'](bits,his,atom['menus_lh'],include_second_correlations=True);assert len(rows)==437
    for s in spec:
        ss,p,H=two_source(atom,s)
        finalp=[sum(bits[k] for k in s[3])+sum(x[:-1]) for x in ss]
        for m in range(s[2]):
            B=sum(x[m] for x in ss)
            rows[f'{s[0]}:5:offdiag:{m}']=sum((F(4*x[-1]-B+x[m],pp+1) for x,pp in zip(ss,finalp)),F(0))
        for m,n in combinations_with_replacement(range(s[2]),2):
            for pat,v in zip(patterns,pair_rows(p,H,ss,m,n)):rows[f'{s[0]}:pair:{m}{n}:{pat}']=v
    assert len(rows)==557
    for source in spec[:2]:
        ss,p,H=two_source(atom,source)
        for target in spec:
            if target[0]==source[0]:continue
            tt=expand(atom,target);assert [x[0] for x in ss]==[x[0] for x in tt]
            # Constant source background in each T-label makes any such
            # label-preserving order yield exactly the same pair cost.
            for m,n in combinations_with_replacement(range(target[2]),2):
                for pat,v in zip(patterns,pair_rows(p,H,tt,m,n)):rows[f'crosspair:{source[0]}:{target[0]}:{m}{n}:{pat}']=v
    assert len(rows)==717
    source=spec[0];ss=expand(atom,source);load=[bits[0]+bits[1]+x[0]+x[1] for x in ss];dd=[F(1,p+1) for p in load]
    A=sum((di*x[-1] for di,x in zip(dd,ss)),F(0));D=sum(dd,F(0))
    for target in spec[1:]:
        tt=expand(atom,target)
        for m in range(1,target[2]):
            K=sum(x[m] for x in tt);top=bottom=F(0)
            for t in (0,1):
                ds=sorted(di for di,x in zip(dd,ss) if x[0]==t);k=sum(x[m] for x in tt if x[0]==t)
                bottom+=sum(ds[:k],F(0));top+=sum(sorted(ds,reverse=True)[:k],F(0))
            dname=f'crossfinal:AB:{target[0]}:{m}D';oname=f'crossfinal:AB:{target[0]}:{m}O'
            rows[dname]=A-bottom
            if oname in reused:
                rows[oname]=F(rec['M_upper' if m==2 else 'N_upper']);reused_coefficients+=1
            else:rows[oname]=4*A-K*D+top
    assert len(rows)==727 and set(rows)==set(names)
    for n in names:
        if n not in reused:totals[n]+=mass*rows[n];new_coefficients+=1
    mat.append({'atom':ai,'mass':mass,'coefficients':[rows[n] for n in names]})
totals.update(reused)
assert new_coefficients==725*69==50025 and reused_coefficients==2*69==138
assert all(totals[n]==F(data['slacks'][n])>=0 for n in names)
assert F(old['W'])==F(data['welfare'])==1 and F(old['comparison_cover'])==F(data['comparison_cover'])>2

# New conditional-signature fixtures. Direct envelope costs use literal
# matching permutations; the conditioned side uses sorted support functions.
def comps(n,k):
    if k==1:yield(n,);return
    for j in range(n+1):
        for tail in comps(n-j,k-1):yield(j,)+tail
def states(hist,dim):return [t for t,n in zip(product((0,1),repeat=dim),hist) for _ in range(n)]
def actual(hist,dim,base):
    ss=states(hist,dim);p=[base+sum(t[:-1]) for t in ss]
    return ss,p,sum((F(t[-1],pp+1) for t,pp in zip(ss,p)),F(0))
def signature(hist,dim,base):
    ss,p,A=actual(hist,dim,base)
    return tuple(sum(t[0]==label and pp==c for t,pp in zip(ss,p)) for label in (0,1) for c in range(5))
def source_den(sig,label):return [F(1,c+1) for c in range(5) for _ in range(sig[label*5+c])]
def phi(sig,hist,dim,positions,alpha,beta):
    ss=states(hist,dim);D=sum((F(n,c%5+1) for c,n in enumerate(sig)),F(0))
    B=sum(b*sum(t[pos] for t in ss) for pos,b in zip(positions,beta));v=F(0)
    for label in (0,1):
        ds=sorted(source_den(sig,label),reverse=True)
        vv=sorted((sum((b-a)*t[pos] for pos,a,b in zip(positions,alpha,beta)) for t in ss if t[0]==label),reverse=True)
        assert len(ds)==len(vv);v+=sum((d*x for d,x in zip(ds,vv)),F(0))
    return -B*D+v
literal_envelope_evaluations=literal_assignments=0
def direct_envelope(sh,sd,sbase,th,td,positions,alpha,beta):
    global literal_envelope_evaluations,literal_assignments
    ss,p,A=actual(sh,sd,sbase);tt=states(th,td);groups=[]
    for label in (0,1):
        pp=[i for i,t in enumerate(ss) if t[0]==label];values=[tuple(t[pos] for pos in positions) for t in tt if t[0]==label]
        assert len(pp)==len(values);groups.append((pp,set(permutations(values))))
    best=None
    for choices in product(*(g[1] for g in groups)):
        assigned=[None]*len(ss)
        for (pp,_),vals in zip(groups,choices):
            for i,t in zip(pp,vals):assigned[i]=t
        value=F(0);q=len(ss)
        for j,(aa,bb) in enumerate(zip(alpha,beta)):
            diagonal=off=F(0)
            for i in range(q):
                diagonal+=F(ss[i][-1]-assigned[i][j],p[i]+1)
                for k in range(q):
                    if i!=k:off+=F(ss[i][-1]-assigned[k][j],p[i]+1)
            value+=aa*diagonal+bb*off
        best=value if best is None else max(best,value);literal_assignments+=1
    literal_envelope_evaluations+=1
    return best
def g(hist,dim):
    if dim==3:return sum(n*(2*t[0]*t[1]-t[2]) for n,t in zip(hist,product((0,1),repeat=3)))
    return sum(n*(t[0]-t[1]*t[2]+2*t[3]) for n,t in zip(hist,product((0,1),repeat=4)))
dims=[3,4]
edges=[(0,1,(2,3),(0,0),(1,1)),(1,0,(1,2),(1,0),(0,2)),(0,0,(1,2),(1,1),(0,0)),(1,1,(1,2,3),(1,0,0),(0,1,2))]
lambda_sets=[(1,1,1,1),(2,1,0,3)]
factor_cases=[];histogram_pair_evaluations=0
for q in (1,2):
    hs=[list(comps(q,2**dim)) for dim in dims]
    for d in range(q+1):
        allowed=[[h for h in hh if sum(n*t[0] for n,t in zip(h,product((0,1),repeat=dim)))==d] for hh,dim in zip(hs,dims)]
        for abit,bbit in product((0,1),repeat=2):
            bases=[abit+bbit,abit]
            fibers=[]
            for hh,dim,base in zip(allowed,dims,bases):
                ff=defaultdict(list)
                for h in hh:ff[signature(h,dim,base)].append(h)
                fibers.append(ff)
            for lambdas in lambda_sets:
                best_direct=None;direct_witness=None
                for h0,h1 in product(*allowed):
                    hist=[h0,h1];score=F(g(h0,3)+g(h1,4))
                    for lam,(s,t,pos,alpha,beta) in zip(lambdas,edges):
                        if lam:score+=lam*direct_envelope(hist[s],dims[s],bases[s],hist[t],dims[t],pos,alpha,beta)
                    histogram_pair_evaluations+=1
                    if best_direct is None or score>best_direct:best_direct=score;direct_witness=hist
                best_cond=None;signature_witness=None
                for sig0,sig1 in product(*[list(f) for f in fibers]):
                    sigs=[sig0,sig1];score=F(0)
                    for family in (0,1):
                        inner=[]
                        for h in fibers[family][sigs[family]]:
                            val=F(g(h,dims[family]));A=actual(h,dims[family],bases[family])[2]
                            for lam,(s,t,pos,alpha,beta) in zip(lambdas,edges):
                                if s==family:val+=lam*sum(a+(q-1)*b for a,b in zip(alpha,beta))*A
                                if t==family:val+=lam*phi(sigs[s],h,dims[family],pos,alpha,beta)
                            inner.append(val)
                        score+=max(inner)
                    if best_cond is None or score>best_cond:best_cond=score;signature_witness=sigs
                assert best_direct==best_cond
                factor_cases.append({'q':q,'common_T_count':d,'fixed_customer_bits_A_B':[abit,bbit],'source_fixed_loads':bases,'lambdas':lambdas,'allowed_histogram_counts':[len(v) for v in allowed],'signature_counts':[len(v) for v in fibers],'literal_maximum':best_direct,'conditioned_maximum':best_cond,'maximizing_histograms':direct_witness,'maximizing_signatures':signature_witness})
assert len(factor_cases)==40 and histogram_pair_evaluations==14464

def enc(v):
    if isinstance(v,F):return str(v)
    if isinstance(v,dict):return {k:enc(x) for k,x in v.items()}
    if isinstance(v,(tuple,list)):return [enc(x) for x in v]
    return v
result={'status':'passed','new_math_entry_attempts':1,'new_math_entry_successes':1,'failed_math_attempts':0,'original_CLI_entries':0,'external_solver_calls':0,
 'primal727':{'input_sha256':hashlib.sha256(P.read_bytes()).hexdigest(),'helper_sha256':hashlib.sha256(helper.read_bytes()).hexdigest(),'helper_scope':'AST function prefix reused437 direct evaluator only; no oldCLI/oldpoint ordual loop','atoms':69,'rows':727,'row_blocks':[437,10,110,160,10],'newly_evaluated_rows':725,'new_atom_coefficients':new_coefficients,'reused_rows':list(reused),'reused_atom_coefficients':reused_coefficients,'W_and_O_and_domain_reused_from_sameSHA_HG':True,'W':old['W'],'comparison_cover':old['comparison_cover'],'zero_slacks':sum(v==0 for v in totals.values()),'minimum_slack':min(totals.values()),'all727_values_match_original_report':True,'row_order':names,'total_slacks':totals,'atom_matrix':mat,'reused217matching_experiment_new_runs':0,'fulluniverse_dual_or_optimum_new_certification':False},
 'signature_factorization':{'q_values':[1,2],'family_dimensions':dims,'shared_anchor_membership_first_coordinate':True,'edges':edges,'has_self_loops_and_two_family_cycle':True,'all_common_T_count_cases_retained':True,'fixed_customer_A_B_bits_all4':True,'lambda_sets':lambda_sets,'conditional_maximum_cases':len(factor_cases),'histogram_pair_evaluations':histogram_pair_evaluations,'literal_joint_envelope_evaluations':literal_envelope_evaluations,'literal_matching_assignments':literal_assignments,'cases':factor_cases,'not_real_SPE_fixtures':True,'not_full_fiveplayer_universe_dual_pricing':True},
 'unexecuted_original_contracts':['parentfirst60full557audit','parentfinal61full717audit','all4fulluniverseduals','65/76primalchecks','18/36stepfractionalpriceprobes','originalsignature13952tuple24maximaaudit'],
 'scope':'Combined sameSHA reuse and new complete727 primal check, plus finite literal-vs-conditioned signature maxima. General factorization proved analytically; no root welfare payment or fullSPE/OPT realization.'}
OUT.write_text(json.dumps(enc(result),ensure_ascii=False,indent=2)+'\n')
print(json.dumps(enc({'status':'passed','new727_rows':725,'reused_rows':2,'primal_atoms':69,'zero_slacks':sum(v==0 for v in totals.values()),'conditional_maxima':len(factor_cases),'histogram_pairs':histogram_pair_evaluations,'literal_envelopes':literal_envelope_evaluations,'literal_matchings':literal_assignments,'new217runs':0,'original_CLI':0,'solver_calls':0}),ensure_ascii=False))
