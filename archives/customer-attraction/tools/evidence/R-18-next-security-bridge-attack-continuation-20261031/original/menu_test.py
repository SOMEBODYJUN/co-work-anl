"""Numerical check of enlarged true-first-deviation menu, not general security."""
from pathlib import Path
from itertools import product
import numpy as np,json,sys
from scipy.optimize import linprog
ROOT=Path(__file__).resolve().parents[6];sys.path.insert(0,str(ROOT))
from customer_attraction import Instance
P=Path(__file__).resolve().parent

def menu_cap(g,actions):
    k=g.topic_count;m=g.players
    def terminal(h):
        while len(h)<m:h=h+(actions[h],)
        return h
    actual=terminal(())
    menu=set()
    for i in range(m):
        for a in range(k):
            z=terminal(actual[:i]+(a,));menu.add(tuple(sorted(z[:i]+z[i+1:])))
    bg=sorted(menu); A=np.array([[sum(c.multiplicity/(1+sum(b in c.topics for b in B)) for c in g.customers if a in c.topics) for a in range(k)] for B in bg])
    res=linprog(np.r_[np.zeros(len(bg)),1.],A_ub=np.c_[A.T,-np.ones(k)],b_ub=np.zeros(k),A_eq=np.array([np.r_[np.ones(len(bg)),0]]),b_eq=[1],bounds=[(0,None)]*len(bg)+[(None,None)],method='highs');assert res.success
    W=g.welfare(g.counts(actual));return {'actual':list(actual),'W':W,'menu_size':len(bg),'cap':float(res.x[-1]),'ratio_mcap_W':float(m*res.x[-1]/W),'Q':[[list(B),float(q)] for B,q in zip(bg,res.x[:-1]) if q>1e-9]}

def main():
    report={}
    for ex in (ROOT/'examples/customer_attraction').glob('*.json'):
        cp=ROOT/'evidence/certificates/customer_attraction'/ex.name
        if not cp.exists():continue
        g=Instance.from_dict(json.loads(ex.read_text()));d=json.loads(cp.read_text());s=d.get('strategy')
        if not s:continue
        actions={tuple(r['history']):r['action'] for r in s['actions']}
        if len(actions)!=sum(g.topic_count**j for j in range(g.players)):continue
        report[ex.stem]=menu_cap(g,actions);print(ex.stem,report[ex.stem]['ratio_mcap_W'],report[ex.stem]['menu_size'],flush=True)
    (P/'first_deviation_menu_known_games.json').write_text(json.dumps(report,indent=2))
if __name__=='__main__':main()
