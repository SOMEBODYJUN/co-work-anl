"""Independent, generator-free audit of the conditional joint Z-Z extension.

The original 702 and five compact rows involve only hist/K, which are fixed.
All other raw rows are rebuilt literally below. No research module is imported.
"""
from collections import defaultdict
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
import hashlib, json

HERE=Path(__file__).resolve().parent
WORK=HERE.parent
ROOT=next(p for p in HERE.parents if (p/'work.py').exists())
OLD=ROOT/'research/workspaces/customer-attraction/R-c4f1ef099fad483c9f81283b61eb0b53/six_astra/attractive_nested_exact.json'
NEW=WORK/'six_query/repair_zz_exact.json'

def canonical(xs):
    labels={}
    return tuple(labels.setdefault(x,len(labels)) for x in xs)

def group_key(g):
    return g[0],g[1],tuple(g[2]),tuple(g[3])

def safe(n,d):
    return Q(n,d) if n else Q()

def main():
    old=json.loads(OLD.read_text());new=json.loads(NEW.read_text())
    assert new['source_sha256']==hashlib.sha256(OLD.read_bytes()).hexdigest()
    cols=old['columns'];K=Q(cols[0]['weight']);assert cols[0]['kind']=='K'
    hists={i:c for i,c in enumerate(cols) if c['kind']=='hist'}
    # hist_column_old is a pre-state-expansion index, whereas hists are final
    # indices.  Recover linkage by the ordered blocks, independently of offsets.
    groups={hi:{} for hi in hists};hi=None
    for ci,c in enumerate(cols):
        if c['kind']=='hist':hi=ci
        elif c['kind']=='joint-reply':groups[hi].setdefault(group_key(c['group']),{})[tuple(c['state'])]=Q(c['weight'])
    modes=defaultdict(list)
    for mi,m in enumerate(new['modes']):
        assert m['hist_column'] in hists
        modes[m['hist_column']].append((mi,Q(m['mass']),frozenset(group_key(g) for g in m['r'])))
    zs={}
    for v in new['variables']:
        k=(v['mode'],group_key(v['group']));assert k not in zs
        q=Q(v['z_mass']);mass=Q(v['mass']);assert 0<=q<=mass
        assert mass==Q(new['modes'][v['mode']]['mass']);zs[k]=q
    rows=defaultdict(Q);rr_marginal_checks=0;state_bound_checks=0;mode_checks=0;pair_evaluations=0
    edges=tuple((f,i,j) for f,i,j in product(range(2),range(6),range(6)) if f or i!=j)
    pats=tuple(product((0,1),repeat=3))
    p3=tuple(sorted({canonical(v) for v in product(range(3),repeat=3)}))
    p4=tuple(sorted({canonical(v) for v in product(range(4),repeat=4)}))
    # Precreate even identically empty aggregate classes.
    for f in range(2):
        for name in ('source','pair','price','capacity',*('actual'+str(k) for k in range(6)),'ownR','reverseR'):
            rows['nested-basic',f,name]=Q()
        for q,pat in product(range(3),p3):rows['nested-Z-old',f,q,pat]=Q()
        for pat in p3:rows['nested-old-Z',f,pat]=Q()
        for name in ('source','ownB','ownC','ownT','optavg',*('actual'+str(k) for k in range(6)),'Bavg','Cavg','reverse','price','capacity'):
            rows['R-basic',f,name]=Q()
        for q,pat in product(range(3),p3):rows['R-old',f,q,pat]=Q()
        for pat in p3:rows['old-R',f,pat]=Q()
    for f,g,pat in product(range(2),range(2),p4):
        for name in ('R-R','Z-R','R-Z','pair-RR','Z-Z'):rows[name,f,g,pat]=Q()
    for hi,hc in hists.items():
        mass=Q(hc['weight']);gs=groups[hi];assert all(set(v)=={(0,1),(1,0),(1,1)} for v in gs.values())
        a=tuple(map(int,hc['actual_bits']));assert len(a)==6
        words=tuple(w for w,n in zip(pats,hc['hist']) for _ in range(n));assert len(words)==6
        keys={e:(e[0],int(e[1]==e[2]),words[e[1]],words[e[2]]) for e in edges}
        assert set(keys.values())==set(gs)
        q={g:s[1,0]+s[1,1] for g,s in gs.items()}
        assert all(0<=v<=mass for v in q.values())
        thresholds=sorted({Q(),mass,*q.values()})
        expected=[(up-lo,frozenset(g for g in gs if q[g]>=up)) for lo,up in zip(thresholds,thresholds[1:]) if up>lo]
        assert [(w,r) for _,w,r in modes[hi]]==expected
        assert sum((w for _,w,_ in modes[hi]),Q())==mass
        for g in gs:
            assert sum((w for _,w,r in modes[hi] if g in r),Q())==q[g]
            y01=sum((zs[mi,g] for mi,w,r in modes[hi] if g not in r),Q())
            y10=sum((w-zs[mi,g] for mi,w,r in modes[hi] if g in r),Q())
            y11=sum((zs[mi,g] for mi,w,r in modes[hi] if g in r),Q())
            assert min(y01,y10,y11)>=0 and y01+y10+y11<=mass
            assert y10+y11==q[g];state_bound_checks+=1
        # All old RR intersections are upper bounded by min of their marginals;
        # the new threshold construction realizes that common maximum.
        for c in cols:
            if c['kind']=='overlap' and c['hist_column']==hi:
                g,h=map(group_key,c['groups']);v=sum((w for _,w,r in modes[hi] if g in r and h in r),Q())
                assert v==min(q[g],q[h]);assert v>=Q(c['weight']);rr_marginal_checks+=1
        p=sum(a[:3]);pa=sum(a[:4]);ell=sum(a[:5]);whole=sum(a);D=(pa+1)*(pa+2)
        u5=safe(a[4],whole);u6=safe(a[5],whole);ha=safe(a[4]+a[5],whole)+Q(a[4],D)
        nb=sum(w[1] for w in words);nc=sum(w[2] for w in words)
        for mi,w,rset in modes[hi]:
            assert w>0
            z={g:zs[mi,g] for g in gs};assert len(z)==len(gs);mode_checks+=1
            r={g:int(g in rset) for g in gs}
            for e in edges:
                f,i,j=e;ge=keys[e];re=r[ge];ze=z[ge];ti,bi,ci=words[i];yj=words[j][1+f]
                de=p+ti+yj+1;den=pa+re+1;vz=ze/den;vr=w*re/de
                # Original R source and all its old terminal comparisons.
                rows['R-basic',f,'source']+=w*safe(bi,p+ti+bi+ci)-w*safe(yj,p+ti+yj+re)
                for name,query in [('ownB',bi),('ownC',ci),('ownT',ti),('optavg',Q(hc['d'],6)),*[(('actual'+str(k)),a[k]) for k in range(6)],('Bavg',Q(nb,6)),('Cavg',Q(nc,6))]:
                    rows['R-basic',f,name]+=vr-w*query/de
                rows['R-basic',f,'reverse']+=w*safe(ci,p+ti+bi+ci)-w*re/(p+ti+bi+1)
                rows['R-basic',f,'price']+=w*u6-w*re/(ell+1)
                rows['R-basic',f,'capacity']-=w*re
                # New Z source after the actual first four choices.
                rows['nested-basic',f,'source']+=w*u5-w*re/(pa+1)+re*ze/D
                rows['nested-basic',f,'pair']+=w*ha-(w*re+ze)/(pa+1)+re*ze/D
                rows['nested-basic',f,'price']+=w*u6-ze/(ell+1)
                rows['nested-basic',f,'capacity']-=ze
                for k in range(6):rows['nested-basic',f,'actual'+str(k)]+=vz-w*a[k]/den
                rows['nested-basic',f,'ownR']+=vz-w*re/den
                rows['nested-basic',f,'reverseR']+=(w*re-ze)/de
                for k,(tk,bk,ck) in enumerate(words):
                    for query in range(3):
                        pat=canonical((i,j,k))
                        rows['R-old',f,query,pat]+=vr-w*words[k][query]/de
                        rows['nested-Z-old',f,query,pat]+=vz-w*words[k][query]/den
                    pat=canonical((k,i,j));oldpay=w*safe(ck,p+tk+bk+ck)
                    rows['old-R',f,pat]+=oldpay-w*re/(p+tk+bk+1)
                    rows['nested-old-Z',f,pat]+=oldpay-ze/(p+tk+bk+1)
                for ee in edges:
                    g,k,l=ee;gf=keys[ee];rf=r[gf];zf=z[gf];pat=canonical((i,j,k,l))
                    rows['R-R',f,g,pat]+=w*(re-rf)/de
                    rows['Z-R',f,g,pat]+=vz-w*rf/den
                    rows['R-Z',f,g,pat]+=(w*re-zf)/de
                    rows['pair-RR',f,g,pat]+=w*ha-w*(re+rf)/(pa+1)+w*re*rf/D
                    rows['Z-Z',f,g,pat]+=(ze-zf)/den
                    pair_evaluations+=1
    assert len(zs)==sum(len(groups[hi])*len(ms) for hi,ms in modes.items())
    for f,count in ((0,30),(1,36)):
        rows['R-basic',f,'capacity']+=count*K
        rows['nested-basic',f,'capacity']+=count*K
    assert state_bound_checks==194 and 2*rr_marginal_checks==2612
    assert 702+5+len(rows)+state_bound_checks+2*rr_marginal_checks==new['rows']==3949
    assert len(rows)==436 # R32+R-old30+old-R10+RR60+nested64+attractive180+ZZ60
    assert min(rows.values())>=0, min(rows.items(),key=lambda kv:kv[1])
    W=sum(Q(c['weight']) for c in hists.values() if '1' in c['actual_bits'])
    O=sum(Q(c['weight']) for c in hists.values() if c['d']>0)
    assert W==Q(new['fixed_W'])==Q(old['W']) and W<Q(1,2) and O==1
    result={'scope':'Independent differential extension audit; original 702+5 hist/K-only rows inherited unchanged from identified source. No SPE claim.',
      'source_sha256':hashlib.sha256(OLD.read_bytes()).hexdigest(),'extension_sha256':hashlib.sha256(NEW.read_bytes()).hexdigest(),
      'histograms':len(hists),'positive_R_modes':mode_checks,'Z_variables':len(zs),'literal_edge_pairs':pair_evaluations,
      'joint_state_bounds_checked':state_bound_checks,'RR_intersection_checks':rr_marginal_checks,'RR_upper_bounds_checked':2*rr_marginal_checks,'total_rows_accounted':702+5+len(rows)+state_bound_checks+2*rr_marginal_checks,'independently_rebuilt_raw_rows':len(rows),'minimum_rebuilt_slack':str(min(rows.values())),
      'ZZ_classes':60,'structurally_nonempty_ZZ_classes':len({(e[0],ee[0],canonical((*e[1:],*ee[1:]))) for e in edges for ee in edges}),'nonzero_ZZ_classes':sum(v!=0 for k,v in rows.items() if k[0]=='Z-Z'),'minimum_ZZ_slack':str(min(v for k,v in rows.items() if k[0]=='Z-Z')),
      'O':str(O),'W':str(W),'strict_half_gap':str(1-2*W),'conditional_joint_realization':'R deterministic; Z Bernoulli independently per orbit conditional on mode; all rows affine in Z so first moments suffice.'}
    (HERE/'audit_zz_joint.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
