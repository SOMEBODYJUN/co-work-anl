"""New bounded Fraction check of displayed certificates, not an original program replay."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json

def H(c):
    return sum((F(1, j) for j in range(1, c+1)), F())

def examine(name, groups, second, third, root_action, expected):
    topics = len(second)
    def finish(h):
        h = list(h)
        if not h:
            h.append(root_action)
        if len(h) == 1:
            h.append(second[h[0]])
        if len(h) == 2:
            h.append(third[h[0]][h[1]])
        return tuple(h)
    def utility(z, i):
        return sum((F(n, sum(a in M for a in z)) for M, n in groups if z[i] in M), F())
    def phi(z):
        return sum((n*H(sum(a in M for a in z)) for M, n in groups), F())
    def welfare(z):
        return sum(n for M, n in groups if any(a in M for a in z))
    tables = []
    for depth in range(3):
        for h in product(range(topics), repeat=depth):
            z = finish(h)
            vals = [utility(finish(h+(a,)), depth) for a in range(topics)]
            assert vals[z[depth]] == max(vals), (name, h, vals)
            tables.append({'h': h, 'chosen': z[depth], 'values': list(map(str, vals))})
    z = finish(())
    C = z[-1]
    promoted = finish((C,))
    gamma = utility(z, 0)-utility(promoted, 0)
    tax = sum((F(n, (int(C in M)+1)*(int(C in M)+2))
               for M, n in groups if promoted[1] in M and promoted[2] not in M), F())
    assert phi(z)-phi(promoted) == tax == 1
    assert [str(phi(z)), str(phi(promoted)), str(gamma)] == expected
    # Actual same-policy replay chain: force original topics after promoted C.
    leaves = [promoted]
    for j in range(1, 3):
        leaves.append(finish((C,)+z[:j]))
    chain = []
    for j in range(2):
        i = j+1
        before, after = leaves[j:j+2]
        gap = utility(before, i)-utility(after, i)
        delete_gap = phi(after[:i]+after[i+1:])-phi(before[:i]+before[i+1:])
        assert gap >= 0 and phi(after)-phi(before) == delete_gap-gap
        chain.append({'before': before, 'after': after, 'IC_slack': str(gap), 'deleted_phi_change': str(delete_gap)})
    assert sum((F(x['deleted_phi_change'])-F(x['IC_slack']) for x in chain), F()) == phi(z)-phi(promoted)
    # All true root/T/Q forks; prices use separate actual root/middle wallets.
    K = max(sum(n for M, n in groups if a in M) for a in range(topics))
    U, V0 = utility(z, 0), utility(z, 1)
    fork_rows = []
    for T, Q in product(range(topics), repeat=2):
        first = finish((T,))
        B, C0 = first[-2:]
        second_leaf = finish((T, C0))
        V = second_leaf[-1]
        c1 = U-utility(first, 0)
        c2 = utility(first, 1)-utility(second_leaf, 1)
        query_original_Q = sum((F(n, int(T in M)+int(B in M)+1) for M, n in groups if Q in M), F())
        query_promoted_Q = sum((F(n, int(T in M)+int(C0 in M)+1) for M, n in groups if Q in M), F())
        query_original_V = sum((F(n, int(T in M)+int(B in M)+1) for M, n in groups if V in M), F())
        c3 = utility(first, 2)-query_original_Q
        c4 = utility(second_leaf, 2)-query_promoted_Q
        c5 = utility(first, 2)-query_original_V
        assert min(c1, c2, c3, c4, c5) >= 0
        pi = {a: sum((F(n, 3) for M, n in groups if a in M), F()) for a in range(topics)}
        rho = {a: sum((F(n, int(z[0] in M)+2) for M, n in groups if a in M), F()) for a in range(topics)}
        assert max(pi.values()) <= U and max(rho.values()) <= V0
        primitive = (c1+F(1,50)*c2+F(49,800)*c3+F(1,50)*c4+F(3,160)*c5
            +F(3,50)*(U-pi[C0])+F(1,800)*(U-pi[V])
            +F(24,125)*(V0-rho[B])+F(24,125)*(V0-rho[C0])+F(1,250)*(V0-rho[V])
            +F(1,500)*(K-sum(n for M,n in groups if B in M)))
        raw_sum = F()
        min_sum = F()
        for M,n in groups:
            t,q,b,c,v = (int(a in M) for a in (T,Q,B,C0,V))
            p,s = 0,0
            px,rx = F(1,3),F(1,int(z[0] in M)+2)
            raw_sum += n*cost(p,t,q,s,b,c,v,px,rx)
            min_sum += n*min(cost(p,t,q,0,bb,cc,vv,px,rx) for bb,cc,vv in product(range(2),repeat=3))
        lhs = U+F(49,800)*U+F(97,250)*V0+F(1,500)*K
        assert lhs-raw_sum == primitive >= 0 and lhs >= min_sum
        fork_rows.append({'T':T,'Q':Q,'five_IC':list(map(str,[c1,c2,c3,c4,c5])),
                          'sum_nonnegative_slacks':str(primitive),'lhs_minus_sum_min':str(lhs-min_sum)})
    return {'name':name,'nodes':len(tables),'action_values_including_stay':len(tables)*topics,
        'all_node_tables':tables,'actual_path':z,'actual_utility':list(map(str,[utility(z,i) for i in range(3)])),
        'promoted_path':promoted,'promoted_utility':list(map(str,[utility(promoted,i) for i in range(3)])),
        'phi':[str(phi(z)),str(phi(promoted))],'welfare':[welfare(z),welfare(promoted)],
        'opt':max(welfare(zz) for zz in product(range(topics),repeat=3)),
        'source_IC_slack':str(gamma),'new_branch_tax':str(tax),'replay_chain':chain,'fork_rows':fork_rows}

def share(n,d):
    return F(n,d) if n else F()

def cost(p,t,q,s,b,c,v,pi,rho):
    e=p+t+s;z1=e+b+c;z2=e+c+v
    return (share(t,z1)+F(1,50)*(share(c,z2)-share(b,z1))
        +F(49,800)*(F(q,e+b+1)-share(c,z1))
        +F(1,50)*(F(q,e+c+1)-share(v,z2))
        +F(3,160)*(F(v,e+b+1)-share(c,z1))
        +b*(F(24,125)*rho+F(1,500))+c*(F(3,50)*pi+F(24,125)*rho)
        +v*(F(1,800)*pi+F(1,250)*rho)+F(49,1600)*s)

one = examine('three-topic sharp reset',[(set((0,2)),2),(set((1,)),2),(set((0,1)),3)],
    [1,2,1],[[1,1,1],[0,0,1],[1,0,1]],0,['21/2','19/2','1/2'])
two = examine('four-topic zero selected slacks',[(set((0,)),1),(set((2,)),2),(set((1,2)),2),(set((0,1,3)),2)],
    [1,2,3,1],[[2,2,2,2],[2,2,0,2],[1,0,0,2],[2,2,2,2]],0,['9','8','0'])
assert [x['IC_slack'] for x in two['replay_chain']] == ['0','0']
assert [x['deleted_phi_change'] for x in two['replay_chain']] == ['1','0']
compression = []
for k in range(3,10):
    for p,t,q in product(range(3),range(2),range(2)):
        literal=[cost(p,t,q,sum(bits[:-3]),*bits[-3:],F(1,8),F(1,7)) for bits in product(range(2),repeat=k)]
        compact=[cost(p,t,q,s,b,c,v,F(1,8),F(1,7)) for s in range(k-2) for b,c,v in product(range(2),repeat=3)]
        assert len(compact)==8*(k-2) and min(literal)==min(compact)
    compression.append({'k':k,'literal_memberships':2**k,'compact_candidates':8*(k-2),'p_t_q_cases':12})
report={'status':'PASS','role':'new exact bounded selfcheck; original program entries=0',
    'certificate_checks':[one,two],'compression_checks':compression,
    'zero_example_source_strategy':'author table, not parent independently reconstructed D->A variant',
    'not_executed':['author original scripts','parent independent source','702/3889 point validators','LP/MILP'],
    'general_quantifiers':'analytic proofs, not finite scans'}
Path('report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'status':'PASS','nodes':[one['nodes'],two['nodes']],
    'action_values_including_stay':[one['action_values_including_stay'],two['action_values_including_stay']],
    'true_forks':len(one['fork_rows'])+len(two['fork_rows']),'compression_cases':len(compression)*12}))
