"""Main: independent full1586 primal/dual, full face, real C budgets, six new cuts."""
from pathlib import Path
from fractions import Fraction as F
from hashlib import sha256
from itertools import product
import json
import sympy as sp

W=Path(__file__).resolve().parent
P=W/'visible_maximum_joint_v4_solve'
def load(p): return json.loads(p.read_text())
def sh(p): return sha256(p.read_bytes()).hexdigest()
def dot(a,z): return sum((F(v)*z[int(k)] for k,v in a.items()),F(0))

def main():
    out=W/'main_visible_c_v4_certificate_check.json'
    assert not out.exists()
    ip=W/'visible_maximum_joint_v4/exact_input.json'
    cp=P/'exact_certificate.json'
    assert sh(ip)=='fbd3b0cb65736b5c41b64dd630b442e9647b701e446c36819e3f726c620ac839'
    assert sh(cp)=='6049aba7ddb134159f95adea1f3bc6470bdfcb902a111e702e52b9b6f3cec34b'
    inp,cert,face=load(ip),load(cp),load(P/'optimal_face.json')
    rows,eqs=inp['raw_rows'],inp['equalities']
    z=list(map(F,cert['primal']))
    y=list(map(F,cert['dual']['raw_row_weights']))
    eta=list(map(F,cert['dual']['equality_multipliers']))
    residual=list(map(F,cert['dual']['nonnegative_column_residual']))
    assert len(rows)==len(y)==1586 and len(z)==len(residual)==513 and len(eqs)==len(eta)==2
    assert min(z)>=0 and min(y)>=0 and min(residual)>=0
    slacks=[]
    for k,r in enumerate(rows):
        slack=dot(r['a'],z)-F(r['rhs']);slacks.append(slack)
        assert slack==F(cert['raw_row_slacks'][k])>=0 and slack*y[k]==0
    for eq in eqs: assert dot(eq['a'],z)==F(eq['rhs'])
    positive=[i for i,v in enumerate(y) if v]
    assert positive==[46,47,134,218,221,222,868,1018,1433,1438,1439]
    for h in range(513):
        v=F(inp['objective'].get(str(h),'0'))
        v-=sum((y[k]*F(rows[k]['a'].get(str(h),'0')) for k in positive),F(0))
        v-=sum((w*F(eq['a'].get(str(h),'0')) for w,eq in zip(eta,eqs)),F(0))
        assert v==residual[h] and v*z[h]==0
    alpha=dot(inp['objective'],z)
    dual=sum((y[k]*F(rows[k]['rhs']) for k in positive),F(0))+sum((w*F(eq['rhs']) for w,eq in zip(eta,eqs)),F(0))
    assert alpha==dual==F(cert['objective'])
    zero=[h for h,r in enumerate(residual) if not r]
    assert zero==face['zero_residual_columns'] and len(zero)==20
    equations=eqs+[rows[k] for k in positive]
    E=[[F(r['a'].get(str(h),'0')) for h in zero] for r in equations]
    rhs=[F(r['rhs']) for r in equations]
    assert sp.Matrix(E).rank()==13
    coords={r['column']:[F(r['constant'])]+list(map(F,r['parameter_coefficients'])) for r in face['coordinates']}
    assert sorted(coords)==zero
    for k in range(8):
        for er,target in zip(E,rhs):
            assert sum((v*coords[h][k] for v,h in zip(er,zero)),F(0))==(target if k==0 else 0)
    assert sp.Matrix([[coords[h][k] for k in range(1,8)] for h in zero]).rank()==7
    assert len(face['all1586_raw_inequality_restrictions'])==1586
    for row,rec in zip(rows,face['all1586_raw_inequality_restrictions']):
        values=[sum((F(row['a'].get(str(h),'0'))*coords[h][k] for h in zero),F(0))-(F(row['rhs']) if k==0 else 0) for k in range(8)]
        assert values==[F(rec['constant'])]+list(map(F,rec['parameter_coefficients']))
    functionals={}
    atoms=list(product((0,1),repeat=9))
    for h in range(513):
        if h==512:
            K=F(1);u2=A1=cOut=oOut=F(0);N={j:F(0) for j in range(3,6)}
        else:
            bits=atoms[h];actual=bits[:6];p,c,o=actual[0],bits[8],bits[7]
            K=F(0);u2=F(actual[1],sum(actual)) if sum(actual) else F(0)
            A1=F(actual[0]);cOut=F(c*(1-o));oOut=F(o*(1-c))
            N={j:F(o,6*(p+(j-2)*c+7-j)) for j in range(3,6)}
        vals={'K':K,'u2_minus_K_over5':u2-K/5,'size_A1':A1,'C_outside_O_mass':cOut,'O_outside_C_mass':oOut,
              **{f'K_over5_minus_N{j}':K/5-N[j] for j in range(3,6)},'N5_minus_N3':N[5]-N[3]}
        for k in [868,927,1002,1433,1441,1018]: vals[f'raw_slack_{k}']=F(rows[k]['a'].get(str(h),'0'))
        for name,value in vals.items(): functionals.setdefault(name,[]).append(value)
    fixed={}
    for rec in load(P/'true_branch_face_functionals.json')['functionals']:
        name=rec['name'];target=functionals[name]
        assert all(F(rec['functional'].get(str(h),'0'))==target[h] for h in range(513))
        weights=list(map(F,rec['signed_face_equation_weights']))
        extra={int(k):F(v) for k,v in rec['signed_forced_zero_column_weights'].items()}
        assert all(h not in zero for h in extra)
        for h in range(513):
            assert target[h]==sum((w*F(r['a'].get(str(h),'0')) for w,r in zip(weights,equations)),F(0))+extra.get(h,F(0))
        val=sum((v*w for v,w in zip(rhs,weights)),F(0))-F(rec['subtracted_rhs'])
        assert val==F(rec['value'])
        assert all(sum((target[h]*coords[h][k] for h in zero),F(0))==0 for k in range(1,8))
        fixed[name]=str(val)
    assert F(fixed['u2_minus_K_over5'])==0
    assert all(F(fixed[f'K_over5_minus_N{j}'])<0 for j in range(3,6))
    assert F(fixed['C_outside_O_mass'])==0 and F(fixed['O_outside_C_mass'])==1-F(fixed['K'])>0
    for h in range(513):
        ec=F(eqs[1]['a'].get(str(h),'0'))
        assert F(rows[1441]['a'].get(str(h),'0'))==F(rows[1018]['a'].get(str(h),'0'))-F(7,10)*ec
        assert functionals['u2_minus_K_over5'][h]==(F(rows[1433]['a'].get(str(h),'0'))-F(rows[1018]['a'].get(str(h),'0')))/9+F(5,18)*ec
    # Reconstruct both complete nonnegative true branch wallets before using equality.
    theta=(F(12425,31104),F(175,432),F(5,12))
    zeros={};physical=0
    for s in [0,9]:
        a=25+sum(theta)-s
        for p,c,o in product((0,1),repeat=3):
            anchor=F(5*c,2)+F(24*c,p+5)-F(s*c,5)+F(o,6*(p+4*c+1))
            anchor+=sum(theta[j-3]*F(o,6*(p+(j-2)*c+7-j)) for j in range(3,6))
            good=[]
            for tail in product((0,1),repeat=4):
                L=p+c+sum(tail)
                cost=(a*c-tail[3]-sum(theta[k]*tail[k] for k in range(3)))/L if L else F(0)
                cost+=F(sum(tail[:3]),2)+tail[3]+F(o,6*(p+c+sum(tail[:3])+1))
                cost+=sum(theta[j-3]*F(o,6*(p+c+sum(tail[:j-3])+7-j)) for j in range(3,6))
                assert cost>=anchor;physical+=1
                if cost==anchor: good.append(tail)
            assert good;zeros[(s,p,c,o)]=set(good)
    common=[]
    for p,c,o in product((0,1),repeat=3):
        tails=sorted(zeros[(0,p,c,o)]&zeros[(9,p,c,o)])
        assert tails
        for t in tails:
            L=p+c+sum(t);share=F(c,L) if L else F(0)
            assert share==F(c,5)
            if c: assert t[:3]==(1,1,1)
        common.append({'pco':[p,c,o],'all_common_zero_tails':list(map(list,tails))})
    assert len(zeros[(9,0,1,0)])==2 and len(zeros[(0,1,1,0)])==2
    assert len(zeros[(9,0,0,1)])==5
    assert sum(len(r['all_common_zero_tails']) for r in common)==13
    # Six new rows are already independently paid by new CAP/SAFE weights.
    seed=load(W/'main_cap_coupled_safe_seed/check_result.json')
    assert seed['status']=='DIRECT_REAL_BUDGET_ENDPOINTS_PASS'
    cuts=[]
    for r in load(W/'main_cap_coupled_safe_seed/exact_rows.json'):
        values=[sum((F(r['a'].get(str(h),'0'))*coords[h][k] for h in zero),F(0)) for k in range(8)]
        assert all(v==0 for v in values[1:]) and values[0]<0
        assert values[0]==F(r['increment'])*F(fixed[f"K_over5_minus_N{r['increment_source']}"])
        cuts.append({'name':r['name'],'whole_face_value':str(values[0]),'decimal':float(values[0])})
    result={'status':'PASS_MAIN_FULL1586_RAW513_DUAL_FULL_FACE_TRUE_BRANCH_AND_SIX_UNIVERSAL_CUTS',
       'optimizer_calls':0,'input_sha256':sh(ip),'certificate_sha256':sh(cp),'face_sha256':sh(P/'optimal_face.json'),
       'raw_rows':1586,'nonnegative_columns':513,'equalities':2,'alpha':str(alpha),'alpha_decimal':float(alpha),
       'positive_dual_raw_indices':positive,'whole_zero_support':zero,'restricted_rank':13,'affine_parameters':7,
       'fixed_functionals':fixed,'whole_face_signed_functional_columns':15*513,'true_branch_hidden_states':physical,
       'all_common_weak_zero_states':common,'six_cap_coupled_whole_face_cuts':cuts,
       'scope':'The full necessary cone gives the exact universal welfare lower bound alpha, and its entire optimum face has no full ordered SPE realization. Six new directly paid universal cuts quantify separation; no half theorem or SPE counterexample.'}
    out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ['fixed_functionals','all_common_weak_zero_states','scope']},ensure_ascii=False))

if __name__=='__main__':main()
