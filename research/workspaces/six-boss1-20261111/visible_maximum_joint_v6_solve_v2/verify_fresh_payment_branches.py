#!/usr/bin/env python3
"""Independent exact customer-payoff audit. Standard library only.

Does not import the diagnostic generator, a builder, the solver, recovery, or
face analysis. Reads the frozen original rows and current exact certificate.
"""
import hashlib
import itertools
import json
from fractions import Fraction as Q
from pathlib import Path

OUT = Path(__file__).resolve().parent
REPO = OUT.parents[3]
WS = OUT.parent


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def load(p):
    return json.loads(p.read_text())


def cube(n):
    return list(itertools.product(range(2), repeat=n))


def utility(b, j):
    return Q(b[j-1], sum(b[:6])) if sum(b[:6]) else Q(0)


def customer_budget_cost(prefix, forced, tails, source, ic, caps, safes, menu):
    # Sum separate actual customer shares and the individual legal queries.
    tail = dict(zip(range(source+1,7), tails))
    load_here = prefix+forced+sum(tails)
    pay = lambda member: Q(member, load_here) if load_here else Q(0)
    cost = ic*pay(forced)
    for j in range(source+1,6):
        cost += caps[j]*tail[j]-safes[j]*pay(tail[j])
    cost += tail[6]-pay(tail[6])
    for member in menu:
        cost += Q(member,6*(prefix+forced+sum(tails[:-1])+1))
        for j in range(source+1,6):
            cost += safes[j]*Q(member,6*(prefix+forced+sum(tail[k] for k in range(source+1,j))+7-j))
    return cost


def x_budget_cost(b, y, t):
    oldD=sum(b[:4])+1
    newD=sum(b[:3])+b[6]+1
    # These are the six independently stated true wallet customer columns.
    columns=[Q(b[6],sum(b[:3])+1+y+t),Q(y,oldD),Q(t),
             (Q(b[7],6)-t)/(newD+y),
             (Q(b[5])+Q(b[7],6))/newD-Q(b[5]*b[7],6*newD*(newD+1))
             -Q(y,newD+t)-Q(t,newD+y)-Q(y,newD*(newD+1)),
             (Q(t)+Q(b[7],6))/oldD-Q(t*b[7],6*oldD*(oldD+1))]
    return sum(w*c for w,c in zip([4096,800,71,384,512,900],columns))


def c30_column(h, q, r, y, t):
    prefix=h[0]+h[1]
    payoff3=Q(q,prefix+1+r+y+t)
    safe4=[Q(v,prefix+h[2]+3) for v in (r,y,t)]
    safe6=[Q(v,prefix+h[2]+h[3]+h[4]+1) for v in (r,y,t)]
    D=prefix+q+r+1
    last=Q(h[6],6*(D+y))-Q(t,D+y)
    pair=Q(h[6],3*D)-Q(y,D+t)-Q(t,D+y)-Q(y,D*(D+1))
    return 126000*payoff3+sum(w*v for w,v in zip([43,31218,34458],safe4))+1654*sum(safe6)+5400*last+7740*pair


def check_columns(raw, v, reported):
    assert len(v)==len(reported)==513
    for j in range(513):
        assert Q(raw['a'].get(str(j),0))==v[j]
        assert Q(reported[j])==0


def affine(v, face):
    coordinates={z['column']:(Q(z['constant']),list(map(Q,z['parameter_coefficients']))) for z in face['coordinates']}
    n=len(face['parameters'])
    constant=Q(0); direction=[Q(0)]*n
    for j,c in enumerate(v):
        if j in coordinates:
            base,dirs=coordinates[j]
            constant+=c*base
            direction=[x+c*y for x,y in zip(direction,dirs)]
    return constant,direction


def main():
    diagnostic=load(OUT/'fresh_payment_branches.json')
    pins=load(OUT/'fresh_diagnostic_source_pins.json')
    assert sha(OUT/'fresh_diagnostic_source_pins.json')==diagnostic['diagnostic_source_pins_sha256']
    for path,pin in pins['files'].items():
        p=REPO/path
        assert p.stat().st_size==pin['bytes'] and sha(p)==pin['sha256'],path
    assert sha(WS/'visible_maximum_joint_v6/exact_input.json')=='8f953bca6b65a8093d5fcf0fdb5a432ba3603137fe1015cd06fc8f6324e68769'
    assert sha(OUT/'exact_certificate.json')=='bbacce728e8172049b52e8468e4e6921d316854a2113528e5c74d64d7372f028'
    assert sha(OUT/'optimal_face.json')=='7258aacace9180c43e8bc8a30a103bc3bd090eb6c19dd77f9a771c01d2c8be77'
    model=diagnostic['corrected_X_model']
    assert model['P']=='P_y=sum_{j=1}^4 1[y in actual A_j]'
    assert model['selection']=='One legal label X in argmax over the entire common catalog of sum_{y in Q} 1/(P_y+1)'
    assert model['same_X_everywhere'] and not model['maximality_at_other_histories_assumed']
    data=load(WS/'visible_maximum_joint_v6/exact_input.json');rows=data['raw_rows']
    cert=load(OUT/'exact_certificate.json');face=load(OUT/'optimal_face.json')
    atoms=[tuple(z['a'])+(z['x'],z['o'],z['c']) for z in data['atom_columns']]
    assert atoms==cube(9)
    paid=[i for i,v in enumerate(cert['dual']['raw_row_weights']) if Q(v)>0]
    assert paid==diagnostic['fresh_positive_raw_indices']==[47,134,218,221,2564,3459,3468,3739,4012,4067,4107,4176]
    # All paid rows are tight on the full affine face, not merely at one point.
    for i in paid:
        v=[Q(rows[i]['a'].get(str(j),0)) for j in range(513)]
        c,d=affine(v,face)
        assert c==Q(rows[i]['rhs']) and not any(d)
    records=diagnostic['seven_minimal_CAP_rows']
    weak={}; menus_checked=0; local_states=0
    for record in records:
        idx=record['raw_index'];raw=rows[idx];m=raw.get('source_row_metadata',raw);w=m.get('weights',{})
        source=m['source'];target=m.get('forced_target',m.get('target'));target='C' if target=='C-only' else target
        tau={int(k):Q(v) for k,v in m.get('tau_by_true_source',w.get('tau',{})).items()}
        beta={int(k):Q(v) for k,v in m.get('middle_CAP_weights',w.get('beta',{})).items()}
        ic=Q(m.get('source_IC_weight',w.get('source_IC')))
        S=Q(m.get('K_weight',m.get('total_K_weight',w.get('K_before_C_equality'))))
        mu=Q(m.get('free_C_equality_multiplier',m.get('C_equality_multiplier')) or 0)
        assert ic>0 and all(v>0 for v in beta.values()) and all(v>=0 for v in tau.values())
        assert S==1+sum(beta.values())
        assert Q(record['source_IC_weight'])==ic and Q(record['signed_C_equality_multiplier'])==mu
        assert record['ordered_history']==[f'A{k}' for k in range(1,source)]+[target]
        assert record['source_metadata_verbatim']=={k:v for k,v in raw.items() if k!='a'}
        tab={(z['p'],z['t'],z['o']):z for z in record['state_tables']}
        assert len(tab)==source*4
        mins={}; weak[idx]={}
        for p,t,o in itertools.product(range(source),range(2),range(2)):
            report=tab[p,t,o];v={}
            for tail in cube(6-source):
                tailstr=''.join(map(str,tail))
                baseline=customer_budget_cost(p,t,tail,source,ic,beta,tau,[o,0,0,0,0,0])
                v[tailstr]=baseline;local_states+=1
                rawr=next(z for z in report['all_tail_costs'] if z['tail']==tailstr)
                assert Q(rawr['cost'])==baseline
                zeroq=customer_budget_cost(p,t,tail,source,ic,beta,tau,[0]*6)
                oneq=customer_budget_cost(p,t,tail,source,ic,beta,tau,[1,0,0,0,0,0])
                slope=oneq-zeroq
                assert slope>0 and Q(rawr['query_slope'])==6*slope
                for menu in cube(6):
                    if int(any(menu))==o:
                        true=customer_budget_cost(p,t,tail,source,ic,beta,tau,menu)
                        assert true-baseline==(sum(menu)-o)*slope>=0
                        menus_checked+=1
            lo=min(v.values());mins[p,t,o]=lo
            weak[idx][p,t,o]=sorted(z for z,value in v.items() if value==lo)
            assert Q(report['minimum'])==lo and sorted(report['weak_tails'])==weak[idx][p,t,o]
            for z in report['all_tail_costs']:assert Q(z['residual'])==v[z['tail']]-lo>=0
        coef=[]
        for b in atoms:
            t=b[8] if target=='C' else b[int(target[1:])-1]
            coef.append(ic*utility(b,source)+mu*b[8]-mins[sum(b[:source-1]),t,b[7]])
        check_columns(raw,coef+[S-mu],record['all513_column_identity_residuals'])
    for group in diagnostic['same_history_weak_intersections']:
        ids=group['raw_indices']; matching=[r for r in records if r['ordered_history']==group['ordered_history']]
        assert ids==[r['raw_index'] for r in matching]
        for item in group['all_state_intersections']:
            key=(item['p'],item['t'],item['o']); common=set(weak[ids[0]][key])
            for i in ids[1:]:common.intersection_update(weak[i][key])
            assert sorted(common)==item['common_weak_tails']
    assert next(g for g in diagnostic['same_history_weak_intersections'] if g['raw_indices']==[3459,3468])['ordered_history']==['A1','A2','A5']
    assert next(g for g in diagnostic['same_history_weak_intersections'] if g['raw_indices']==[3739])['ordered_history']==['A1','A2','A3','A5']

    direct={r['raw_index']:r for r in diagnostic['direct_legacy_wallets']}
    v47=[utility(b,6)-Q(b[7],6*(sum(b[:5])+1)) for b in atoms]+[Q(0)]
    v134=[]
    for b in atoms:
        D=sum(b[:4])+1
        # Wallet RHS u5+F_X minus the exact X/union query cost.
        v134.append(utility(b,5)+Q(b[6],D)-(Q(b[6])+Q(b[7],6))/D+Q(b[6]*b[7],6*D*(D+1)))
    check_columns(rows[47],v47,direct[47]['all513_column_identity_residuals'])
    check_columns(rows[134],v134+[Q(0)],direct[134]['all513_column_identity_residuals'])
    xr=diagnostic['true_X_tail_row'];xm={}
    assert len(xr['state_tables'])==256
    for entry in xr['state_tables']:
        b=tuple(entry['actual_six_x_o']); costs={''.join(map(str,z)):x_budget_cost(b,*z) for z in cube(2)}
        lo=min(costs.values());xm[b]=lo
        assert Q(entry['minimum'])==lo and sorted(entry['weak_tails'])==sorted(z for z,v in costs.items() if v==lo)
        for z in entry['all_tail_costs']:assert Q(z['cost'])==costs[z['tail']] and Q(z['residual'])==costs[z['tail']]-lo>=0
    xv=[4096*utility(b,4)+900*utility(b,5)+Q(1700*b[6],sum(b[:4])+1)-xm[b[:8]] for b in atoms]+[Q(71)]
    check_columns(rows[218],xv,xr['all513_column_identity_residuals'])
    cr=diagnostic['actual_requery30_row'];cm={}
    assert len(cr['state_tables'])==128
    for entry in cr['state_tables']:
        h=tuple(entry['actual_six_and_o']);values=[]
        for q in (0,1):
            vals={''.join(map(str,z)):c30_column(h,q,*z) for z in cube(3)};lo=min(vals.values());values.append(lo)
            report=entry['query_tables'][q]
            assert Q(report['minimum'])==lo and sorted(report['weak_tails'])==sorted(z for z,v in vals.items() if v==lo)
            for z in report['all_tail_costs']:assert Q(z['cost'])==vals[z['tail']] and Q(z['residual'])==vals[z['tail']]-lo>=0
        assert values[1]-values[0]==Q(entry['a1_minus_a0'])>0
        envelope=values[0] if not h[6] else (5*values[0]+values[1])/6
        cm[h]=envelope;assert Q(entry['union_envelope'])==envelope
    cv=[126000*utility(b,3)+65719*utility(b,4)+4962*utility(b,6)-cm[b[:6]+(b[7],)] for b in atoms]+[Q(0)]
    check_columns(rows[221],cv,cr['all513_column_identity_residuals'])

    rr=diagnostic['root270_row'];den=Q(67510295447690880)
    ww=[67510295447690880,622403086173831,3736778489617071,3696167188982850,3608286607200810,3553563630176244,1712829042623520,2292281651099340,24602518440,61096128288912]
    assert ww==rr['original_ten_budget_integer_weights']
    bcoef=Q(883952004100291,8438786930961360);ocoef=Q(37482242363557,1875285984658080);eta=Q(1087978231314917,84387869309613600)
    rootzero=[];rootfacezero=[]
    for idx,h in enumerate(cube(7)):
        b=h[:6]+(0,h[6],h[0]);D=sum(b[:4])+1;p=sum(b[:3]);o=h[6]
        cvec=[-utility(b,1),-Q(b[1]),-Q(b[2]),-Q(b[3]),-Q(b[4]),-Q(b[5]),
              utility(b,6)-Q(o,6*(sum(b[:5])+1)),
              utility(b,5)+utility(b,6)+Q(b[4],D*(D+1))-Q(o,3*D),
              126000*utility(b,3)+65719*utility(b,4)+4962*utility(b,6)-cm[h],
              25*utility(b,4)-(Q(3,2)+Q(24,p+3))*b[5]-Q(o,6*(p+1+2*b[5]))]
        residual=-(sum(v*w for v,w in zip(cvec,ww))+22380459227386502*h[0]+1349360725088052*o)/den
        adjusted=residual-eta*h[0]*(1-o);entry=rr['all128_states'][idx]
        assert entry['c_b2_b3_b4_b5_b6_o']==list(h)
        assert list(map(Q,entry['ten_unscaled_budget_column_coefficients']))==cvec
        assert Q(entry['original_remainder'])==residual and Q(entry['strict_outside_remainder'])==adjusted>=0
        if adjusted==0:
            rootzero.append(idx)
            if not h[0]*(1-o):rootfacezero.append(idx)
    assert rootzero==rr['weak_state_ids_before_face_C_outside_zero']==[0,1,3,5,9,17,33,102,103,115,121,123,125]
    assert rootfacezero==rr['weak_state_ids_after_face_C_outside_zero']==[0,1,3,5,9,17,33,103,115,121,123,125]
    assert (sum(ww[1:6])+Q(3,2)*ww[9]-22380459227386502)/den==-bcoef
    assert -Q(1349360725088052)/den==-ocoef and ww[0]/den==1
    rv=[utility(b,1)-ocoef*b[7]-eta*b[8]*(1-b[7]) for b in atoms]+[-bcoef]
    check_columns(rows[4176],rv,rr['all513_column_identity_residuals'])

    face_functions={
        'u2_minus_K_over_5':[utility(b,2) for b in atoms]+[Q(-1,5)],
        'C_outside_O':[Q(b[8]*(1-b[7])) for b in atoms]+[Q(0)],
        'N4_C_minus_K_over_5':[Q(b[7],6*(b[0]+2*b[8]+3)) for b in atoms]+[Q(-1,5)],
        'size_A5':[Q(b[4]) for b in atoms]+[Q(0)],
        'size_A6':[Q(b[5]) for b in atoms]+[Q(0)],
        'C_intersect_A1':[Q(b[8]*b[0]) for b in atoms]+[Q(0)],
        'C_outside_A1':[Q(b[8]*(1-b[0])) for b in atoms]+[Q(0)],
    }
    constants={}
    for name,v in face_functions.items():
        report=diagnostic['fresh_full_face_functionals'][name];const,dirs=affine(v,face)
        assert list(map(Q,report['full513_coefficients']))==v
        assert Q(report['constant'])==const and list(map(Q,report['parameter_coefficients']))==dirs and not any(dirs)
        constants[name]=const
    assert constants['C_outside_O']==constants['u2_minus_K_over_5']==0
    cstates={k:sorted(set(weak[4012][k]) & set(weak[4067][k])) for k in weak[4012]}
    assert cstates[0,1,0]==[] and cstates[0,1,1]==['1111'] and cstates[1,1,1]==['1101','1110']
    for p in (0,1):
        for s in cstates[p,1,1]:
            assert s[0]==s[1]=='1' and p+1+sum(map(int,s))==5
    # Strictly positive CAPs turn the pointwise C inclusion into exact coverage.
    for idx in (4012,4067):
        w=rows[idx]['source_row_metadata']['weights']
        assert all(Q(v)>0 for v in w['beta'].values()) and Q(w['tau']['4'])>0
    gap=constants['N4_C_minus_K_over_5']
    assert gap==Q(diagnostic['whole_face_SPE_obstruction']['positive_gap'])>0
    result={
        'status':'PASS_INDEPENDENT_FRESH_TRUE_PAYMENT_AND_WHOLE_FACE_OBSTRUCTION',
        'input_sha256':sha(WS/'visible_maximum_joint_v6/exact_input.json'),
        'certificate_sha256':sha(OUT/'exact_certificate.json'),'face_sha256':sha(OUT/'optimal_face.json'),
        'diagnostic_sha256':sha(OUT/'fresh_payment_branches.json'),'diagnostic_source_pins_sha256':sha(OUT/'fresh_diagnostic_source_pins.json'),
        'all_positive_raw_rows':paid,'all513_columns_for_each_paid_row_checked':12*513,
        'all_positive_rows_tight_on_whole_affine_face':12,'minimal_CAP_tail_states_checked':local_states,
        'individual_six_label_membership_checks':menus_checked,'X_tail_states_checked':1024,'requery30_tail_states_checked':2048,
        'root_source_columns_checked':131,'root_before_face_weak_ids':rootzero,'root_after_face_weak_ids':rootfacezero,
        'same_history_intersections_checked':len(diagnostic['same_history_weak_intersections']),
        'whole_face_new_functional_identities_checked':len(face_functions),
        'whole_face_SPE_obstruction_gap':str(gap),'corrected_actual_first_four_global_X_binding_checked':True,
        'optimizer_calls':0,'builder_solver_recovery_face_or_diagnostic_generator_imported':False,
        'scope':'Necessary real-history obstruction excludes the entire current exact alpha face. No uniform epsilon, half, or SPE realization is asserted.'}
    (OUT/'fresh_payment_branches_check.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(result,ensure_ascii=False,indent=2))


if __name__=='__main__':main()
