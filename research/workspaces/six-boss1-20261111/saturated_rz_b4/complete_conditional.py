"""Construct common literal atoms from conditional order moments.

Every identified event identity is proved by SCC.  Unrelated equal-sized
events may be assigned equal intervals as a constructive choice only.
Full-own-support leaves are filled inside the core's two event regions.
"""
from __future__ import annotations
from collections import defaultdict
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
import argparse,json
import numpy as np
from extract_face import parse_point, sha, orbit
from conditional_b4 import serial

def orient(face):
    mp=face['variable_map'];n=len(face['free_classes']);ad=[set() for _ in range(n)]
    for c in face['clauses']:
        pp=[];skip=False
        for l in c['forbidden']:
            m=mp[l//2];b=l%2
            if 'constant' in m:
                if m['constant']!=b:skip=True
            else:pp.append((m['free_variable'],b^m['flip']))
        if skip or len(pp)<2:continue
        (a,x),(b,y)=pp
        if a==b:assert x!=y;continue
        parity=1^x^y;ad[a].add((b,parity));ad[b].add((a,parity))
    signs={};components=[]
    for root in range(n):
        if root in signs:continue
        signs[root]=0;stack=[root];cc=[]
        while stack:
            a=stack.pop();cc.append(a)
            for b,p in ad[a]:
                if b in signs:assert signs[b]==signs[a]^p
                else:signs[b]=signs[a]^p;stack.append(b)
        components.append(sorted(cc))
    return [signs[i] for i in range(n)],components

def construct(point,facepath,momentpath):
    raw,nodes,data=parse_point(point)
    face=json.loads(Path(facepath).read_text());moment=json.loads(Path(momentpath).read_text())
    assert face['point_sha256']==moment['model']['point_sha256']==sha(point)
    assert moment['model']['face_sha256']==sha(facepath)
    sol=list(map(Q,moment['discovery']['exact_solution']));model=moment['model']
    tables=defaultdict(lambda:[Q()]*4)
    for key,m in zip(model['variables'],sol[:-1]):
        h,g,s,a=key;tables[h,g,tuple(s)][a]=m
    blocks=[];orientation_records=[]
    for hrec in face['hist_records']:
        if 'face' not in hrec:continue
        h=hrec['hist_column'];d=data[h];fc=hrec['face'];signs,components=orient(fc)
        orientation_records.append(dict(hist_column=h,orientation=signs,components=components))
        mp=fc['variable_map'];nodeg=model['node_groups'][str(h)]
        for s,eta in sorted(d['B4'].items()):
            if not eta:continue
            rho=[tables[h,nodeg[e],s] for e in range(66)]
            masses=[]
            for m in rho:
                assert sum(m)==eta
                masses.extend([m[2]+m[3],m[1]+m[3]])
            intervals=[]
            for v,m in enumerate(mp):
                if 'constant' in m:
                    assert masses[v]==eta*m['constant']
                    intervals.append([(Q(),eta)] if m['constant'] else [])
                else:
                    fi=m['free_variable'];rep=fc['free_classes'][fi]['variable']
                    want=masses[rep] if not m['flip'] else eta-masses[rep]
                    assert masses[v]==want
                    sign=signs[fi]^m['flip']
                    intervals.append([(eta-masses[v],eta)] if sign else [(Q(),masses[v])])
            # Non-core event of a full-four-state node is isolated in the face.
            for e,(fam,i,j) in enumerate(nodes):
                if not all(d['own'][e]):continue
                core=2*e+(1 if fam else 0);leaf=2*e+(0 if fam else 1)
                assert not fc['adjacency'][2*leaf] and not fc['adjacency'][2*leaf+1]
                ranges=[(a,b) for a,b in intervals[core] if a<b]
                points=sorted({Q(),eta,*[x for r in ranges for x in r]})
                pieces=[]
                for a,b in zip(points,points[1:]):
                    if a==b:continue
                    cv=int(any(l<=(a+b)/2<r for l,r in ranges))
                    # state code always 2*R+Z
                    state=2*cv+1 if not fam else 2+cv
                    amount=rho[e][state]
                    assert 0<=amount<=b-a
                    if amount:pieces.append((a,a+amount))
                intervals[leaf]=pieces
            intervals=[[(a,b) for a,b in rs if a<b] for rs in intervals]
            bp=sorted({Q(),eta,*[x for rs in intervals for r in rs for x in r]})
            atoms=[];owncheck=[[Q()]*4 for e in range(66)]
            for a,b in zip(bp,bp[1:]):
                u=(a+b)/2;bits=[int(any(l<=u<r for l,r in rs)) for rs in intervals]
                states=[2*bits[2*e]+bits[2*e+1] for e in range(66)]
                for c in fc['clauses']:
                    assert not all(bits[l//2]==l%2 for l in c['forbidden'])
                for e,st in enumerate(states):owncheck[e][st]+=b-a
                atoms.append(dict(mass=b-a,states=states))
            assert owncheck==rho
            blocks.append(dict(hist_column=h,B4_state=s,mass=eta,
                               intervals=intervals,breakpoints=bp,atoms=atoms))
    return dict(point_sha256=sha(point),face_sha256=sha(facepath),moment_sha256=sha(momentpath),
                source_sha256=sha(Path(__file__)),literal_node_order=nodes,blocks=blocks,
                orientation_records=orientation_records,
                symmetrization='For each base atom and each of 720 S6 permutations move words and literal node indices together; mass / 720'),data,nodes

def audit(w,data,nodes):
    os=defaultdict(list)
    for e,ne in enumerate(nodes):
        for f,nf in enumerate(nodes):os[orbit(ne,nf)].append((e,f))
    idx={cl:(np.array([e for e,f in pp]),np.array([f for e,f in pp])) for cl,pp in os.items()}
    vals=defaultdict(Q);bvals=defaultdict(Q)
    for h,d in data.items():
        p=sum(d['actual'][:3]);P=sum(d['actual'][:4]);own=d['own']
        den=[p+d['words'][i][0]+d['words'][j][1+f]+1 for f,i,j in nodes]
        for cl,pp in os.items():
            for e,f in pp:
                qe=own[e][2]+own[e][3];qf=own[f][2]+own[f][3];vf=own[f][1]+own[f][3]
                vals['R-R',cl]+=(qe-qf)/Q(den[e]*len(pp))
                vals['R-Z',cl]+=(qe-vf)/Q(den[e]*len(pp))
    for block in w['blocks']:
        h=block['hist_column'];d=data[h];P=sum(d['actual'][:4]);s=block['B4_state']
        fd=sum(d['actual'][:3])+d['actual'][5]+s[0]+1
        for atom in block['atoms']:
            mass=Q(atom['mass']);states=np.array(atom['states'],dtype=int);r=states//2;z=states%2
            for flag in (0,1):
                mask=(r==flag).astype(int)
                for kind,target in [('Z-R',r),('Z-Z',z)]:
                    mat=mask[:,None]*(z[:,None]-target[None,:])
                    for cl,(ii,jj) in idx.items():
                        cnt=int(mat[ii,jj].sum())
                        if cnt:vals[kind,cl]+=mass*Q(cnt,len(ii)*(P+1+flag))
            for orb in ((0,0),(1,0),(1,1)):
                es=[e for e,(f,i,j) in enumerate(nodes) if (f,int(i==j))==orb];n=len(es)
                bvals['F-to-R',orb]+=mass*Q(n*s[1]-int(r[es].sum()),n*fd)
                bvals['F-to-Z',orb]+=mass*Q(n*s[1]-int(z[es].sum()),n*fd)
                for k in range(3):
                    bvals['Z-to-X',orb,k]+=mass*sum((Q(int(z[e])-s[k],P+1+int(r[e])) for e in es),Q())/n
    rows=[dict(kind=k,orbit=cl,literal_queries=len(os[cl]),slack=str(v),slack_float=float(v)) for (k,cl),v in sorted(vals.items())]
    for kind in ('R-R','R-Z','Z-R','Z-Z'):
        for cl in os:
            if (kind,cl) not in vals:rows.append(dict(kind=kind,orbit=cl,literal_queries=len(os[cl]),slack='0',slack_float=0.))
    brr=[dict(query=k,slack=str(v),slack_float=float(v)) for k,v in sorted(bvals.items())]
    return dict(old_rows=rows,B4_rows=brr,old_negative_orbits=[r for r in rows if Q(r['slack'])<0],
                B4_negative_orbits=[r for r in brr if Q(r['slack'])<0],base_atoms=sum(len(b['atoms']) for b in w['blocks']),
                minimum_old_slack=str(min(Q(r['slack']) for r in rows)),minimum_B4_slack=str(min(bvals.values())),
                full_network_feasible=all(Q(r['slack'])>=0 for r in rows+brr))

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--point',type=Path,required=True);ap.add_argument('--face',type=Path,required=True)
    ap.add_argument('--moments',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);args=ap.parse_args()
    w,data,nodes=construct(args.point,args.face,args.moments);w['audit']=audit(w,data,nodes)
    args.output.write_text(json.dumps(serial(w),indent=2,ensure_ascii=False)+'\n')
    print(json.dumps(serial({k:v for k,v in w['audit'].items() if k not in ('old_rows','B4_rows')})))

if __name__=='__main__':main()
