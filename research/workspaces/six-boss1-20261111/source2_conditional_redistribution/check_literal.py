#!/usr/bin/env python3
"""Independent Fraction audit.  Reads JSON, never imports the derivation code.

The envelope is independently recovered by intersecting, for each of the 16
tails, all 15 affine dominance half-intervals.  Row reconstruction starts
with individual player shares and actual menu indices.
"""
from fractions import Fraction as Q
from itertools import product, combinations
from pathlib import Path
from collections import Counter
import hashlib
import json

BASE = Path(__file__).resolve().parent
LIMIT = Q(5977,6912)
INITIAL5 = Q(43,48)
MID_S = Q(61273,6912)
EPSILON = Q(1,144)
TAILS = tuple(product(range(2), repeat=4))
TYPES = tuple(product(range(2), repeat=9))
COUNTS = Counter()
DOMINANCE = []
ROW_CHECKS = []


def load(filename):
    return json.loads((BASE/filename).read_text())


def dump(filename, data):
    (BASE/filename).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')


def lin_value(line, x):
    return line[0]+line[1]*x


def plus(x,y):
    return x[0]+y[0],x[1]+y[1]


def times(x,k):
    return x[0]*k,x[1]*k


def literal_weights(q0,s,x):
    u4=LIMIT-x;u5=INITIAL5+x
    b3=q0/2+q0*u4/12+q0*u5/6
    b4=q0/2+u4+q0*u5/6
    b5=q0/2+u5
    return (Q(0),u4,u5),(b3,b4,b5),25+u4+u5-s,1+b3+b4+b5


def literal_cost(case,ctx,tail,x):
    p=ctx['p']; t=ctx['t']; q=Q(ctx['q'])
    tau,beta,a,total=literal_weights(Q(case['q0']),Q(case['s']),x)
    r3,r4,r5,z=tail; L=p+t+r3+r4+r5+z
    def share(member):
        return Q(member,L) if member else Q(0)
    # Each true player's customer share is reconstructed separately.
    answer=a*share(t)-share(z)
    for w,r in zip(tau,tail[:3]):
        answer-=w*share(r)
    for cap,r in zip(beta,tail[:3]):
        answer+=cap*r
    answer+=z
    answer+=q/Q(p+t+r3+r4+r5+1)
    answer+=tau[0]*q/Q(p+t+4)
    answer+=tau[1]*q/Q(p+t+r3+3)
    answer+=tau[2]*q/Q(p+t+r3+r4+2)
    return answer


def literal_affine(case,ctx,tail):
    p=ctx['p'];t=ctx['t'];q=Q(ctx['q']);s=Q(case['s']);q0=Q(case['q0'])
    r3,r4,r5,z=tail;L=p+t+r3+r4+r5+z
    tau0=(Q(0),LIMIT,INITIAL5); tau1=(Q(0),Q(-1),Q(1))
    beta0=(q0/2+q0*LIMIT/12+q0*INITIAL5/6,
           q0/2+LIMIT+q0*INITIAL5/6,q0/2+INITIAL5)
    beta1=(q0/12,-1+q0/6,Q(1))
    a=25+LIMIT+INITIAL5-s
    const=(a*t-z-sum(w*r for w,r in zip(tau0,tail[:3])))/L if L else Q(0)
    slope=-sum(w*r for w,r in zip(tau1,tail[:3]))/L if L else Q(0)
    const+=sum(w*r for w,r in zip(beta0,tail[:3]))+z+q/Q(p+t+r3+r4+r5+1)
    slope+=sum(w*r for w,r in zip(beta1,tail[:3]))
    den=(p+t+4,p+t+r3+3,p+t+r3+r4+2)
    const+=sum(w*q/Q(d) for w,d in zip(tau0,den))
    slope+=sum(w*q/Q(d) for w,d in zip(tau1,den))
    return const,slope


def dominance_intervals(lines,left=Q(0),right=LIMIT):
    result={}
    for r,(c,b) in lines.items():
        lo,hi=left,right
        possible=True
        for v,(other_c,other_b) in lines.items():
            const=c-other_c;slope=b-other_b
            if slope>0:
                hi=min(hi,-const/slope)
            elif slope<0:
                lo=max(lo,-const/slope)
            elif const>0:
                possible=False;break
        if possible and lo<=hi:
            result[r]=(lo,hi)
    assert result
    return result


def true_minimum(case,cid,x):
    ctx=case['contexts'][cid]
    values={''.join(map(str,r)):literal_cost(case,ctx,r,x) for r in TAILS}
    low=min(values.values())
    return low,[r for r in values if values[r]==low],values


def audit_envelopes(case):
    computed={}
    full=set()
    for cid,ctx in case['contexts'].items():
        lines={''.join(map(str,r)):literal_affine(case,ctx,r) for r in TAILS}
        computed[cid]=lines
        for tail,line in lines.items():
            assert tuple(map(Q,case['states'][cid][tail]))==line
            for x in [Q(0),LIMIT,EPSILON]:
                assert lin_value(line,x)==literal_cost(case,ctx,tuple(map(int,tail)),x)
                COUNTS['literal_affine_numeric_checks']+=1
            COUNTS['affine_states']+=1
        admissible=dominance_intervals(lines)
        points=sorted({x for span in admissible.values() for x in span})
        claimed=case['envelopes'][cid]
        assert points==list(map(Q,claimed['breakpoints']))
        full.update(points)
        DOMINANCE.append({'case':case['id'],'context':cid,
            'tail_dominance_intervals':{r:list(map(str,span)) for r,span in admissible.items()},
            'inactive_tails':[r for r in lines if r not in admissible],
            'breakpoints':list(map(str,points))})
        for rec in claimed['points']:
            x=Q(rec['delta']);low,active,values=true_minimum(case,cid,x)
            assert low==Q(rec['minimum']) and active==rec['active_tails']
            assert values=={r:Q(v) for r,v in rec['all_16_costs'].items()}
            COUNTS['conditional_point_state_checks']+=16
        for rec in claimed['open_cells']:
            left,right=Q(rec['left']),Q(rec['right']);x=(left+right)/2
            active=[r for r,(lo,hi) in admissible.items() if lo<x<hi]
            assert active==rec['active_tails']
            chosen=lines[active[0]]
            assert tuple(map(Q,rec['minimum_affine']))==chosen
            for r,line in lines.items():
                gaps=[lin_value(line,left)-lin_value(chosen,left),
                      lin_value(line,right)-lin_value(chosen,right)]
                assert min(gaps)>=0
                assert gaps==list(map(Q,rec['all_16_endpoint_gaps'][r]))
                COUNTS['segment_endpoint_state_comparisons']+=2
            COUNTS['conditional_open_cells']+=1
    return computed,sorted(full)


def select_line(lines,x):
    return min(lines.values(),key=lambda lin:lin_value(lin,x))


def independent_fd_lines(case,computed,p,d,x):
    ans=(Q(0),Q(0))
    if d<6:
        ans=plus(ans,times(select_line(computed[f'p{p}_d{d}_t0'],x),Q(6-d,6)))
    if d>0:
        ans=plus(ans,times(select_line(computed[f'p{p}_d{d}_t1'],x),Q(d,6)))
    return ans


def physical_values(case,p,x):
    m={}
    for d in range(7):
        if d<6:
            m[(d,0)]=true_minimum(case,f'p{p}_d{d}_t0',x)[0]
        if d>0:
            m[(d,1)]=true_minimum(case,f'p{p}_d{d}_t1',x)[0]
    f={}
    for d in range(7):
        total=Q(0)
        if d<6:total+=Q(6-d,6)*m[(d,0)]
        if d>0:total+=Q(d,6)*m[(d,1)]
        f[d]=total
    return m,f


def audit_projection(case,computed,coarse):
    projection=case['projection']; crossings=[];allpoints=set(coarse)
    strict_gaps=[]
    for left,right in zip(coarse,coarse[1:]):
        x=(left+right)/2
        for p in (0,1):
            f={d:independent_fd_lines(case,computed,p,d,x) for d in range(1,7)}
            for d,e in combinations(range(1,7),2):
                a,b=f[d][0]-f[e][0],f[d][1]-f[e][1]
                if b:
                    crossing=-a/b
                    if left<=crossing<=right:
                        allpoints.add(crossing)
                        crossings.append((p,d,e,str(crossing)))
                elif a==0:
                    crossings.append((p,d,e,'identical'))
            winners=dominance_intervals(f,left,right)
            for d,(lo,hi) in winners.items():
                assert lo<=hi
            # Six-way comparison precedes recording that d=1 alone wins.
            assert set(winners)=={1}
            for d in range(2,7):
                gap=min(lin_value(f[d],left)-lin_value(f[1],left),
                        lin_value(f[d],right)-lin_value(f[1],right))
                assert gap>0
                strict_gaps.append({'p':p,'d':d,'cell':[str(left),str(right)],'positive_lower_bound':str(gap)})
    assert not crossings and not projection['all_f_pair_intersections']
    assert list(map(str,sorted(allpoints)))==case['breakpoints']
    assert projection['conditional_breakpoints']==list(map(str,coarse))
    for rec in projection['points']:
        x=Q(rec['delta'])
        for pp in rec['prefix_tables']:
            _,f=physical_values(case,pp['p'],x)
            g=min(f[d] for d in range(1,7))
            assert f=={int(d):Q(v) for d,v in pp['f'].items()}
            assert Q(pp['G'])==g
            assert pp['active_d']==[d for d in range(1,7) if f[d]==g]
            assert f[0]==0
            COUNTS['outer_f_point_values']+=7
    for rec in projection['open_cells']:
        left,right=Q(rec['left']),Q(rec['right']);x=(left+right)/2
        for pp in rec['prefix_tables']:
            p=pp['p'];f={d:independent_fd_lines(case,computed,p,d,x) for d in range(7)}
            assert {str(d):list(map(str,ff)) for d,ff in f.items()}==pp['f_affine']
            best=min(lin_value(f[d],x) for d in range(1,7))
            active=[d for d in range(1,7) if lin_value(f[d],x)==best]
            assert active==pp['active_d']
            g=f[active[0]]
            assert list(map(str,g))==pp['G_affine']
            for d in range(1,7):
                gaps=[lin_value(f[d],left)-lin_value(g,left),lin_value(f[d],right)-lin_value(g,right)]
                assert list(map(str,gaps))==pp['all_6_endpoint_gaps'][str(d)]
                COUNTS['G_segment_pair_endpoint_checks']+=2
    return strict_gaps


def reconstructed_row(case,target,x):
    tau,beta,a,S=literal_weights(Q(case['q0']),Q(case['s']),x)
    c_only=target=='C-only';mu=S-Q(case['s'])/5
    if case['mode']=='pure':
        target_index=8 if target in ['C','C-only'] else (6 if target=='X' else int(target[1:])-1)
        minima={(p,t,o):true_minimum(case,f'p{p}_t{t}_o{o}',x)[0]
                for p,t,o in product(range(2),repeat=3)}
    else:
        G={p:min(v for d,v in physical_values(case,p,x)[1].items() if d>0) for p in range(2)}
    vector=[]
    for b in TYPES:
        actual=sum(b[:6]);u2=Q(b[1],actual) if b[1] else Q(0)
        rhs=minima[(b[0],b[target_index],b[7])] if case['mode']=='pure' else b[7]*G[b[0]]
        vector.append(a*u2-rhs+(mu*b[8] if c_only else 0))
    vector.append(S-mu if c_only else S)
    return vector


def pure_closed(case,p,t,o,x):
    tau,beta,a,S=literal_weights(Q(1,6),Q(case['s']),x)
    anchor=t*(S+Q(24,p+5)-Q(case['s'])/5)
    anchor+=Q(o,6*(p+4*t+1))
    anchor+=tau[1]*Q(o,6*(p+2*t+3))+tau[2]*Q(o,6*(p+3*t+2))
    loss=Q(0)
    if t and p:
        loss=max(Q(0),Q(4,5)*x-Q(o,180))
    elif t:
        loss=max(Q(0),(Q(case['s'])-MID_S)/20-Q(13,18)*x-Q(o,120)*(1+tau[2]),
                 Q(3,4)*x+Q(case['s'])/20-Q(427,960)-Q(o,120))
    return anchor-loss,loss


def compact_G(case,p,x):
    tau,beta,a,S=literal_weights(Q(1,5),Q(case['s']),x)
    W=S+Q(24,p+5)-Q(case['s'])/5
    Z=Q(1,5)*(Q(1,p+1)+tau[1]/Q(p+3)+tau[2]/Q(p+2))
    if p:
        loss=max(Q(187,8640)-Q(23,30)*x,Q(1,60)+Q(4,5)*x)
    else:
        loss=max(Q(0),-Q(19427,46080)+Q(case['s'])/20-Q(43,60)*x,
                 -Q(137,320)+Q(case['s'])/20+Q(3,4)*x)
    return (5*Z+W-loss)/6


def audit_compact_formula_by_affine_states(case,computed):
    """Prove each compact formula continuously by literal state coefficients.

    Each displayed candidate is a real tail line.  On each certified full
    envelope cell and point at least one of those candidates is active.
    Thus candidate omission cannot change the minimum anywhere in the domain.
    """
    if case['mode']=='pure':
        for cid,ctx in case['contexts'].items():
            p,t,o=ctx['p'],ctx['t'],ctx['o']
            candidates=['0000'] if not t else (['1110','1101'] if p else ['1111','1011','1101'])
            expressions={}
            for x in [Q(0),Q(1)]:
                tau,beta,a,S=literal_weights(Q(1,6),Q(case['s']),x)
                A=t*(S+Q(24,p+5)-Q(case['s'])/5)+Q(o,6*(p+4*t+1))
                A+=tau[1]*Q(o,6*(p+2*t+3))+tau[2]*Q(o,6*(p+3*t+2))
                if not t:
                    expressions[x]=[A]
                elif p:
                    expressions[x]=[A,A-Q(4,5)*x+Q(o,180)]
                else:
                    h4=(Q(case['s'])-MID_S)/20-Q(13,18)*x-Q(o,120)*(1+tau[2])
                    h5=Q(3,4)*x+Q(case['s'])/20-Q(427,960)-Q(o,120)
                    expressions[x]=[A,A-h4,A-h5]
            for k,r in enumerate(candidates):
                expected=(expressions[Q(0)][k],expressions[Q(1)][k]-expressions[Q(0)][k])
                assert computed[cid][r]==expected
                COUNTS['compact_formula_actual_affine_candidates']+=1
            env=case['envelopes'][cid]
            for rec in env['points']+env['open_cells']:
                assert set(candidates)&set(rec['active_tails'])
                COUNTS['compact_formula_continuous_cover_checks']+=1
    else:
        for p in (0,1):
            c0=f'p{p}_d1_t0';c1=f'p{p}_d1_t1'
            candidates=['1011','1101'] if p else ['1111','1011','1101']
            expressions={}
            for x in [Q(0),Q(1)]:
                tau,beta,a,S=literal_weights(Q(1,5),Q(case['s']),x)
                W=S+Q(24,p+5)-Q(case['s'])/5
                Z=Q(1,5)*(Q(1,p+1)+tau[1]/Q(p+3)+tau[2]/Q(p+2))
                if p:
                    h4=Q(187,8640)-Q(23,30)*x
                    h5=Q(1,60)+Q(4,5)*x
                    expressions[x]=[Z,W-h4,W-h5]
                else:
                    h4=-Q(19427,46080)+Q(case['s'])/20-Q(43,60)*x
                    h5=-Q(137,320)+Q(case['s'])/20+Q(3,4)*x
                    expressions[x]=[Z,W,W-h4,W-h5]
            for k,(cid,r) in enumerate([(c0,'0000')]+[(c1,r) for r in candidates]):
                expected=(expressions[Q(0)][k],expressions[Q(1)][k]-expressions[Q(0)][k])
                assert computed[cid][r]==expected
                COUNTS['compact_formula_actual_affine_candidates']+=1
            for cid,allowed in [(c0,['0000']),(c1,candidates)]:
                env=case['envelopes'][cid]
                for rec in env['points']+env['open_cells']:
                    assert set(allowed)&set(rec['active_tails'])
                    COUNTS['compact_formula_continuous_cover_checks']+=1


def main():
    data=load('exact_envelopes.json');case_map={c['id']:c for c in data['cases']}
    g_certificates=[];all_samples={}
    for case in data['cases']:
        for x in [Q(0),LIMIT]:
            tau,beta,a,S=literal_weights(Q(case['q0']),Q(case['s']),x)
            assert min(tau)>=0 and min(beta)>0 and a>0 and S>0
            COUNTS['weight_endpoint_checks']+=8
        computed,coarse=audit_envelopes(case)
        audit_compact_formula_by_affine_states(case,computed)
        if case['mode']=='pure':
            assert list(map(str,coarse))==case['breakpoints']
        else:
            g_certificates.append({'case':case['id'],'strict_pair_gaps':audit_projection(case,computed,coarse)})
        bp=list(map(Q,case['breakpoints']))
        all_samples[case['id']]=sorted(set(bp+[EPSILON]+[(x+y)/2 for x,y in zip(bp,bp[1:])]))
        for x in all_samples[case['id']]:
            if case['mode']=='pure':
                for p,t,o in product(range(2),repeat=3):
                    actual=true_minimum(case,f'p{p}_t{t}_o{o}',x)[0]
                    assert actual==pure_closed(case,p,t,o,x)[0]
                    COUNTS['pure_closed_formula_checks']+=1
            else:
                for p in range(2):
                    m,f=physical_values(case,p,x)
                    assert compact_G(case,p,x)==min(f[d] for d in range(1,7))
                    COUNTS['ordered_closed_formula_checks']+=1
                    for menu in product(range(2),repeat=6):
                        d=sum(menu)
                        outer=Q(0)
                        for k,t in enumerate(menu):
                            actual_q=sum(menu[l] for l in range(6) if l!=k)*Q(1,5)
                            assert actual_q==Q(d-t,5)
                            outer+=m[(d,t)]/6
                            COUNTS['actual_five_query_means']+=1
                        assert outer==f[d]
                        COUNTS['actual_64_menu_outer_checks']+=1
    # Physical query identities: all 64 menus, all six indices, all possible denominators.
    for menu in product(range(2),repeat=6):
        d=sum(menu);o=int(d>0)
        for den in range(1,7):
            true_six=sum(Q(t,den) for t in menu)/6
            assert true_six-Q(o,6*den)==Q(d-o,6*den)>=0
            COUNTS['six_query_union_identities']+=1
            for k,t in enumerate(menu):
                true_five=sum(Q(menu[l],den) for l in range(6) if l!=k)/5
                assert true_five==Q(d-t,5*den)
                COUNTS['five_query_index_identities']+=1
    weak=load('all_weak_minimum_tables.json')['tables']
    for record in weak:
        case=case_map[record['case']];x=Q(record['delta'])
        for entry in record['tables']:
            low,active,values=true_minimum(case,entry['context'],x)
            assert Q(entry['minimum'])==low and entry['all_active_tails']==active
            COUNTS['global_sample_hidden_states']+=16
            COUNTS['global_sample_minimum_tables']+=1
            COUNTS['all_weak_active_tail_occurrences']+=len(active)
    endpoint=load('exact_family.json')['rows']+load('epsilon_rows.json')['rows']
    for row in endpoint:
        case=case_map[row['case']];x=Q(row['delta'])
        actual=list(map(Q,row['a']));expect=reconstructed_row(case,row['target'],x)
        assert len(actual)==513 and actual==expect
        assert row['numeric_divisor']=='25'
        ROW_CHECKS.append({'row':row['id'],'kind':'point','columns':513,'all_residuals_zero':True})
        COUNTS['point_row_columns']+=513
        if row['target']=='C-only':
            general=reconstructed_row(case,'C',x)
            mu=Q(row['C_equality_multiplier'])
            expected=[general[k]+mu*b[8] for k,b in enumerate(TYPES)]+[general[512]-mu]
            assert actual==expected
            COUNTS['C_equality_columns']+=513
    for row in load('affine_family.json')['rows']:
        case=case_map[row['case']];left,right=Q(row['left']),Q(row['right'])
        constant=list(map(Q,row['intercept']));slope=list(map(Q,row['delta_coefficient']))
        assert len(constant)==len(slope)==513
        lv=reconstructed_row(case,row['target'],left);rv=reconstructed_row(case,row['target'],right)
        for k in range(513):
            expected_slope=(rv[k]-lv[k])/(right-left)
            expected_constant=lv[k]-expected_slope*left
            assert slope[k]==expected_slope and constant[k]==expected_constant
            COUNTS['affine_row_coefficients']+=2
        mid=(left+right)/2
        mv=reconstructed_row(case,row['target'],mid)
        assert mv==[constant[k]+mid*slope[k] for k in range(513)]
        ROW_CHECKS.append({'row':row['id'],'kind':'affine','columns':513,'coefficient_pairs':513,'all_residuals_zero':True})
        COUNTS['affine_midpoint_columns']+=513
    epsilon=[]
    for cid in ['pure_q6_s0','pure_q6_sstar']:
        case=case_map[cid];old=reconstructed_row(case,'C-only',Q(0));new=reconstructed_row(case,'C-only',EPSILON)
        residuals=[]
        for k,b in enumerate(TYPES):
            p,c,o=b[0],b[8],b[7]
            deltaN=Q(o,6*(p+3*c+2))-Q(o,6*(p+2*c+3))
            claim=-EPSILON*deltaN+Q(1,180)*p*c*(1-o)
            if cid.endswith('sstar'):claim+=Q(101,27648)*(1-p)*c*(1-o)
            residuals.append(new[k]-old[k]-claim)
        residuals.append(new[512]-old[512])
        assert set(residuals)=={Q(0)}
        epsilon.append({'case':cid,'delta':str(EPSILON),'all_513_residuals':list(map(str,residuals)),
                        'status':'PASS','counterexample':None})
        COUNTS['epsilon_identity_columns']+=513
    # Source byte protection: only the four explicitly read sources are inspected.
    root=BASE.parents[3]
    pins=load('source_pins.json')
    for source in pins['sources']:
        assert hashlib.sha256((root/source['path']).read_bytes()).hexdigest()==source['sha256']
        COUNTS['source_pin_checks']+=1
    dump('literal_dominance_intervals.json',{'method':'all per-tail dominance half-interval intersections',
                                          'records':DOMINANCE})
    dump('literal_strict_G_comparisons.json',{'all_six_d_compared_before_selecting':True,
                                           'certificates':g_certificates})
    dump('literal_row_checks.json',{'all_rows_checked':ROW_CHECKS})
    dump('literal_epsilon_checks.json',{'identities':epsilon})
    dump('literal_checker_output.json',{'status':'PASS','agent_id':'/root/source2_conditional_redistribution',
          'independent':'JSON-only inputs; direct individual shares; independent affine coefficient expansion; per-tail dominance intervals',
          'counts':dict(COUNTS),'optimizer_calls':0,'global_candidate_reads':0,
          'mathematical_failures':[],'scope':'the specified true source-2 wallets on all six closed parameter segments'})
    print(json.dumps(dict(COUNTS),ensure_ascii=False),flush=True)


if __name__=='__main__':
    main()
