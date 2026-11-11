"""Independent full-domain query and min-bound audit; no builder imports.

The inherited 893 rows have their separately rerun frozen literal audit.
Every additional row is rebuilt here from literal E=0/1 and full B4 states.
The plus sign of each min coefficient is checked by a full Boolean table.
"""
from collections import Counter,defaultdict
from fractions import Fraction as Q
from hashlib import sha256
from itertools import permutations,product
from pathlib import Path
import gzip
import json

HERE=Path(__file__).resolve().parent
POINT=HERE.parent/'full624_augmented_lp/recovery/augmented_lp_exact.json'
BASE=HERE.parent/'z_successor_20910'
EXPECTED='cb45ee6f8df153764c91bd77d0543527cc44719ff7cc43646ffce06a7921a932'

def sha(p):return sha256(p.read_bytes()).hexdigest()
def frac(n,d):
    if not d:assert not n;return Q()
    return Q(n,d)
def key(v):return tuple(sorted((j,c) for j,c in v.items() if c))
def decode(v):return {j:Q(c) for j,c in v}
def plus(out,vec,factor=Q(1)):
    for j,c in vec.items():out[j]+=factor*c
def sparse(v):return [[j,str(c)] for j,c in sorted(v.items()) if c]
def cname(v):
    order=[];out=[]
    for item in v:
        if item not in order:order.append(item)
        out.append(str(order.index(item)))
    return ''.join(out)

def main():
    assert sha(POINT)==EXPECTED
    point=json.loads(POINT.read_bytes());oldcols=point['columns'][:4849]
    lift=json.loads(gzip.decompress((HERE/'symbolic_lift.json.gz').read_bytes()))
    base=json.loads((BASE/'symbolic_lift.json').read_bytes())
    fixed=json.loads((HERE/'fixed_envelopes.json').read_bytes())
    exact=json.loads((BASE/'exact_certificate.json').read_bytes())
    inherited=json.loads((HERE/'inherited_independent_certificate_audit.json').read_bytes())
    assert inherited['all_776_rational_values_and_893_rows_verified']
    assert inherited['point_sha256']==EXPECTED==lift['point_sha256']
    assert inherited['symbolic_lift_sha256']==sha(BASE/'symbolic_lift.json')==lift['base_symbolic_sha256']
    assert sha(BASE/'exact_certificate.json')==lift['base_certificate_sha256']
    assert lift['old_descriptors']==[{k:v for k,v in c.items() if k!='weight'} for c in oldcols]
    assert lift['rows'][:893]==base['rows'] and lift['new_columns'][:776]==base['new_columns']
    val=[Q(c['weight']) for c in oldcols]+[Q(x) for x in exact['new_values']]
    hist={};rz=defaultdict(dict);b4=defaultdict(dict);column_hist={}
    for j,c in enumerate(oldcols):
        if c['kind']=='hist':h=j;hist[h]=c;column_hist[j]=h
        elif c['kind']=='joint-reply':
            f,d,wi,wj=c['group'];g=f,d,tuple(wi),tuple(wj)
            rz[h].setdefault(g,{})[tuple(c['state'])]=j;column_hist[j]=h
        elif c['kind']=='actual-B-family-state' and c['source']==4:
            b4[c['hist_column']][tuple(c['hidden'])+(c['ell']//6,)]=j;column_hist[j]=c['hist_column']
    xx={}
    for j,c in enumerate(lift['new_columns'][:776],4849):
        f,d,wi,wj=c['group'];g=f,d,tuple(wi),tuple(wj)
        xx[c['hist_column'],g,tuple(c['old_state'])]=j;column_hist[j]=c['hist_column']
    assert len(xx)==776 and len(hist)==16 and sum(map(len,rz.values()))==194
    assert all(set(states)==set(product((0,1),repeat=3)) for states in b4.values())
    def mass(h,g,r,z,e=None):
        old={rz[h][g][r,z]:Q(1)} if r or z else {h:Q(1),**{j:Q(-1) for j in rz[h][g].values()}}
        if e is None:return old
        if e:return {xx[h,g,(r,z)]:Q(1)}
        old[xx[h,g,(r,z)]]=Q(-1);return old
    def evalv(v):return sum((val[j]*c for j,c in v.items()),Q())
    def gp(words,e):return e[0],int(e[1]==e[2]),words[e[1]],words[e[2]]
    nodes=[(f,i,j) for i in range(6) for j in range(6) for f in (0,1) if f or i!=j]
    no=defaultdict(list);po=defaultdict(list)
    for e in nodes:
        no[e[0],int(e[1]==e[2])].append(e)
        for t in nodes:po[e[0],t[0],cname(e[1:]+t[1:])].append((e,t))
    assert len(po)==42 and len(no)==3
    perm=list(permutations(range(6)));frequency_checks=0
    for orb,items in po.items():
        e,t=items[-1]
        got=Counter(((e[0],p[e[1]],p[e[2]]),(t[0],p[t[1]],p[t[2]])) for p in perm)
        assert got==Counter({pair:720//len(items) for pair in items});frequency_checks+=720
    for orb,items in no.items():
        f,i,j=items[-1];got=Counter((f,p[i],p[j]) for p in perm)
        assert got==Counter({e:720//len(items) for e in items});frequency_checks+=720

    rebuilt={};literal_atoms=0;hist_frequency_images=0
    def rr(name):return rebuilt.setdefault(name,{'linear':defaultdict(Q),'mins':defaultdict(Q)})
    def line(name,v,scale):plus(rr(name)['linear'],v,scale)
    def upper(name,a,b,scale):
        assert scale>0
        aa,bb=key(a),key(b)
        if aa==bb:line(name,a,scale)
        else:rr(name)['mins'][tuple(sorted((aa,bb)))]+=scale
    for h,c in hist.items():
        bits=list(map(int,c['actual_bits']));P=sum(bits[:4]);p3=sum(bits[:3])
        words=[w for w,n in zip(product((0,1),repeat=3),c['hist']) for _ in range(n)]
        for orb,items in po.items():
            e,t=items[0]
            mapped=Counter((gp(words,(e[0],p[e[1]],p[e[2]])),
                            gp(words,(t[0],p[t[1]],p[t[2]])),e==t) for p in perm)
            direct=Counter((gp(words,a),gp(words,b),a==b) for a,b in items)
            assert mapped==Counter({k:n*(720//len(items)) for k,n in direct.items()})
            hist_frequency_images+=720
        src={};margin={}
        for g in rz[h]:
            atoms=[((r,z,e),mass(h,g,r,z,e)) for r,z,e in product((0,1),repeat=3)]
            for source in ('E','Z'):
                v=defaultdict(Q)
                for (r,z,e),m in atoms:
                    income=frac(e,P+z+e) if source=='E' else frac(z,P+r+z)
                    plus(v,m,income);literal_atoms+=1
                src[g,source]=v
            for target,k in [('R',0),('Z',1),('E',2)]:
                v=defaultdict(Q)
                for s,m in atoms:plus(v,m,s[k])
                margin[g,target]=v
                assert evalv(v)>=0 and evalv(v)<=val[h]
        for orb,pairlist in po.items():
            grouped=Counter((gp(words,e),gp(words,t),e==t) for e,t in pairlist)
            for (g,t,same),multiplicity in grouped.items():
                factor=Q(multiplicity,len(pairlist))
                for source,target in [('E','R'),('E','Z'),('E','E'),('Z','E')]:
                    name=(source+'-to-'+target,*orb)
                    if same:
                        for r,z,e in product((0,1),repeat=3):
                            pbit=z if source=='E' else r
                            choose=e if source=='E' else z
                            query={'R':r,'Z':z,'E':e}[target]
                            coefficient=frac(choose,P+pbit+choose)-frac(query,P+pbit+query)
                            line(name,mass(h,g,r,z,e),factor*coefficient);literal_atoms+=1
                    else:
                        line(name,src[g,source],factor)
                        line(name,margin[t,target],-factor/Q(P+1))
                        upper(name,margin[g,'Z' if source=='E' else 'R'],margin[t,target],factor/Q((P+1)*(P+2)))
        for orb,items in no.items():
            bmargin={k:{j:Q(1) for s,j in b4[h].items() if s[k]} for k in (0,1)}
            for g,n in Counter(gp(words,e) for e in items).items():
                factor=Q(n,len(items));d=p3+bits[5]
                name=('H2-to-E',*orb)
                for (h1,h2,y),j in b4[h].items():line(name,{j:Q(1)},factor*frac(h2,d+h1+h2));literal_atoms+=1
                line(name,margin[g,'E'],-factor/Q(d+1))
                upper(name,bmargin[0],margin[g,'E'],factor/Q((d+1)*(d+2)))
                for k in (0,1):
                    name=('E-to-H'+str(k+1),*orb)
                    line(name,src[g,'E'],factor);line(name,bmargin[k],-factor/Q(P+1))
                    upper(name,margin[g,'Z'],bmargin[k],factor/Q((P+1)*(P+2)))
    assert len(rebuilt)==177
    mins={}
    for i,c in enumerate(lift['new_columns'][776:]):
        assert c['kind']=='positive-min-upper'
        a,b=decode(c['a']),decode(c['b']);mk=tuple(sorted((key(a),key(b))))
        assert mk not in mins and key(a)!=key(b)
        mins[mk]=5625+i
    expected_minset={k for r in rebuilt.values() for k,c in r['mins'].items() if c}
    assert set(mins)==expected_minset
    assert len(mins)==10258
    transports=0
    for (a,b),j in mins.items():
        hs={column_hist[k] for k,c in (*a,*b) if c};assert len(hs)==1
        h=next(iter(hs));u=evalv(dict(a));v=evalv(dict(b));m=min(u,v);H=val[h]
        cells=[H-u-v+m,v-m,u-m,m]
        assert min(cells)>=0 and sum(cells,Q())==H
        assert cells[2]+cells[3]==u and cells[1]+cells[3]==v
        assert str(m)==fixed['min_expressions'][j-5625]['value']
        transports+=1
    value_by_name={};allcoefficients=0
    for saved in fixed['rows']:
        name=tuple(saved['name']);r=rebuilt[name]
        assert key(decode(saved['linear']))==key(r['linear'])
        expected={mins[k]-5625:v for k,v in r['mins'].items() if v}
        assert {j:Q(v) for j,v in saved['min_terms']}==expected
        s=evalv(r['linear'])+sum((coef*min(evalv(dict(k[0])),evalv(dict(k[1]))) for k,coef in r['mins'].items()),Q())
        assert str(s)==saved['value'];value_by_name[name]=s
        allcoefficients+=len(key(r['linear']))+len(expected)
    # Rebuild every exact duplicate and zero alias before checking linearization.
    def ek(r):return key(r['linear']),tuple((k,v) for k,v in sorted(r['mins'].items()) if v)
    refs={(key(decode(r['row'])),()):('base',i,r['name']) for i,r in enumerate(base['rows'])}
    refs[((),())]=('zero',None,[]);unique=[];mapping=[]
    for name,r in sorted(rebuilt.items()):
        k=ek(r)
        if k not in refs:refs[k]=('new',len(unique),list(name));unique.append((name,r))
        typ,i,nm=refs[k]
        mapping.append({'requested':list(name),'reference_kind':typ,'reference_index':i,'reference_name':nm})
    assert mapping==lift['exact_deduplication']==fixed['exact_deduplication']
    assert len(unique)==163
    expected_rows=[]
    for name,r in unique:
        v=defaultdict(Q,r['linear'])
        for k,c in r['mins'].items():v[mins[k]]+=c;assert c>0
        expected_rows.append({'name':list(name),'row':sparse(v)})
    for (a,b),j in sorted(mins.items(),key=lambda item:item[1]):
        for side,vv in [('a',a),('b',b)]:
            v=defaultdict(Q,dict(vv));v[j]-=1
            expected_rows.append({'name':['min-upper',j,side],'row':sparse(v)})
    assert expected_rows==lift['rows'][893:]
    assert len(lift['rows'])==21572 and len(lift['new_columns'])==11034
    assert lift['nonnegative_new_columns'] is True and lift['row_constants']==0
    truths=Counter()
    for p in range(5):
        for prefix,query,chosen in product((0,1),repeat=3):
            true=frac(chosen,p+prefix+chosen)-frac(query,p+prefix+query)
            expression=frac(chosen,p+prefix+chosen)-frac(query,p+1)+frac(prefix*query,(p+1)*(p+2))
            assert true==expression;truths['literal_terminal_query']=truths['literal_terminal_query']+1
    wallets=[]
    for name in sorted(rebuilt):
        kind=name[0]
        if kind in ('E-to-R','E-to-Z','E-to-E','Z-to-E'):
            items=po[tuple(name[1:])];sources=Counter(a for a,b in items)
            assert len(set(sources.values()))==1
            wallet={'name':list(name),'weight':str(Q(1,len(items))),
                    'source_count':len(sources),'source_multiplicity':next(iter(sources.values())),
                    'source_history':'(A1,A2,A3,A4,Z_e)' if kind.startswith('E-') else '(A1,A2,A3,A4,R_e)',
                    'source_denominator':'P+z_e+1' if kind.startswith('E-') else 'P+r_e+1'}
        else:
            items=no[tuple(name[1:])]
            wallet={'name':list(name),'weight':str(Q(1,len(items))),
                    'source_count':1 if kind=='H2-to-E' else len(items),
                    'source_multiplicity':len(items) if kind=='H2-to-E' else 1,
                    'source_history':'(A1,A2,A3,A6,H1)' if kind=='H2-to-E' else '(A1,A2,A3,A4,Z_e)',
                    'source_denominator':'p3+a6+h1+1' if kind=='H2-to-E' else 'P+z_e+1'}
        wallet.update(global_fixed_weight=True,source_budget_paid_once=True,
                      customer_or_hist_dependent_row_weights=False)
        wallets.append(wallet)
    (HERE/'wallet_audit.json').write_text(json.dumps({'wallets':wallets},ensure_ascii=False,indent=2)+'\n')
    report={'scope':'Independent full-domain symbolic and literal audit of all single-query upper envelopes; no common realization.',
            'point_sha256':sha(POINT),'symbolic_lift_sha256':sha(HERE/'symbolic_lift.json.gz'),
            'fixed_envelopes_sha256':sha(HERE/'fixed_envelopes.json'),'audit_source_sha256':sha(Path(__file__)),
            'inherited_audit_sha256':sha(HERE/'inherited_independent_certificate_audit.json'),
            'histograms':len(hist),'zero_mass_histograms':[h for h in hist if val[h]==0],
            'old_columns':4849,'new_E_columns':776,'min_columns':len(mins),'all_new_columns':11034,
            'retained_rows':893,'requested_envelope_rows':177,'unique_added_query_rows':len(unique),
            'min_bound_rows':20516,'all_rows_checked':21572,
            'all_nonzero_coefficients_checked':sum(len(r['row']) for r in lift['rows']),
            'requested_envelope_coefficients_checked':allcoefficients,
            'four_index_orbits':42,'node_orbits':3,'permutation_images':frequency_checks,
            'all_16_hist_pair_group_frequency_images':hist_frequency_images,
            'literal_state_evaluations':literal_atoms,'boolean_truth_tables':dict(truths),
            'maximal_2x2_transport_checks':transports,'all_min_main_coefficients_positive':True,
            'all_min_auxiliary_bounds_nonnegative_and_le_both':True,'every_B4_wallet_from_full_8_states':True,
            'B4_third_bit_queried_as_label':False,'duplicate_mappings_checked':len(mapping),
            'source_wallets_checked':len(wallets),'every_source_budget_paid_once':True,
            'negative_fixed_E_rows':sum(v<0 for v in value_by_name.values()),'optimization_calls':0,'passed':True}
    (HERE/'preflight_literal_audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(report,ensure_ascii=False))

if __name__=='__main__':main()
