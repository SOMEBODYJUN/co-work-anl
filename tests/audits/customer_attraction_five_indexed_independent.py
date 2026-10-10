"""Standard-library audit reconstructed from individual actions and raw utility.
No discovery modules or compact row evaluator are imported.
"""
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
import json,time
REPO=Path(__file__).resolve().parents[2]
CERTIFICATE_PATH=REPO/'evidence/certificates/customer_attraction/five_player_indexed_bound.json'
LABELS='ABCDEUVWXY'
PATHS={'actual':'ABCDE','second':'AEUVW','third':'ABEXY'}
START={'actual':0,'second':2,'third':3}
FAMILIES=list(PATHS)
SCALE=120

def utility(action,prior):
    return Q(action,sum(prior)+action) if action else Q(0)
def payoff(path,i):return utility(path[i],path[:i]+path[i+1:])
def security(action,prefix,remaining):return Q(action,sum(prefix)+remaining)
def tail_tax(prefix,first):return Q(first,(sum(prefix)+1)*(sum(prefix)+2))
def indices(hist,arity):
    out=[]
    for n,b in zip(hist,product((0,1),repeat=arity)):out.extend([b]*n)
    assert len(out)==5
    return out

def old_individual(b,d,lhs):
    out={};opt=int(d>0);T=[1]*d+[0]*(5-d)
    L=[]
    for ell,h in lhs:
        assert 0<=h<=d and 0<=ell-h<=5-d
        L.append([1]*h+[0]*(d-h)+[1]*(ell-h)+[0]*(5-d-ell+h))
    def sh(pn,i):return payoff([b[t] for t in PATHS[pn]],i)
    for f,(pn,path) in enumerate(PATHS.items()):
        pp=[b[t] for t in path[:3]];ss=[sh(pn,i) for i in range(5)]
        H=ss[3]+ss[4]+tail_tax(pp,b[path[3]])
        for i in range(START[pn],5):
            pre=[b[t] for t in path[:i]];k=5-i
            for topic in LABELS:out[f'{pn}:{i+1}:K:{topic}']=ss[i]-security(b[topic],pre,k)
            out[f'{pn}:{i+1}:sum-opt']=sum((ss[i]-security(t,pre,k) for t in T),Q(0))
            out[f'{pn}:{i+1}:O']=5*k*ss[i]+Q(sum(pre),sum(pre)+k)-opt
        out[f'{pn}:r2:O']=Q(5,2)*H+Q(sum(pp),sum(pp)+1)-opt
        out[f'{pn}:r2:exact-opt']=10*H-sum((utility(T[i],pp+[T[j]]) for i in range(5) for j in range(5) if i!=j),Q(0))
        out[f'{pn}:reply:S']=sum((ss[3]-utility(T[i],pp+[L[f][i]]) for i in range(5)),Q(0))
        out[f'{pn}:reply:V']=sum((utility(L[f][i],pp+[T[i]])-utility(L[f][j],pp+[T[i]]) for i in range(5) for j in range(5) if i!=j),Q(0))
        out[f'{pn}:reply:Z']=sum((ss[4]-utility(l,pp+[b[path[3]]]) for l in L[f]),Q(0))
        out[f'{pn}:reply:P']=sum((ss[4]-utility(t,pp+[b[path[3]]]) for t in T),Q(0))
        out[f'{pn}:reply:clone-opt']=sum((utility(L[f][i],pp+[T[i]])-utility(T[i],pp+[T[i]]) for i in range(5)),Q(0))
        out[f'{pn}:reply:all-opt']=sum((utility(L[f][i],pp+[T[i]])-utility(T[j],pp+[T[i]]) for i in range(5) for j in range(5)),Q(0))
        for g,tf in enumerate(FAMILIES):
            if f!=g:out[f'{pn}:reply:cross-L-{tf}']=sum((utility(L[f][i],pp+[T[i]])-utility(L[g][j],pp+[T[i]]) for i in range(5) for j in range(5)),Q(0))
        for topic in LABELS:out[f'{pn}:reply:topic-{topic}']=sum((utility(L[f][i],pp+[T[i]])-utility(b[topic],pp+[T[i]]) for i in range(5)),Q(0))
        for nn,p2 in PATHS.items():
            for i in range(START[nn],5):out[f'{nn}:{i+1}:sum-L-{pn}']=sum((sh(nn,i)-security(l,[b[t] for t in p2[:i]],5-i) for l in L[f]),Q(0))
    out['F:second']=sh('actual',1)-sh('second',1)
    out['F:third']=sh('actual',2)-sh('third',2)
    return out,T,L

def all_rows(bits,histograms,lhs):
    b=dict(zip(LABELS,bits));tri=[indices(h,3) for h in histograms[:2]];quad=indices(histograms[2],4)
    d=sum(t[0] for t in tri[0]);assert sum(t[0] for t in tri[1])==d==sum(t[0] for t in quad)
    out,T,L=old_individual(b,d,lhs);opt=int(d>0)
    def sh(pn,i):return payoff([b[t] for t in PATHS[pn]],i)
    for tag,data,pre,path0 in [('AB',tri[0],[b['A'],b['B']],'actual'),('AE',tri[1],[b['A'],b['E']],'second')]:
        true=[pre+list(z) for z in data];z3=[payoff(p,2) for p in true];z4=[payoff(p,3) for p in true];z5=[payoff(p,4) for p in true]
        menus={'X':[z[1] for z in data],'Y':[z[2] for z in data]}
        H=[z4[i]+z5[i]+tail_tax(true[i][:3],true[i][3]) for i in range(5)]
        def add(n,v):out[tag+':'+n]=v
        add('F3',sum((sh(path0,2)-v for v in z3),Q(0)))
        for topic in LABELS:
            add('4:K:'+topic,sum((z4[i]-security(b[topic],true[i][:3],2) for i in range(5)),Q(0)))
            add('5:K:'+topic,sum((z5[i]-utility(b[topic],true[i][:4]) for i in range(5)),Q(0)))
        for role,pay,k in [(4,z4,2),(5,z5,1)]:
            add(str(role)+':sum-opt',sum((pay[i]-security(t,true[i][:role-1],k) for i in range(5) for t in T),Q(0)))
            for name,menu in menus.items():add(str(role)+':sum-'+name,sum((pay[i]-security(a,true[i][:role-1],k) for i in range(5) for a in menu),Q(0)))
        add('4:own-T',sum((z4[i]-security(data[i][0],true[i][:3],2) for i in range(5)),Q(0)))
        add('5:own-T',sum((z5[i]-utility(data[i][0],true[i][:4]) for i in range(5)),Q(0)))
        add('5:own-X',sum((z5[i]-utility(data[i][1],true[i][:4]) for i in range(5)),Q(0)))
        add('4:own-Y',sum((z4[i]-security(data[i][2],true[i][:3],2) for i in range(5)),Q(0)))
        add('r2:O',sum((Q(5,2)*H[i]+Q(sum(true[i][:3]),sum(true[i][:3])+1)-opt for i in range(5)),Q(0)))
        add('r2:exact-opt',10*sum(H)-sum((utility(T[j],true[i][:3]+[T[k]]) for i in range(5) for j in range(5) for k in range(5) if j!=k),Q(0)))
        for f,(pn,path) in enumerate(PATHS.items()):
            pp=[b[t] for t in path[:3]];hold=sh(pn,3)+sh(pn,4)+tail_tax(pp,b[path[3]])
            for name,menu in menus.items():
                for i in range(START[pn],5):add(f'{pn}:{i+1}:sum-{name}',sum((sh(pn,i)-security(a,[b[t] for t in path[:i]],5-i) for a in menu),Q(0)))
                add(f'{pn}:reply:all-{name}',sum((utility(L[f][i],pp+[T[i]])-utility(a,pp+[T[i]]) for i in range(5) for a in menu),Q(0)))
            for name,mm,nn in [('XX',menus['X'],menus['X']),('XY',menus['X'],menus['Y']),('YY',menus['Y'],menus['Y'])]:
                add(f'{pn}:r2:menu-{name}',25*hold-sum((utility(a,pp+[c])+utility(c,pp+[a]) for a in mm for c in nn),Q(0)))
        for name,mm,nn in [('XX',menus['X'],menus['X']),('XY',menus['X'],menus['Y']),('YY',menus['Y'],menus['Y'])]:
            add('r2:menu-'+name,25*sum(H)-sum((utility(a,true[i][:3]+[c])+utility(c,true[i][:3]+[a]) for i in range(5) for a in mm for c in nn),Q(0)))
    pre=[b['A']];true=[pre+list(z) for z in quad];menus={m:[z[j] for z in quad] for m,j in [('U',1),('V',2),('W',3)]}
    pays={i:[payoff(p,i-1) for p in true] for i in (3,4,5)}
    out['Sbranch:F2']=sum((sh('actual',1)-payoff(p,1) for p in true),Q(0))
    for role in (3,4,5):
        for topic in LABELS:out[f'Sbranch:{role}:K:{topic}']=sum((pays[role][i]-security(b[topic],true[i][:role-1],6-role) for i in range(5)),Q(0))
        out[f'Sbranch:{role}:sum-opt']=sum((pays[role][i]-security(t,true[i][:role-1],6-role) for i in range(5) for t in T),Q(0))
        for name,menu in menus.items():out[f'Sbranch:{role}:sum-{name}']=sum((pays[role][i]-security(a,true[i][:role-1],6-role) for i in range(5) for a in menu),Q(0))
    for role,name,j in [(3,'T',0),(3,'V',2),(3,'W',3),(4,'U',1),(4,'W',3),(5,'T',0),(5,'U',1),(5,'V',2)]:
        out[f'Sbranch:{role}:own-{name}']=sum((pays[role][i]-security(quad[i][j],true[i][:role-1],6-role) for i in range(5)),Q(0))
    H=[pays[4][i]+pays[5][i]+tail_tax(true[i][:3],true[i][3]) for i in range(5)]
    out['Sbranch:r2:O']=sum((Q(5,2)*H[i]+Q(sum(true[i][:3]),sum(true[i][:3])+1)-opt for i in range(5)),Q(0))
    out['Sbranch:r2:exact-opt']=10*sum(H)-sum((utility(T[j],true[i][:3]+[T[k]]) for i in range(5) for j in range(5) for k in range(5) if j!=k),Q(0))
    for pn,path in PATHS.items():
        for i in range(START[pn],5):
            for name,menu in menus.items():out[f'{pn}:{i+1}:sum-S{name}']=sum((sh(pn,i)-security(a,[b[t] for t in path[:i]],5-i) for a in menu),Q(0))
    return out

def scaled(v):
    x=v*SCALE;assert x.denominator==1
    return x.numerator

def compositions(n,k):
    if k==1:yield (n,);return
    for j in range(n+1):
        for h in compositions(n-j,k-1):yield (j,)+h

def audit():
    t0=time.time();certificate=json.loads(CERTIFICATE_PATH.read_text());pr=certificate['primal'];du=certificate['dual']
    C=int(du['common_denominator']);beta=Q(du['beta']);bn=int(du['beta_numerator']);lam=du['integer_multipliers']
    assert beta==Q(bn,C) and all(Q(du['multipliers'][n])*C==v and v>=0 for n,v in lam.items())
    assert len(pr['atoms'])==64 and len(lam)==57 and pr['denominator']>0 and beta<Q(2063,1000)
    rownames=pr['rows'];assert len(rownames)==len(set(rownames))==437
    totals=dict.fromkeys(rownames,0);w=0;o=0;atomr=[]
    for a in pr['atoms']:
        bits=tuple(map(int,a['bits']));hs=[a['AB_hist'],a['AE_hist'],a['second_hist']]
        assert len(bits)==10 and all(v in (0,1) for v in bits)
        assert [len(h) for h in hs]==[8,8,16] and all(isinstance(v,int) and v>=0 for h in hs for v in h)
        rr=all_rows(bits,hs,a['menus_lh']);assert set(rr)==set(rownames) and len(rr)==437
        num=int(a['mass_numerator']);assert num>0
        rowints={n:scaled(v) for n,v in rr.items()}
        for n,v in rowints.items():totals[n]+=num*v
        flag=int(any(bits[:5]));od=int(sum(n*z[0] for n,z in zip(hs[0],product((0,1),repeat=3)))>0)
        w+=num*flag;o+=num*od
        atomr.append(bn*SCALE*flag-C*SCALE*od-sum(lam[n]*rowints[n] for n in lam))
    denom=int(pr['denominator']);assert w==denom and Q(o,denom)==beta
    assert min(totals.values())>=0 and all(totals[n]==0 for n in lam) and all(x==0 for x in atomr)
    assert Q(pr['gap_above_two'])==beta-2>0
    
    # Active dual compilation from individual history utility; all arithmetic is exact.
    frows={tag:{} for tag in ['AB','AE','Sbranch']};oldlam={}
    for n,v in lam.items():
        tag=n.split(':')[0]
        if tag in frows:frows[tag][n]=v
        elif ':sum-S' in n:frows['Sbranch'][n]=v
        else:oldlam[n]=v
    assert all(n.startswith('F:') or n.split(':')[1].isdigit() or n.split(':')[1:] in [['reply','S'],['reply','V'],['reply','Z']] for n in oldlam)
    hist={};tps={};sparse={};groups={}
    for tag,k in [('AB',3),('AE',3),('Sbranch',4)]:
        tps[tag]=list(product((0,1),repeat=k));hist[tag]=list(compositions(5,2**k))
        sparse[tag]=[[(j,n) for j,n in enumerate(h) if n] for h in hist[tag]]
        groups[tag]=[[] for _ in range(6)]
        for j,h in enumerate(hist[tag]):groups[tag][sum(n*t[0] for n,t in zip(h,tps[tag]))].append(j)
    cache={};masks=0;minrho=None;zeros=0;table=[None]*32
    def family_max(tag,b,d):
        types=tps[tag];p=b['A']+(b['B'] if tag=='AB' else b['E'] if tag=='AE' else 0)
        constant=0;cost=[0]*len(types);nonlinear=[]
        def sh(pn,i):return payoff([b[t] for t in PATHS[pn]],i)
        for name,l in frows[tag].items():
            if name==tag+':F3' or name=='Sbranch:F2':
                orig='actual' if tag!='AE' else 'second';role=1 if tag=='Sbranch' else 2
                constant+=l*scaled(5*sh(orig,role))
                for j,z in enumerate(types):cost[j]-=l*scaled(utility(z[0],[p]+list(z[1:])))
            elif name.startswith(tag+':') and name.split(':')[1].isdigit():
                rest=name[len(tag)+1:];role=int(rest.split(':')[0]);pos=role-(3 if tag!='Sbranch' else 2)
                remain=6-role
                for j,z in enumerate(types):
                    pre=[p]+list(z[:pos]);pay=utility(z[pos],[p]+list(z[:pos])+list(z[pos+1:]))
                    if ':K:' in rest:cost[j]+=l*scaled(pay-security(b[rest[-1]],pre,remain))
                    elif ':sum-' in rest:cost[j]+=l*scaled(5*pay)
                    else:raise AssertionError(name)
                if ':sum-' in rest:
                    menu=rest.split(':sum-')[1];mpos={'X':1,'Y':2,'U':1,'V':2,'W':3}[menu]
                    de=[scaled(security(1,[p]+list(z[:pos]),remain)) for z in types]
                    nonlinear.append((l,mpos,tuple(de)))
            else:
                rest=name[len(tag)+1:] if name.startswith(tag+':') else name
                pn,role,menu=rest.split(':');assert menu.startswith('sum-')
                role=int(role)-1;m=menu.split('sum-')[1].replace('S','');mpos={'X':1,'Y':2,'U':1,'V':2,'W':3}[m]
                pre=[b[t] for t in PATHS[pn][:role]]
                constant+=l*scaled(5*sh(pn,role))
                for j,z in enumerate(types):cost[j]-=l*scaled(security(z[mpos],pre,5-role))
        key=(tag,d,tuple(cost),tuple(nonlinear))
        if key not in cache:
            best=None
            for hi in groups[tag][d]:
                sp=sparse[tag][hi];v=sum(cost[j]*n for j,n in sp)
                for l,pos,de in nonlinear:
                    count=sum(types[j][pos]*n for j,n in sp)
                    den=sum(de[j]*n for j,n in sp)
                    v-=l*count*den
                if best is None or v>best:best=v
            cache[key]=best
        return constant+cache[key]
    for bits in product((0,1),repeat=10):
        b=dict(zip(LABELS,bits));flag=int(any(bits[:5]));pattern=sum(bits[i]<<(4-i) for i in range(5))
        for d in range(6):
            rr,_,_=old_individual(b,d,[(0,0)]*3)
            score=sum(l*scaled(rr[n]) for n,l in oldlam.items())
            for pn,path in PATHS.items():
                ls=oldlam.get(pn+':reply:S',0);lv=oldlam.get(pn+':reply:V',0);lz=oldlam.get(pn+':reply:Z',0)
                assert ls==5*lv
                p=sum(b[t] for t in path[:3]);co=lv*scaled(Q(d,(p+1)*(p+2)))-lz*scaled(Q(1,p+b[path[3]]+1))
                score+=max(0,5*co)
            score+=sum(family_max(tag,b,d) for tag in frows)
            rho=bn*SCALE*flag-C*SCALE*int(d>0)-score
            assert rho>=0,(bits,d,rho)
            minrho=rho if minrho is None else min(minrho,rho)
            table[pattern]=rho if table[pattern] is None else min(table[pattern],rho)
            zeros+=int(rho==0);masks+=1

    result={'success':True,'method':'Raw per-index Fraction utility and exact scaled separated histogram maximization; no discovery/core imports','row_count':437,'primal_atoms':len(pr['atoms']),'nonnegative_primal_slacks':437,'zero_primal_slacks':sum(v==0 for v in totals.values()),'nonnegative_dual_multipliers':len(lam),'global_fixed_mask_d_cases':masks,'histogram_counts':{tag:len(hist[tag]) for tag in hist},'histogram_score_contexts':len(cache),'minimum_scaled_residual':minrho,'zero_separated_cases':zeros,'actual_pattern_minima':table,'beta':str(beta),'gap_above_two':str(beta-2),'primal_welfare':str(Q(w,denom)),'primal_cover':str(Q(o,denom)),'seconds':time.time()-t0}
    import hashlib
    result['certificate_sha256']=hashlib.sha256(CERTIFICATE_PATH.read_bytes()).hexdigest()
    result['audit_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    primary=json.loads((REPO/'evidence/runs/2026-10-10/customer_attraction_five_indexed.json').read_text())
    assert primary['certificate_sha256']==result['certificate_sha256']
    assert primary['dual_beta']==result['beta'] and primary['zero_conditional_residuals']==result['zero_separated_cases']
    assert [primary['minimum_by_actual_mask'][format(i,'05b')] for i in range(32)]==list(map(str,result['actual_pattern_minima']))
    result['matches_primary_actual_pattern_minima']=True
    print(json.dumps(result,indent=2),flush=True)
if __name__=='__main__':audit()
