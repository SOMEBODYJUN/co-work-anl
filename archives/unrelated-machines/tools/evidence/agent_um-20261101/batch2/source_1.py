#!/usr/bin/env python3
"""Independent exact audit of sparse-path deep shared-sink conditional CONFIG.
Formal theorem domain k>=3; expanded k=3 is a domain-instance structural test.
No external LP solver or proposer code is used. Raw instance has omitted infinity edges.
"""
from fractions import Fraction as F
from collections import defaultdict
import hashlib,json,sys,platform


def parameters(k):
    r=F(k-1,k);s0=1
    while k*r**s0>1:s0+=1
    assert s0>=2
    M=(k-1)*k**(s0-2);H=s0
    while 2**(H-2)<M:H+=1
    return r,s0,M,H,F(1,2**(H-2))

class Audit:
    def __init__(self,k):
        self.k=k;self.r,self.s0,self.M,self.H,self.gamma=parameters(k)
        self.T=F(k+1,k);self.B=F(2*k-1,k);self.z=('z',)
        self.jobs={};self.cores=[];self.blocks=[];self.children={};self.incoming={}
        self.types={};self.ordinary={}
        for tree in range(2):
            level=[()]
            for depth in range(self.H):
                for address in level:
                    v=(tree,address);self.cores.append(v);self.children[v]=[]
                    if depth==self.H-1:
                        self.blocks.append(v)
                        for t in range(k):
                            j=('star',tree,address,t);u=('t',tree,address,t)
                            self.jobs[j]={v:F(1,k),u:F(1)};self.types[j]='star'
                            self.children[v].append(j);self.ordinary[j]=(v,u)
                    else:
                        for c in range(k):
                            child=(tree,address+(c,));j=('core',tree,address,c)
                            self.jobs[j]={v:F(1,k),child:F(1)};self.types[j]='core'
                            self.children[v].append(j);self.incoming[child]=j;self.ordinary[j]=(v,child)
                level=[a+(c,) for a in level for c in range(k)]
        bridge=('bridge',);self.bridge=bridge
        self.jobs[bridge]={(0,()):F(1),(1,()):F(1)};self.types[bridge]='bridge'
        self.incoming[(0,())]=bridge;self.incoming[(1,())]=bridge
        for tree,address in self.blocks:
            for t in range(k-1):
                j=('block',tree,address,t)
                self.jobs[j]={('t',tree,address,t):F(1),('t',tree,address,t+1):F(1),self.z:self.gamma}
                self.types[j]='block'
        self.machines=set(i for p in self.jobs.values() for i in p)
        self.block_jobs={v:[('block',v[0],v[1],t) for t in range(k-1)] for v in self.blocks}

    def witness(self,query=None):
        k=self.k;alpha={v:F(0) for v in self.cores};parent_remove={};escaped=set();star_override={};path_forced={}
        # A query's tree gets bridge mass zero except for a bridge query.
        chosen_tree=0
        if query is not None:
            j,i=query
            typ=self.types[j]
            if typ=='bridge':chosen_tree=i[0]
            elif typ in ('core','star','block'):chosen_tree=1-j[1]
        for v in self.cores:
            if v[0]==chosen_tree:alpha[v]=self.r**len(v[1])
        if query is not None:
            j,i=query;typ=self.types[j]
            if typ=='core':
                parent,child=self.ordinary[j]
                if i==child:
                    parent_remove[parent]=j
                    depth=len(child[1]);s=self.H-depth
                    for v in self.cores:
                        if v[0]==child[0] and v[1][:depth]==child[1]:
                            alpha[v]=self.r**(len(v[1])-depth)
                    if s<self.s0:
                        for v in self.blocks:
                            if v[0]==child[0] and v[1][:depth]==child[1]:escaped.update(self.block_jobs[v])
            elif typ=='star':
                parent,terminal=self.ordinary[j]
                if i==terminal:
                    parent_remove[parent]=j;star_override[parent]=(j,terminal)
                    path_forced[parent]=('vacant',terminal[-1])
            elif typ=='block':
                v=(j[1],j[2])
                if i==self.z:escaped.add(j)
                else:path_forced[v]=('forced',j[-1],i[-1])
        configs=defaultdict(list)
        # Each tuple is (weight, frozenset of jobs); include empty configurations.
        def add(i,w,S):
            if w:configs[i].append((w,frozenset(S)))
        for v in self.cores:
            a=alpha[v];inc=self.incoming[v];outs=self.children[v]
            if v in parent_remove:
                assert a==0
                add(v,F(1),[j for j in outs if j!=parent_remove[v]])
            else:
                add(v,1-a,outs)
                for j in outs:add(v,a/k,[inc,j])
        for v in self.blocks:
            a=self.r*alpha[v]
            for t in range(k):
                i=('t',v[0],v[1],t);star=('star',v[0],v[1],t)
                am=F(1) if v in star_override and star_override[v][0]==star else (F(0) if v in star_override else a)
                add(i,am,[star]);occ=am
                for b in self.block_jobs[v]:
                    if b in escaped:continue
                    left=b[-1];right=left+1
                    if v in path_forced:
                        rule=path_forced[v]
                        if rule[0]=='vacant':dest=left if left<rule[1] else right
                        else:dest=left if rule[2]==rule[1] else right
                        bm=F(int(t==dest))
                    elif t==left:bm=F(k-1-left,k)
                    elif t==right:bm=F(left+1,k)
                    else:bm=F(0)
                    add(i,bm,[b]);occ+=bm
                add(i,1-occ,[])
        add(self.z,F(1),escaped)
        return configs

    def validate(self,configs,query=None):
        coverage=defaultdict(F);marginal=defaultdict(F);big_count=defaultdict(F);maxload=F(0);sinkload=F(0);count=0
        for i,cols in configs.items():
            mass=F(0)
            for w,S in cols:
                assert w>=0,(i,w,S)
                mass+=w;load=F(0);count+=1
                for j in S:
                    assert i in self.jobs[j]
                    load+=self.jobs[j][i];coverage[j]+=w;marginal[i,j]+=w
                    if self.jobs[j][i]>self.T/2:big_count[i]+=w
                assert load<=self.T,(i,load,self.T)
                maxload=max(maxload,load)
                if i==self.z:sinkload=max(sinkload,load)
            assert mass==1,(i,mass)
        assert all(coverage[j]==1 for j in self.jobs)
        assert all(big_count[i]<=1 for i in self.machines)
        if query:
            j,i=query;assert marginal[i,j]==1,(query,marginal[i,j])
        return {'columns':count,'max_configuration_load':str(maxload),'sink_configuration_load':str(sinkload),'max_projected_big_cardinality':str(max(big_count.values(),default=F(0)))}

    def upper_schedule(self):
        sigma={};active_tree=0
        sigma[self.bridge]=(active_tree,())
        # Follow all-zero labels to terminal zero, orient its path away from terminal zero.
        for j,(parent,child) in self.ordinary.items():
            if parent[0]==active_tree and all(c==0 for c in parent[1]) and j[-1]==0:sigma[j]=child
            else:sigma[j]=parent
        for v in self.blocks:
            vacant=0
            for b in self.block_jobs[v]:sigma[b]=('t',v[0],v[1],b[-1]+1)
        loads=defaultdict(F)
        for j,i in sigma.items():loads[i]+=self.jobs[j][i]
        assert len(sigma)==len(self.jobs)
        assert max(loads.values())==self.B
        return {'makespan':str(max(loads.values())),'all_jobs_assigned':len(sigma)}

    def representatives(self):
        out=[]
        for tree in range(2):
            out.append((self.bridge,(tree,())))
            for depth in range(1,self.H):
                j=('core',tree,(0,)*(depth-1),0)
                for i in self.jobs[j]:out.append((j,i))
            for t in range(self.k):
                j=('star',tree,(0,)*(self.H-1),t)
                for i in self.jobs[j]:out.append((j,i))
            for t in range(self.k-1):
                j=('block',tree,(0,)*(self.H-1),t)
                for i in self.jobs[j]:out.append((j,i))
        return out

def bag_and_preprocessing_checks(a):
    z=a.z;bags={('bridgebag',):frozenset([(0,()),(1,()),z])};edges=[]
    for tree,address in a.cores:
        if not address:continue
        key=('corebag',tree,address)
        bags[key]=frozenset([(tree,address[:-1]),(tree,address),z])
        parent=('bridgebag',) if len(address)==1 else ('corebag',tree,address[:-1])
        edges.append((key,parent))
    for v in a.blocks:
        tree,address=v
        for t in range(a.k-1):
            key=('pathbag',tree,address,t)
            bags[key]=frozenset([v,('t',tree,address,t),('t',tree,address,t+1),z])
            parent=('corebag',tree,address) if t==0 else ('pathbag',tree,address,t-1)
            edges.append((key,parent))
    adjacency=defaultdict(set)
    for u,v in edges:adjacency[u].add(v);adjacency[v].add(u)
    def connected(nodes):
        seen=set();stack=[next(iter(nodes))]
        while stack:
            u=stack.pop()
            if u in seen:continue
            seen.add(u);stack.extend(adjacency[u]&nodes-seen)
        return seen==nodes
    assert len(edges)==len(bags)-1 and connected(set(bags))
    for i in a.machines:
        occurs={b for b,S in bags.items() if i in S}
        assert occurs and connected(occurs)
    for j,p in a.jobs.items():assert any(set(p)<=S for S in bags.values())
    max_separator=max(len(bags[u]&bags[v]) for u,v in edges)
    assert max(map(len,bags.values()))==4 and max_separator==3
    neighbours=defaultdict(list)
    for j,p in a.jobs.items():
        for i,v in p.items():neighbours[i].append((j,v))
    triggered=[]
    for i,items in neighbours.items():
        total=sum((p for j,p in items),F(0))
        if total>a.T and all(total-p<=a.T for j,p in items):triggered.append(i)
    endpoints={('t',v[0],v[1],t) for v in a.blocks for t in [0,a.k-1]}
    assert set(triggered)==endpoints
    return {'bags':len(bags),'bag_tree_edges':len(edges),'max_bag_size':4,'max_separator_size':max_separator,
            'all_job_domains_contained':True,'all_machine_running_intersections_checked':True,
            'minimal_star_triggers':len(triggered),'trigger_set':'exactly both endpoint terminals of every block'}

def formula_checks():
    rows=[]
    for k in range(3,41):
        r,s0,M,H,g=parameters(k)
        assert k*r**(s0-1)>1 and k*r**s0<=1
        assert H>=s0 and g*M<=1 and g*2**(H-1)==2
        for d in range(1,H):
            s=H-d
            escaped=(k-1)*k**(s-1) if s<s0 else 0
            assert escaped<=M and g*escaped<=1
        assert F(2*k-1,k)/F(k+1,k)==2-F(3,k+1)
        rows.append({'k':k,'s0':s0,'H':H,'M':str(M),'gamma':str(g)})
    return {'k_range':[3,40],'parameter_and_all_depth_cases':len(rows),'rows':rows}

if __name__=='__main__':
    a=Audit(3)
    reps=[(j,i) for j,p in a.jobs.items() for i in p];checks=[]
    for query in reps:
        checks.append(a.validate(a.witness(query),query))
    baseline=a.validate(a.witness())
    data={'status':'passed','python':platform.python_version(),'arithmetic':'fractions.Fraction; exact rational; no LP oracle',
          'source_sha256':hashlib.sha256(open(__file__,'rb').read()).hexdigest(),
          'expanded_test':{'k':3,'formal_domain':True,'H':a.H,'s0':a.s0,'machines':len(a.machines),'jobs':len(a.jobs),
                           'finite_edges':sum(map(len,a.jobs.values())),'queries':len(reps),'scope':'every expanded finite edge; full x_e=1 configuration certificate checked independently',
                           'baseline':baseline,'upper_schedule':a.upper_schedule(),'max_sink_load_over_queries':str(max(F(x['sink_configuration_load']) for x in checks))},
          'formula_checks':formula_checks(),
          'bag_and_preprocessing_checks':bag_and_preprocessing_checks(a),
          'not_checked':['Expanded k>=4 instances: exponential size prevents explicit expansion here.',
                         'General theorem relies on mathematical proof, not these finite checks.',
                         'No global priority/novelty certification or target approximation algorithm.']}
    json.dump(data,sys.stdout,ensure_ascii=False,indent=2);print()
