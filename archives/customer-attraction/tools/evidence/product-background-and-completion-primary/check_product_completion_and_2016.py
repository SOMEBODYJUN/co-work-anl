"""One NEW exact entry: product boundary, two-player completion, 2016 rows.

No original missing CLI, old GX53/100, old GO557/220, policy search,
61-atom point, solver or original weak-iid policy audit is run here.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product,combinations_with_replacement
from collections import defaultdict
import hashlib,json
E=Path(__file__).resolve().parent;OUT=E/'new-product-completion-and-2016.json'
if OUT.exists():raise SystemExit('Successful new definition entry exists; do not rerun')

def comp(n,k):
    if k==1:yield(n,);return
    for j in range(n+1):
        for tail in comp(n-j,k-1):yield(j,)+tail

# Discrete chord and explicit independent constructions, finite own domain.
pcases=[];load_vectors=constructed_products=product_ordered_outcomes=0
for K in range(1,6):
    for r in range(6):
        q,s=divmod(r,K);V=F(K-s,K*(q+1))+F(s,K*(q+2));equal=0
        for h in comp(r,K):
            load_vectors+=1;avg=sum((F(1,x+1) for x in h),F(0))/K
            assert avg>=V
            for x in h:
                rem=F(1,x+1)-(F(1,q+1)-F(x-q,(q+1)*(q+2)))
                assert rem==F((x-q)*(x-q-1),(x+1)*(q+1)*(q+2))>=0
            if avg==V:
                assert all(x in (q,q+1) for x in h);equal+=1
        base=[q+int(j<s) for j in range(K)]
        cyclic=[sum((F(1,base[(j-i)%K]+1) for i in range(K)),F(0))/K for j in range(K)]
        assert cyclic==[V]*K
        attainable=(s==0 or K%s==0)
        queries=None;outcomes=0
        if attainable:
            marginals=[]
            for j in range(K):marginals.extend([{j:F(1)} for _ in range(q)])
            if s:
                block=K//s
                for i in range(s):marginals.append({j:F(1,block) for j in range(i*block,(i+1)*block)})
            assert len(marginals)==r
            queries=[F(0)]*K;probability=F(0)
            for choices in product(*(list(p.items()) for p in marginals)):
                labels=[j for j,w in choices];prob=F(1)
                for j,w in choices:prob*=w
                probability+=prob;outcomes+=1
                for j in range(K):queries[j]+=prob*F(1,1+labels.count(j))
            assert probability==1 and queries==[V]*K
            constructed_products+=1;product_ordered_outcomes+=outcomes
        pcases.append({'K':K,'r':r,'q':q,'s':s,'V':V,'balanced_count_vectors':equal,'product_attainment_by_proved_condition':attainable,'constructed_product_query_values':queries,'enumerated_constructed_outcomes':outcomes})

# Exact feasible K3,r2 product in Q[t]/(2t^2+5t-4). No optimization.
def qa(x,y):return x[0]+y[0],x[1]+y[1]
def qm(x,y):return x[0]*y[0]+2*x[1]*y[1],x[0]*y[1]+x[1]*y[0]-F(5,2)*x[1]*y[1]
def qs(x,c):return x[0]*c,x[1]*c
zero=(F(0),F(0));one=(F(1),F(0));t=(F(0),F(1));omt=(F(1),F(-1))
p1=[t,omt,zero];p2=[zero,omt,t];alg=[]
for query in range(3):
    val=zero
    for i,j in product(range(3),repeat=2):val=qa(val,qs(qm(p1[i],p2[j]),F(1,1+int(i==query)+int(j==query))))
    alg.append(val)
assert alg==[(F(1),F(-1,2))]*3
lo,hi=F(63,100),F(16,25)
assert 2*lo*lo+5*lo-4<0<2*hi*hi+5*hi-4 and 0<lo<hi<F(2,3)
assert F(1)-hi/2>F(2,3)

# The unit-client two-player noncompletion illustration.
A=set(range(4));T=set(range(2,8));B=set(range(8,13));catalog=[A,B,T];names=['A','B','T']
def payoff(z,i):return sum((F(1,sum(x in catalog[a] for a in z)) for x in catalog[z[i]]),F(0))
BR={a:[b for b in range(3) if payoff((a,b),1)==max(payoff((a,c),1) for c in range(3))] for a in range(3)}
L={a:min(payoff((a,b),0) for b in BR[a]) for a in range(3)};threshold=max(L.values())
fullSPE=[];node_comparisons=0;formal_policies=0
for replies in product(*(BR[a] for a in range(3))):
    for root in range(3):
        formal_policies+=1;ok=True
        for a in range(3):
            for alt in range(3):
                node_comparisons+=1
                if payoff((a,replies[a]),1)<payoff((a,alt),1):ok=False
        for alt in range(3):
            node_comparisons+=1
            if payoff((root,replies[root]),0)<payoff((alt,replies[alt]),0):ok=False
        if ok:fullSPE.append({'root':root,'last_by_root':replies,'path':(root,replies[root])})
criteria=[]
for a,b in product(range(3),repeat=2):
    criterion=b in BR[a] and payoff((a,b),0)>=threshold
    realized=any(x['path']==(a,b) for x in fullSPE)
    assert criterion==realized
    criteria.append({'path':(names[a],names[b]),'B_is_best_reply':b in BR[a],'entering_payoff':payoff((a,b),0),'threshold':threshold,'completion_exists':criterion})
assert len(fullSPE)==2 and {tuple(x['path']) for x in fullSPE}=={(2,1)}
U=payoff((0,1),0)+payoff((0,1),1);tax=F(len(A),2);H=U+tax
pairslacks={}
for i,j in product(range(3),repeat=2):pairslacks[names[i]+names[j]]=H-(len(catalog[i])+len(catalog[j])-F(len(catalog[i]&catalog[j]),2))
assert U==9 and H==11 and all(v>=0 for v in pairslacks.values()) and pairslacks['TB']==0
assert payoff((2,1),0)-payoff((0,1),0)==2 and F(len(A),2)-F(len(A&B),2)==2

# 2016 previously untested rows on the SAME new60 point: do not recompute
# its already-successful old557 slacks or GO cross-family220 envelopes.
P=E/'comparison/research/workspaces/customer-attraction/R-c4732bee2f7b4e50a70568170e3334ae/round4_pricing/exact_primal_overlap1.json'
assert hashlib.sha256(P.read_bytes()).hexdigest()=='11a26c56faca5a3331a4f2ab002455aa6ca115f999ddde2eced6f1edd39c0825'
point=json.loads(P.read_text());atoms=point['atoms'];assert len(atoms)==60
total=defaultdict(F);peratom=[]
paths=[('actual',(0,1,2,3,4)),('second',(0,4,5,6,7)),('third',(0,1,4,8,9))]
spec=[('AB','AB_hist',3,(0,1)),('AE','AE_hist',3,(0,4)),('SB','second_hist',4,(0,))]
def frac(n,d):return F(n,d) if n else F(0)
for ai,atom in enumerate(atoms):
    bits=tuple(map(int,atom['bits']));w=F(atom['exact_mass']);expanded={};q=5
    for tag,key,dim,fixed in spec:
        states=list(product((0,1),repeat=dim));expanded[tag]=[s for s,n in zip(states,atom[key]) for _ in range(n)]
    ds=[sum(s[0] for s in expanded[tag]) for tag,key,dim,fixed in spec];assert len(set(ds))==1;d=ds[0]
    menus=[(x,1,b) for x,b in zip('ABCDEUVWXY',bits)]+[('T',5,d)]
    menus += [('L.'+name,5,atom['menus_lh'][i][0]) for i,(name,path) in enumerate(paths)]
    for tag,key,dim,fixed in spec:
        for pos in range(1,dim):menus.append((tag+'.'+str(pos),5,sum(s[pos] for s in expanded[tag])))
    assert len(menus)==21
    sources=[];rows={}
    for name,path in paths:
        p=sum(bits[i] for i in path[:3]);v=bits[path[3]];z=bits[path[4]]
        Hh=frac(v+z,p+v+z)+F(v,(p+1)*(p+2))
        sources.append((name,[p],[Hh]))
    for tag,key,dim,fixed in spec:
        fixedload=sum(bits[i] for i in fixed);p=[fixedload+sum(s[:-2]) for s in expanded[tag]]
        hh=[frac(s[-2]+s[-1],v+s[-2]+s[-1])+F(s[-2],(v+1)*(v+2)) for s,v in zip(expanded[tag],p)]
        sources.append((tag,p,hh))
    for name,p,hh in sources:
        Hsum=sum(hh,F(0));aa=sum((F(1,v+1) for v in p),F(0));bb=sum((F(1,(v+1)*(v+2)) for v in p),F(0))
        for (M,nM,mM),(N,nN,mN) in combinations_with_replacement(menus,2):
            rows[f'cart:{name}:{M}:{N}']=nM*nN*Hsum-(nN*mM+nM*mN)*aa+mM*mN*bb
    assert len(rows)==1386
    for tag,key,dim,fixed in spec:
        ss=expanded[tag];fixedload=sum(bits[i] for i in fixed);pp=[fixedload+sum(s[:-2]) for s in ss]
        hh=[frac(s[-2]+s[-1],v+s[-2]+s[-1])+F(s[-2],(v+1)*(v+2)) for s,v in zip(ss,pp)]
        Hsum=sum(hh,F(0));aa=sum((F(1,v+1) for v in pp),F(0));bb=sum((F(1,(v+1)*(v+2)) for v in pp),F(0))
        for own in range(dim):
            z=[s[own] for s in ss];Z=sum(z);za=sum((F(zz,v+1) for zz,v in zip(z,pp)),F(0));zb=sum((F(zz,(v+1)*(v+2)) for zz,v in zip(z,pp)),F(0))
            for N,nN,mN in menus:
                rows[f'diag:{tag}:{own}:{N}']=nN*Hsum-nN*za-mN*aa+mN*zb
                rows[f'off:{tag}:{own}:{N}']=(q-1)*nN*Hsum-nN*(Z*aa-za)-(q-1)*mN*aa+mN*(Z*bb-zb)
        for pos in range(1,dim):
            current=sum((frac(s[pos],fixedload+sum(s)) for s in ss),F(0))
            worst=sum((F(1,fixedload+sum(s[:pos])+dim-pos) for s in ss),F(0))
            for N,nN,mN in menus:rows[f'direct:{tag}:{pos}:{N}']=nN*current-mN*worst
    for idx,(name,path) in enumerate(paths):
        p=sum(bits[i] for i in path[:3]);ell,h=atom['menus_lh'][idx]
        current=F(ell-h,p+1)+F(h,p+2);inverse=F(q-d,p+1)+F(d,p+2)
        for N,nN,mN in menus:rows[f'direct:L.{name}:{N}']=nN*current-mN*inverse
    assert len(rows)==2016
    for name,val in rows.items():total[name]+=w*val
    peratom.append({'atom':ai,'mass':w,'coefficients':[rows[name] for name in sorted(rows)]})
assert len(total)==2016 and all(v>=0 for v in total.values())

def enc(v):
    if isinstance(v,F):return str(v)
    if isinstance(v,dict):return {k:enc(x) for k,x in v.items()}
    if isinstance(v,(tuple,list)):return [enc(x) for x in v]
    return v
result={'status':'passed','new_math_entry_attempts':1,'new_math_entry_successes':1,'failed_math_attempts':0,'original_CLI_entries':0,'external_solver_calls':0,
 'product':{'K_range':[1,5],'r_range':[0,5],'parameter_cases':len(pcases),'count_vectors':load_vectors,'constructed_products':constructed_products,'constructed_product_ordered_outcomes':product_ordered_outcomes,'cases':pcases,'general_iff_by_analytic_proof_not_finite_scan':True,'K3r2_feasible_product_query_values_Qt':alg,'t_isolating_interval':[lo,hi],'minimal_polynomial':'2t^2+5t-4','product_optimum_not_claimed':True},
 'two_player':{'unit_clients':13,'catalog':{n:sorted(c) for n,c in zip(names,catalog)},'BR':{names[a]:[names[b] for b in bs] for a,bs in BR.items()},'worst_entering_L':{names[a]:v for a,v in L.items()},'threshold':threshold,'advertised_path':['A','B'],'advertised_W':U,'advertised_H':H,'all9_pair_slacks':pairslacks,'actual_root_profitable_T_gap':F(2),'formal_reply_policy_root_pairs':formal_policies,'literal_node_comparisons':node_comparisons,'fullSPE_count':len(fullSPE),'fullSPE_policies':fullSPE,'nine_path_completion_criteria':criteria,'only_fullSPE_ordered_path':['T','B'],'not_half_counterexample':True},
 'new60_2016':{'input_sha256':hashlib.sha256(P.read_bytes()).hexdigest(),'atoms':60,'menu_lists':21,'row_counts':{'Cartesian':1386,'ownindex_diag_offdiag':420,'direct':210},'rows':len(total),'atom_coefficients':60*2016,'zero_total_slacks':sum(v==0 for v in total.values()),'minimum_total_slack':min(total.values()),'row_order':sorted(total),'total_slacks':dict(total),'atom_rows':peratom,'all_nonnegative':True,'old557_orGO220_recomputed':False},
 'not_newly_verified':['missingoriginal70policysearchandselected9over5witness','missing61atom717pointtwoexactnegativecuts','oldweakpolicyfulltrees/GX53and100','GOold557andcross220'],
 'scope':'Own finite product construction checks, exact two-player completion illustration and new2016 rows on selected60. No universal welfare proof, full policy search certification or numerical product optimum.'}
OUT.write_text(json.dumps(enc(result),ensure_ascii=False,indent=2)+'\n')
print(json.dumps(enc({'status':'passed','product_cases':len(pcases),'count_vectors':load_vectors,'constructed_products':constructed_products,'two_player_fullSPE':len(fullSPE),'2016_rows':len(total),'2016_negative_rows':sum(v<0 for v in total.values()),'2016_zero_rows':sum(v==0 for v in total.values()),'new_entries':1,'original_entries':0,'solver_calls':0}),ensure_ascii=False))
