"""Build the full four-state E-successor necessary lift at the 20910 point.

Every new coordinate is an average of distinct, synchronously S6-indexed
labels, never an identification of their events.  The old 00 mass remains
H-m01-m10-m11 symbolically.  No common old R/Z customer network is fixed.
The optional complete old-R-to-E family needs no unknown intersections.
"""
from collections import Counter, defaultdict
from fractions import Fraction as F
from hashlib import sha256
from itertools import permutations, product
from pathlib import Path
import gzip
import json

HERE = Path(__file__).resolve().parent
WORK = HERE.parent
REPO = WORK.parents[2]
POINT = WORK/'full624_augmented_lp/recovery/augmented_lp_exact.json'
MATRIX = WORK/'full624_augmented_lp/recovery/exact_matrix.json.gz'
POINT_SHA = 'cb45ee6f8df153764c91bd77d0543527cc44719ff7cc43646ffce06a7921a932'
MATRIX_SHA = '96388092e21621f157b4428ce99f98b93afa99ed3a0c12c72b1d6475c26fba30'
DESC_SHA = 'afce2dcdff01e9393c04e317ee6bd52f5c0b378daedd92816647412243362460'
OLD = 4849
STATES = tuple(product((0,1), repeat=2))
WORDS = tuple(product((0,1), repeat=3))
NODES = tuple((f,i,j) for f,i,j in product(range(2),range(6),range(6)) if f or i!=j)


def sha(p):
    return sha256(p.read_bytes()).hexdigest()


def save(name, value):
    (HERE/name).write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n')


def canon(xs):
    d = {}
    return ''.join(str(d.setdefault(x,len(d))) for x in xs)


def group(raw):
    return raw[0],raw[1],tuple(raw[2]),tuple(raw[3])


def rawgroup(g):
    return [g[0],g[1],list(g[2]),list(g[3])]


def sparse(r):
    return [[j,str(v)] for j,v in sorted(r.items()) if v]


def share(n,d):
    return F(n,d) if n else F()


def main():
    assert sha(POINT)==POINT_SHA and sha(MATRIX)==MATRIX_SHA
    point=json.loads(POINT.read_bytes())
    matrix=json.loads(gzip.decompress(MATRIX.read_bytes()))
    assert len(matrix['rows'])==20910 and len(matrix['columns'])==20585
    assert all(c=={k:v for k,v in p.items() if k!='weight'}
               for c,p in zip(matrix['columns'],point['columns']))
    desc=matrix['columns'][:OLD]
    assert sha256(json.dumps(desc,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()==DESC_SHA
    weights=[F(c['weight']) for c in point['columns'][:OLD]]
    hist={}; groups=defaultdict(dict)
    for j,c in enumerate(desc):
        if c['kind']=='hist':
            h=j;hist[h]=c
        elif c['kind']=='joint-reply':
            groups[h].setdefault(group(c['group']),{})[tuple(c['state'])]=j
    assert len(hist)==16 and sum(map(len,groups.values()))==194
    assert len(NODES)==66 and all(v>=0 for v in weights)

    nodeorbits=defaultdict(list); tripleorbits=defaultdict(list); pairorbits=defaultdict(list)
    for e in NODES:
        f,i,j=e
        nodeorbits[f,int(i==j)].append(e)
        for k in range(6):tripleorbits[f,canon((i,j,k))].append((*e,k))
        for ee in NODES:
            ff,k,l=ee
            pairorbits[f,ff,canon((i,j,k,l))].append((*e,*ee))
    assert (len(nodeorbits),len(tripleorbits),len(pairorbits))==(3,8,42)

    # Count all 720 synchronous permutations, including stabilizer repetitions.
    perms=tuple(permutations(range(6)))
    orbit_checks=[]
    for kind,orbits in [('node',nodeorbits),('query-index',tripleorbits),('R-E-pair',pairorbits)]:
        for orb,members in sorted(orbits.items()):
            rep=members[0]
            if kind=='node':
                f,i,j=rep;freq=Counter((f,p[i],p[j]) for p in perms)
            elif kind=='query-index':
                f,i,j,k=rep;freq=Counter((f,p[i],p[j],p[k]) for p in perms)
            else:
                f,i,j,ff,k,l=rep;freq=Counter((f,p[i],p[j],ff,p[k],p[l]) for p in perms)
            assert set(freq)==set(members) and sum(freq.values())==720
            assert set(freq.values())=={720//len(members)}
            orbit_checks.append({'kind':kind,'orbit':list(orb),'size':len(members),
                                 'per_member_frequency':720//len(members),
                                 'representative':list(rep),'members':[list(t) for t in members]})

    cols=[]; xcols={}; named_groups=[]; oldmass=[]
    for h,c in hist.items():
        ws=tuple(w for w,n in zip(WORDS,c['hist']) for _ in range(n))
        assert len(ws)==6 and sum(w[0] for w in ws)==c['d']
        seen=defaultdict(list)
        for e in NODES:
            f,i,j=e;seen[f,int(i==j),ws[i],ws[j]].append(e)
        assert set(seen)==set(groups[h])
        for g,ids in groups[h].items():
            assert set(ids)==set(STATES[1:])
            masses={s:weights[j] for s,j in ids.items()}
            masses[0,0]=weights[h]-sum(masses.values(),F())
            assert min(masses.values())>=0
            for s in STATES:
                xcols[h,g,s]=OLD+len(cols)
                cols.append({'kind':'E-given-own-RZ-state','hist_column':h,
                             'group':rawgroup(g),'old_state':list(s),
                             'named_nodes':[list(e) for e in seen[g]],
                             'semantics':'Average of distinct synchronized label joint masses, not equal events.'})
                oldmass.append({'hist_column':h,'group':rawgroup(g),'old_state':list(s),
                                'value':str(masses[s])})
            named_groups.append({'hist_column':h,'group':rawgroup(g),'named_nodes':[list(e) for e in seen[g]],
                                 'multiplicity':len(seen[g])})
        for orb,members in nodeorbits.items():
            f,i,j=members[0]
            full=Counter((f,int(p[i]==p[j]),ws[p[i]],ws[p[j]]) for p in perms)
            direct=Counter((ff,int(ii==jj),ws[ii],ws[jj]) for ff,ii,jj in members)
            assert full==Counter({g:n*(720//len(members)) for g,n in direct.items()})
    assert len(cols)==776

    rows=defaultdict(lambda:defaultdict(F))
    def add(name,j,v):
        if v:rows[tuple(name)][j]+=v
    def mass(name,h,g,s,v):
        if s==(0,0):
            add(name,h,v)
            for j in groups[h][g].values():add(name,j,-v)
        else:add(name,groups[h][g][s],v)
    def node_group(h,e,ws):
        f,i,j=e
        return f,int(i==j),ws[i],ws[j]
    def xsum(name,h,g,v):
        for s in STATES:add(name,xcols[h,g,s],v)

    for h,c in hist.items():
        bits=tuple(map(int,c['actual_bits']))
        p3,P,total=sum(bits[:3]),sum(bits[:4]),sum(bits)
        ws=tuple(w for w,n in zip(WORDS,c['hist']) for _ in range(n))
        for g in groups[h]:
            for s in STATES:
                nm=('E-at-most-old-state',xcols[h,g,s])
                mass(nm,h,g,s,F(1));add(nm,xcols[h,g,s],-1)
        for orb,members in nodeorbits.items():
            fac=F(1,len(members))
            add(('A5-force-Z-with-E',*orb),h,share(bits[4],total))
            for k in range(1,7):
                nm=('A-safe-to-E',k,*orb) if k<6 else ('A6-to-E',*orb)
                add(nm,h,share(bits[k-1],total))
            for e in members:
                f,i,j=e;g=node_group(h,e,ws)
                for s in STATES:
                    r,z=s;x=xcols[h,g,s];den=P+z+1
                    nm=('A5-force-Z-with-E',*orb)
                    mass(nm,h,g,s,-fac*F(z,P+1))
                    add(nm,x,fac*F(z,(P+1)*(P+2)))
                    for k,ak in enumerate(bits,1):
                        nm=('E-to-A',k,*orb)
                        add(nm,x,fac/den);mass(nm,h,g,s,-fac*F(ak,den))
                    for slot,kind in enumerate(('R','Z')):
                        nm=('E-to-own-'+kind,*orb)
                        add(nm,x,fac/den);mass(nm,h,g,s,-fac*F(s[slot],den))
                    nm=('own-Z-to-E',*orb)
                    mass(nm,h,g,s,fac*F(z,P+r+1));add(nm,x,-fac/F(P+r+1))
                    add(('capacity-E',*orb),x,-fac)
                    for k in range(1,7):
                        nm=('A-safe-to-E',k,*orb) if k<6 else ('A6-to-E',*orb)
                        add(nm,x,-fac/F(sum(bits[:k-1])+7-k))
        for orb,members in tripleorbits.items():
            fac=F(1,len(members))
            for f,i,j,k in members:
                g=node_group(h,(f,i,j),ws)
                for slot,kind in enumerate(('T','B','C')):
                    nm=('E-to-'+kind,*orb)
                    for s in STATES:
                        den=P+s[1]+1
                        add(nm,xcols[h,g,s],fac/den)
                        mass(nm,h,g,s,-fac*F(ws[k][slot],den))
        for orb,members in pairorbits.items():
            fac=F(1,len(members))
            nm=('old-R-to-E',*orb)
            for f,i,j,ff,k,l in members:
                source=node_group(h,(f,i,j),ws)
                target=node_group(h,(ff,k,l),ws)
                den=p3+ws[i][0]+ws[j][1+f]+1
                for s in STATES:
                    mass(nm,h,source,s,fac*F(s[0],den))
                    add(nm,xcols[h,target,s],-fac/F(den))
    for orb in nodeorbits:add(('capacity-E',*orb),0,F(1))
    ordered=sorted(rows.items(),key=lambda nr:str(nr[0]))
    assert len(ordered)==893
    payload={
        'schema':1,
        'scope':'Necessary four-state E successor lift over all 16 fixed histograms; no fixed common old network, no cross-E/R/Z realization or SPE claim.',
        'point_path':str(POINT.relative_to(REPO)),'point_sha256':sha(POINT),
        'old_matrix_path':str(MATRIX.relative_to(REPO)),'old_matrix_sha256':sha(MATRIX),
        'original_columns':OLD,'point_columns':20585,'point_rows':20910,
        'old_descriptors':desc,'new_columns':cols,'rows':[{'name':list(nm),'row':sparse(r)} for nm,r in ordered],
        'row_constants':0,'nonnegative_new_columns':True,
        'zero_mass_hist_columns':[h for h in hist if weights[h]==0],
        'hist_columns':list(hist),'family_counts':dict(Counter(nm[0] for nm,r in ordered)),
        'new_column_count':len(cols),'group_count':len(named_groups),'named_node_count':len(NODES),
        'old_auxiliary_coefficients_absent':all(j<OLD+len(cols) for nm,r in ordered for j in r),
        'same_source_R_rows':[['old-R-to-E',0,0,'0101'],['old-R-to-E',1,1,'0101'],['old-R-to-E',1,1,'0000']],
        'added_cross_R_query_rows':39,
        'not_imposed':['Unknown cross-old-R/Z intersections','E-to-cross-old-R/Z queries','Cross-old-Z-to-E queries','E-to-E queries','Equality of same-group named events'],
    }
    save('symbolic_lift.json',payload)
    save('orbit_audit.json',{'scope':'All groupings are global synchronous S6 averages; no fractional query label is created.',
                            'permutations':720,'orbit_count':len(orbit_checks),'orbits':orbit_checks,
                            'permutation_images_checked':720*len(orbit_checks),
                            'hist_group_frequency_checks':16*3*720,
                            'named_groups':named_groups,'all_orbit_frequencies_exact':True})
    save('input_audit.json',{'point_sha256':sha(POINT),'matrix_sha256':sha(MATRIX),
                             'original_descriptor_sha256':DESC_SHA,'old_states':oldmass,
                             'original_positive_columns':sum(v>0 for v in weights),
                             'K':str(weights[0]),'W':point['W'],'O':point['O'],
                             'incomes':[str(sum(weights[h]*share(int(hist[h]['actual_bits'][k]),sum(map(int,hist[h]['actual_bits']))) for h in hist)) for k in range(6)],
                             'old_descriptors_match_full_matrix':True,'zero_state_formula_preserved':True,
                             'inputs':[{'path':str(p.relative_to(REPO)),'sha256':sha(p)} for p in [POINT,MATRIX,WORK/'main_20910_audit.json',WORK/'main_z_successor_contract.md',WORK/'main_exact_two_tail_contract.md',REPO/'archives/customer-attraction/state/定义/共同目录完整历史模型--定义.md']]})
    print(json.dumps({'rows':len(ordered),'new_columns':len(cols),'global_rows':len(ordered)-776,
                      'family_counts':payload['family_counts'],'point_sha256':sha(POINT),
                      'symbolic_lift_sha256':sha(HERE/'symbolic_lift.json')},ensure_ascii=False))


if __name__=='__main__':
    main()
