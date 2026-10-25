"""Independent finite full-policy oracle for the query envelope recurrence."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib,json,sys,platform,subprocess
from query_envelope import QueryEnvelope
from customer_attraction import Instance, CustomerType, verify_certificate


def actual_and_score(instance, actions, weights):
    """Direct unit-customer calculation, not the outcome recursion or model payoffs."""
    p,m=instance.topic_count,instance.players
    units=[c.topics for c in instance.customers for _ in range(c.multiplicity)]
    def finish(h):
        h=tuple(h)
        while len(h)<m:h=h+(actions[h],)
        return h
    def pay(leaf,i):
        return sum((F(1,sum(a in tastes for a in leaf))
                    for tastes in units if leaf[i] in tastes),F(0))
    leaf=finish(());counts=tuple(leaf.count(a)for a in range(p));w=sum(any(a in tastes for a in leaf)for tastes in units)
    rows=[sum((weights[a]*pay(finish(leaf[:i]+(a,)),i)for a in range(p)),F(0))for i in range(m)]
    root_gain=max(pay(finish((a,)),0)for a in range(p))-pay(leaf,0)
    return leaf,counts,w,rows,max(F(0),root_gain),finish,pay


def brute(instance,weights):
    p,m=instance.topic_count,instance.players
    histories=[h for k in range(m)for h in product(range(p),repeat=k)]
    answer={};root_plan_best=None;spe_count=0;plan_count=0
    optimum=max(sum(any(a in c.topics for a in leaf)*c.multiplicity
                    for c in instance.customers)
                for leaf in product(range(p),repeat=m))
    for choices in product(range(p),repeat=len(histories)):
        actions=dict(zip(histories,choices))
        leaf,counts,w,rows,regret,finish,pay=actual_and_score(instance,actions,weights)
        valid=True
        for h in histories[1:]:
            u=pay(finish(h),len(h))
            if any(pay(finish(h+(a,)),len(h))>u for a in range(p)):
                valid=False;break
        if not valid:continue
        plan_count+=1
        gap=optimum-2*w-3*regret
        root_plan_best=gap if root_plan_best is None else max(root_plan_best,gap)
        if regret:continue
        spe_count+=1
        candidate=(sum(rows,F(0)),min(rows))
        if counts not in answer:answer[counts]=candidate
        else:answer[counts]=tuple(min(a,b)for a,b in zip(answer[counts],candidate))
    return answer,root_plan_best,{'full_policies':p**len(histories),'credible_child_plans':plan_count,'full_SPE':spe_count}


def main():
    checks=[]
    cases=[
        (2,1,[(1,1),(2,2)],(1,2)),
        (2,2,[(1,1),(2,1),(3,1)],(2,1)),
        (2,3,[(1,1),(2,1),(3,1)],(1,2)),
        (2,3,[],(2,0)),
        (2,3,[(1,2)],(0,3)),
        (2,3,[(1,1),(2,2)],(F(1,2),F(3,2))),
        (3,2,[(1,1),(2,1),(4,1),(3,1),(6,2)],(1,2,0)),
        (3,2,[(7,1)],(0,0,0)),
    ]
    for p,m,types,weights in cases:
        inst=Instance(tuple(map(str,range(p))),tuple(CustomerType(frozenset(a for a in range(p)if mask>>a&1),n)for mask,n in types),m)
        calc=QueryEnvelope(inst,weights);actual=calc.values();expected,root_expected,stats=brute(inst,tuple(map(F,weights)))
        assert actual==expected,(p,m,actual,expected)
        assert calc.root_repair_bad_gap()[0]==root_expected
        for terminal,(score,_)in actual.items():
            cert=calc.sum_certificate(terminal);verify_certificate(inst,cert).assert_valid()
            leaf,counts,w,rows,regret,_,_=actual_and_score(inst,cert.actions,tuple(map(F,weights)))
            assert counts==terminal and sum(rows,F(0))==score and regret==0
        checks.append({'topics':p,'players':m,'types':types,'query_weights':list(map(str,weights)),**stats,'conditional_terminal_outcomes':len(actual),'root_repair_max_bad_gap':str(root_expected)})
    # Invalid domain and boundary weights must fail, rather than silently cast.
    for players,weights in [(0,(1,1)),(1,(-1,1)),(1,(1,))]:
        inst=Instance(('a','b'),(),players)
        try:QueryEnvelope(inst,weights)
        except ValueError:pass
        else:raise AssertionError('invalid domain accepted')
    result={'status':'passed','method':'All full ordered-history policies enumerated; direct expanded-unit payoffs. Independent of outcome-set recurrence. Reconstructed certificates separately checked.','cases':checks,'domain_failures_checked':3,'limits':'Finite implementation checks; the all-input recurrence relies on its mathematical proof. No general query-payment inequality, half bound, external review, or novelty certification.'}
    repo=Path(__file__).resolve().parents[5]
    result['python_version']=platform.python_version()
    result['base_commit']=subprocess.check_output(['git','rev-parse','HEAD'],cwd=repo,text=True).strip()
    result['source_sha256']={str(p.relative_to(repo)):hashlib.sha256(p.read_bytes()).hexdigest()
                            for p in [Path(__file__).resolve(),Path(__file__).with_name('query_envelope.py').resolve(),
                                      repo/'customer_attraction/exact.py',repo/'customer_attraction/model.py',repo/'customer_attraction/certificate.py']}
    target=Path(__file__).with_name('checks.json')
    target.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'status':result['status'],'cases':len(checks),'full_policy_assignments':sum(c['full_policies']for c in checks),'conditional_outcomes':sum(c['conditional_terminal_outcomes']for c in checks)},ensure_ascii=False))

if __name__=='__main__':main()
