"""Rebuild both complete 66-node phases from a newly supplied exact point.

This does not transfer any old slack or assert IC feasibility.  All interval
atoms and own four-state marginals are recomputed using the new Fraction data.
"""
from __future__ import annotations
import sys
sys.dont_write_bytecode=True
import argparse,json
from fractions import Fraction as F
from itertools import permutations
from pathlib import Path
from common import *

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--point',type=Path,required=True)
    ap.add_argument('--output',type=Path,required=True);args=ap.parse_args()
    point,cols,masses,hist,groups,ov,families=parse(args.point)
    phases={}
    for phase in ('A','B'):
        entries=[]
        for hi,h in hist.items():
            H=masses[hi];ws=words(h);defs=[];endpoints={F(),H}
            for e in NODES:
                a,b,c,d=marg(hi,groups[hi][ng(e,ws)],masses)
                q=c+d;v=b+d;t=d
                if phase=='A' or e[0]==0:
                    rr=((F(),q),);zz=((F(),t),(q,q+v-t))
                else:
                    rr=((F(),t),(v,v+q-t));zz=((F(),v),)
                assert all(0<=a<=b<=H for a,b in rr+zz)
                defs.append((rr,zz));endpoints.update(x for ab in rr+zz for x in ab)
            ends=sorted(endpoints);atoms=[];sums=[[F() for _ in range(4)] for _ in NODES]
            for left,right in zip(ends,ends[1:]):
                u=(left+right)/2;states=[]
                for k,(rr,zz) in enumerate(defs):
                    r=int(any(a<=u<b for a,b in rr));z=int(any(a<=u<b for a,b in zz));s=2*r+z
                    states.append(s);sums[k][s]+=right-left
                atoms.append({'mass':str(right-left),'states':states})
            for k,e in enumerate(NODES):assert tuple(sums[k])==marg(hi,groups[hi][ng(e,ws)],masses)
            entries.append({'hist_column':hi,'P':sum(map(int,h['actual_bits'][:4])),
                'actual_bits':h['actual_bits'],'hist':h['hist'],'mass':str(H),
                'interval_breakpoints':list(map(str,ends)),
                'node_intervals':[{'literal':e,'R':[[str(a),str(b)] for a,b in rr],
                    'Z':[[str(a),str(b)] for a,b in zz]} for e,(rr,zz) in zip(NODES,defs)],
                'atoms':atoms})
        phases[phase]=entries
    out=meta(args.point)|{'source_sha256':sha(Path(__file__)),
        'scope':'Two exact common candidates preserving all own marginals at this point; IC feasibility is checked separately',
        'W':point['W'],'literal_node_order':NODES,'phase_A_weight':'1/2','phase_B_weight':'1/2',
        'symmetrization':{'permutations':list(permutations(range(6))),
            'mass_rule':'phase_weight * atom.mass / 720',
            'state_rule':'move base node (f,i,j) to (f,pi(i),pi(j)) and move old words by the same pi'},
        'phases':phases,'base_atoms':{p:sum(len(h['atoms']) for h in phases[p]) for p in phases},
        'expanded_positive_atoms':720*sum(len(h['atoms']) for p in phases for h in phases[p])}
    dump(args.output,out)
    print(json.dumps({k:v for k,v in out.items() if k not in ('phases','symmetrization','literal_node_order')},ensure_ascii=False))

if __name__=='__main__':main()
