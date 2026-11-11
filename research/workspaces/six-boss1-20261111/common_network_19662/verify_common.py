"""Independent literal-payoff and margin audit of the common RZ/B4 measure.

No imports from a parser, discoverer, constructor, or another verifier.
All 720 synchronous S6 permutations are explicit.  Integer counts multiply
exact rational masses; margins and original payoff formulas decide the result.
"""
from __future__ import annotations
from collections import defaultdict
from fractions import Fraction as Q
from hashlib import sha256
from itertools import permutations,product
from math import lcm
from pathlib import Path
import argparse,gzip,json
import numpy as np

POINT_SHA='b0ca65cfe61e5e3ef09537cba2a986c171aeaa7106f673077f803c80ee2b68e3'
DESC_SHA='afce2dcdff01e9393c04e317ee6bd52f5c0b378daedd92816647412243362460'
KINDS=('R-R','R-Z','Z-R','Z-Z')

def sha(p):return sha256(p.read_bytes()).hexdigest()
def canon(xs):
    names={}
    return tuple(names.setdefault(x,len(names)) for x in xs)
def pairclass(e,f):return e[0],f[0],canon(e[1:]+f[1:])
def serial(v):
    if isinstance(v,Q):return str(v)
    if isinstance(v,dict):return {str(k):serial(x) for k,x in v.items()}
    if isinstance(v,(list,tuple)):return [serial(x) for x in v]
    return v

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--point',type=Path,required=True)
    ap.add_argument('--witness',type=Path,required=True);ap.add_argument('--output',type=Path,required=True)
    ap.add_argument('--materialize',type=Path);args=ap.parse_args()
    assert sha(args.point)==POINT_SHA
    raw=json.loads(args.point.read_bytes());w=json.loads(args.witness.read_bytes())
    assert w['point_sha256']==POINT_SHA
    cols=raw['columns'][:4849]
    desc=[{k:v for k,v in c.items() if k!='weight'} for c in cols]
    assert sha256(json.dumps(desc,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()==DESC_SHA
    masses=[Q(c['weight']) for c in cols];hist={};groups=defaultdict(dict);b4=defaultdict(dict);current=None
    for j,c in enumerate(cols):
        if c['kind']=='hist':current=j;hist[j]=c
        elif c['kind']=='joint-reply':
            f,diag,wi,wj=c['group'];g=(f,diag,tuple(wi),tuple(wj))
            groups[current].setdefault(g,{})[tuple(c['state'])]=masses[j]
        elif c['kind']=='actual-B-family-state' and c['source']==4:
            assert set(c)=={'kind','source','hist_column','hidden','ell','weight'}
            assert len(c['hidden'])==2 and c['ell'] in (0,6)
            s=tuple(c['hidden'])+(c['ell']//6,)
            assert s not in b4[c['hist_column']]
            b4[c['hist_column']][s]=masses[j]
    assert len(hist)==16 and sum(map(len,groups.values()))==194
    for h,gg in groups.items():
        for g,m in gg.items():
            assert set(m)=={(0,1),(1,0),(1,1)}
            m[0,0]=masses[h]-sum(m.values())
            assert min(m.values())>=0
        assert set(b4[h])==set(product(range(2),repeat=3))
        assert sum(b4[h].values(),Q())==masses[h]
    assert sum((masses[h] for h in hist),Q())==1
    nodes=[e for e in product(range(2),range(6),range(6)) if e[0] or e[1]!=e[2]]
    assert [list(e) for e in nodes]==w['literal_node_order']
    ni={e:i for i,e in enumerate(nodes)}
    perms=list(permutations(range(6)));assert len(perms)==720
    inverse=np.empty((720,66),dtype=np.int64)
    for pi,p in enumerate(perms):
        for k,(f,i,j) in enumerate(nodes):inverse[pi,ni[f,p[i],p[j]]]=k
    orbits=defaultdict(list)
    for i,e in enumerate(nodes):
        for j,f in enumerate(nodes):orbits[pairclass(e,f)].append((i,j))
    assert len(orbits)==42
    indices={o:(np.array([i for i,j in pp]),np.array([j for i,j in pp])) for o,pp in orbits.items()}
    one_orbits={(0,0):[],(1,0):[],(1,1):[]}
    for i,(f,a,b) in enumerate(nodes):one_orbits[f,int(a==b)].append(i)
    assert [len(one_orbits[o]) for o in one_orbits]==[30,30,6]
    blocks={b['hist_column']:b for b in w['blocks']}
    assert len(blocks)==len(w['blocks']) and set(blocks)=={h for h in hist if masses[h]}
    values=defaultdict(Q);bv=defaultdict(Q)
    own_checks=0;b4_checks=0;prefix_checks=0;integer_checks=0;B4_integer_checks=0
    total=Q();scale=1;base_atoms=0;expanded=0;own_by_h={};hist_records=[]
    writer=gzip.open(args.materialize,'wt',encoding='utf-8') if args.materialize else None
    try:
      for h,hc in hist.items():
        H=masses[h];actual=tuple(map(int,hc['actual_bits']))
        words=tuple(word for word,n in zip(product(range(2),repeat=3),hc['hist']) for _ in range(n))
        assert len(words)==6 and sum(t for t,b,c in words)==hc['d']
        expected=[groups[h][(f,int(i==j),words[i],words[j])] for f,i,j in nodes]
        own_by_h[h]=[[m[s] for s in product(range(2),repeat=2)] for m in expected]
        own=[[Q()]*4 for _ in nodes];bmargin={s:Q() for s in b4[h]}
        p3=sum(actual[:3]);P=sum(actual[:4])
        oldden=np.array([p3+words[i][0]+words[j][1+f]+1 for f,i,j in nodes],dtype=np.int64)[inverse]
        if H:
            block=blocks[h]
            assert block['actual_bits']==hc['actual_bits'] and block['hist']==hc['hist']
            for pi,perm in enumerate(perms):
                moved=[None]*6
                for i in range(6):moved[perm[i]]=words[i]
                for k,(f,i,j) in enumerate(nodes):
                    assert oldden[pi,k]==p3+moved[i][0]+moved[j][1+f]+1
                    old=nodes[inverse[pi,k]]
                    assert (f,int(i==j),moved[i],moved[j])==(old[0],int(old[1]==old[2]),words[old[1]],words[old[2]])
                    prefix_checks+=1
        atoms=blocks[h]['atoms'] if H else []
        local=Q()
        for ai,atom in enumerate(atoms):
            mass=Q(atom['mass']);ss=atom['states'];s=tuple(atom['B4_state'])
            assert mass>0 and len(ss)==66 and all(a in range(4) for a in ss)
            assert s in b4[h] and b4[h][s]>0
            for k,a in enumerate(ss):own[k][a]+=mass
            bmargin[s]+=mass;local+=mass;total+=mass
            scale=lcm(scale,(mass/720).denominator);base_atoms+=1;expanded+=720
            state=np.array(ss,dtype=np.int64)[inverse];r=state//2;z=state%2
            coefs=[]
            for den in range(1,7):
                mask=(oldden==den).astype(np.int64)
                if not mask.any():continue
                ownr=(mask*r).sum(axis=0)[:,None]
                coefs.append(('R-R',den,ownr-mask.T@r))
                coefs.append(('R-Z',den,ownr-mask.T@z))
            for flag in (0,1):
                mask=(r==flag).astype(np.int64);den=P+flag+1
                ownz=(mask*z).sum(axis=0)[:,None]
                coefs.append(('Z-R',den,ownz-mask.T@r))
                coefs.append(('Z-Z',den,ownz-mask.T@z))
            for kind,den,mat in coefs:
                for o,(ii,jj) in indices.items():
                    vv=mat[ii,jj];cnt=int(vv[0]);assert (vv==cnt).all()
                    integer_checks+=len(vv)
                    values[kind,o]+=mass*Q(cnt,720*den)
            fden=p3+actual[5]+s[0]+1
            bcoefs=[('F-to-R',None,fden,720*s[1]-r.sum(axis=0)),
                    ('F-to-Z',None,fden,720*s[1]-z.sum(axis=0))]
            for flag in (0,1):
                mask=(r==flag).astype(np.int64)
                ownz=(mask*z).sum(axis=0);counts=mask.sum(axis=0)
                for k in range(3):bcoefs.append(('Z-to-X',k,P+flag+1,ownz-s[k]*counts))
            for kind,k,den,arr in bcoefs:
                for o,ids in one_orbits.items():
                    vv=arr[ids];cnt=int(vv[0]);assert (vv==cnt).all()
                    B4_integer_checks+=len(vv)
                    bv[kind,o,k]+=mass*Q(cnt,720*den)
            if writer:
                for pi,perm in enumerate(perms):
                    moved=[None]*6
                    for i in range(6):moved[perm[i]]=words[i]
                    row=dict(hist_column=h,base_atom=ai,permutation=perm,mass=str(mass/720),
                             actual_bits=actual,old_words=moved,RZ_states=state[pi].tolist(),B4_state=s)
                    writer.write(json.dumps(row,separators=(',',':'))+'\n')
        assert local==H
        for k,m in enumerate(expected):
            for st in product(range(2),repeat=2):
                assert own[k][2*st[0]+st[1]]==m[st]
                own_checks+=1
        for s,m in b4[h].items():assert bmargin[s]==m;b4_checks+=1
        hist_records.append(dict(hist_column=h,mass=H,canonical_atoms=len(atoms),
                                 B4_full_state_margins=[dict(state=s,mass=m) for s,m in sorted(bmargin.items())]))
    finally:
        if writer:writer.close()
    assert total==1 and base_atoms==w['base_atoms'] and expanded==w['expanded_atoms']
    class_rows=[];literal_rows=[];summary={};minima={}
    for kind in KINDS:
        allv=[]
        for o,pp in orbits.items():
            v=values[kind,o]
            class_rows.append(dict(kind=kind,orbit=o,literal_count=len(pp),slack=v))
            for i,j in pp:
                literal_rows.append(dict(kind=kind,source=nodes[i],query=nodes[j],slack=v));allv.append(v)
        summary[kind]=dict(total=len(allv),negative=sum(v<0 for v in allv),zero=sum(v==0 for v in allv),positive=sum(v>0 for v in allv))
        minima[kind]=dict(minimum=min(allv),minimum_positive=min((v for v in allv if v>0),default=Q()))
    brows=[];bliteral=[]
    for o,ids in one_orbits.items():
        for kind,k in [('F-to-R',None),('F-to-Z',None)]+[('Z-to-X',k) for k in range(3)]:
            v=bv[kind,o,k];brows.append(dict(kind=kind,orbit=o,target_index=k,slack=v,slack_float=float(v)))
            for i in ids:bliteral.append(dict(kind=kind,node=nodes[i],target_index=k,slack=v))
    assert len(literal_rows)==17424 and len(brows)==15 and len(bliteral)==330
    upper=[]
    for o,pp in orbits.items():
        if all(i==j for i,j in pp):continue
        val=Q()
        for h,hc in hist.items():
            P=sum(map(int,hc['actual_bits'][:4]));D=(P+1)*(P+2);own=own_by_h[h]
            for i,j in pp:
                qe=own[i][2]+own[i][3];ve=own[i][1]+own[i][3];vf=own[j][1]+own[j][3];te=own[i][3]
                val+=((ve-vf)/Q(P+1)+(min(qe,vf)-te)/Q(D))/len(pp)
        upper.append(dict(orbit=o,literal_count=len(pp),upper=val))
    assert len(upper)==39 and all(r['upper']>0 for r in upper)
    # Marginal-only upper bounds use a single Fréchet overlap each.  They are
    # independently valid for arbitrary joint measures, not merely phases.
    BF=sum((eta*Q(s[1],sum(map(int,hist[h]['actual_bits'][:3]))+
             int(hist[h]['actual_bits'][5])+s[0]+1)
            for h in hist for s,eta in b4[h].items()),Q())
    bupper=[]
    for o,ids in one_orbits.items():
        BZ=sum(((own_by_h[h][i][1]/Q(sum(map(int,hist[h]['actual_bits'][:4]))+1)+
                 own_by_h[h][i][3]/Q(sum(map(int,hist[h]['actual_bits'][:4]))+2))/len(ids)
                for h in hist for i in ids),Q())
        for kind,k in [('F-to-R',None),('F-to-Z',None)]+[('Z-to-X',k) for k in range(3)]:
            lower=Q()
            for h,hc in hist.items():
                a=tuple(map(int,hc['actual_bits']));P=sum(a[:4]);d0=sum(a[:3])+a[5]+1
                high=sum((eta*s[0] for s,eta in b4[h].items()),Q())
                target=sum((eta*s[k] for s,eta in b4[h].items()),Q()) if k is not None else None
                for i in ids:
                    own=own_by_h[h][i];q=own[2]+own[3];v=own[1]+own[3]
                    if kind=='Z-to-X':
                        lower+=(target/Q(P+1)-min(q,target)/Q((P+1)*(P+2)))/len(ids)
                    else:
                        need=q if kind=='F-to-R' else v;inter=min(need,high)
                        lower+=((need-inter)/Q(d0)+inter/Q(d0+1))/len(ids)
            val=(BZ if kind=='Z-to-X' else BF)-lower
            assert val>=bv[kind,o,k]
            bupper.append(dict(kind=kind,orbit=o,target_index=k,upper=val,upper_float=float(val)))
    report=dict(scope='Exact common customer measure for 17424 old literal IC and 15 orbit B4 IC (330 literal expansions), preserving all own four-state and B4 full eight-state margins; not full SPE or a welfare theorem',
        status='PASS' if all(s['negative']==0 for s in summary.values()) and all(r['slack']>=0 for r in brows) else 'FAIL',
        point_path=str(args.point),point_sha256=POINT_SHA,witness_path=str(args.witness),witness_sha256=sha(args.witness),
        independent_verifier_sha256=sha(Path(__file__)),original_descriptor_sha256=DESC_SHA,
        arithmetic='Integer membership counts under all 720 simultaneous permutations, exact Fraction masses, original payoff denominators',
        canonical_atoms=base_atoms,expanded_positive_atoms=expanded,total_mass=total,
        unit_customer_scale=str(scale),unit_customer_scale_digits=len(str(scale)),
        own_four_state_checks=own_checks,B4_eight_state_checks=b4_checks,true_R_prefix_checks=prefix_checks,
        old_literal_integer_coefficient_checks=integer_checks,B4_literal_integer_coefficient_checks=B4_integer_checks,
        old_summary=summary,old_minima=minima,B4_summary=dict(orbit_queries=15,literal_queries=330,
            negative=sum(r['slack']<0 for r in brows),zero=sum(r['slack']==0 for r in brows),positive=sum(r['slack']>0 for r in brows)),
        hist_records=hist_records,old_class_rows=class_rows,old_literal_queries=literal_rows,
        B4_orbit_rows=brows,B4_literal_rows=bliteral,new_point_nonself_ZZ_upper=upper,
        B4_single_query_upper=bupper,
        no_old_saturation_transfer=True)
    if args.materialize:
        report['materialized_atoms']=dict(path=str(args.materialize),sha256=sha(args.materialize),records=expanded)
    args.output.write_text(json.dumps(serial(report),ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(serial({k:v for k,v in report.items() if k not in
        ('hist_records','old_class_rows','old_literal_queries','B4_orbit_rows','B4_literal_rows','new_point_nonself_ZZ_upper','B4_single_query_upper','unit_customer_scale')})),flush=True)

if __name__=='__main__':main()
