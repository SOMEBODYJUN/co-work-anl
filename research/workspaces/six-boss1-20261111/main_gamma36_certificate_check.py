"""Main independently pays the factor36 debit and replays all 513 columns."""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
from hashlib import sha256
import json

W=Path(__file__).resolve().parent


def read(p):return json.loads(p.read_text())
def sha(p):return sha256(p.read_bytes()).hexdigest()
def vec(v):
    if isinstance(v,list):
        assert len(v)==513
        return list(map(F,v))
    assert isinstance(v,dict) and all(0<=int(k)<513 for k in v)
    return [F(v.get(str(h),'0')) for h in range(513)]


def main():
    out=W/'main_gamma36_certificate_check.json';assert not out.exists()
    ap=W/'delta_uniform_audit/certificate_gamma36.json'
    assert sha(ap)=='7c98da8d67c2deaa3b7541a761b3e9f6fa80a7deab00ac80e229d0cd57de15d9'
    new=read(ap);inp=read(W/'visible_maximum_joint_v5/exact_input.json')
    old=read(W/'visible_maximum_joint_v5_solve/exact_certificate.json')
    rows=inp['raw_rows'];y=list(map(F,old['dual']['raw_row_weights']))
    oldr=list(map(F,old['dual']['nonnegative_column_residual']));oldEC=F(old['dual']['equality_multipliers'][1])
    lam0,lamr=y[2606],y[868];eps=F(1,144);eta=F(1087978231314917,84387869309613600)
    gamma=lam0*eps/36;alpha=F(old['objective']);anew=(alpha+gamma)/(1+gamma)
    assert gamma==F(new['gamma']) and anew==F(new['alpha_new'])
    assert anew>F(read(W/'main_delta_uniform_improvement/exact_certificate.json')['alpha_new'])>alpha
    assert set(new['row_coefficient_overrides'])=={'868','2606'}
    over={int(k):vec(v['coefficients']) for k,v in new['row_coefficient_overrides'].items()}
    assert over[868]==vec(read(W/'main_root270_strict_outside/ROOT270_STRICT_C_OUTSIDE.json')['a'])
    assert over[2606]==vec(read(W/'main_delta_uniform_improvement/two_true_delta_cuts.json')[0]['a_coefficients'])
    yn=list(y)
    for k in range(869,875):yn[k]+=gamma
    assert yn==list(map(F,new['all3056_payments_before_normalization']))
    assert [v/(1+gamma) for v in yn]==list(map(F,new['all3056_payments_normalized']))
    positive=[k for k,v in enumerate(yn) if v]
    assert positive==new['positive_raw_indices'] and len(positive)==16
    freeEC=oldEC-lam0*F(1528993,497664)
    assert freeEC==F(new['free_EC_weight_before_normalization'])
    assert freeEC/(1+gamma)==F(new['free_EC_weight_normalized'])
    rr=[];debits=[];identity=[]
    for h,bits in enumerate(list(product((0,1),repeat=9))+[None]):
        if bits is None:
            r=oldr[h]
        else:
            p,c,o=bits[0],bits[8],bits[7]
            debit=lam0*eps*F(p*o*(1-c),72)
            if p*o*(1-c):
                assert oldr[h]-debit>0;debits.append(oldr[h]-debit)
            tc=c*(sum((F(1,sum(bits[:i])+6-i) for i in range(6)),F(0))-1)
            assert tc>=0
            r=oldr[h]-debit+(lamr*eta+gamma)*c*(1-o)-lam0*F(p*c*(1-o),180)+gamma*tc
        assert r==F(new['all513_residuals_before_normalization'][h])>=0
        assert r/(1+gamma)==F(new['all513_residuals_normalized'][h]);rr.append(r)
        oh=F(inp['equalities'][0]['a'].get(str(h),'0'))
        ec=F(inp['equalities'][1]['a'].get(str(h),'0'))
        lhs=(1+gamma)*F(inp['objective'].get(str(h),'0'))-(alpha+gamma)*oh
        rhs=r+freeEC*ec
        for k in positive:
            coeff=over[k][h] if k in over else F(rows[k]['a'].get(str(h),'0'))-F(rows[k]['rhs'])*oh
            rhs+=yn[k]*coeff
        assert lhs==rhs
        identity.append(str(lhs-rhs))
    assert len(debits)==64
    assert [h for h,r in enumerate(rr) if not r]==new['zero_residual_columns']==[0,2,14,18,22,50,74,499,512]
    assert len([r for r in rows if F(r['rhs'])==-1])==len(new['all30_rhs_minus_one_rows_retained'])==30
    result={'status':'PASS_MAIN_GAMMA36_ALL513_UNIVERSAL_IDENTITY','optimizer_calls':0,'gamma':str(gamma),
            'alpha':str(anew),'alpha_decimal':float(anew),'improvement_over_old':str(anew-alpha),
            'debit_columns':64,'minimum_after_debit':str(min(debits)),'positive_payments':16,
            'full_identity_columns':513,'zero_residual_columns':new['zero_residual_columns'],
            'free_C_weight':str(freeEC),'all_identity_residuals':identity,
            'proof_personally_read_complete':True,'audit_certificate_sha256':sha(ap),
            'audit_proof_sha256':sha(W/'delta_uniform_audit/proof.md'),
            'audit_manifest_sha256':sha(W/'delta_uniform_audit/freeze_manifest.json'),
            'scope':'Original complete-history common-catalog pure SPE, any six legal query union. Uniform bound, not new LP optimum or half.'}
    out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ['all_identity_residuals','scope']},ensure_ascii=False))


if __name__=='__main__':main()
