"""Independent exact audit of the joint R/Z/B4/D customer measure.

No imports from analyze, discover, recover, or another verifier.  The script
reads original point coordinates and evaluates actual payoff formulas under
all 720 simultaneous permutations.  Saved LP coefficients are not used for
the payoff certification.
"""
from collections import defaultdict,deque
from fractions import Fraction as Q
from hashlib import sha256
from itertools import product,permutations
from math import lcm
from pathlib import Path
import json,time
import numpy as np

HERE=Path(__file__).resolve().parent;WORK=HERE.parent
POINT=WORK/'union_augmented_lp/augmented_lp_exact.json'
POINT_SHA='b0ca65cfe61e5e3ef09537cba2a986c171aeaa7106f673077f803c80ee2b68e3'
def sha(p):return sha256(p.read_bytes()).hexdigest()
def serial(v):
    if isinstance(v,Q):return str(v)
    if isinstance(v,dict):return {str(k):serial(x) for k,x in v.items()}
    if isinstance(v,(list,tuple)):return [serial(x) for x in v]
    return v
def canon(xs):
    d={};return ''.join(str(d.setdefault(x,len(d))) for x in xs)
def share(a,b):return Q(a,b) if a else Q()

def main():
    start=time.perf_counter();assert sha(POINT)==POINT_SHA
    point=json.loads(POINT.read_bytes());cols=point['columns'];values=[Q(c['weight']) for c in cols]
    hist={};own=defaultdict(dict);b4=defaultdict(dict);cur=None
    for j,c in enumerate(cols[:4849]):
        if c['kind']=='hist':cur=j;hist[j]=c
        elif c['kind']=='joint-reply':
            f,s,wi,wj=c['group'];g=(f,s,tuple(wi),tuple(wj));own[cur].setdefault(g,{})[tuple(c['state'])]=values[j]
        elif c['kind']=='actual-B-family-state' and c['source']==4:
            b4[c['hist_column']][tuple(c['hidden'])+(c['ell']//6,)]=values[j]
    for h,gg in own.items():
        for m in gg.values():m[0,0]=values[h]-sum(m.values(),Q())
    expectedD=json.loads((WORK/'fifth_reply_interface/D_marginals.json').read_bytes())
    D={r['hist_column']:{tuple(c['word']):Q(c['value']) for c in r['D']} for r in expectedD['hist_and_D_marginals']}
    old=json.loads((WORK/'common_network_19662/common_atoms.json').read_bytes())
    witness=json.loads((HERE/'common_atoms_with_D.json').read_bytes())
    exact=json.loads((HERE/'exact_extension.json').read_bytes())
    assert witness['point_sha256']==POINT_SHA and exact['witness_sha256']==sha(HERE/'common_atoms_with_D.json')
    assert witness['source_sha256']==sha(WORK/'common_network_19662/common_atoms.json')
    oldblocks={b['hist_column']:b for b in old['blocks']};blocks={b['hist_column']:b for b in witness['blocks']}
    kernels={(r['hist_column'],r['atom_index']):r for r in exact['conditional_distributions']}
    nodes=[e for e in product(range(2),range(6),range(6)) if e[0] or e[1]!=e[2]];node_index={e:k for k,e in enumerate(nodes)}
    assert witness['literal_node_order']==old['literal_node_order']==[list(e) for e in nodes]
    perms=list(permutations(range(6)));nd=np.empty((720,6),dtype=np.int64);ne=np.empty((720,66),dtype=np.int64)
    for pi,p in enumerate(perms):
        for i in range(6):nd[pi,p[i]]=i
        for e,(f,j,k) in enumerate(nodes):ne[pi,node_index[f,p[j],p[k]]]=e
    pair=defaultdict(list);triple=defaultdict(list)
    for i,j in product(range(6),repeat=2):pair[int(i==j)].append(i*6+j)
    for i in range(6):
        for e,(f,j,k) in enumerate(nodes):triple[f,canon((i,j,k))].append(i*66+e)
    assert sorted(map(len,triple.values()))==[6,30,30,30,30,30,120,120]
    sums=defaultdict(Q);literal_counts={};integer_checks=0;prefix_checks=0
    def record(base,num,den,mass,groups):
        nonlocal integer_checks
        num=np.asarray(num,dtype=np.int64).reshape(720,-1)
        den=np.broadcast_to(np.asarray(den,dtype=np.int64),num.shape).reshape(720,-1)
        assert np.all(num[den==0]==0)
        for o,ids in groups.items():
            name=tuple(base)+tuple(o);literal_counts[name]=len(ids)
        for divisor in np.unique(den):
            if divisor==0:continue
            counts=(num*(den==divisor)).sum(axis=0)
            for o,ids in groups.items():
                cc=counts[ids];v=int(cc[0]);assert np.all(cc==v),('S6 orbit not constant',base,o)
                integer_checks+=len(ids);sums[tuple(base)+tuple(o)]+=mass*Q(v,720*int(divisor))
    single={():list(range(6))}
    pair_groups={(same,):ids for same,ids in pair.items()}
    triple_groups={tuple(o):ids for o,ids in triple.items()}
    total=Q();scale=1;atom_count=0;projection_checks=0;kernel_checks=0;Dmargin_checks=0
    hist_margins=[];clause_checks=0
    boolean=json.loads((HERE/'boolean_analysis.json').read_bytes());graphs={r['hist_column']:r for r in boolean['hist_records'] if not r['vacuous']}
    for h,hc in hist.items():
        H=values[h];a=tuple(map(int,hc['actual_bits']));p3=sum(a[:3]);P=sum(a[:4]);tot=sum(a)
        words=tuple(w for w,n in zip(product(range(2),repeat=3),hc['hist']) for _ in range(n))
        ww=np.array(words,dtype=np.int64)[nd];tt=ww[:,:,0];bb=ww[:,:,1];cc=ww[:,:,2]
        rden=np.array([p3+words[j][0]+words[k][1+f]+1 for f,j,k in nodes],dtype=np.int64)[ne]
        for pi,p in enumerate(perms):
            for e,(f,j,k) in enumerate(nodes):
                assert rden[pi,e]==p3+ww[pi,j,0]+ww[pi,k,1+f]+1;prefix_checks+=1
        dm=[Q()]*6;project=defaultdict(Q);subatoms=defaultdict(dict)
        if H:
            block=blocks[h];assert block['actual_bits']==hc['actual_bits'] and block['hist']==hc['hist']
            atoms=block['atoms']
        else:assert h not in blocks;atoms=[]
        for atom in atoms:
            mass=Q(atom['mass']);assert mass>0;ai=atom['source_atom_index'];source=oldblocks[h]['atoms'][ai]
            assert atom['states']==source['states'] and atom['B4_state']==source['B4_state']
            bits=tuple(atom['D_bits']);assert len(bits)==6 and all(x in (0,1) for x in bits)
            assert bits not in subatoms[ai];subatoms[ai][bits]=mass;project[ai]+=mass
            for i,b in enumerate(bits):dm[i]+=mass*b
            total+=mass;scale=lcm(scale,(mass/720).denominator);atom_count+=1
            assignment=atom['B4_state']+[s//2 for s in atom['states']]+[s%2 for s in atom['states']]+list(bits)
            for clause in graphs[h]['clauses']:
                assert any(assignment[l//2]==l%2 for l in clause['literals']);clause_checks+=1
            dd=np.array(bits,dtype=np.int64)[nd]
            ss=np.array(atom['states'],dtype=np.int64)[ne];rr=ss//2;zz=ss%2
            h1,h2,y=atom['B4_state'];den=P+tt+1
            sums['D-source',]+=mass*share(a[4],tot)
            record(('D-source',),-tt,P+tt+dd,mass,single)
            record(('capacity-D',),-dd,1,mass,single)
            for k in range(1,7):
                name=('A-to-D-safe' if k<6 else 'A6-to-D',k)
                sums[name]+=mass*share(a[k-1],tot)
                record(name,-dd,sum(a[:k-1])+7-k,mass,single)
            for k,ak in enumerate(a,1):record(('D-to-A',k),dd-ak,den,mass,single)
            for k,hbit in enumerate((h1,h2),1):record(('D-to-H',k),dd-hbit,den,mass,single)
            pairden=np.broadcast_to(den[:,:,None],(720,6,6)).reshape(720,36)
            for slot,kind in enumerate(('T','B','C')):
                pairnum=(dd[:,:,None]-ww[:,None,:,slot]).reshape(720,36)
                record(('D-to-'+kind,),pairnum,pairden,mass,pair_groups)
            record(('D-to-D',),(dd[:,:,None]-dd[:,None,:]).reshape(720,36),pairden,mass,pair_groups)
            for kind,num in (('B-safe-to-D',bb),('C-to-D',cc)):
                source_num=np.broadcast_to(num[:,None,:],(720,6,6)).reshape(720,36)
                source_den=np.broadcast_to((p3+tt+bb+cc)[:,None,:],(720,6,6)).reshape(720,36)
                record((kind,),source_num,source_den,mass,pair_groups)
                query_den=p3+tt+(2 if kind=='B-safe-to-D' else bb+1)
                query_den=np.broadcast_to(query_den[:,None,:],(720,6,6)).reshape(720,36)
                query_num=-np.broadcast_to(dd[:,:,None],(720,6,6)).reshape(720,36)
                record((kind,),query_num,query_den,mass,pair_groups)
            sums['H1-safe-to-D',]+=mass*share(h1,p3+a[5]+h1+h2)
            record(('H1-safe-to-D',),-dd,p3+a[5]+2,mass,single)
            record(('F-to-D',),h2-dd,p3+a[5]+h1+1,mass,single)
            dden=np.broadcast_to(den[:,:,None],(720,6,66)).reshape(720,396)
            for kind,q in (('R',rr),('Z',zz)):
                record(('D-to-'+kind,),(dd[:,:,None]-q[:,None,:]).reshape(720,396),dden,mass,triple_groups)
            for kind,num,qden in (('R-to-D',rr,rden),('Z-to-D',zz,P+rr+1)):
                record((kind,),(num[:,None,:]-dd[:,:,None]).reshape(720,396),
                       np.broadcast_to(qden[:,None,:],(720,6,66)).reshape(720,396),mass,triple_groups)
        if H:
            for ai,source in enumerate(oldblocks[h]['atoms']):
                mass=Q(source['mass']);assert project[ai]==mass;projection_checks+=1
                kernel=kernels[h,ai];probs=list(map(Q,kernel['D_conditional_probabilities']))
                assert Q(kernel['old_mass'])==mass and all(0<=p<=1 for p in probs)
                for bits in product(range(2),repeat=6):
                    mm=mass
                    for bit,p in zip(bits,probs):mm*=p if bit else 1-p
                    assert subatoms[ai].get(bits,Q())==mm;kernel_checks+=1
                for i,p in enumerate(probs):assert sum((mm*bits[i] for bits,mm in subatoms[ai].items()),Q())==mass*p
        margins=[]
        for w,expected in D[h].items():
            ids=[i for i,wi in enumerate(words) if wi==w];found=sum((dm[i] for i in ids),Q())/len(ids)
            assert found==expected;Dmargin_checks+=1;margins.append(dict(word=w,mass=found))
        hist_margins.append(dict(hist_column=h,mass=H,D=margins))
    sums['capacity-D',]+=values[0]
    assert total==1 and atom_count==100==witness['base_atoms'] and witness['expanded_atoms']==72000
    assert scale==int(exact['unit_customer_scale']) and len(str(scale))==595
    assert len(sums)==62 and len(literal_counts)==62 and sum(literal_counts.values())==1908
    rows=[dict(name=list(n),literal_count=literal_counts[n],slack=v,approx=float(v)) for n,v in sorted(sums.items(),key=lambda nv:str(nv[0]))]
    assert min(sums.values())>=0
    old_lift=json.loads((WORK/'fifth_reply_interface/exact_lift.json').read_bytes())
    symbolic=json.loads((WORK/'fifth_reply_interface/symbolic_lift.json').read_bytes())
    assert symbolic['old_descriptors']==[{k:v for k,v in c.items() if k!='weight'} for c in cols]
    augmented=values+list(map(Q,old_lift['new_values']));projection=[]
    for r,saved in zip(symbolic['rows'],old_lift['rows']):
        assert r['name']==saved['name'];v=sum((Q(c)*augmented[j] for j,c in r['row']),Q())
        assert v==Q(saved['slack']) and v>=0;projection.append(dict(name=r['name'],slack=v))
    assert len(projection)==1180
    fixed_slacks={tuple(r['name']):Q(r['slack']) for r in old_lift['rows']}
    comparisons=[]
    for name,v in sums.items():
        upper=name
        if name[0]=='Z-to-D':upper=('Z-to-D-upper',*name[1:])
        if name[0]=='F-to-D':upper=('F-to-D-upper',)
        gap=fixed_slacks[upper]-v
        if upper==name:assert gap==0
        else:assert gap>=0
        comparisons.append(dict(actual_name=name,projection_name=upper,projection_slack=fixed_slacks[upper],actual_slack=v,min_relaxation_gap=gap))
    old_report=json.loads((HERE/'old_network_verification.json').read_bytes())
    assert old_report['status']=='PASS' and old_report['witness_sha256']==sha(HERE/'common_atoms_with_D.json')
    assert old_report['canonical_atoms']==100 and old_report['expanded_positive_atoms']==72000
    old_reference=json.loads((WORK/'common_network_19662/independent_verification.json').read_bytes())
    assert old_report['old_literal_queries']==old_reference['old_literal_queries']
    assert old_report['B4_literal_rows']==old_reference['B4_literal_rows']
    # The pointwise conditionals have no D_i-D_j constraint.  Their product is
    # therefore sufficient; the true D_i -> D_j denominator contains neither
    # hidden D bit, and its expectation depends on their two marginals only.
    report=dict(status='PASS',scope='Exact common customer coverage layer for all old R/Z nodes, the same B4, and all six genuine fifth-source D labels; not full SPE or a six-provider counterexample',
                point_sha256=POINT_SHA,witness_sha256=sha(HERE/'common_atoms_with_D.json'),verifier_sha256=sha(Path(__file__)),
                arithmetic='All 720 synchronous permutations; integer membership sums and original payoff denominators; Fraction masses',
                canonical_joint_atoms=atom_count,expanded_joint_atoms=720*atom_count,total_mass=total,unit_customer_scale=str(scale),unit_customer_scale_digits=len(str(scale)),
                old_atom_projection_checks=projection_checks,conditional_product_state_checks=kernel_checks,
                D_marginal_checks=Dmargin_checks,zero_face_clause_checks=clause_checks,actual_R_prefix_checks=prefix_checks,
                D_integer_coefficient_checks=integer_checks,D_orbit_rows=len(rows),D_literal_rows=sum(literal_counts.values()),
                D_summary=dict(orbit_negative=sum(v<0 for v in sums.values()),orbit_zero=sum(v==0 for v in sums.values()),orbit_positive=sum(v>0 for v in sums.values()),
                               literal_negative=sum(literal_counts[n] for n,v in sums.items() if v<0),literal_zero=sum(literal_counts[n] for n,v in sums.items() if v==0),literal_positive=sum(literal_counts[n] for n,v in sums.items() if v>0)),
                true_D_rows=rows,projection_vs_true=sorted(comparisons,key=lambda r:str(r['actual_name'])),all_1180_projection_rows=projection,
                hist_D_marginals=hist_margins,old_network_verification_sha256=sha(HERE/'old_network_verification.json'),
                old_17424_literal_rows=old_report['old_summary'],same_B4_15_orbit_rows=old_report['B4_summary'],
                all_old_network_and_B4_slacks_preserved=True,elapsed_seconds=time.perf_counter()-start)
    (HERE/'independent_verification.json').write_text(json.dumps(serial(report),ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(serial({k:v for k,v in report.items() if k not in ('unit_customer_scale','true_D_rows','projection_vs_true','all_1180_projection_rows','hist_D_marginals')})))

if __name__=='__main__':main()
