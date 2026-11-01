"""Independent unit-customer Fraction verification. No original import/BI/LP/RNG."""
from pathlib import Path
from fractions import Fraction as F
from functools import lru_cache
import datetime,gzip,hashlib,itertools,json,math,platform,sys,time
ROOT=Path(__file__).resolve().parent
OUT=ROOT/'exact'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    assert not OUT.exists(),'one definition-level event only'
    OUT.mkdir();start=time.perf_counter();when=datetime.datetime.now(datetime.timezone.utc).isoformat()
    capture=ROOT/'replay/saved-point-capture.json';cases=json.loads(capture.read_text())
    summaries=[];ledgers=[]
    for rec in cases:
        path=ROOT/'original'/rec['source'];d=json.loads(path.read_text());q,r=d['q'],d['r'];prefix=d['prefix']
        w={int(k):v for k,v in d['weights'].items()}
        assert all(type(k)==int and 0<k<(1<<q) and type(v)==int and v>0 for k,v in w.items())
        customers=[tuple(a for a in range(q) if mask>>a&1)for mask,count in w.items()for _ in range(count)]
        oldload=[sum(prefix[a]for a in interest)for interest in customers]
        a=d['witness'][0];assert d['witness'][1]==a
        t=sum((F(1,b+r)for interest,b in zip(customers,oldload)if a in interest),F())
        # Pure query a guarantees t against every legal r-1-slot opponent.
        # The same bound works for each dynamic player: at most r remaining covers per customer.
        opponent=[0]*q;opponent[a]=r-1
        dual=[sum((F(1,1+b+sum(opponent[j]for j in interest))for interest,b in zip(customers,oldload)if j0 in interest),F())for j0 in range(q)]
        assert dual[a]==t and max(dual)==t
        strategy={tuple(h):action for h,action in rec['strategy']}
        expected_decisions=sum(q**k for k in range(r));assert len(strategy)==expected_decisions
        checks=[];terminals=set();level_nodes=[0]*(r+1)
        @lru_cache(None)
        def utility(action,c):
            return sum((F(1,b+sum(c[j]for j in interest))for interest,b in zip(customers,oldload)if action in interest),F())
        def walk(h,c):
            level_nodes[len(h)]+=1
            if len(h)==r:
                terminals.add(c);return c
            chosen=strategy[h];assert 0<=chosen<q
            children=[]
            for action in range(q):
                after=tuple(c[j]+int(j==action)for j in range(q))
                children.append(walk(h+(action,),after))
            prescribed=children[chosen];own=utility(chosen,prescribed)
            for action,leaf in enumerate(children):
                other=utility(action,leaf);slack=own-other
                checks.append({'history':h,'chosen':chosen,'deviation':action,'prescribed_terminal':prescribed,
                               'deviation_terminal':leaf,'prescribed_payoff':str(own),'deviation_payoff':str(other),'slack':str(slack)})
                assert slack>=0
            return prescribed
        terminal=walk((),(0,)*q)
        h=();actual=[]
        for _ in range(r):
            action=strategy[h];actual.append(action);h+=(action,)
        assert actual==[a]*r and list(terminal)==d['witness'][2]
        pay=[utility(action,terminal)for action in actual]
        assert all(x>=t for x in pay) and pay[0]+pay[1]==F(d['pair'])==2*t
        # Check passive old-cache capture against direct shares; this adds no old calls.
        assert len(rec['terminals'])==math.comb(r+q-1,q-1)==len(terminals)
        exact_table_checks=0
        for c,scaled in zip(rec['terminals'],rec['scaled_topic_payoffs']):
            # The old implementation defines a hypothetical score also for absent topics;
            # its denominator omits the query. Such scores are not player payoffs.
            for action in range(q):
                if c[action]>0:
                    assert F(scaled[action],rec['scale'])==utility(action,tuple(c));exact_table_checks+=1
        assert rec['pair']==d['pair'] and rec['witness']==d['witness']
        zero=sum(F(x['slack'])==0 for x in checks)
        summary={'source':rec['source'],'input_sha256':sha(path),'q':q,'r':r,'background_providers':sum(prefix),
            'total_providers':sum(prefix)+r,'positive_types':len(w),'unit_customers':len(customers),'prefix':prefix,
            'actual_actions':actual,'terminal_counts':terminal,'actual_payoffs':[str(x)for x in pay],
            'exact_static_value':str(t),'exact_minimum_first_pair':str(2*t),'exact_ratio':'1',
            'pure_query':a,'pure_opponent_counts':opponent,'all_query_values_against_pure_opponent':[str(x)for x in dual],
            'static_pure_dual_slacks':[str(t-x)for x in dual],
            'pure_primal_global_argument':'Every interested customer has at most r-1 competing covers, giving denominator <= oldload+r; all r-1 competitors choose the query to attain equality.',
            'dynamic_minimum_argument':'Every remaining player can choose this pure query and guarantee the same t despite all observed continuations; full verified policy attains 2t.',
            'ordered_decision_histories':len(strategy),'ordered_leaves':q**r,'ordered_tree_nodes':sum(level_nodes),'nodes_by_depth':level_nodes,
            'all_action_comparisons':len(checks),'nonself_comparisons':len(checks)-len(strategy),'zero_slack':zero,'positive_slack':len(checks)-zero,
            'minimum_slack':str(min(F(x['slack'])for x in checks)),
            'terminal_count_vectors':len(terminals),'original_present_topic_payoff_checks':exact_table_checks,
            'saved_decimal_v_minus_exact':str(F(str(d['v']))-t),'saved_binary_v_minus_exact':str(F(d['v'])-t),
            'new_decimal_v_minus_exact':str(F(str(rec['v']))-t),'new_binary_v_minus_exact':str(F(rec['v'])-t),
            'saved_ratio':d['ratio'],'new_ratio':rec['ratio'],'saved_query_equals_new':d['p']==rec['p'],
            'scope':'three fixed exact integer instances; no universal background pair theorem; no original random trajectory reconstruction'}
        summaries.append(summary);ledgers.append({'source':rec['source'],'all_ordered_history_checks':checks})
    report={'status':'PASS','implementation':'independent unit-customer shares, pure primal-dual saddle proof and complete ordered-history policy audit',
            'counts':{'original_imports':0,'original_helpers':0,'BI':0,'LP':0,'RNG':0,'fixed_inputs':3,
                      'unit_customers':sum(x['unit_customers']for x in summaries),
                      'all_action_comparisons':sum(x['all_action_comparisons']for x in summaries),
                      'ordered_decision_histories':sum(x['ordered_decision_histories']for x in summaries),
                      'static_opponent_rows':3,'static_query_entries':sum(x['q']for x in summaries)},'cases':summaries}
    (OUT/'exact-audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    (OUT/'full-history-ledger.json.gz').write_bytes(gzip.compress((json.dumps(ledgers,separators=(',',':'))+'\n').encode(),mtime=0))
    event={'started_at_utc':when,'finished_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'elapsed_seconds':time.perf_counter()-start,
           'python':sys.version,'platform':platform.platform(),'exit_code':0,'assertions_enabled':__debug__,
           'inputs':[{'path':str(p),'bytes':p.stat().st_size,'sha256':sha(p)}for p in [Path(__file__),capture]+sorted((ROOT/'original').glob('*.json'))],
           'outputs':[{'path':p.name,'bytes':p.stat().st_size,'sha256':sha(p)}for p in OUT.iterdir()if p.is_file()]}
    (OUT/'execution.json').write_text(json.dumps(event,indent=2)+'\n')
    print(json.dumps({'status':'PASS','seconds':time.perf_counter()-start,'counts':report['counts']}))
if __name__=='__main__':main()
