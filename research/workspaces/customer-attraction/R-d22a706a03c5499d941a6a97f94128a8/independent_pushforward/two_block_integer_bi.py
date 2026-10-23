from pathlib import Path
import numpy as np,json,time
from fractions import Fraction as F

def comps(total,k):
    if k==1:yield (total,);return
    for q in range(total+1):
        for rest in comps(total-q,k-1):yield (q,)+rest

def main():
    start=time.time();m=8;k=8;scale=840
    levels=[list(comps(s,k)) for s in range(m+1)];states=sum(levels,[]);ix={q:i for i,q in enumerate(states)};tails=levels[m];tx={q:i for i,q in enumerate(tails)};T=len(tails)
    print('states',len(states),'terminals',T,flush=True)
    types=[]
    for shift in (0,4):
        for mask,w in [(1,2),(10,4),(5,6),(12,3),(15,1)]:types.append((mask<<shift,w))
    pay=np.zeros((k,T),np.int64)
    for j,q in enumerate(tails):
        for mask,w in types:
            load=sum(q[a] for a in range(k) if mask>>a&1)
            if load:
                for a in range(k):
                    if q[a] and mask>>a&1:pay[a,j]+=w*(scale//load)
    R=np.zeros((len(states),T),bool);threshold=np.zeros(len(states),np.int64)
    for j,q in enumerate(tails):R[ix[q],j]=True
    for depth in range(m-1,-1,-1):
        for q in levels[depth]:
            children=[];floors=[]
            for a in range(k):
                z=list(q);z[a]+=1;zz=ix[tuple(z)];children.append(zz);floors.append(int(pay[a,R[zz]].min()))
            h=max(floors);threshold[ix[q]]=h
            for a,ch in enumerate(children):R[ix[q]] |= R[ch] & (pay[a]>=h)
        print('depth',depth,'seconds',round(time.time()-start,2),'outcomes',int(R[[ix[q] for q in levels[depth]]].sum()),flush=True)
    base=(2,1,1,0);local=[[(2,0,1,1)],[(1,1,1,1),(2,1,0,1)],[(1,0,2,1)],[(1,0,1,2)]]
    out={'scale':scale,'root_threshold':str(F(int(threshold[ix[(0,)*8]]),scale)),'root_targets':[]}
    for a in range(k):
        pref=tuple(int(a==z) for z in range(k));row={'root':a,'targets':[]}
        for loc in local[a%4]:
            q=loc+base if a<4 else base+loc;j=tx[q]
            row['targets'].append({'counts':q,'child_realizable':bool(R[ix[pref],j]),'root_payoff':str(F(int(pay[a,j]),scale))})
        out['root_targets'].append(row)
    # A complete finite-state strategy certificate: the memory target is updated
    # separately after every actual action, so no ordered histories are merged.
    nodes=[];memo={}
    def make(q,target):
        key=(q,target)
        if key in memo:return memo[key]
        nodeid=len(nodes);memo[key]=nodeid;node={'counts':list(q),'target':target,'action':None,'children':[]};nodes.append(node)
        if sum(q)==m:
            assert tx[q]==target
            return nodeid
        h=threshold[ix[q]];options=[]
        for a in range(k):
            z=list(q);z[a]+=1;qq=tuple(z);idx=ix[qq]
            if R[idx,target] and pay[a,target]>=h:options.append(a)
        assert options
        chosen=options[0];node['action']=chosen
        for a in range(k):
            z=list(q);z[a]+=1;qq=tuple(z)
            if a==chosen:childtarget=target
            else:
                ids=np.flatnonzero(R[ix[qq]])
                childtarget=int(ids[np.argmin(pay[a,ids])])
            node['children'].append(make(qq,childtarget))
        return nodeid
    root={'counts':[0]*8,'target':tx[(1,0,1,2)+base],'action':3,'children':[]}
    for a in range(k):
        pref=tuple(int(a==z) for z in range(k));loc=local[a%4][0]
        target=loc+base if a<4 else base+loc
        root['children'].append(make(pref,tx[target]))
    # Definition-level DAG audit does not consult R, thresholds, or feasibility.
    customers=[(mask,w) for mask,w in types]
    seen={}
    def utility(q,a):
        return sum(F(w,sum(q[t] for t in range(k) if mask>>t&1)) for mask,w in customers if mask>>a&1)
    def audit(node):
        q=tuple(node['counts'])
        if sum(q)==m:
            assert node['action'] is None and not node['children'] and tx[q]==node['target']
            return q
        leaves=[]
        for a,nid in enumerate(node['children']):
            child=nodes[nid];wanted=list(q);wanted[a]+=1
            assert child['counts']==wanted
            if nid not in seen:seen[nid]=audit(child)
            leaves.append(seen[nid])
        chosen=node['action'];actual=leaves[chosen]
        assert tx[actual]==node['target']
        assert all(utility(actual,chosen)>=utility(leaves[a],a) for a in range(k))
        return actual
    actual=audit(root);out['DAG_certificate']={'nodes':len(nodes),'visited':len(seen),'actual_counts':list(actual),'valid':True}
    certpath=Path(__file__).with_name('two_block_integer_bi_certificate.json')
    certpath.write_text(json.dumps({'players':m,'topics':k,'customer_types':types,'terminals':tails,'root':root,'nodes':nodes},separators=(',',':'))+'\n')
    path=Path(__file__).with_name('two_block_integer_bi_result.json');path.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2),flush=True)
if __name__=='__main__':main()
