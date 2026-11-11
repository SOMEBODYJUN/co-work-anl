"""Independent exact verification from saved interval/atom data.

Does not import the constructor or its parser.  Expands all 720 permutations
and evaluates (z_e-z_f)/(P+1+r_e) directly for every one of 4356 literal
queries.  Numpy performs only bounded integer counting; every mass and payoff
is a Fraction.  Also emits all 77040 rational customer atoms in gzip JSONL.
"""
from __future__ import annotations

from collections import Counter,defaultdict
from fractions import Fraction as Q
from hashlib import sha256
from itertools import permutations,product
from math import lcm
from pathlib import Path
import gzip
import json
import numpy as np

HERE=Path(__file__).resolve().parent
POINT=HERE.parent/'zz_closure_lp/round2/augmented_lp_exact.json'
WITNESS=HERE/'common_completion_19556.json'
EXPECTED='bf47390017e37f49f47a8f89126eb8e812982e16bd535adb555f042c178a2ca3'


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def canonical(xs):
    lookup={};out=[]
    for x in xs:
        if x not in lookup:
            lookup[x]=len(lookup)
        out.append(lookup[x])
    return tuple(out)


def cl(e,f):
    return e[0],f[0],canonical(e[1:]+f[1:])


def dump(path,obj):
    path.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')


def main():
    assert digest(POINT)==EXPECTED
    original=json.loads(POINT.read_bytes())
    w=json.loads(WITNESS.read_bytes())
    cols=original['columns'][:4849]
    masses=[Q(c['weight']) for c in cols]
    hist={};desired=defaultdict(dict);current=None
    for k,c in enumerate(cols):
        if c['kind']=='hist':
            current=k;hist[k]=c
        elif c['kind']=='joint-reply':
            g=c['group'];g=(g[0],g[1],tuple(g[2]),tuple(g[3]))
            desired[current].setdefault(g,{})[tuple(c['state'])]=masses[k]
    for hi,gg in desired.items():
        for g,p in gg.items():
            assert set(p)=={(0,1),(1,0),(1,1)}
            p[(0,0)]=masses[hi]-sum(p.values())
            assert min(p.values())>=0
    ns=[tuple(x) for x in w['literal_node_order']]
    expected_nodes=[x for x in product(range(2),range(6),range(6)) if x[0] or x[1]!=x[2]]
    assert ns==expected_nodes and len(ns)==66
    pos={e:i for i,e in enumerate(ns)}
    perms=[tuple(x) for x in w['symmetrization']['permutations']]
    assert set(perms)==set(permutations(range(6))) and len(perms)==720
    # inverse[p,target] gives the source node whose state is assigned to target.
    inverse=np.empty((720,66),dtype=np.int64)
    for pi,p in enumerate(perms):
        for source,(f,i,j) in enumerate(ns):
            inverse[pi,pos[f,p[i],p[j]]]=source
    phase_weights={'A':Q(w['phase_A_weight']),'B':Q(w['phase_B_weight'])}
    assert min(phase_weights.values())>0 and sum(phase_weights.values())==1
    slacks=[[Q() for _ in ns] for _ in ns]
    phase_slacks={phase:[[Q() for _ in ns] for _ in ns] for phase in ('A','B')}
    total_mass=Q();expanded_count=0;unit_scale=1;per_hist=[]
    expanded_path=HERE/'common_atoms_19556.jsonl.gz'
    with expanded_path.open('wb') as raw:
      with gzip.GzipFile(filename='',mode='wb',fileobj=raw,mtime=0) as gz:
        def write_obj(obj):
            gz.write((json.dumps(obj,sort_keys=True,separators=(',',':'))+'\n').encode())
        write_obj({'type':'header','source_witness_sha256':digest(WITNESS),
                   'node_order':ns,'state_encoding':['00','01','10','11'],
                   'note':'Every following record is one positive rational customer atom; repeat a record mass*unit_scale times after multiplying by the reported common denominator.'})
        for phase in ('A','B'):
          entries=w['phases'][phase]
          assert len(entries)==16 and {x['hist_column'] for x in entries}==set(hist)
          for ent in entries:
            hi=ent['hist_column'];h=hist[hi];H=masses[hi]
            assert ent['actual_bits']==h['actual_bits'] and ent['hist']==h['hist']
            P=sum(int(x) for x in h['actual_bits'][:4]);assert ent['P']==P
            ws=[word for word,n in zip(product(range(2),repeat=3),h['hist']) for _ in range(n)]
            assert len(ws)==6
            gs=[(f,int(i==j),ws[i],ws[j]) for f,i,j in ns]
            bp=list(map(Q,ent['interval_breakpoints']))
            assert bp==sorted(set(bp)) and bp[0]==0 and bp[-1]==H
            assert len(ent['atoms'])==len(bp)-1
            assert [tuple(x['literal']) for x in ent['node_intervals']]==ns
            actual=[[Q() for _ in range(4)] for _ in ns]
            # Explicitly verify that moving nodes and old words together keeps g.
            permuted_words=[]
            for pi,p in enumerate(perms):
                pws=[None]*6
                for i in range(6):pws[p[i]]=ws[i]
                for target,(f,i,j) in enumerate(ns):
                    assert gs[inverse[pi,target]]==(f,int(i==j),pws[i],pws[j])
                permuted_words.append([''.join(map(str,x)) for x in pws])
            for ai,atom in enumerate(ent['atoms']):
                mass=Q(atom['mass']);assert mass==bp[ai+1]-bp[ai]>0
                states=atom['states'];assert len(states)==66 and all(0<=x<=3 for x in states)
                midpoint=(bp[ai]+bp[ai+1])/2
                for k,node in enumerate(ent['node_intervals']):
                    bits=[]
                    for which in ('R','Z'):
                        intervals=[tuple(map(Q,x)) for x in node[which]]
                        assert all(0<=a<=b<=H for a,b in intervals)
                        bits.append(int(any(a<=midpoint<b for a,b in intervals)))
                    assert 2*bits[0]+bits[1]==states[k]
                    actual[k][states[k]]+=mass
                expanded=np.array(states,dtype=np.int64)[inverse]
                r=expanded//2;z=expanded%2
                # Whole direct-payoff integer coefficients over all 720 copies.
                r0=1-r
                own0=(r0*z).sum(axis=0)
                own1=(r*z).sum(axis=0)
                coef0=own0[:,None]-r0.T@z
                coef1=own1[:,None]-r.T@z
                unweighted=mass/720
                scaled=phase_weights[phase]*unweighted
                unit_scale=lcm(unit_scale,scaled.denominator)
                total_mass+=720*scaled
                for i in range(66):
                    for j in range(66):
                        direct=unweighted*(Q(int(coef0[i,j]),P+1)+Q(int(coef1[i,j]),P+2))
                        phase_slacks[phase][i][j]+=direct
                        slacks[i][j]+=phase_weights[phase]*direct
                for pi in range(720):
                    write_obj({'type':'atom','phase':phase,'hist':hi,'base_atom':ai,
                        'permutation':pi,'mass':str(scaled),'actual_bits':h['actual_bits'],
                        'old_words':permuted_words[pi],
                        'states':''.join(map(str,expanded[pi].tolist()))})
                    expanded_count+=1
            for k,g in enumerate(gs):
                assert actual[k]==[desired[hi][g][st] for st in product(range(2),repeat=2)]
            assert sum((Q(a['mass']) for a in ent['atoms']),Q())==H
            per_hist.append({'phase':phase,'hist':hi,'base_atoms':len(ent['atoms']),
                             'mass':str(H),'literal_own_marginals_verified':66,
                             'full_permutation_group_equivariance_checks':720*66})
    assert total_mass==sum((masses[h] for h in hist),Q())==1
    assert expanded_count==77040==w['positive_expanded_atoms']
    records={tuple((r['class'][0],r['class'][1],tuple(r['class'][2]))):r for r in w['records']}
    literal=[]
    for i,e in enumerate(ns):
        for j,f in enumerate(ns):
            cls=cl(e,f);record=records[cls]
            assert slacks[i][j]==Q(record['individual_IC_slack'])
            for phase in ('A','B'):
                assert phase_slacks[phase][i][j]==Q(record[f'phase_{phase}_orbit_sum'])/record['literal_pairs']
            assert slacks[i][j]>=0
            if i==j:assert slacks[i][j]==0
            else:assert slacks[i][j]>0
            literal.append({'source':e,'query':f,'class':cls,
                            'IC_direct_exact':str(slacks[i][j])})
    # Independently verify the six-IC cost identity on all 64 states and P=0..4.
    cost_check=[]
    for ss in product(range(4),repeat=3):
        rz=[divmod(s,2) for s in ss];n=Counter(ss)
        cost=n[1]*n[2]-n[0]*n[3]
        for P in range(5):
            direct=sum((Q(rz[i][1]-rz[j][1],P+1+rz[i][0])
                        for i in range(3) for j in range(3) if i!=j),Q())
            assert (P+1)*(P+2)*direct==cost
        cost_check.append({'states':ss,'cost':cost,'checked_P':list(range(5))})
    minimum=min(slacks[i][j] for i in range(66) for j in range(66) if i!=j)
    report={'scope':w['scope'],'input_sha256':digest(POINT),'witness_sha256':digest(WITNESS),
            'verification_source_sha256':digest(Path(__file__)),
            'direct_formula':'(z_source-z_query)/(P+1+r_source)',
            'integer_counts':'all 720 permutations explicitly expanded; int64 matrices only count 0/1 states',
            'mass_arithmetic':'fractions.Fraction throughout',
            'all_literal_queries_verified':4356,'strictly_positive_nonself':4290,
            'self_zero':66,'negative':0,'all_own_marginals_verified':True,
            'minimum_nonself_slack':str(minimum),'minimum_nonself_slack_float':float(minimum),
            'phase_B_weight':w['phase_B_weight'],'total_rational_customer_mass':str(total_mass),
            'positive_expanded_atoms':expanded_count,
            'expanded_atoms_path':str(expanded_path),'expanded_atoms_sha256':digest(expanded_path),
            'unit_customer_scale':str(unit_scale),'unit_customer_scale_decimal_digits':len(str(unit_scale)),
            'total_unit_customers_after_scaling':str(total_mass*unit_scale),
            'per_hist':per_hist,'six_IC_identity_all_64_states':cost_check,
            'literal_queries':literal}
    dump(HERE/'completion_verification.json',report)
    print(json.dumps({k:v for k,v in report.items() if k not in ('literal_queries','six_IC_identity_all_64_states','per_hist','unit_customer_scale','total_unit_customers_after_scaling')},ensure_ascii=False))


if __name__=='__main__':
    main()
