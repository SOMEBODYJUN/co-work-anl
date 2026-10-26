"""Independent representation replay for the new explicit joint atom point.

This file does not import joint_atoms.  It aggregates complete assignments into
the previously frozen 3889-row schema, calls that original exact verifier, and
computes all sixty Z->Z classes directly from 66 labeled replies per atom.
The old verifier's scope and implementation limitations are inherited.
"""
from pathlib import Path
from collections import defaultdict
from fractions import Fraction as F
from itertools import product
import hashlib,json,sys

HERE=Path(__file__).resolve().parent
ROOT=next(p for p in HERE.parents if (p/'work.py').exists())
OLD=ROOT/'research/workspaces/customer-attraction/R-c4f1ef099fad483c9f81283b61eb0b53/six_astra'
sys.path.insert(0,str(OLD))
import attractive_nested as old

def partition(xs):
    result=[];lookup={}
    for x in xs:
        if x not in lookup:lookup[x]=len(lookup)
        result.append(lookup[x])
    return tuple(result)

def canonical_group(g):return g[0],g[1],tuple(g[2]),tuple(g[3])

def main():
    file=HERE/'joint_atoms_exact.json';data=json.loads(file.read_text())
    original=json.loads((OLD/'attractive_nested_exact.json').read_text())
    histmass=defaultdict(F);states=defaultdict(F);rr=defaultdict(F)
    zz=defaultdict(F);w=F();o=F();atomcounts=defaultdict(int)
    pats={partition(x) for x in product(range(4),repeat=4)}
    for f,g,p in product(range(2),range(2),pats):zz[f,g,p]=F()
    for a in data['atoms']:
        hi=a['hist_index'];mass=F(a['weight']);assert mass>0
        h=data['histograms'][hi];r=a['R'];z=a['Z'];gs=list(map(canonical_group,data['groups'][hi]));gi={g:i for i,g in enumerate(gs)}
        assert len(r)==len(z)==len(gs) and all(b in (0,1) for b in r+z)
        histmass[hi]+=mass;atomcounts[hi]+=1
        for j,g in enumerate(gs):states[hi,g,r[j],z[j]]+=mass
        for i,g in enumerate(gs):
            for j,gg in enumerate(gs):
                if r[i] and r[j]:rr[hi,tuple(sorted((g,gg)))]+=mass
        actual=tuple(map(int,h['actual_bits']));pa=sum(actual[:4])
        words=[p for p,n in zip(product(range(2),repeat=3),h['hist']) for _ in range(n)]
        assert len(words)==6
        def bits(e):
            fam,i,j=e;index=gi[fam,int(i==j),words[i],words[j]]
            return r[index],z[index]
        edges=[e for e in product(range(2),range(6),range(6)) if e[0] or e[1]!=e[2]]
        for e in edges:
            re,ze=bits(e);f,i,j=e
            for ee in edges:
                _,zf=bits(ee);g,k,l=ee
                zz[f,g,partition((i,j,k,l))]+=mass*F(ze-zf,pa+re+1)
        w+=mass*int(any(actual));o+=mass*int(h['d']>0)
    assert o==1 and w==F(data['W']) and w<F(1,2)
    # Fill the old schema from explicit assignments, with no polynomial map.
    hi=-1
    for c in original['columns']:
        if c['kind']=='K':c['weight']=data['K']
        elif c['kind']=='hist':
            hi+=1;assert {k:v for k,v in c.items() if k!='weight'}=={k:v for k,v in data['histograms'][hi].items() if k!='weight'}
            c['weight']=str(histmass[hi])
        elif c['kind']=='joint-reply':
            r,z=c['state'];c['weight']=str(states[hi,canonical_group(c['group']),r,z])
        elif c['kind']=='overlap':
            # The recorded hist_column is an index in the old column array.
            before=original['columns'][:c['hist_column']+1]
            overlap_hi=sum(x['kind']=='hist' for x in before)-1
            pair=tuple(sorted(map(canonical_group,c['groups'])))
            # rr stores both ordered traversals when groups differ.
            c['weight']=str(rr[overlap_hi,pair]/2)
        else:raise AssertionError(c['kind'])
    original['W']=str(w);original['O']='1';original['strict_half_gap']=str(1-2*w)
    original['scope']='Exact aggregation of the new complete joint R,Z atom point into the frozen old lifted schema; not the old witness or an SPE'
    original['positive_columns']=sum(F(c['weight'])>0 for c in original['columns'])
    inherited=old.verify(original)
    assert min(zz.values())>=0
    report={'claim':'CA-SIX-EXPLICIT-RZ-ZZ-ATOMS-OBSTRUCTION-v1','source_sha256':hashlib.sha256(file.read_bytes()).hexdigest(),
      'scope':'exact feasible necessary-condition point on 16 old histograms, with complete joint R,Z membership atoms; not a game/SPE or half counterexample',
      'old_lifted_verification':inherited,'raw_rows':1143,'old_raw_rows':1083,'new_literal_ZZ_rows':60,
      'literal_ZZ_comparisons':len(data['atoms'])*66*66,'minimum_ZZ_slack':str(min(zz.values())),
      'O':str(o),'W':str(w),'strict_half_gap':str(1-2*w),'positive_atoms':len(data['atoms']),
      'positive_histograms':sum(v>0 for v in histmass.values()),'atom_counts':dict(atomcounts),
      'ZZ_slacks':[{'families':[f,g],'partition':list(p),'slack':str(v)} for (f,g,p),v in sorted(zz.items())]}
    (HERE/'joint_atoms_verify.json').write_text(json.dumps(report,indent=2)+'\n')
    (HERE/'joint_atoms_old_schema.json').write_text(json.dumps(original,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='ZZ_slacks'},indent=2))

if __name__=='__main__':main()
