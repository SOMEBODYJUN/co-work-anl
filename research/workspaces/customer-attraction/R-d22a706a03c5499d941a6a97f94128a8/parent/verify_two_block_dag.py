"""Independent complete-strategy DAG and exact matrix certificate audit.
Does not import the discovery solver, its verifier, or any repository game package.
A node routes every action to a child, so finite unfolding covers every ordered history.
"""
from fractions import Fraction as F
from functools import lru_cache
from pathlib import Path
import json

BASE=Path(__file__).resolve().parents[1]
SOURCE=BASE/'counterexample/pure_menu_two_block_dag.json'
LOCAL=[((0,),2),((1,3),4),((0,2),6),((2,3),3),((0,1,2,3),1)]
UNITS=[frozenset(a+4*b for a in interest)
       for b in range(2) for interest,n in LOCAL for _ in range(n)]
TOPICS=[frozenset(i for i,t in enumerate(UNITS) if a in t) for a in range(8)]

@lru_cache(None)
def scaled_payoffs(q):
    load=[sum(q[a] for a in interest) for interest in UNITS]
    return tuple(sum(840//load[x] for x in TOPICS[a]) if q[a]>0 else 0 for a in range(8))

def inserted(a,q):
    return sum((F(1,1+sum(q[b] for b in UNITS[x])) for x in TOPICS[a]),F(0))

def main():
    cert=json.loads(SOURCE.read_text())
    assert cert['schema']=='CA_COMPLETE_SPE_DAG_v1'
    nodes=cert['nodes']; root=cert['root']
    assert nodes[root]['counts']==[0]*8 and nodes[root]['action']==3
    reached=set(); stack=[root]; comparisons=0; min_gap=None; leaves=0
    while stack:
        j=stack.pop()
        if j in reached:continue
        reached.add(j)
        n=nodes[j]; c=tuple(n['counts']); q=tuple(n['target']); a=n['action']; ch=n['children']
        assert len(c)==len(q)==8 and all(type(v) is int and v>=0 for v in c+q)
        assert sum(q)==8 and all(x<=y for x,y in zip(c,q))
        depth=sum(c)
        if depth==8:
            assert a is None and ch==[] and c==q
            leaves+=1;continue
        assert depth<8 and type(a) is int and 0<=a<8 and len(ch)==8
        assert tuple(nodes[ch[a]]['target'])==q
        follow=scaled_payoffs(q)[a]
        for b,child in enumerate(ch):
            assert type(child) is int and 0<=child<len(nodes)
            cn=nodes[child]; expected=list(c);expected[b]+=1
            assert cn['counts']==expected
            cq=tuple(cn['target'])
            assert sum(cq)==8 and cq[b]>0
            gap=follow-scaled_payoffs(cq)[b]
            assert gap>=0,(j,b,gap)
            comparisons+=1;min_gap=gap if min_gap is None else min(min_gap,gap)
            stack.append(child)
    assert len(reached)==len(nodes)==13872 and leaves==6435 and comparisons==59496
    cols=[tuple(nodes[ch]['target']) for ch in nodes[root]['children']]
    assert cols==[tuple(q) for q in cert['root_columns']]
    self_u=[F(scaled_payoffs(q)[a],840) for a,q in enumerate(cols)]
    assert self_u==[F(13,4),F(9,4),F(13,4),F(13,4)]*2
    u=F(13,4)
    K=[[inserted(a,q) for q in cols] for a in range(8)]
    pure=[max(K[a][b] for a in range(8)) for b in range(8)]
    assert pure==[F(37,10)]*8 and min(pure)>u
    for b in range(8):assert K[7 if b<4 else 3][b]==F(37,10)
    Q=[F(0),F(0),F(1,14),F(3,7)]*2
    p=[F(0),F(0),F(2,7),F(3,14)]*2
    assert sum(p)==sum(Q)==1
    row=[sum((K[a][b]*Q[b] for b in range(8)),F(0)) for a in range(8)]
    col=[sum((p[a]*K[a][b] for a in range(8)),F(0)) for b in range(8)]
    V=F(851,280)
    assert max(row)==min(col)==V<u
    path=[]; j=root
    while nodes[j]['action'] is not None:
        a=nodes[j]['action'];path.append(a);j=nodes[j]['children'][a]
    q=tuple(nodes[j]['target'])
    W=sum(any(q[a]>0 for a in interest) for interest in UNITS)
    assert W==len(UNITS)==32
    result={'status':'PASS','scope':'specified finite complete strategy DAG only',
      'unit_customers':32,'topics':8,'players':8,'DAG_nodes':len(nodes),'terminal_nodes':leaves,
      'decision_comparisons_including_self':comparisons,'minimum_scaled_gap':min_gap,
      'ordered_histories_represented':sum(8**i for i in range(8)),
      'actual_path':path,'actual_payoffs':[str(F(scaled_payoffs(q)[a],840)) for a in path],
      'W':W,'OPT':32,'root_self_payoffs':list(map(str,self_u)),
      'pure_menu_caps':list(map(str,pure)),'root_u':str(u),'pure_cap_minus_u':str(min(pure)-u),
      'K':[[str(v) for v in r] for r in K],'primal_Q':list(map(str,Q)),
      'dual_p':list(map(str,p)),'KQ':list(map(str,row)),'pK':list(map(str,col)),
      'exact_mixed_menu_value':str(V),'root_u_minus_mixed_value':str(u-V)}
    out=Path(__file__).with_name('two_block_dag_independent_audit.json')
    out.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ('status','unit_customers','DAG_nodes','decision_comparisons_including_self','ordered_histories_represented','W','OPT','root_u','pure_cap_minus_u','exact_mixed_menu_value','root_u_minus_mixed_value')}))

if __name__=='__main__':main()
