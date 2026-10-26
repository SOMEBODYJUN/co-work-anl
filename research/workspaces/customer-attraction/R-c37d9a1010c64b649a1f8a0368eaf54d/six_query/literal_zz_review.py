"""Data-only reconstruction of every added Z->Z row.

No research row generator is imported.  All 66 reply labels and all ordered
label pairs are expanded literally.  The report concerns a jointly distributed
membership witness in the enlarged necessary-condition domain, not an SPE.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
from hashlib import sha256
import json

HERE=Path(__file__).resolve().parent
ROOT=next(p for p in HERE.parents if (p/'work.py').exists())
SOURCE=ROOT/'research/workspaces/customer-attraction/R-c4f1ef099fad483c9f81283b61eb0b53/six_astra/attractive_nested_exact.json'

def partition(xs):
    seen={};out=[]
    for x in xs:
        if x not in seen:seen[x]=len(seen)
        out.append(seen[x])
    return tuple(out)

def groupkey(g):return g[0],g[1],tuple(g[2]),tuple(g[3])

def main():
    raw=SOURCE.read_bytes();old=json.loads(raw);saved=json.loads((HERE/'repair_zz_exact.json').read_text())
    assert saved['source_sha256']==sha256(raw).hexdigest()
    hist={j:c for j,c in enumerate(old['columns']) if c['kind']=='hist'}
    oldr={};hi=None
    for c in old['columns']:
        if c['kind']=='hist':hi=old['columns'].index(c)
        if c['kind']=='joint-reply' and c['state'][0]:
            key=hi,groupkey(c['group']);oldr[key]=oldr.get(key,F())+F(c['weight'])
    variables={}
    for v in saved['variables']:
        assert 0<=F(v['z_mass'])<=F(v['mass'])
        variables[v['mode'],groupkey(v['group'])]=F(v['z_mass'])
    modes=saved['modes'];recovered_hist={};recovered_r={};slacks={};comparisons=0
    for mi,mode in enumerate(modes):
        hi=mode['hist_column'];c=hist[hi];mass=F(mode['mass']);assert mass>0
        recovered_hist[hi]=recovered_hist.get(hi,F())+mass
        ones=set(map(groupkey,mode['r']))
        z={g:v for (ii,g),v in variables.items() if ii==mi}
        for g in z:
            recovered_r[hi,g]=recovered_r.get((hi,g),F())+mass*int(g in ones)
        a=tuple(map(int,c['actual_bits']));pa=sum(a[:4]);words=[]
        for word,count in zip(product((0,1),repeat=3),c['hist']):words.extend([word]*count)
        assert len(words)==6
        def grp(e):return e[0],int(e[1]==e[2]),words[e[1]],words[e[2]]
        labels=[e for e in product(range(2),range(6),range(6)) if e[0] or e[1]!=e[2]]
        for e in labels:
            ge=grp(e);r=int(ge in ones)
            for f in labels:
                gf=grp(f);key=e[0],f[0],partition((*e[1:],*f[1:]))
                slacks[key]=slacks.get(key,F())+(z[ge]-z[gf])/F(pa+r+1)
                comparisons+=1
    assert all(recovered_hist.get(hi,F())==F(c['weight']) for hi,c in hist.items())
    assert all(recovered_r.get(k,F())==q for k,q in oldr.items())
    assert min(slacks.values())>=0
    # The formerly most negative class is e=(B,i,j), f=(C,i,l), i,j,l distinct.
    key=0,1,(0,1,0,2)
    report={'scope':__doc__,'source_sha256':sha256(raw).hexdigest(),'repair_sha256':sha256((HERE/'repair_zz_exact.json').read_bytes()).hexdigest(),
            'fixed_hist_and_R_marginals_exact':True,'mode_count':len(modes),'literal_comparisons':comparisons,'nonempty_index_classes':len(slacks),
            'minimum_ZZ_slack':str(min(slacks.values())),'formerly_negative_class_slack':str(slacks[key]),
            'all_class_slacks':[{'class':[f,g,list(p)],'slack':str(v)} for (f,g,p),v in sorted(slacks.items())]}
    (HERE/'literal_zz_review.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='all_class_slacks'},indent=2))

if __name__=='__main__':main()
