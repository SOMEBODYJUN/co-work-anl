"""Independent exact reconstruction of parent's proposed two-tail counterexample."""
from fractions import Fraction as F
import json
from pathlib import Path

ROWS=[(1,1,8),(2,0,5),(4,0,3),(8,0,3),(20,0,2),(24,0,2),(36,0,2),(40,0,2),(49,0,2),(50,0,2)]
LABELS=['A','B','T','Q','R','S','E']
member=[]
for mask,b,n in ROWS:
 member.append([int(bool(mask&(1<<a))) for a in range(6)]+[int(mask==1)])

def payoff(a,terminal):
 return sum((F(n, b+sum(bits[j] for j in terminal)) for (mask,b,n),bits in zip(ROWS,member) if bits[a]), F(0))

def fmt(x): return str(x)

def run():
 replies=[1,4,4,4,5,4]
 table=[]
 for a in range(7):
  values=[payoff(c,[a,c]) for c in range(7)]
  chosen=replies[a] if a<6 else max(range(7),key=lambda c:values[c])
  assert values[chosen]==max(values),(a,chosen,values)
  if a==6: replies.append(chosen)
  table.append(values)
 root=[payoff(a,[a,replies[a]]) for a in range(7)]
 assert root[0]==max(root)
 actual=[0,1]
 u=[payoff(a,actual) for a in actual]
 d=[i for i,bits in enumerate(member) if not bits[0] and not bits[1] and (bits[2] or bits[3])]
 assert all(ROWS[i][1]==0 for i in d)
 D=sum(ROWS[i][2] for i in d)
 assert D==14 and u==[F(6),F(7)]
 price=D-2*u[0]
 assert price==2 and price>max(F(0),u[1]-u[0])
 # E is the exact legal background action, selected once before this tail.
 assert all(b==bits[6] for (mask,b,n),bits in zip(ROWS,member))
 # Exact B_D(6): T,Q cover disjoint 7-blocks; R,S have four D clients.
 # Every theme has D size <=7 and D total=14. Thus coverage <=min(7*tau,14),
 # so coverage-6*tau <=2, achieved by z_T=z_Q=1.
 per_theme=[sum(ROWS[i][2] for i in d if member[i][a]) for a in range(7)]
 assert per_theme==[0,0,7,7,4,4,0]
 result={'status':'exact complete-tail SPE verification, independent author reconstruction', 'rows':[{'old_mask':mask,'background':b,'unit_customers':n} for mask,b,n in ROWS], 'labels':LABELS,'replies':replies,'last_player_payoff_table':[[fmt(v) for v in row] for row in table], 'first_player_deviation_values':[fmt(v) for v in root], 'actual':actual,'actual_utilities':[fmt(v) for v in u], 'protected_D':D,'B_D_uA':fmt(price),'protected_to_profit':fmt(F(D,sum(u))), 'legal_background_topic':'E'}
 path=Path(__file__).with_name('protected_counterexample_independent_audit.json'); path.write_text(json.dumps(result,indent=2))
 print(json.dumps(result,indent=2))

def audit_zero_background():
 rows=[(mask,0,4 if mask==1 else n) for mask,b,n in ROWS]
 def u(a,terminal):
  return sum((F(n,sum(int(bool(mask&(1<<j))) for j in terminal)) for mask,b,n in rows if mask&(1<<a)),F(0))
 replies=[1,4,4,4,5,4]
 table=[[u(c,[a,c]) for c in range(6)] for a in range(6)]
 assert all(table[a][replies[a]]==max(table[a]) for a in range(6))
 root=[u(a,[a,replies[a]]) for a in range(6)]
 assert root==[F(6)]*6
 assert sum(n for mask,b,n in rows)==27
 actual=[u(0,[0,1]),u(1,[0,1])]
 assert actual==[F(6),F(7)]
 protected=sum(n for mask,b,n in rows if not(mask&3) and mask&12)
 assert protected==14
 welfare=[]
 for a in range(6):
  for c in range(a,6): welfare.append((sum(n for mask,b,n in rows if mask&((1<<a)|(1<<c))),(a,c)))
 optimum=max(v for v,pair in welfare)
 result={'status':'exact complete zero-root SPE verification','players':2,'topics':6,'unit_customers':27,'rows':rows,'replies':replies,'last_payoff_table':[[str(v) for v in row] for row in table],'first_payoff_values':[str(v) for v in root],'actual_utilities':[str(v) for v in actual],'W':13,'D':protected,'OPT_2':optimum,'B_D_6':2}
 Path(__file__).with_name('protected_zero_root_independent_audit.json').write_text(json.dumps(result,indent=2))
 print(json.dumps(result,indent=2))

if __name__=='__main__':
 run()
 audit_zero_background()
