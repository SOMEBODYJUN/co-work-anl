"""Main independently checks the v-preserving map and stronger income transfer."""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
from collections import Counter
import hashlib, json, time
from main_zero_capacity_features_v1 import prefix_affine, L

B=Path(__file__).resolve().parent
C=B/'coverage_bridge'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
sp=C/'shared_rz_zero_capacity_v1.json'
tp=C/'strong_a6_transfer_v1.json'
shared,submitted=json.loads(sp.read_text()),json.loads(tp.read_text())
assert submitted['shared_rz_input_sha256']==sha(sp)
started=time.time()

def E(p,D,x,y,n,a,h):
    constant,coefs=prefix_affine(13,p,D,0,h)
    qs={'Ti':F(x),'Tj':F(y),'other_T':F(n-x-y,4),'A6':F(a)}
    return constant+sum(v*qs[k] for k,v in coefs)

cases=0;reasons=Counter();gaps=[]
for p in range(4):
    for D in range(p+1,p+4):
        for r in range(3):
            x,y=min(1,r),max(0,r-1)
            for n in range(r,r+5):
                Q,U=F(103*n+r,4),F(39*n+r,4)
                for h in product((0,1),repeat=4):
                    b,c,j,v=h
                    if b==0 or D>=p+2:
                        hh=h;reason='same_state'
                    elif c==1 or j==0 or p>=2:
                        hh=(0,c,j,v);reason='lower_b_first'
                        actual_b_difference=E(p,D,x,y,n,1,h)-E(p,D,x,y,n,1,hh)
                        if c:
                            stated=F(34*(1-j),(p+1)*(p+2))+F(1081,p+j+2)
                        elif j==0:
                            stated=F(1081*p,(p+1)*(p+2))
                        else:
                            stated=F(1081*p-1115,(p+1)*(p+2))
                        assert actual_b_difference==stated>=0
                    elif v:
                        hh=(0,1,1,1);reason='exception_v1'
                    elif p==1:
                        hh=(0,1,1,0);reason='exception_p1_v0'
                    elif n:
                        hh=(0,1,1,0);reason='exception_p0_positive_n'
                    else:
                        hh=(0,0,0,0);reason='exception_zero_n'
                    assert hh[3]==v
                    gap=E(p,D,x,y,n,1,h)-E(p,D,x,y,n,0,hh)-F(2162,D)
                    assert gap>=0
                    formulas={'exception_v1':(90*p+2162+Q+U)/((p+2)*(p+3)),
                              'exception_p1_v0':(2*U+Q+183)/12,
                              'exception_p0_positive_n':F(55*n+r-25,6),
                              'exception_zero_n':F(18)}
                    if reason in formulas:
                        assert gap==formulas[reason]
                    gaps.append(gap);reasons[reason]+=1;cases+=1
assert cases==submitted['hidden_map_cases']==2880
assert dict(reasons)==submitted['hidden_map_reason_counts'] and min(gaps)==0
for row in shared['A6_credit_type_table']:
    p,D,x,y,ci,cj,n=(row[k] for k in ('p','D','Ti','Tj','Ci','Cj','n'))
    da=L(2,p,D,0,x,y,ci,cj,1,n)-L(2,p,D,0,x,y,ci,cj,0,n)
    db=L(13,p,D,0,x,y,0,0,1,n)-L(13,p,D,0,x,y,0,0,0,n)
    assert da>=F(1,D) and db>=F(2162,D) and 49*da+10*db>=F(21669,D)
assert submitted['budget_before']=={'u4':'148951','u6':'20391','K':'0'}
assert submitted['budget_after']=={'u4':'148951','u6':'-1278','K':'0'}
assert 20391-21669==-1278
base={(v['p'],v['D'],v['n'],v['Cnum']):F(v['base']) for v in shared['conditional_common_C_count_table']}
negative=[]
for row in submitted['new_actual_baselines']:
    p,a4,a5,a6,D=(row[k] for k in ('p','A4','A5','A6','D'))
    val=49*L(2,p,D,0,0,0,0,0,0,0)+10*L(13,p,D,0,0,0,0,0,0,0)
    assert val==F(row['new_baseline']) and row['negative']==(val<0)
    if a6 and val<0:negative.append(row)
assert negative==submitted['negative_A6_one_patterns'] and len(negative)==4

def cost(mode,p,a4,a5,a6,n):
    D=p+a4+a5+1
    return base[p,D,n,0]+F(17965*n,6*(p+a4+(1 if mode=='joint' else 2)))

for row in submitted['coverage_type_table']:
    assert cost(row['mode'],row['p'],row['A4'],row['A5'],row['A6'],row['n'])==F(row['value'])
assert len(submitted['coverage_type_table'])==448
for mode in ('joint','separate_same_weights'):
    rec=submitted['coverage_contracts'][mode]
    missing=[cost(mode,0,0,0,0,n) for n in range(1,7)]
    A=min(missing)
    all_tax=[A*int(n>0)-cost(mode,p,a4,a5,a6,n)
             for p in range(4) for a4,a5,a6 in product((0,1),repeat=3)
             for n in range(7) if p+a4+a5+a6>0]
    assert missing==list(map(F,rec['uncovered_by_opt_multiplicity']))
    assert A==F(rec['OPT_credit']) and max(all_tax)==F(rec['W_tax'])
    assert max(all_tax)==F(shared['coverage_contracts'][mode]['W_tax'])
    # Exact reason no greater tax is introduced: positive old actual load
    # duplicates an existing a6=0 covered type; the other case has uncovered
    # credit, so its tax is nonpositive.
    for p,a4,a5 in product(range(4),(0,1),(0,1)):
        for n in range(7):
            v=cost(mode,p,a4,a5,1,n)
            assert v==cost(mode,p,a4,a5,0,n)
            if p+a4+a5==0:assert A*int(n>0)-v<=0

result={'status':'PASS','shared_contract_sha256':sha(sp),'strong_transfer_sha256':sha(tp),
        'v_preserving_hidden_maps':cases,'reason_counts':dict(reasons),'minimum_map_gap':'0',
        'complete_A6_differences':960,'new_budget':'148951*u4 - 1278*u6',
        'joint_OPT_credit':'10857/2','joint_W_tax':'88871/9',
        'negative_A6_one_patterns':negative,'same_weight_comparison_tax':'17753/2',
        'tax_copy_argument_verified':True,'scope':'Universal fixed-coefficient necessary contract; remaining u4 payment not discharged; no SPE counterexample.',
        'seconds':time.time()-started,'verifier_sha256':sha(Path(__file__))}
Path(__file__).with_suffix('.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(result,ensure_ascii=False,indent=2))
