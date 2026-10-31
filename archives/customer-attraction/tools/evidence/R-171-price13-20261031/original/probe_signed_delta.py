"""Definition-level exact true-relay delta audit and finite packet probe.

All outputs here are personal research checkpoints, not a general half proof.
"""
from fractions import Fraction as F
from itertools import product, combinations
from pathlib import Path
import gzip
import hashlib
import json
import shutil

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[5]


def unpack_packet():
    source = ROOT / 'research/workspaces/customer-attraction/R-c50fecc37aa44fb4a69a2122bb70e5fe/security/refined_tax_k10_packet.json.gz'
    snapshot = HERE / 'packet13_source.json.gz'
    if not snapshot.exists():
        shutil.copyfile(source, snapshot)
    assert hashlib.sha256(source.read_bytes()).digest() == hashlib.sha256(snapshot.read_bytes()).digest()
    with gzip.open(snapshot, 'rt') as f:
        data = json.load(f)
    customers = []
    for c in data['instance']['customers']:
        customers += [frozenset(c['topics'])] * c['multiplicity']
    nodes = data['nodes']
    k,m=len(data['instance']['topics']),data['instance']['players']
    assert nodes[data['root']]['counts']==[0]*k
    reached=set();stack=[data['root']]
    while stack:
        j=stack.pop()
        if j in reached:continue
        reached.add(j);node=nodes[j]
        assert len(node['counts'])==k
        assert all(isinstance(v,int) and v>=0 for v in node['counts'])
        if 'action' not in node:
            assert sum(node['counts'])==m
            continue
        assert sum(node['counts'])<m and 0<=node['action']<k
        assert len(node['children'])==k
        for a,child in enumerate(node['children']):
            expected=node['counts'].copy();expected[a]+=1
            assert nodes[child]['counts']==expected
            stack.append(child)
    assert len(reached)==len(nodes)
    targets, lasts = [None] * len(nodes), [None] * len(nodes)
    for j in sorted(range(len(nodes)), key=lambda j: -sum(nodes[j]['counts'])):
        node = nodes[j]
        if 'action' not in node:
            targets[j] = tuple(node['counts'])
        else:
            child = node['children'][node['action']]
            targets[j] = targets[child]
            lasts[j] = node['action'] if 'action' not in nodes[child] else lasts[child]
    def choose(h):
        j = data['root']
        for a in h:
            j = nodes[j]['children'][a]
        return nodes[j]['action']
    return data, customers, nodes, targets, lasts, choose, source


def payoff(customers, a, counts):
    return sum((F(1, sum(counts[b] for b in C)) for C in customers if a in C), F(0))


def menus(customers, m, k, choose):
    def finish(h):
        while len(h) < m:
            h += (choose(h),)
        return h
    path = finish(())
    counts = [path.count(a) for a in range(k)]
    values = [payoff(customers, a, counts) for a in path]
    matrices, rows = [], []
    for i in range(m-1):
        leaves = [finish(path[:i] + (a,)) for a in range(k)]
        replies = [leaf[-1] for leaf in leaves]
        d = counts.copy()
        d[path[i]] -= 1
        d[path[-1]] -= 1
        diagonal = [payoff(customers, a, [leaf.count(b) for b in range(k)]) for a, leaf in enumerate(leaves)]
        matrix = [[sum((F(1, 1 + sum(d[b] for b in C) + (replies[q] in C)) for C in customers if a in C), F(0)) - diagonal[a] for q in range(k)] for a in range(k)]
        matrices.append(matrix)
        rows.append(dict(i=i+1, actual=path[i], last=path[-1], replies=replies, true_diagonal=list(map(str, diagonal)), delta_matrix=[[str(v) for v in row] for row in matrix]))
    total = [[sum((M[a][b] for M in matrices),F(0)) for b in range(k)] for a in range(k)]
    W = sum(values)
    return path, values, matrices, total, rows, W


def qvalue(matrix, p):
    return sum((p[a]*p[b]*matrix[a][b] for a in range(len(p)) for b in range(len(p))), F(0))


def main():
    scalar_checks=0
    for d,a,eta,q,e,u in product(range(6),range(2),[F(0),F(1,2),F(1),F(2)],[F(0),F(1,2),F(1)],[F(0),F(1,4),F(1,2),F(1)],[F(0),F(1,2),F(1),F(2),F(5)]):
        t=min(F(1,d+1),F(1,d+2)+eta/F(d+a+1))
        R=q*min(1,u)-u/F(d+1)-eta*e/F(d+a+1)+u*e/F((d+1)*(d+2))
        bound=max(0,q-t)*min(1,u)-max(0,u-1)/F(d+2)
        assert R<=bound
        scalar_checks+=1
    old_customers = []
    for x,y in product(range(3),range(3,6)):
        old_customers.append(frozenset([x,y]))
    for xx,yy in product(combinations(range(3),2),combinations(range(3,6),2)):
        old_customers += [frozenset(xx+yy)]*3
    def old_choose(h):
        if not h:return 0
        if len(h)==1:return 3 if h[0]<3 else 0
        return min(a for a in (range(3) if h[1]<3 else range(3,6)) if a not in h)
    path,values,Ms,total,rows,W=menus(old_customers,3,6,old_choose)
    assert path==(0,3,4) and values==[10,12,12]
    mu=[F(1,6)]*6
    assert qvalue(Ms[0],mu)==F(7,18)
    assert max(v for row in Ms[0] for v in row)==2
    assert qvalue(Ms[0],[F(0),F(0),F(0),F(0),F(1),F(0)])==2
    old=dict(path=path,payoffs=list(map(str,values)),W=str(W),menus=rows,uniform_delta_root=str(qvalue(Ms[0],mu)),root_delta_max='2',root_max_proof='All delta matrix entries <=2; point mass at topic 4 attains 2.')
    old_checks=0
    for t in range(3):
        for h in product(range(6),repeat=t):
            def finish_old(hh):
                while len(hh)<3:hh+=(old_choose(hh),)
                return hh
            leaf=finish_old(h)
            own=payoff(old_customers,old_choose(h),[leaf.count(a) for a in range(6)])
            for a in range(6):
                alternative=finish_old(h+(a,))
                assert own>=payoff(old_customers,a,[alternative.count(b) for b in range(6)])
                old_checks+=1
    old['SPE_comparisons']=old_checks
    data,customers,nodes,targets,lasts,choose,source=unpack_packet()
    m,k=data['instance']['players'],len(data['instance']['topics'])
    checks=0
    all_comparisons=[]
    for j,node in enumerate(nodes):
        if 'action' not in node:continue
        own=payoff(customers,node['action'],targets[j])
        alternative_payoffs=[]
        for a,child in enumerate(node['children']):
            alt=payoff(customers,a,targets[child])
            assert own >= alt
            alternative_payoffs.append(str(alt))
            checks += 1
        all_comparisons.append(dict(node=j,counts=node['counts'],action=node['action'],true_target=targets[j],own=str(own),alternative_payoffs=alternative_payoffs,margins=[str(own-F(v)) for v in alternative_payoffs]))
    audit=dict(source=str(source.relative_to(ROOT)),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),nodes=len(nodes),comparisons=checks,nonterminal_node_comparisons=all_comparisons)
    with gzip.open(HERE/'packet13_all_nodes_audit.json.gz','wt') as f:
        json.dump(audit,f,separators=(',',':'))
    path,values,Ms,total,rows,W=menus(customers,m,k,choose)
    budget=(W+values[-1])/(2*m)
    result=dict(status='Finite exact audit of fixed complete SPE and rational queries; not a general result',source=str(source.relative_to(ROOT)),nodes=len(nodes),SPE_comparisons=checks,path=path,payoffs=list(map(str,values)),W=str(W),budget=str(budget),menus=rows,total_delta_matrix=[[str(v) for v in row] for row in total])
    for name,p in [('uniform',[F(1,k)]*k),('T',[F(0),F(0),F(1),F(0),F(0),F(0)])]:
        result[name]=dict(delta_by_player=[str(qvalue(M,p)) for M in Ms],total=str(qvalue(total,p)),excess=str(qvalue(total,p)-budget))
    def counts_of(n,k):
        if k==1:
            yield (n,)
        else:
            for a in range(n+1):
                for tail in counts_of(n-a,k-1):
                    yield (a,)+tail
    optimum_queries=[]
    for c in counts_of(m,k):
        coverage=sum(any(c[a] for a in C) for C in customers)
        if coverage==len(customers):
            optimum_queries.append((qvalue(total,[F(v,m) for v in c]),c))
    best,worst=min(optimum_queries),max(optimum_queries)
    result['optimal_empirical_queries']=dict(number=len(optimum_queries),minimum_delta=str(best[0]),minimum_counts=best[1],maximum_delta=str(worst[0]),maximum_counts=worst[1],maximum_excess=str(worst[0]-budget),above_budget=sum(v>budget for v,c in optimum_queries))
    result['nonrepeated_optimal_queries']=[]
    for extras in [(),(3,),(4,),(3,4)]:
        support=(0,1,2,5)+extras
        p=[F(a in support,len(support)) for a in range(k)]
        result['nonrepeated_optimal_queries'].append(dict(support=support,total_delta=str(qvalue(total,p))))
    assert max(v for row in total for v in row)==5
    result['exact_simplex_maximum']='5: every total matrix entry is <=5, and point masses at B or T attain 5'
    p=[F(v,m) for v in worst[1]]
    all_counts=[path.count(a) for a in range(k)]
    credit_current=F(0);credit_last_menu=F(0);overlap_credit=F(0)
    for i,row in enumerate(rows):
        expected_true=sum((p[a]*F(row['true_diagonal'][a]) for a in range(k)),F(0))
        credit_current+=m*(values[i]-expected_true)
        d=all_counts.copy();d[path[i]]-=1;d[path[-1]]-=1
        for C in customers:
            dx=sum(d[b] for b in C);ax=path[i] in C
            t=min(F(1,dx+1),F(1,dx+2)+F(1,2*(dx+1+ax)))
            ux=sum(worst[1][b] for b in C)
            overlap_credit+=(1-t)*(1-min(1,ux))+F(max(0,ux-1),dx+2)
        last_ref=sum((p[a]*sum((F(1,1+sum(d[b] for b in C)+(path[i] in C)) for C in customers if row['replies'][a] in C),F(0)) for a in range(k)),F(0))
        credit_last_menu+=(values[-1]-last_ref)/2
    before_last=all_counts.copy();before_last[path[-1]]-=1
    true_last=[]
    for a in range(k):
        terminal=before_last.copy();terminal[a]+=1
        true_last.append(payoff(customers,a,terminal))
    for C in customers:
        px=sum(before_last[b] for b in C)
        ux=sum(worst[1][b] for b in C)
        overlap_credit+=F(px,px+1)*(1-min(1,ux))+F(max(0,ux-1),px+1)
    credit_last_player=m*(values[-1]-sum((p[a]*true_last[a] for a in range(k)),F(0)))
    credits=credit_current+credit_last_menu+credit_last_player
    result['worst_optimal_query_true_G_credits']=dict(current_credit=str(credit_current),last_menu_credit=str(credit_last_menu),last_player_credit=str(credit_last_player),total_credit=str(credits),adjusted_total_delta=str(worst[0]-credits/m),adjusted_excess=str(worst[0]-credits/m-budget))
    result['worst_optimal_query_true_G_credits'].update(overlap_credit=str(overlap_credit),overlap_adjusted_excess=str(worst[0]-(credits+overlap_credit)/m-budget))
    report=dict(old36=old,packet13=result,overlap_scalar=dict(exact_fraction_checks=scalar_checks,status='Finite boundary audit only; general proof in note'))
    (HERE/'signed_delta_report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:{z:v for z,v in d.items() if z not in ('menus','total_delta_matrix')} for k,d in report.items()},indent=2))


if __name__=='__main__':main()
