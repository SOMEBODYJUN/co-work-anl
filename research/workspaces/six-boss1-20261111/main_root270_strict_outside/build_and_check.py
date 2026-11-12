"""Expose the already proved strict ROOT270 C\O remainder as a full row."""
from pathlib import Path
from hashlib import sha256
from fractions import Fraction as F
from itertools import product
import json

P=Path(__file__).resolve().parent
W=P.parent


def read(p):return json.loads(p.read_text())
def sha(p):return sha256(p.read_bytes()).hexdigest()


def main():
    assert not (P/'freeze_manifest.json').exists()
    ip=W/'visible_maximum_joint_v5/exact_input.json'
    assert sha(ip)=='12f456dfbc789a5c1826d248e4851b84f66b428554d181b7ba12cbfdb920f3ac'
    old=read(ip)['raw_rows'][868]
    assert old['name']=='ROOT270_TRUE_BRANCH_P25'
    src=W/'main_delta_uniform_improvement'
    cert=read(src/'exact_certificate.json')
    assert cert['status']=='PASS_MAIN_UNIFORM_DELTA_ROOT_REMAINDER_FULL513_CERTIFICATE'
    root=read(W/'maximal_root_tail_wallet_v3/exact_certificate.json')
    a,b=F(root['universal_root_line']['a']),F(root['universal_root_line']['b'])
    eta=F(1087978231314917,84387869309613600)
    residual=list(map(F,read(src/'root131_replay.json')['all129_remainders']))
    states=list(product((0,1),repeat=7))
    assert all(residual[h]-eta*x[0]*(1-x[6])>=0 for h,x in enumerate(states))
    assert min(residual[h] for h,x in enumerate(states) if x[0] and not x[6])==eta
    cs={};checks=[]
    for h,x in enumerate(list(product((0,1),repeat=9))+[None]):
        if x is None:want=-a;cout=0
        else:
            load_=sum(x[:6]);u1=F(x[0],load_) if load_ else F(0)
            cout=x[8]*(1-x[7]);want=u1-b*x[7]-eta*cout
        assert want==F(old['a'].get(str(h),'0'))-eta*cout
        if want:cs[str(h)]=str(want)
        checks.append({'column':h,'coefficient':str(want),'difference':'0'})
    row={'name':'ROOT270_STRICT_C_OUTSIDE','family':'TRUE_ROOT_C_OUTSIDE_REMAINDER','a':cs,'rhs':'0',
         'numerical_divisor':'1','source':'ROOT270 true ten-budget root certificate',
         'C_outside_remainder':str(eta),'all_513_columns_preserved':True,
         'model':'Original six-provider common finite nonempty labeled catalog, full ordered-history pure SPE; arbitrary six legal query union; C is a legal maximum-size label.'}
    (P/'ROOT270_STRICT_C_OUTSIDE.json').write_text(json.dumps(row,ensure_ascii=False,indent=2)+'\n')
    (P/'all513_column_checks.json').write_text(json.dumps(checks,indent=2)+'\n')
    report={'status':'PASS_MAIN_ROOT270_STRICT_REMAINDER_ALL128_ROOT_STATES_ALL513_VISIBLE_COLUMNS',
            'root_states':128,'visible_columns':513,'optimizer_calls':0,'eta':str(eta),
            'source_pins':{str(p.relative_to(W)):sha(p) for p in [ip,src/'exact_certificate.json',src/'root131_replay.json',src/'proof.md',W/'maximal_root_tail_wallet_v3/exact_certificate.json']}}
    (P/'check_result.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    manifest={'status':'MAIN_FROZEN_TRUE_ROOT_STRICT_ROW','row_file':'ROOT270_STRICT_C_OUTSIDE.json',
              'raw_rows':1,'columns':513,'optimizer_calls':0,
              'artifacts':{p.name:sha(p) for p in sorted(P.iterdir()) if p.is_file()}}
    (P/'freeze_manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'status':manifest['status'],'row_sha256':sha(P/'ROOT270_STRICT_C_OUTSIDE.json'),'manifest_sha256':sha(P/'freeze_manifest.json')},ensure_ascii=False))


if __name__=='__main__':main()
