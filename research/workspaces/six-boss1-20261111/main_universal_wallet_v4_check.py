"""Main independent exact replay of 225 raw rows and 257 dual columns."""
from pathlib import Path
from fractions import Fraction as F
from hashlib import sha256
import json

HERE=Path(__file__).resolve().parent


def main():
    base=HERE/'universal_union_wallet_v4'
    ip,cp=base/'exact_input.json',base/'exact_certificate.json'
    assert sha256(ip.read_bytes()).hexdigest()=='b520abb0565c6df7ae4192971bf90d712ddf92a4304f3ce51710cd9b2617b8f5'
    assert sha256(cp.read_bytes()).hexdigest()=='290f90feba9bf7ec8232e16e59f02b7f4e05dc41413f14510592c3d16ef28819'
    inp,cert=json.loads(ip.read_text()),json.loads(cp.read_text())
    prior=json.loads((HERE/'universal_union_wallet_v3/exact_input.json').read_text())
    assert inp['raw_rows'][:221]==prior['raw_rows']
    for name in ['atom_columns','objective','equality','K_column','nonnegative_columns']:
        assert inp[name]==prior[name]
    rows={r['name']:r for r in inp['raw_rows']}; assert len(rows)==225
    released=json.loads((HERE/'main_thirty_index_strengthening/exact_certificate.json').read_text())
    for row in released['rows']:
        actual=rows[row['name']]
        assert F(actual['rhs'])==F(row['rhs'])==0
        assert all(F(actual['a'].get(str(j),0))==F(row['a'][str(j)]) for j in range(257))
    x={str(j):F(cert['primal'].get(str(j),0)) for j in range(257)}
    assert min(x.values())>=0
    def dot(v):return sum((F(c)*x[j] for j,c in v.items()),F(0))
    assert dot(inp['equality']['a'])==F(inp['equality']['rhs'])==1
    slacks={name:dot(row['a'])-F(row['rhs']) for name,row in rows.items()}
    assert all(v>=0 and v==F(cert['raw_row_slacks'][k]) for k,v in slacks.items())
    obj=dot(inp['objective']);assert obj==F(cert['objective'])
    dual=cert['dual']; lam={k:F(v) for k,v in dual['row_weights'].items()}
    assert len(lam)==11 and min(lam.values())>0
    nu=F(dual['normalization_multiplier']); residual=[]
    for j in range(257):
        k=str(j)
        r=F(inp['objective'].get(k,0))-nu*F(inp['equality']['a'].get(k,0))
        r-=sum((v*F(rows[name]['a'].get(k,0)) for name,v in lam.items()),F(0))
        assert r==F(dual['nonnegative_column_residual'].get(k,0))>=0
        assert r*x[k]==0
        residual.append(r)
    assert nu*F(inp['equality']['rhs'])+sum((v*F(rows[k]['rhs']) for k,v in lam.items()),F(0))==obj
    assert all(slacks[k]==0 for k in lam)
    assert all(row['name'] in lam for row in released['rows'])
    out={'status':'PASS_MAIN_ALL225_ROWS257_COLUMNS_AND_FOUR_RELEASED_ROWS','optimizer_calls':0,
         'input_sha256':sha256(ip.read_bytes()).hexdigest(),'certificate_sha256':sha256(cp.read_bytes()).hexdigest(),
         'all221_old_rows_identical':True,'raw_rows':225,'columns':257,'positive_budget_count':len(lam),
         'positive_atom_residuals':sum(r>0 for r in residual[:256]),
         'zero_residual_columns':[j for j,r in enumerate(residual) if r==0],
         'positive_budget_weights':{k:str(v) for k,v in lam.items()},'K':cert['K'],
         'objective':str(obj),'objective_decimal':float(obj),'half_gap':str(F(1,2)-obj),
         'not_claimed':['SPE realization','half coverage','whole optimum-face exclusion by this matrix replay alone']}
    print(json.dumps(out,ensure_ascii=False,indent=2))


if __name__=='__main__':main()
