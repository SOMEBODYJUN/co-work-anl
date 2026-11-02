"""Apply sibling's independently derived transport cuts to new717-row point."""
from fractions import Fraction as F
import sys,json
from full_pricing import HERE,ACTOR
sys.path.insert(0,str(ACTOR/'round4_coupling'))
from joint_transport import frozen_report
from pair_transport import evaluate
path=HERE/'exact_primal_cross_pair.json';doc=json.loads(path.read_text());atoms=doc['atoms'];mass=[F(a['exact_mass']) for a in atoms]
joint=frozen_report(atoms,mass);pair=evaluate(path)
report={'scope':'Additional necessary-condition separation only; no SPE counterexample','joint_terminal':joint,'cross_pair':pair}
(HERE/'cross_point_separation.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:{'negative_rows':len(v['negative_rows']),**({'negative_despite_both_components_nonnegative':len(v['negative_despite_both_component_envelopes_nonnegative'])} if k=='joint_terminal' else {'minimum':v['minimum']})} for k,v in report.items() if isinstance(v,dict)},indent=2),flush=True)
