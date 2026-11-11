"""Main independently replays all1003/513, whole-face affine data and new cut."""
from pathlib import Path
from fractions import Fraction as F
from hashlib import sha256
import json
import sympy as sp

W=Path(__file__).resolve().parent


def load(rel):
    return json.loads((W/rel).read_text())


def main():
    out=W/'main_visible_c_v2_certificate_check.json'
    assert not out.exists()
    inp=load('visible_maximum_joint_v2/exact_input.json')
    p='visible_maximum_joint_v2_solve/'
    cert=load(p+'exact_certificate.json')
    face=load(p+'optimal_face.json')
    assert sha256((W/(p+'exact_certificate.json')).read_bytes()).hexdigest()=='b9c1d5339b21823b5f448f8c8242bf8b1394b181c099c2bf7d87c68d3f227aea'
    rows=inp['raw_rows']; eqs=inp['equalities']; z=list(map(F,cert['primal']))
    y=list(map(F,cert['dual']['raw_row_weights'])); eta=list(map(F,cert['dual']['equality_multipliers']))
    residual=list(map(F,cert['dual']['nonnegative_column_residual']))
    assert len(rows)==len(y)==1003 and len(z)==len(residual)==513 and len(eta)==2
    assert min(z)>=0 and min(y)>=0 and min(residual)>=0
    def dot(a,v):
        return sum((F(x)*v[int(j)] for j,x in a.items()),F(0))
    for k,row in enumerate(rows):
        slack=dot(row['a'],z)-F(row['rhs'])
        assert slack==F(cert['raw_row_slacks'][k])>=0 and slack*y[k]==0
    for j,eq in enumerate(eqs):
        assert dot(eq['a'],z)==F(eq['rhs'])
    for j in range(513):
        r=F(inp['objective'].get(str(j),'0'))
        r-=sum((w*F(row['a'].get(str(j),'0')) for w,row in zip(y,rows) if w),F(0))
        r-=sum((w*F(eq['a'].get(str(j),'0')) for w,eq in zip(eta,eqs)),F(0))
        assert r==residual[j] and r*z[j]==0
    alpha=dot(inp['objective'],z)
    dual=sum((w*F(row['rhs']) for w,row in zip(y,rows)),F(0))+sum((w*F(eq['rhs']) for w,eq in zip(eta,eqs)),F(0))
    assert alpha==dual==F(cert['objective'])
    zero=[j for j,r in enumerate(residual) if not r]
    assert zero==face['zero_residual_columns']
    pos=[i for i,w in enumerate(y) if w]
    equations=eqs+[rows[i] for i in pos]
    E=[[F(row['a'].get(str(j),'0')) for j in zero] for row in equations]
    h=[F(row['rhs']) for row in equations]
    assert sp.Matrix(E).rank()==14
    coords={r['column']:[F(r['constant'])]+list(map(F,r['parameter_coefficients'])) for r in face['coordinates']}
    assert sorted(coords)==zero
    for k in range(8):
        for i,er in enumerate(E):
            assert sum((v*coords[j][k] for v,j in zip(er,zero)),F(0))==(h[i] if k==0 else 0)
    assert sp.Matrix([[coords[j][k] for k in range(1,8)] for j in zero]).rank()==7
    for row,record in zip(rows,face['raw_inequality_restrictions']):
        expected=[]
        for k in range(8):
            v=sum((F(row['a'].get(str(j),'0'))*coords[j][k] for j in zero),F(0))
            expected.append(v-(F(row['rhs']) if k==0 else 0))
        assert expected==[F(record['constant'])]+list(map(F,record['parameter_coefficients']))
    fixed={}
    for record in face['fixed_functionals']:
        name=record['name']; target=[]
        for j in zero:
            if j==512:
                K=F(1); A=X=U=S=F(0)
            else:
                bits=[(j>>k)&1 for k in range(8,-1,-1)]
                a,x,o,c=bits[:6],bits[6],bits[7],bits[8]
                K=F(0);A=F(a[0]);X=F(x);U=F(a[1],sum(a)) if any(a) else F(0)
                S=U-F(c,a[0]+5)
                assert not (a[0] and not c) and not (a[0] and x)
            outside=F(0) if j==512 else F(c*(1-o))
            values=dict(K=K,size_A1=A,size_X=X,u2=U,u2_minus_K_over5=U-K/5,C_outside_O_mass=outside,
                        old_P25_C_Omean_slack=F(rows[927]['a'].get(str(j),'0')),
                        ROOT270_slack=F(rows[868]['a'].get(str(j),'0')),
                        NS5_slack=F(rows[1002]['a'].get(str(j),'0')))
            target.append(values[name])
        weights=list(map(F,record['signed_equation_weights']))
        assert all(sum((weights[i]*E[i][k] for i in range(14)),F(0))==target[k] for k in range(21))
        assert sum((w*v for w,v in zip(weights,h)),F(0))==F(record['value'])
        fixed[name]=record['value']
    assert F(fixed['u2_minus_K_over5'])>0
    new=load('main_source2_maximum_nested_safe/SOURCE2_MAXIMUM_C_NESTED_SOURCE5_SAFE.json')
    target=[]
    for j in zero:
        if j==512: payoff_minus_K5=F(-1,5)
        else:
            a=[(j>>k)&1 for k in range(8,2,-1)]
            payoff_minus_K5=F(a[1],sum(a)) if any(a) else F(0)
        target.append(5*F(new['a'].get(str(j),'0'))-515*payoff_minus_K5)
    values=[sum((v*coords[j][k] for v,j in zip(target,zero)),F(0)) for k in range(8)]
    # Direct reweighting proof, before any comparison of valid rows.
    hidden=load('main_source2_maximum_nested_safe/hidden_state_checks.json')
    for state in hidden:
        L=state['p']+state['c']+sum(state['r'])
        share=F(state['c'],L) if L else F(0)
        new_residual=F(state['residual'])-F(103,12)*(share-F(state['c'],5))
        assert new_residual>=0
    assert 25-F(103,12)==F(197,12)>0
    assert all(v==0 for v in values[1:]) and values[0]<0
    result=dict(status='PASS_MAIN_FULL1003_RAW513_DUAL_AND_WHOLE_FACE_WITH_NEW_UNIVERSAL_CUT',
                optimizer_calls=0,raw_rows=1003,columns=513,equalities=2,
                whole_zero_support=zero,restricted_rank=14,affine_parameters=7,
                alpha=str(alpha),alpha_decimal=float(alpha),fixed_functionals=fixed,
                new_reweighted_985_cut_entire_face_value=str(values[0]),new_cut_face_decimal=float(values[0]),
                proof_review='Main read the complete NS5 proof and 11-zero-state face exclusion. Main directly reweighted source IC to197/12 and checked all128 new residuals before deriving the985-row; this is not subtraction of valid inequalities.')
    out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ['fixed_functionals','whole_zero_support','proof_review']},ensure_ascii=False))


if __name__=='__main__':
    main()
