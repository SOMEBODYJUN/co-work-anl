#!/usr/bin/env python3
"""Independent audit of Main CAP4 and the strict universal bound.

Python standard-library rational arithmetic only. No optimizer, no Main builder
import or execution. The literal root payoffs are reconstructed in this file.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product, combinations_with_replacement
from hashlib import sha256
from math import lcm, gcd
import json

HERE=Path(__file__).resolve().parent
WS=HERE.parent
REPO=WS.parents[2]
MAIN=WS/'main_root30_cap4_strict_bound'
N=257

def read(p):return json.loads(p.read_text())
def sha(p):return sha256(p.read_bytes()).hexdigest()
def save(n,x):(HERE/n).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def vec(d):return [F(d.get(str(j),'0')) for j in range(N)]
def dot(a,b):return sum((x*y for x,y in zip(a,b)),F(0))
def share(n,d):
    assert d or not n
    return F(n,d) if d else F(0)
def coeff(r,j):return F(r['a'].get(str(j),'0'))

def requery_envelopes(bits):
    p,a2,a3,a4,a5,a6,o=bits;b=p+a2
    c30={};c36={}
    for q,r,y,t in product((0,1),repeat=4):
        D=b+q+r+1;menu=(o,0,0,0,0,0)
        pair=sum((F(menu[i]+menu[j],D)-F(menu[i]*menu[j],D*(D+1))
                  for i in range(6) for j in range(6) if i!=j),F(0))/30
        value=F(126000*q,b+1+r+y+t)+F(43*r+31218*y+34458*t,b+a3+3)
        value+=F(1654*(r+y+t),b+a3+a4+a5+1)
        value+=5400*(F(o,6*(D+y))-F(t,D+y))
        value+=7740*(pair-F(y,D+t)-F(t,D+y)-F(y,D*(D+1)))
        c30[(q,r,y,t)]=value
        c36[(q,r,y,t)]=value-F(215*o,D*(D+1))
    def envelope(costs):
        lo=[min(v for state,v in costs.items() if state[0]==q) for q in (0,1)]
        return lo[0] if not o else min((5*lo[0]+lo[1])/6,lo[1])
    return envelope(c30),envelope(c36)

def literal_root(bits,cut36):
    labels=bits[:6];o=bits[6];load=sum(labels);u=[share(q,load) for q in labels]
    out={'ROOT_IC':-u[0],'BRANCH_UNION_OPT':-F(load>0),'ROOT_K_FLOOR':F(0)}
    for j in range(2,7):out[f'CAP_B{j}']=-F(labels[j-1])
    roles=['C','B2','B3','B4','B5','B6','Omean'];qs=list(map(F,labels))+[F(o,6)]
    for j in range(2,7):
        for role,q in zip(roles,qs):out[f'SAFE_j{j}|{role}']=u[j-1]-q/(sum(labels[:j-1])+7-j)
    D=1+sum(labels[:4]);wallet=u[4]+u[5]+F(labels[4],D*(D+1))
    for left,right in combinations_with_replacement(range(7),2):
        overlap=F(o,36) if left==right==6 else qs[left]*qs[right]
        out[f'PAIR|{roles[left]}|{roles[right]}']=wallet-(qs[left]+qs[right])/D+overlap/(D*(D+1))
    out['OPT_SOURCE3_REQUERY_CUT']=cut36
    return out

def main():
    pins=read(HERE/'source_pins.json')
    for n,h in pins['workspace_sources'].items():assert sha(WS/n)==h,n
    model=pins['model_definition'];assert sha(REPO/model['path'])==model['sha256']
    oldpins=read(HERE/'prior_frozen_hashes.json')
    assert len(oldpins)==196
    for n,h in oldpins.items():assert sha(WS/n)==h,n
    manifest=read(MAIN/'manifest.json')
    assert manifest['optimizer_calls']==0
    for item in manifest['files']:
        p=MAIN/item['path'];assert sha(p)==item['sha256'] and p.stat().st_size==item['bytes']
    candidate=read(MAIN/'exact_certificate.json')
    parent=read(WS/'main_root30_capacity_feedback/exact_certificate.json')
    assert candidate['optimizer_calls']==0
    assert candidate['parent_certificate_sha256']==sha(WS/'main_root30_capacity_feedback/exact_certificate.json')
    original=read(WS/'maximal_root_tail_wallet_v2/exact_input.json')
    roots={r['name']:r for r in original['raw_rows']};assert len(roots)==72
    pair_cases=0
    for menu in product((0,1),repeat=6):
        d,o=sum(menu),int(any(menu))
        for D in range(1,6):
            exact=sum((F(menu[k]+menu[l],D)-F(menu[k]*menu[l],D*(D+1))
                       for k in range(6) for l in range(6) if k!=l),F(0))/30
            assert exact==F(d,3*D)-F(d*(d-1),30*D*(D+1))>=F(o,3*D)
            pair_cases+=1
    assert pair_cases==320
    real30={};root_states=[]
    for h,bits in enumerate(product((0,1),repeat=7)):
        m30,m36=requery_envelopes(bits)
        wallet=share(126000*bits[2]+65719*bits[3]+4962*bits[5],sum(bits[:6]))
        literal=literal_root(bits,wallet-m36)
        assert set(literal)==set(roots)
        for n,v in literal.items():assert v==coeff(roots[n],h)
        literal['PAIR|Omean|Omean']-=F(bits[6],36*(1+sum(bits[:4]))*(2+sum(bits[:4])))
        literal['OPT_SOURCE3_REQUERY_CUT']=wallet-m30
        real30[h]=literal
    for name,row in roots.items():
        assert coeff(row,128)==F(name in ['ROOT_IC','ROOT_K_FLOOR'])
        assert F(row['bK'])==(F(-1) if name.startswith('CAP_') else F(1,6) if name=='ROOT_K_FLOOR' else F(0))
        assert F(row['bO'])==(F(-1) if name=='BRANCH_UNION_OPT' else F(0))
    weights2={n:F(v) for n,v in parent['new_weights'].items()}
    assert len(weights2)==10 and all(v>0 for v in weights2.values())
    assert 'BRANCH_UNION_OPT' not in weights2
    piK=F(parent['free_mass_multipliers']['K']);piO2=F(parent['free_mass_multipliers']['O'])
    a2,b2=F(parent['new_a']),F(parent['new_b'])
    rho2={}
    for j in range(129):
        p=F((j>>6)&1) if j<128 else F(0);o=F(j%2) if j<128 else F(0)
        r=F(j==128)-sum(w*(real30[j][n] if j<128 else coeff(roots[n],j)) for n,w in weights2.items())-piK*p-piO2*o
        assert r==F(parent['all129_residuals'][str(j)])>=0
        rho2[j]=r
    assert a2==piK+sum(w*F(roots[n]['bK']) for n,w in weights2.items())
    assert b2==piO2+sum(w*F(roots[n]['bO']) for n,w in weights2.items())
    domain=[h for h in range(128) if h%2 and not ((h>>3)&1)]
    assert len(domain)==32
    delta=min(rho2[h] for h in domain)
    assert delta==F(1242901025,57296293387767)==F(candidate['delta'])>0
    attaining=[h for h in domain if rho2[h]==delta]
    assert attaining==candidate['delta_attaining_types']==[17]
    weights4=weights2.copy();weights4['CAP_B4']+=delta
    assert weights4=={n:F(v) for n,v in candidate['new_weights'].items()}
    assert all(v>0 for v in weights4.values())
    piO4=piO2+delta;a4=a2-delta;b4=b2+delta
    assert a4==F(candidate['new_a'])==F(117135582158121,1145925867755340)
    assert b4==F(candidate['new_b'])==F(23074097917720,1145925867755340)
    assert F(candidate['free_mass_multipliers']['K'])==piK
    assert F(candidate['free_mass_multipliers']['O'])==piO4
    rho4={};classes={(o,y4):[] for o,y4 in product((0,1),repeat=2)}
    for j in range(129):
        p=F((j>>6)&1) if j<128 else F(0);o=F(j%2) if j<128 else F(0)
        r=F(j==128)-sum(w*(real30[j][n] if j<128 else coeff(roots[n],j)) for n,w in weights4.items())-piK*p-piO4*o
        expected=rho2[j]+(delta*(((j>>3)&1)-(j%2)) if j<128 else F(0))
        assert r==expected==F(candidate['all129_root_residuals'][str(j)])>=0
        rho4[j]=r
        if j<128:
            classes[(j%2,(j>>3)&1)].append(r)
            root_states.append({'h':j,'bits':list(map(int,format(j,'07b'))),'parent_residual':str(rho2[j]),'new_residual':str(r)})
    Kres=-a4+piK+sum(w*F(roots[n]['bK']) for n,w in weights4.items())
    Ores=-b4+piO4+sum(w*F(roots[n]['bO']) for n,w in weights4.items())
    assert Kres==Ores==rho4[128]==0
    assert all(len(v)==32 and min(v)>=0 for v in classes.values())
    assert [h for h in range(128) if not rho4[h]]==candidate['new_root_zero_types']==[0,2,9,17,125]
    common=lcm(a4.denominator,b4.denominator)
    ints=[common,int(common*a4),int(common*b4)];divisor=gcd(gcd(ints[0],ints[1]),ints[2]);ints=[v//divisor for v in ints]
    assert dict(zip(['u','K','O'],map(str,ints)))==candidate['new_integer_line']
    save('root128_checks.json',{'delta_domain':domain,'delta':str(delta),'attaining':attaining,'all_states':root_states,
        'four_class_minima':{f'o{o}_y4{y}':str(min(v)) for (o,y),v in classes.items()},
        'free_u_K_O_residuals':['0','0','0'],'positive_root_weights':{n:str(v) for n,v in weights4.items()},
        'free_multipliers':{'K':str(piK),'O':str(piO4)}})
    with (HERE/'root131_column_checks.tsv').open('w') as f:
        f.write('column\trole\tparent_residual\tnew_residual\tstatus\n')
        for j in range(129):
            f.write(f'{j}\t{"root_atom" if j<128 else "u"}\t{rho2[j]}\t{rho4[j]}\tPASS\n')
        f.write('129\tK\t0\t0\tPASS\n130\tO\t0\t0\tPASS\n')

    v6=read(WS/'universal_union_wallet_v6/exact_input.json')
    cert=read(WS/'universal_union_wallet_v6/exact_certificate.json')
    assert cert['input_sha256']==sha(WS/'universal_union_wallet_v6/exact_input.json')
    assert v6['variables']==257 and v6['nonnegative_columns']==list(range(257))
    atoms=v6['atom_columns'];assert len(atoms)==256
    for j,bits in enumerate(product((0,1),repeat=8)):
        assert atoms[j]=={'index':j,'a':list(bits[:6]),'x':bits[6],'o':bits[7]}
    row4=read(MAIN/'ROOT30_B2_B4_CAPACITY_FEEDBACK.json')
    assert row4==candidate['new_root_row'] and row4['name']=='ROOT30_B2_B4_CAPACITY_FEEDBACK'
    assert F(row4['rhs'])==0 and F(row4['numerical_divisor'])==1
    newroot=[share(r['a'][0],sum(r['a']))-b4*r['o'] for r in atoms]+[-a4]
    assert newroot==vec(row4['a'])
    cost=vec(v6['objective']);eq=vec(v6['equality']['a'])
    assert cost==[F(bool(sum(r['a']))) for r in atoms]+[F(0)]
    assert eq==[F(r['o']) for r in atoms]+[F(0)]
    original_rows={r['name']:r for r in v6['raw_rows']}

    # Each source's genuine deviation has its own continuation count q.
    physical=[]
    for i in range(1,7):
        for p in range(i):
            for q in range(7-i):
                actual=F(1,p+1+q);safe=F(1,p+7-i)
                assert actual>=safe>=F(1,6)
                physical.append({'source':i,'prefix_load':p,'true_tail_count':q,'IC_to_SAFE_residual':str(actual-safe),'SAFE_to_K6_residual':str(safe-F(1,6))})
    assert len(physical)==56
    clients=[]
    for bits in product((0,1),repeat=6):
        residual=sum((F(1,sum(bits[:i-1])+7-i) for i in range(1,7)),F(0))-1
        assert residual>=0
        clients.append({'actual_bits':list(bits),'residual_on_C':str(residual)})
    assert clients==candidate['W_minus_K_true_SAFE_client_residuals']
    floor_sum=[F(0)]*N
    for i in range(1,7):
        row=original_rows[f'SIZE_FLOOR_{i}']
        expected=[share(r['a'][i-1],sum(r['a'])) for r in atoms]+[-F(1,6)]
        assert vec(row['a'])==expected and F(row['rhs'])==0
        floor_sum=[a+b for a,b in zip(floor_sum,expected)]
    wk=cost.copy();wk[256]-=1
    assert floor_sum==wk
    save('W_minus_K_source_check.json',{'status':'PASS','physical_deviation_cases':physical,'client_residuals':clients,
        'all257_W_minus_K_coefficients':[str(v) for v in wk],
        'six_floor_rows_sum_exactly_to_W_minus_K':True,
        'true_history_note':'Each actual source forces the same legal size-maximal C and follows its own prescribed true continuation; no suffix is frozen or spliced.'})

    oldweights={n:F(v) for n,v in cert['dual']['row_weights'].items()}
    assert len(oldweights)==12 and all(w>0 for w in oldweights.values())
    assert all(F(original_rows[n]['rhs'])==0 for n in oldweights)
    alpha=F(cert['objective']);nu=F(cert['dual']['normalization_multiplier']);assert alpha==nu
    oldres=vec(cert['dual']['nonnegative_column_residual']);assert all(v>=0 for v in oldres)
    for j in range(N):
        assert cost[j]-alpha*eq[j]==sum(w*coeff(original_rows[n],j) for n,w in oldweights.items())+oldres[j]
    oldname='ROOT30_B2_CAPACITY_FEEDBACK';newname=row4['name']
    lam=oldweights[oldname];beta=lam*delta
    assert beta==F(candidate['beta'])==F(candidate['additional_W_minus_K_weight'])>0
    assert alpha==F(candidate['old_alpha6'])
    strict=(alpha+beta)/(1+beta)
    assert strict==F(candidate['strict_alpha'])==F(891124490754754277833367477478333164168,2024943754229983091736619905135906627503)
    assert strict-alpha==F(candidate['strict_gain'])==beta*(1-alpha)/(1+beta)>0
    assert strict<F(1,2)
    assert oldweights=={n:F(w) for n,w in candidate['global_positive_row_weights'].items()}
    assert candidate['global_payment_replaces']=={oldname:newname}
    assert vec(candidate['all257_global_residuals'])==oldres
    newweights_global={newname if n==oldname else n:w for n,w in oldweights.items()}
    normalized_res=[]
    for j in range(N):
        lhs=(1+beta)*cost[j]-(alpha+beta)*eq[j]
        paid=sum(w*(newroot[j] if n==oldname else coeff(original_rows[n],j)) for n,w in oldweights.items())
        assert lhs==paid+oldres[j]+beta*wk[j]
        res=oldres[j]/(1+beta);normalized_res.append(res)
        assert cost[j]-strict*eq[j]==paid/(1+beta)+beta*wk[j]/(1+beta)+res
    # Explicit expansion of W-K into the six existing genuine SIZE_FLOOR rows.
    expanded={n:w/(1+beta) for n,w in newweights_global.items()}
    for i in range(1,7):expanded[f'SIZE_FLOOR_{i}']=beta/(1+beta)
    assert len(expanded)==18 and all(w>0 for w in expanded.values())
    for j in range(N):
        assert cost[j]-strict*eq[j]==sum(w*(newroot[j] if n==newname else coeff(original_rows[n],j)) for n,w in expanded.items())+normalized_res[j]
    point=vec(cert['primal']);assert dot(eq,point)==1
    assert dot(vec(original_rows[oldname]['a']),point)==0
    point_value=dot(newroot,point)
    assert point_value==-delta*(1-point[256])==F(candidate['v6_point_value'])<0
    assert newroot[0]==0
    save('global_audit_certificate.json',{'status':'PASS','optimizer_calls':0,'old_alpha':str(alpha),'lambda_root':str(lam),
        'delta4':str(delta),'beta':str(beta),'strict_alpha':str(strict),'strict_gain':str(strict-alpha),
        'unscaled_identity':'(1+beta)W-(alpha6+beta)O = lambda_root Rcap4 + other11_old_payments + old256_residuals + beta(W-K)',
        'root_replaced_only':{oldname:newname},'positive_composite_payments':{n:str(w) for n,w in newweights_global.items()},
        'W_minus_K_weight':str(beta),'all257_original_residuals':[str(v) for v in oldres],
        'normalized_positive_expanded_weights':{n:str(w) for n,w in expanded.items()},
        'all257_normalized_nonnegative_residuals':[str(v) for v in normalized_res],
        'v6_representative_new_root_value':str(point_value),
        'scope':'A feasible exact universal dual payment, not an optimizer result or a sharpness/SPE realization claim.'})
    with (HERE/'global257_column_checks.tsv').open('w') as f:
        f.write('column\told_residual\tnormalized_residual\tWK_coefficient\tstatus\n')
        for j in range(N):f.write(f'{j}\t{oldres[j]}\t{normalized_res[j]}\t{wk[j]}\tPASS\n')
    result={'status':'PASS_INDEPENDENT_EXACT_SOURCE_AND_GLOBAL_AUDIT','optimizer_calls':0,'main_builder_imported_or_executed':False,
        'main_manifest_sha256':sha(MAIN/'manifest.json'),'main_certificate_sha256':sha(MAIN/'exact_certificate.json'),
        'source_proof_sha256':sha(MAIN/'proof.md'),'source_root_row_sha256':sha(MAIN/'ROOT30_B2_B4_CAPACITY_FEEDBACK.json'),
        'prior_frozen_files_unchanged':len(oldpins),'old_root72_literal_coefficients':72*129,'C30_states_rebuilt':2048,
        'arbitrary_menu_PAIR30_cases':pair_cases,
        'parent_root_free_columns_checked':131,'new_root_free_columns_checked':131,'delta_domain_size':32,'delta4':str(delta),
        'delta_attaining_types':attaining,'root_four_classes_checked':4,'new_root_zero_types':[0,2,9,17,125],
        'visible_root_columns_checked':257,'true_IC_to_SAFE_cases':56,'WK_actual_client_types':64,'WK_existing_floor_columns_checked':257,
        'old_global_columns_checked':257,'new_global_columns_checked':257,'normalized_expanded_columns_checked':257,
        'composite_positive_payments_including_WK':13,'expanded_positive_budgets':18,
        'strict_alpha':str(strict),'strict_alpha_decimal':float(strict),'strict_gain':str(strict-alpha),
        'strict_gain_decimal':float(strict-alpha),'old_and_new_K_residual':'0','no_unpaid_subtraction':True,
        'root_line_valid_for_arbitrary_six_query_union':True,'root_dominance_comparison_requires_O_ge_K':True,
        'OPT_zero_handled_without_division':True,'weak_ties_aliases_and_true_continuations_preserved':True,
        'not_claimed':['half','new optimal LP value','best known global bound','SPE counterexample','root270 result']}
    save('audit_result.json',result)
    print(json.dumps(result,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
