"""Main exact replay of 546 raw rows, full source31/BG inputs, and all257 columns."""
from pathlib import Path
from fractions import Fraction as F
from hashlib import sha256
import json

HERE=Path(__file__).resolve().parent


def main():
    ip=HERE/'universal_union_wallet_v5/exact_input.json'
    cp=HERE/'universal_union_wallet_v5/exact_certificate.json'
    assert sha256(ip.read_bytes()).hexdigest()=='3b2065e702c5590d50ebc8acd5ea30337e82db2a84585f87040acd36e91db553'
    assert sha256(cp.read_bytes()).hexdigest()=='5e5a2377ed780f4a9c9f58ca8703fc5a473d41ea1945a654aa0ee6c0efa0deda'
    inp,cert=json.loads(ip.read_text()),json.loads(cp.read_text())
    old=json.loads((HERE/'universal_union_wallet_v4/exact_input.json').read_text())
    assert inp['raw_rows'][:225]==old['raw_rows']
    for name in ['atom_columns','objective','equality','K_column','nonnegative_columns']:assert inp[name]==old[name]
    rows={r['name']:r for r in inp['raw_rows']}; assert len(rows)==546
    fam=json.loads((HERE/'main_all_source31_family/exact_family.json').read_text())
    for row in fam['rows']:
        actual=rows[row['name']]
        assert F(actual['rhs'])==0
        assert all(F(actual['a'].get(str(j),0))==F(row['a'][str(j)]) for j in range(257))
    bg=json.loads((HERE/'main_background_projection/exact_projection.json').read_text())
    bgr=rows['BG5_ACTUAL_SIX_DELETION_PROJECTION'];assert F(bgr['rhs'])==0
    assert all(F(bgr['a'].get(str(j),0))==F(bg['all257_coefficients'][str(j)]) for j in range(257))
    x={str(j):F(cert['primal'].get(str(j),0)) for j in range(257)};assert min(x.values())>=0
    def dot(v):return sum((F(c)*x[j] for j,c in v.items()),F(0))
    assert dot(inp['equality']['a'])==F(inp['equality']['rhs'])==1
    slacks={k:dot(r['a'])-F(r['rhs']) for k,r in rows.items()}
    assert all(v>=0 and v==F(cert['raw_row_slacks'][k]) for k,v in slacks.items())
    objective=dot(inp['objective']);assert objective==F(cert['objective'])
    dual=cert['dual'];lam={k:F(v) for k,v in dual['row_weights'].items()}
    assert len(lam)==11 and min(lam.values())>0
    nu=F(dual['normalization_multiplier']);residual=[]
    for j in range(257):
        k=str(j);r=F(inp['objective'].get(k,0))-nu*F(inp['equality']['a'].get(k,0))
        r-=sum((v*F(rows[name]['a'].get(k,0)) for name,v in lam.items()),F(0))
        assert r==F(dual['nonnegative_column_residual'].get(k,0))>=0 and r*x[k]==0
        residual.append(r)
    assert nu*F(inp['equality']['rhs'])+sum((v*F(rows[k]['rhs']) for k,v in lam.items()),F(0))==objective
    assert all(slacks[k]==0 for k in lam)
    result={'status':'PASS_MAIN_ALL546_ROWS257_COLUMNS_SOURCE31_AND_BG','optimizer_calls':0,
            'input_sha256':sha256(ip.read_bytes()).hexdigest(),'certificate_sha256':sha256(cp.read_bytes()).hexdigest(),
            'old225_rows_identical':True,'source31_coefficients_checked':82240,'BG_coefficients_checked':257,
            'raw_rows':546,'columns':257,'objective':str(objective),'objective_decimal':float(objective),'K':cert['K'],
            'positive_budget_weights':{k:str(v) for k,v in lam.items()},
            'positive_primal_atoms':[j for j in range(256) if x[str(j)]>0],
            'zero_residual_columns':[j for j,v in enumerate(residual) if v==0],
            'released_for_precise_new_obligations':True,
            'not_claimed':['complete SPE realization','half coverage','whole optimum-face exclusion']}
    print(json.dumps(result,ensure_ascii=False,indent=2))


if __name__=='__main__':main()
