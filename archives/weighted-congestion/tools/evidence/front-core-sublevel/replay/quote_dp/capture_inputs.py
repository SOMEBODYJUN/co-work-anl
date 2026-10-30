import json,runpy,sys
from fractions import Fraction
from pathlib import Path
records=[];seen=set()
def enc(v):
    if isinstance(v,Fraction):return str(v)
    if hasattr(v,'masks') and hasattr(v,'coefficients'):return {'masks':list(v.masks),'coefficients':enc(v.coefficients)}
    if isinstance(v,dict):return {str(k):enc(x) for k,x in v.items()}
    if isinstance(v,(list,tuple)):return [enc(x) for x in v]
    if isinstance(v,(set,frozenset)):return sorted(v)
    return v
def profile(f,event,arg):
    name=f.f_code.co_name
    if name not in ('solve','build','run_case','ratio_min','next_states'):return
    loc=f.f_locals;file=Path(f.f_code.co_filename).name
    if event=='call' and name=='solve' and file=='quote_dp_audit.py':
        records.append({'kind':'QDP solve','game':enc(loc['game']),'bags':enc(loc['bags']),'children':enc(loc['children']),'beta':enc(loc['beta']),'eps':enc(loc['eps'])})
    elif event=='return' and name=='build' and file=='front_quote_audit.py':
        records.append({'kind':'FQDP literal game','test':f.f_back.f_locals['test'],'game':enc(arg[0]),'classes':enc(arg[1]),'RD':enc(arg[2])})
    elif event=='call' and name=='solve' and file=='front_quote_audit.py':
        records.append({'kind':'FQDP solve parameters','domains':enc(loc['domains']),'bags':enc(loc['bags']),'children':enc(loc['children']),'beta':enc(loc['beta']),'eps':enc(loc['eps'])})
    elif event=='return' and name=='run_case' and file=='sparse_repair_audit.py':
        records.append({'kind':'sparse literal game','n':loc['n'],'alpha':enc(loc['alpha']),'p':loc['p'],'epsilon':enc(loc['epsilon']),'degree_override':loc['degree_override'],'degree':loc['D'],'weights':enc(loc['weights']),'allowed_actions':[[0,1] for _ in range(loc['n'])]+[[0]],'base':enc(loc['base']),'gates':enc(loc['gates'])})
    elif event=='call' and file=='audit.py' and f.f_back:
        p=f.f_back;pl=p.f_locals;parent=p.f_code.co_name
        if name=='ratio_min' and parent=='integral_audits':
            key=('integral',pl['_'])
            if key not in seen:
                seen.add(key);records.append({'kind':'integral source game','index':pl['_'],'weights':enc(pl['weights']),'menus':enc(pl['menus']),'polynomials':enc(pl['polynomials']),'seed':enc(pl['seed']),'cap':enc(pl['cap'])})
        elif name=='next_states' and parent=='transfer_audits':
            key=('tail',pl['_'])
            if key not in seen:
                seen.add(key);records.append({'kind':'high-degree tail game','index':pl['_'],'weights':enc(pl['weights']),'menus':enc(pl['menus']),'polynomials':enc(pl['orig']),'seed':enc(pl['seed']),'cap':enc(pl['cap']),'degree':pl['d'],'kappa':enc(pl['kappa']),'alpha':enc(pl['alpha'])})
sys.setprofile(profile)
try:runpy.run_path(sys.argv[1],run_name='__main__')
finally:
    sys.setprofile(None)
    Path('actual-game-inputs.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n')
