"""Seven real last-player menu ICs, priced under five shared load layers.

Every old family uses the same ell=sum(max first-four bits). The complete
32-state max block is restricted to that ell before its argmax. Float only.
"""
import sys,json
import numpy as np
import max_menu_tuple_pricing as mt
import max_menu_joint_pricing as mj
import menu_ap_pricing as mp
import lift_maximum_branch as lm
LAST=[(f'{g}:MaxLast:{m}',g,m) for g,menus in mp.MENUS.items() for m in menus]
def last_rows(a,mb):
    ans={};p=sum(mb[:4]);u=lm.q(mb[4],sum(mb))
    for name,g,m in LAST:
        j=mp.MENUS[g].index(m)+1;k=4 if g=='Sbranch' else 3;c=sum(n*t[j] for n,t in zip(a[mp.FIELDS[g]],mp.TYPES[k]));ans[name]=5*u-lm.q(c,p+1)
    return ans
class Universe(mt.Universe):
    def __init__(self):
        super().__init__();self.names +=[z[0] for z in LAST];self.maxnames +=[z[0] for z in LAST];self.layer=None
        print(json.dumps({'true_max_last_menu_rows':len(LAST),'total_rows':len(self.names)}),flush=True)
    def atom_rows(self,a):
        rr=super().atom_rows(a);rr.update(last_rows(a,tuple(map(int,a['max_bits']))));return rr
    def block_coeff(self,name):
        if ':MaxLast:' not in name:return super().block_coeff(name)
        total=self.SMB.sum(1);return 5*np.divide(self.SMB[:,4],total,out=np.zeros(32),where=total>0)[None,None,:]
    def maximum_scores(self,lam):
        score=super().maximum_scores(lam);assert self.layer in range(5);score[:,:,self.SMB[:,:4].sum(1)!=self.layer]=-1e100;return score
    def family_score(self,bits,tag,weights,integer=False):
        last=[(n,v) for n,v in weights if ':MaxLast:' in n];rest=[(n,v) for n,v in weights if ':MaxLast:' not in n]
        key,const,vec,me,mh=super().family_score(bits,tag,rest,integer=integer);co=[]
        for n,v in last:
            menu=n.split(':')[-1];co.append((menu,v));vec.append((-120*v/(self.layer+1),self.countarr[tag][menu]))
        return (key[0],key,self.layer,tuple(co)),const,vec,me,mh
    def price(self,lam,beta,batch=80,**kw):
        minimum=None;allcols=[];contexts=0
        for ell in range(5):
            self.layer=ell;value,cols,count=super().price(lam,beta,batch=batch,**kw);minimum=value if minimum is None else min(minimum,value);allcols+=cols;contexts+=count
        allcols.sort(key=lambda z:z[0]);seen=set();chosen=[]
        for v,a in allcols:
            key=mp.atom_key(a)+(a['max_bits'],)
            if key not in seen:chosen.append((v,a));seen.add(key)
            if len(chosen)>=batch:break
        self.layer=None;return minimum,chosen,contexts
if __name__=='__main__':mj.run(int(sys.argv[1]) if len(sys.argv)>1 else 8,Universe,'max_menu_last_discovery.json','max_menu_tuple_discovery.json')
