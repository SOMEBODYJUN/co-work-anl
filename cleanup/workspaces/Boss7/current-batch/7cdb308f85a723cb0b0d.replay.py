import json,itertools
from fractions import Fraction
src=json.load(open('cleanup/workspaces/Boss7/current-batch/7cdb308f85a723cb0b0d.source.json'))
w=src['weights']; p=src['p']; m=src['m']; path=tuple(src['path']); actions={(tuple(a['history'])):a['action'] for a in src['strategy']['actions']}
def payoff(history, selected):
    counts=[history.count(a) for a in range(p)]
    s=Fraction(0)
    for mask,c in enumerate(w,1):
        if mask>>selected & 1:
            den=sum(counts[a] for a in range(p) if mask>>a & 1)
            s += Fraction(c,den)
    return s
def welfare(history):
    return sum(c for mask,c in enumerate(w,1) if any(mask>>a & 1 for a in history))
def check_strategy():
    min_slack=None; bad=[]; rows=0; strict=0; ties=0
    for d in range(m):
      for h in itertools.product(range(p), repeat=d):
        act=actions[h]
        # Build prescribed continuation from h by taking action at each prefix.
        def terminal(hh):
          hh=tuple(hh)
          while len(hh)<m:
            hh += (actions[hh],)
          return hh
        actual_path=terminal(h)
        actual=payoff(actual_path,act)
        for b in range(p):
          branch=terminal(h+(b,))
          dev=payoff(branch,b)
          slack=actual-dev; rows += 1
          if b==act: ties += 1
          elif slack>0: strict += 1
          if min_slack is None or slack<min_slack: min_slack=slack
          if slack<0: bad.append({'history':h,'action':act,'deviation':b,'slack':str(slack),'actual':str(actual),'deviation_payoff':str(dev)})
    return {'decision_rows_including_self':rows,'strict_nonself':strict,'self_rows':ties,'min_slack':str(min_slack),'bad':bad}
summary=check_strategy()
# Enumerate all unordered multisets of length m for OPT.
triples=list(itertools.combinations_with_replacement(range(p),m))
values=[welfare(t) for t in triples]; opt=max(values); opts=[t for t,v in zip(triples,values) if v==opt]
actual=tuple(path); root=path[0]
obj2=opt-welfare(actual)-2*payoff(actual,root); obj3=opt-welfare(actual)-3*payoff(actual,root)
out={'source_id':src.get('id'),'p':p,'m':m,'weights_sum':sum(w),'actual_path':actual,'actual_welfare':welfare(actual),'actual_utilities':[str(payoff(actual,a)) for a in actual],'optimum':opt,'optimal_portfolios':opts,'strategy_check':summary,'fixed_bridge_objectives':{'mult2':str(obj2),'mult3':str(obj3)},'source_report':{k:src[k] for k in ('objective','portfolio','utilities','welfare','optimum') if k in src}}
json.dump(out,open('cleanup/workspaces/Boss7/current-batch/7cdb308f85a723cb0b0d.replay.json','w'),ensure_ascii=False,indent=2); print(json.dumps(out,ensure_ascii=False,indent=2))
