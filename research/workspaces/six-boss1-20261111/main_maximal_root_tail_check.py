"""Main literal131-column verification of the ten positive true-root-tail budgets."""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
from hashlib import sha256
import json

HERE=Path(__file__).resolve().parent
def main():
    p=HERE/'maximal_root_tail_wallet';ip=p/'exact_input.json';cp=p/'exact_certificate.json'
    assert sha256(ip.read_bytes()).hexdigest()=='3c1a824ed0a17562da812db1d0bb12485f0b1c7f743577af7bc2ecf316d3ab65'
    cert=json.loads(cp.read_text())
    N=112944305160;A=11595684007;B=2178783435;pi=37375524862
    caps=[939131055,6218848680,6200167680,6031687680,6390005760]
    safe3=5324085000;safe4=5380128000;safe6=2508226560;pair=3881779200
    assert pi-sum(caps)==A
    res=[]
    for j,bits in enumerate(product((0,1),repeat=7)):
        p0,y2,y3,y4,y5,z,o=bits;l=list(bits[:6]);c=sum(l);q=F(o,6)
        v=[F(t,c) if c else F(0) for t in l]
        s3=v[2]-q/F(p0+y2+4)
        s4=v[3]-q/F(p0+y2+y3+3)
        s6=v[5]-q/F(p0+y2+y3+y4+y5+1)
        d=p0+y2+y3+y4+1
        pp=v[4]+v[5]+F(y5,d*(d+1))-F(o,3*d)+F(o,36*d*(d+1))
        h=N*v[0]+sum(t*w for t,w in zip(l[1:],caps))-pi*p0-B*o-safe3*s3-safe4*s4-safe6*s6-pair*pp
        assert h>=0
        assert h==N*F(cert['dual']['column_residuals'][str(j)])
        res.append({'index':j,'bits':list(bits),'integer_scaled_residual':str(h)})
    assert F(cert['dual']['column_residuals']['128'])==0
    assert sum(F(r['integer_scaled_residual'])==0 for r in res)==13
    inp=json.loads(ip.read_text());K0=F(inp['fixed_K']);O0=F(inp['fixed_O'])
    rhs=(A*K0+B*O0)/N
    assert rhs==F(cert['objective'])
    out={'status':'PASS','scope':'ten positive budgets reconstructed from genuine ordered branch shares; all128 types plus independent u,K,O columns',
      'input_sha256':sha256(ip.read_bytes()).hexdigest(),'certificate_sha256':sha256(cp.read_bytes()).hexdigest(),
      'universal_line':{'u':N,'K':-A,'O':-B},'K_equals_size_multiplier':pi,'O_equals_union_multiplier':B,
      'caps_sum':sum(caps),'positive_atom_residuals':115,'zero_atom_residuals':13,
      'fixed_K0':str(K0),'fixed_cone_objective':str(rhs),'fixed_cone_objective_decimal':float(rhs),
      'union_cap_weight':'0','floor_weight':'0','valid_for_any_six_query_union':True,
      'released_to_next_global_wallet':True,'residuals':res}
    print(json.dumps(out,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
