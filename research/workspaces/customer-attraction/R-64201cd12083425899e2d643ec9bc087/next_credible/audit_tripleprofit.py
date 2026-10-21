"""Definition-level check of retained-coordinate row formulas on complete SPEs.
The universal necessity is proved in README; these finite fixtures test formulas.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import combinations,combinations_with_replacement,product
import json,sys
from offdiagonal_probe import rows as offrows,types,quads
from crossmenu_probe import rows as crossrows
from menutax_probe import rows as taxrows
from alignedtax_probe import rows as alignrows
from tripleprofit_probe import rows as triplerows
ROOT=Path(__file__).resolve().parents[5];sys.path.insert(0,str(ROOT))
from customer_attraction import Instance,StrategyCertificate,verify_certificate

def audit(path):
 data=json.loads(path.read_text());inst=Instance.from_dict(data['instance']);cert=StrategyCertificate.from_dict(data['certificate']);check=verify_certificate(inst,cert);check.assert_valid();act=cert.actions
 def cont(h):
  while len(h)<5:h=h+(act[h],)
  return h
 s=cont(());A,B,C,D,E=s;second=cont((A,E));third=cont((A,B,E));fixed=s+second[2:]+third[3:];assert len(fixed)==10
 opt=max(combinations(range(inst.topic_count),5),key=lambda ts:inst.welfare(inst.counts(ts)))
 prefs=[s[:3],second[:3],third[:3]];old=[[act[pr+(t,)] for t in opt] for pr in prefs]
 AB=[cont((A,B,t)) for t in opt];AE=[cont((A,E,t)) for t in opt];S=[cont((A,t)) for t in opt]
 menus={l:[t] for l,t in zip('ABCDEUVWXY',fixed)};menus['T']=list(opt)
 for i,L in enumerate(old):menus['L'+str(i)]=L
 for tag,ps,first,names in [('AB',AB,3,'XY'),('AE',AE,3,'XY'),('Sbranch',S,2,'UVW')]:
  for i,n in enumerate(names):menus[tag+':'+n]=[p[first+i] for p in ps]
 atoms=[]
 for cu in inst.customers:
  ts=cu.topics;bits=''.join(str(int(t in ts)) for t in fixed);hists=[]
  for ps,first,tys in [(AB,3,types),(AE,3,types),(S,2,quads)]:
   hist=[0]*len(tys)
   for i,p in enumerate(ps):hist[tys.index((int(opt[i] in ts),)+tuple(int(t in ts) for t in p[first:]))]+=1
   hists.append(hist)
  lh=[[sum(t in ts for t in L),sum(t in ts and t0 in ts for t,t0 in zip(L,opt))] for L in old]
  atoms.append((cu.multiplicity,{'bits':bits,'AB_hist':hists[0],'AE_hist':hists[1],'second_hist':hists[2],'menus_lh':lh}))
 def payoff(p,i):return inst.player_payoffs(p)[i]
 def floor(prefix,t):
  return sum((F(cu.multiplicity,int(sum(a in cu.topics for a in prefix))+5-len(prefix)) for cu in inst.customers if t in cu.topics),F())
 def tax(prefix,a,b):
  ans=F()
  for cu in inst.customers:
   d=sum(t in cu.topics for t in prefix);n=int(a in cu.topics)+int(b in cu.topics)
   if n:ans+=F(cu.multiplicity*n,d+n)
  return ans
 def H(p):
  z=payoff(p,3)+payoff(p,4)
  for cu in inst.customers:
   if p[3] in cu.topics:
    d=sum(t in cu.topics for t in p[:3]);z+=F(cu.multiplicity,(d+1)*(d+2))
  return z
 direct={}
 for f,(pn,p) in enumerate(zip(('actual','second','third'),(s,second,third))):
  direct[pn+':old-last:off-T']=sum((payoff(prefs[f]+(opt[i],old[f][i]),4)-floor(prefs[f]+(opt[i],),opt[j]) for i in range(5) for j in range(5) if i!=j),F())
 for tag,ps,first,names in [('AB',AB,3,'XY'),('AE',AE,3,'XY'),('Sbranch',S,2,'UVW')]:
  local={'T':list(opt)};local.update({n:menus[tag+':'+n] for n in names})
  for po in range(len(names)):
   idx=first+po
   for n,L in local.items():direct[f'{tag}:node-{po+1}:off-{n}']=sum((payoff(p,idx)-floor(p[:idx],L[j]) for i,p in enumerate(ps) for j in range(5) if i!=j),F())
   for mn,L in menus.items():
    if len(L)==5 and mn!='T':direct[f'{tag}:node-{po+1}:crossmenu-{mn}']=sum((payoff(p,idx)-floor(p[:idx],t) for p in ps for t in L),F())
 groups=[(pn,[p]) for pn,p in zip(('actual','second','third'),(s,second,third))]+[('AB',AB),('AE',AE),('Sbranch',S)]
 pairs=[('T','L'+str(i)) for i in range(3)]
 for tag,ns in [('AB','XY'),('AE','XY'),('Sbranch','UVW')]:
  ms=['T']+[tag+':'+n for n in ns];pairs+=list(combinations_with_replacement(ms,2))
 for tag,ps in groups:
  for ma,mb in combinations_with_replacement(menus,2):direct[f'{tag}:newtax:{ma}|{mb}']=sum((H(p)-tax(p[:3],a,b) for p in ps for a in menus[ma] for b in menus[mb]),F())
  for ma,mb in pairs:
   direct[f'{tag}:align-tax:{ma}|{mb}']=sum((H(p)-tax(p[:3],menus[ma][i],menus[mb][i]) for p in ps for i in range(5)),F())
   direct[f'{tag}:off-tax:{ma}|{mb}']=sum((H(p)-tax(p[:3],menus[ma][i],menus[mb][j]) for p in ps for i in range(5) for j in range(5) if i!=j),F())
 def profit(prefix,tri):
  return sum((F(cu.multiplicity*sum(t in cu.topics for t in tri),sum(t in cu.topics for t in prefix+tri)) for cu in inst.customers if any(t in cu.topics for t in tri)),F())
 for source,ns in [('AB','TXY'),('AE','TXY'),('Sbranch','TUVW')]:
  lm=[menus['T']]+[menus[source+':'+n] for n in ns[1:]]
  for positions in combinations_with_replacement(range(len(ns)),3):
   title=source+':'+''.join(ns[i] for i in positions)
   triples=[tuple(lm[pos][i] for pos in positions) for i in range(5)]
   for group,p in [('AB',s),('AE',second)]:
    direct[f'{group}:three-profit:{title}']=sum((F(5,3)*sum(inst.player_payoffs(p)[2:])-profit(p[:2],tri) for tri in triples),F())
   for mode in ('all','align','off'):
    direct[f'Sbranch:three-profit-{mode}:{title}']=sum((F(5,3)*sum(inst.player_payoffs(p)[2:])-profit(p[:2],tri) for i,p in enumerate(S) for j,tri in enumerate(triples) if mode=='all' or (mode=='align' and i==j) or (mode=='off' and i!=j)),F())
 projected={}
 for mass,a in atoms:
  rr={};rr.update(offrows(a));rr.update(crossrows(a));rr.update(taxrows(a));rr.update(alignrows(a));rr.update(triplerows(a))
  for n,v in rr.items():projected[n]=projected.get(n,F())+mass*v
 assert set(projected)==set(direct),(len(projected),len(direct),set(projected)-set(direct))
 assert all(projected[n]==direct[n] for n in direct),[n for n in direct if projected[n]!=direct[n]][:3]
 assert all(v>=0 for v in direct.values()),[n for n,v in direct.items() if v<0]
 return {'fixture':str(path.relative_to(ROOT)),'histories':check.checked_histories,'deviations':check.checked_deviations,'rows':len(direct),'minimum_slack':str(min(direct.values())),'root':s,'optimal':opt}

if __name__=='__main__':
 base=ROOT/'research/workspaces/customer-attraction/R-64201cd12083425899e2d643ec9bc087/counterexample'
 report={'scope':'finite formula audit, not universal welfare proof','fixtures':[audit(base/f) for f in ('cascade_m5p7_best.json',)]}
 print(json.dumps(report,indent=2));Path(__file__).with_suffix('.json').write_text(json.dumps(report,indent=2)+'\n')
