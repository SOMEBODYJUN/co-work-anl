#!/usr/bin/env python3
"""Independent standard-library literal reconstruction; no builder import."""
from pathlib import Path
from fractions import Fraction as Q
from itertools import product,combinations_with_replacement
import json,gzip,hashlib

DIR=Path(__file__).resolve().parent
WS=DIR.parent
ZERO=Q(0)
def hashfile(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(name,obj):(DIR/name).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')
def payoff(member,other_load):return Q(1,other_load+1) if member else ZERO
def members(label,atom,tail):
    if label=='Omean':return [atom['o'],0,0,0,0,0]
    if label=='X':return [atom['x']]
    if label[0]=='A':return [atom['a'][int(label[1:])-1]]
    if label[0]=='T':return [tail[int(label[1:])-1]]
    raise AssertionError(label)
def mean_payoff(label,atom,tail,other):
    values=members(label,atom,tail)
    return sum((payoff(q,other) for q in values),ZERO)/len(values)
def pair_query(left,right,atom,tail,background):
    lvals=members(left,atom,tail);rvals=members(right,atom,tail)
    # Literal Cartesian average over actual binary legal-query representatives.
    # For Omean/Omean this explicitly has 36 terms, including repeated indices.
    return sum((payoff(l,background)+payoff(r,background+l) for l in lvals for r in rvals),ZERO)/(len(lvals)*len(rvals))
def literal_A(row,atom,tail):
    a=atom['a'];i=row['source'];x=atom['x'];before=sum(a[:i-1]);actual4=sum(a[:4])
    family=row['family'];queries=row['queries']
    if family=='IC':return payoff(x,before+sum(tail))
    if family=='SAFE':
        j=row['actual_source'];q=members(queries[0],atom,tail)[0]
        return payoff(q,sum(a[:j-1])+6-j)
    if family=='MAX':return mean_payoff(queries[0],atom,tail,actual4)
    if family=='CAP':return Q(members(queries[0],atom,tail)[0])
    if family=='MX':return mean_payoff(queries[0],atom,tail,actual4+x)
    if family=='BR':
        preceding=before+x+sum(tail[:-1])
        return mean_payoff(queries[0],atom,tail,preceding)-payoff(tail[-1],preceding)
    if family=='RC':return pair_query(*queries,atom,tail,actual4)
    if family=='PAIR':
        p=before+x+sum(tail[:-2]);z,t=tail[-2:]
        wallet=payoff(z,p+t)+payoff(t,p+z)+payoff(z,p)-payoff(z,p+z)
        return pair_query(*queries,atom,tail,p)-wallet
    raise AssertionError(family)
def literal_b(row,atom):
    a=atom['a'];total=sum(a)
    actual=lambda j: Q(a[j-1],total) if total else ZERO
    family=row['family']
    if family=='IC':return actual(row['source'])
    if family=='SAFE':return actual(row['actual_source'])
    if family=='MAX':return payoff(atom['x'],sum(a[:4]))
    if family=='MX':return actual(5)
    if family=='RC':return actual(5)+payoff(atom['x'],sum(a[:4]))
    return ZERO
def expected_descriptors():
    out=[]
    for i in range(1,5):
        new=[f'T{j}' for j in range(1,7-i)]
        visible=['A1','A2','A3','A4','A5','A6','X','Omean']
        out.append(('IC',i,(),None))
        for tail in new:
            out.extend(('SAFE',i,(tail,),j) for j in range(1,7))
            out.extend((fam,i,(tail,),None) for fam in ('MAX','CAP','MX'))
        out.extend(('BR',i,(q,),None) for q in visible+new[:-1])
        out.extend(('PAIR',i,qr,None) for qr in combinations_with_replacement(visible+new,2))
        out.extend(('RC',i,qr,None) for qr in combinations_with_replacement(new,2))
        out.extend(('RC',i,(q,r),None) for q in new for r in visible)
    return out
def proof_checks():
    count={'PAIR_three_IC_identity':0,'actual_MX_identity':0,'actual_RC_identity':0,'mean_weakening':0,'SAFE_worst_tail':0}
    for p in range(5):
        f=lambda v:payoff(v,p)
        U=lambda v,w:payoff(v,p+w)
        g=lambda v,w:f(v)-U(v,w)
        for z,t,l,r,j in product((0,1),repeat=5):
            s=U(z,t);w=U(t,z)
            lhs=s+w+g(z,z)-f(l)-f(r)+g(l,r)
            rhs=(s-U(l,j))+(U(j,l)-U(r,l))+(w-U(j,z))+(g(z,z)-g(z,j))
            assert lhs==rhs and g(z,z)-g(z,j)>=0
            count['PAIR_three_IC_identity']+=1
        for z,t,x,q,v in product((0,1),repeat=5):
            u=U(z,t)
            assert u-U(q,x)==(u-U(x,v))+(U(v,x)-U(q,x))+(f(x)-f(v))
            count['actual_MX_identity']+=1
        for z,t,x,q,r,v in product((0,1),repeat=6):
            u=U(z,t)
            assert u+f(x)-f(q)-f(r)+g(q,r)==(u-U(q,v))+(U(v,q)-U(r,q))+(f(x)-f(v))
            count['actual_RC_identity']+=1
    for p in range(6):
        for d in range(7):
            real=[int(j<d) for j in range(6)];o=int(d>0);weak=[o,0,0,0,0,0]
            assert sum(payoff(q,p) for q in real)>=sum(payoff(q,p) for q in weak)
            for q in (0,1):
                strong=sum(payoff(q,p)+payoff(r,p+q) for r in real)/6
                weakened=sum(payoff(q,p)+payoff(r,p+q) for r in weak)/6
                assert strong>=weakened;count['mean_weakening']+=1
            full=sum(payoff(q,p)+payoff(r,p+q) for q in real for r in real)/36
            reduced=sum(payoff(q,p)+payoff(r,p+q) for q in weak for r in weak)/36
            assert full>=reduced
            assert reduced==Q(o,3*(p+1))-Q(o,36*(p+1)*(p+2))
            count['mean_weakening']+=1
    for j in range(1,7):
        for b in range(j):
            for q in (0,1):
                for tail in product((0,1),repeat=6-j):
                    assert payoff(q,b+sum(tail))>=payoff(q,b+6-j)
                    count['SAFE_worst_tail']+=1
    return count
def check_input():
    data=json.loads(gzip.decompress((DIR/'exact_input.json.gz').read_bytes()))
    old_input=WS/'universal_union_wallet_lp/exact_input.json';old_cert=WS/'universal_union_wallet_lp/exact_certificate.json'
    assert hashfile(old_input)==data['point_input_sha256']=='f87a60372dee7449332b17721be6aa70012fb3aca251825cb2e9dd755ff01e41'
    assert hashfile(old_cert)==data['point_certificate_sha256']=='ccc085060427e2999a8e4f00ac3414d7e20a1c6e66aeba8d3e658ae34cb16c85'
    old=json.loads(old_input.read_text());point=json.loads(old_cert.read_text())
    atoms=[]
    for index,bits in enumerate(product((0,1),repeat=8)):
        atoms.append({'index':index,'a':list(bits[:6]),'x':bits[6],'o':bits[7]})
    assert data['all_base_atoms']==old['atom_columns']==atoms
    mass={int(k):Q(v) for k,v in point['primal'].items() if int(k)<256 and Q(v)>0}
    assert data['fixed_positive_mass']=={str(k):str(v) for k,v in mass.items()}
    K=Q(point['K']);assert Q(data['fixed_K'])==K
    assert sum(mass.values())==1 and len(mass)==13
    # Replay all released 217 rows without invoking their old checker or builder.
    vector={int(k):Q(v) for k,v in point['primal'].items()}
    for row in old['raw_rows']:
        slack=sum((Q(v)*vector.get(int(k),ZERO) for k,v in row['a'].items()),ZERO)-Q(row['rhs'])
        assert slack>=0 and str(slack)==point['raw_row_slacks'][row['name']]
    columns=[];equations=[]
    for i in range(1,5):
        for v in sorted(mass):
            positions=[]
            for tail in product((0,1),repeat=6-i):
                positions.append(len(columns));columns.append({'index':len(columns),'source':i,'atom':v,'tail':list(tail)})
            equations.append({'name':f'MASS_i{i}_v{v}','source':i,'atom':v,'a':{str(p):'1' for p in positions},'rhs':str(mass[v])})
    assert columns==data['columns'] and equations==data['equalities']
    assert data['nonnegative_columns']==list(range(780))
    rows=data['inequalities'];expected=expected_descriptors();assert len(rows)==len(expected)==608
    checked=0;rhs_count=0
    for row,(fam,i,queries,j) in zip(rows,expected):
        assert (row['family'],row['source'],tuple(row['queries']),row.get('actual_source'))==(fam,i,queries,j)
        expected_name=f'{fam}_i{i}'+(f'_j{j}' if j else '')+('|'+'|'.join(queries) if queries else '')
        assert row['name']==expected_name
        expected_z={str(v['index']):str(literal_b(row,v)) for v in atoms if literal_b(row,v)}
        assert row['base_z']==expected_z
        expected_K=int(fam=='CAP');assert Q(row['base_K'])==expected_K
        fixed_rhs=sum((literal_b(row,atoms[v])*mass[v] for v in mass),ZERO)+expected_K*K
        assert Q(row['rhs'])==fixed_rhs;rhs_count+=1
        coeffs={}
        for col in columns:
            val=literal_A(row,atoms[col['atom']],col['tail']) if col['source']==i else ZERO
            checked+=1
            if val:coeffs[str(col['index'])]=str(val)
        assert row['a']==coeffs,row['name']
    before=json.loads((DIR/'frozen_sources_before.json').read_text())
    assert all(hashfile(WS/p)==h for p,h in before.items())
    result={'status':'PASS','scope':'Independent standard-library literal coefficient reconstruction, fixed-point replay, and payment identities. No builder import and no optimizer.',
            'input_sha256':hashfile(DIR/'exact_input.json.gz'),'all_256_types_checked':len(atoms),'columns':len(columns),'mass_equations':len(equations),
            'raw_inequalities':len(rows),'matrix_entries_compared_including_zeros':checked,'base_coefficients_compared':len(atoms)*len(rows),
            'fixed_right_sides_compared':rhs_count,'released_raw_rows_replayed':len(old['raw_rows']),'frozen_old_files_unchanged':len(before),
            'proof_checks':proof_checks()}
    save('literal_input_check.json',result);print(json.dumps(result,indent=2))
    return data

def check_certificate(data):
    path=DIR/'exact_certificate.json'
    if not path.exists():return
    cert=json.loads(path.read_text());assert cert['input_sha256']==hashfile(DIR/'exact_input.json.gz')
    assert cert['discovery_sha256']==hashfile(DIR/'discovery_output.json')
    assert cert['status']=='EXACT_INFEASIBLE' and cert['optimizer_calls']==1
    weights={k:Q(v) for k,v in cert['row_weights'].items()}
    assert weights and all(w>0 for w in weights.values())
    rows={r['name']:r for r in data['inequalities']}
    assert set(weights)<=set(rows)
    assert sum(weights.values())==cert['weight_sum']==6763
    chosen=[rows[name] for name in weights]
    atoms=data['all_base_atoms']
    minima_file=DIR/'universal_minima.json.gz';residual_file=DIR/'universal_state_residuals.tsv.gz'
    ucert=cert['universal_cut']
    assert ucert['minima_sha256']==hashfile(minima_file)
    assert ucert['state_residuals_sha256']==hashfile(residual_file)
    saved_minima=json.loads(gzip.decompress(minima_file.read_bytes()))
    saved_residuals=gzip.decompress(residual_file.read_bytes()).decode().splitlines()
    assert saved_residuals[0]=='source\tatom\ttail\tweighted_A\tminimum\tresidual'
    reconstructed=[];minima={};state_count=0;zero_count=0;positive_count=0
    residue_position=1
    for i in range(1,5):
        local=[r for r in chosen if r['source']==i]
        for atom in atoms:
            vals=[]
            for tail in product((0,1),repeat=6-i):
                v=sum((weights[r['name']]*literal_A(r,atom,tail) for r in local),ZERO)
                vals.append((tail,v))
            m=min(v for t,v in vals);minima[i,atom['index']]=m
            reconstructed.append({'source':i,'atom':atom['index'],'minimum':str(m),'minimizing_tail_codes':[k for k,(t,v) in enumerate(vals) if v==m]})
            for tail,val in vals:
                residual=val-m;assert residual>=0
                expected=f'{i}\t{atom["index"]}\t{"".join(map(str,tail))}\t{val}\t{m}\t{residual}'
                assert saved_residuals[residue_position]==expected
                residue_position+=1;state_count+=1
                zero_count+=int(residual==0);positive_count+=int(residual>0)
    assert reconstructed==saved_minima
    assert residue_position==len(saved_residuals) and state_count==15360
    assert ucert['all_types']==256 and ucert['source_type_minima']==len(minima)==1024 and ucert['tail_states']==state_count
    cut={}
    for atom in atoms:
        base=sum((weights[r['name']]*literal_b(r,atom) for r in chosen),ZERO)
        value=base-sum(minima[i,atom['index']] for i in range(1,5))
        cut[str(atom['index'])]=str(value)
    assert cut==ucert['cut_z']
    cut_K=sum(weights[r['name']] for r in chosen if r['family']=='CAP')
    assert cut_K==Q(ucert['cut_K'])==71
    mass={int(k):Q(v) for k,v in data['fixed_positive_mass'].items()};K=Q(data['fixed_K'])
    fixed_minimum=sum((minima[i,v]*weight for i in range(1,5) for v,weight in mass.items()),ZERO)
    fixed_rhs=sum((weights[r['name']]*Q(r['rhs']) for r in chosen),ZERO)
    fixed_C=fixed_rhs-fixed_minimum
    assert fixed_C<0 and fixed_C==Q(cert['fixed_projection_cut_value'])
    assert fixed_rhs==Q(cert['fixed_weighted_rhs']) and fixed_minimum==Q(cert['fixed_weighted_mass_lower_bound'])
    assert fixed_C==sum((Q(cut[str(v)])*weight for v,weight in mass.items()),ZERO)+cut_K*K
    assert cert['fixed_mass_lower_multipliers']=={f'MASS_i{i}_v{v}':str(minima[i,v]) for i in range(1,5) for v in mass}
    residuals={}
    for col in data['columns']:
        A=sum((weights[r['name']]*literal_A(r,atoms[col['atom']],col['tail']) for r in chosen if r['source']==col['source']),ZERO)
        residual=A-minima[col['source'],col['atom']]
        assert residual>=0
        residuals[str(col['index'])]=str(residual)
    assert residuals==cert['fixed_nonnegative_residual_columns']
    assert -fixed_C/sum(weights.values())==Q(cert['normalized_phase_I_lower_bound'])
    sources=sorted(set(rows[n]['source'] for n in weights));assert sources==cert['nonzero_branch_sources']==[4]
    # Check the displayed six-term closed formula separately on every type and
    # every source-4 tail. This is not imported from the generator.
    formula_checks=0
    for atom in atoms:
        a=atom['a'];b=sum(a[:3]);x=atom['x'];theta=Q(atom['o'],6);d=b+x+1;D=sum(a[:4])+1
        for z,t in product((0,1),repeat=2):
            formula=(Q(4096*x,b+1+z+t)+Q(800*z,D)+71*t
                     +384*(theta-t)/(d+z)
                     +512*((a[5]+theta)/d-a[5]*theta/(d*(d+1))-Q(z,d+t)-Q(t,d+z)-Q(z,d*(d+1)))
                     +900*((t+theta)/D-t*theta/(D*(D+1))))
            literal=sum((weights[r['name']]*literal_A(r,atom,(z,t)) for r in chosen),ZERO)
            assert formula==literal;formula_checks+=1
    frozen=json.loads((DIR/'frozen_sources_before.json').read_text())
    assert all(hashfile(WS/p)==h for p,h in frozen.items())
    result={'status':'PASS','conclusion':'Exact infeasibility of the released point; universally valid ALL-256-type projection cut. No half or full-SPE claim.',
            'input_sha256':hashfile(DIR/'exact_input.json.gz'),'certificate_sha256':hashfile(path),
            'positive_integer_row_weights':len(weights),'supported_sources':sources,
            'all_boolean_types':256,'source_type_minima':len(minima),'all_tail_states':state_count,
            'nonnegative_universal_residuals':state_count,'zero_universal_residuals':zero_count,'positive_universal_residuals':positive_count,
            'fixed_nonnegative_residual_columns':len(residuals),'fixed_mass_multipliers':len(cert['fixed_mass_lower_multipliers']),
            'displayed_formula_checks':formula_checks,'cut_value':str(fixed_C),'normalized_phase_I_lower_bound':cert['normalized_phase_I_lower_bound'],
            'frozen_old_files_unchanged':len(frozen),'uses_optimizer':False,'imports_builder':False}
    save('literal_certificate_check.json',result);print(json.dumps(result,indent=2))

if __name__=='__main__':check_certificate(check_input())
