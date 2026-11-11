#!/usr/bin/env python3
"""Independent standard-library binary-share and full Cartesian audit."""
from pathlib import Path
from fractions import Fraction as Q
from itertools import product,combinations_with_replacement
import json,hashlib
H=Path(__file__).resolve().parent;WS=H.parent;ROOT=WS.parents[2];Z=Q(0)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(n,v):(H/n).write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n')
def share(bit,others):return Q(1,others+1) if bit else Z
def query_members(label,h,q,tail):
    bits=h['bits']
    if label=='C':return [bits[0]]
    if label[0]=='B':return [bits[int(label[1:])-1]]
    if label=='Q':return [q]
    if label[0]=='R':return [tail[int(label[1:])-4]]
    if label=='Omean':return [bits[6],0,0,0,0,0]
    raise AssertionError(label)
def mean_query(label,h,q,s,others):
    vals=query_members(label,h,q,s)
    return sum((share(bit,others) for bit in vals),Z)/len(vals)
def pair_query(left,right,h,q,s,others):
    ls=query_members(left,h,q,s);rs=query_members(right,h,q,s)
    return sum((share(l,others)+share(r,others+l) for l in ls for r in rs),Z)/(len(ls)*len(rs))
def literal_A(row,h,q,s):
    old=h['bits'][:6];family=row['family'];new=[old[0],old[1],q,*s]
    if family=='SOURCE_IC':return share(q,old[0]+old[1]+sum(s))
    if family=='CAP':return Q(s[row['tail']-4])
    if family=='OLD_SAFE':
        j=row['source'];return share(s[row['tail']-4],sum(old[:j-1])+6-j)
    if family=='ROOT_SIZE':return Q(s[row['tail']-4],6)
    if family=='NEW_SAFE':
        j=row['source'];return mean_query(row['queries'][0],h,q,s,sum(new[:j-1])+6-j)-share(new[j-1],sum(new)-new[j-1])
    if family=='PAIR':
        bg=sum(new[:4]);y,z=s[1:]
        wallet=share(y,bg+z)+share(z,bg+y)+share(y,bg)-share(y,bg+y)
        return pair_query(*row['queries'],h,q,s,bg)-wallet
    raise AssertionError(family)
def old_payoff(h,j):
    l=h['bits'][:6];return share(l[j-1],sum(l)-l[j-1])
def literal_base(row,h):
    if row['family']=='SOURCE_IC':return old_payoff(h,3)
    if row['family']=='OLD_SAFE':return old_payoff(h,row['source'])
    return Z
def descriptors():
    out=[{'name':'SOURCE3_AVERAGE_IC','family':'SOURCE_IC'}]
    for j in range(4,7):out.append({'name':f'CAP_R{j}','family':'CAP','tail':j})
    for i in range(2,7):
        for j in range(4,7):out.append({'name':f'OLD_SAFE_j{i}|R{j}','family':'OLD_SAFE','source':i,'tail':j})
    for j in range(4,7):out.append({'name':f'ROOT_SIZE_R{j}','family':'ROOT_SIZE','tail':j})
    qs=['C','B2','B3','B4','B5','B6','Q','R4','R5','R6','Omean']
    for i in range(4,7):
        for label in qs:out.append({'name':f'NEW_SAFE_j{i}|{label}','family':'NEW_SAFE','source':i,'queries':[label]})
    for left,right in combinations_with_replacement(qs,2):out.append({'name':f'PAIR|{left}|{right}','family':'PAIR','queries':[left,right]})
    assert len(out)==121;return out
def proof_checks():
    counts={'PAIR_three_true_IC':0,'SAFE_worst_future_patterns':0,'inner_mean_weakening':0,'moment_envelope_checks':0}
    for bg in range(5):
        U=lambda v,w:share(v,bg+w)
        f=lambda v:share(v,bg)
        g=lambda v,w:f(v)-U(v,w)
        for y,z,l,r,j in product((0,1),repeat=5):
            v5=U(y,z);v6=U(z,y)
            assert v5+v6+g(y,y)-f(l)-f(r)+g(l,r)==(v5-U(l,j))+(U(j,l)-U(r,l))+(v6-U(j,y))+(g(y,y)-g(y,j))
            assert g(y,y)-g(y,j)>=0;counts['PAIR_three_true_IC']+=1
    for i in range(2,7):
        for bg in range(i):
            for query in (0,1):
                for rest in product((0,1),repeat=6-i):
                    assert share(query,bg+sum(rest))>=share(query,bg+6-i);counts['SAFE_worst_future_patterns']+=1
    for bg in range(6):
        for multiplicity in range(7):
            strong=[int(k<multiplicity) for k in range(6)];o=int(multiplicity>0);weak=[o,0,0,0,0,0]
            assert sum(share(v,bg) for v in strong)>=sum(share(v,bg) for v in weak);counts['inner_mean_weakening']+=1
            for fixed in (0,1):
                assert sum(share(fixed,bg)+share(v,bg+fixed) for v in strong)>=sum(share(fixed,bg)+share(v,bg+fixed) for v in weak)
                counts['inner_mean_weakening']+=1
            full=sum(share(l,bg)+share(r,bg+l) for l in strong for r in strong)/36
            weakened=sum(share(l,bg)+share(r,bg+l) for l in weak for r in weak)/36
            assert full>=weakened==Q(o,3*(bg+1))-Q(o,36*(bg+1)*(bg+2));counts['inner_mean_weakening']+=1
    # Algebraic envelope identity checked on signs and every allowed menu count.
    for a0,a1,o in product((Q(-2),Q(0),Q(3,2)),(Q(-1),Q(0),Q(4,3)),(0,1)):
        delta=max(a1-a0,Z);gamma=max(a0-a1,Z)
        m=a0+delta*o/6-gamma*o
        expected=a0 if not o else min((5*a0+a1)/6,a1);assert m==expected
        for d in ([0] if not o else range(1,7)):
            assert (1-Q(d,6))*a0+Q(d,6)*a1>=m;counts['moment_envelope_checks']+=1
    return counts
def check_input():
    inp=json.loads((H/'exact_input.json').read_text());oldp=WS/'maximal_root_tail_wallet'
    assert sha(oldp/'exact_input.json')==inp['old_input_sha256']=='3c1a824ed0a17562da812db1d0bb12485f0b1c7f743577af7bc2ecf316d3ab65'
    assert sha(oldp/'exact_certificate.json')==inp['old_certificate_sha256']=='80d9267b6ed9b5e47c4f8ea92523aaf1e73754eb28416e4117f8db754b88d771'
    old=json.loads((oldp/'exact_input.json').read_text());cert=json.loads((oldp/'exact_certificate.json').read_text())
    release=json.loads((WS/'main_maximal_root_tail_check.json').read_text());assert release['status']=='PASS'
    atoms=[{'index':i,'bits':list(bits)} for i,bits in enumerate(product((0,1),repeat=7))]
    assert inp['all_old_atoms']==old['atoms']==atoms
    mass={int(k):Q(v) for k,v in cert['primal'].items() if int(k)<128 and Q(v)>0};u=Q(cert['objective']);K=Q(old['fixed_K'])
    assert inp['fixed_mass']=={str(k):str(v) for k,v in mass.items()} and Q(inp['fixed_u'])==u and Q(inp['fixed_K'])==K
    oldvector={int(k):Q(v) for k,v in cert['primal'].items()}
    for row in old['raw_rows']:
        slack=sum((Q(v)*oldvector.get(int(j),Z) for j,v in row['a'].items()),Z)-Q(row['rhs'])
        assert slack>=0 and str(slack)==cert['raw_row_slacks'][row['name']]
    columns=[];equations=[]
    for atom in sorted(mass):
        positions=[]
        for q in (0,1):
            for tail in product((0,1),repeat=3):
                positions.append(len(columns));columns.append({'index':len(columns),'atom':atom,'q':q,'tail':list(tail)})
        equations.append({'name':f'MASS_h{atom}','atom':atom,'a':{str(j):'1' for j in positions},'rhs':str(mass[atom])})
    assert inp['columns']==columns and inp['equalities']==equations and inp['nonnegative_columns']==list(range(160))
    rows=inp['raw_rows'];assert len(rows)==141 and inp['true_row_count']==121
    expected=descriptors();checks=0;basechecks=0
    for row,desc in zip(rows[:121],expected):
        assert {k:row[k] for k in desc}==desc
        bz={str(a['index']):str(literal_base(row,a)) for a in atoms if literal_base(row,a)}
        assert row['base_z']==bz;basechecks+=128
        bK=int(row['family']=='CAP');bu=int(row['family']=='ROOT_SIZE')
        assert Q(row['base_K'])==bK and Q(row['base_u'])==bu
        rhs=sum((literal_base(row,atoms[h])*m for h,m in mass.items()),Z)+bK*K+bu*u
        assert Q(row['rhs'])==rhs
        aa={}
        for col in columns:
            value=literal_A(row,atoms[col['atom']],col['q'],col['tail']);checks+=1
            if value:aa[str(col['index'])]=str(value)
        assert row['a']==aa,row['name']
    pos=121
    for h in sorted(mass):
        o=atoms[h]['bits'][6]
        for kind,sign,bz in [('Q_LOWER',-1,-Q(o,6)),('Q_UPPER',1,Q(o))]:
            row=rows[pos];pos+=1
            expected={'name':f'{kind}_h{h}','family':kind,'atom':h,'base_z':{str(h):str(bz)} if bz else {},'base_K':'0','base_u':'0','rhs':str(bz*mass[h]),
                      'a':{str(c['index']):str(sign) for c in columns if c['atom']==h and c['q']==1}}
            assert row==expected;checks+=160
    old_v3=sum((old_payoff(atoms[h],3)*m for h,m in mass.items()),Z)
    old_safe3=sum((Q(atoms[h]['bits'][6],6*(sum(atoms[h]['bits'][:2])+4))*m for h,m in mass.items()),Z)
    assert old_v3==old_safe3
    frozen=json.loads((H/'frozen_sources_before.json').read_text());assert all(sha(ROOT/p)==h for p,h in frozen.items())
    rawkeys=[(tuple(sorted(r['a'].items())),tuple(sorted(r['base_z'].items())),r['base_K'],r['base_u']) for r in rows]
    out={'status':'PASS','input_sha256':sha(H/'exact_input.json'),'variables':160,'raw_inequalities':141,'true_budgets':121,'q_moment_bounds':20,'mass_equations':10,
         'all_matrix_entries_compared':checks,'all_old_base_type_coefficients_compared':basechecks,'old_raw_rows_replayed':71,
         'zero_rows_retained':[r['name'] for r in rows if not r['a'] and Q(r['rhs'])==0],
         'affine_duplicates_retained':len(rawkeys)-len(set(rawkeys)),
         'old_SAFE3_Omean_exactly_tight':True,'old_v3':str(old_v3),'proof_checks':proof_checks(),
         'frozen_source_files_unchanged':len(frozen),'uses_optimizer':False,'imports_builder':False}
    save('literal_input_check.json',out);print(json.dumps(out,indent=2));return inp
def check_certificate(inp):
    path=H/'exact_certificate.json'
    if not path.exists():return
    cert=json.loads(path.read_text());assert cert['status']=='EXACT_INFEASIBLE' and cert['optimizer_calls']==1
    assert cert['input_sha256']==sha(H/'exact_input.json') and cert['discovery_sha256']==sha(H/'discovery_output.json')
    rows={r['name']:r for r in inp['raw_rows']};true_names={r['name'] for r in inp['raw_rows'][:121]}
    weights={n:Q(w) for n,w in cert['genuine_row_weights'].items()}
    assert set(weights)<=true_names and all(w>0 for w in weights.values())
    atoms=inp['all_old_atoms'];saved=json.loads((H/'universal_moment_envelope.json').read_text())
    ucert=cert['universal_cut'];assert ucert['envelope_sha256']==sha(H/'universal_moment_envelope.json')
    assert ucert['state_residuals_sha256']==sha(H/'all_2048_state_residuals.tsv')
    lines=(H/'all_2048_state_residuals.tsv').read_text().splitlines()
    assert lines[0]=='atom\tq\ttail\tweighted_A\taq_minimum\tlower_weight\tupper_weight\tresidual'
    envelope=[];env={};cut={};state_count=0;zero_count=0;positive_count=0;formula_count=0;moment_count=0
    for atom in atoms:
        vals={q:[(s,sum((w*literal_A(rows[n],atom,q,s) for n,w in weights.items()),Z)) for s in product((0,1),repeat=3)] for q in (0,1)}
        a0=min(v for s,v in vals[0]);a1=min(v for s,v in vals[1]);lower=max(a1-a0,Z);upper=max(a0-a1,Z);o=atom['bits'][6]
        m=a0 if o==0 else min((5*a0+a1)/6,a1)
        assert m==a0+lower*Q(o,6)-upper*o
        rec={'atom':atom['index'],'a0':str(a0),'a1':str(a1),'lower_weight':str(lower),'upper_weight':str(upper),'minimum':str(m),
             'argmin_q0':[k for k,(s,v) in enumerate(vals[0]) if v==a0], 'argmin_q1':[k for k,(s,v) in enumerate(vals[1]) if v==a1]}
        envelope.append(rec);env[atom['index']]=rec
        for d_opt in ([0] if not o else range(1,7)):
            theta=Q(d_opt,6);assert (1-theta)*a0+theta*a1>=m;moment_count+=1
        p,y2,y3,y4,y5,z,oo=atom['bits'];b=p+y2;oldD4=b+y3+3;oldD6=b+y3+y4+y5+1
        for q in (0,1):
            aq=a0 if q==0 else a1
            for s,value in vals[q]:
                residual=value+(upper-lower)*q-a0;assert residual==value-aq>=0
                state_count+=1;zero_count+=int(residual==0);positive_count+=int(residual>0)
                expected=f'{atom["index"]}\t{q}\t{"".join(map(str,s))}\t{value}\t{aq}\t{lower}\t{upper}\t{residual}'
                assert lines[state_count]==expected
                r,y,t=s;D=b+q+r+1;theta=Q(o,6)
                formula=(Q(126000*q,b+1+r+y+t)+Q(43*r+31218*y+34458*t,oldD4)+Q(1654*(r+y+t),oldD6)
                         +5400*(theta-t)/(D+y)
                         +7740*(Q(o,3*D)-Q(o,36*D*(D+1))-Q(y,D+t)-Q(t,D+y)-Q(y,D*(D+1))))
                assert formula==value;formula_count+=1
        base=sum((w*literal_base(rows[n],atom) for n,w in weights.items()),Z)
        cut[str(atom['index'])]=str(base-m)
    assert saved==envelope and state_count==2048 and len(lines)==2049
    assert cut==ucert['cut_z'] and ucert['all_old_types']==128 and ucert['all_q_tail_states']==2048 and ucert['q_interval']=='[o/6,o]'
    baseK=sum(w*Q(rows[n]['base_K']) for n,w in weights.items());baseu=sum(w*Q(rows[n]['base_u']) for n,w in weights.items())
    assert baseK==Q(ucert['cut_K'])==0 and baseu==Q(ucert['cut_u'])==0
    expected_wallet={f'v{i}':Z for i in range(1,7)};expected_wallet.update(K=baseK,u=baseu)
    for n,w in weights.items():
        row=rows[n]
        if row['family']=='SOURCE_IC':expected_wallet['v3']+=w
        if row['family']=='OLD_SAFE':expected_wallet[f'v{row["source"]}']+=w
    assert cert['wallet_coefficients']=={k:str(v) for k,v in expected_wallet.items()}
    mass={int(k):Q(v) for k,v in inp['fixed_mass'].items()};K=Q(inp['fixed_K']);u=Q(inp['fixed_u'])
    B=sum((w*Q(rows[n]['rhs']) for n,w in weights.items()),Z)
    M=sum((Q(env[h]['minimum'])*v for h,v in mass.items()),Z);C=B-M
    assert C<0 and C==Q(cert['fixed_cut_value']) and B==Q(cert['fixed_weighted_budget_rhs']) and M==Q(cert['fixed_weighted_moment_minimum'])
    assert C==sum((Q(cut[str(h)])*v for h,v in mass.items()),Z)+baseK*K+baseu*u
    assert cert['fixed_extended_q_weights']=={str(h):{'lower':env[h]['lower_weight'],'upper':env[h]['upper_weight']} for h in mass}
    assert cert['fixed_mass_multipliers']=={str(h):env[h]['a0'] for h in mass}
    fixedres={}
    for col in inp['columns']:
        e=env[col['atom']]
        A=sum((w*literal_A(rows[n],atoms[col['atom']],col['q'],col['tail']) for n,w in weights.items()),Z)
        rr=A+(Q(e['upper_weight'])-Q(e['lower_weight']))*col['q']-Q(e['a0']);assert rr>=0
        fixedres[str(col['index'])]=str(rr)
    assert fixedres==cert['fixed_column_residuals']
    N=sum(weights.values())+sum(Q(env[h]['lower_weight'])+Q(env[h]['upper_weight']) for h in mass)
    assert N==Q(cert['extended_certificate_weight_sum']) and -C/N==Q(cert['extended_phase_I_lower_bound'])
    # Independently verify the recovered finite phase-I dual, including the
    # original moment-row weights. Its objective is a lower bound only.
    ph=cert['recovered_phase_dual'];pw={n:Q(v) for n,v in ph['row_weights'].items()};beta={n:Q(v) for n,v in ph['mass_multipliers'].items()}
    assert all(v>=0 for v in pw.values()) and sum(pw.values())==1
    for col in inp['columns']:
        r=sum((v*Q(rows[n]['a'].get(str(col['index']),'0')) for n,v in pw.items()),Z)-beta[f'MASS_h{col["atom"]}']
        assert r>=0 and r==Q(ph['column_residuals'][str(col['index'])])
    lowerbound=sum((beta[e['name']]*Q(e['rhs']) for e in inp['equalities']),Z)-sum((v*Q(rows[n]['rhs']) for n,v in pw.items()),Z)
    assert lowerbound==Q(ph['lower_bound'])>0 and Q(ph['epsilon_residual'])==0
    frozen=json.loads((H/'frozen_sources_before.json').read_text());assert all(sha(ROOT/p)==h for p,h in frozen.items())
    out={'status':'PASS','claim':'Exact fixed-point infeasibility and an all128-type valid moment-envelope cut; no partition, SPE, or sharp-global-root-line claim.',
         'input_sha256':sha(H/'exact_input.json'),'certificate_sha256':sha(path),'positive_genuine_weights':len(weights),
         'all_old_types':128,'all_q_tail_states':state_count,'zero_state_residuals':zero_count,'positive_state_residuals':positive_count,
         'positive_lower_moment_weights':sum(Q(e['lower_weight'])>0 for e in envelope),'positive_upper_moment_weights':sum(Q(e['upper_weight'])>0 for e in envelope),
         'minimum_a1_minus_a0':str(min(Q(e['a1'])-Q(e['a0']) for e in envelope)),
         'menu_multiplicity_envelope_checks':moment_count,'displayed_formula_checks':formula_count,
         'old_cut_atom_columns_checked':128,'old_cut_parameter_columns_checked':2,'fixed_nonnegative_residual_columns':160,
         'cut_value':str(C),'recovered_phase_dual_lower_bound':str(lowerbound),'extended_phase_I_lower_bound':str(-C/N),
         'frozen_old_sources_unchanged':len(frozen),'uses_optimizer':False,'imports_builder':False}
    save('literal_certificate_check.json',out);print(json.dumps(out,indent=2))

if __name__=='__main__':check_certificate(check_input())
