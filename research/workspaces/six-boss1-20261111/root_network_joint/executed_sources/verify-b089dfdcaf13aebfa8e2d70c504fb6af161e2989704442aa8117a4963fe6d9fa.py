"""Independent standard-library audit; imports no construction or optimizer.

Enumerate every positive six-root Cartesian column, recover both marginals,
and project only after that enumeration.  Literal true-node payoffs recover
all 458 rows.  Independently check every transportation primal/dual and the
two extended dual inequalities at every state in their full Boolean domains.
"""
from collections import Counter,defaultdict
from fractions import Fraction as F
from itertools import product,permutations
from math import prod,factorial,lcm
from pathlib import Path
import hashlib,json,time,sys

HERE=Path(__file__).resolve().parent;BASE=HERE.parent
PIN='b0ca65cfe61e5e3ef09537cba2a986c171aeaa7106f673077f803c80ee2b68e3'
MUPIN='9866e82bbc40e661d15d4aee3a4472fd99137ade5a9fa7fd0872f6344ffe0966'
NETPIN='91599404ee03184bbb072767d7d55761b95bcc89e1d55e748aebf2ee60f19c54'


def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def bits(s,n):return tuple(int(c) for c in format(s,'0'+str(n)+'b'))
def q(n,d):
    assert d or n==0
    return F(n,d) if n else F()
def freeze(v):return tuple(freeze(x) for x in v) if isinstance(v,list) else v
def canon(xs):
    names={}
    return tuple(names.setdefault(x,len(names)) for x in xs)
def serial(v):
    if isinstance(v,F):return str(v)
    if isinstance(v,dict):return {str(k):serial(x) for k,x in v.items()}
    if isinstance(v,(tuple,list)):return [serial(x) for x in v]
    return v
def pair_wallet(p,b,c):
    return F(b,p+1+c)+F(c,p+1+b)+F(b,(p+1)*(p+2))


def pair_row_coefficient(name,v,w,s,t):
    e,d=bits(s,5),bits(t,5);st,dt=v//4,w//4
    if name[0]=='cross-floor':
        k,l=name[1:]
        return q(e[k],st+sum(e))-F(d[l],st+sum(e[:k])+5-k)
    x,y=name[1:];pref=st+sum(e[:3]);donor=(dt,)+d
    return pair_wallet(pref,e[3],e[4])-F(donor[x]+donor[y],pref+1)+F(donor[x]*donor[y],(pref+1)*(pref+2))


def main():
    begin=time.monotonic()
    pointpath=BASE/'union_augmented_lp/augmented_lp_exact.json'
    mupath=BASE/'root_marginal_closure/marginal_completion_exact.json'
    netpath=BASE/'fifth_reply_common/common_atoms_with_D.json'
    assert sha(pointpath)==PIN and sha(mupath)==MUPIN and sha(netpath)==NETPIN
    point,mc,net=[json.loads(p.read_text()) for p in (pointpath,mupath,netpath)]
    saved=json.loads((HERE/'conditional_product_exact.json').read_text())
    bounds=json.loads((HERE/'fixed_mu_upper_bounds_exact.json').read_text())
    cuts=json.loads((HERE/'full32_obstruction_rows_exact.json').read_text())
    assert mc['point_sha256']==net['point_sha256']==saved['point_sha256']==PIN
    hist={j:c for j,c in enumerate(point['columns']) if c['kind']=='hist'}
    H={h:F(c['weight']) for h,c in hist.items()}
    words={h:tuple(w for w,n in enumerate(c['hist']) for _ in range(n)) for h,c in hist.items()}
    desc=[dict(hist=h,old_word=w,state=s) for h,c in hist.items() for w,n in enumerate(c['hist']) if n for s in range(32)]
    assert len(desc)==1216 and desc==cuts['mu_columns']
    mu={};groups=defaultdict(dict);positive=[]
    for j,(d,raw) in enumerate(zip(desc,mc['mu'])):
        value=F(raw);assert value>=0
        mu[d['hist'],d['old_word'],d['state']]=value
        if value:
            groups[d['hist'],d['old_word']][d['state']]=value
            positive.append(dict(column=j,**d,mass=str(value)))
    assert positive==mc['positive_states'] and len(positive)==35
    assert len(hist)==16 and sum(v>0 for v in H.values())==10
    for h,c in hist.items():
        assert c['d']==sum(c['hist'][4:])==1
        for w in set(words[h]):assert sum(groups[h,w].values(),F())==H[h]
    blocks={b['hist_column']:b for b in net['blocks']}
    nodes=tuple(e for e in product(range(2),range(6),range(6)) if e[0] or e[1]!=e[2])
    assert list(map(list,nodes))==net['literal_node_order'] and len(nodes)==66
    orbit=defaultdict(list)
    for i in range(6):
        for ei,(f,j,k) in enumerate(nodes):orbit[f,canon((i,j,k))].append((i,ei))
    perms=list(permutations(range(6)));frequency=0
    for o,indices in orbit.items():
        i,ei=indices[0];f,j,k=nodes[ei]
        cc=Counter((p[i],p[j],p[k]) for p in perms)
        expected={(ii,nodes[ee][1],nodes[ee][2]) for ii,ee in indices}
        assert set(cc)==expected and set(cc.values())=={720//len(indices)};frequency+=720
    for i,j in product(range(6),repeat=2):
        cc=Counter((p[i],p[j]) for p in perms)
        assert len(cc)==(6 if i==j else 30) and set(cc.values())=={120 if i==j else 24};frequency+=720
    # Enumerate the entire complete domain, before using any projection.
    network_margin=defaultdict(F);local=defaultdict(F);root_law=defaultdict(F)
    total=F();columns=0;denominator=1;domain=[]
    for h,c in hist.items():
        supports=[sorted(groups[h,w]) for w in words[h]]
        size=prod(map(len,supports));atoms=blocks.get(h,{}).get('atoms',[])
        domain.append((h,size,len(atoms),size*len(atoms)))
        if H[h]:
            assert blocks[h]['actual_bits']==c['actual_bits'] and blocks[h]['hist']==c['hist']
            assert sum((F(a['mass']) for a in atoms),F())==H[h]
        else:assert not atoms
        for ai,atom in enumerate(atoms):
            for ss in product(*supports):
                mass=F(atom['mass'])
                for w,s in zip(words[h],ss):mass*=groups[h,w][s]/H[h]
                assert mass>0
                network_margin[h,ai]+=mass;root_law[h,ss]+=mass;total+=mass;columns+=1
                denominator=lcm(denominator,(mass/720).denominator)
                for i,s in enumerate(ss):local[h,ai,i,s]+=mass
    assert columns==3086 and columns*720==2221920 and total==1
    assert sum(d[1] for d in domain)==1303
    assert [(d['hist'],d['full_named_root_vectors'],d['network_atoms'],d['canonical_joint_columns']) for d in saved['domain']]==domain
    for (h,ai),mass in network_margin.items():assert mass==F(blocks[h]['atoms'][ai]['mass'])
    assert len(network_margin)==100
    single=defaultdict(F)
    for (h,ai,i,s),mass in local.items():
        assert mass==F(blocks[h]['atoms'][ai]['mass'])*groups[h,words[h][i]][s]/H[h]
        single[h,i,s]+=mass
    for (h,i,s),mass in single.items():assert mass==groups[h,words[h][i]][s]
    pair=defaultdict(F)
    for (h,ss),mass in root_law.items():
        assert mass==H[h]*prod(groups[h,w][s]/H[h] for w,s in zip(words[h],ss))
        for i,j in product(range(6),repeat=2):
            if i!=j:pair[h,i,j,ss[i],ss[j]]+=mass
    for (h,i,j,s,t),mass in pair.items():
        assert mass==groups[h,words[h][i]][s]*groups[h,words[h][j]][t]/H[h]
    # Rebuild all original literal budgets with their own genuine sources.
    cap=next(F(c['weight']) for c in point['columns'] if c['kind']=='K')
    pays=[sum((H[h]*q(int(c['actual_bits'][i]),sum(map(int,c['actual_bits']))) for h,c in hist.items()),F()) for i in range(6)]
    assert sum(pays)==F(point['W']) and sum(H.values(),F())==F(point['O'])==1
    table={}
    for t in range(2):
        for r in json.loads((BASE/f'background_five_bridge/fixed53_b{t}_profit.json').read_text())['min_by_actual_and_d']:
            table[t,int(r['actual'],2),r['d']]=F(r['min_rho'])
    assert len(table)==384
    sums=defaultdict(F);sums['gamma',]=-F(226487,10**21)*cap-F(5,6)
    sums['root-source',]=pays[0]
    for k in range(5):
        sums['price',k]=pays[5];sums['capacity',k]=cap
        for i in range(5):sums['actual-floor',i,k]=pays[i]
    awallet=F()
    for h,c in hist.items():
        a=tuple(map(int,c['actual_bits']));awallet+=H[h]*pair_wallet(sum(a[:4]),a[4],a[5])
    for x in range(6):
        for y in range(x,6):sums['actual-pair',x,y]=awallet
    old_literal_evaluations=0
    for (h,i,s),mass in single.items():
        a=tuple(map(int,hist[h]['actual_bits']));ow=list(map(lambda w:bits(w,3),words[h]));t=ow[i][0]
        e=bits(s,5);totalroot=t+sum(e);factor=mass/6
        sums['gamma',]+=factor*(2*q(sum(e),totalroot)-table[t,s,1-t])
        sums['root-source',]-=factor*q(t,totalroot)
        for k in range(5):
            den=t+sum(e[:k])+5-k;pay=q(e[k],totalroot)
            sums['price',k]-=factor*F(e[k],sum(a[:5])+1)
            sums['capacity',k]-=factor*e[k]
            for j in range(6):sums['floor-actual',k,j]+=factor*(pay-F(a[j],den))
            sums['floor-other-opt',k]+=factor*(5*pay-F(1-t,den))
            sums['floor-root',k]+=factor*(pay-F(t,den))
            for l in range(5):
                if k!=l:sums['floor-own-tail',k,l]+=factor*(pay-F(e[l],den))
            for j in range(5):sums['actual-floor',j,k]-=factor*F(e[k],sum(a[:j])+6-j)
        donor=(t,)+e;ap=sum(a[:4])
        for x in range(6):
            for y in range(x,6):sums['actual-pair',x,y]-=factor*(F(donor[x]+donor[y],ap+1)-F(donor[x]*donor[y],(ap+1)*(ap+2)))
        pref=t+sum(e[:3]);nwallet=pair_wallet(pref,e[3],e[4])
        for j,(ot,b,c) in enumerate(ow):
            rel,norm=('same',6) if i==j else ('off',30)
            fac=mass/norm;p=sum(a[:3])+ot;owallet=pair_wallet(p,b,c)
            for k in range(5):
                sums['C-to-Y',k,rel]+=fac*F(c-e[k],p+b+1)
                sums['B-to-Y',k,rel]+=fac*(F(b,p+1+c)-F(e[k],p+2))
            sums['Y5-to-C',rel]+=fac*(q(e[4],totalroot)-F(c,t+sum(e[:4])+1))
            sums['Y5-to-B',rel]+=fac*(q(e[4],totalroot)-F(b,t+sum(e[:4])+1))
            for k in range(4):
                for label,member in (('B',b),('C',c)):
                    sums['Y-to-old',k,label,rel]+=fac*(q(e[k],totalroot)-F(member,t+sum(e[:k])+5-k))
            for k in range(5):
                for l in range(k,5):sums['old-pair-to-Y',k,l,rel]+=fac*(owallet-F(e[k]+e[l],p+1)+F(e[k]*e[l],(p+1)*(p+2)))
            for v,w,vb,wb in (('B','B',b,b),('B','C',b,c),('C','C',c,c)):
                sums['new-pair-to-old',v,w,rel]+=fac*(nwallet-F(vb+wb,pref+1)+F(vb*wb,(pref+1)*(pref+2)))
            old_literal_evaluations+=38
    cross_literal_evaluations=0
    for (h,i,j,s,t),mass in pair.items():
        v,w=words[h][i],words[h][j]
        for k,l in product(range(5),repeat=2):
            name=('cross-floor',k,l);sums[name]+=mass*pair_row_coefficient(name,v,w,s,t)/6;cross_literal_evaluations+=1
        for k in range(6):
            for l in range(k,6):
                name=('cross-pair',k,l);sums[name]+=mass*pair_row_coefficient(name,v,w,s,t)/30;cross_literal_evaluations+=1
    # Independent literal payoff numerators, grouped only by equal denominators.
    new_literal_evaluations=0
    for (h,ai,i,s),mass in local.items():
        atom=blocks[h]['atoms'][ai];a=tuple(map(int,hist[h]['actual_bits']));ow=list(map(lambda w:bits(w,3),words[h]))
        e=bits(s,5);t=ow[i][0];tot=t+sum(e);p3=sum(a[:3]);P=sum(a[:4])
        terms=defaultdict(lambda:defaultdict(int))
        def put(name,num,den):
            nonlocal new_literal_evaluations
            assert den or not num
            if num:terms[name][den]+=num
            else:terms[name]
            new_literal_evaluations+=1
        for ei,(f,j,k) in enumerate(nodes):
            r,z=divmod(atom['states'][ei],2);o=(f,canon((i,j,k)));norm=len(orbit[o])
            for l in range(5):
                den=t+sum(e[:l])+5-l
                put(('R-to-Y',o,l),r-e[l],norm*(p3+ow[j][0]+ow[k][1+f]+1))
                put(('Z-to-Y',o,l),z-e[l],norm*(P+r+1))
                for label,b in (('R',r),('Z',z)):
                    put(('Y-to-'+label,o,l),e[l],norm*tot)
                    put(('Y-to-'+label,o,l),-b,norm*den)
        h1,h2,_=atom['B4_state'];base=p3+a[5]
        for l in range(5):
            den=t+sum(e[:l])+5-l
            put(('F-to-Y',l),h2-e[l],6*(base+h1+1))
            put(('H1-safe-to-Y',l),h1,6*(base+h2+1));put(('H1-safe-to-Y',l),-e[l],6*(base+2))
            for label,b in (('H1',h1),('H2',h2)):
                put(('Y-to-'+label,l),e[l],6*tot);put(('Y-to-'+label,l),-b,6*den)
            for k in range(l,5):
                name=('B4-pair-to-Y',l,k)
                put(name,h1,6*(base+h2+1));put(name,h2,6*(base+h1+1))
                put(name,h1+e[l]*e[k],6*(base+1)*(base+2));put(name,-e[l]-e[k],6*(base+1))
        pref=t+sum(e[:3])
        for label,b,c in (('11',h1,h1),('12',h1,h2),('22',h2,h2)):
            name=('Y-pair-to-B4',label)
            put(name,e[3],6*(pref+1+e[4]));put(name,e[4],6*(pref+1+e[3]))
            put(name,e[3]+b*c,6*(pref+1)*(pref+2));put(name,-b-c,6*(pref+1))
        for j in range(6):
            rel,norm=('same',6) if i==j else ('off',30);d=atom['D_bits'][j]
            for l in range(5):
                put(('D-to-Y',l,rel),d-e[l],norm*(P+ow[j][0]+1))
                put(('Y-to-D',l,rel),e[l],norm*tot)
                put(('Y-to-D',l,rel),-d,norm*(t+sum(e[:l])+5-l))
        for name,denoms in terms.items():sums[name]+=mass*sum((F(n,d) for d,n in denoms.items()),F())
    assert len(sums)==458
    for row in saved['rows']:
        name=freeze(row['name']);assert sums[name]==F(row['slack']),(name,sums[name],row['slack'])
    assert sum(v<0 for v in sums.values())==7 and sum(v==0 for v in sums.values())==5
    assert sum(v>0 for v in sums.values())==446
    # Check upper bounds entirely from primal feasibility and dual domination.
    own={};cur=None;own_index={}
    for j,c in enumerate(point['columns'][:4849]):
        if c['kind']=='hist':cur=j
        elif c['kind']=='joint-reply':
            f,d,v,w=c['group'];key=(cur,f,d,tuple(v),tuple(w))
            own.setdefault(key,{})[tuple(c['state'])]=F(c['weight'])
            own_index.setdefault(key,{})[tuple(c['state'])]=j
    for key,ss in own.items():ss[0,0]=H[key[0]]-sum(ss.values(),F())
    transport_checks=0;dual_cells=0;negative_upper=[]
    for row in bounds['rows']:
        name=freeze(row['name']);bound=F()
        for p in row['pieces']:
            h=p['hist'];left={r['state']:F(r['mass']) for r in p['left']};right={r['state']:F(r['mass']) for r in p['right']}
            alpha={r['state']:F(r['dual']) for r in p['left']};beta={r['state']:F(r['dual']) for r in p['right']}
            if name[0] in ('cross-floor','cross-pair'):
                v,w=p['source_old_word'],p['donor_old_word']
                assert left==groups[h,v] and right==groups[h,w]
                count=hist[h]['hist'][v]*(hist[h]['hist'][w]-int(v==w))
                assert count==p['named_pair_count']
                factor=F(count,6 if name[0]=='cross-floor' else 30)
                coefficient=lambda s,t:pair_row_coefficient(name,v,w,s,t)
            else:
                assert name==('Y-to-R',(1,(0,0,0)),4)
                w=p['root_old_word'];assert left==groups[h,w]
                ss=own[h,1,1,bits(w,3),bits(w,3)];rr=ss[1,0]+ss[1,1]
                assert right=={r:v for r,v in [(0,H[h]-rr),(1,rr)] if v}
                factor=F(hist[h]['hist'][w],6)
                def coefficient(s,r):
                    e=bits(s,5);t=w//4
                    return q(e[4],t+sum(e))-F(r,t+sum(e[:4])+1)
            assert factor==F(p['factor'])
            for ix,s in enumerate(left):
                for iy,t in enumerate(right):
                    c=coefficient(s,t);assert c==F(p['coefficients'][ix][iy])
                    assert alpha[s]+beta[t]>=c;dual_cells+=1
            lm=defaultdict(F);rm=defaultdict(F);pv=F()
            for z in p['optimal_pair_coupling']:
                s,t=z['left'],z['right'];mass=F(z['mass']);assert mass>0
                lm[s]+=mass;rm[t]+=mass;pv+=mass*coefficient(s,t)
            assert dict(lm)==left and dict(rm)==right
            dual=sum((left[s]*alpha[s] for s in left),F())+sum((right[t]*beta[t] for t in right),F())
            assert pv==dual==F(p['upper']);bound+=factor*dual;transport_checks+=1
        assert bound==F(row['upper']) and sums[name]<=bound
        if bound<0:negative_upper.append(dict(name=name,upper=bound,approx=float(bound)))
    assert transport_checks==293 and len(negative_upper)==2
    # Independently reconstruct both full-domain symbolic rows.
    muindex={(d['hist'],d['old_word'],d['state']):j for j,d in enumerate(desc)}
    cut_cells=0;cut_coefficients=0
    for row in cuts['rows']:
        name=freeze(row['source_query']);mcoef=defaultdict(F);ocoef=defaultdict(F);seen=set();cells=0
        for p in row['pieces']:
            h=p['hist'];alpha=list(map(F,p['alpha']));beta=list(map(F,p['beta']));assert len(alpha)==32
            if name[0]=='cross-pair':
                v,w=p['source_old_word'],p['donor_old_word'];seen.add((h,v,w))
                count=hist[h]['hist'][v]*(hist[h]['hist'][w]-int(v==w));factor=F(count,30)
                assert count>0 and len(beta)==32
                for s,t in product(range(32),repeat=2):
                    assert alpha[s]+beta[t]>=pair_row_coefficient(name,v,w,s,t);cells+=1
                for s in range(32):mcoef[muindex[h,v,s]]+=factor*alpha[s];mcoef[muindex[h,w,s]]+=factor*beta[s]
            else:
                w=p['root_old_word'];seen.add((h,w));factor=F(hist[h]['hist'][w],6);assert len(beta)==2
                for s,r in product(range(32),range(2)):
                    e=bits(s,5);t=w//4;c=q(e[4],t+sum(e))-F(r,t+sum(e[:4])+1)
                    assert alpha[s]+beta[r]>=c;cells+=1
                for s in range(32):mcoef[muindex[h,w,s]]+=factor*alpha[s]
                ocoef[h]+=factor*beta[0]
                ss=own_index[h,1,1,bits(w,3),bits(w,3)];assert [ss[1,0],ss[1,1]]==p['R_old_columns']
                for j in (ss[1,0],ss[1,1]):ocoef[j]+=factor*(beta[1]-beta[0])
            assert factor==F(p['factor'])
        if name[0]=='cross-pair':
            expected={(h,v,w) for h,c in hist.items() for v,nv in enumerate(c['hist']) for w,nw in enumerate(c['hist']) if nv*(nw-int(v==w))>0}
        else:expected={(h,w) for h,c in hist.items() for w,n in enumerate(c['hist']) if n}
        assert seen==expected
        mcoef={j:v for j,v in mcoef.items() if v};ocoef={j:v for j,v in ocoef.items() if v}
        assert mcoef=={j:F(v) for j,v in row['mu']} and ocoef=={j:F(v) for j,v in row['old']}
        value=sum((F(mc['mu'][j])*v for j,v in mcoef.items()),F())+sum((F(point['columns'][j]['weight'])*v for j,v in ocoef.items()),F())
        assert value==F(row['current_mu_value'])<0 and cells==row['full_domain_dominance_cells']
        cut_cells+=cells;cut_coefficients+=len(mcoef)+len(ocoef)
    assert cut_cells==cuts['total_full_domain_dominance_cells']
    report=dict(status='INDEPENDENT_LITERAL_KERNEL_AND_FIXED_MU_OBSTRUCTION_PASS',script_sha256=sha(Path(__file__)),
        input_sha256=dict(point=PIN,mu=MUPIN,network=NETPIN,product=sha(HERE/'conditional_product_exact.json'),
                          bounds=sha(HERE/'fixed_mu_upper_bounds_exact.json'),full32_rows=sha(HERE/'full32_obstruction_rows_exact.json')),
        all_mu_states=1216,positive_mu_states=35,groups=38,zero_hist_fibers=6,
        canonical_kernel_columns=columns,S6_copies=720*columns,total_mass=total,
        exact_network_atom_marginals=len(network_margin),explicit_named_root_vectors=len(root_law),
        exact_named_single_root_projections=len(single),exact_network_root_projections=len(local),
        exact_distinct_root_pair_projections=len(pair),S6_frequency_checks=frequency,
        all_literal_orbit_rows=len(sums),negative_rows=7,zero_rows=5,positive_rows=446,
        original_BC_literal_evaluations=old_literal_evaluations,cross_root_literal_evaluations=cross_literal_evaluations,
        new_literal_numerator_terms=new_literal_evaluations,unit_customer_scale_digits=len(str(denominator)),
        exact_transport_primal_dual_checks=transport_checks,transport_dual_cells=dual_cells,
        negative_fixed_mu_upper_bounds=negative_upper,full32_cut_rows=2,full32_dominance_cells=cut_cells,
        symbolic_cut_nonzero_coefficient_checks=cut_coefficients,
        common_phase_I_runs=0,phase_I_not_run_reason='Two exact upper bounds already exclude this fixed mu over every common coupling, independently of the 100-atom network.',
        no_SPE_claim=True,no_original_point_exclusion=True,elapsed_seconds=time.monotonic()-begin)
    (HERE/'independent_audit.json').write_text(json.dumps(serial(report),ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(serial(report),ensure_ascii=False))


if __name__=='__main__':main()
