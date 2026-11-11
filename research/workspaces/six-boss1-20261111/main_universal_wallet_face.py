"""Exact optimal-face exclusion and constructive strict bound; no optimizer."""
from pathlib import Path
from fractions import Fraction as F
from hashlib import sha256
import json
import sympy as sp

HERE=Path(__file__).resolve().parent
def main():
    base=HERE/'universal_union_wallet_lp'
    ip=base/'exact_input.json';cp=base/'exact_certificate.json'
    assert sha256(ip.read_bytes()).hexdigest()=='f87a60372dee7449332b17721be6aa70012fb3aca251825cb2e9dd755ff01e41'
    assert sha256(cp.read_bytes()).hexdigest()=='ccc085060427e2999a8e4f00ac3414d7e20a1c6e66aeba8d3e658ae34cb16c85'
    a=json.loads(ip.read_text());cert=json.loads(cp.read_text())
    rows={r['name']:r for r in a['raw_rows']}
    names=list(cert['dual']['row_weights'])
    lam={k:F(v) for k,v in cert['dual']['row_weights'].items()}
    h={j:F(cert['dual']['nonnegative_column_residual'].get(str(j),'0')) for j in range(257)}
    zeros=[j for j in range(257) if h[j]==0]
    erow=a['equality']; selected=[erow]+[rows[k] for k in names]
    A=sp.Matrix([[sp.Rational(r['a'].get(str(j),'0')) for j in zeros] for r in selected])
    assert len(zeros)==18 and A.rank()==14
    obj={int(k):F(v) for k,v in a['objective'].items()}
    o={int(k):F(v) for k,v in erow['a'].items()}
    new={}
    for atom in a['atom_columns']:
        j=atom['index'];bits=atom['a'];c=sum(bits)
        new[j]=10980*(F(bits[0],c) if c else F(0))-87*atom['o']
    new[256]=F(-1658)
    def identity(target):
        sol,params=A.T.gauss_jordan_solve(sp.Matrix([sp.Rational(target.get(j,0)) for j in zeros]))
        assert params.rows==0
        coeff=[F(str(v)) for v in sol]
        rem={j:target.get(j,F(0))-sum((coeff[k]*F(r['a'].get(str(j),'0')) for k,r in enumerate(selected)),F(0)) for j in range(257)}
        assert all(rem[j]==0 for j in zeros)
        assert all(h[j]>0 for j,v in rem.items() if v)
        return coeff,rem
    kcoef,krem=identity({256:F(1)})
    assert kcoef[0]==F(cert['K'])
    ncoef,nrem=identity(new)
    ell=ncoef[0];assert ell<0
    assert ell==(189*kcoef[0]-69)/5
    ar={k:v for k,v in zip(names,ncoef[1:])}
    candidates=[(lam[k]/v,'row:'+k) for k,v in ar.items() if v>0]
    candidates += [(h[j]/v,'column:'+str(j)) for j,v in nrem.items() if v>0]
    gamma=min(v for v,_ in candidates)
    assert gamma>0
    alpha=F(cert['objective']);bound=alpha-gamma*ell
    newlam={k:lam[k]-gamma*ar[k] for k in names}
    newh={j:h[j]-gamma*nrem[j] for j in range(257)}
    assert min(newlam.values())>=0 and min(newh.values())>=0
    for j in range(257):
        rhs=gamma*new[j]+sum((v*F(rows[k]['a'].get(str(j),'0')) for k,v in newlam.items()),F(0))+newh[j]
        assert rhs==obj.get(j,F(0))-bound*o.get(j,F(0))
    out={
      'status':'PASS','optimizer_calls':0,'scope':'all256 types, original217-row entire optimal face',
      'input_sha256':sha256(ip.read_bytes()).hexdigest(),'certificate_sha256':sha256(cp.read_bytes()).hexdigest(),
      'positive_dual_row_names':names,'zero_residual_columns':zeros,'restricted_rank':14,'restricted_dimension':4,
      'K_identity':{'normalization_coefficient':str(kcoef[0]),'row_coefficients':{k:str(v) for k,v in zip(names,kcoef[1:])},'column_coefficients':{str(j):str(v) for j,v in krem.items() if v}},
      'new_row':{str(j):str(v) for j,v in new.items() if v},
      'new_row_face_identity':{'normalization_coefficient':str(ell),'row_coefficients':{k:str(v) for k,v in ar.items()},'column_coefficients':{str(j):str(v) for j,v in nrem.items() if v}},
      'whole_optimal_face_excluded':True,'constant_new_row_on_normalized_face':str(ell),
      'constructive_strict_bound':{'old_alpha':str(alpha),'gamma':str(gamma),'binding_ratio_candidates':[label for v,label in candidates if v==gamma],
        'bound':str(bound),'bound_decimal':float(bound),'improvement':str(bound-alpha),
        'new_root_row_weight':str(gamma),'old_row_weights':{k:str(v) for k,v in newlam.items() if v},
        'nonnegative_column_residual':{str(j):str(v) for j,v in newh.items() if v},
        'matching_primal_claimed':False,'best_known_bound_claimed':False},
    }
    print(json.dumps(out,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
