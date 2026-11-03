"""Exact separation by old-(P) mixed optimal/fixed five-topic queries.

This is an application of the already certified true-H projection, not a
new parent theorem. Only strict exact separators justify adding rows.
"""
from pathlib import Path
from fractions import Fraction as F
from math import comb
import json,hashlib
import trueH_own_index_pricing as oi
fc=oi.fc;cm=oi.cm;th=oi.th;HERE=Path(__file__).resolve().parent
SOURCE=HERE.parent/'certificate/exact_current_source_own_index_v1.json'
LABELS=list(cm.mp.LABELS)+[f'z{i}' for i in range(5)]
def mixedF(p,d,q,r):
    return sum((F(comb(d,s)*comb(5-d,r-s),comb(5,r))*th.FT[p][s+(5-r)*q] for s in range(r+1) if s<=d and 0<=r-s<=5-d),F(0))
def menu_count(a,name):
    if name=='opt':return sum(a['AB_hist'][4:])
    if ':' in name:
        tag,m=name.split(':');return cm.counts(a,tag)[m]
    raise ValueError(name)
def context(a,node):
    bits=tuple(map(int,a['bits']));mb=tuple(map(int,a['max_bits']))
    if node=='max':return sum(mb[:2]),cm.lm.q(mb[2],sum(mb))
    p,k,u=cm.mp.source(bits,(node,2));assert k==3;return p,u
def Jquery(a,name,t=None):
    bits=tuple(map(int,a['bits']));mb=tuple(map(int,a['max_bits']))
    if name in LABELS:return 5*fc.query(bits,mb,name)
    if name.startswith('own'):
        assert t is not None;return 5*t[int(name[3:])]
    return menu_count(a,name)
def coefficient(a,node,Q,r,J):
    bits=tuple(map(int,a['bits']));mb=tuple(map(int,a['max_bits']));M=mb[0];d=sum(a['AB_hist'][4:]);q=fc.query(bits,mb,Q)
    if node!='indexed':
        p,u=context(a,node);return 17040*u+1085*M-F(2679*Jquery(a,J),p+3)-mixedF(p,d,q,r)
    bg=bits[cm.mp.LABELS.index('A')]
    return sum((v*(17040*cm.lm.q(t[1],bg+sum(t))+1085*M-F(2679*Jquery(a,J,t),bg+t[0]+3)-mixedF(bg+t[0],d,q,r)) for v,t in zip(a['second_hist'],cm.mp.TYPES[4])),F(0))
def run():
    src=json.loads(SOURCE.read_text());atoms=src['atoms'];masses=[F(a['exact_mass']) for a in atoms]
    fixedJ=LABELS+['opt']+[f'{tag}:{m}' for tag,menus in cm.mp.MENUS.items() for m in menus]
    indexedJ=LABELS+['opt']+[f'Sbranch:{m}' for m in cm.mp.MENUS['Sbranch']]+[f'own{i}' for i in range(4)]
    reports=[];negative=[]
    for node in ('max','actual','second','indexed'):
        candidates=indexedJ if node=='indexed' else fixedJ
        # The J part separates from T. Choose one strongest allowed query
        # globally for this entire source, rather than per customer.
        cost={J:sum(m* (coefficient(a,node,'A',0,'opt')-coefficient(a,node,'A',0,J)) for a,m in zip(atoms,masses)) for J in candidates}
        best=max(candidates,key=cost.get)
        rows=[]
        for Q in LABELS:
            for r in range(1,5):
                slack=sum(m*coefficient(a,node,Q,r,best) for a,m in zip(atoms,masses))
                entry={'source_node':node,'repeated_Q':Q,'optimal_subset_size':r,'J_query':best,'exact_slack':str(slack)}
                rows.append(entry)
                if slack<0:negative.append(entry)
        reports.append({'source_node':node,'strongest_allowed_J':best,'query_classes':candidates,'checked_rows':len(rows),'minimum_exact_slack':str(min(F(x['exact_slack']) for x in rows)),'rows':rows})
    out={'status':'exact-separation-complete','scope':__doc__,'source':str(SOURCE),'source_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),'positive_exact_atoms':len(atoms),'checked_mixed_rows':sum(x['checked_rows'] for x in reports),'negative_count':len(negative),'negative_rows':negative,'reports':reports}
    HERE.joinpath('mixed_optimal_query_separation.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ('negative_rows','reports')},indent=2));print(json.dumps([{'node':x['source_node'],'J':x['strongest_allowed_J'],'minimum':x['minimum_exact_slack']} for x in reports],indent=2))
if __name__=='__main__':run()
