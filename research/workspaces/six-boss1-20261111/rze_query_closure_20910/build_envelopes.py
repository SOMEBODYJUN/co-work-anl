"""Complete single-query upper envelopes at the cb45 20910 point.

Keep each real terminal history and its own source income.  All min terms
are upper envelopes, never common intersections.  Old state 00 remains
H-m01-m10-m11 until evaluation.  This script performs no optimization.
"""
from collections import Counter, defaultdict
from fractions import Fraction as F
from hashlib import sha256
from itertools import permutations, product
from pathlib import Path
import argparse
import gzip
import json

HERE=Path(__file__).resolve().parent
WORK=HERE.parent
ROOT=WORK.parents[2]
BASE=WORK/'z_successor_20910'
POINT=WORK/'full624_augmented_lp/recovery/augmented_lp_exact.json'
POINT_SHA='cb45ee6f8df153764c91bd77d0543527cc44719ff7cc43646ffce06a7921a932'
BASE_SHA='76573a43318fd55f38b5ccab8eee04b4c2e2bb7f54ea5b68a4c5bc4930f6c48b'
CERT_SHA='00c78a5f23de4ff30d5fc66af362d95767a8b67c101dfa863ad701cffa225c30'
OLD=4849
STATES=tuple(product((0,1),repeat=2))
WORDS=tuple(product((0,1),repeat=3))
NODES=tuple((f,i,j) for f,i,j in product(range(2),range(6),range(6)) if f or i!=j)

def sha(p): return sha256(p.read_bytes()).hexdigest()
def save(n,d): (HERE/n).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def sparse(r): return [[j,str(v)] for j,v in sorted(r.items()) if v]
def vector(xs): return {j:F(v) for j,v in xs}
def key(r): return tuple((j,v) for j,v in sorted(r.items()) if v)
def add(r,v,c=F(1)):
    for j,a in v.items(): r[j]+=c*a
def unit(j): return {j:F(1)}
def canon(xs):
    seen={}
    return ''.join(str(seen.setdefault(v,len(seen))) for v in xs)
def gp(words,e):
    f,i,j=e
    return f,int(i==j),words[i],words[j]
def group(x): return x[0],x[1],tuple(x[2]),tuple(x[3])

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--matrix',action='store_true');args=ap.parse_args()
    assert sha(POINT)==POINT_SHA
    assert sha(BASE/'symbolic_lift.json')==BASE_SHA
    assert sha(BASE/'exact_certificate.json')==CERT_SHA
    point=json.loads(POINT.read_bytes());base=json.loads((BASE/'symbolic_lift.json').read_bytes())
    cert=json.loads((BASE/'exact_certificate.json').read_bytes())
    olddesc=[{k:v for k,v in c.items() if k!='weight'} for c in point['columns'][:OLD]]
    assert olddesc==base['old_descriptors'] and cert['kind']=='primal'
    vals=[F(c['weight']) for c in point['columns'][:OLD]]+[F(v) for v in cert['new_values']]
    assert len(vals)==5625 and min(vals)>=0
    old=defaultdict(dict);hist={};b4=defaultdict(dict)
    for j,c in enumerate(olddesc):
        if c['kind']=='hist': h=j;hist[j]=c
        elif c['kind']=='joint-reply':
            # hist_column_old is a legacy index; the surrounding hist block
            # determines the present 4849-column coordinate.
            old[h].setdefault(group(c['group']),{})[tuple(c['state'])]=j
        elif c['kind']=='actual-B-family-state' and c['source']==4:
            b4[c['hist_column']][(*c['hidden'],c['ell']//6)]=j
    xs={(c['hist_column'],group(c['group']),tuple(c['old_state'])):OLD+i for i,c in enumerate(base['new_columns'])}
    assert len(hist)==len(b4)==16 and sum(map(len,old.values()))==194 and len(xs)==776
    assert all(set(states)==set(product((0,1),repeat=3)) for states in b4.values())

    def mass(h,g,s):
        return unit(old[h][g][s]) if s!=(0,0) else {h:F(1),**{j:F(-1) for j in old[h][g].values()}}
    def margin(h,g,typ):
        r=defaultdict(F)
        for s in STATES:
            if typ=='E': add(r,unit(xs[h,g,s]))
            elif s[0 if typ=='R' else 1]: add(r,mass(h,g,s))
        return dict(r)
    def bmargin(h,k): return {j:F(1) for s,j in b4[h].items() if s[k]}
    def evalv(r): return sum((a*vals[j] for j,a in r.items()),F())
    rows={};mins={}
    def row(name): return rows.setdefault(tuple(name),{'linear':defaultdict(F),'mins':defaultdict(F)})
    def lin(name,v,c=F(1)): add(row(name)['linear'],v,c)
    def plusmin(name,a,b,c):
        ka,kb=key(a),key(b)
        if ka==kb: lin(name,a,c); return
        k=tuple(sorted((ka,kb)))
        if k not in mins: mins[k]={'a':dict(k[0]),'b':dict(k[1])}
        row(name)['mins'][k]+=c
    nodeorbits=defaultdict(list);pairs=defaultdict(list)
    for f,i,j in NODES:
        nodeorbits[f,int(i==j)].append((f,i,j))
        for ff,k,l in NODES: pairs[f,ff,canon((i,j,k,l))].append(((f,i,j),(ff,k,l)))
    assert len(pairs)==42 and sum(map(len,pairs.values()))==4356
    perms=tuple(permutations(range(6)));orbit_checks=[]
    for orbit,members in sorted(pairs.items()):
        (f,i,j),(ff,k,l)=members[0]
        images=Counter(((f,p[i],p[j]),(ff,p[k],p[l])) for p in perms)
        assert images==Counter({m:720//len(members) for m in members})
        orbit_checks.append({'orbit':list(orbit),'size':len(members),'frequency':720//len(members),
                             'representative':[list(members[0][0]),list(members[0][1])],
                             'members':[[list(a),list(b)] for a,b in members]})

    # Source earnings are linear in the original full R/Z and new E joint states.
    for h,c in hist.items():
        bits=tuple(map(int,c['actual_bits']));P=sum(bits[:4]);p3=sum(bits[:3])
        words=tuple(w for w,n in zip(WORDS,c['hist']) for _ in range(n))
        assert len(words)==6
        for g in old[h]:
            for s in STATES:
                assert F(0)<=vals[xs[h,g,s]]<=evalv(mass(h,g,s))
        assert sum((vals[j] for j in b4[h].values()),F())==vals[h]
        sm={};inc={};bm={k:bmargin(h,k) for k in (0,1)}
        for g in old[h]:
            for typ in ('R','Z','E'): sm[g,typ]=margin(h,g,typ)
            inc[g,'E']={xs[h,g,s]:F(1,P+s[1]+1) for s in STATES}
            iz=defaultdict(F)
            for r,z in STATES:
                if z:add(iz,mass(h,g,(r,z)),F(1,P+r+1))
            inc[g,'Z']=dict(iz)
        for orbit,members in pairs.items():
            fac=F(1,len(members));blockcount=Counter((gp(words,e),gp(words,f),e==f) for e,f in members)
            for (ge,gf,same),mult in blockcount.items():
                w=fac*mult
                for source,target in (('E','R'),('E','Z'),('E','E'),('Z','E')):
                    name=(source+'-to-'+target,*orbit)
                    lin(name,inc[ge,source],w);lin(name,sm[gf,target],-w/F(P+1))
                    if same:
                        overlap=defaultdict(F)
                        if source=='E' and target=='R': add(overlap,mass(h,ge,(1,1)))
                        elif source=='E' and target=='Z': add(overlap,sm[ge,'Z'])
                        elif source=='E' and target=='E':
                            for s in STATES:
                                if s[1]: add(overlap,unit(xs[h,ge,s]))
                        elif source=='Z' and target=='E':
                            for s in STATES:
                                if s[0]: add(overlap,unit(xs[h,ge,s]))
                        lin(name,overlap,w/F((P+1)*(P+2)))
                    else: plusmin(name,sm[ge,'Z' if source=='E' else 'R'],sm[gf,target],w/F((P+1)*(P+2)))
        for orbit,members in nodeorbits.items():
            fac=F(1,len(members));counts=Counter(gp(words,e) for e in members)
            for g,mult in counts.items():
                w=fac*mult;d=p3+bits[5]+1
                name=('H2-to-E',*orbit)
                lin(name,{j:F(s[1],d+s[0]) for s,j in b4[h].items() if s[1]},w)
                lin(name,sm[g,'E'],-w/F(d))
                plusmin(name,bm[0],sm[g,'E'],w/F(d*(d+1)))
                for k in (0,1):
                    name=('E-to-H'+str(k+1),*orbit)
                    lin(name,inc[g,'E'],w);lin(name,bm[k],-w/F(P+1))
                    plusmin(name,sm[g,'Z'],bm[k],w/F((P+1)*(P+2)))
    assert len(rows)==177
    # Full expressions are retained, then deduplicated by exact coefficients.
    def exprkey(r): return key(r['linear']),tuple((k,v) for k,v in sorted(r['mins'].items()) if v)
    refs={};aliases=[];unique=[]
    for i,r in enumerate(base['rows']):refs[(tuple((j,F(v)) for j,v in r['row']),())]=('base',i,r['name'])
    refs[((),())]=('zero',None,[])
    for name,r in sorted(rows.items()):
        ek=exprkey(r)
        if ek in refs: ref=refs[ek]
        else:
            ref=('new',len(unique),list(name));refs[ek]=ref;unique.append((name,r))
        aliases.append({'requested':list(name),'reference_kind':ref[0],'reference_index':ref[1],'reference_name':ref[2]})
    minids={k:i for i,k in enumerate(sorted(mins))}
    serialized=[]
    for name,r in sorted(rows.items()):
        value=evalv(r['linear'])+sum((a*min(evalv(mins[k]['a']),evalv(mins[k]['b'])) for k,a in r['mins'].items()),F())
        serialized.append({'name':list(name),'linear':sparse(r['linear']),
                           'min_terms':[[minids[k],str(a)] for k,a in sorted(r['mins'].items()) if a],
                           'value':str(value),'float':float(value)})
    oldslacks=[sum((F(v)*vals[j] for j,v in r['row']),F()) for r in base['rows']]
    assert all(s>=0 for s in oldslacks) and list(map(str,oldslacks))==cert['row_slacks']
    negative=[r for r in serialized if F(r['value'])<0]
    summary={'point_sha256':POINT_SHA,'base_symbolic_sha256':BASE_SHA,'base_certificate_sha256':CERT_SHA,
             'histograms':len(hist),'zero_histograms':[h for h in hist if vals[h]==0],
             'old_columns':OLD,'groups':sum(map(len,old.values())),'E_columns':len(xs),'retained_base_rows':len(base['rows']),
             'pair_orbits':len(pairs),'pair_orbit_images':42*720,'requested_pair_rows':168,'requested_B4_rows':9,
             'unique_additional_rows':len(unique),'duplicate_or_zero_rows':len(aliases)-len(unique),
             'min_expressions':len(minids),'negative_rows':len(negative),'first_negative':negative[0] if negative else None,
             'minimum_row':min(serialized,key=lambda r:F(r['value']))['name'],
             'minimum_value':min((F(r['value']) for r in serialized),default=F()).__str__(),
             'family_counts':dict(Counter(r['name'][0] for r in serialized)),
             'negative_family_counts':dict(Counter(r['name'][0] for r in negative)),
             'all_retained_base_rows_nonnegative':True,'all_symbolic_columns_preserved':True,
             'common_realization_asserted':False,'optimization_calls':0}
    payload={'scope':'Complete individual-query upper envelopes; no common coupling or SPE conclusion.',
             'point_sha256':POINT_SHA,'base_symbolic_sha256':BASE_SHA,'base_certificate_sha256':CERT_SHA,
             'original_columns':OLD,'existing_new_columns':base['new_columns'],
             'min_expressions':[{'a':sparse(mins[k]['a']),'b':sparse(mins[k]['b']),
                                 'value':str(min(evalv(mins[k]['a']),evalv(mins[k]['b'])))} for k in sorted(mins)],
             'rows':serialized,'exact_deduplication':aliases,'summary':summary}
    save('fixed_envelopes.json',payload)
    save('orbit_audit.json',{'permutations':720,'pair_orbits':orbit_checks,
                            'node_orbits':[{'orbit':list(k),'members':[list(e) for e in es]} for k,es in sorted(nodeorbits.items())]})
    save('fixed_summary.json',summary)
    if args.matrix:
        cols=base['new_columns']+[{'kind':'positive-min-upper','a':sparse(mins[k]['a']),'b':sparse(mins[k]['b'])} for k in sorted(mins)]
        fullrows=list(base['rows'])
        for name,r in unique:
            v=defaultdict(F,r['linear'])
            for k,a in r['mins'].items():v[5625+minids[k]]+=a
            fullrows.append({'name':list(name),'row':sparse(v)})
        for k in sorted(mins):
            j=5625+minids[k]
            for side in ('a','b'):
                v=defaultdict(F,mins[k][side]);v[j]-=1
                fullrows.append({'name':['min-upper',j,side],'row':sparse(v)})
        matrix={'scope':'Necessary complete single-query envelope lift. Min auxiliaries do not denote common intersections.',
                'point_path':str(POINT.relative_to(ROOT)),'point_sha256':POINT_SHA,
                'base_symbolic_sha256':BASE_SHA,'base_certificate_sha256':CERT_SHA,
                'original_columns':OLD,'old_descriptors':olddesc,'new_columns':cols,'rows':fullrows,
                'row_constants':0,'nonnegative_new_columns':True,'exact_deduplication':aliases,
                'hist_columns':list(hist),'zero_mass_hist_columns':[h for h in hist if vals[h]==0]}
        raw=(json.dumps(matrix,ensure_ascii=False,separators=(',',':'))+'\n').encode()
        with (HERE/'symbolic_lift.json.gz').open('wb') as out:
            with gzip.GzipFile(filename='',mode='wb',fileobj=out,mtime=0) as gz:gz.write(raw)
        size={'rows':len(fullrows),'new_columns':len(cols),'phase_I_columns':len(cols)+1,
              'old_columns':OLD,'all_symbolic_columns':OLD+len(cols),
              'base_rows':len(base['rows']),'new_query_rows':len(unique),'min_bound_rows':2*len(mins),
              'nonzero_coefficients':sum(len(r['row']) for r in fullrows),
              'uncompressed_bytes':len(raw),'compressed_bytes':(HERE/'symbolic_lift.json.gz').stat().st_size,
              'symbolic_lift_sha256':sha(HERE/'symbolic_lift.json.gz'),'optimization_calls':0}
        save('matrix_size.json',size);print(json.dumps(size))
    compact=dict(summary)
    if negative:compact['first_negative']={k:negative[0][k] for k in ('name','value','float')}
    print(json.dumps(compact,ensure_ascii=False))

if __name__=='__main__':main()
