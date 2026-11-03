"""Candidate generation on fixed complete-history SPE cones; no universal theorem."""
import gzip,json,sys,importlib.util,argparse,time
from pathlib import Path
from fractions import Fraction
from itertools import combinations
import numpy as np
from scipy.optimize import linprog
ROOT=Path(__file__).resolve().parents[5]
spec=importlib.util.spec_from_file_location('floor_lp',ROOT/'tests/audits/customer_attraction_strategy_lp.py')
lib=importlib.util.module_from_spec(spec);sys.modules[spec.name]=lib;spec.loader.exec_module(lib)
OUT=Path(__file__).resolve().parent

def exact_vertex(cone,res):
    values=tuple(Fraction(float(v)).limit_denominator(10**7) for v in res.x[:len(cone.welfare)])
    if not cone.verify(values):
        values=cone.recover_vertex(res.x[:len(cone.welfare)])
    return values

def probe(cone,name):
    h=();path=[]
    while len(h)<cone.players:
        a=cone.actions[h];path.append(a);h+=(a,)
    G=-cone.matrix;zero=np.zeros(len(cone.rows));w=np.array(cone.welfare,float)
    best={'floor':-1.0,'kplus':-1.0,'missing':-1.0};records=[]
    for a in sorted(set(path)):
        u=np.array(lib.payoff_row(cone.topics,cone.root,a),float)
        local=(-1,None)
        for J in combinations(range(cone.topics),min(cone.topics,cone.players)):
            o=np.array(lib.coverage_row(cone.topics,J),float)
            # All objectives homogeneous. W=1 normalization enables exact recovery.
            obj=o-2*cone.players*u
            res=linprog(-obj,A_ub=G,b_ub=zero,A_eq=[w],b_eq=[1],bounds=(0,None),method='highs')
            if not res.success:raise RuntimeError(res.message)
            if -res.fun>local[0]:local=(-res.fun,J)
            if -res.fun>best['floor']:best['floor']=-res.fun
            # K is a new LP variable, constrained above every theme size.
            rows=np.zeros((len(G)+cone.topics,len(w)+1));rows[:len(G),:-1]=G
            for b in range(cone.topics):rows[len(G)+b,:-1]=[int(mask>>b&1) for mask in range(1,1<<cone.topics)];rows[len(G)+b,-1]=-1
            objective=np.r_[o-cone.players*u,-1]
            kres=linprog(-objective,A_ub=rows,b_ub=np.zeros(len(rows)),A_eq=[np.r_[w,0]],b_eq=[1],bounds=(0,None),method='highs')
            if not kres.success:raise RuntimeError(kres.message)
            best['kplus']=max(best['kplus'],-kres.fun)
            # OPT-W<=m ui, the current public candidate, distinct from weakfloor.
            mobj=o-w-cone.players*u
            mres=linprog(-mobj,A_ub=G,b_ub=zero,A_eq=[w],b_eq=[1],bounds=(0,None),method='highs')
            if not mres.success:raise RuntimeError(mres.message)
            best['missing']=max(best['missing'],-mres.fun)
            for typ,r,obj2 in [('floor',res,obj),('missing',mres,mobj),('kplus',kres,objective)]:
                if -r.fun<=1e-7:continue
                values=exact_vertex(cone,r)
                if values is None or not cone.verify(values) or lib.dot(cone.welfare,values)!=1:continue
                if typ=='kplus':
                    K=max(sum(v for mask,v in enumerate(values,1) if mask>>b&1) for b in range(cone.topics))
                    val=lib.dot(lib.coverage_row(cone.topics,J),values)-cone.players*lib.dot(lib.payoff_row(cone.topics,cone.root,a),values)-K
                else:val=lib.dot(tuple(Fraction(x) for x in obj2),values)
                if val<=0:continue
                clones=lib.integer_clones(values)
                assert lib.independently_verify(cone,clones)
                record={'name':name,'type':typ,'a':a,'path':path,'portfolio':J,'value':str(val),'clones':clones,'actions':[{'history':h,'action':b} for h,b in cone.actions.items()]}
                target=OUT/f'candidate_{name}_{typ}_{a}.json';target.write_text(json.dumps(record,indent=2))
                print('FOUND',target,flush=True)
        records.append({'a':a,'max_floor':local[0],'portfolio':local[1]})
    out={'name':name,'players':cone.players,'topics':cone.topics,'path':path,'rows':len(G),'best':best,'players_checked':records}
    print(json.dumps(out),flush=True)
    return out

def sources():
    for name in ['individual_security_failure','root_tax_failure']:
        d=json.loads((ROOT/f'evidence/certificates/customer_attraction/{name}.json').read_text())
        acts={tuple(x['history']):x['action'] for x in d['strategy']['actions']}
        p=max(max(h,default=0) for h in acts)+1;n=max(map(len,acts))+1
        yield name,lib.StrategyCone(p,n,acts)
    for d in json.load(gzip.open(ROOT/'evidence/certificates/customer_attraction/new_policy_security_cones.json.gz','rt'))['cases']:
        acts={tuple(x['history']):x['action'] for x in d['policy']}
        yield d['name'],lib.StrategyCone(d['topics'],d['players'],acts)

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--limit',type=int,default=100);args=ap.parse_args()
    records=[]
    for i,(name,cone) in enumerate(sources()):
        if i>=args.limit:break
        records.append(probe(cone,name));(OUT/'cone_probe_results.json').write_text(json.dumps(records,indent=2))
