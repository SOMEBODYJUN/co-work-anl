"""Exact local strongPAIR identity and direct-edge coefficient audit, not SPE."""
import argparse
import ast
from collections import Counter
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
import hashlib
import json
from pathlib import Path
from types import SimpleNamespace

def selected(path, names, namespace):
    tree = ast.parse(path.read_text())
    nodes = [n for n in tree.body if (isinstance(n, ast.FunctionDef) and n.name in names)
             or (isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id in names for t in n.targets))]
    assert len(nodes) == len(names)
    exec(compile(ast.Module(body=nodes, type_ignores=[]), str(path), 'exec'), namespace)
    return namespace

def sha(path):
    b = path.read_bytes()
    return {'name': path.name, 'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}

def share(bit, denominator):
    return F(bit, denominator) if bit else F(0)

def U(x, y, b):
    return share(x, b+x+y)

def pair_value(b, a, z, t, q):
    den = (b+1)*(b+2)
    return U(a,z,b)+U(z,a,b)+F(a,den)-F(t+q,b+1)+F(t*q,den)

def check_local_identity():
    checked = 0
    for b in range(5):
        for a,z,t,q,j in product(range(2),repeat=5):
            ic1=U(a,z,b)-U(t,j,b)
            ic2=U(j,t,b)-U(q,t,b)
            ic3=U(z,a,b)-U(j,a,b)
            remainder=F(a*(1-j),(b+1)*(b+2))
            assert remainder >= 0
            assert pair_value(b,a,z,t,q)==ic1+ic2+ic3+remainder
            checked+=1
    return checked

def direct_rows(cols, keys):
    rows=[[F(0)]*len(cols) for _ in keys]
    patterns=list(product(range(2),repeat=3));current=None;all_edges=[]
    for col,c in enumerate(cols):
        if c['kind']=='hist':
            current=c;a=tuple(map(int,c['actual_bits']));b=sum(a[:4])
            words=[w for w,count in zip(patterns,c['hist']) for _ in range(count)]
            assert len(words)==6 and c['d']==sum(w[0] for w in words)
            all_edges=[(f,int(i==j),words[i],words[j]) for f in range(2) for i in range(6) for j in range(6) if f or i!=j]
            assert Counter((f,d) for f,d,wi,wj in all_edges)==Counter({(0,0):30,(1,0):30,(1,1):6})
            for row,(member,f,d,qi) in zip(rows,keys):
                for ff,dd,wi,wj in all_edges:
                    if (ff,dd)==(f,d):
                        q=(*a,*wi,*wj)[qi]
                        row[col]+=pair_value(b,a[4],a[5],0,q)
        elif c['kind']=='joint-reply':
            assert current is not None
            a=tuple(map(int,current['actual_bits']));b=sum(a[:4]);f,d,wi,wj=c['group'];g=(f,d,tuple(wi),tuple(wj))
            represented=[edge for edge in all_edges if edge==g];assert represented
            for row,(member,ff,dd,qi) in zip(rows,keys):
                if (ff,dd)==(f,d):
                    t=c['state'][member]
                    for _,_,wi,wj in represented:
                        q=(*a,*wi,*wj)[qi]
                        row[col]+=pair_value(b,a[4],a[5],t,q)-pair_value(b,a[4],a[5],0,q)
        else:
            assert c['kind'] in ('K','overlap')
    return rows

def main():
    p=argparse.ArgumentParser()
    for name in ['source','old-query','priced','cuts','out']:p.add_argument('--'+name,type=Path,required=True)
    p.add_argument('--point',type=Path,action='append',required=True);a=p.parse_args()
    hidden=selected(a.priced,{'_rational','_inputs','_share','branch_value','projected','projected_by_count'},{'Fraction':F,'product':product})
    oq=selected(a.old_query,{'PAT','GS','psi','groups','row'},{'F':F,'product':product,'lru_cache':lru_cache,'projected_by_count':hidden['projected_by_count']})
    original=selected(a.source,{'KEYS','query','rows'},{'F':F,'product':product,'oq':SimpleNamespace(**oq)})
    keys=tuple((m,f,d,q) for m in range(2) for f,d in [(0,0),(1,0),(1,1)] for q in range(12))
    assert original['KEYS']==keys
    output={'scope':'72 mixed strongPAIR rows only; three-IC identity, explicit edge coefficients, and eight historical-cut equality. No full graph/LP/SPE.','sources':[sha(a.source),sha(a.old_query),sha(a.priced),sha(a.cuts)],'source_execution':'AST-selected mathematical functions/constants only; no original main or dependency graph import','local_three_IC_identities':check_local_identity(),'points':[]}
    cuts=json.loads(a.cuts.read_text())['selected'];canonical=None
    for path in a.point:
        data=json.loads(path.read_text());cols=data['columns'];desc=[{k:v for k,v in c.items() if k!='weight'} for c in cols]
        if canonical is None:canonical=desc
        assert desc==canonical
        got=original['rows'](cols);want=direct_rows(cols,keys);assert got==want
        weights=[F(c['weight']) for c in cols];assert min(weights)>=0
        slacks=[sum((v*w for v,w in zip(row,weights)),F(0)) for row in want]
        mapping=[];vectors=[]
        for item in cuts:
            cut=item['cut'];i,m,f,d,q,mode,aa,mu=cut
            assert i==4 and F(aa)==F(mu)==1
            key=(m,f,d,q+6);j=keys.index(key);row=oq['row'](cols,cut)
            assert row==got[j]
            vectors.append(tuple(row));mapping.append({'cut':cut,'mixed_key':list(key),'coefficient_equalities':len(cols),'slack':str(slacks[j])})
        assert len(set(vectors))==3
        output['points'].append({'input':sha(path),'columns':len(cols),'keys':len(keys),'coefficient_equalities':len(cols)*len(keys),'all_descriptors_equal_first':True,'negative_rows':sum(x<0 for x in slacks),'zero_rows':sum(x==0 for x in slacks),'minimum_slack':str(min(slacks)),'first_min_key':list(keys[slacks.index(min(slacks))]),'old_cut_distinct_vectors':len(set(vectors)),'old_cut_mapping':mapping,'slacks':[{'key':list(k),'value':str(v)} for k,v in zip(keys,slacks)]})
    output['pass']=True;a.out.write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps({'local_identities':output['local_three_IC_identities'],'points':[{k:d[k] for k in ['coefficient_equalities','negative_rows','zero_rows','minimum_slack','first_min_key','old_cut_distinct_vectors']} for d in output['points']]},indent=2))

if __name__=='__main__':main()
