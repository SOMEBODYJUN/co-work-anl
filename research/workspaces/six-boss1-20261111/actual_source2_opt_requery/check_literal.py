#!/usr/bin/env python3
"""Independent literal replay of static samples and payment identities.

Reads JSON only; does not import/execute the coefficient kernel or generator.
No point, matrix builder, optimizer, third-party arithmetic or full8192 table.
"""
from collections import Counter
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations_with_replacement, product
from pathlib import Path
import ast
import json

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]

def load(name):return json.loads((HERE/name).read_text())
def digest(path):return sha256(path.read_bytes()).hexdigest()
def pure_bits(label,atom,q,tail):
    if label=='X':return atom['x']
    if label=='Q':return q
    if label in ['A1','A2','A3','A4','A5','A6']:
        return atom['a'][['A1','A2','A3','A4','A5','A6'].index(label)]
    return tail[['R3','R4','R5','R6'].index(label)]

def query_memberships(label,atom,q,tail):
    if label=='Omean':return [atom['o'],0,0,0,0,0]
    return [pure_bits(label,atom,q,tail)]

def literal_pair_cost(labels,atom,q,tail,D):
    left=query_memberships(labels[0],atom,q,tail)
    right=query_memberships(labels[1],atom,q,tail)
    if labels==['Omean','Omean']:
        pairs=[(left[i],left[j]) for i in range(6) for j in range(6) if i!=j]
    else:pairs=list(product(left,right))
    # f(L)+U(R,L), evaluated directly as legal two-insertion benefits.
    return sum((F(l,D)+F(r,D+l) for l,r in pairs),F(0))/len(pairs)

def literal_row(row,atom,q,tail):
    old=atom['a'];profile=[old[0],q]+tail
    oldload=sum(old);newload=sum(profile)
    f=row['family'];queries=row['queries'];b=F(0);K=F(0)
    def oldpay(j):return F(old[j-1],oldload) if oldload else F(0)
    def mean_safe(label,prefix,remaining):
        bits=query_memberships(label,atom,q,tail)
        return sum((F(bit,prefix+remaining) for bit in bits),F(0))/len(bits)
    if f=='IC_SOURCE2':
        A=F(q,old[0]+1+sum(tail));b=oldpay(2)
    elif f=='CAP':A=F(pure_bits(queries[0],atom,q,tail));K=F(1)
    elif f=='ACTUAL_SAFE':
        j=row['source'];A=mean_safe(queries[0],sum(old[:j-1]),7-j);b=oldpay(j)
    elif f=='MAX':
        A=F(pure_bits(queries[0],atom,q,tail),1+sum(old[:4]))
        b=F(atom['x'],1+sum(old[:4]))
    elif f=='MX':
        A=F(pure_bits(queries[0],atom,q,tail),1+sum(old[:4])+atom['x']);b=oldpay(5)
    elif f=='NEW_SAFE':
        j=row['source'];wallet=F(profile[j-1],newload) if newload else F(0)
        A=mean_safe(queries[0],sum(profile[:j-1]),7-j)-wallet
    elif f=='NEW_PAIR':
        D=1+sum(profile[:4]);y,z=profile[-2:]
        wallet=F(y,D+z)+F(z,D+y)+F(y*y,D*(D+1))
        A=literal_pair_cost(queries,atom,q,tail,D)-wallet
    elif f=='ACTUAL_RC':
        D=1+sum(old[:4]);A=literal_pair_cost(queries,atom,q,tail,D)
        b=oldpay(5)+F(atom['x'],D)
    else:raise AssertionError(f)
    return A,b,K

def main():
    catalog=load('row_catalogue.json');rows=catalog['rows']
    expected={'IC_SOURCE2':1,'CAP':5,'ACTUAL_SAFE':29,'MAX':5,'MX':5,
              'NEW_SAFE':52,'NEW_PAIR':91,'ACTUAL_RC':55}
    assert len(rows)==243 and dict(Counter(r['family'] for r in rows))==expected
    assert [r['index'] for r in rows]==list(range(243))
    assert len({r['name'] for r in rows})==243
    assert all(not r['own_Q_extension'] for r in rows[:235])
    assert all(r['own_Q_extension'] for r in rows[235:])
    new=['Q','R3','R4','R5','R6'];old=[f'A{i}' for i in range(1,7)]+['X','Omean']
    queries=[f'A{i}' for i in range(1,7)]+['X']+new+['Omean']
    pairkey=lambda p:tuple(sorted(p))
    newpairs=[r for r in rows if r['family']=='NEW_PAIR']
    rcpairs=[r for r in rows if r['family']=='ACTUAL_RC']
    assert {pairkey(r['queries']) for r in newpairs}=={pairkey(p) for p in combinations_with_replacement(queries,2)}
    old36={pairkey(p) for p in combinations_with_replacement(old,2)}
    requiredrc={pairkey(p) for p in combinations_with_replacement(new,2)}|{pairkey((x,y)) for x in new for y in old}
    assert {pairkey(r['queries']) for r in rcpairs}==requiredrc
    assert not (requiredrc&old36) and len(old36)==36
    distinct30=[r['name'] for r in rows if r['inner_averaging']=='distinct30_union']
    assert distinct30==['NEW_PAIR|Omean|Omean']
    assert sum('Omean' in r['queries'] for r in rcpairs)==5
    assert sum(r['queries'].count('Omean')==1 for r in newpairs)==12
    assert 'ACTUAL_SAFE_j2|Q' not in {r['name'] for r in rows}
    assert [(r['family'],r.get('source')) for r in rows[235:]]==[
        ('CAP',None),('MAX',None),('MX',None),('ACTUAL_SAFE',1),
        ('ACTUAL_SAFE',3),('ACTUAL_SAFE',4),('ACTUAL_SAFE',5),('ACTUAL_SAFE',6)]
    expected_rhs={
        'IC_SOURCE2':{'u2':'1'},'CAP':{'K':'1'},'MAX':{'F_X':'1'},
        'MX':{'u5':'1'},'ACTUAL_RC':{'u5':'1','F_X':'1'},'NEW_SAFE':{},'NEW_PAIR':{}}
    for r in rows:
        rhs={f'u{r["source"]}':'1'} if r['family']=='ACTUAL_SAFE' else expected_rhs[r['family']]
        assert r['rhs']==rhs,r['name']
    sample_data=load('literal_samples.json');samples=sample_data['states']
    assert len(samples)==sample_data['state_count']==12
    cells=0;zero_checks=0
    for state in samples:
        assert len(state['coefficients'])==243
        for row,out in zip(rows,state['coefficients']):
            assert out['row']==row['name']
            got=tuple(F(out[k]) for k in ['A','b_atom','b_K'])
            want=literal_row(row,state['atom'],state['q'],state['tail'])
            assert got==want,(state['id'],row['name'],got,want)
            cells+=3
            if row['name']=='NEW_SAFE_j6|R6':assert got==(F(0),F(0),F(0));zero_checks+=1

    # True two-player payment identity, with all query/reply bits independent.
    pair_checks=0;rc_checks=0;mx_checks=0
    for D in range(1,6):
        U=lambda x,y:F(x,D+y)
        g=lambda x,y:F(x*y,D*(D+1))
        for c,d,t,q,j in product((0,1),repeat=5):
            H=U(c,d)+U(d,c)+g(c,c)
            gamma1=U(c,d)-U(t,j)
            gamma2=U(j,t)-U(q,t)
            gamma3=U(d,c)-U(j,c)
            extra=g(c,c)-g(c,j)
            assert H-F(t+q,D)+g(t,q)==gamma1+gamma2+gamma3+extra
            assert extra>=0
            pair_checks+=1
        for t,q,j in product((0,1),repeat=3):
            # Coordinates are constant, actual u5, and common F_X.
            paid=(-U(t,j)+U(j,t)-U(q,t)-F(j,D),F(1),F(1))
            target=(-F(t+q,D)+g(t,q),F(1),F(1))
            assert paid==target;rc_checks+=1
        for l,x in product((0,1),repeat=2):
            assert F(l,D)+F(x,D+l)-F(l,D+x)==F(x,D)
            mx_checks+=1

    mean30_checks=0;pure_mean_checks=0
    for D in range(1,6):
        for d in range(7):
            bits=[1]*d+[0]*(6-d);o=int(d>0)
            avg30=sum((F(bits[i],D)+F(bits[j],D+bits[i])
                       for i in range(6) for j in range(6) if i!=j),F(0))/30
            closed=F(d,3*D)-F(d*(d-1),30*D*(D+1))
            assert avg30==closed and avg30>=F(o,3*D)
            if d:
                assert avg30-F(1,3*D)==F((d-1)*(10*(D+1)-d),30*D*(D+1))
            avg36=sum((F(left,D)+F(right,D+left) for left in bits for right in bits),F(0))/36
            assert avg30-avg36==F(d*(6-d),180*D*(D+1))
            mean30_checks+=1
            for l in (0,1):
                average=sum((F(l,D)+F(bit,D+l) for bit in bits),F(0))/6
                weakened=F(l,D)+F(o,6*(D+l))
                assert average>=weakened
                assert weakened==F(l,D)+F(o,6*D)-F(l*o,6*D*(D+1))
                pure_mean_checks+=1

    source2_safe_checks=0
    for a1,q,*tail in product((0,1),repeat=6):
        extra=F(q,a1+1+sum(tail))-F(q,a1+5)
        assert extra>=0;source2_safe_checks+=1
    envelope_checks=0
    for a0,a1,o in product([F(-2),F(-1,3),F(0),F(1,2),F(2)],
                          [F(-2),F(-1,3),F(0),F(1,2),F(2)],(0,1)):
        delta=max(a1-a0,F(0));gamma=max(a0-a1,F(0))
        m=a0+delta*F(o,6)-gamma*o
        vertices=[F(0)] if o==0 else [F(1,6),F(1)]
        assert m==min((1-r)*a0+r*a1 for r in vertices)
        for q in (0,1):
            aq=a0 if q==0 else a1
            for nonnegative_extra in (F(0),F(1,7)):
                W=aq+nonnegative_extra
                residual=W+(gamma-delta)*q-a0
                assert residual==nonnegative_extra>=0
                assert -W+delta*q-gamma*q+residual+a0==0
        assert -delta*F(o,6)+gamma*o-a0==-m
        envelope_checks+=1

    template=load('symbolic_template.json');release=load('main_point_release_template.json')
    assert template['optimizer_calls']==0 and template['matrix_constructed'] is False
    assert all(template[k] is None for k in ['fixed_input','fixed_matrix','fixed_rhs','full8192_matrix','certificate','projection_weights'])
    bound_fields=['point_version','exact_input_path','exact_input_sha256',
        'primal_certificate_path','primal_certificate_sha256','baseline_row_catalogue_path',
        'baseline_row_catalogue_sha256','baseline_old36_actual_RC_version',
        'baseline_Omean_Omean_averaging','common_X_semantics','K','O','all256_masses',
        'positive_support','positive_support_size','phase_I_authorization']
    assert all(release[k] is None for k in bound_fields)
    assert not (HERE/'exact_input.json').exists() and not (HERE/'exact_certificate.json').exists()
    imports={}
    for name in ['symbolic_coefficients.py','build_symbolic_package.py']:
        tree=ast.parse((HERE/name).read_text())
        modules=[]
        for node in ast.walk(tree):
            if isinstance(node,ast.Import):modules.extend(alias.name for alias in node.names)
            elif isinstance(node,ast.ImportFrom):modules.append(node.module)
        allowed={'fractions','itertools','json','collections','hashlib','pathlib','sys','symbolic_coefficients'}
        assert set(modules)<=allowed,(name,modules)
        imports[name]=sorted(set(modules))
    frozen=load('frozen_sources_before.json')['file_sha256']
    changed=[p for p,h in frozen.items() if digest(ROOT/p)!=h]
    assert not changed,changed
    out={
        'status':'PASS_SYMBOLIC_UNBOUND', 'genuine_rows':243,'family_counts':expected,
        'static_sample_states':12,'static_sample_row_evaluations':2916,
        'static_sample_fraction_entries':cells,'zero_terminal_SAFE_samples':zero_checks,
        'pure_PAIR_payment_identities':pair_checks,'RC_free_wallet_identities':rc_checks,
        'MX_RC_mass_identities':mx_checks,'distinct30_exact_menu_tests':mean30_checks,
        'pure_mean_inner6_tests':pure_mean_checks,'source2_Q_SAFE_implication_cases':source2_safe_checks,
        'signed_moment_envelope_cases':envelope_checks,
        'old_RC_pairs_omitted':36,'distinct30_rows':distinct30,
        'point_bound':False,'matrix_constructed':False,'optimizer_calls':0,
        'full8192_state_verification':False,
        'verification_limit':'Exact source identities plus twelve sample states; no fixed-point or full-state certificate exists.',
        'read_only_source_files_checked':len(frozen),'changed_old_files':changed,
        'imports_checked':imports,
        'file_sha256':{p:digest(HERE/p) for p in ['derivation.md','symbolic_coefficients.py',
            'row_catalogue.json','audit_interface.json','symbolic_template.json',
            'main_point_release_template.json','literal_samples.json']}}
    (HERE/'literal_symbolic_check.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k not in ['imports_checked','file_sha256']},indent=2))

if __name__=='__main__':main()
