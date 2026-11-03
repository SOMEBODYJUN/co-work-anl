"""Sparse integer exact replay of existing seven-max seat assets, without LP.

Reconstructs all row coefficients independently. An integer common denominator
keeps replay inexpensive while preserving exact Fraction identities.
"""
from fractions import Fraction as F
from itertools import combinations_with_replacement
from pathlib import Path
from math import lcm
from collections import defaultdict
import json,time

ROOT=Path(__file__).resolve().parents[1]
OUT=Path(__file__).resolve().parent

def routes(n):
    def rec(a):
        if len(a)==n:yield tuple(a);return
        for j in range(max(a)+2):yield from rec(a+[j])
    return list(rec([0]))

def targets(route,n):
    u=max(route)+1
    for mask in range(1<<u):
        k=n-mask.bit_count()
        if 0<=k<=7-u:yield mask+(((1<<k)-1)<<u)

def columns(n,route):
    out=[]
    for I in range(1,128):
        eligible=sum(1<<t for t,j in enumerate(route[:-1]) if (I>>j)&1)
        last=((I>>route[-1])&1)<<(n-1);J=eligible
        while True:
            out.append((I,J+last))
            if not J:break
            J=(J-1)&eligible
    return out

def descriptions(n,extra):
    ans=[('M',t) for t in range(n)]+[('L',j) for j in range(7)]
    ans += [('T',j,k) for j,k in combinations_with_replacement(range(7),2)]
    for marker in extra:
      if marker==0:ans += [('worst',t,j) for t in range(n-1) for j in range(7)]
      elif marker==5:ans += [('H',t,H) for t in range(n-1) for H in range(1,128)]
      else:ans += [('profit',marker,tt) for tt in combinations_with_replacement(range(7),marker)]
    return ans

def setup(n):
    A=[F(n+t,(t+1)*(7*n-5*t)) for t in range(n-1)]+[F(1,n+6)]
    B=[F(2,7*n-5*t) for t in range(n-1)]+[F(n+1,n*(n+6))]
    A=[min(A[t:]) for t in range(n)];B=[min(B[t:]) for t in range(n)]
    D=750*lcm(*range(1,n*(n+6)+1),*[x.denominator for x in A+B])
    return D,[int(D*x) for x in A],[int(D*x) for x in B]

def row(n,I,J,desc,D,A,B):
    count=J.bit_count();m=I.bit_count()
    share=lambda t:D//count if (J>>t)&1 else 0
    mem=lambda j:(I>>j)&1
    prior=lambda t:(J&((1<<t)-1)).bit_count()
    kind=desc[0]
    if kind=='M':
        t=desc[1];return share(t)-(D//n if m==7 else A[t] if m==1 else B[t])
    if kind=='L':return share(n-1)-mem(desc[1])*D//(prior(n-1)+1)
    if kind=='T':
        h=prior(n-2);e=mem(desc[1])+mem(desc[2]);tax=((J>>(n-2))&1)*D//((h+1)*(h+2))
        return share(n-2)+share(n-1)+tax-(e*D//(h+e) if e else 0)
    if kind=='worst':
        t,j=desc[1:];return share(t)-mem(j)*D//(prior(t)+n-t)
    if kind=='H':
        t,H=desc[1:];h=prior(t);r=n-t;factor=r+H.bit_count()-1
        floor=D//n if m==7 else int(bool(I&H))*D//(factor*(h+1)) if m==1 else (I&H).bit_count()*D//(factor*(h+r))
        return share(t)-floor
    if kind=='profit':
        r,tt=desc[1:];h=prior(n-r);e=sum(mem(j) for j in tt)
        num,den=(5,3) if r==3 else (1499,750)
        return num*sum(share(t) for t in range(n-r,n))//den-(e*D//(h+e) if e else 0)
    if kind=='seat':
        t,j,k=desc[1:];h=prior(t)
        floor=D//n if m==7 else mem(j)*D//(h+(k if m==1 else n-t))
        return share(t)-floor
    raise AssertionError(desc)

def direct_as_tree(item,n):
    return {'status':'complete','n':n,'route':item['route'],'K':item['target'],
            'columns':item['columns'],'base_extra':[0,5],
            'base_rows':len(item['multipliers']),
            'nodes':[{'id':0,'path':[],'leaf':True,'dual':[(q,str(F(v,item['scale']))) for q,v in enumerate(item['multipliers']) if v], 'minimum':item['minimum']}],
            'leaf_count':1,
            'seat_ids':[(t,j,k) for t in range(n-1) for j in range(7) for k in range(1,n-t+1)]}

def structural(cert):
    n=cert['n'];base=descriptions(n,cert['base_extra']);assert len(base)==cert['base_rows']
    seats=[('seat',t,j,k) for t in range(n-1) for j in range(7) for k in range(1,n-t+1)]
    assert [list(x[1:]) for x in seats]==[list(x) for x in cert['seat_ids']]
    nodes=cert['nodes'];assert cert['status']=='complete'
    assert [x['id'] for x in nodes]==list(range(len(nodes)))
    reached=set();leaves=[]
    def walk(i):
        if i in reached:return
        reached.add(i);node=nodes[i];path=node['path']
        assert path==sorted(set(path)) and all(0<=q<len(seats) for q in path)
        if node['leaf']:
            weights=[]
            for q,w in node['dual']:
                assert 0<=q<len(base)+len(path);w=F(w);assert w>=0
                weights.append((base[q] if q<len(base) else seats[path[q-len(base)]],w))
            leaves.append((node,weights));return
        t=node['t'];clause=node['clause'];children=node['children'];r=n-t
        assert len(clause)==len(set(clause))==len(children)==r
        assert all(0<=si<len(seats) and seats[si][1]==t for si in clause)
        for si,child in zip(clause,children):
            assert nodes[child]['path']==sorted(set(path+[si]));walk(child)
    assert nodes[0]['path']==[];walk(0)
    assert reached==set(range(len(nodes))) and len(leaves)==cert['leaf_count']
    return leaves

def run(n,certs,expected):
    start=time.time();D,A,B=setup(n);groups=defaultdict(list)
    for name,cert in certs:
        key=(tuple(cert['route']),cert['K']);assert key in expected
        assert cert['n']==n and cert['K'].bit_count()==n
        groups[key[0]].append((name,cert,structural(cert)))
    records=[];checks=0;global_min=None
    for ri,(route,items) in enumerate(sorted(groups.items())):
        cols=columns(n,route);needed={desc for _,_,ls in items for _,ws in ls for desc,w in ws}
        table={desc:[row(n,I,J,desc,D,A,B) for I,J in cols] for desc in needed}
        for name,cert,leaves in items:
            assert len(cols)==cert['columns'];minimum=None;leafchecks=0
            for node,weights in leaves:
                scale=lcm(*(w.denominator for _,w in weights)) if weights else 1
                integer=[(table[desc],int(w*scale)) for desc,w in weights]
                mn=None
                for ci,(I,J) in enumerate(cols):
                    r=(int(bool(J))*D-int(bool(I&cert['K']))*(D//2))*scale-sum(vec[ci]*w for vec,w in integer)
                    assert r>=0,(n,route,cert['K'],node['id'],I,J,r)
                    mn=r if mn is None else min(mn,r)
                exact=F(mn,D*scale);assert exact==F(node['minimum'])
                minimum=exact if minimum is None else min(minimum,exact);leafchecks+=len(cols)
            checks+=leafchecks;global_min=minimum if global_min is None else min(global_min,minimum)
            records.append({'name':name,'route':route,'K':cert['K'],'nodes':len(cert['nodes']),'leaves':len(leaves),'checks':leafchecks,'minimum':str(minimum)})
        if ri%25==0:print(json.dumps({'n':n,'reviewed_routes':ri+1,'certificates':len(records),'exact_checks':checks,'seconds':round(time.time()-start,1)}),flush=True)
    present={(tuple(x['route']),x['K']) for x in records};missing=sorted(expected-present)
    return {'status':'passed_existing_assets','n':n,'expected_routes':len(routes(n)), 'expected_orbits':len(expected),'reviewed_orbits':len(present),'missing_orbits':[{'route':r,'K':K} for r,K in missing], 'certificates':records,'exact_checks':checks,'minimum':str(global_min),'elapsed':time.time()-start}

if __name__=='__main__':
    expected={n:{(r,K) for r in routes(n) for K in targets(r,n)} for n in (5,6)}
    certs5=[(p.name,json.loads(p.read_text())) for p in sorted((ROOT/'seven_maxima_new_rows/seat_trees_n5').glob('*.json'))]
    scan6=json.loads((ROOT/'seven_maxima_new_rows/scan_n6_seat.json').read_text())
    assert {(tuple(x['route']),x['target']) for x in scan6['certificates']}==expected[6]
    certs6=[('scan_n6_seat direct '+str(i),direct_as_tree(x,6)) for i,x in enumerate(scan6['certificates']) if 'multipliers' in x]
    certs6.extend((p.name,json.loads(p.read_text())) for p in sorted((ROOT/'seven_maxima_joint/n6_route_assets').glob('seat_tree*.json')))
    result={'status':'passed_existing_assets','scope':'Exact proof replay only; no missing certificate search or generation.', 'n5':run(5,certs5,expected[5]),'n6':run(6,certs6,expected[6])}
    (OUT/'independent_seat_assets.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({n:{k:v for k,v in result[n].items() if k not in ('certificates','missing_orbits')} for n in ('n5','n6')},indent=2))
