"""Exact finite attacks for laminar maximal-incidence greedy protection.

Direct protection checks independently evaluate individual unit customers.
SPE outcomes use the canonical complete-history continuation solver. Neither
finite component proves the universal theorem. Default output is stdout;
--output refuses to overwrite an existing report.
"""
from fractions import Fraction as F
from itertools import product, combinations, combinations_with_replacement
from pathlib import Path
import argparse
import hashlib
import random,json,sys,time
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from customer_attraction.model import Instance
from customer_attraction.exact import ExactSPESolver

def protection_test(catalog,n):
    covered=set().union(*catalog)
    maxima=[a for a,S in enumerate(catalog) if not any(S<T for T in catalog)]
    violations=[];count=0
    for t in range(n-1):
      for history in product(range(len(catalog)),repeat=t):
        load={x:sum(x in catalog[a] for a in history) for x in covered}
        immediate=[sum((F(1,load[x]+1) for x in S),F()) for S in catalog]
        top=max(immediate)
        for a in maxima:
          if immediate[a]!=top:continue
          for future in product(range(len(catalog)),repeat=n-t-1):
            terminal=history+(a,)+future
            total={x:sum(x in catalog[b] for b in terminal) for x in covered}
            own=sum((F(1,total[x]) for x in catalog[a]),F())
            followers=[sum((F(1,total[x]) for x in catalog[b]),F()) for b in future]
            count+=1
            if own<min(followers):
                violations.append((history,a,future,own,followers))
                return count,violations
    return count,violations

def check_spe(catalog,n):
    maxima = set(S for S in catalog if not any(S < T for T in catalog))
    covered = set().union(*catalog)
    signatures = [frozenset(j for j, S in enumerate(maxima) if x in S)
                  for x in covered]
    assert all(not (I & J) or I <= J or J <= I
               for I in signatures for J in signatures)
    common = set.intersection(*(set(S) for S in maxima))
    core = len(common)
    inst=Instance.from_topic_sets(catalog,n)
    sol=ExactSPESolver(inst)
    opt=inst.optimal_welfare()
    # Exact common last-slot floor, minimized over all legal length-(n-1) counts.
    prefixes=[]
    for chosen in combinations_with_replacement(range(len(catalog)),n-1):
      counts=tuple(chosen.count(a) for a in range(len(catalog)))
      prefixes.append(counts)
    def join(p,a):
      covered=set().union(*catalog)
      load={x:sum(p[b] for b,S in enumerate(catalog) if x in S) for x in covered}
      return sum((F(1,load[x]+1) for x in catalog[a]),F())
    theta=min(max(join(p,a) for a in range(len(catalog))) for p in prefixes)
    assert theta >= F(core,n) + F(opt-core,2*n-1)
    checks=0
    for q in sol.outcomes():
      assert F(opt) <= core + F(2*n-1,n)*(inst.welfare(q)-core)
    # All legal prefix states: if q_a>p_a, a new player really selects label a.
    for depth in range(n):
      for chosen in combinations_with_replacement(range(len(catalog)),depth):
        p=tuple(chosen.count(a) for a in range(len(catalog)))
        for q in sol.outcomes(p):
          for a in range(len(catalog)):
            if q[a]>p[a]:
              assert inst.topic_payoff(a,q)>=theta,(catalog,n,p,q,a,theta)
              checks+=1
    return len(sol.outcomes()),checks,sol.stats.count_states

if __name__=='__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    if args.output is not None and args.output.exists():
        parser.error('refusing to overwrite an existing output report')
    start=time.time();report={'protection_cases':0,'protection_comparisons':0,'spe_cases':0,'spe_outcomes':0,'spe_player_topic_checks':0,'spe_states':0}
    # Nontrivial hierarchy: two maximals share root+branch, third shares root only.
    # Every subset is allowed as a candidate extra catalog action, including omitted cores.
    maxima=[frozenset({0,1,2}),frozenset({0,1,3}),frozenset({0,4})]
    subs=set()
    for S in maxima:
      for k in range(len(S)+1):
        subs.update(frozenset(t) for t in combinations(S,k))
    proper=sorted(subs-set(maxima),key=lambda x:(len(x),sorted(x)))
    catalogs=[tuple(maxima)]
    catalogs += [tuple(maxima+[S]) for S in proper]
    catalogs += [tuple(maxima+[proper[i],proper[j]]) for i in range(len(proper)) for j in range(i+1,len(proper))]
    for cat in catalogs:
      for n in [2,3,4]:
        count,fail=protection_test(cat,n)
        assert not fail,(cat,n,fail)
        report['protection_cases']+=1;report['protection_comparisons']+=count
        out,ch,st=check_spe(cat,n)
        report['spe_cases']+=1;report['spe_outcomes']+=out;report['spe_player_topic_checks']+=ch;report['spe_states']+=st
    # Weight each laminar customer block using distinct unit copies.
    rng=random.Random(88219)
    for trial in range(300):
      m=rng.randrange(3,6);weights=[rng.randrange(0,8) for _ in range(m+3)]
      signatures=[frozenset(range(m)),frozenset(range(2)),frozenset(range(2,m))]+[frozenset({j}) for j in range(m)]
      vals=[]
      for t,(I,w) in enumerate(zip(signatures,weights)):
        vals += [(t,k,I) for k in range(w)]
      maxima=[frozenset((t,k) for t,k,I in vals if j in I) for j in range(m)]
      # Ensure positive singleton blocks, hence all declared maxima are genuine.
      for j in range(m):maxima[j]=maxima[j]|{('private',j)}
      extras=[frozenset(x for x in sorted(maxima[rng.randrange(m)],key=repr) if rng.randrange(2)) for _ in range(rng.randrange(0,3))]
      cat=tuple(maxima+extras);n=rng.randrange(2,7)
      out,ch,st=check_spe(cat,n)
      report['spe_cases']+=1;report['spe_outcomes']+=out;report['spe_player_topic_checks']+=ch;report['spe_states']+=st
      covered=set().union(*cat)
      for it in range(100):
        t=rng.randrange(n-1);h=tuple(rng.randrange(len(cat)) for _ in range(t))
        load={x:sum(x in cat[b] for b in h) for x in covered}
        immediate=[sum((F(1,load[x]+1) for x in S),F()) for S in cat]
        a=rng.choice([b for b in range(m) if immediate[b]==max(immediate)])
        f=tuple(rng.randrange(len(cat)) for _ in range(n-t-1));term=h+(a,)+f
        total={x:sum(x in cat[b] for b in term) for x in covered}
        u=lambda b:sum((F(1,total[x]) for x in cat[b]),F())
        assert u(a)>=min(map(u,f)),(cat,n,h,a,f)
        report['protection_comparisons']+=1
    # Boundary cases: zero customers, empty action, unique maximum, duplicates, n=1.
    for cat in [(frozenset(),),(frozenset(),frozenset()),
                (frozenset(),frozenset({0}),frozenset({0})),
                (frozenset({0,1}),frozenset({0}),frozenset({1})),
                (frozenset({0,1}),frozenset({0,2}),frozenset({0,1}))]:
      for n in range(1,5):
        count,fail=protection_test(cat,n)
        assert not fail
        report['protection_cases']+=1;report['protection_comparisons']+=count
        out,ch,st=check_spe(cat,n)
        report['spe_cases']+=1;report['spe_outcomes']+=out;report['spe_player_topic_checks']+=ch;report['spe_states']+=st
    # Exact failure just outside incidence laminar: crossed shared blocks.
    X=frozenset(('x',i) for i in range(4));Y=frozenset(('y',i) for i in range(4))
    Z=frozenset(('z',i) for i in range(3));V=frozenset(('v',i) for i in range(3))
    cat=(X|Y,X|Z,Y|V)
    assert [len(S) for S in cat]==[8,7,7]
    count,fail=protection_test(cat,3)
    assert fail and fail[0][3]==4 and fail[0][4]==[F(5),F(5)]
    report['crossed_incidence_failure']={'topic_sizes':[8,7,7],'greedy_leader':0,'future':[1,2],'final_payoffs':['4','5','5'],'customers':14}
    report['scope'] = {
        'players': '1 through 6 in the stated finite families',
        'exhaustive_protection_cases': report['protection_cases'],
        'exhaustive_protection_comparisons': report['protection_comparisons']-30000,
        'weighted_seeded_cases': 300,
        'weighted_seed': 88219,
        'random_protection_comparisons': 30000,
        'catalog_family': 'three nested maxima with zero, one, or two internal subsets; weighted two-branch hierarchies; boundary catalogs',
        'spe_quantifier': 'all canonical SPE outcomes at every legal count prefix; complete-history continuation semantics',
        'checks': ['actual-follower greedy protection', 'every remaining new-topic payoff >= global theta_n', 'theta_n >= c/n+(OPT_n-c)/(2n-1)', 'OPT_n <= c+(2-1/n)(W-c)'],
        'not_established_by_test': 'the universal theorem or unrestricted half coverage',
    }
    source_paths = [
        Path(__file__).resolve(),
        ROOT/'research/current/customer_attraction/laminar_incidence_bound.md',
        ROOT/'customer_attraction/exact.py',
        ROOT/'customer_attraction/model.py',
    ]
    report['source_sha256'] = {
        str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in source_paths
    }
    report['elapsed_seconds']=round(time.time()-start,3)
    rendered = json.dumps(report,indent=2)+'\n'
    print(rendered,end='')
    if args.output is not None:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        with args.output.open('x') as stream:
            stream.write(rendered)

