"""Independent Fraction reconstruction of the 240 saved four-source queries.

Uses the certified 3x6 table and literal input fields. No legacy code,
scientific library, optimizer, pricing oracle or SPE evaluator is imported.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
from math import comb
import hashlib,json
HERE=Path(__file__).resolve().parent
REPO=HERE.parents[4]
PREFIX='research/workspaces/customer-attraction/R-d3981c0168644971803a9c3380ed687c/round8_five/maxroot'
SRC=HERE/'original'/PREFIX
POINT=REPO/'archives/customer-attraction/tools/evidence/five-root-parent-audits-primary/source-root/research/workspaces/customer-attraction/R-d3981c0168644971803a9c3380ed687c/round8_five/certificate/exact_current_source_own_index_v1.json'
FT=((F(0),F(960),F(1220),F(1480),F(1740),F(2000)),
    (F(0),F(1665,4),F(2745,4),F(3785,4),F(4825,4),F(5865,4)),
    (F(0),F(320),F(524),F(728),F(932),F(1136)))
OLD='ABCDEUVWXY'
LABELS=list(OLD)+['z'+str(i) for i in range(5)]
MENUS={'AB':['mX','mY'],'AE':['mX','mY'],'Sbranch':['mU','mV','mW']}
FIELDS={'AB':'AB_hist','AE':'AE_hist','Sbranch':'second_hist'}
T4=list(product((0,1),repeat=4))
def share(a,b):return F(a,b) if a else F(0)
def member(a,label):return int(a['max_bits'][int(label[1:])]) if label.startswith('z') else int(a['bits'][OLD.index(label)])
def dopt(a):return sum(a['AB_hist'][4:])
def menu_count(a,name,theta=None):
    if name in LABELS:return 5*member(a,name)
    if name=='opt':return dopt(a)
    if name.startswith('own'):return 5*theta[int(name[3:])]
    tag,menu=name.split(':');types=product((0,1),repeat=4 if tag=='Sbranch' else 3);i=MENUS[tag].index(menu)+1
    return sum(n*t[i] for n,t in zip(a[FIELDS[tag]],types))
def sources(a,node):
    if node=='indexed':
        bg=member(a,'A')
        return [(n,bg+t[0],share(t[1],bg+sum(t)),t) for n,t in zip(a['second_hist'],T4) if n]
    if node=='max':
        b=list(map(int,a['max_bits']));return [(1,b[0]+b[1],share(b[2],sum(b)),None)]
    labels='ABCDE' if node=='actual' else 'AEUVW';b=[member(a,l) for l in labels]
    return [(1,b[0]+b[1],share(b[2],sum(b)),None)]
def mixed(p,d,q,r):
    return sum((F(comb(d,s)*comb(5-d,r-s),comb(5,r))*FT[p][s+(5-r)*q]
                for s in range(r+1) if s<=d and 0<=r-s<=5-d),F(0))
def coef(a,node,Q,r,J):
    return sum((n*(17040*u+1085*member(a,'z0')
                   -F(2679*menu_count(a,J,t),p+3)-mixed(p,dopt(a),member(a,Q),r))
                for n,p,u,t in sources(a,node)),F(0))
def run():
    raw=json.loads((SRC/'mixed_optimal_query_separation.json').read_text())
    assert hashlib.sha256(POINT.read_bytes()).hexdigest()==raw['source_sha256']
    data=json.loads(POINT.read_text());atoms=data['atoms'];masses=[F(a['exact_mass']) for a in atoms]
    results=[];checks=0
    for saved in raw['reports']:
        node=saved['source_node']
        bank=LABELS+['opt']+([f'{tag}:{c}' for tag,menus in MENUS.items() for c in menus]
                           if node!='indexed' else ['Sbranch:'+c for c in MENUS['Sbranch']]+['own'+str(i) for i in range(4)])
        assert bank==saved['query_classes'] and len(bank)==23
        costs={J:sum((m*sum((F(n*menu_count(a,J,t),p+3) for n,p,u,t in sources(a,node)),F(0))
                      for a,m in zip(atoms,masses)),F(0)) for J in bank}
        best=max(bank,key=costs.get);assert best==saved['strongest_allowed_J']
        expected={(r['repeated_Q'],r['optimal_subset_size']):F(r['exact_slack']) for r in saved['rows']}
        slacks={}
        for Q in LABELS:
            for r in range(1,5):
                v=sum((m*coef(a,node,Q,r,best) for a,m in zip(atoms,masses)),F(0))
                assert v==expected[Q,r] and v>0
                slacks[Q,r]=v;checks+=len(atoms)
        assert min(slacks.values())==F(saved['minimum_exact_slack'])
        results.append(dict(source=node,chosen_J=best,explicit_rows=len(slacks),minimum=str(min(slacks.values())),
                            all_saved_values_equal=True,J_bank_size=len(bank),
                            dominance='Other 22 J choices only increase each whole-source row; no per-customer J selection.'))
    assert len(atoms)==63 and checks==15120
    out=dict(status='PASS_NEW_EXACT_FOUR_SOURCE_MIXED_QUERY_RECONSTRUCTION',input_sha256=raw['source_sha256'],
             atoms=63,explicit_rows=240,coefficient_contributions=checks,negative_rows=0,reports=results,
             logically_covered_fixed_bank_rows=4*23*15*4,
             boundary='Fixed point and the stated finite Q/J banks, r1..4 only; no complete-extension feasibility, universal redundancy or SPE claim')
    (HERE/'mixed-query-definition-check.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':run()
