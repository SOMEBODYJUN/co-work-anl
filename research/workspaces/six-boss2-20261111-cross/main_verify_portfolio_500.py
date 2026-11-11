"""Main's exact replay of the readable 23-integer-weight strictness row."""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib,time
B=Path(__file__).resolve().parent
source=B/'main_verify_portfolio_pair_5744.py'
ns={'__file__':str(source)}
exec(compile(source.read_text().split('\nstart = time.time()\n',1)[0],str(source),'exec'),ns)
p=B/'joint_requery/portfolio_comparison/joint_common_denominator_5744.json';a=json.loads(p.read_text());d=F(a['source_sum_integer'])
rec={k:a[k] for k in ['i','k','member','orb']}
rec.update(weights={k:str(F(v)/d) for k,v in a['weights_integer'].items()},source_weight_sum='1',u6_coefficient=str(F(a['u6_coefficient_integer'])/d),K_coefficient=str(F(a['K_coefficient_integer'])/d),sparse_row=a['sparse_row_normalized'],exact_slack=a['slack_normalized_exact'])
start=time.time();r=ns['audit'](rec)
assert F(r['exact_slack'])*d==F(a['slack_integer_exact'])
report={'status':'PASS','scope':'Independent shared-17-query full-column reconstruction of the 23-integer-weight row; combined with the 17 exact old lifts gives strict cone separation','input_sha256':a['source_sha256'],'pack_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'integer_source_weight':str(d),'integer_u6_weight':a['u6_coefficient_integer'],'integer_K_weight':a['K_coefficient_integer'],'integer_scale_slack':a['slack_integer_exact'],'row':r,'seconds':time.time()-start}
Path(__file__).with_suffix('.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps(report,ensure_ascii=False,indent=2))
