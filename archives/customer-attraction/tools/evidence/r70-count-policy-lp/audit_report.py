"""Independent exact saved-policy audit; no original import, optimizer or BI solver."""
from collections import Counter
from fractions import Fraction as F
import gzip, hashlib, json, math, struct
from pathlib import Path

HERE=Path(__file__).resolve().parent
SOURCE=Path('/workspace/scratch/c0ab78c47566/round16-r70-count-policy-result.json')
data=json.loads(SOURCE.read_text())
assert hashlib.sha256(SOURCE.read_bytes()).hexdigest()=='56d49b0c3bb4baa29bf695547d4afb0ac8bfb3dd956c809ed3b6a696ca6bae3a'
capture=json.loads(gzip.decompress((HERE/'capture.json.gz').read_bytes()))
assert list(data)==['seed','trial','gap','omit','actual','weights','action']
assert data['seed']==28491 and data['trial']==5 and data['omit']==2

def compositions(total,slots):
    if slots==1:
        yield (total,)
    else:
        for first in range(total,-1,-1):
            for suffix in compositions(total-first,slots-1):
                yield (first,)+suffix

layers=[list(compositions(d,7)) for d in range(7)]
states=[q for layer in layers for q in layer]
ids={q:i for i,q in enumerate(states)}
termids={q:i for i,q in enumerate(layers[-1])}
assert list(map(len,layers))==[1,7,28,84,210,462,924]
assert len(states)==1716 and len(data['action'])==1716 and len(data['weights'])==127
action=data['action'];assert set(action[:792])=={2,4}
assert Counter(action)==Counter({2:619,4:173,-1:924})
assert action[792:]==[-1]*924
mass=[F(v).limit_denominator(1000000) for v in data['weights']]
scale=math.lcm(*(v.denominator for v in mass))
assert scale==11 and sum(mass)==1
integer={m:int(x*scale) for m,x in enumerate(mass,1) if x}
assert integer=={1:1,2:1,8:1,20:6,32:1,64:1}
assert F(data['gap']).limit_denominator(1000000)==-F(1,11)

def child(q,a):
    return tuple(v+int(j==a) for j,v in enumerate(q))

def finish_table(actions):
    out={q:q for q in layers[-1]}
    for d in range(5,-1,-1):
        for q in layers[d]:out[q]=out[child(q,actions[ids[q]])]
    return out

def payoff(q,a):
    assert q[a]>0
    return sum((F(n,sum(q[j] for j in range(7) if m>>j&1))
                for m,n in integer.items() if m>>a&1),F())

def unit_coefficient(q,a,m):
    assert q[a]>0
    return F(int(m>>a&1),sum(q[j] for j in range(7) if m>>j&1)) if m>>a&1 else F()

out=finish_table(action)
q=(0,)*7;path=[]
while sum(q)<6:
    a=action[ids[q]];path.append(a);q=child(q,a)
assert list(q)==data['actual']==[0,0,4,0,2,0,0]
assert out[(0,)*7]==q
assert action==capture['solve_policy'][5]['action']
# All six captured recursive outcome arrays, from their own different policies.
for rec in capture['solve_policy']:
    assert len(rec['action'])==len(rec['outcome'])==1716
    o=finish_table(rec['action'])
    assert [termids[o[q]] for q in states]==rec['outcome']

state_records=[];slacks=[];weighted_histories=0;weighted_nonself=0
all_rows=[];coefficient_digest=hashlib.sha256();float_digest=hashlib.sha256()
max_float_error=F();row_index=0
for d,layer in enumerate(layers):
    for q in layer:
        sid=ids[q]
        record={'state_id':sid,'past_counts':list(q),'action':action[sid],
                'outcome_counts':list(out[q]),'outcome_terminal_index':termids[out[q]]}
        if d<6:
            multiplicity=math.factorial(d)//math.prod(math.factorial(v) for v in q)
            weighted_histories+=multiplicity;weighted_nonself+=6*multiplicity
            values=[payoff(out[child(q,a)],a) for a in range(7)]
            own=values[action[sid]]
            gains=[own-v for v in values]
            assert min(gains)>=0
            old_private=d-q[2]-q[4]
            assert own==F(6,6-old_private)
            for a in [0,1,3,5,6]:assert values[a]==F(1,q[a]+1)
            assert values[2]==values[4]==own
            slacks+=gains
            record.update({'ordered_history_multiplicity':multiplicity,
                           'all_7_current_player_payoffs':list(map(str,values)),
                           'all_7_IC_slacks':list(map(str,gains))})
            for a in range(7):
                if a==action[sid]:continue
                z=out[child(q,a)];ownz=out[q]
                floats=capture['last_policy_A_ub'][row_index]
                assert len(floats)==127
                for m,observed in enumerate(floats,1):
                    exact=unit_coefficient(z,a,m)-unit_coefficient(ownz,action[sid],m)
                    scaled=exact*60;assert scaled.denominator==1
                    coefficient_digest.update(struct.pack('<h',int(scaled)))
                    float_digest.update(struct.pack('<d',observed))
                    error=abs(F(observed)-exact)
                    max_float_error=max(max_float_error,error)
                    assert error<F(1,10**14)
                all_rows.append({'row':row_index,'state_id':sid,'alternative':a,'exact_integer_point_slack':str(own-values[a])})
                row_index+=1
        state_records.append(record)
assert weighted_histories==19608 and weighted_nonself==117648
assert row_index==4752 and len(slacks)==5544
assert float_digest.hexdigest()==capture['policy_lp'][5]['matrix']['float64_c_sha256']
assert len(capture['linprog'])==42
for pi,rec in enumerate(capture['policy_lp']):
    assert rec['matrix']['shape']==[4752,127]
    actual=layers[-1][rec['actual_terminal_index']]
    for omit in range(7):
        lp=capture['linprog'][7*pi+omit]
        assert lp['success'] and lp['status']==0 and lp['A_ub']==rec['matrix']
        assert lp['A_eq']==[[1.]*127] and lp['b_eq']==[1.]
        expected=[-(1-int(m==1<<omit)-2*int(any(actual[j] and (m>>j&1) for j in range(7)))) for m in range(1,128)]
        assert expected==lp['c']

coverage=lambda counts:sum(n for m,n in integer.items() if any(counts[j] and (m>>j&1) for j in range(7)))
terminal_coverages=[coverage(t) for t in layers[-1]]
assert max(terminal_coverages)==11 and coverage(out[(0,)*7])==6
omit_coverages=[sum(n for m,n in integer.items() if m!=1<<omit) for omit in range(7)]
assert omit_coverages==[10,10,11,10,11,10,10]
assert all(F(v-12,11)<=0 for v in omit_coverages)
report={
 'status':'PASS','kind':'one independent exact saved count-policy and coefficient reconstruction',
 'source_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
 'original_imports':0,'LP_calls':0,'canonical_SPE_solver_calls':0,
 'layer_sizes':list(map(len,layers)),'states':1716,'decision_count_states':792,'terminal_count_states':924,
 'ordered_decision_histories_covered_by_count_lift':19608,
 'nonself_count_IC_rows':4752,'self_inclusive_count_comparisons':5544,
 'nonself_ordered_IC_rows_covered_by_count_lift':117648,
 'action_histogram':{str(k):v for k,v in sorted(Counter(action).items())},
 'weights_zero_based_negative_zero_indices':[j for j,v in enumerate(data['weights']) if not v and v.hex().startswith('-')],
 'exact_recovery_scale':scale,'positive_types':[{'mask':m,'topics':[a for a in range(7) if m>>a&1],'unit_customers':n} for m,n in integer.items()],
 'unit_customers':sum(integer.values()),'actual_ordered_path':path,'actual_counts':data['actual'],
 'actual_payoffs':[str(payoff(out[(0,)*7],a)) for a in path],
 'W':6,'OPT6':11,'half_gap_OPT_minus_2W':-1,'normalized_gap':'-1/11',
 'seven_omit_coverages':omit_coverages,'seven_normalized_objectives_at_saved_point':[str(F(v-12,11)) for v in omit_coverages],
 'minimum_IC_slack':str(min(slacks)),'zero_IC_slacks':sum(v==0 for v in slacks),'strict_IC_slacks':sum(v>0 for v in slacks),
 'captured_policy_outcome_arrays_reconstructed':6,
 'last_policy_matrix_coefficients_checked':4752*127,
 'exact_matrix_times_60_int16_le_sha256':coefficient_digest.hexdigest(),
 'maximum_source_float_coefficient_error':str(max_float_error),
 'new_capture_objective_coefficients_checked':42*127,
 'terminal_coverages_checked':924,
 'policy_definition':'sigma(h) = saved action[state_id(count(h))]; this lift preserves this policy, not every full-history policy',
 'all_1716_states':state_records,'all_4752_nonself_rows':all_rows,
 'limits':['No exact LP optimum or dual certificate asserted.','Six sampled policies do not enumerate count policies or all full-history SPE.','Same-coverage labels 2 and 4 are retained in the saved policy.']}
raw=(json.dumps(report,ensure_ascii=False,separators=(',',':'))+'\n').encode()
with (HERE/'exact-audit.json.gz').open('wb') as f:
    with gzip.GzipFile(fileobj=f,mode='wb',mtime=0) as z:z.write(raw)
summary={k:v for k,v in report.items() if k not in ['all_1716_states','all_4752_nonself_rows']}
summary['detail_uncompressed_bytes']=len(raw);summary['detail_uncompressed_sha256']=hashlib.sha256(raw).hexdigest()
summary['detail_gzip_sha256']=hashlib.sha256((HERE/'exact-audit.json.gz').read_bytes()).hexdigest()
(HERE/'exact-audit-summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(summary,ensure_ascii=False))
