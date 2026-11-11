"""Independent literal-query verification on all old R/Z terminal nodes.

No imports from any constructor/parser.  Explicitly expand S6, preserve the
true old-R prefix, count integer payoff coefficients, and accumulate exact
Fractions.  Orbit constancy is verified on each whole 66x66 coefficient array.
"""
from __future__ import annotations
from collections import Counter,defaultdict
from fractions import Fraction as Q
from hashlib import sha256
from itertools import permutations,product
from math import lcm
from pathlib import Path
import argparse,json
import numpy as np

KINDS=('R-R','R-Z','Z-R','Z-Z')

def sha(p):return sha256(p.read_bytes()).hexdigest()

def canonical(xs):
    d={};out=[]
    for x in xs:
        if x not in d:d[x]=len(d)
        out.append(d[x])
    return tuple(out)

def cls(e,f):return e[0],f[0],canonical(e[1:]+f[1:])

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--point',type=Path,required=True)
    ap.add_argument('--witness',type=Path,required=True);ap.add_argument('--audit',type=Path,required=True)
    ap.add_argument('--output',type=Path,required=True);args=ap.parse_args()
    inp=json.loads(args.point.read_bytes());w=json.loads(args.witness.read_bytes());audit=json.loads(args.audit.read_bytes())
    assert w['input_sha256']==audit['input_sha256']==sha(args.point)
    assert audit['witness_sha256']==sha(args.witness)
    cols=inp['columns'][:4849];masses=[Q(c['weight']) for c in cols]
    hist={};marg=defaultdict(dict);hi=None
    for j,c in enumerate(cols):
        if c['kind']=='hist':hi=j;hist[j]=c
        elif c['kind']=='joint-reply':
            gg=c['group'];g=(gg[0],gg[1],tuple(gg[2]),tuple(gg[3]))
            marg[hi].setdefault(g,{})[tuple(c['state'])]=masses[j]
    for h,gg in marg.items():
        for g,p in gg.items():p[0,0]=masses[h]-sum(p.values())
    ns=[tuple(x) for x in w['literal_node_order']]
    assert ns==[e for e in product(range(2),range(6),range(6)) if e[0] or e[1]!=e[2]]
    ni={e:i for i,e in enumerate(ns)}
    perms=[tuple(x) for x in w['symmetrization']['permutations']]
    assert len(perms)==720 and set(perms)==set(permutations(range(6)))
    inverse=np.empty((720,66),dtype=np.int64)
    for k,p in enumerate(perms):
        for i,(f,a,b) in enumerate(ns):inverse[k,ni[f,p[a],p[b]]]=i
    orbit=defaultdict(list)
    for i,e in enumerate(ns):
        for j,f in enumerate(ns):orbit[cls(e,f)].append((i,j))
    index={cl:(np.array([i for i,j in pairs]),np.array([j for i,j in pairs])) for cl,pairs in orbit.items()}
    values={phase:defaultdict(Q) for phase in ('A','B')}
    per_hist={phase:defaultdict(dict) for phase in ('A','B')}
    mass_sum=Q();scale=1;atoms_total=0;prefix_checks=0;own_checks=0;coefficient_checks=0
    weights={phase:Q(w[f'phase_{phase}_weight']) for phase in ('A','B')}
    assert sum(weights.values())==1 and min(weights.values())>=0
    for phase in ('A','B'):
      if not weights[phase]:continue
      for ent in w['phases'][phase]:
        h=ent['hist_column'];hc=hist[h];H=masses[h]
        assert ent['actual_bits']==hc['actual_bits'] and ent['hist']==hc['hist']
        ws=[z for z,n in zip(product(range(2),repeat=3),hc['hist']) for _ in range(n)]
        p=sum(int(x) for x in hc['actual_bits'][:3]);P=sum(int(x) for x in hc['actual_bits'][:4])
        gs=[(f,int(i==j),ws[i],ws[j]) for f,i,j in ns]
        oldden=np.array([p+ws[i][0]+ws[j][1+f]+1 for f,i,j in ns],dtype=np.int64)[inverse]
        for pi,perm in enumerate(perms):
            pws=[None]*6
            for i in range(6):pws[perm[i]]=ws[i]
            for k,(f,i,j) in enumerate(ns):
                assert oldden[pi,k]==p+pws[i][0]+pws[j][1+f]+1
                assert gs[inverse[pi,k]]==(f,int(i==j),pws[i],pws[j])
                prefix_checks+=1
        bp=list(map(Q,ent['interval_breakpoints']))
        assert bp==sorted(set(bp)) and bp[0]==0 and bp[-1]==H
        assert len(ent['atoms'])==len(bp)-1
        expected=[[Q() for _ in range(4)] for e in ns]
        local=defaultdict(Q)
        for ai,atom in enumerate(ent['atoms']):
            mass=Q(atom['mass']);assert mass==bp[ai+1]-bp[ai]>0
            ss=atom['states'];u=(bp[ai]+bp[ai+1])/2
            assert len(ss)==66
            for k,node in enumerate(ent['node_intervals']):
                assert tuple(node['literal'])==ns[k]
                bits=[]
                for kind in ('R','Z'):
                    ranges=[tuple(map(Q,x)) for x in node[kind]]
                    assert all(0<=a<=b<=H for a,b in ranges)
                    bits.append(int(any(a<=u<b for a,b in ranges)))
                assert 2*bits[0]+bits[1]==ss[k]
                expected[k][ss[k]]+=mass
            expanded=np.array(ss,dtype=np.int64)[inverse];r=expanded//2;z=expanded%2
            coef=[]
            for den in range(1,7):
                mask=(oldden==den).astype(np.int64)
                if not mask.any():continue
                own=(mask*r).sum(axis=0)[:,None]
                coef.append(('R-R',den,own-mask.T@r))
                coef.append(('R-Z',den,own-mask.T@z))
            for flag in (0,1):
                mask=(r==flag).astype(np.int64);den=P+1+flag
                own=(mask*z).sum(axis=0)[:,None]
                coef.append(('Z-R',den,own-mask.T@r))
                coef.append(('Z-Z',den,own-mask.T@z))
            for kind,den,mat in coef:
                for cl,(ii,jj) in index.items():
                    vals=mat[ii,jj];v=int(vals[0]);assert (vals==v).all()
                    coefficient_checks+=len(vals)
                    local[kind,cl]+=mass*Q(v,720*den)
            weighted=weights[phase]*mass/720
            scale=lcm(scale,weighted.denominator);mass_sum+=720*weighted;atoms_total+=720
        for k,g in enumerate(gs):
            assert expected[k]==[marg[h][g][st] for st in product(range(2),repeat=2)]
            own_checks+=1
        for kind in KINDS:
            for cl in orbit:
                v=local[kind,cl];values[phase][kind,cl]+=v;per_hist[phase][kind,cl][h]=v
    assert mass_sum==sum((masses[h] for h in hist),Q())
    saved={(r['kind'],(r['class'][0],r['class'][1],tuple(r['class'][2]))):r for r in audit['records']}
    literal=[];summary={};minima={};rows=[]
    for kind in KINDS:
        allv=[]
        for cl,pairs in orbit.items():
            a=values['A'][kind,cl];b=values['B'][kind,cl];v=weights['A']*a+weights['B']*b
            rec=saved[kind,cl]
            if weights['A']:assert a==Q(rec['phase_A'])/len(pairs)
            if weights['B']:assert b==Q(rec['phase_B'])/len(pairs)
            assert v==(weights['A']*Q(rec['phase_A'])+weights['B']*Q(rec['phase_B']))/len(pairs)
            rows.append({'kind':kind,'class':cl,'literal_queries':len(pairs),
                         'phase_A_per_literal':str(a) if weights['A'] else None,
                         'phase_B_per_literal':str(b) if weights['B'] else None,
                         'mixture_per_literal':str(v)})
            for i,j in pairs:
                literal.append({'kind':kind,'source':ns[i],'query':ns[j],'slack':str(v)})
                allv.append(v)
        summary[kind]={'queries':len(allv),'negative':sum(v<0 for v in allv),'zero':sum(v==0 for v in allv),'positive':sum(v>0 for v in allv)}
        minima[kind]={'minimum':str(min(allv)),'minimum_positive':str(min((v for v in allv if v>0),default=Q())),
                      'minimum_float':float(min(allv)),
                      'minimum_positive_float':float(min((v for v in allv if v>0),default=Q()))}
    out={'scope':'Exact common coverage completion for all 132 named R/Z terminal nodes querying the same 132 R/Z labels, with true R and Z prefixes; not full SPE',
        'input_path':str(args.point),'input_sha256':sha(args.point),'witness_sha256':sha(args.witness),
        'audit_sha256':sha(args.audit),'verification_source_sha256':sha(Path(__file__)),
        'full_network_feasible':all(v['negative']==0 for v in summary.values()),
        'arithmetic':'Integer 720-permutation membership counts, exact Fraction masses and direct payoffs',
        'phase_weights':{p:str(v) for p,v in weights.items()},
        'verified_positive_weight_phases':[p for p in weights if weights[p]],'summary':summary,'minima':minima,
        'literal_query_count':len(literal),'expanded_positive_atoms':atoms_total,
        'total_customer_mass':str(mass_sum),'unit_customer_scale':str(scale),'unit_scale_digits':len(str(scale)),
        'own_marginal_checks':own_checks,'true_R_prefix_checks':prefix_checks,
        'literal_integer_coefficient_checks':coefficient_checks,
        'class_records':rows,'literal_queries':literal}
    args.output.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k not in ('class_records','literal_queries','unit_customer_scale')},ensure_ascii=False))

if __name__=='__main__':main()
