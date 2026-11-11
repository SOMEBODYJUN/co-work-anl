"""Independent Fraction source audit and optional exact v4 certificate check.

No builder or optimizer is imported. Old frozen packages are read-only.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product, combinations_with_replacement
from hashlib import sha256
from math import lcm
import json

HERE=Path(__file__).resolve().parent
WS=HERE.parent
MAIN=WS/'main_thirty_index_strengthening'
EXPECTED={
 'ACTUAL_OPT_REQUERY_30_CUT':'dec77323cc38458881861bde1b982b9da199eb2580b6bd96b41a7374b0842daf',
 'RC_OPT_30':'cc5d278270b8ff14c285d8e57220290184b1954b96799573ad724c89ddb6d35f',
 'SOURCE2_MAXSIZE_31':'6f73c6db9547a35e0201fb88d7cb4f1f51f5b6d718ab8b331a8a3420860e01ee',
 'ROOT_REQUERY_30_FIXED_DUAL':'b0fdab9c9bb2c447884aabc20f31f15f6460ecfcc0ff7f1e905437ab0d9563a4'}


def sha(p):return sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def save(n,v):(HERE/n).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def dot(a,b):return sum((F(v)*F(b.get(str(j),'0')) for j,v in a.items()),F(0))
def share(n,d):return F(n,d) if d else F(0)
def coeff(r,j):return F(r['a'].get(str(j),'0'))


def requery(bits):
    p,a2,a3,a4,a5,a6,o=bits;b=p+a2
    states30={};states36={}
    for q,r,y,t in product((0,1),repeat=4):
        D=b+q+r+1
        # The literal mean below is over the30 ordered unequal indices.
        menu=(o,0,0,0,0,0)
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
        return (aq[0] if not o else min((5*aq[0]+aq[1])/6,aq[1])),aq
    m30,aq=envelope(states30);m36,oldaq=envelope(states36)
    assert m30-m36>=F(43*o,6)
    return m30,m36,aq,states30,states36


def root_literal(bits,c36):
    l=bits[:6];o=bits[6];c=sum(l);u=[share(q,c) for q in l]
    out={'ROOT_IC':-u[0],'BRANCH_UNION_OPT':-F(c>0),'ROOT_K_FLOOR':F(0)}
    for j in range(2,7):out[f'CAP_B{j}']=-F(l[j-1])
    roles=['C','B2','B3','B4','B5','B6','Omean'];qs=list(map(F,l))+[F(o,6)]
    for j in range(2,7):
        for role,q in zip(roles,qs):out[f'SAFE_j{j}|{role}']=u[j-1]-q/(sum(l[:j-1])+7-j)
    D=1+sum(l[:4]);wallet=u[4]+u[5]+F(l[4],D*(D+1))
    for left,right in combinations_with_replacement(range(7),2):
        overlap=F(o,36) if left==right==6 else qs[left]*qs[right]
        out[f'PAIR|{roles[left]}|{roles[right]}']=wallet-(qs[left]+qs[right])/D+overlap/(D*(D+1))
    out['OPT_SOURCE3_REQUERY_CUT']=c36
    return out


def main():
    data=read(HERE/'exact_input.json');base=read(WS/'universal_union_wallet_v3/exact_input.json')
    assert sha(WS/'universal_union_wallet_v3/exact_input.json')=='d5808676b4a59bc9a63deece83e291887ead8847a7177c3afac4221523f30f55'
    assert len(data['raw_rows'])==225 and data['raw_rows'][:221]==base['raw_rows']
    for k in ['variables','K_column','atom_columns','nonnegative_columns','objective','equality']:
        assert data[k]==base[k],k
    assert data['variables']==257 and data['nonnegative_columns']==list(range(257))
    for j,atom in enumerate(data['atom_columns']):
        bits=list(map(int,format(j,'08b')))
        assert atom=={'index':j,'a':bits[:6],'x':bits[6],'o':bits[7]}
    preserved=0
    for file in ['prior_83_frozen_hashes.json','v3_face_frozen_hashes.json']:
        pins=read(HERE/file)
        for n,h in pins.items():assert sha(WS/n)==h,n
        preserved+=len(pins)
    release=read(HERE/'main_release.json')
    assert release['authorized_by']=='/root' and release['optimizer_calls_authorized']==1
    assert sha(HERE/'main_release.json')=='0f58e0a933eb311a13c04b450b6278efa46f178372893cca21b8d10a100edd26'
    for item in release['rows']:
        for art in [item['coefficient_source']]+item['proof_sources']:
            assert sha(WS/art['path'])==art['sha256']
    released={n:read(MAIN/(n+'.json')) for n in EXPECTED}
    for n,h in EXPECTED.items():assert sha(MAIN/(n+'.json'))==h,n
    assert data['raw_rows'][221:]==list(released.values())
    assert all(set(row['a'])=={str(j) for j in range(257)} for row in released.values())

    pair_count=0
    for menu in product((0,1),repeat=6):
        d=sum(menu);o=int(d>0)
        for D in range(1,6):
            mean=sum((F(menu[i]+menu[j],D)-F(menu[i]*menu[j],D*(D+1))
                      for i in range(6) for j in range(6) if i!=j),F(0))/30
            formula=F(d,3*D)-F(d*(d-1),30*D*(D+1))
            assert mean==formula>=F(o,3*D)
            assert formula-(F(d,3*D)-F(d*d,36*D*(D+1)))==F(d*(6-d),180*D*(D+1))>=0
            pair_count+=1
    main_envelopes=read(MAIN/'requery30_envelopes.json');main_states=read(MAIN/'requery30_states.json')
    m30={};m36={};c30={};c36={};pos=zero=count=0
    for h,bits in enumerate(product((0,1),repeat=7)):
        mm,oldmm,aq,states,oldstates=requery(bits);m30[h]=mm;m36[h]=oldmm
        wallet=share(126000*bits[2]+65719*bits[3]+4962*bits[5],sum(bits[:6]))
        c30[h]=wallet-mm;c36[h]=wallet-oldmm
        delta=max(aq[1]-aq[0],F(0));gamma=max(aq[0]-aq[1],F(0));assert delta>0 and gamma==0
        env=main_envelopes[h]
        assert F(env['a0'])==aq[0] and F(env['a1'])==aq[1] and F(env['m30'])==mm and F(env['m36'])==oldmm
        for state,val in states.items():
            rho=val+(gamma-delta)*state[0]-aq[0];assert rho>=0
            source=main_states[count]
            assert source['h']==h and source['state']==list(state)
            assert F(source['cost'])==val and F(source['old36_cost'])==oldstates[state] and F(source['residual'])==rho
            pos+=rho>0;zero+=rho==0;count+=1
    assert count==2048 and pair_count==320
    s2_count=0
    for a,t,q in product((0,1),repeat=3):
        minimum=4*t+F(30*t,a+5)+F(q,a+1+4*t);vals=[]
        for d3,d4,d5,z in product((0,1),repeat=4):
            s=d3+d4+d5;v=share(31*t-z,a+t+s+z)+s+z+F(q,a+t+s+1)
            assert v>=minimum;vals.append(v);s2_count+=1
        assert min(vals)==minimum

    root=read(WS/'maximal_root_tail_wallet_v2/exact_input.json');rc=read(WS/'maximal_root_tail_wallet_v2/exact_certificate.json')
    assert sha(WS/'maximal_root_tail_wallet_v2/exact_input.json')=='86a235bf210862ef8f8bbbdea7ac324e71f691a8aa7af455a821e6379cfe117d'
    assert sha(WS/'maximal_root_tail_wallet_v2/exact_certificate.json')=='8b38a322e3b6ddffefee25d3db157e3fbbddb284a4b636143360bd00d4db5b46'
    rrows={r['name']:r for r in root['raw_rows']};assert len(rrows)==72
    literals={}
    for h,bits in enumerate(product((0,1),repeat=7)):
        literals[h]=root_literal(bits,c36[h]);assert set(literals[h])==set(rrows)
        for n,v in literals[h].items():assert v==coeff(rrows[n],h)
    for n,row in rrows.items():
        assert coeff(row,128)==F(n in ['ROOT_IC','ROOT_K_FLOOR'])
        expectedK=F(-1) if n.startswith('CAP_') else F(1,6) if n=='ROOT_K_FLOOR' else F(0)
        expectedO=F(-1) if n=='BRANCH_UNION_OPT' else F(0)
        assert F(row['bK'])==expectedK and F(row['bO'])==expectedO
    lam={n:F(q) for n,q in rc['dual']['original_unscaled_row_weights'].items()};assert all(q>=0 for q in lam.values())
    pip,pio=F(rc['dual']['equality_C_size']),F(rc['dual']['equality_OPT_union'])
    a=pip+sum(v*F(rrows[n]['bK']) for n,v in lam.items())
    oldb=pio+sum(v*F(rrows[n]['bO']) for n,v in lam.items())
    oldrho={};shift={}
    for j in range(129):
        p=F(int(format(j,'07b')[0])) if j<128 else F(0);o=F(j%2) if j<128 else F(0)
        res=F(j==128)-sum(v*coeff(rrows[n],j) for n,v in lam.items())-pip*p-pio*o
        assert res==F(rc['dual']['column_residuals'][str(j)])>=0;oldrho[j]=res
        if j<128:
            bits=list(map(int,format(j,'07b')));D=1+sum(bits[:4])
            shift[j]=res+lam['PAIR|Omean|Omean']*F(bits[6],36*D*(D+1))+lam['OPT_SOURCE3_REQUERY_CUT']*(m30[j]-m36[j])
    eta=min(shift[h] for h in range(128) if h%2);newb=oldb+eta
    assert eta==F(10132956584,286481466938835)>0
    assert a==F(7821007338521,76395057850356) and newb==F(11447284999013,572962933877670)
    for j in range(129):
        p=F(int(format(j,'07b')[0])) if j<128 else F(0);o=F(j%2) if j<128 else F(0)
        weighted=F(0)
        for n,v in lam.items():
            col=coeff(rrows[n],j)
            if j<128 and n=='PAIR|Omean|Omean':
                bits=list(map(int,format(j,'07b')));D=1+sum(bits[:4]);col-=F(bits[6],36*D*(D+1))
            if j<128 and n=='OPT_SOURCE3_REQUERY_CUT':col=c30[j]
            weighted+=v*col
        res=F(j==128)-weighted-pip*p-(pio+eta)*o
        assert res==(shift[j]-eta*o if j<128 else oldrho[j])>=0
    assert a==pip+sum(v*F(rrows[n]['bK']) for n,v in lam.items())
    assert newb==pio+eta+sum(v*F(rrows[n]['bO']) for n,v in lam.items())
    maincert=read(MAIN/'exact_certificate.json')
    assert F(maincert['root_old_a'])==a and F(maincert['root_new_b'])==newb

    for j,atom in enumerate(data['atom_columns']):
        aa=atom['a'];x=atom['x'];o=atom['o'];c=sum(aa);P=sum(aa[:4]);h=int(''.join(map(str,aa+[o])),2)
        expected={
          'ACTUAL_OPT_REQUERY_30_CUT':c30[h],
          'RC_OPT_30':share(aa[4],c)+F(x,P+1)-F(o,3*(P+1)),
          'SOURCE2_MAXSIZE_31':share(31*aa[1],c)-4*aa[5]-F(30*aa[5],aa[0]+5)-F(x,aa[0]+1+4*aa[5]),
          'ROOT_REQUERY_30_FIXED_DUAL':share(aa[0],c)-newb*o}
        for n,v in expected.items():assert coeff(released[n],j)==v
    for n,k in [('ACTUAL_OPT_REQUERY_30_CUT',F(0)),('RC_OPT_30',F(0)),('SOURCE2_MAXSIZE_31',F(4)),('ROOT_REQUERY_30_FIXED_DUAL',-a)]:
        assert coeff(released[n],256)==k
    unique=[];seen=set()
    for row in data['raw_rows']:
        key=(tuple(coeff(row,j) for j in range(257)),F(row['rhs']))
        if not any(key[0]) and key[1]==0:continue
        if key not in seen:unique.append(row);seen.add(key)
    assert unique==data['unique_rows'] and len(unique)==213
    scales=read(HERE/'numerical_scaling.json')['scales']
    for row in unique:
        s=F(row['numerical_divisor']) if 'numerical_divisor' in row else max([F(1),abs(F(row['rhs']))]+[abs(F(v)) for v in row['a'].values()])
        assert F(scales[row['name']])==s>0

    strict=read(WS/'v3_optimum_joint_face/strict_dual_certificate.json');bnd=F(strict['new_bound'])
    weights={n:F(v) for n,v in strict['old_row_weights'].items() if F(v)}
    weights['ACTUAL_OPT_REQUERY_30_CUT']=F(strict['ACTUAL_OPT_REQUERY_CUT_weight'])
    by={r['name']:r for r in data['raw_rows']};baseline_res={}
    for j in range(257):
        oldG=F(strict['new_cut_all257_coefficients'][str(j)]);newG=coeff(released['ACTUAL_OPT_REQUERY_30_CUT'],j)
        assert oldG-newG>=0
        res=F(strict['all257_nonnegative_column_residuals'][str(j)])+weights['ACTUAL_OPT_REQUERY_30_CUT']*(oldG-newG)
        assert res>=0
        assert F(data['objective'].get(str(j),'0'))-bnd*F(data['equality']['a'].get(str(j),'0'))==sum(w*coeff(by[n],j) for n,w in weights.items())+res
        baseline_res[str(j)]=str(res)
    save('baseline_dual_extension.json',{'objective':str(bnd),'row_weights':{n:str(v) for n,v in weights.items()},'normalization_multiplier':str(bnd),'all257_residuals':baseline_res,'reason':'C36=C30+nonnegative all-type envelope improvement; old strict dual therefore extends.'})
    face=read(WS/'v3_optimum_joint_face/face_certificate.json');diagnostics={}
    for n,row in released.items():
        val=dot(row['a'],face['constant']);dt=dot(row['a'],face['t_direction']);ds=dot(row['a'],face['sigma_direction'])
        assert val<0 and dt==ds==0
        diagnostics[n]={'whole_v3_face_value':str(val),'decimal':float(val),'t_direction':'0','sigma_direction':'0'}
    save('old_face_diagnostics.json',diagnostics)
    report={'status':'PASS','optimizer_calls_in_checker':0,'input_sha256':sha(HERE/'exact_input.json'),
      'base221_rows_identical':True,'base_coefficient_checks':221*257,'full256_types':True,'columns':257,'raw_rows':225,'unique_rows':213,
      'new_row_coefficient_checks':4*257,'pair30_states':pair_count,'C30_states':count,'C30_envelopes':128,
      'C30_positive_residuals':pos,'C30_zero_residuals':zero,'source2_states':s2_count,
      'root72_literal_coefficients':72*129,'root_old_and_new_free_columns_checked':131,
      'root_K_coefficient':str(-a),'root_O_coefficient':str(-newb),'root_eta':str(eta),
      'baseline_bound':str(bnd),'baseline_all257_nonnegative':True,'previous_frozen_files_unchanged':preserved,
      'all_scaling_strictly_positive':True,'four_row_sha256':EXPECTED}
    save('source_check.json',report)

    cp=HERE/'exact_certificate.json'
    if cp.exists():
        cert=read(cp);assert cert['input_sha256']==sha(HERE/'exact_input.json')
        z={str(j):F(cert['primal'].get(str(j),'0')) for j in range(257)};assert all(v>=0 for v in z.values())
        assert dot(data['equality']['a'],z)==F(data['equality']['rhs'])==1
        slacks={r['name']:dot(r['a'],z)-F(r['rhs']) for r in data['raw_rows']};assert all(v>=0 for v in slacks.values())
        assert all(F(cert['raw_row_slacks'][n])==v for n,v in slacks.items())
        W=dot(data['objective'],z);assert W==F(cert['objective'])
        yy={n:F(v) for n,v in cert['dual']['row_weights'].items()};nu=F(cert['dual']['normalization_multiplier'])
        assert all(v>=0 for v in yy.values())
        residual={}
        for j in range(257):
            v=F(data['objective'].get(str(j),'0'))-nu*F(data['equality']['a'].get(str(j),'0'))-sum(w*coeff(by[n],j) for n,w in yy.items())
            assert v==F(cert['dual']['nonnegative_column_residual'].get(str(j),'0'))>=0
            assert v*z[str(j)]==0;residual[j]=v
        assert nu+sum(v*F(by[n]['rhs']) for n,v in yy.items())==W
        assert all(yy[n]*slacks[n]==0 for n in yy)
        scale=lcm(W.denominator,nu.denominator,*(v.denominator for v in yy.values()))
        save('global_identity.json',{'scale':str(scale),'objective_numerator':str(W*scale),'normalization_numerator':str(nu*scale),
          'integer_budget_weights':{n:str(v*scale) for n,v in yy.items()},'all257_scaled_residuals':{str(j):str(v*scale) for j,v in residual.items()}})
        save('residual_index.json',{'zero_dual_columns':[j for j,v in residual.items() if v==0],'positive_dual_columns':[j for j,v in residual.items() if v>0],
          'all257_dual_residuals':{str(j):str(v) for j,v in residual.items()},
          'raw_rows':[{'index':i,'name':r['name'],'slack':str(slacks[r['name']]),'tight':slacks[r['name']]==0} for i,r in enumerate(data['raw_rows'])]})
        report.update({'status':'PASS_EXACT_PRIMAL_DUAL','objective':str(W),'objective_decimal':float(W),
          'all225_primal_rows_pass':True,'all257_dual_columns_pass':True,'matching_objectives':True,
          'positive_primal_atoms':sum(z[str(j)]>0 for j in range(256)),'positive_dual_budgets':sum(v>0 for v in yy.values()),
          'zero_dual_columns':[j for j,v in residual.items() if v==0]})
        diagnostic_path=HERE/'point_diagnostics.json'
        if diagnostic_path.exists():
            diagnostics=read(diagnostic_path)
            assert diagnostics['input_sha256']==sha(HERE/'exact_input.json')
            assert diagnostics['certificate_sha256']==sha(cp)
            bg=diagnostics['background_projection']
            assert len(bg['all257_coefficients'])==257
            assert dot(bg['all257_coefficients'],z)==F(bg['value'])
            candidate=diagnostics['source2_T_A5_Q_X']
            for j in range(256):
                aa=list(map(int,format(j,'08b')));c=sum(aa[:6]);T=aa[4]
                expected=share(31*aa[1],c)-4*T-F(30*T,aa[0]+5)-F(aa[6],aa[0]+1+4*T)
                assert F(candidate['all257_coefficients'][str(j)])==expected
            assert F(candidate['all257_coefficients']['256'])==4
            assert dot(candidate['all257_coefficients'],z)==F(candidate['value'])<0
            report['post_recovery_diagnostics_checked']=True
            report['background_candidate_value']=bg['value']
            report['source2_A5_X_candidate_value']=candidate['value']
        save('checker_output.json',report)
    print(json.dumps(report,ensure_ascii=False,indent=2))


if __name__=='__main__':main()
