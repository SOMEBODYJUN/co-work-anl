#!/usr/bin/env python3
"""Independent Fraction source/release audit and optional exact v6 replay.

No builder imports and no optimizer. Every write stays in this new package.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product, combinations_with_replacement
from hashlib import sha256
from math import lcm
import json

HERE=Path(__file__).resolve().parent
WS=HERE.parent
N=257

def read(path):return json.loads(path.read_text())
def sha(path):return sha256(path.read_bytes()).hexdigest()
def save(name,value):(HERE/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
def vec(row):return [F(row.get(str(j),'0')) for j in range(N)]
def dot(a,b):return sum((x*y for x,y in zip(a,b)),F(0))
def share(n,d):
    assert d or not n
    return F(n,d) if d else F(0)
def coeff(row,j):return F(row['a'].get(str(j),'0'))

def minimum(p,n,t,q):
    return F(n+1,2)*t+F(24*t,p+n+1)+F(q,p+1+n*t)

def mean_cost(p,n,t,q,o):
    c=F(n+1,2);D=p+n+1
    if t is not None and q is not None:return minimum(p,n,t,q)
    if t is not None:return c*t+F(24*t,D)+F(o,6*(p+1+n*t))
    if q is not None:return F(q,p+1)+F(o,6)*(c+F(24,D)-F(n*q,(p+1)*D))
    return o*(c/6+F(4,D)+F(1,6*(p+1)))

def requery(bits):
    p,a2,a3,a4,a5,a6,o=bits;b=p+a2
    states30={};states36={}
    for q,r,y,t in product((0,1),repeat=4):
        D=b+q+r+1;menu=(o,0,0,0,0,0)
        pair=sum((F(menu[i]+menu[j],D)-F(menu[i]*menu[j],D*(D+1))
                  for i in range(6) for j in range(6) if i!=j),F(0))/30
        val=F(126000*q,b+1+r+y+t)
        val+=F(43*r+31218*y+34458*t,b+a3+3)
        val+=F(1654*(r+y+t),b+a3+a4+a5+1)
        val+=5400*(F(o,6*(D+y))-F(t,D+y))
        val+=7740*(pair-F(y,D+t)-F(t,D+y)-F(y,D*(D+1)))
        states30[(q,r,y,t)]=val
        states36[(q,r,y,t)]=val-F(215*o,D*(D+1))
    def envelope(costs):
        aq=[min(v for k,v in costs.items() if k[0]==q) for q in (0,1)]
        return aq[0] if not o else min((5*aq[0]+aq[1])/6,aq[1])
    return envelope(states30),envelope(states36)

def root_literal(bits,c36):
    labels=bits[:6];o=bits[6];load=sum(labels);u=[share(q,load) for q in labels]
    out={'ROOT_IC':-u[0],'BRANCH_UNION_OPT':-F(load>0),'ROOT_K_FLOOR':F(0)}
    for j in range(2,7):out[f'CAP_B{j}']=-F(labels[j-1])
    roles=['C','B2','B3','B4','B5','B6','Omean'];queries=list(map(F,labels))+[F(o,6)]
    for j in range(2,7):
        for role,q in zip(roles,queries):out[f'SAFE_j{j}|{role}']=u[j-1]-q/(sum(labels[:j-1])+7-j)
    D=1+sum(labels[:4]);wallet=u[4]+u[5]+F(labels[4],D*(D+1))
    for left,right in combinations_with_replacement(range(7),2):
        overlap=F(o,36) if left==right==6 else queries[left]*queries[right]
        out[f'PAIR|{roles[left]}|{roles[right]}']=wallet-(queries[left]+queries[right])/D+overlap/(D*(D+1))
    out['OPT_SOURCE3_REQUERY_CUT']=c36
    return out

def main():
    inp=read(HERE/'exact_input.json');release=read(HERE/'main_release.json')
    config=read(HERE/'preparation_config.json')
    assert release['authorized_by']=='/root' and release['status']=='MAIN_EXPLICIT_867_ROW_RELEASE'
    assert release['optimizer_calls_authorized']==1
    assert inp['v6_main_release_sha256']==sha(HERE/'main_release.json')
    assert inp['v6_source_sha256']==release['source_sha256']
    for n,h in release['source_sha256'].items():assert sha(WS/n)==h,n
    pins=read(HERE/'prior_frozen_hashes.json')
    for n,h in pins.items():assert sha(WS/n)==h,n
    assert len(pins)==163
    assert sha(WS/config['baseline_input'])==config['baseline_input_sha256']
    assert sha(WS/config['baseline_certificate'])==config['baseline_certificate_sha256']
    baseline=read(WS/config['baseline_input']);oldcert=read(WS/config['baseline_certificate'])
    assert oldcert['input_sha256']==config['baseline_input_sha256']
    assert inp['raw_rows'][:546]==baseline['raw_rows']
    assert len(inp['raw_rows'])==inp['raw_inequality_count']==867
    assert inp['variables']==N and inp['K_column']==256 and inp['nonnegative_columns']==list(range(N))
    for field in ['objective','equality','atom_columns','inequality_convention']:
        assert inp[field]==baseline[field],field
    atoms=inp['atom_columns']
    assert len(atoms)==256
    for j,bits in enumerate(product((0,1),repeat=8)):
        assert atoms[j]=={'index':j,'a':list(bits[:6]),'x':bits[6],'o':bits[7]}
    objective,eq=vec(inp['objective']),vec(inp['equality']['a'])
    assert objective==[F(bool(sum(r['a']))) for r in atoms]+[F(0)]
    assert eq==[F(r['o']) for r in atoms]+[F(0)] and F(inp['equality']['rhs'])==1

    family=read(WS/release['family_path'])
    states=minima=menus=mixed=0
    for i in range(1,6):
        n=6-i
        for p in range(i):
            for t,q in product((0,1),repeat=2):
                values=[]
                for tails in product((0,1),repeat=n):
                    s,z=sum(tails[:-1]),tails[-1]
                    phi=share(25*t-z,p+t+s+z)+F(s,2)+z+F(q,p+t+s+1)
                    values.append(phi);states+=1
                assert min(values)==minimum(p,n,t,q)
                minima+=1
            for menu in product((0,1),repeat=6):
                d,o=sum(menu),int(any(menu));c=F(n+1,2);D=p+n+1
                exact=sum((minimum(p,n,menu[k],menu[l]) for k in range(6) for l in range(6) if k!=l),F(0))/30
                formula=F(d,6)*(c+F(24,D)+F(1,p+1))-F(n*d*(d-1),30*(p+1)*D)
                assert exact==formula and exact>=mean_cost(p,n,None,None,o);menus+=1
                for bit in (0,1):
                    assert sum((minimum(p,n,bit,q) for q in menu),F(0))/6>=mean_cost(p,n,bit,None,o)
                    assert sum((minimum(p,n,t,bit) for t in menu),F(0))/6>=mean_cost(p,n,None,bit,o)
                    mixed+=2
    assert (states,minima,menus,mixed)==(456,60,960,3840)
    assert len(family['rows'])==320 and inp['raw_rows'][546:866]==family['rows']
    oldrows={r['name']:r for r in baseline['raw_rows']}
    for offset,(i,T,Q) in enumerate(product(range(1,6),range(1,9),range(1,9))):
        row=inp['raw_rows'][546+offset];n=6-i;c=F(n+1,2)
        assert (row['source'],row['T'],row['Q'])==(i,T,Q)
        assert row['name']==f'PORTFOLIO25_i{i}_T{T}_Q{Q}'
        assert F(row['rhs'])==0 and F(row['numerical_divisor'])==25
        expect=[];cap=[]
        for atom in atoms:
            a=atom['a'];roles=a+[atom['x']];p=sum(a[:i-1])
            t=roles[T-1] if T<8 else None;q=roles[Q-1] if Q<8 else None
            expect.append(25*share(a[i-1],sum(a))-mean_cost(p,n,t,q,atom['o']))
            cap.append(-F(t) if t is not None else -F(atom['o'],6))
        expect.append(c);cap.append(F(1))
        assert vec(row['a'])==expect,row['name']
        old=vec(oldrows[f'PORTFOLIO31_i{i}_T{T}_Q{Q}']['a'])
        safe=vec(oldrows[f'SAFE_{i}_{T}']['a'])
        assert all(old[j]==expect[j]+6*safe[j]+F(n-1,2)*cap[j] for j in range(N))

    # Rebuild old root72 and both thirty-pair changes from literal payoffs.
    root=read(WS/'maximal_root_tail_wallet_v2/exact_input.json')
    rootcert=read(WS/'maximal_root_tail_wallet_v2/exact_certificate.json')
    parent=read(WS/'main_thirty_index_strengthening/exact_certificate.json')
    newcert=read(WS/'main_root30_capacity_feedback/exact_certificate.json')
    assert newcert['parent_certificate_sha256']==sha(WS/'main_thirty_index_strengthening/exact_certificate.json')
    rrows={r['name']:r for r in root['raw_rows']};assert len(rrows)==72
    cuts30={};cuts36={};values30={}
    for h,bits in enumerate(product((0,1),repeat=7)):
        m30,m36=requery(bits)
        wallet=share(126000*bits[2]+65719*bits[3]+4962*bits[5],sum(bits[:6]))
        cuts30[h]=wallet-m30;cuts36[h]=wallet-m36
        literal=root_literal(bits,cuts36[h]);assert set(literal)==set(rrows)
        for name,value in literal.items():assert coeff(rrows[name],h)==value
        literal['PAIR|Omean|Omean']-=F(bits[6],36*(1+sum(bits[:4]))*(2+sum(bits[:4])))
        literal['OPT_SOURCE3_REQUERY_CUT']=cuts30[h]
        values30[h]=literal
    for name,row in rrows.items():
        assert coeff(row,128)==F(name in ['ROOT_IC','ROOT_K_FLOOR'])
        assert F(row['bK'])==(F(-1) if name.startswith('CAP_') else F(1,6) if name=='ROOT_K_FLOOR' else F(0))
        assert F(row['bO'])==(F(-1) if name=='BRANCH_UNION_OPT' else F(0))
    weights={n:F(w) for n,w in rootcert['dual']['original_unscaled_row_weights'].items()}
    assert all(w>0 for w in weights.values()) and len(weights)==10
    assert weights=={n:F(w) for n,w in parent['root_fixed_weights'].items()}
    pip=F(rootcert['dual']['equality_C_size']);oldpio=F(rootcert['dual']['equality_OPT_union'])
    a=pip+sum(w*F(rrows[n]['bK']) for n,w in weights.items())
    original_b=oldpio+sum(w*F(rrows[n]['bO']) for n,w in weights.items())
    provisional={};oldres={}
    for j in range(129):
        p=F((j>>6)&1) if j<128 else F(0);o=F(j%2) if j<128 else F(0)
        oldres[j]=F(j==128)-sum(w*coeff(rrows[n],j) for n,w in weights.items())-pip*p-oldpio*o
        assert oldres[j]==F(rootcert['dual']['column_residuals'][str(j)])>=0
        if j<128:
            provisional[j]=-sum(w*values30[j][n] for n,w in weights.items())-pip*p-oldpio*o
    eta=min(provisional[h] for h in range(128) if h%2)
    assert eta==F(10132956584,286481466938835)>0
    pio=oldpio+eta;b=original_b+eta
    rho={j:(provisional[j]-eta*(j%2) if j<128 else oldres[j]) for j in range(129)}
    assert all(v>=0 for v in rho.values())
    assert rho=={int(j):F(v) for j,v in parent['root_all129_residuals'].items()}
    assert a==F(parent['root_old_a'])==F(7821007338521,76395057850356)
    assert b==F(parent['root_new_b'])==F(11447284999013,572962933877670)
    assert pip==F(parent['root_equality_multipliers']['K']) and pio==F(parent['root_equality_multipliers']['O'])
    delta=min(rho[h] for h in range(128) if h%2 and not ((h>>5)&1))
    assert delta==F(77334949597,572962933877670)==F(newcert['delta'])>0
    assert [h for h in range(128) if h%2 and not ((h>>5)&1) and rho[h]==delta]==[9]
    newweights=weights.copy();newweights['CAP_B2']+=delta
    newpio=pio+delta;newa=a-delta;newb=b+delta
    assert all(w>0 for w in newweights.values())
    assert newweights=={n:F(w) for n,w in newcert['new_weights'].items()}
    assert newa==F(newcert['new_a'])==F(117160440178621,1145925867755340)
    assert newb==F(newcert['new_b'])==F(23049239897220,1145925867755340)
    assert pip==F(newcert['free_mass_multipliers']['K']) and newpio==F(newcert['free_mass_multipliers']['O'])
    newrho={};classes={(o,y):[] for o,y in product((0,1),repeat=2)}
    for j in range(129):
        p=F((j>>6)&1) if j<128 else F(0);o=F(j%2) if j<128 else F(0)
        residual=F(j==128)-sum(w*(values30[j][n] if j<128 else coeff(rrows[n],j)) for n,w in newweights.items())-pip*p-newpio*o
        target=rho[j]+(delta*(((j>>5)&1)-(j%2)) if j<128 else F(0))
        assert residual==target>=0 and residual==F(newcert['all129_residuals'][str(j)])
        newrho[j]=residual
        if j<128:classes[(j%2,(j>>5)&1)].append(residual)
    # The two parameter columns are genuine free columns, not fixed numbers.
    Kres=-newa+pip+sum(w*F(rrows[n]['bK']) for n,w in newweights.items())
    Ores=-newb+newpio+sum(w*F(rrows[n]['bO']) for n,w in newweights.items())
    assert Kres==Ores==newrho[128]==0
    assert [j for j in range(128) if rho[j]==0]==[0,2,125]
    assert [j for j in range(128) if newrho[j]==0]==[0,2,9,125]
    assert all(len(v)==32 and min(v)>=0 for v in classes.values())
    rootrow=read(WS/release['root_row_path'])
    assert inp['raw_rows'][866]==rootrow==newcert['row']
    expected=[share(r['a'][0],sum(r['a']))-newb*r['o'] for r in atoms]+[-newa]
    assert vec(rootrow['a'])==expected and F(rootrow['rhs'])==0 and F(rootrow['numerical_divisor'])==1
    save('root_feedback_check.json',{'status':'PASS','optimizer_calls':0,'literal_root72_columns':72*129,
        'requery30_literal_states':2048,'old_and_new_free_column_checks':131,'delta':str(delta),
        'old_a':str(a),'old_b':str(b),'new_a':str(newa),'new_b':str(newb),'u_K_O_free_residuals':['0','0','0'],
        'new_weights':{n:str(w) for n,w in newweights.items()},'free_multipliers':{'K':str(pip),'O':str(newpio)},
        'all129_old_residuals':{str(j):str(v) for j,v in rho.items()},'all129_new_residuals':{str(j):str(v) for j,v in newrho.items()},
        'four_class_minima':{f'o{o}_y2{y}':str(min(v)) for (o,y),v in classes.items()},'new_zero_atoms':[0,2,9,125],
        'actual_all257_coefficients_match':True,'source_semantics':'Only the same real CAP_B2 weight increases; O multiplier is free. C is a true size-maximizing legal root label.'})

    seen={};unique=[];mapping=[];zeros=[];duplicates=[]
    for k,row in enumerate(inp['raw_rows']):
        key=(tuple(vec(row['a'])),F(row['rhs']))
        if not any(key[0]) and key[1]==0:
            zeros.append(row['name']);mapping.append({'raw_index':k,'name':row['name'],'status':'zero','unique_index':None})
        elif key in seen:
            first,uid=seen[key];duplicates.append({'name':row['name'],'identical_to':inp['raw_rows'][first]['name']})
            mapping.append({'raw_index':k,'name':row['name'],'status':'duplicate','first_raw_index':first,'unique_index':uid})
        else:
            uid=len(unique);seen[key]=(k,uid);unique.append(row)
            mapping.append({'raw_index':k,'name':row['name'],'status':'kept','unique_index':uid})
    assert unique==inp['unique_rows'] and len(unique)==inp['unique_inequality_count']==798
    assert zeros==inp['removed_zero_rows'] and duplicates==inp['removed_exact_duplicate_rows']
    assert mapping==read(HERE/'duplicate_mapping.json')
    scales=read(HERE/'numerical_scaling.json')['scales']
    assert set(scales)=={r['name'] for r in unique}
    for row in unique:
        s=F(row['numerical_divisor']) if 'numerical_divisor' in row else max([F(1),abs(F(row['rhs']))]+[abs(v) for v in vec(row['a'])])
        assert F(scales[row['name']])==s>0

    oldz=vec(oldcert['primal']);assert all(v>=0 for v in oldz) and dot(eq,oldz)==1
    for row in baseline['raw_rows']:assert dot(vec(row['a']),oldz)-F(row['rhs'])>=0
    row_by_name={row['name']:row for row in unique}
    weights={name:F(v) for name,v in oldcert['dual']['row_weights'].items()}
    nu=F(oldcert['dual']['normalization_multiplier']);assert all(v>=0 for v in weights.values())
    residual=[objective[j]-nu*eq[j]-sum(w*F(row_by_name[name]['a'].get(str(j),'0')) for name,w in weights.items()) for j in range(N)]
    assert all(v>=0 for v in residual) and residual==vec(oldcert['dual']['nonnegative_column_residual'])
    oldbound=nu+sum(w*F(row_by_name[name]['rhs']) for name,w in weights.items())
    assert oldbound==F(oldcert['objective'])==dot(objective,oldz)
    save('baseline_dual_extension.json',{'status':'PASS','objective':str(oldbound),'all257_columns_pass':257,
        'old_positive_weights':{n:str(w) for n,w in weights.items()},'new_row_weights':'all zero',
        'normalization_multiplier':str(nu),'all257_residuals':[str(v) for v in residual]})
    newvalues={r['name']:dot(vec(r['a']),oldz)-F(r['rhs']) for r in inp['raw_rows'][546:]}
    save('old_point_diagnostics.json',{'status':'PASS','optimizer_calls':0,'all321_new_row_values':{n:str(v) for n,v in newvalues.items()},
        'negative_family_rows':sum(v<0 for n,v in newvalues.items() if n.startswith('PORTFOLIO25')),
        'new_root_value':str(newvalues['ROOT30_B2_CAPACITY_FEEDBACK'])})
    source_result={'status':'PASS','optimizer_calls_by_checker':0,'input_sha256':sha(HERE/'exact_input.json'),
        'raw_rows':867,'unique_rows':798,'columns':257,'unchanged_old_raw_rows':546,'unchanged_frozen_files':len(pins),
        'source25_literal_states':states,'source25_minima':minima,'ordered_unequal_menu_cases':menus,'mixed_mean_cases':mixed,
        'family_coefficients_independently_rebuilt':320*257,'full_column_P31_P25_decompositions':320*257,
        'root72_literal_coefficients':72*129,'root_requery30_states':2048,'root_feedback_all_free_columns':131,
        'root_feedback_four_class_nonnegativity':True,'root_actual_columns_checked':257,'root_delta':str(delta),
        'zero_rows':len(zeros),'exact_duplicate_rows':len(duplicates),'all_positive_numerical_scalings':True,
        'old_bound_extended':str(oldbound),'source_sha256':release['source_sha256']}
    save('source_check.json',source_result)
    if not (HERE/'exact_certificate.json').exists():
        print(json.dumps(source_result,indent=2));return

    # Final certificate checks are appended below, independently of recovery.
    cert = read(HERE/'exact_certificate.json')
    assert cert['input_sha256'] == sha(HERE/'exact_input.json') and cert['optimizer_calls'] == 1
    z = vec(cert['primal'])
    assert all(v>=0 for v in z) and dot(eq,z)==1
    rawslack = [dot(vec(row['a']),z)-F(row['rhs']) for row in inp['raw_rows']]
    assert all(v>=0 for v in rawslack)
    assert {row['name']:str(s) for row,s in zip(inp['raw_rows'],rawslack)} == cert['raw_row_slacks']
    W = dot(objective,z)
    assert W == F(cert['objective']) and W >= oldbound and F(cert['K']) == z[256]
    weights = {name:F(v) for name,v in cert['dual']['row_weights'].items()}
    assert all(v>0 for v in weights.values()) and set(weights) <= set(row_by_name)
    nu = F(cert['dual']['normalization_multiplier'])
    residual = [objective[j]-nu*eq[j]-sum(w*F(row_by_name[name]['a'].get(str(j),'0')) for name,w in weights.items()) for j in range(N)]
    assert all(v>=0 for v in residual) and residual == vec(cert['dual']['nonnegative_column_residual'])
    bound = nu+sum(w*F(row_by_name[name]['rhs']) for name,w in weights.items())
    assert bound == W == F(cert['dual']['objective'])
    assert all(residual[j]*z[j]==0 for j in range(N))
    for name,w in weights.items():
        row = row_by_name[name]
        assert w*(dot(vec(row['a']),z)-F(row['rhs'])) == 0
    positive_atom = [j for j in range(256) if z[j]>0]
    positive_residual = [j for j in range(N) if residual[j]>0]
    zero_residual = [j for j in range(N) if not residual[j]]
    tight = [i for i,s in enumerate(rawslack) if not s]
    indices = {'positive_atom_columns':positive_atom,'positive_primal_columns':[j for j in range(N) if z[j]>0],
        'positive_dual_raw_rows':[i for i,row in enumerate(inp['raw_rows']) if row['name'] in weights],
        'tight_raw_row_indices':tight,'tight_raw_row_names':[inp['raw_rows'][i]['name'] for i in tight],
        'zero_column_residual_indices':zero_residual,'positive_column_residual_indices':positive_residual,
        'positive_dual_unique_indices':[i for i,row in enumerate(unique) if row['name'] in weights]}
    save('residual_index.json',indices)
    scale = lcm(W.denominator,nu.denominator,*(w.denominator for w in weights.values()))
    paid = {name:str(scale*w) for name,w in weights.items()}
    scaled_res = [scale*v for v in residual]
    identity = {'scope':'All257 unscaled rational columns; global homogeneous identity uses each rhs times O.',
        'formula':'E W - N O = sum p_i (a_i dot (z,K) - rhs_i O) + sum r_j (z,K)_j',
        'E':str(scale),'N':str(scale*W),'positive_integer_row_payments':paid,
        'normalization_multiplier_scaled':str(scale*nu),
        'all257_scaled_residuals':[str(v) for v in scaled_res],
        'K_residual':str(scaled_res[256]),'all_residuals_nonnegative':True}
    assert all(F(v).denominator==1 for v in paid.values()) and F(identity['N']).denominator==1
    save('global_identity.json',identity)
    with (HERE/'all257_column_checks.tsv').open('w') as f:
        f.write('column\ta1_a6\tx\to\tprimal_mass\texact_dual_residual\tcomplementarity\n')
        for j in range(N):
            r=atoms[j] if j<256 else None
            f.write(f"{j}\t{''.join(map(str,r['a'])) if r else 'K'}\t{r['x'] if r else ''}\t{r['o'] if r else ''}\t{z[j]}\t{residual[j]}\t{z[j]*residual[j]}\n")
    result={'status':'PASS','optimizer_calls_by_checker':0,'input_sha256':sha(HERE/'exact_input.json'),
        'certificate_sha256':sha(HERE/'exact_certificate.json'),'all_raw_rows_checked':867,'all_columns_checked':257,
        'objective':str(W),'objective_decimal':float(W),'half_gap':str(F(1,2)-W),
        'positive_atoms':len(positive_atom),'positive_dual_rows':len(weights),'positive_column_residuals':len(positive_residual),
        'zero_column_residuals':len(zero_residual),'complementarity':True,'exact_duality_gap':'0',
        'K':str(z[256]),'K_residual':str(residual[256]),'source_preflight':'PASS','unchanged_frozen_files':len(pins)}
    save('checker_output.json',result)
    print(json.dumps(result,indent=2))

if __name__=='__main__':
    main()
