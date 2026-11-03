"""Can the frozen template primal support a genuine max-branch last menu?

No game/SPE conclusion: this tests extension by aggregate necessary rows.
New variables disintegrate each frozen atom over all five-index (T,R)
membership histograms, preserving its old exact mass.
"""
from pathlib import Path
from fractions import Fraction as F
import json
import numpy as np
from scipy.optimize import linprog

ROOT=next(p for p in Path(__file__).resolve().parents if (p/'AGENTS.md').exists())
SRC=ROOT/'research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round13/certificate/exact_max_menu_tuple_primal.json'
PATHS={'actual':('ABCDE',0),'second':('AEUVW',2),'third':('ABEXY',3)}
LABELS='ABCDEUVWXY'


def q(a,b):return F(a,b) if a else F(0)
def aa(k):return 8*(k-1)+k*k


def rows(atom,ell,h,mode):
    bits=dict(zip(LABELS,map(int,atom['bits'])))
    mb=tuple(map(int,atom['max_bits']));m=mb[0]
    d=sum(atom['AB_hist'][4:]);p=sum(mb[:3]);tot=sum(mb)
    v4=q(mb[3],tot);v5=q(mb[4],tot);den=(p+1)*(p+2)
    rr={
       'penult_true':5*v4-q(d,p+1)+q(h,den),
       'last_actual_menu':5*v5-q(ell,p+mb[3]+1),
       'reply_cross':q(d*ell-5*h,den),
       'reply_self':q(ell,p+1)-q(h,den)-q(d,p+2),
       'menu_max_cap':5*m-ell,
    }
    for tag,x in list(bits.items())+[(f'M{i}',x) for i,x in enumerate(mb)]:
        rr[f'reply_BR:{tag}']=q(ell,p+1)-q(h,den)-q(5*x,p+1)+q(x*d,den)
    nodes=[]
    for pn,(path,start) in PATHS.items():
        bb=[bits[t] for t in path];load=sum(bb)
        for i in range(start,5):nodes.append((f'{pn}:{i}',q(bb[i],load),sum(bb[:i]),5-i))
    for i in range(1,5):nodes.append((f'max:{i}',q(mb[i],tot),sum(mb[:i]),5-i))
    fixed=list(bits.items())+[(f'M{i}',x) for i,x in enumerate(mb)]+[('opt',d)]
    for tag,u,pre,k in nodes:
        rr[f'floor:{tag}']=5*u-q(ell,pre+k)
        if mode=='ap':
            a=aa(k)
            for lab,c in fixed:
                nc=5 if lab=='opt' else 1
                rr[f'AP:R:{lab}:{tag}']=5*nc*a*u-q((a-2)*nc*ell+2*ell*c,pre+k)-q(2*(5*c-ell*c),pre+1)
                rr[f'AP:{lab}:R:{tag}']=5*nc*a*u-q((a-2)*5*c+2*c*ell,pre+k)-q(2*(nc*ell-c*ell),pre+1)
            rr[f'AP:R:R:{tag}']=25*a*u-q((a-2)*5*ell+2*ell*ell,pre+k)-q(2*(5*ell-ell*ell),pre+1)
    return rr


def main():
    data=json.loads(SRC.read_text());atoms=data['atoms']
    out={'scope':'fixed-primal extension feasibility only; not a game or SPE','source':str(SRC.relative_to(ROOT)),'results':[]}
    for mode in ('basic','ap'):
        choices=[];cols=[];names=None
        for i,atom in enumerate(atoms):
            d=sum(atom['AB_hist'][4:])
            for ell in range(6):
                for h in range(max(0,d+ell-5),min(d,ell)+1):
                    rr=rows(atom,ell,h,mode)
                    if names is None:names=list(rr)
                    assert names==list(rr)
                    choices.append((i,ell,h));cols.append([float(rr[n]) for n in names])
        mat=np.array(cols).T
        eq=np.zeros((len(atoms),len(cols)))
        for j,(i,_,_) in enumerate(choices):eq[i,j]=1
        mass=np.array([float(F(a['exact_mass'])) for a in atoms])
        z=linprog(np.zeros(len(cols)),A_ub=-mat,b_ub=np.zeros(len(names)),A_eq=eq,b_eq=mass,bounds=(0,None),method='highs')
        rec={'mode':mode,'rows':len(names),'choices':len(cols),'success':bool(z.success),'message':z.message}
        if z.success:rec['minimum_slack']=float((mat@z.x).min())
        if mode=='basic' and not z.success:
            # Convex separating certificate: lambda>=0, sum lambda=1,
            # y_i >= max_choice lambda.dot(row_i(choice)). Negative mass.y
            # excludes every permitted splitting of the frozen atom masses.
            nr=len(names);na=len(atoms)
            cons=np.zeros((len(cols),nr+na));cons[:,:nr]=mat.T
            for j,(i,_,_) in enumerate(choices):cons[j,nr+i]=-1
            cost=np.concatenate([np.zeros(nr),mass]);norm=np.zeros((1,nr+na));norm[0,:nr]=1
            dz=linprog(cost,A_ub=cons,b_ub=np.zeros(len(cols)),A_eq=norm,b_eq=[1.],bounds=[(0,None)]*nr+[(None,None)]*na,method='highs')
            rec['dual_success']=bool(dz.success)
            if dz.success:
                lam=[F(float(x)).limit_denominator(10**7) for x in dz.x[:nr]]
                values=[None]*na
                for (i,ell,h) in choices:
                    rr=rows(atoms[i],ell,h,mode)
                    v=sum((l*rr[n] for l,n in zip(lam,names)),F(0))
                    if values[i] is None or v>values[i]:values[i]=v
                deficit=sum((F(a['exact_mass'])*v for a,v in zip(atoms,values)),F(0))
                rec['exact_separator']={'lambda':{n:str(l) for n,l in zip(names,lam) if l},'weighted_maximum':str(deficit),'weighted_maximum_float':float(deficit),'verified_negative':bool(deficit<0)}
        out['results'].append(rec)
    print(json.dumps(out,indent=2))


if __name__=='__main__':main()
