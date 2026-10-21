"""Discover only: full ordered-policy cones versus B(min actual payoff)<=W.

Each fixed nonnegative query menu z gives a linear necessary price inequality.
LP retains every ordered history incentive and the actual payoff minimum rows.
"""
from pathlib import Path
import importlib.util
import itertools
import json
import math
import argparse
import numpy as np
from scipy.optimize import linprog

ROOT = Path(__file__).resolve().parents[5]
HELPER = ROOT / 'research/workspaces/customer-attraction/R-64201cd12083425899e2d643ec9bc087/round3_boss/cone_opportunity_attack.py'
spec=importlib.util.spec_from_file_location('oldcone', HELPER)
helper=importlib.util.module_from_spec(spec)
spec.loader.exec_module(helper)

def attack(label, cert, subsets=False):
    data=helper.prepare(cert)
    if data is None:
        return None
    p,m,masks,member,actions,terminal,root,path,payoff,rows,w=data
    menus=[]
    for size in (range(2,p+1) if subsets else [p]):
        for support in itertools.combinations(range(p),size):
            deg=member[list(support)].sum(axis=0)
            for d in range(1,size+1):
                menus.append((support,d,np.minimum(1,deg/d),size/d))
    best={'max_violation':-math.inf}
    for a in sorted(set(path)):
        ua=payoff(root,a)
        mins=np.array([ua-payoff(root,b) for b in sorted(set(path)) if a!=b])
        aub=np.vstack((rows,mins)) if len(mins) else rows
        for support,d,cov,tau in menus:
            target=cov-tau*ua-w
            ans=linprog(-target,A_ub=aub,b_ub=np.zeros(len(aub)),A_eq=np.ones((1,len(masks))),b_eq=[1],bounds=(0,None),method='highs')
            if ans.success and -ans.fun>best['max_violation']+1e-12:
                best={'max_violation':float(-ans.fun),'minimum_topic':a,'support':support,'divisor':d,'weights':{str(mask):float(v) for mask,v in zip(masks,ans.x) if v>1e-9}}
    return {'source':label,'players':m,'topics':p,'histories':len(actions),'actual_path':path,**best}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--subsets',action='store_true');ap.add_argument('--limit',type=int,default=99999);ap.add_argument('--output',type=Path,required=True);args=ap.parse_args()
    reports=[]
    for source in sorted((ROOT/'evidence/certificates/customer_attraction').glob('*.json')):
        for label,cert in helper.policies(json.loads(source.read_text()),str(source.relative_to(ROOT))):
            report=attack(label,cert,args.subsets)
            if report:
                reports.append(report)
                print(json.dumps({k:v for k,v in report.items() if k!='weights'}),flush=True)
                args.output.write_text(json.dumps({'status':'finite numerical fixed-policy cone exploration only','reports':reports},indent=2)+'\n')
                if report['max_violation']>1e-7 or len(reports)>=args.limit:return
if __name__=='__main__':main()
