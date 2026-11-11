"""Main exact replay of all219 rows and all257 dual columns, no optimizer."""
from pathlib import Path
from fractions import Fraction as F
from hashlib import sha256
import json

HERE=Path(__file__).resolve().parent
def main():
    p=HERE/'universal_union_wallet_v2';ip=p/'exact_input.json';cp=p/'exact_certificate.json'
    assert sha256(ip.read_bytes()).hexdigest()=='bb7c66e141b9ab6080c5fbafe6c00f966a95247269ff54d2ae3abae7809f35f2'
    assert sha256(cp.read_bytes()).hexdigest()=='12d4f059b7be021c8b3c89ed6adf3bde208750da6ce0eee79c383a813d50b36b'
    a=json.loads(ip.read_text());c=json.loads(cp.read_text())
    x={int(j):F(v) for j,v in c['primal'].items()}
    assert all(v>=0 for v in x.values())
    def dot(v):return sum((F(q)*x.get(int(j),F(0)) for j,q in v.items()),F(0))
    eq=a['equality'];assert dot(eq['a'])==F(eq['rhs'])==1
    rows={r['name']:r for r in a['raw_rows']};assert len(rows)==219
    slacks={k:dot(r['a'])-F(r['rhs']) for k,r in rows.items()}
    assert min(slacks.values())>=0
    assert all(slacks[k]==F(v) for k,v in c['raw_row_slacks'].items())
    obj=dot(a['objective']);assert obj==F(c['objective'])==F(22634634904624698063,52739368771603064323)
    d=c['dual'];lam={k:F(v) for k,v in d['row_weights'].items()};nu=F(d['normalization_multiplier'])
    assert len(lam)==10 and min(lam.values())>0
    rr=[]
    for j in range(257):
        k=str(j);r=F(a['objective'].get(k,'0'))-nu*F(eq['a'].get(k,'0'))
        r-=sum((v*F(rows[n]['a'].get(k,'0')) for n,v in lam.items()),F(0))
        assert r>=0 and r==F(d['nonnegative_column_residual'].get(k,'0'))
        assert r*x.get(j,F(0))==0
        rr.append(r)
    assert nu*F(eq['rhs'])+sum((v*F(rows[k]['rhs']) for k,v in lam.items()),F(0))==obj
    assert all(slacks[k]==0 for k in lam)
    assert 'ROOT_BRANCH_NEW' in lam and 'TRUE_X_TAIL_CUT' in lam
    out={'status':'PASS','scope':'Main exact primal/dual matrix replay; semantic source checks are separately bound',
         'input_sha256':sha256(ip.read_bytes()).hexdigest(),'certificate_sha256':sha256(cp.read_bytes()).hexdigest(),
         'all_original_rows':219,'all_nonnegative_columns':257,'positive_primal_atoms':len(x)-1,
         'positive_dual_rows':10,'positive_customer_residuals':sum(r>0 for r in rr[:256]),
         'zero_customer_residuals':sum(r==0 for r in rr[:256]),'K_residual':str(rr[256]),
         'objective':str(obj),'objective_decimal':float(obj),'half_gap':str(F(1,2)-obj),
         'K':c['K'],'released_for_precise_new_obligations':True,
         'not_claimed':['complete SPE realization','half coverage','best-known bound']}
    print(json.dumps(out,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
