"""Definition-level exact audit, using only the Python standard library.

Reads the prior compact full-history strategy; expands all 36 unit customers,
checks every automaton edge and SPE comparison, and independently reconstructs
the root member kernel, its UNIQUE stationary distribution, and the weak-cap
violation. Does not import any repository solver or any exploratory LP script.
"""
from pathlib import Path
from fractions import Fraction as F
from collections import deque
import gzip,json,math

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[4]
SOURCE=ROOT/'research/workspaces/customer-attraction/R-c50fecc37aa44fb4a69a2122bb70e5fe/security/refined_tax_k10_packet.json.gz'

def unique_solution(rows,rhs,unknowns):
    a=[list(map(F,r))+[F(b)]for r,b in zip(rows,rhs)]
    pivots=[];pos=0
    for col in range(unknowns):
        pivot=next((i for i in range(pos,len(a))if a[i][col]),None)
        if pivot is None:continue
        a[pos],a[pivot]=a[pivot],a[pos]
        scale=a[pos][col];a[pos]=[x/scale for x in a[pos]]
        for i in range(len(a)):
            if i!=pos and a[i][col]:
                scale=a[i][col];a[i]=[x-scale*y for x,y in zip(a[i],a[pos])]
        pivots.append(col);pos+=1
    assert all(any(r[:unknowns])or not r[-1]for r in a),'inconsistent system'
    assert len(pivots)==unknowns,('nonunique',pivots)
    solution=[F(0)]*unknowns
    for i,c in enumerate(pivots):solution[c]=a[i][-1]
    return solution,len(pivots)

def main():
    packet=json.load(gzip.open(SOURCE,'rt'))
    inst=packet['instance'];n=inst['players'];k=len(inst['topics']);nodes=packet['nodes'];root=packet['root']
    customers=[]
    for item in inst['customers']:
        for _ in range(item['multiplicity']):customers.append(frozenset(item['topics']))
    lcm=math.lcm(*range(1,n+1))
    counts=[tuple(node['counts'])for node in nodes]
    assert counts[root]==(0,)*k
    seen={root};queue=deque([root]);edges=0
    while queue:
        i=queue.popleft();node=nodes[i];depth=sum(counts[i])
        if node.get('terminal'):
            assert depth==n;continue
        assert depth<n and len(node['children'])==k and 0<=node['action']<k
        for a,ch in enumerate(node['children']):
            expected=tuple(x+int(a==b)for b,x in enumerate(counts[i]))
            assert counts[ch]==expected
            edges+=1
            if ch not in seen:seen.add(ch);queue.append(ch)
    assert len(seen)==len(nodes)
    outcome={}
    for i in sorted(range(len(nodes)),key=lambda i:-sum(counts[i])):
        node=nodes[i]
        outcome[i]=counts[i]if node.get('terminal')else outcome[node['children'][node['action']]]
    def payoff_units(a,terminal):
        return sum(lcm//sum(terminal[t]for t in customer)for customer in customers if a in customer)
    comparisons=0;min_difference=None
    for i,node in enumerate(nodes):
        if node.get('terminal'):continue
        actual=payoff_units(node['action'],outcome[i])
        for a,ch in enumerate(node['children']):
            diff=actual-payoff_units(a,outcome[ch]);assert diff>=0
            comparisons+=1
            min_difference=diff if min_difference is None else min(min_difference,diff)
    actual=outcome[root]
    W=sum(any(actual[a]>0 for a in customer)for customer in customers)
    tails=[]
    for a,ch in enumerate(nodes[root]['children']):
        tail=tuple(x-int(a==b)for b,x in enumerate(outcome[ch]))
        assert min(tail)>=0 and sum(tail)==n-1
        tails.append(tail)
    kernel=[[F(x,n-1)for x in tail]for tail in tails]
    eq=[[kernel[a][b]-int(a==b)for a in range(k)]for b in range(k)]
    pi,rank=unique_solution(eq+[[1]*k],[0]*k+[1],k)
    assert min(pi)>=0 and sum(pi)==1
    assert all(sum(pi[a]*kernel[a][b]for a in range(k))==pi[b]for b in range(k))
    zero_columns=[b for b in range(k)if all(not kernel[a][b]for a in range(k))]
    assert all(pi[b]==0 for b in zero_columns)
    def entrant(a,tail):
        return sum((F(1,1+sum(tail[t]for t in customer))for customer in customers if a in customer),F(0))
    matrix=[[entrant(a,tail)for tail in tails]for a in range(k)]
    values=[sum(pi[b]*matrix[a][b]for b in range(k))for a in range(k)]
    cap=max(values);query=values.index(cap);threshold=F(2*W,2*n-1)
    assert cap>threshold
    # Explicit alternate root-menu mixture: this saves even the strong cap.
    alternate=[F(1,6),F(1,3),F(0),F(0),F(1,3),F(1,6)]
    alt_values=[sum(alternate[b]*matrix[a][b]for b in range(k))for a in range(k)]
    assert max(alt_values)<F(W,n)
    menu_query=[F(0),F(5,18),F(7,18),F(1,6),F(1,6),F(0)]
    menu_lower=[sum(menu_query[a]*matrix[a][b]for a in range(k))for b in range(k)]
    assert all(x==F(29,12)for x in menu_lower)
    assert max(alt_values)==F(29,12)
    # Static unrestricted background: P^9,A,B,T. This does not inspect query.
    static=(1,1,1,0,0,9)
    assert sum(static)==n-1
    static_values=[entrant(a,static)for a in range(k)]
    assert max(static_values)==F(5,2)<F(W,n)
    result={'scope':'Only the prescribed root response-member stationary kernel fails the WEAK cap W/(n-1/2); unrestricted security and arbitrary menu mixtures are not refuted.',
      'source':str(SOURCE.relative_to(ROOT)),
      'unit_customers':len(customers),'players':n,'topics':inst['topics'],
      'automaton_nodes':len(nodes),'edges':edges,'complete_SPE_comparisons':comparisons,
      'nonself_SPE_comparisons':comparisons*(k-1)//k,
      'minimum_SPE_difference':str(F(min_difference,lcm)),
      'actual_counts':actual,'W':W,'root_response_tails':tails,
      'stationary_equation_rank_including_normalization':rank,'zero_columns':zero_columns,
      'stationary_pi':[str(x)for x in pi],
      'query_by_root_tail_matrix':[[str(x)for x in row]for row in matrix],
      'stationary_query_values':[str(x)for x in values],
      'cap_query':inst['topics'][query],'cap':str(cap),'weak_threshold':str(threshold),'weak_gap':str(cap-threshold),
      'alternate_root_menu_probabilities':[str(x)for x in alternate],
      'alternate_root_menu_query_values':[str(x)for x in alt_values],
      'alternate_root_menu_cap':str(max(alt_values)),'strong_threshold':str(F(W,n)),
      'root_menu_optimal_query':[str(x)for x in menu_query],
      'root_menu_query_values_by_background':[str(x)for x in menu_lower],
      'root_menu_minimax_value':'29/12',
      'unrestricted_static_background':static,'unrestricted_static_query_values':[str(x)for x in static_values],
      'true_security_upper_bound':str(max(static_values))}
    output=HERE/'root_stationary_weak_audit.json'
    output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
