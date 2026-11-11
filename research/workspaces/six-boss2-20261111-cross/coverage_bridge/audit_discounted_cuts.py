#!/usr/bin/env python3
"""Independent Fraction audit: policies, orbit enumeration, columns, finite depth.

Does not import either discovery generator.  Four deterministic policies are
solved by 2x2 Cramer's rule, then their common optimum is checked against every
Bellman inequality.  Orbit counts come from literal six-index enumeration.
"""
from fractions import Fraction as F
from itertools import product
from collections import Counter
from pathlib import Path
import hashlib,json,sys


def div(n,d):return n/F(d) if n else F(0)


def policy_values(cost,theta):
    values=[]
    for f0,f1 in product((0,1),repeat=2):
        a=1-theta*(f0==0);b=-theta*(f0==1)
        c=-theta*(f1==0);d=1-theta*(f1==1)
        det=a*d-b*c;assert det>0
        e0=cost[0,f0];e1=cost[1,f1]
        values.append(((e0*d-b*e1)/det,(a*e1-c*e0)/det))
    optimum=tuple(min(v[t] for v in values) for t in (0,1))
    assert any(v==optimum for v in values)
    for t in (0,1):
        assert optimum[t]==min(cost[t,c]+theta*optimum[c] for c in (0,1))
    return optimum


def raw_costs(h,g,state,cut):
    bits=tuple(int(c) for c in h['actual_bits']);src=cut['source']-1;k=6-src
    p=sum(bits[:src]);ell=sum(bits[:5]);f,diag,wi,wj=g
    pars={n:F(v) for n,v in cut['parameters'].items()}
    query={f'A{i+1}':F(v) for i,v in enumerate(bits)}
    for n,v in zip(('Ti','Bi','Ci','Tj','Bj','Cj'),wi+wj):query[n]=F(v)
    query['R'],query['Z']=map(F,state)
    pats=list(product((0,1),repeat=3));total=[sum(n*w[a] for n,w in zip(h['hist'],pats)) for a in range(3)]
    for a,n in enumerate(('other_T','other_B','other_C')):
        exc=wi[a]+(0 if diag else wj[a]);query[n]=F(total[a]-exc,5 if diag else 4)
    M=sum((v for n,v in pars.items() if n.startswith('mu_')),F(0))
    out={}
    for t,c in product((0,1),repeat=2):
        candidates=[]
        for s in range(k-1):
            z=p+t+s+c
            value=div(pars.get('source',F(0))*t-M*c,z)
            value+=pars.get('alpha_mid',F(0))*F(s,ell+1)+pars.get('alpha_last',F(0))*F(c,ell+1)
            value+=pars.get('beta_mid',F(0))*s+pars.get('beta_last',F(0))*c
            qsum=sum((v*(F(t) if n=='mu_current' else query[n[3:]]) for n,v in pars.items() if n.startswith('mu_')),F(0))
            value+=qsum/(p+t+s+1)
            candidates.append(value)
        out[t,c]=min(candidates)
    return out


def orbit_groups(hist,orb):
    words=[]
    for word,n in zip(product((0,1),repeat=3),hist):words.extend([word]*n)
    assert len(words)==6
    f,diag=orb;counts=Counter()
    for i,j in product(range(6),repeat=2):
        if (i==j)!=bool(diag):continue
        counts[f,diag,words[i],words[j]]+=1
    assert sum(counts.values())==(6 if diag else 30)
    return counts


def main():
    point_path,report_path,outpath=map(Path,sys.argv[1:4])
    point=json.loads(point_path.read_text());report=json.loads(report_path.read_text());cols=point['columns']
    cuts=sorted([r for r in report['results'] if F(r.get('exact_slack','0'))<0],key=lambda r:F(r['exact_slack']))
    weights=list(F(c['weight']) for c in cols);audits=[]
    for number,cut in enumerate(cuts):
        theta=F(cut['theta']);pars={n:F(v) for n,v in cut['parameters'].items()};src=cut['source']-1;k=6-src
        orb=tuple(cut['orbit']);member=cut['member'];ct=6 if orb[1] else 30
        row=[F(0)]*len(cols);hi=None;hist=None;group_counts=None;cache={};finite_cache={}
        counts=0
        def phi(g,st,depth=None):
            nonlocal counts
            key=(hi,g,st)
            if key not in cache:
                edges=raw_costs(hist,g,st,cut);V=policy_values(edges,theta)
                cache[key]=((1-theta)*V[st[member]],edges)
                counts+=4*(k-1)
            if depth is None:return cache[key][0]
            edges=cache[key][1];v=[F(0),F(0)]
            for _ in range(depth):v=[min(edges[t,c]+theta*v[c] for c in (0,1)) for t in (0,1)]
            return (1-theta)/(1-theta**depth)*v[st[member]]
        finite_depths=range(1,25) if number==0 else []
        finite_rows={n:[F(0)]*len(cols) for n in finite_depths}
        for j,col in enumerate(cols):
            if col['kind']=='K':
                row[j]=(k-2)*pars.get('beta_mid',F(0))+pars.get('beta_last',F(0))
                for n in finite_depths:finite_rows[n][j]=row[j]
            elif col['kind']=='hist':
                hi=j;hist=col;group_counts=orbit_groups(col['hist'],orb);bits=list(map(int,col['actual_bits']));c=sum(bits)
                base=div(pars.get('source',F(0))*bits[src],c)
                base+=div(((k-2)*pars.get('alpha_mid',F(0))+pars.get('alpha_last',F(0)))*bits[5],c)
                row[j]=base-sum((F(q,ct)*phi(g,(0,0)) for g,q in group_counts.items()),F(0))
                for n in finite_depths:finite_rows[n][j]=base-sum((F(q,ct)*phi(g,(0,0),n) for g,q in group_counts.items()),F(0))
            elif col['kind']=='joint-reply':
                f,diag,wi,wj=col['group'];g=f,diag,tuple(wi),tuple(wj)
                if g[:2]!=orb:continue
                st=tuple(col['state']);q=group_counts[g]
                row[j]=-F(q,ct)*(phi(g,st)-phi(g,(0,0)))
                for n in finite_depths:finite_rows[n][j]=-F(q,ct)*(phi(g,st,n)-phi(g,(0,0),n))
        stored=[F(0)]*len(cols)
        for j,v in cut['row_nonzero']:stored[j]=F(v)
        assert row==stored
        slack=sum((a*b for a,b in zip(row,weights)),F(0))
        assert slack==F(cut['exact_slack'])<0
        digest=hashlib.sha256(json.dumps(list(map(str,row)),separators=(',',':')).encode()).hexdigest()
        assert digest==cut['row_sha256']
        fslacks={n:sum((a*b for a,b in zip(r,weights)),F(0)) for n,r in finite_rows.items()}
        item={'source':cut['source'],'member':member,'orbit':cut['orbit'],'theta':cut['theta'],
              'columns':len(row),'evaluated_visible_query_states':len(cache),'raw_bellman_actions_checked':counts,
              'exact_slack':str(slack),'row_sha256':digest,'full_row_matches':True,
              'finite_depth_slacks':{str(n):str(v) for n,v in fslacks.items()}}
        if fslacks:
            bad=[n for n,v in fslacks.items() if v<0];item['first_strict_finite_depth']=min(bad) if bad else None
            print('FINITE_DEPTHS',[(n,float(v)) for n,v in fslacks.items()],flush=True)
            if bad:
                n=min(bad);item['first_finite_row_nonzero']=[[j,str(v)] for j,v in enumerate(finite_rows[n]) if v]
                item['first_finite_row_sha256']=hashlib.sha256(json.dumps(list(map(str,finite_rows[n])),separators=(',',':')).encode()).hexdigest()
        audits.append(item)
    output={'scope':'independent exact audit of six saved local cuts, not complete-SPE or half theorem',
            'point':str(point_path),'point_sha256':hashlib.sha256(point_path.read_bytes()).hexdigest(),
            'report':str(report_path),'report_sha256':hashlib.sha256(report_path.read_bytes()).hexdigest(),
            'cuts':audits,'all_passed':True}
    outpath.write_text(json.dumps(output,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'audited_cuts':len(audits),'all_passed':True}),flush=True)


if __name__=='__main__':main()
