"""One small phase-I LP on the fixed certified 92-atom old network.

d[a,i] is actual joint mass of atom a and D_i, with 0 <= d[a,i] <= m[a].
The single S6 symmetrization moves old words, old nodes and all D names together.
No min auxiliary is used as a physical overlap in any payoff row.
"""
from collections import defaultdict
from fractions import Fraction as Q
from pathlib import Path
import json,time
import numpy as np
import scipy
from scipy.optimize import linprog
from scipy.sparse import lil_matrix
from analyze import HERE,WORK,POINT,NETWORK,POINT_SHA,NODES,read,canon,sha,dump

def sparse(d):return [[k,str(v)] for k,v in sorted(d.items()) if v]

def main():
    data,_=read();nw=json.loads(NETWORK.read_bytes());assert nw['point_sha256']==POINT_SHA
    assert nw['literal_node_order']==[list(e) for e in NODES]
    boolean=json.loads((HERE/'boolean_analysis.json').read_bytes())
    assert boolean['status']=='NO_BOOLEAN_OR_MARGINAL_ORDER_OBSTRUCTION'
    graphs={r['hist_column']:r for r in boolean['hist_records'] if not r['vacuous']}
    variables=[];varid={};atoms=[];bounds=[];blockers=[]
    for block in nw['blocks']:
        h=block['hist_column'];d=data[h];g=graphs[h]
        assert block['hist']==d['hist']['hist'] and block['actual_bits']==d['hist']['actual_bits']
        for ai,a in enumerate(block['atoms']):
            mass=Q(a['mass']);known=a['B4_state']+[s//2 for s in a['states']]+[s%2 for s in a['states']]
            atoms.append(dict(hist_column=h,atom_index=ai,**a))
            for i in range(6):
                allowed=[];why={}
                for bit in (0,1):
                    ok=True
                    for ci,c in enumerate(g['clauses']):
                        ls=c['literals'];ds={l//2-135 for l in ls if l//2>=135}
                        assert len(ds)<=1
                        if ds and ds!={i}:continue
                        vals=[known[l//2] if l//2<135 else bit for l in ls]
                        if not any(v==l%2 for v,l in zip(vals,ls)):
                            ok=False;why[bit]=ci;break
                    if ok:allowed.append(bit)
                assert allowed,('Fixed network atom excluded by exact zero-face logic',h,ai,i)
                v=len(variables);varid[h,ai,i]=v
                variables.append(dict(hist_column=h,atom_index=ai,index=i,mass=mass,word=d['words'][i],allowed_bits=allowed))
                bounds.append((mass if allowed==[1] else Q(),Q() if allowed==[0] else mass))
                blockers.append(why)
    assert len(atoms)==92 and len(variables)==552
    eq=[]
    for h,d in data.items():
        h_atoms=[a for a in atoms if a['hist_column']==h]
        for w,xx in d['x'].items():
            ids=[i for i,word in enumerate(d['words']) if word==w]
            rr={varid[h,a['atom_index'],i]:Q(1) for a in h_atoms for i in ids}
            eq.append(dict(name=['D-marginal',h,*w],row=sparse(rr),rhs=xx*len(ids)))
    triple=defaultdict(list)
    for i in range(6):
        for e,(f,j,k) in enumerate(NODES):triple[f,canon((i,j,k))].append((i,e))
    inequalities=[]
    for o,ms in sorted(triple.items()):
        rr=defaultdict(Q);rhs=Q()
        for a in atoms:
            h=a['hist_column'];d=data[h];P=sum(d['a'][:4]);mass=Q(a['mass']);ai=a['atom_index']
            for i,e in ms:
                r,z=divmod(a['states'][e],2);fac=Q(1,len(ms)*(P+r+1))
                rhs+=mass*z*fac;rr[varid[h,ai,i]]+=fac
        inequalities.append(dict(name=['Z-to-D',*o],row=sparse(rr),rhs=rhs))
    rr=defaultdict(Q);rhs=Q()
    for a in atoms:
        h=a['hist_column'];d=data[h];s=a['B4_state'];den=sum(d['a'][:3])+d['a'][5]+s[0]+1;mass=Q(a['mass'])
        rhs+=mass*Q(s[1],den)
        for i in range(6):rr[varid[h,a['atom_index'],i]]+=Q(1,6*den)
    inequalities.append(dict(name=['F-to-D'],row=sparse(rr),rhs=rhs))
    model=dict(scope='Fixed certified 92-atom network extension, uniform synchronous S6, one D conditional mass per atom and named index',
               point_sha256=POINT_SHA,network_sha256=sha(NETWORK),D_marginals_sha256=sha(WORK/'fifth_reply_interface/D_marginals.json'),
               boolean_analysis_sha256=sha(HERE/'boolean_analysis.json'),variables=variables,bounds=bounds,forbidden_bit_clause_witnesses=blockers,
               equalities=eq,inequalities=inequalities,inequality_convention='row dot d <= rhs',
               conditional_gluing='Given an old network atom, independently choose six Bernoulli D bits with probabilities d[a,i]/mass[a], then apply each permutation with mass divided by 720.')
    dump(HERE/'fixed_network_lp.json',model)
    n=len(variables);ae=lil_matrix((len(eq),n+1));au=lil_matrix((len(inequalities),n+1))
    for k,r in enumerate(eq):
        for j,v in r['row']:ae[k,j]=float(Q(v))
    for k,r in enumerate(inequalities):
        for j,v in r['row']:au[k,j]=float(Q(v))
        au[k,n]=-1.
    c=np.zeros(n+1);c[n]=1
    t=time.perf_counter()
    res=linprog(c,A_ub=au.tocsr(),b_ub=np.array([float(r['rhs']) for r in inequalities]),
                A_eq=ae.tocsr(),b_eq=np.array([float(r['rhs']) for r in eq]),
                bounds=[(float(lo),float(hi)) for lo,hi in bounds]+[(0,None)],method='highs',
                options={'time_limit':60,'primal_feasibility_tolerance':1e-9,'dual_feasibility_tolerance':1e-9})
    elapsed=time.perf_counter()-t
    result=dict(scope=model['scope'],optimizer_calls=1,scipy_version=scipy.__version__,status=int(res.status),success=bool(res.success),
                message=res.message,iterations=int(res.nit),elapsed_seconds=elapsed,script_sha256=sha(Path(__file__)),
                model_sha256=sha(HERE/'fixed_network_lp.json'),objective=None if res.fun is None else float(res.fun),
                variables=n,forced_endpoint_variables=sum(lo==hi for lo,hi in bounds),free_variables=sum(lo<hi for lo,hi in bounds),
                equality_rows=len(eq),true_payoff_rows=len(inequalities))
    if res.x is not None:
        result.update(x=res.x.tolist(),equality_residuals=res.eqlin.residual.tolist(),inequality_residuals=res.ineqlin.residual.tolist(),
                      equality_duals=res.eqlin.marginals.tolist(),inequality_duals=res.ineqlin.marginals.tolist(),
                      lower_duals=res.lower.marginals.tolist(),upper_duals=res.upper.marginals.tolist())
    dump(HERE/'phase_I_discovery.json',result)
    print(json.dumps({k:v for k,v in result.items() if k not in ('x','equality_residuals','inequality_residuals','equality_duals','inequality_duals','lower_duals','upper_duals')}))

if __name__=='__main__':main()
