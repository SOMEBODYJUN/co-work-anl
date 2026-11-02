"""Rebuild only two frozen full-O SAFE owner witnesses from fixed source data.

Standard-library Fraction implementation of the stated row kernel. Does not
execute/import original test_role_cap, run any owner LP, repeat complete SPE IC
verification, or run the already certified 26-client quadratic example.
"""
from pathlib import Path
from functools import lru_cache
from itertools import product
from fractions import Fraction as F
import argparse, datetime, hashlib, json, platform, subprocess, sys, time

INPUT_ROOT='archives/customer-attraction/tools/evidence/r51-static-opt-matching-primary/runtime'

def fp(p):return {'size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}

def evaluate(repo, base):
    report=json.loads((base/'original/global_credit/role_cap_results.json').read_text())
    selected=('root_tax_failure','coverage_opportunity_failure')
    answers=[]
    for name in selected:
        case=next(c for c in report['cases']if c['name']==name)
        p=repo/INPUT_ROOT/'examples/customer_attraction'/(name+'.json')
        q=repo/INPUT_ROOT/'evidence/certificates/customer_attraction'/(name+'.json')
        instance=json.loads(p.read_text());cert=json.loads(q.read_text());s=cert.get('strategy',cert)
        nodes=s['actions'];policy={tuple(x['history']):x['action']for x in nodes}
        m=instance['players'];catalog=len(instance['topics'])
        assert len(policy)==len(nodes)and set(policy)=={h for depth in range(m)for h in product(range(catalog),repeat=depth)}
        assert all(type(v)is int and 0<=v<catalog for v in policy.values())
        types=[(frozenset(x['topics']),x.get('multiplicity',1))for x in instance['customers']]
        @lru_cache(None)
        def finish(h):
            return h if len(h)==m else finish(h+(policy[h],))
        @lru_cache(None)
        def loads(leaf):return tuple(sum(a in c for a in leaf)for c,n in types)
        @lru_cache(None)
        def payoff(leaf,i):
            return sum((F(n,l)for(c,n),l in zip(types,loads(leaf))if leaf[i]in c),F())
        actual=finish(());u=tuple(payoff(actual,i)for i in range(m))
        assert list(actual)==case['actual']and list(map(str,u))==case['u']
        @lru_cache(None)
        def safe(h):
            i=len(h);action=policy[h];B=finish(h);A=finish(actual[:i]+(action,))
            v=payoff(B,i);assert v>0
            ca,cb=loads(A),loads(B);diag=F();edges=[]
            for x,(members,n) in enumerate(types):
                if action not in members:continue
                ja={j for j in range(m)if j!=i and A[j]in members}
                jb={j for j in range(m)if j!=i and B[j]in members}
                unit=F(n,ca[x]*cb[x]);diag+=(1+len(ja&jb))*unit
                edges.extend((j,x,unit)for j in ja-jb)
            assert diag+sum((v for j,x,v in edges),F())==v
            result=[F()for _ in range(m)];result[i]+=diag/v
            for j,x,amount in edges:
                if j<i:result[j]+=amount/v
                else:
                    child=safe(A[:j])
                    for role in range(m):result[role]+=amount/v*child[role]
            assert min(result)>=0 and sum(result)==1
            return tuple(result)
        @lru_cache(None)
        def unit_source(i,action,x):
            leaf=finish(actual[:i]+(action,));members,n=types[x];load=loads(leaf)[x]
            assert action in members and load>0
            result=[F()for _ in range(m)]
            for j in range(m):
                if leaf[j]not in members:continue
                if j<=i:result[j]+=F(1,load)
                else:
                    child=safe(leaf[:j])
                    for role in range(m):result[role]+=child[role]/load
            assert min(result)>=0 and sum(result)==1
            return tuple(result)
        witness=case['modes']['safe']['witness'];T=tuple(witness['tuple']);owners={int(x):i for x,i in witness['owners_by_type'].items()}
        covered=[x for x,(members,n)in enumerate(types)if any(a in members for a in T)]
        assert set(owners)==set(covered)
        assert all(T[owners[x]]in types[x][0]for x in covered)
        # The specified comparison covers every unit client, proving its true
        # optimality by a universe upper bound, with no tuple enumeration.
        assert len(covered)==len(types)
        total_clients=sum(n for c,n in types);assert total_clients==case['OPT']
        masses=[F()for _ in range(m)];columns=[]
        for x in covered:
            owner=owners[x];vec=unit_source(owner,T[owner],x);n=types[x][1]
            for role in range(m):masses[role]+=n*vec[role]
            columns.append({'type_index':x,'multiplicity':n,'eligible_owner':owner,'query_topic':T[owner],
                            'query_terminal':list(finish(actual[:owner]+(T[owner],))),
                            'unit_role_vector':list(map(str,vec))})
        target=witness['target_role_zero_based'];cap=2*u[target]
        assert list(map(str,masses))==witness['all_role_mass']
        assert masses[target]==F(witness['mass'])and cap==F(witness['cap2'])
        assert masses[target]/cap==F(witness['ratio'])>1
        assert sum(masses)==total_clients
        answers.append({'name':name,'comparison_tuple':list(T),'actual':list(actual),'u':list(map(str,u)),
                        'OPT_proved_by_all_clients_covered':total_clients,'all_role_mass':list(map(str,masses)),
                        'target':target,'target_mass':str(masses[target]),'cap':str(cap),
                        'strict_excess':str(masses[target]-cap),'ratio':str(masses[target]/cap),
                        'all_frozen_witness_fields_match':True,'source_columns':columns,
                        'only_reached_safe_contexts':safe.cache_info().currsize,
                        'complete_key_inventory':len(policy),
                        'instance':{'path':str(p.relative_to(repo)),**fp(p)},
                        'policy':{'path':str(q.relative_to(repo)),**fp(q)}})
    result={'scope':'two exact SAFE fixed-owner violations only; no all-tuple/owner LP replay or new game/SPE verification',
            'selected_cases':answers,'new_standard_library_definition_checker':True,'python':platform.python_version(),
            'original_role_cap_main_or_imports':0,'original_role_cap_run_calls':0,'owner_LP_calls':0,
            'all_complete_SPE_IC_rechecks':0,'quadratic_fixed_certificate_runs':0,
            'existing_source_SPE_validity_reused_by_frozen_bytes':True}
    (base/'replay/two-safe-witnesses.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'cases':[{k:v for k,v in a.items()if k in ('name','target_mass','cap','strict_excess','ratio','only_reached_safe_contexts')}for a in answers],
                      'original_main':0,'LP':0,'old_SPE_IC_rechecks':0,'quadratic_runs':0},ensure_ascii=False,indent=2))

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--repo',required=True,type=Path);ap.add_argument('--worker',action='store_true');a=ap.parse_args()
    base=Path(__file__).resolve().parent;out=base/'replay';out.mkdir(exist_ok=True)
    if a.worker:evaluate(a.repo.resolve(),base);return
    cmd=[sys.executable,'-I',str(Path(__file__).resolve()),'--repo',str(a.repo.resolve()),'--worker']
    t=time.monotonic();started=datetime.datetime.now(datetime.timezone.utc).isoformat();p=subprocess.run(cmd,capture_output=True,text=True)
    stdout=out/'stdout.txt';stderr=out/'stderr.txt';stdout.write_text(p.stdout);stderr.write_text(p.stderr)
    event={'argv':cmd,'start_utc':started,'elapsed_seconds':time.monotonic()-t,'returncode':p.returncode,
           'driver':fp(Path(__file__)),'stdout':fp(stdout),'stderr':fp(stderr)}
    (out/'execution-record.json').write_text(json.dumps(event,ensure_ascii=False,indent=2)+'\n')
    print(p.stdout,end='');print(p.stderr,end='',file=sys.stderr)
    if p.returncode:raise SystemExit(p.returncode)
    print(json.dumps(event,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
