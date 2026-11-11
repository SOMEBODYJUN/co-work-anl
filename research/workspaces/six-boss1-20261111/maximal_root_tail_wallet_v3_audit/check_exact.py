#!/usr/bin/env python3
"""Independent literal reconstruction and exact certificate audit of root270.

Only standard-library arithmetic. No producer, optimizer, or previous checker
is imported/executed. All row coefficients are rebuilt from true shares,
literal menu averages and explicit hidden-tail minimization.
"""
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations_with_replacement, product
from pathlib import Path
import json
import re

HERE=Path(__file__).resolve().parent
WS=HERE.parent
REPO=WS.parents[2]
SRC=WS/'maximal_root_tail_wallet_v3'
ROLES=('C','B2','B3','B4','B5','B6','Omean')
KSTAR=F('87254934961879537539921985657780687995/449980920529477462633417363589807278334')
PINS={
    'maximal_root_tail_wallet_v3/exact_input.json':
        '01c57b65a82b682d222cb449407416c4db0de60961c90d6eaafd35d15b1f79d0',
    'maximal_root_tail_wallet_v3/exact_certificate.json':
        'b7d27bcddc6da34bed635bf7c36a607ffea130b56bcb0f62803b94b3c20dc925',
    'maximal_root_tail_wallet_v3/proof.md':
        'f5d47adde14fd247eeb55a4d1afa282400030ff361966e47c62deeabd1810851',
    'maximal_root_tail_wallet_v3/freeze_manifest.json':
        'c53dcf0806895d60ace71c7636bcb65defd15b30861abd26aff30a373b8e33a0',
    'maximal_root_tail_wallet_v2/exact_input.json':
        '86a235bf210862ef8f8bbbdea7ac324e71f691a8aa7af455a821e6379cfe117d',
    'main_all_source25_family/proof.md':
        'abe4e15a1d07b97ff230514f82415106267ad317bd94ef34ff0f0a3131f46bd0',
    'main_all_source25_family/exact_family.json':
        '8965ab6534776f0cc9570979128df1e99835e0cc0bf60ce9d4a87b5354d4bec0',
    'main_thirty_index_strengthening/requery30_envelopes.json':
        '14ef732b35d0f859113daf92c8dda1f08330413682b057c69a57543a41a360bc',
    'universal_union_wallet_v6/exact_input.json':
        '49532be5fae2913f2ab56ae641452510d7b0f8f14ff7049de0dd62fa7b9a8936',
    'universal_union_wallet_v6/exact_certificate.json':
        '98fa318efae0c6fef36e87b1861d559ede340ab4aaf7ed390c426854e5711f1d',
}


def digest(p):return sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def dot(a,b):return sum((x*y for x,y in zip(a,b)),F(0))


def share(bit,prefix,followers=0):
    assert bit in (0,1) and prefix>=0 and followers>=0
    return F(1,prefix+1+followers) if bit else F(0)


def payoff(seq,i):
    return share(seq[i],sum(seq[:i]),sum(seq[i+1:]))


def pure_pair(t,q,D):
    return share(t,D-1,q)+share(q,D-1)


def wallet(seq):
    p=sum(seq[:4]);y,z=seq[4:]
    return payoff(seq,4)+payoff(seq,5)+share(y,p)-share(y,p,1)


def menu_pair(D,o,distinct):
    menu=(o,0,0,0,0,0)
    pairs=[(i,j) for i in range(6) for j in range(6) if not distinct or i!=j]
    return sum((pure_pair(menu[i],menu[j],D) for i,j in pairs),F(0))/len(pairs)


PAIR_COST={(D,o,mode):menu_pair(D,o,mode)
           for D,o,mode in product(range(1,6),(0,1),(False,True))}


def source3_cost(h,state,distinct):
    seq,o=h[:6],h[6]
    q,r,y,t=state
    dev=seq[:2]+(q,r,y,t)
    value=126000*payoff(dev,2)
    for bit,weight in zip((r,y,t),(43,31218,34458)):
        value+=weight*share(bit,sum(seq[:3]),2)
    for bit in (r,y,t):value+=1654*share(bit,sum(seq[:5]))
    value+=5400*(share(o,sum(dev[:5]))/6-payoff(dev,5))
    value+=7740*(PAIR_COST[1+sum(dev[:4]),o,distinct]-wallet(dev))
    return value


def p25_hidden(p,t,q,tail):
    return (25*share(t,p,sum(tail))+F(sum(tail[:-1]),2)+tail[-1]
            -share(tail[-1],p+t+sum(tail[:-1]))
            +share(q,p+t+sum(tail[:-1])))


def main():
    for path,want in PINS.items():assert digest(WS/path)==want,path
    inp=read(SRC/'exact_input.json');cert=read(SRC/'exact_certificate.json')
    old=read(WS/'maximal_root_tail_wallet_v2/exact_input.json')
    assert cert['input_sha256']==PINS['maximal_root_tail_wallet_v3/exact_input.json']
    assert F(inp['fixed_K'])==KSTAR and F(inp['fixed_O'])==1
    assert inp['root_u_column']==128 and inp['nonnegative_columns']==list(range(129))
    assert inp['convention']=='A*x >= bK*K+bO*O'
    assert inp['objective']=={'128':'1'}
    atoms=list(product((0,1),repeat=7))
    assert inp['atoms']==[{'index':h,'bits':list(bits)} for h,bits in enumerate(atoms)]
    for previous,current in zip(old['raw_rows'],inp['raw_rows'][:72]):
        assert {k:v for k,v in previous.items() if k!='rhs'}=={
            k:v for k,v in current.items() if k!='rhs'}
    assert len(old['raw_rows'])==72

    # Both Cartesian36 and distinct-index30 are reconstructed literally.
    pair_menu_cases=mixed_menu_cases=0
    for D in range(1,6):
        for menu in product((0,1),repeat=6):
            d=sum(menu);o=int(d>0)
            for mode in (False,True):
                pairs=[(i,j) for i in range(6) for j in range(6) if not mode or i!=j]
                val=sum((pure_pair(menu[i],menu[j],D) for i,j in pairs),F(0))/len(pairs)
                formula=F(d,3*D)-(F(d*(d-1),30*D*(D+1)) if mode else F(d*d,36*D*(D+1)))
                assert val==formula and val>=PAIR_COST[D,o,mode]
                pair_menu_cases+=1
            for t in (0,1):
                val=sum((pure_pair(t,q,D) for q in menu),F(0))/6
                lower=sum((pure_pair(t,q,D) for q in (o,0,0,0,0,0)),F(0))/6
                assert val>=lower
                mixed_menu_cases+=1

    # Full128 old types, each with both q values and eight own true tails.
    main_table=read(WS/'main_thirty_index_strengthening/requery30_envelopes.json')
    local_table=read(SRC/'literal_c30_envelopes.json')
    local_states={(r['h'],r['q'],tuple(r['tail'])):r
                  for r in read(SRC/'literal_c30_states.json')}
    envelopes={};source3_state_count=0;residual_counts={False:[0,0],True:[0,0]}
    for mode in (False,True):
        for h,bits in enumerate(atoms):
            vals={state:source3_cost(bits,state,mode) for state in product((0,1),repeat=4)}
            a0=min(v for state,v in vals.items() if state[0]==0)
            a1=min(v for state,v in vals.items() if state[0]==1)
            o=bits[6];delta=max(a1-a0,F(0));gamma=max(a0-a1,F(0))
            m=a0 if not o else min((5*a0+a1)/6,a1)
            assert m==a0+delta*o/6-gamma*o
            assert m==F(main_table[h]['m30' if mode else 'm36'])
            envelopes[mode,h]=m
            for state,value in vals.items():
                residual=value+(gamma-delta)*state[0]-a0
                assert residual>=0
                residual_counts[mode][0]+=residual==0
                residual_counts[mode][1]+=residual>0
                if mode:
                    stored=local_states[h,state[0],state[1:]]
                    assert F(stored['cost'])==value and F(stored['residual'])==residual
                source3_state_count+=1
            if mode:
                entry=local_table[h]
                assert entry['h']==h and tuple(entry['bits'])==bits
                for key,value in [('a0',a0),('a1',a1),('delta',delta),('gamma',gamma),('m30',m)]:
                    assert F(entry[key])==value
                cost=126000*payoff(bits[:6],2)+65719*payoff(bits[:6],3)+4962*payoff(bits[:6],5)-m
                assert F(entry['coefficient'])==cost==F(main_table[h]['cut'])
    assert source3_state_count==4096

    p25_min={};p25_hidden_cases=0
    stated_p25={(r['i'],r['p'],r['t'],r['q'],tuple(r['tail'])):r
                for r in read(SRC/'literal_p25_states.json')}
    for i in range(2,6):
        n=6-i
        for p in range(i):
            for t,q in product((0,1),repeat=2):
                values={tail:p25_hidden(p,t,q,tail) for tail in product((0,1),repeat=n)}
                m=min(values.values());p25_min[i,p,t,q]=m
                assert m==F(n+1,2)*t+F(24*t,p+n+1)+F(q,p+1+n*t)
                for tail,value in values.items():
                    stored=stated_p25[i,p,t,q,tail]
                    assert F(stored['cost'])==value
                    assert F(stored['minimum'])==m and F(stored['residual'])==value-m>=0
                    p25_hidden_cases+=1
    assert p25_hidden_cases==328 and len(p25_min)==56

    def role_value(role,bits):
        return bits[ROLES.index(role)] if role!='Omean' else 2

    def p25_cost(i,p,t,q,o):
        menu=(o,0,0,0,0,0)
        if t<2 and q<2:return p25_min[i,p,t,q]
        if t==2 and q<2:return sum((p25_min[i,p,b,q] for b in menu),F(0))/6
        if t<2 and q==2:return sum((p25_min[i,p,t,b] for b in menu),F(0))/6
        return sum((p25_min[i,p,menu[k],menu[l]] for k in range(6)
                    for l in range(6) if k!=l),F(0))/30

    p25_double_cases=p25_single_cases=0
    for i in range(2,6):
        n=6-i
        for p in range(i):
            A=F(n+1,2)+F(24,p+n+1);B=F(1,p+1);C=F(n,(p+1)*(p+n+1))
            assert A-C>0 and B-C>0
            for menu in product((0,1),repeat=6):
                d=sum(menu);o=int(d>0)
                for bit in (0,1):
                    first=sum((p25_min[i,p,t,bit] for t in menu),F(0))/6
                    second=sum((p25_min[i,p,bit,q] for q in menu),F(0))/6
                    assert first==B*bit+F(d,6)*(A-C*bit)>=p25_cost(i,p,2,bit,o)
                    assert second==A*bit+F(d,6)*(B-C*bit)>=p25_cost(i,p,bit,2,o)
                    p25_single_cases+=2
                val=sum((p25_min[i,p,menu[k],menu[l]] for k in range(6)
                         for l in range(6) if k!=l),F(0))/30
                assert val==F(d,6)*(A+B)-F(d*(d-1),30)*C>=p25_cost(i,p,2,2,o)
                p25_double_cases+=1
    assert p25_double_cases==896 and p25_single_cases==3584

    def weak_pair(queries,bits,distinct=False):
        D=1+sum(bits[:4]);o=bits[6]
        t,q=(role_value(role,bits) for role in queries)
        if t==q==2:return PAIR_COST[D,o,distinct]
        if t==2 or q==2:
            pure=q if t==2 else t
            return sum((pure_pair(pure,b,D) for b in (o,0,0,0,0,0)),F(0))/6
        return pure_pair(t,q,D)

    expected=[]
    def add(name,family,**metadata):expected.append({'name':name,'family':family,**metadata})
    add('ROOT_IC','ROOT_IC')
    for i in range(2,7):add('CAP_B%d'%i,'CAP',source=i)
    add('BRANCH_UNION_OPT','UNION');add('ROOT_K_FLOOR','FLOOR')
    for i in range(2,7):
        for q in ROLES:add('SAFE_j%d|%s'%(i,q),'SAFE',source=i,queries=[q])
    for pair in combinations_with_replacement(ROLES,2):add('PAIR|'+'|'.join(pair),'PAIR',queries=list(pair))
    add('OPT_SOURCE3_REQUERY_CUT','REQUERY_CUT')
    add('PAIR30|Omean|Omean','PAIR30',queries=['Omean','Omean'])
    add('OPT_SOURCE3_REQUERY_30_CUT','REQUERY_30_CUT')
    for i in range(2,6):
        for t,q in product(ROLES,repeat=2):
            add('PORTFOLIO25_i%d|T=%s|Q=%s'%(i,t,q),'ROOT_BRANCH_PORTFOLIO25',source=i,T=t,Q=q)
    rows=inp['raw_rows'];assert len(rows)==len(expected)==270
    matrix=[];bKs=[];bOs=[];divisors=[]
    for declared,spec in zip(rows,expected):
        for key,value in spec.items():assert declared[key]==value,(spec['name'],key)
        fam=spec['family'];i=spec.get('source')
        bK=F(-1) if fam=='CAP' else F(1,6) if fam=='FLOOR' else F(-(7-i),2) if fam=='ROOT_BRANCH_PORTFOLIO25' else F(0)
        bO=F(-1) if fam=='UNION' else F(0)
        divisor=F(126000) if fam in ('REQUERY_CUT','REQUERY_30_CUT') else F(25) if fam=='ROOT_BRANCH_PORTFOLIO25' else F(1)
        assert F(declared['bK'])==bK and F(declared['bO'])==bO
        assert F(declared['rhs'])==bK*KSTAR+bO
        assert F(declared['numerical_divisor'])==divisor>0
        values=[]
        for h,bits in enumerate(atoms):
            seq,o=bits[:6],bits[6]
            if fam=='ROOT_IC':value=-payoff(seq,0)
            elif fam=='CAP':value=-F(seq[i-1])
            elif fam=='UNION':value=-F(int(any(seq)))
            elif fam=='FLOOR':value=F(0)
            elif fam=='SAFE':
                role=spec['queries'][0];p=sum(seq[:i-1])
                costs=(o,0,0,0,0,0) if role=='Omean' else (role_value(role,bits),)
                value=payoff(seq,i-1)-sum((share(b,p,6-i) for b in costs),F(0))/len(costs)
            elif fam in ('PAIR','PAIR30'):
                value=wallet(seq)-weak_pair(spec['queries'],bits,fam=='PAIR30')
            elif fam in ('REQUERY_CUT','REQUERY_30_CUT'):
                value=126000*payoff(seq,2)+65719*payoff(seq,3)+4962*payoff(seq,5)-envelopes[fam=='REQUERY_30_CUT',h]
            elif fam=='ROOT_BRANCH_PORTFOLIO25':
                p=sum(seq[:i-1]);t=role_value(spec['T'],bits);q=role_value(spec['Q'],bits)
                value=25*payoff(seq,i-1)-p25_cost(i,p,t,q,o)
            else:raise AssertionError(fam)
            assert value==F(declared['a'].get(str(h),'0')),(spec['name'],h)
            values.append(value)
        u_value=F(int(fam in ('ROOT_IC','FLOOR')))
        assert u_value==F(declared['a'].get('128','0'))
        assert set(declared['a']).issubset({str(j) for j in range(129)})
        values.append(u_value);matrix.append(values);bKs.append(bK);bOs.append(bO);divisors.append(divisor)
    names=[r['name'] for r in expected];index={name:i for i,name in enumerate(names)}
    objective=[F(0)]*128+[F(1)]
    E_C=[F(bits[0]) for bits in atoms]+[F(0)]
    E_O=[F(bits[6]) for bits in atoms]+[F(0)]
    assert len(inp['equalities'])==2
    for row,values,rhs,param in zip(inp['equalities'],(E_C,E_O),(KSTAR,F(1)),('K','O')):
        assert row['parameter']==param and F(row['rhs'])==rhs
        assert [F(row['a'].get(str(j),'0')) for j in range(129)]==values

    # Highlighted positive P25 row, independently in the compact true-share form.
    p25_name='PORTFOLIO25_i4|T=B6|Q=Omean';p25_index=index[p25_name]
    assert bKs[p25_index]==F(-3,2) and bOs[p25_index]==0
    for h,bits in enumerate(atoms):
        seq,o=bits[:6],bits[6];p=sum(seq[:3]);t=seq[5]
        compact=25*payoff(seq,3)-(F(3,2)+F(24,p+3))*t-F(o,6*(p+1+2*t))
        assert compact==matrix[p25_index][h]
    assert matrix[p25_index][128]==0

    # Exact primal and all raw rows, including zero/duplicate rows.
    assert set(cert['primal']).issubset({str(j) for j in range(129)})
    primal=[F(cert['primal'].get(str(j),'0')) for j in range(129)]
    assert all(v>=0 for v in primal)
    assert dot(E_C,primal)==KSTAR and dot(E_O,primal)==1
    slacks=[]
    assert set(cert['raw_unscaled_row_slacks'])==set(names)
    for name,row,bK,bO in zip(names,matrix,bKs,bOs):
        slack=dot(row,primal)-bK*KSTAR-bO
        assert slack>=0 and slack==F(cert['raw_unscaled_row_slacks'][name]),name
        slacks.append(slack)
    primal_objective=dot(objective,primal)
    assert primal_objective==F(cert['objective'])
    primal_den=int(cert['primal_common_denominator']);assert primal_den>0
    positive_primal=[j for j,v in enumerate(primal) if v>0]
    assert set(cert['integer_primal'])=={str(j) for j in positive_primal}
    for j in positive_primal:
        assert F(int(cert['integer_primal'][str(j)]),primal_den)==primal[j]

    # Exact dual, independent K/O parameters, and all129 column residuals.
    dual=cert['dual'];raw={k:F(v) for k,v in dual['original_unscaled_row_weights'].items()}
    assert set(raw).issubset(index) and all(v>0 for v in raw.values()) and len(raw)==10
    expected_positive={'ROOT_IC',*(f'CAP_B{i}' for i in range(2,7)),
                       'SAFE_j6|Omean','PAIR30|Omean|Omean','OPT_SOURCE3_REQUERY_30_CUT',p25_name}
    assert set(raw)==expected_positive
    lam=[raw.get(name,F(0)) for name in names]
    piC=F(dual['equality_C_size']);piO=F(dual['equality_OPT_union'])
    residual=[]
    assert set(dual['column_residuals'])=={str(j) for j in range(129)}
    for j in range(129):
        r=objective[j]-sum((weight*row[j] for weight,row in zip(lam,matrix)),F(0))-piC*E_C[j]-piO*E_O[j]
        assert r>=0 and r==F(dual['column_residuals'][str(j)]),j
        residual.append(r)
    assert all(weight*slack==0 for weight,slack in zip(lam,slacks))
    assert all(r*x==0 for r,x in zip(residual,primal))
    a=piC+dot(lam,bKs);b=piO+dot(lam,bOs)
    assert a==F(cert['universal_root_line']['a']) and b==F(cert['universal_root_line']['b'])
    dual_value=a*KSTAR+b
    assert dual_value==primal_objective
    assert dual_value==sum((weight*(bK*KSTAR+bO) for weight,bK,bO in zip(lam,bKs,bOs)),F(0))+piC*KSTAR+piO
    assert raw.get('BRANCH_UNION_OPT',0)==0==F(cert['branch_union_OPT_weight'])
    assert raw.get('ROOT_K_FLOOR',0)==0==F(cert['root_K_floor_weight'])

    integer_line={key:int(val) for key,val in cert['universal_root_line']['integer_line'].items()}
    assert integer_line=={'u':16877573861922720,'K':1767904008200582,'O':337340181272013}
    assert F(integer_line['K'],integer_line['u'])==a and F(integer_line['O'],integer_line['u'])==b
    DB=int(dual['common_budget_denominator'])
    assert DB==67510295447690880==4*integer_line['u']
    L={name:DB*value for name,value in raw.items()}
    assert all(value.denominator==1 for value in L.values())
    assert {k:int(v) for k,v in dual['integer_original_row_weights'].items()}=={k:int(v) for k,v in L.items()}
    betaC,betaO=DB*piC,DB*piO
    assert [int(betaC),int(betaO)]==[int(v) for v in dual['integer_equality_multipliers']]
    assert betaC==22380459227386502 and betaO==1349360725088052
    cap_sum=sum(L[f'CAP_B{i}'] for i in range(2,7))
    p25_K_cost=F(3,2)*L[p25_name]
    assert cap_sum==15217199002150806 and p25_K_cost==91644192433368
    assert betaC-cap_sum-p25_K_cost==4*integer_line['K']
    assert betaO==4*integer_line['O']
    expected_K_parts={name:lam[r]*bKs[r] for r,name in enumerate(names) if lam[r]*bKs[r]}
    expected_O_parts={name:lam[r]*bOs[r] for r,name in enumerate(names) if lam[r]*bOs[r]}
    assert {k:F(v) for k,v in dual['K_parameter_contributions'].items()}==expected_K_parts
    assert {k:F(v) for k,v in dual['O_parameter_contributions'].items()}==expected_O_parts

    identity={}
    for j in range(129):
        rhs=sum((weight*row[j] for weight,row in zip(lam,matrix)),F(0))+residual[j]+piC*E_C[j]+piO*E_O[j]
        identity[str(j)]=objective[j]-rhs
        integer_rhs=sum((L.get(name,F(0))*row[j] for name,row in zip(names,matrix)),F(0))+DB*residual[j]+betaC*E_C[j]+betaO*E_O[j]
        assert DB*objective[j]==integer_rhs
    identity['K']=-a-(-dot(lam,bKs)-piC)
    identity['O']=-b-(-dot(lam,bOs)-piO)
    assert all(v==0 for v in identity.values()) and len(identity)==131
    assert {k:F(v) for k,v in cert['homogeneous_131_column_identity_residuals'].items()}==identity
    scaled={k:F(v) for k,v in dual['scaled_solver_form_weights'].items()}
    assert set(scaled)==set(raw)
    for name,value in raw.items():assert scaled[name]==value*divisors[index[name]]
    for j in range(131):
        if j<129:columns=[row[j] for row in matrix]
        elif j==129:columns=bKs
        else:columns=bOs
        assert sum((scaled.get(name,F(0))*col/d for name,col,d in zip(names,columns,divisors)),F(0))==dot(lam,columns)

    # Proof transcription: all ten integer payments and every positive mass.
    proof=(SRC/'proof.md').read_text()
    labels={'ROOT_IC':'ROOT_IC',**{f'CAP_B{i}':f'CAP_B{i}' for i in range(2,7)},
            'SAFE_j6|Omean':'SAFE_j6(Omean)','PAIR30|Omean|Omean':'PAIR30(Omean,Omean)',
            'OPT_SOURCE3_REQUERY_30_CUT':'C30原126000尺度',
            p25_name:'P25_i4(T=B6,Q=Omean)原25尺度'}
    for name,label in labels.items():
        hit=re.search(r'^\| '+re.escape(label)+r' \| (\d+) \|$',proof,re.M)
        assert hit and F(hit.group(1))==L[name],name
    point_rows=re.findall(r'^\| (\d+) \| ([01]{7}) \| (\d+) \|$',proof,re.M)
    assert len(point_rows)==10
    assert {int(j) for j,bits,num in point_rows}==set(positive_primal)-{128}
    for j,bits,num in point_rows:
        assert int(bits,2)==int(j) and F(int(num),primal_den)==primal[int(j)]
    assert int(re.search(r'E=(\d+)',proof).group(1))==primal_den
    assert F(int(re.search(r'u=(\d+)/E',proof).group(1)),primal_den)==primal[128]

    # Read the released v6 vector only for K provenance and the stated root gap.
    v6inp=read(WS/'universal_union_wallet_v6/exact_input.json')
    v6cert=read(WS/'universal_union_wallet_v6/exact_certificate.json')
    actual_types=list(product((0,1),repeat=8))
    assert v6inp['atom_columns']==[
        {'index':j,'a':list(bits[:6]),'x':bits[6],'o':bits[7]}
        for j,bits in enumerate(actual_types)]
    old_point={int(k):F(v) for k,v in v6cert['primal'].items()}
    assert old_point[256]==KSTAR
    old_u=sum((old_point.get(j,F(0))*payoff(bits[:6],0) for j,bits in enumerate(actual_types)),F(0))
    comparison=cert['comparison_at_released_K']
    assert old_u==F(comparison['v6_actual_root_u'])
    gap=primal_objective-old_u
    assert gap==F(comparison['root_gap_over_v6_u'])>0
    assert old_u==F(comparison['ROOT30_B2_a'])*KSTAR+F(comparison['ROOT30_B2_b'])
    zeros=[j for j in range(128) if residual[j]==0]
    assert zeros==[0,1,3,5,9,17,33,103,115,121,123,125] and residual[128]==0
    files=[WS/p for p in PINS]
    files += [SRC/'source_review.md',SRC/'literal_c30_states.json',SRC/'literal_c30_envelopes.json',
              SRC/'literal_p25_states.json',WS/'maximal_root_tail_wallet/derivation.md',
              WS/'main_thirty_index_strengthening/proof.md',
              REPO/'archives/customer-attraction/state/定义/共同目录完整历史模型--定义.md',
              REPO/'archives/customer-attraction/state/引理/末两人重叠比较与任意索引聚合--引理.md',
              REPO/'archives/customer-attraction/state/引理/共享真实末回复的组合查询投影与同源重配权--引理.md']
    result={
        'status':'PASS_INDEPENDENT_LITERAL_ROOT270_PRIMAL_DUAL_AND_131_COLUMNS',
        'raw_rows':270,'nonnegative_columns':129,'equalities':2,
        'unscaled_coefficient_comparisons':270*129,'independent_K_O_parameter_comparisons':540,
        'old72_symbolic_rows_preserved':True,'fixed_K':str(KSTAR),'fixed_O':'1',
        'PAIR_full36_and_distinct30_literal_menu_cases':pair_menu_cases,
        'PAIR_mixed_menu_cases':mixed_menu_cases,
        'C36_and_C30_literal_hidden_states':source3_state_count,
        'C36_envelopes':128,'C30_envelopes':128,
        'P25_literal_hidden_states':p25_hidden_cases,'P25_exact_minima':len(p25_min),
        'P25_double30_menu_cases':p25_double_cases,'P25_single_menu_cases':p25_single_cases,
        'highlighted_P25_row':p25_name,'highlighted_P25_K_cost':'3/2',
        'positive_primal_atoms':[j for j in positive_primal if j<128],
        'primal_exact_objective':str(primal_objective),'dual_exact_objective':str(dual_value),
        'primal_dual_gap':'0','primal_all270_slacks_nonnegative':True,
        'dual_positive_rows':list(raw),'dual_all129_residuals_nonnegative':True,
        'atom_residual_zero_indices':zeros,'atom_residual_positive_count':116,
        'u_residual':'0','row_and_column_complementarity':'PASS',
        'homogeneous_identity_columns':131,'scaled_unscaled_identity_columns':131,
        'free_equality_C_multiplier':str(piC),'free_equality_O_multiplier':str(piO),
        'universal_root_line':{k:str(v) for k,v in integer_line.items()},
        'slope':str(a),'intercept':str(b),'integer_budget_denominator':DB,
        'integer_budget_scale_over_primitive_line':4,
        'integer_cap_total':str(cap_sum),'integer_P25_K_cost':str(p25_K_cost),
        'integer_C_equality':str(betaC),'integer_O_equality':str(betaO),
        'proof_positive_integer_payment_rows_checked':10,
        'proof_positive_atom_rows_checked':10,
        'branch_union_OPT_weight':'0','root_K_floor_weight':'0',
        'universal_line_scope':'Any six legal query labels and their union; C must be a genuine maximum naked-size label and u is the original actual root payoff.',
        'whole270_system_scope':'O=OPT6 because the system retains the branch-union cap.',
        'v6_vector_root_u':str(old_u),'specified_root_gap_over_v6':str(gap),
        'v6_use_scope':'Read only its released K and visible actual-root payoff; no full v6 LP or whole-face audit.',
        'source_sha256':{str(p.relative_to(REPO)):digest(p) for p in files},
        'optimizer_calls':0,'Main_builder_or_prior_audit_code_executed_or_imported':False,
        'not_claimed':['complete SPE realization','global root sharpness','whole v6 optimum-face exclusion',
                       'recovery-rank certification','best-known bound or half theorem'],
        'outstanding_errors':[],
    }
    (HERE/'audit_result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ('status','raw_rows','unscaled_coefficient_comparisons',
                     'homogeneous_identity_columns','primal_exact_objective','universal_root_line',
                     'highlighted_P25_K_cost','integer_budget_scale_over_primitive_line',
                     'specified_root_gap_over_v6','outstanding_errors')},indent=2))


if __name__=='__main__':main()
