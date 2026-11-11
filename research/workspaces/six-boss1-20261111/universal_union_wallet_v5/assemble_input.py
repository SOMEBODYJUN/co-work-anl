"""Assemble the explicitly released v5 input; exact arithmetic, no optimizer."""
from pathlib import Path
from fractions import Fraction as F
from hashlib import sha256
from copy import deepcopy
import json

HERE=Path(__file__).resolve().parent
WS=HERE.parent
REPO=WS.parents[2]
PINS={
 'universal_union_wallet_v4/exact_input.json':'b520abb0565c6df7ae4192971bf90d712ddf92a4304f3ce51710cd9b2617b8f5',
 'universal_union_wallet_v4/exact_certificate.json':'290f90feba9bf7ec8232e16e59f02b7f4e05dc41413f14510592c3d16ef28819',
 'main_all_source31_family/exact_family.json':'0268bef0a826fc1872f9b7ec7fa5d0433b1730b8670d69098a9d2c8edb5dedfd',
 'main_all_source31_family/proof.md':'ec178fdc2d5a7d3de95a4924b8d5b847551907b551ddc3e80b61544eb728ab69',
 'main_background_projection/exact_projection.json':'f39ae91167d96f015c188159e3efb9dcbf7436640e058467b0ead1386c4744cc',
 'main_background_projection/proof.md':'c0a91bd77fa98be58fbeab3a8477c296d2c05496440933c8158046bb7227b845',
 'background_five_bridge/fixed53_b0_profit.json':'0e5ab5156e98eda9e967e8227e760c7181e77d4db78540aee8b367b1769861ed',
 'background_five_bridge/fixed53_b1_profit.json':'ece4ff20dfd3fc6f7a33c2efd6a7b4af4f21fb2089523a13517246746aabfa64'}

def sha(p):return sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def save(n,x):(HERE/n).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')

def main():
    assert not (HERE/'exact_input.json').exists() and not (HERE/'single_lp_started.txt').exists()
    for n,h in PINS.items():assert sha(WS/n)==h,n
    oldpins=read(HERE/'prior_frozen_hashes.json')
    for n,h in oldpins.items():assert sha(WS/n)==h,n
    base=read(WS/'universal_union_wallet_v4/exact_input.json')
    family=read(WS/'main_all_source31_family/exact_family.json')
    bg=read(WS/'main_background_projection/exact_projection.json')
    assert len(base['raw_rows'])==225 and len(family['rows'])==320
    assert base['variables']==257 and base['nonnegative_columns']==list(range(257))
    for r in family['rows']:
        assert set(r['a'])=={str(j) for j in range(257)} and F(r['rhs'])==0
        assert F(r['numerical_divisor'])==31
    assert set(bg['all257_coefficients'])=={str(j) for j in range(257)}
    assert F(bg['all257_coefficients']['256'])==-F(226487,10**21)
    bgrow={'name':'BG5_ACTUAL_SIX_DELETION_PROJECTION','family':'BG5_SIX_DELETION_PROJECTION',
           'a':deepcopy(bg['all257_coefficients']),'rhs':'0','numerical_divisor':'1'}
    release={'authorized_by':'/root','status':'MAIN_EXPLICIT_546_ROW_RELEASE','optimizer_calls_authorized':1,
       'scope':'225 frozen raw rows,320 complete source31 rows,one BG-PROJ; full256 types+K; one LP only after source preflight.',
       'authority_note':'Recorded from Main explicit release after independent source-family audit; no authorization inferred from files.',
       'expected_raw_rows':546,'expected_columns':257,'source_sha256':PINS,
       'menu_semantics':'30 ordered unequal indices with repeated labels permitted; no synthetic legal O action',
       'background_domain_scope':'Original fixed53 background source proof and complete saved tables inherited; no claim to rerun its large hidden-domain oracle.'}
    save('main_release.json',release)
    inp=deepcopy(base)
    inp['scope']='v5 exact546 raw necessary rows,full256 actual/X/O types+K;225 baseline rows unchanged,320 source31,one background profit projection.'
    inp['raw_rows']=deepcopy(base['raw_rows'])+deepcopy(family['rows'])+[bgrow]
    assert inp['raw_rows'][:225]==base['raw_rows'] and len(inp['raw_rows'])==546
    seen={};unique=[];mapping=[];zeros=[];duplicates=[]
    for k,r in enumerate(inp['raw_rows']):
        key=(tuple(F(r['a'].get(str(j),'0')) for j in range(257)),F(r['rhs']))
        if not any(key[0]) and key[1]==0:
            zeros.append(r['name']);mapping.append({'raw_index':k,'name':r['name'],'status':'zero','unique_index':None});continue
        if key in seen:
            prev,uid=seen[key];duplicates.append({'name':r['name'],'identical_to':inp['raw_rows'][prev]['name']})
            mapping.append({'raw_index':k,'name':r['name'],'status':'duplicate','first_raw_index':prev,'unique_index':uid});continue
        uid=len(unique);seen[key]=(k,uid);unique.append(deepcopy(r))
        mapping.append({'raw_index':k,'name':r['name'],'status':'kept','unique_index':uid})
    inp['unique_rows']=unique;inp['raw_inequality_count']=546;inp['unique_inequality_count']=len(unique)
    inp['removed_zero_rows']=zeros;inp['removed_exact_duplicate_rows']=duplicates
    inp['v5_main_release_sha256']=sha(HERE/'main_release.json');inp['v5_source_sha256']=PINS
    save('exact_input.json',inp);save('duplicate_mapping.json',mapping)
    scales={}
    for row in unique:
        s=F(row['numerical_divisor']) if 'numerical_divisor' in row else max([F(1),abs(F(row['rhs']))]+[abs(F(v)) for v in row['a'].values()])
        assert s>0;scales[row['name']]=str(s)
    save('numerical_scaling.json',{'scope':'Original exact rows never scaled in input. Solver only divides by positive values.',
         'rule':'Use explicit released numerical_divisor where present,else max(1,abs(rhs),max_abs_column). New family31,BG1.','scales':scales})
    owner=REPO/'archives/customer-attraction/state/引理/一位背景五人利润的独占客户收费--引理.md'
    save('background_owner_pin.json',{'path':str(owner.relative_to(REPO)),'sha256':sha(owner),
      'read_scope':'Definitions,physical source rows,and complete fixed53 identity in sections1-4; later58-weight results not used.'})
    print(json.dumps({'status':'ASSEMBLED_ONLY_NO_OPTIMIZER','raw_rows':546,'unique_rows':len(unique),'columns':257,
       'input_sha256':sha(HERE/'exact_input.json'),'release_sha256':sha(HERE/'main_release.json'),
       'zero_rows':len(zeros),'duplicate_rows':len(duplicates),'frozen_files_unchanged':len(oldpins)},indent=2))

if __name__=='__main__':main()
