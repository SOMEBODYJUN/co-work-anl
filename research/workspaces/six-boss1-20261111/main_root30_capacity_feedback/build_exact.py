"""Main exact nonnegative CAP(B2) feedback on ROOT30; no optimization."""
from pathlib import Path
from fractions import Fraction as F
from hashlib import sha256
from itertools import product
from math import lcm,gcd
import json

HERE=Path(__file__).resolve().parent
WS=HERE.parent


def main():
    parent=WS/'main_thirty_index_strengthening/exact_certificate.json'
    c=json.loads(parent.read_text())
    r={int(j):F(v) for j,v in c['root_all129_residuals'].items()}
    delta=min(r[h] for h in range(128) if h%2 and not ((h>>5)&1))
    assert delta==F(77334949597,572962933877670)>0
    a=F(c['root_old_a'])-delta;b=F(c['root_new_b'])+delta
    weights={k:F(v) for k,v in c['root_fixed_weights'].items()};weights['CAP_B2']+=delta
    pip=F(c['root_equality_multipliers']['K']);pio=F(c['root_equality_multipliers']['O'])+delta
    ip=WS/'maximal_root_tail_wallet_v2/exact_input.json'
    assert sha256(ip.read_bytes()).hexdigest()=='86a235bf210862ef8f8bbbdea7ac324e71f691a8aa7af455a821e6379cfe117d'
    original=json.loads(ip.read_text());rows={v['name']:v for v in original['raw_rows']}
    envelope=json.loads((WS/'main_thirty_index_strengthening/requery30_envelopes.json').read_text())
    residual={}
    for h,bits in enumerate(product((0,1),repeat=7)):
        p,y2,y3,y4,y5,z,o=bits;D=1+p+y2+y3+y4
        values={name:F(row['a'].get(str(h),0)) for name,row in rows.items()}
        values['PAIR|Omean|Omean']-=F(o,36*D*(D+1))
        values['OPT_SOURCE3_REQUERY_CUT']=F(envelope[h]['cut'])
        rho=-sum((weight*values[name] for name,weight in weights.items()),F(0))-pip*p-pio*o
        assert rho==r[h]+delta*(y2-o)>=0
        residual[str(h)]=str(rho)
    assert 1-sum((weight*F(rows[name]['a'].get('128',0)) for name,weight in weights.items()),F(0))==0
    assert pip+sum((weight*F(rows[name]['bK']) for name,weight in weights.items()),F(0))==a
    assert pio+sum((weight*F(rows[name]['bO']) for name,weight in weights.items()),F(0))==b
    residual['128']='0'
    scale=lcm(a.denominator,b.denominator);ints=[scale,int(scale*a),int(scale*b)]
    divisor=gcd(gcd(ints[0],ints[1]),ints[2]);ints=[v//divisor for v in ints]
    visible=json.loads((WS/'universal_union_wallet_v5/exact_input.json').read_text());coeff={}
    for atom in visible['atom_columns']:
        aa=atom['a'];total=sum(aa);coeff[str(atom['index'])]=str((F(aa[0],total) if total else F(0))-b*atom['o'])
    coeff['256']=str(-a)
    row={'name':'ROOT30_B2_CAPACITY_FEEDBACK','family':'ROOT30_CAPACITY_FEEDBACK','a':coeff,'rhs':'0','numerical_divisor':'1'}
    point=json.loads((WS/'universal_union_wallet_v5/exact_certificate.json').read_text())['primal']
    value=sum((F(v)*F(point.get(j,0)) for j,v in coeff.items()),F(0))
    out={'status':'PASS_MAIN_ALL131_COLUMNS_POSITIVE_CAPACITY_FEEDBACK','optimizer_calls':0,
         'parent_certificate_sha256':sha256(parent.read_bytes()).hexdigest(),'delta':str(delta),
         'old_zero_atom_types':[h for h in range(128) if r[h]==0],
         'delta_attaining_types':[h for h in range(128) if h%2 and not ((h>>5)&1) and r[h]==delta],
         'new_integer_line':dict(zip(['u','K','O'],map(str,ints))),
         'new_a':str(a),'new_b':str(b),'new_weights':{k:str(v) for k,v in weights.items()},
         'free_mass_multipliers':{'K':str(pip),'O':str(pio)},'all129_residuals':residual,
         'row':row,'v5_point_value':str(value),'v5_point_value_decimal':float(value),
         'scope':'Any six legal query union; comparison with ROOT30 is strict whenever O>K. No new root cone optimum claim.'}
    (HERE/'exact_certificate.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
    (HERE/'ROOT30_B2_CAPACITY_FEEDBACK.json').write_text(json.dumps(row,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:out[k] for k in ['status','delta','new_integer_line','v5_point_value','v5_point_value_decimal']},ensure_ascii=False,indent=2))
    print('row_sha256',sha256((HERE/'ROOT30_B2_CAPACITY_FEEDBACK.json').read_bytes()).hexdigest())


if __name__=='__main__':main()
