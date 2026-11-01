"""Three saved points: unit-client terminal arithmetic only; no BI or strategy audit."""
from collections import Counter
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def convert(x):
    if isinstance(x, F):
        return str(x)
    if isinstance(x, dict):
        return {str(k):convert(v) for k,v in x.items()}
    if isinstance(x, (list,tuple)):
        return [convert(v) for v in x]
    return x


def audit(k):
    path = HERE/'original'/f'padding_k{k}.json'
    raw = path.read_bytes()
    data = json.loads(raw)
    assert set(data) == {'k','players','instance','path','terminal','welfare','optimum','nodes',
        'decision_nodes','comparisons','minimum_slack','M','G','refined_tax_gap','g','scope'}
    assert data['k']==k and data['players']==data['instance']['players']==k+3
    assert data['instance']['topics']==['A','B','T','D','E','P']
    assert [x['topics'] for x in data['instance']['customers']]==[[0],[1],[2],[2,3],[2,4],[0,3,4],[1,3,4],[5]]
    assert [x['multiplicity'] for x in data['instance']['customers']]==[4,4,2,2,2,6,2,5*k]
    clients = [frozenset(c['topics']) for c in data['instance']['customers'] for _ in range(c['multiplicity'])]
    m = data['players']
    assert len(clients)==5*k+22
    assert data['path']==[5]*k+[0,0,1]
    counts = [data['path'].count(a) for a in range(6)]
    assert counts==data['terminal']==[2,1,0,0,0,k]
    loads = [sum(counts[a] for a in c) for c in clients]
    welfare = sum(t>0 for t in loads)
    occupied_payoffs = [sum((F(1,t) for c,t in zip(clients,loads) if a in c and counts[a]>0),F(0)) for a in range(6)]
    actual = [occupied_payoffs[a] for a in data['path']]
    assert actual==[F(5)]*(k+2)+[F(6)]
    assert sum(actual)==welfare==data['welfare']==5*k+16
    alpha = F(m-1,m)
    g = [sum((F(1)/(1+alpha*t) for c,t in zip(clients,loads) if a in c),F(0)) for a in range(6)]
    G = sum((F(1)/(1+alpha*t) for t in loads if t>0),F(0))
    M = max(g)
    gap = m*M-welfare-G
    assert g==list(map(F,data['g'])) and G==F(data['G']) and M==F(data['M'])==6
    assert gap==F(data['refined_tax_gap'])
    # Finite supports, not equilibrium or LP enumeration. Repetition fills unused player slots.
    supports = []
    for mask in range(64):
        if mask.bit_count()<=m:
            value=sum(any(mask>>a&1 for a in c) for c in clients)
            supports.append([mask,value])
    optimum=max(value for mask,value in supports)
    assert optimum==data['optimum']==len(clients)
    assert sum(bool(c & {0,1,2,5}) for c in clients)==optimum
    competitors=[1,1,1,0,0,k-1]
    assert sum(competitors)==m-1
    queries=[sum((F(1,1+sum(competitors[b] for b in c)) for c in clients if a in c),F(0)) for a in range(6)]
    assert queries==[F(5),F(3),F(3),F(5),F(5),F(5)]
    # min_slack and DAG sizes are retained historical fields, not re-proved by terminal arithmetic.
    assert data['comparisons']==6*data['decision_nodes'] and data['minimum_slack']=='0'
    return dict(k=k,players=m,input=dict(path=str(path.relative_to(HERE)),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest()),
        unit_clients=len(clients),membership_masks=[sum(1<<a for a in c['topics']) for c in data['instance']['customers']],
        actual_counts=counts,actual_path=data['path'],customer_load_histogram=dict(sorted(Counter(loads).items())),
        occupied_topic_payoffs=occupied_payoffs,actual_player_payoffs=actual,welfare=welfare,optimum=optimum,
        welfare_ratio=F(welfare,optimum),half_slack=2*welfare-optimum,
        alpha=alpha,g=g,M=M,G=G,refined_tax_gap=gap,low_player_tax_deficit=M-G/m-5,
        static_competitors=competitors,static_query_payoffs=queries,static_safety_upper_bound=5,
        welfare_minus_players_times_static_upper_bound=welfare-5*m,
        all_support_coverage_rows=supports,coverage_supports_checked=len(supports),
        original_DAG_statistics_retained={name:data[name] for name in ['nodes','decision_nodes','comparisons','minimum_slack']},
        original_DAG_statistics_recomputed=False)


def main():
    points=[audit(k) for k in [1,5,10]]
    result=convert(dict(status='PASS',scope='Independent unit-client terminal, tax, support coverage and one legal static-opponent calculation; not a full-strategy audit',
        original_entries=0,original_helper_calls=0,BI_calls=0,LP_calls=0,full_DAG_IC_checks=0,
        independent_terminal_audit_runs=1,total_unit_clients=sum(x['unit_clients'] for x in points),
        coverage_supports_checked=sum(x['coverage_supports_checked'] for x in points),points=points))
    (HERE/'terminal-audit.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(dict(status='PASS',points=3,unit_clients=result['total_unit_clients'],support_rows=result['coverage_supports_checked'],original_calls=0,BI=0,LP=0,full_DAG_IC=0)))


if __name__=='__main__':
    main()
