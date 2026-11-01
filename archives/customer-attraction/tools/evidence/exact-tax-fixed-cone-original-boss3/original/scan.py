"""Candidate search for the OPEN exact-tax bridge in already published SPE cones.

LP is discovery only. A positive witness must pass exact Fraction cone checks.
No claim is made from nonpositive floating LP answers or this finite cone list.
"""
from pathlib import Path
from fractions import Fraction as F
import sys, json, hashlib
import numpy as np
from scipy.optimize import linprog

ROOT = next(p for p in Path(__file__).resolve().parents if (p/'customer_attraction/__init__.py').is_file())
sys.path.insert(0,str(ROOT/'tests/audits'))
from customer_attraction_strategy_lp import StrategyCone, dot, serializable, integer_clones

def get_actions(o):
    if not isinstance(o,dict): return None
    for key in ('strategy','certificate'):
        if key in o:
            a=get_actions(o[key])
            if a: return a
    a=o.get('actions')
    if not isinstance(a,list) or not a: return None
    try:
        if isinstance(a[0],dict): return {tuple(x['history']):x['action'] for x in a}
        return {tuple(h):v for h,v in a}
    except (KeyError,ValueError,TypeError): return None

def run():
    paths=sorted((ROOT/'evidence/certificates/customer_attraction').glob('*.json'))
    paths+=sorted((ROOT/'research/workspaces/customer-attraction').rglob('*.json'))
    seen=set(); records=[]; best=None
    for path in paths:
        if Path(__file__).parent in path.parents: continue
        try: o=json.loads(path.read_text())
        except (OSError,ValueError):continue
        actions=get_actions(o)
        if not actions: continue
        m=max(map(len,actions))+1
        p=max(max(actions.values()),max((max(h) for h in actions if h),default=0))+1
        if p>7 or m>5 or len(actions)>3000:continue
        key=hashlib.sha256(repr(sorted(actions.items())).encode()).hexdigest()
        if key in seen:continue
        seen.add(key)
        try:cone=StrategyCone(p,m,actions)
        except ValueError:continue
        loads=[sum(cone.root[a] for a in range(p) if mask>>a&1) for mask in range(1,1<<p)]
        gc=tuple(F(int(c>0))/(1+F(m-1,m)*c) for c in loads)
        scores=[]
        for a in range(p):
            ga=tuple(F(int(mask>>a&1))/(1+F(m-1,m)*c) for mask,c in zip(range(1,1<<p),loads))
            obj=tuple(m*x-y-z for x,y,z in zip(ga,cone.welfare,gc))
            res=linprog(-np.array(obj,dtype=float),A_ub=-cone.matrix,b_ub=np.zeros(len(cone.rows)),A_eq=[cone.welfare],b_eq=[1],bounds=(0,None),method='highs')
            if not res.success:
                scores.append({'query':a,'status':res.message});continue
            values=tuple(F(float(x)).limit_denominator(10**7) for x in res.x)
            if not cone.verify(values) or dot(cone.welfare,values)!=1:values=cone.recover_vertex(res.x)
            exact=values is not None and cone.verify(values) and dot(cone.welfare,values)==1
            scores.append({'query':a,'gap':dot(obj,values) if exact else None,'floating_gap':-res.fun,'exact_primal':exact})
            if exact and (best is None or dot(obj,values)>best['gap']):
                best={'source':str(path.relative_to(ROOT)),'m':m,'p':p,'query':a,'gap':dot(obj,values),'root':cone.root,'integer_clones':integer_clones(values),'actions':[{'history':list(h),'action':v} for h,v in actions.items()]}
                (Path(__file__).parent/'best.json').write_text(json.dumps(serializable(best),indent=2)+'\n')
            if exact and dot(obj,values)>0:
                print(json.dumps(serializable({'POSITIVE':best})),flush=True)
                return
        r={'source':str(path.relative_to(ROOT)),'m':m,'p':p,'root':cone.root,'scores':scores}
        records.append(r)
        print(json.dumps(serializable({'source':r['source'],'best_gap':max((s['gap'] for s in scores if s.get('exact_primal')),default=None)})),flush=True)
        (Path(__file__).parent/'results.json').write_text(json.dumps(serializable({'status':'finite fixed-cone attack only','records':records}),indent=2)+'\n')
    print(json.dumps(serializable({'done':len(records),'best':best})),flush=True)

if __name__=='__main__':run()
