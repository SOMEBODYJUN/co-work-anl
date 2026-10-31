"""Sample full SPE cones using non-minimal credible off-path continuations.

The canonical outcome sets include all pure full-history SPE terminal counts;
its default certificate chooses mover-payoff minima off path. Here every child
SPE outcome with mover payoff <= the specified actual payoff can be selected.
Floating LP only proposes points. Stored integer endpoints and optional exact
optimal duals are independently verified with Fraction on the full history tree.
"""
from __future__ import annotations
import argparse
from fractions import Fraction
from itertools import combinations
import hashlib
import json
from pathlib import Path
import random
import subprocess
import sys
import time

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT));sys.path.insert(0,str(Path(__file__).resolve().parent))
from customer_attraction import ExactSPESolver,Instance,StrategyCertificate,verify_certificate
from customer_attraction_strategy_lp import (StrategyCone,instance_from_clones,
    integer_clones,independently_verify,coverage_row,dot,serializable)


def increment(counts,a):return tuple(x+(i==a) for i,x in enumerate(counts))


def credible_cone(solver,target,rng,mode):
    """A complete strategy on distinct ordered histories, without minimizer restriction."""
    p,m=solver.instance.topic_count,solver.instance.players
    if target not in solver.outcomes():raise ValueError('target is not a child-SPE root outcome')
    actions={};statistics={'non_minimal_off_path_nodes':0,'off_path_nodes':0}
    def expand(h,k,desired):
        if len(h)==m:
            if k!=desired:raise AssertionError('terminal target')
            return
        floor=solver.threshold(k)
        options=[a for a in range(p) if desired in solver.outcomes(increment(k,a))
                 and solver._utility(desired,a)>=floor]
        chosen=rng.choice(options);actions[h]=chosen
        actual=solver._utility(desired,chosen)
        for a in range(p):
            child=increment(k,a)
            if a==chosen:next_target=desired
            else:
                outcomes=solver.outcomes(child)
                menu=[q for q in outcomes if solver._utility(q,a)<=actual]
                if not menu:raise AssertionError('credible menu empty')
                if mode=='max_credible_payoff':
                    value=max(solver._utility(q,a) for q in menu)
                    menu=[q for q in menu if solver._utility(q,a)==value]
                elif mode=='max_credible_welfare':
                    value=max(solver.instance.welfare(q) for q in menu)
                    menu=[q for q in menu if solver.instance.welfare(q)==value]
                elif mode=='min_credible_welfare':
                    value=min(solver.instance.welfare(q) for q in menu)
                    menu=[q for q in menu if solver.instance.welfare(q)==value]
                elif mode!='uniform_credible':raise ValueError(mode)
                next_target=rng.choice(sorted(menu));statistics['off_path_nodes']+=1
                statistics['non_minimal_off_path_nodes']+=int(solver._utility(next_target,a)>
                    min(solver._utility(q,a) for q in outcomes))
            expand(h+(a,),child,next_target)
    expand((),(0,)*p,target)
    cert=StrategyCertificate(actions,target)
    verify_certificate(solver.instance,cert).assert_valid()
    return StrategyCone(p,m,actions),statistics


def exact_export(cone,result):
    clones=integer_clones(result['values'])
    if not independently_verify(cone,clones):raise AssertionError('independent complete-history check')
    candidate=instance_from_clones(cone.topics,cone.players,clones)
    verify_certificate(candidate,StrategyCertificate(cone.actions,cone.root)).assert_valid()
    optimum=candidate.optimal_welfare();welfare=candidate.welfare(cone.root)
    return {'portfolio':result['support'],'integer_clones':clones,
            'objective_value':result['value'],'ratio':Fraction(optimum,welfare),
            'optimum':optimum,'welfare':welfare,
            'dual_bound':result['dual_bound'] if result['dual_optimal'] else None,
            'dual_support':result['dual_support'] if result['dual_optimal'] else ()}


def verify(path):
    """Replay complete trees, rational LP certificates, and original source menus."""
    report=json.loads(path.read_text());checked=duals=sources=0
    for batch in report['batches']:
        p,m=batch['topics'],batch['players']
        for record in batch['cone_proofs']:
            actions={tuple(a['history']):a['action'] for a in record['strategy']['actions']}
            if len(actions)!=len(record['strategy']['actions']):raise AssertionError('duplicate history')
            cone=StrategyCone(p,m,actions)
            if tuple(record['strategy']['terminal_counts'])!=cone.root:raise AssertionError('declared root terminal')
            if 'root_counts' in record and tuple(record['root_counts'])!=cone.root:raise AssertionError('root counts')
            for key,field in (('strategy_sha256','strategy'),('source_integer_clones_sha256','source_integer_clones'),
                              ('portfolio_proofs_sha256','portfolio_proofs')):
                if key in record:
                    digest=hashlib.sha256(json.dumps(record[field],sort_keys=True,separators=(',',':')).encode()).hexdigest()
                    if digest!=record[key]:raise AssertionError('record hash '+field)
            if 'source_integer_clones' in record:
                source=instance_from_clones(p,m,record['source_integer_clones'])
                verify_certificate(source,StrategyCertificate(actions,cone.root)).assert_valid()
                solver=ExactSPESolver(source);nonminimal=offpath=0
                for h,a in actions.items():
                    k=source.counts(h)
                    for b in range(p):
                        if b==a:continue
                        minimum=min(solver._utility(q,b) for q in solver.outcomes(increment(k,b)))
                        branch=solver._utility(cone.terminals[h+(b,)],b)
                        nonminimal+=int(branch>minimum);offpath+=1
                expected={'non_minimal_off_path_nodes':nonminimal,'off_path_nodes':offpath}
                if expected!=record['statistics']:raise AssertionError('credible continuation statistics')
                for example in record.get('source_non_minimal_examples',[]):
                    h=tuple(example['history']);b=example['alternative'];a=actions[h]
                    child=increment(source.counts(h),b)
                    minimum=min(solver._utility(q,b) for q in solver.outcomes(child))
                    branch=solver._utility(cone.terminals[h+(b,)],b)
                    actual=solver._utility(cone.terminals[h],a)
                    if not minimum<branch<=actual:raise AssertionError('non-minimal example')
                    if (str(minimum),str(branch),str(actual))!=(example['minimum_child_spe_payoff'],
                        example['specified_branch_payoff'],example['actual_node_payoff']):raise AssertionError('example payoff')
                sources+=1
            for proof in record['portfolio_proofs']:
                clones=tuple(proof['integer_clones'])
                if not independently_verify(cone,clones):raise AssertionError('non-SPE stored primal')
                candidate=instance_from_clones(p,m,clones)
                verify_certificate(candidate,StrategyCertificate(actions,cone.root)).assert_valid()
                w=candidate.welfare(cone.root);opt=candidate.optimal_welfare()
                if (w,opt)!=(proof['welfare'],proof['optimum']):raise AssertionError('coverage')
                if Fraction(opt,w)!=Fraction(proof['ratio']):raise AssertionError('ratio')
                objective=coverage_row(p,proof['portfolio']);value=dot(objective,clones)/w
                if value!=Fraction(proof['objective_value']):raise AssertionError('objective')
                checked+=1
                if proof['dual_bound'] is None:continue
                beta=Fraction(proof['dual_bound']);mu=[Fraction(0)]*len(cone.rows)
                for idx,x in proof['dual_support']:
                    if idx not in range(len(mu)) or mu[idx]:raise AssertionError('invalid dual index')
                    mu[idx]=Fraction(x)
                if any(x<0 for x in mu):raise AssertionError('negative dual')
                for j,(w,v) in enumerate(zip(cone.welfare,objective)):
                    if beta*w-sum(x*row[j] for x,row in zip(mu,cone.rows))<v:raise AssertionError('dual residual')
                if beta!=value:raise AssertionError('not optimal dual')
                duals+=1
    print(json.dumps({'verified_full_history_integer_primals':checked,
                     'verified_exact_optimal_duals':duals,'verified_original_credible_sources':sources}))


def builtin_sources():
    """Two asymmetric exact source seeds, matching the selected replayable evidence."""
    seeds=[('reply_cycle', {2:1,4:1,8:1,9:1,16:1,17:2,26:1,28:1},(0,0,0,2,3)),
           ('overlap_cycle', {1:10,2:4,4:8,6:2,8:16,12:1,16:32,17:1,24:2},(0,0,1,1,3))]
    return [(label,instance_from_clones(5,5,tuple(weights.get(mask,0) for mask in range(1,32))),target)
            for label,weights,target in seeds]


def clones_of(instance):
    out=[0]*((1<<instance.topic_count)-1)
    for customer in instance.customers:
        mask=sum(1<<a for a in customer.topics)
        if mask:out[mask-1]+=customer.multiplicity
    return tuple(out)


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--instance',type=Path,help='canonical Instance JSON; defaults to two selected five-provider sources')
    ap.add_argument('--target',help='comma-separated terminal topic counts; defaults to up to four worst outcomes')
    ap.add_argument('--variants',type=int,default=2)
    ap.add_argument('--cones',type=int,default=16)
    ap.add_argument('--seed',type=int,default=61260910)
    ap.add_argument('--output',type=Path)
    ap.add_argument('--verify',type=Path)
    args=ap.parse_args()
    if args.cones<1 or args.variants<1:raise ValueError('positive cones and variants required')
    if args.verify:verify(args.verify);return
    if args.output and args.output.exists():raise FileExistsError(args.output)
    if args.target and not args.instance:raise ValueError('--target requires --instance')
    if args.instance:
        instance=Instance.from_dict(json.loads(args.instance.read_text()))
        if instance.players<1:raise ValueError('positive provider count required')
        solver=ExactSPESolver(instance)
        targets=[tuple(map(int,args.target.split(',')))] if args.target else sorted(solver.worst_outcomes())[:4]
        sources=[('supplied_instance',instance,target) for target in targets]
    else:sources=builtin_sources()
    rng=random.Random(args.seed);started=time.monotonic()
    report={'scope':'sampled complete SPE cones with non-minimal credible child continuations',
            'universal_bound_proved':False,'batches':[],'seed':args.seed,
            'base_git_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
            'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    batch=None;seen=set();processed=0
    for label,instance,target in sources:
        p,m=instance.topic_count,instance.players
        if batch is None:
            batch={'players':m,'topics':p,'cone_proofs':[]};report['batches'].append(batch)
        elif (p,m)!=(batch['topics'],batch['players']):raise ValueError('mixed batch dimensions')
        solver=ExactSPESolver(instance)
        for mode in ('max_credible_payoff','max_credible_welfare','min_credible_welfare','uniform_credible'):
            for variant in range(args.variants):
                cone,stats=credible_cone(solver,target,rng,mode)
                key=tuple(sorted(cone.actions.items()))
                if key in seen:continue
                seen.add(key);processed+=1
                record={'source_family':label,'mode':mode,'statistics':stats,
                        'root_counts':cone.root,'constraint_rows':len(cone.rows),
                        'source_integer_clones':clones_of(instance),
                        'strategy':StrategyCertificate(cone.actions,cone.root).to_dict(),'portfolio_proofs':[]}
                for portfolio in combinations(range(p),min(p,m)):
                    result=cone.optimize(portfolio)
                    if result['certified']:record['portfolio_proofs'].append(exact_export(cone,result))
                batch['cone_proofs'].append(record)
                print(json.dumps(serializable({'cone':processed,'source':label,'mode':mode,
                    'non_minimal_off_path_nodes':stats['non_minimal_off_path_nodes'],
                    'exact_portfolio_ratios':[proof['ratio'] for proof in record['portfolio_proofs']]})),flush=True)
                if processed>=args.cones:break
            if processed>=args.cones:break
        if processed>=args.cones:break
    report['elapsed_seconds']=time.monotonic()-started
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(json.dumps(serializable(report),indent=2)+'\n')

if __name__=='__main__':main()
