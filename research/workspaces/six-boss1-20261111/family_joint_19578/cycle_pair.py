"""General two-old-node/B4 cyclic marginal domain, with fourteen true ICs.

e=(0,i,j), f=(1,i,k), where i,j,k are pairwise distinct. Each complete
old-word triple orbit keeps e's own four-state marginal, f's own four-state
marginal, and the complete B4 state marginal. No threshold construction is
imposed. Different triple groups may still have different joint tables.
"""
from __future__ import annotations
import argparse
from collections import Counter,defaultdict
from fractions import Fraction as Q
from hashlib import sha256
from itertools import permutations,product
from pathlib import Path
import json

HERE=Path(__file__).resolve().parent
WORK=HERE.parent
DEFAULT_POINT=WORK/'discounted_augmented_lp/augmented_lp_exact.json'
STATES=((0,0),(0,1),(1,0),(1,1))
SPECS=(('F-to-Re',),('F-to-Ze',),('F-to-Rf',),('F-to-Zf',),
       ('Ze-to-X',0,'H1'),('Ze-to-X',1,'H2'),('Ze-to-X',2,'Y-average'),
       ('Zf-to-X',0,'H1'),('Zf-to-X',1,'H2'),('Zf-to-X',2,'Y-average'),
       ('Ze-to-Rf',),('Ze-to-Zf',),('Zf-to-Re',),('Zf-to-Ze',))


def sha(p):return sha256(Path(p).read_bytes()).hexdigest()


def serial(x):
    if isinstance(x,Q):return str(x)
    if isinstance(x,dict):return {str(k):serial(v)for k,v in x.items()}
    if isinstance(x,(list,tuple)):return [serial(v)for v in x]
    return x


def save(p,x):p.write_text(json.dumps(serial(x),ensure_ascii=False,indent=2)+'\n')


class Point:
    def __init__(self,path):
        self.path=path
        self.raw=json.loads(path.read_bytes())
        self.cols=self.raw['columns'][:4849]
        self.mass=[Q(c['weight'])for c in self.cols]
        assert min(self.mass)>=0
        self.hist={j:c for j,c in enumerate(self.cols)if c['kind']=='hist'}
        self.own=defaultdict(dict);self.family=defaultdict(list)
        h=None
        for j,c in enumerate(self.cols):
            if c['kind']=='hist':h=j
            elif c['kind']=='joint-reply':
                f,d,wi,wj=c['group'];g=f,d,tuple(wi),tuple(wj)
                self.own[h].setdefault(g,{'ids':{},'rho':{}})
                self.own[h][g]['ids'][tuple(c['state'])]=j
                self.own[h][g]['rho'][tuple(c['state'])]=self.mass[j]
            elif c['kind']=='actual-B-family-state' and c['source']==4:
                hi=c['hist_column'];a=tuple(map(int,self.hist[hi]['actual_bits']))
                seq=a[:3]+(a[5],)+tuple(c['hidden'])
                assert len(seq)==6 and c['ell']in(0,6)
                self.family[hi].append({'column':j,'mass':self.mass[j],'denom':sum(seq[:-1])+1,
                                       'last':seq[-1],'members':tuple(c['hidden'])+(Q(c['ell'],6),)})
        for h in self.hist:
            for entry in self.own[h].values():
                assert set(entry['rho'])==set(STATES[1:])
                entry['rho'][0,0]=self.mass[h]-sum(entry['rho'].values(),Q())
                entry['rho']=tuple(entry['rho'][s]for s in STATES)
                assert min(entry['rho'])>=0
            assert sum((s['mass']for s in self.family[h]),Q())==self.mass[h]
        self.blocks=[]
        for h,hist in self.hist.items():
            words=tuple(w for w,n in zip(product((0,1),repeat=3),hist['hist'])for _ in range(n))
            assert len(words)==6
            counts=Counter((words[i],words[j],words[k])for i,j,k in permutations(range(6),3))
            assert sum(counts.values())==120
            for triple,count in sorted(counts.items()):
                wi,wj,wk=triple
                ge=(0,0,wi,wj);gf=(1,0,wi,wk)
                self.blocks.append({'index':len(self.blocks),'hist_column':h,'words':triple,'multiplicity':count,
                                    'omega':Q(count,120),'P':sum(map(int,hist['actual_bits'][:4])),
                                    'e_group':ge,'f_group':gf,'e':self.own[h][ge],'f':self.own[h][gf],
                                    'states':self.family[h]})
        U=sum((s['mass']*Q(s['last'],s['denom'])for ss in self.family.values()for s in ss),Q())
        ue=sum((b['omega']*m*Q(z,b['P']+r+1)for b in self.blocks for (r,z),m in zip(STATES,b['e']['rho'])),Q())
        uf=sum((b['omega']*m*Q(z,b['P']+r+1)for b in self.blocks for (r,z),m in zip(STATES,b['f']['rho'])),Q())
        self.budgets=tuple(U if sp[0].startswith('F-to')else ue if sp[0].startswith('Ze-')else uf for sp in SPECS)

    @staticmethod
    def costs(block,ei,fi,state):
        re,ze=STATES[ei];rf,zf=STATES[fi]
        P=block['P'];w=block['omega'];d=state['denom']
        ans=[w*Q(re,d),w*Q(ze,d),w*Q(rf,d),w*Q(zf,d)]
        ans.extend(w*m/(P+re+1)for m in state['members'])
        ans.extend(w*m/(P+rf+1)for m in state['members'])
        ans.extend((w*Q(rf,P+re+1),w*Q(zf,P+re+1),w*Q(re,P+rf+1),w*Q(ze,P+rf+1)))
        return tuple(ans)

    def evaluate(self,flows):
        costs=[Q()]*len(SPECS);checks=0
        for block,flow in zip(self.blocks,flows):
            ss={s['column']:s for s in block['states']}
            rm=[Q()]*4;cm=[Q()]*4;tm={j:Q()for j in ss};seen=set()
            for ei,fi,j,m in flow:
                assert m>0 and(ei,fi,j)not in seen
                seen.add((ei,fi,j));rm[ei]+=m;cm[fi]+=m;tm[j]+=m
                for k,c in enumerate(self.costs(block,ei,fi,ss[j])):costs[k]+=m*c
            assert tuple(rm)==block['e']['rho'] and tuple(cm)==block['f']['rho']
            assert tm=={j:s['mass']for j,s in ss.items()}
            checks+=8+len(ss)
        qs=[{'query':sp,'budget':b,'cost':c,'slack':b-c}for sp,b,c in zip(SPECS,self.budgets,costs)]
        return {'queries':qs,'query_count':len(qs),'minimum_slack':min(q['slack']for q in qs),
                'all_marginal_checks':checks,'positive_flow_entries':sum(map(len,flows))}


def discover(point):
    import numpy as np
    from scipy.optimize import linprog
    from scipy.sparse import coo_matrix
    variables=[];by_block=defaultdict(list)
    for b in point.blocks:
        for ei,em in enumerate(b['e']['rho']):
            if not em:continue
            for fi,fm in enumerate(b['f']['rho']):
                if not fm:continue
                for s in b['states']:
                    if not s['mass']:continue
                    by_block[b['index']].append(len(variables))
                    variables.append((b['index'],ei,fi,s['column']))
    n=len(variables);er,ec,ev,eb,eq_labels=[],[],[],[],[];ur,uc,uv=[],[],[]
    state_by_col={s['column']:s for ss in point.family.values()for s in ss}
    for b in point.blocks:
        if b['index']not in by_block:continue
        em=[i for i,m in enumerate(b['e']['rho'])if m];fm=[i for i,m in enumerate(b['f']['rho'])if m]
        sm=[s['column']for s in b['states']if s['mass']]
        rows=[('e',i,b['e']['rho'][i])for i in em]+[('f',i,b['f']['rho'][i])for i in fm[:-1]]+[
            ('s',j,state_by_col[j]['mass'])for j in sm[:-1]]
        for typ,val,mass in rows:
            row=len(eb);eb.append(float(mass));eq_labels.append((b['index'],typ,val))
            coord={'e':1,'f':2,'s':3}[typ]
            for v in by_block[b['index']]:
                if variables[v][coord]==val:er.append(row);ec.append(v);ev.append(1.)
    for vi,(bi,ei,fi,j)in enumerate(variables):
        for k,c in enumerate(point.costs(point.blocks[bi],ei,fi,state_by_col[j])):
            if c:ur.append(k);uc.append(vi);uv.append(float(c))
    for k in range(len(SPECS)):ur.append(k);uc.append(n);uv.append(1.)
    ae=coo_matrix((ev,(er,ec)),shape=(len(eb),n+1)).tocsc()
    au=coo_matrix((uv,(ur,uc)),shape=(len(SPECS),n+1)).tocsc()
    obj=np.zeros(n+1);obj[-1]=-1.
    result=linprog(obj,A_eq=ae,b_eq=eb,A_ub=au,b_ub=[float(b)for b in point.budgets],
                   bounds=[(0,None)]*n+[(None,None)],method='highs',
                   options={'primal_feasibility_tolerance':1e-9,'dual_feasibility_tolerance':1e-9})
    report={'status':int(result.status),'message':result.message,'positive_transport_variables':n,
            'equalities':len(eb),'full_blocks':len(point.blocks),'full_finite_cells':sum(16*len(b['states'])for b in point.blocks),
            'variables_in_order':variables,'equality_rows_in_order':eq_labels}
    if not result.success:return report,None
    report.update({'floating_maximum_common_slack':float(result.x[-1]),'floating_IC_weights':(-result.ineqlin.marginals).tolist(),
                   'floating_flow':result.x[:n].tolist(),'floating_equality_potentials':result.eqlin.marginals.tolist()})
    if result.x[-1]<-1e-8:return report,None
    if result.x[-1]<=1e-9:
        # A zero optimum can be an exact face forced by an old terminal IC.
        # Recover the observed support with rational sparse elimination.
        flow,recovery=recover_boundary(point,variables,result.x[:n])
        report['exact_boundary_recovery']=recovery
        return report,flow
    flows=[]
    vmap={v:i for i,v in enumerate(variables)}
    for b in point.blocks:
        erem=list(b['e']['rho']);frem=list(b['f']['rho']);srem={s['column']:s['mass']for s in b['states']if s['mass']}
        entries=defaultdict(Q)
        for ei,em in enumerate(b['e']['rho']):
            if not em:continue
            for fi,fm in enumerate(b['f']['rho']):
                if not fm:continue
                for j in srem:
                    target=Q(str(max(0.,result.x[vmap[b['index'],ei,fi,j]]))).limit_denominator(10**12)
                    mass=min(target,erem[ei],frem[fi],srem[j])
                    if mass:entries[ei,fi,j]+=mass;erem[ei]-=mass;frem[fi]-=mass;srem[j]-=mass
        for ei in range(4):
            for fi in range(4):
                for j in srem:
                    mass=min(erem[ei],frem[fi],srem[j])
                    if mass:entries[ei,fi,j]+=mass;erem[ei]-=mass;frem[fi]-=mass;srem[j]-=mass
        assert not any(erem)and not any(frem)and not any(srem.values())
        flows.append([(ei,fi,j,mass)for(ei,fi,j),mass in sorted(entries.items())if mass])
    return report,flows


def recover_boundary(point,variables,numeric):
    support=[i for i,v in enumerate(numeric)if v>1e-10]
    local={v:i for i,v in enumerate(support)}
    per_block=defaultdict(list)
    for vi in support:per_block[variables[vi][0]].append(vi)
    states={s['column']:s for ss in point.family.values()for s in ss}
    equations=[]
    for b in point.blocks:
        for typ,marginals in (('e',dict(enumerate(b['e']['rho']))),('f',dict(enumerate(b['f']['rho']))),
                              ('s',{s['column']:s['mass']for s in b['states']})):
            coord={'e':1,'f':2,'s':3}[typ]
            for val,mass in marginals.items():
                row={local[vi]:Q(1)for vi in per_block[b['index']]if variables[vi][coord]==val}
                if row or mass:equations.append((row,mass))
    numeric_cost=[0.]*len(SPECS)
    exact_costs={}
    for vi in support:
        bi,ei,fi,j=variables[vi]
        exact_costs[vi]=point.costs(point.blocks[bi],ei,fi,states[j])
        for k,c in enumerate(exact_costs[vi]):numeric_cost[k]+=float(c)*numeric[vi]
    active=[]
    for k,bu in enumerate(point.budgets):
        if abs(float(bu)-numeric_cost[k])<1e-8:
            active.append(k)
            equations.append(({local[vi]:exact_costs[vi][k]for vi in support if exact_costs[vi][k]},bu))
    pivots={}
    for initial,rhs in equations:
        row=dict(initial)
        while row:
            lead=min(row)
            if lead not in pivots:
                factor=row[lead]
                pivots[lead]=({j:c/factor for j,c in row.items()},rhs/factor)
                break
            old,old_rhs=pivots[lead]
            factor=row[lead];rhs-=factor*old_rhs
            for j,c in old.items():
                value=row.get(j,Q())-factor*c
                if value:row[j]=value
                elif j in row:del row[j]
        else:
            if rhs:
                return None,{'support':len(support),'rank':len(pivots),'active_queries':active,
                             'failure':'observed numerical support is inconsistent with exact active equations'}
    answer=[Q(str(numeric[vi])).limit_denominator(10**12)for vi in support]
    for lead,(row,rhs)in sorted(pivots.items(),reverse=True):
        answer[lead]=rhs-sum((c*answer[j]for j,c in row.items()if j!=lead),Q())
    if min(answer,default=Q())<0:
        return None,{'support':len(support),'rank':len(pivots),'active_queries':active,
                     'failure':'exact observed-support recovery has a negative flow','minimum':min(answer)}
    flows=[[]for _ in point.blocks]
    for vi,mass in zip(support,answer):
        if mass:
            bi,ei,fi,j=variables[vi];flows[bi].append((ei,fi,j,mass))
    audit=point.evaluate(flows)
    if audit['minimum_slack']<0:
        return None,{'support':len(support),'rank':len(pivots),'active_queries':active,
                     'failure':'exact observed-support recovery violates an IC','minimum_slack':audit['minimum_slack']}
    return flows,{'support':len(support),'rank':len(pivots),'active_queries':active,
                  'exact_feasible':True,'minimum_slack':audit['minimum_slack']}


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--point',type=Path,default=DEFAULT_POINT)
    ap.add_argument('--out-dir',type=Path,default=HERE)
    ap.add_argument('--prefix',default='cycle_pair_19578')
    ap.add_argument('--sizes-only',action='store_true')
    args=ap.parse_args();args.out_dir.mkdir(parents=True,exist_ok=True)
    point=Point(args.point)
    if args.sizes_only:
        print({'blocks':len(point.blocks),'full_cells':sum(16*len(b['states'])for b in point.blocks),
               'positive_cells':sum(sum(m>0 for m in b['e']['rho'])*sum(m>0 for m in b['f']['rho'])*sum(s['mass']>0 for s in b['states'])for b in point.blocks)})
        return
    discovery,flows=discover(point)
    report={'scope':'general cyclic two-old-node/B4 marginal relaxation; different old-word-triple groups may use different joint tables; not a 66-node common completion or SPE',
            'input_point':str(args.point),'input_sha256':sha(args.point),'input_rows':point.raw['verified_rows'],'input_W':point.raw['W'],
            'source_sha256':sha(Path(__file__)),'node_roles':{'e':[0,'i','j'],'f':[1,'i','k'],'i_j_k':'pairwise distinct'},
            'specs':SPECS,'discovery':discovery}
    print({k:v for k,v in discovery.items()if not k.startswith('floating_')or k=='floating_maximum_common_slack'if k not in('variables_in_order','equality_rows_in_order')},flush=True)
    if flows is not None:
        report.update(point.evaluate(flows));assert report['minimum_slack']>=0
        report['exact_feasible']=True
        report['blocks']=[{'hist_column':b['hist_column'],'old_words':b['words'],'multiplicity':b['multiplicity'],
                           'e_group':b['e_group'],'f_group':b['f_group'],
                           'positive_flow':[{'e_state':STATES[ei],'f_state':STATES[fi],'family_state_column':j,'mass':mass}for ei,fi,j,mass in flow]}
                          for b,flow in zip(point.blocks,flows)]
        print({'exact_feasible':True,'minimum_slack':float(report['minimum_slack']),'positive_flow_entries':report['positive_flow_entries']},flush=True)
    else:report['exact_feasible']=False
    save(args.out_dir/(args.prefix+'.json'),report)


if __name__=='__main__':main()
