"""Exact endpoint/active-equation recovery and finite conditional-product gluing."""
from fractions import Fraction as Q
from itertools import product
from math import lcm
from pathlib import Path
import json
from analyze import HERE,WORK,NETWORK,POINT_SHA,sha,dump

def main():
    model=json.loads((HERE/'fixed_network_lp.json').read_bytes())
    num=json.loads((HERE/'phase_I_discovery.json').read_bytes())
    assert num['success'] and abs(num['objective'])<1e-9 and num['optimizer_calls']==1
    assert num['model_sha256']==sha(HERE/'fixed_network_lp.json')
    n=len(model['variables']);bounds=[tuple(map(Q,b)) for b in model['bounds']]
    exact=[None]*n;unknown=[];endpoint_records=[]
    for j,(lo,hi) in enumerate(bounds):
        v=num['x'][j];tol=1e-10*max(float(hi),1e-8)
        if lo==hi or abs(v-float(lo))<=tol:exact[j]=lo;endpoint_records.append([j,'lower'])
        elif abs(v-float(hi))<=tol:exact[j]=hi;endpoint_records.append([j,'upper'])
        else:unknown.append(j)
    ui={j:k for k,j in enumerate(unknown)};equations=[];origins=[]
    active=list(model['equalities'])
    active += [r for r,v in zip(model['inequalities'],num['inequality_residuals']) if abs(v)<1e-9]
    for r in active:
        row=[Q()]*(len(unknown)+1);rhs=Q(r['rhs'])
        for j,v in r['row']:
            vv=Q(v)
            if j in ui:row[ui[j]]+=vv
            else:rhs-=vv*exact[j]
        row[-1]=rhs;equations.append(row);origins.append(r['name'])
    pivots={};independent=[]
    for row,origin in zip(equations,origins):
        row=row.copy()
        for k,p in sorted(pivots.items()):
            if row[k]:
                q=row[k];row=[a-q*b for a,b in zip(row,p)]
        nz=next((k for k in range(len(unknown)) if row[k]),None)
        if nz is None:assert row[-1]==0,('Inconsistent active row',origin,row[-1]);continue
        q=row[nz];row=[v/q for v in row]
        pivots[nz]=row;independent.append(origin)
    assert len(pivots)==len(unknown),('Underdetermined exact recovery',len(pivots),len(unknown))
    sol=[Q()]*len(unknown)
    for k,row in sorted(pivots.items(),reverse=True):sol[k]=row[-1]-sum((row[j]*sol[j] for j in range(k+1,len(sol))),Q())
    for j,k in ui.items():exact[j]=sol[k]
    assert all(lo<=v<=hi for v,(lo,hi) in zip(exact,bounds))
    eqchecks=[];icchecks=[]
    for r in model['equalities']:
        v=sum((Q(a)*exact[j] for j,a in r['row']),Q())-Q(r['rhs']);assert v==0
        eqchecks.append(dict(name=r['name'],residual=v))
    for r in model['inequalities']:
        v=Q(r['rhs'])-sum((Q(a)*exact[j] for j,a in r['row']),Q());assert v>=0
        icchecks.append(dict(name=r['name'],slack=v,approx=float(v)))
    nw=json.loads(NETWORK.read_bytes());var={(v['hist_column'],v['atom_index'],v['index']):j for j,v in enumerate(model['variables'])}
    blocks=[];conditional=[];scale=1;total=Q();count=0
    for block in nw['blocks']:
        h=block['hist_column'];bb={k:v for k,v in block.items() if k!='atoms'};aa=[]
        for ai,a in enumerate(block['atoms']):
            mass=Q(a['mass']);dm=[exact[var[h,ai,i]] for i in range(6)];probs=[v/mass for v in dm]
            conditional.append(dict(hist_column=h,atom_index=ai,old_mass=mass,D_joint_masses=dm,D_conditional_probabilities=probs))
            subtotal=Q();subcount=0
            for bits in product(range(2),repeat=6):
                mm=mass
                for bit,p in zip(bits,probs):mm*=p if bit else 1-p
                if not mm:continue
                assert mm>0
                atom={k:v for k,v in a.items() if k!='mass'}
                atom.update(mass=mm,D_bits=bits,source_atom_index=ai)
                aa.append(atom);subtotal+=mm;count+=1;total+=mm;subcount+=1
                scale=lcm(scale,(mm/720).denominator)
            assert subtotal==mass
            conditional[-1]['positive_conditional_atoms']=subcount
        bb['atoms']=aa;blocks.append(bb)
    assert total==1
    witness={k:v for k,v in nw.items() if k not in ('scope','source_sha256','blocks','base_atoms','expanded_atoms','symmetrization')}
    witness.update(scope='One common old R/Z and same B4 network with six genuine fifth-source D coverage sets; no full SPE assertion',
                   source_sha256=sha(NETWORK),conditional_extension_sha256=sha(HERE/'fixed_network_lp.json'),
                   symmetrization='Each canonical atom is copied with mass/720 to every pi in S6; pi simultaneously moves old words, literal RZ node indices, and D index i to pi(i); actual and B4 bits stay fixed.',
                   blocks=blocks,base_atoms=count,expanded_atoms=720*count)
    dump(HERE/'common_atoms_with_D.json',witness)
    result=dict(status='EXACT_FEASIBLE',point_sha256=POINT_SHA,network_sha256=sha(NETWORK),
                model_sha256=sha(HERE/'fixed_network_lp.json'),discovery_sha256=sha(HERE/'phase_I_discovery.json'),script_sha256=sha(Path(__file__)),
                original_conditional_variables=n,endpoint_variables=len(endpoint_records),interior_variables=unknown,
                active_equations=len(active),rank=len(pivots),free_variables=0,independent_equation_names=independent,
                endpoint_records=endpoint_records,D_joint_masses=exact,equality_checks=eqchecks,true_payoff_checks=icchecks,
                conditional_distributions=conditional,old_atoms=92,canonical_positive_joint_atoms=count,
                expanded_positive_joint_atoms=720*count,total_mass=total,unit_customer_scale=str(scale),unit_customer_scale_digits=len(str(scale)),
                witness_sha256=sha(HERE/'common_atoms_with_D.json'),
                maximum_change_from_numeric=max(abs(float(v)-num['x'][j]) for j,v in enumerate(exact)))
    dump(HERE/'exact_extension.json',result)
    print(json.dumps({k:v for k,v in result.items() if k not in ('endpoint_records','D_joint_masses','conditional_distributions','unit_customer_scale','equality_checks','true_payoff_checks')}))
    print(json.dumps([dict(name=r['name'],slack=r['approx']) for r in icchecks]))

if __name__=='__main__':main()
