#!/usr/bin/env python3
"""Narrow exact replay of five frozen heterogeneous fixtures and verifier scope.
No assertion here is a universal existence theorem.
"""
from pathlib import Path
from fractions import Fraction as Q
import argparse,json,copy,hashlib
from facility_spe import heterogeneous_two as h
from facility_spe.exact import bounded_overlap as exact
from facility_spe.examples.tight_two import instance


def render(v):
    if isinstance(v,Q):return str(v)
    if isinstance(v,(tuple,list)):return [render(x) for x in v]
    if isinstance(v,dict):return {str(k):render(x) for k,x in v.items()}
    return v


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args()
    root=Path(__file__).resolve().parent;fixtures=root/'original/examples/heterogeneous'
    records=[]
    for f in sorted(fixtures.rglob('*.json')):
        data=json.loads(f.read_text());w,s,u1,u2=h.parsed(data)
        out=h.solve(data);larger=h.solve(data,maximum_only=False);opt=exact.solve(data)
        if not h.verify(data,json.loads(json.dumps(h.serial(out)))):raise RuntimeError('verify returned false')
        if not opt['finite_factor_exists']:raise RuntimeError('fixture had no finite optimum')
        if opt['alpha']>out['alpha']:raise RuntimeError('menu beat true optimum')
        default=[];matrix=[]
        for a in u1:
            row=[]
            for b in u2:
                menu=h.make_menu(w,s,a,b);p=h.guarded_repair(menu['A'],menu['B'],menu['weights'],(1,)*len(menu['weights']))
                if p is None or not h.is_ne(menu['A'],menu['B'],menu['weights'],p):raise RuntimeError('default was invalid')
                default.append({'layout':[a,b],'prob_first':p,'loads':h.load_pair(menu['A'],menu['B'],menu['weights'],p)})
                loc=exact.local(w,s,a,b)
                row.append({'layout':[a,b],'shared':loc['shared'],'first_load_intervals':[[z['lo'],z['hi']] for z in loc['pieces']], 'first_min':loc['min_piece']['lo'],'first_max':loc['max_piece']['hi'],'second_min':loc['total']-loc['max_piece']['hi']})
            matrix.append(row)
        records.append({'file':str(f.relative_to(root)),'raw_sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'kappa':opt['kappa'],'menus_maximum_only':out,'menus_all_singletons':larger,'exact_mixed_optimum':opt,'complete_default_rule':default,'local_spectra':matrix})
    rho=next(r for r in records if r['file'].endswith('rho_lower.json'))
    certificate=copy.deepcopy(rho['menus_maximum_only']);data=json.loads((fixtures/'rho_lower.json').read_text())
    # Meaningful certificate checks remain active even under python -O.
    rejected={}
    changes={
      'wrong_load':lambda c:c['on_path']['loads'].__setitem__(0,c['on_path']['loads'][0]+1),
      'missing_deviation':lambda c:c['deviations'].pop(),
      'duplicate_deviation':lambda c:c['deviations'].append(copy.deepcopy(c['deviations'][0])),
      'non_pure_assignment':lambda c:c['on_path']['prob_first'].__setitem__(0,Q(1,2)),
      'illegal_layout':lambda c:c['on_path'].__setitem__('layout',[2,2]),
      'too_small_factor':lambda c:c.__setitem__('alpha',Q(1)),
    }
    for name,change in changes.items():
        c=copy.deepcopy(certificate);change(c)
        try:h.verify(data,c)
        except (ValueError,TypeError,KeyError):rejected[name]=True
        else:raise RuntimeError('corruption accepted '+name)
    unverified=['finite_factor_exists','guarantee','seed_mode','response_cycle','pair_count','menu_entry_count','default_continuation']
    metadata=copy.deepcopy(certificate)
    for k in unverified:metadata[k]='arbitrary unchecked metadata'
    if not h.verify(data,metadata):raise RuntimeError('metadata probe returned false')
    saved=h.make_menu;h.make_menu=lambda *a,**k:(_ for _ in ()).throw(RuntimeError('forbidden menu call'))
    try:
        independent_of_menu=h.verify(data,certificate)
    finally:h.make_menu=saved
    families=[]
    for m in [5,6,10,1000]:
        data=instance(m);a=exact.solve(data);b=h.solve(data);expected=Q(2*m+10,m+14)
        if a['alpha']!=expected or b['alpha']!=expected or a['kappa']!=2:raise RuntimeError('family mismatch')
        families.append({'M':m,'expected':expected,'exact':a['alpha'],'menu':b['alpha'],'kappa':a['kappa']})
    first=json.loads((fixtures/'tight_two_M1000.json').read_text());second=json.loads((fixtures/'tight_two_undirected_M1000.json').read_text())
    if first!=second or first!=instance(1000):raise RuntimeError('semantic duplicate mismatch')
    graph=first['locations'];symmetric=all((a in graph[b])==(b in graph[a]) for a in range(6) for b in range(6))
    report={'scope':'five exact frozen fixtures; full local support enumeration per fixture, four family parameters, six corruptions, metadata acceptance and default queries; no universal factor-2 theorem','fixtures':records,'family_parameter_checks':families,'two_M1000_files_equal_as_json':first==second,'M1000_generator_matches':first==instance(1000),'six_vertex_incidence_symmetric':symmetric,'corruptions_rejected':rejected,'verify_does_not_call_make_menu':independent_of_menu,'unchecked_metadata_fields_accept_arbitrary_strings':unverified,'optimization_flag':__debug__}
    Path(args.output).write_text(json.dumps(render(report),ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'fixtures':[{'file':r['file'],'exact_optimum':str(r['exact_mixed_optimum']['alpha']),'menu_factor':str(r['menus_maximum_only']['alpha']),'cycle':r['menus_maximum_only']['response_cycle'],'kappa':r['kappa']} for r in records],'family_checks':render(families),'corruptions_rejected':rejected,'__debug__':__debug__},indent=2))
if __name__=='__main__':main()
