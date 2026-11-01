"""Compare original added-row code with literal hidden states and ordered edges.

No original main, inherited full graph build, LP, or optimizer is invoked.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
from functools import lru_cache
from types import SimpleNamespace
from collections import Counter,defaultdict
import ast,json,sys,hashlib,runpy
HERE=Path(__file__).resolve().parent
PAT=tuple(product((0,1),repeat=3))
ORBS=((0,0),(1,0),(1,1))
def share(x,d):return F(x,d) if x else F()
def meta(c):return {k:v for k,v in c.items() if k!='weight'}
def specs():
    out=[]
    for actual_position in (4,5):
        i=actual_position-1;nf=6-actual_position
        for subject in ('R','Z'):
            for orb in ORBS:
                for query in (4,5,'self'):
                    for mode in (('all','last') if nf==2 else ('last',)):
                        for aa in (F(),F(1,4),F(1,2)):
                            for mu in (F(),F(1)):
                                alpha=(aa,)*nf if mode=='all' else (F(),)*(nf-1)+(aa,)
                                out.append((i,subject,orb,query,alpha,mu))
    return out
seen=set()
@lru_cache(None)
def literal(p,ell,t,q,alpha,mu):
    seen.add((p,ell,t,q,alpha,mu))
    vals=[]
    for hidden in product((0,1),repeat=len(alpha)):
        z=p+t+sum(hidden)
        vals.append(share(t,z)+sum((a*bit/F(ell+1) for a,bit in zip(alpha,hidden)),F())
                    -mu*share(hidden[-1],z)+mu*F(q,p+t+sum(hidden[:-1])+1))
    return min(vals)
def parse_groups(cols):
    groups=defaultdict(dict);hist=None
    for j,c in enumerate(cols):
        if c['kind']=='hist':hist=j
        elif c['kind']=='joint-reply':
            f,diag,wi,wj=c['group'];key=(f,diag,tuple(wi),tuple(wj))
            assert tuple(c['state']) in ((0,1),(1,0),(1,1))
            groups[hist].setdefault(key,{})[tuple(c['state'])]=j
    return groups
def reference(cols,sp):
    groups=parse_groups(cols);rows=[[F()]*len(cols) for _ in sp]
    for hi,gs in groups.items():
        c=cols[hi];a=tuple(map(int,c['actual_bits']));words=[w for w,count in zip(PAT,c['hist']) for _ in range(count)]
        assert len(words)==6
        for ri,(i,subject,(f,diag),query,alpha,mu) in enumerate(sp):
            p=sum(a[:i]);ell=sum(a[:5]);budget=share(a[i],sum(a))+sum(alpha)*share(a[5],sum(a))
            q=lambda t:t if query=='self' else a[query]
            zero=literal(p,ell,0,q(0),alpha,mu)
            for j,k in product(range(6),repeat=2):
                if int(j==k)!=diag:continue
                key=(f,diag,words[j],words[k]);states=gs[key]
                rows[ri][hi]+=budget-zero
                for (r,z),col in states.items():
                    t=r if subject=='R' else z
                    rows[ri][col]+=zero-literal(p,ell,t,q(t),alpha,mu)
    return rows
def reference_floors(cols):
    keys=tuple((i,member,f,diag) for i in range(6) for member in range(2) for f,diag in ORBS)
    groups=parse_groups(cols);rows=[[F()]*len(cols) for _ in keys]
    for hi,gs in groups.items():
        c=cols[hi];a=tuple(map(int,c['actual_bits']));words=[w for w,count in zip(PAT,c['hist']) for _ in range(count)]
        for ri,(i,member,f,diag) in enumerate(keys):
            for j,k in product(range(6),repeat=2):
                if int(j==k)!=diag:continue
                rows[ri][hi]+=share(a[i],sum(a))
                for state,col in gs[f,diag,words[j],words[k]].items():
                    rows[ri][col]-=F(state[member],sum(a[:i])+6-i)
    return keys,rows
def audit_structure(point,expected_meta):
    cols=point['columns'];ys=[F(c['weight']) for c in cols]
    assert len(cols)==1905 and [meta(c) for c in cols]==expected_meta
    assert min(ys)>=0 and sum(v>0 for v in ys)==point['positive_columns']
    hist={i:c for i,c in enumerate(cols) if c['kind']=='hist'}
    assert len(hist)==16 and cols[0]['kind']=='K'
    schemas={'K':('kind','weight'),'hist':('kind','actual_bits','d','hist','weight'),'joint-reply':('kind','hist_column_old','group','state','weight'),'overlap':('kind','hist_column','groups','weight')}
    for c in cols:assert tuple(c)==schemas[c['kind']]
    for hi,c in hist.items():
        assert len(c['actual_bits'])==6 and set(c['actual_bits'])<=set('01')
        assert len(c['hist'])==8 and all(isinstance(x,int) and x>=0 for x in c['hist']) and sum(c['hist'])==6
        assert c['d']==sum(n*w[0] for n,w in zip(c['hist'],PAT))
    O=sum((ys[i]*int(c['d']>0) for i,c in hist.items()),F())
    W=sum((ys[i]*int('1' in c['actual_bits']) for i,c in hist.items()),F())
    assert O==F(point['O'])==1 and W==F(point['W']) and 1-2*W==F(point['strict_half_gap'])>0
    groups=parse_groups(cols);jcount=0;ocount=0
    for hi,gs in groups.items():
        for g,states in gs.items():
            assert set(states)=={(0,1),(1,0),(1,1)}
            assert sum((ys[j] for j in states.values()),F())<=ys[hi];jcount+=1
    for j,c in enumerate(cols):
        if c['kind']!='overlap':continue
        for raw in c['groups']:
            g=(raw[0],raw[1],tuple(raw[2]),tuple(raw[3]));states=groups[c['hist_column']][g]
            assert ys[j]<=ys[states[1,0]]+ys[states[1,1]];ocount+=1
    assert jcount==194 and ocount==2612
    return {'O':str(O),'W':str(W),'strict_half_gap_O_minus_2W':str(O-2*W),'K':str(ys[0]),'positive_columns':sum(v>0 for v in ys),'positive_by_kind':dict(Counter(c['kind'] for c,v in zip(cols,ys) if v>0)),'joint_bounds_checked':jcount,'overlap_bounds_checked':ocount,'all_columns_and_top_fields_preserved':True},ys
def main():
    if len(sys.argv)!=2:raise SystemExit('usage: audit_added_price_rows.py /absolute/repository')
    repo=Path(sys.argv[1]);manifest=json.loads((HERE/'source-manifest.json').read_text());points={}
    for rec in json.loads((HERE/'related-manifest.json').read_text()):
        data=(repo/rec['repository_path']).read_bytes()
        assert len(data)==rec['size'] and hashlib.sha256(data).hexdigest()==rec['sha256']

    for rec in manifest:
        source=(HERE if rec['storage_scope']=='package' else repo)/rec['stored_path']
        data=source.read_bytes();assert len(data)==rec['size'] and hashlib.sha256(data).hexdigest()==rec['sha256']
        if source.suffix=='.json':points[source.name]=json.loads(data)
    related=repo/'archives/customer-attraction/tools/evidence/all-reply-actual-floors-program/related/all_reply_floors_exact.json'
    points[related.name]=json.loads(related.read_text())
    original_code=HERE/'original/early_reply_prices.py'
    helper_path=repo/'archives/customer-attraction/tools/evidence/cross-source-graph-program/related/priced_hidden_reply.py'
    helper=runpy.run_path(str(helper_path))
    count_min=lru_cache(None)(helper['projected_by_count'])
    cols=points['cross_source_priced_optimum_exact.json']['columns'];expected_meta=[meta(c) for c in cols]
    def empty_build():return cols,[],[],[F()]*len(cols),[F()]*len(cols)
    ns={'F':F,'product':product,'ORBS':ORBS,'sys':SimpleNamespace(argv=[]),
        'nr':SimpleNamespace(PAT=PAT,share=share),'cross':SimpleNamespace(build=empty_build,psi=count_min)}
    tree=ast.parse(original_code.read_text());node=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='build')
    exec(compile(ast.Module(body=[node],type_ignores=[]),str(original_code),'exec'),ns)
    _,names,original,_,_=ns['build']();sp=specs();assert len(original)==len(sp)==324
    assert names==['early-reply-priced:'+str(x) for x in sp]
    independent=reference(cols,sp)
    for a,b in zip(original,independent):assert a==b
    floor_file=repo/'archives/customer-attraction/tools/evidence/all-reply-actual-floors-program/original/all_reply_actual_floors.py'
    ftree=ast.parse(floor_file.read_text());fnode=next(n for n in ftree.body if isinstance(n,ast.FunctionDef) and n.name=='added_rows')
    fkeys,floors=reference_floors(cols)
    fns={'F':F,'PAT':PAT,'KEYS':fkeys}
    exec(compile(ast.Module(body=[fnode],type_ignores=[]),str(floor_file),'exec'),fns)
    original_floors=fns['added_rows'](cols);assert original_floors==floors
    for p,ell,t,q,alpha,mu in seen:
        assert literal(p,ell,t,q,alpha,mu)==count_min(p,ell,t,q,alpha,(F(),)*len(alpha),mu)
    output={};point_values={}
    for filename,point in points.items():
        summary,ys=audit_structure(point,expected_meta)
        summaries=[];allvals=[]
        for group,keys,rows in (('early-price',sp,independent),('floor',fkeys,floors)):
            vals=[sum((v*ys[j] for j,v in enumerate(row) if v and ys[j]),F()) for row in rows]
            allvals+=vals
            summary[group]={'rows':len(vals),'negative_count':sum(v<0 for v in vals),'zero_count':sum(v==0 for v in vals),'minimum':str(min(vals))}
            summaries.extend({'group':group,'key':str(key),'slack':str(v)} for key,v in zip(keys,vals))
        if filename=='early_reply_exact.json':assert summary['early-price']['negative_count']==0
        if filename=='early_reply_floors_exact.json':assert summary['early-price']['negative_count']==summary['floor']['negative_count']==0
        output[filename]={'header':{k:v for k,v in point.items() if k!='columns'},'summary':summary,'new_row_slacks':summaries}
        point_values[filename]=ys
    def compare(a,b):
        xa,xb=points[a]['columns'],points[b]['columns']
        changed=[{'column':i,'kind':x['kind'],'old_weight':x['weight'],'new_weight':y['weight']} for i,(x,y) in enumerate(zip(xa,xb)) if F(x['weight'])!=F(y['weight'])]
        return {'old':a,'new':b,'all_1905_metadata_equal':True,'W_equal':points[a]['W']==points[b]['W'],'K_equal':xa[0]['weight']==xb[0]['weight'],'hist_masses_equal':all(x['weight']==y['weight'] for x,y in zip(xa,xb) if x['kind']=='hist'),'changed_weight_count':len(changed),'changed_by_kind':dict(Counter(c['kind'] for c in changed)),'changed_columns':changed}
    comparisons=[compare('cross_source_priced_optimum_exact.json','early_reply_exact.json'),compare('all_reply_floors_exact.json','early_reply_floors_exact.json'),compare('early_reply_exact.json','early_reply_floors_exact.json')]
    report={'status':'exact original-vs-literal added-row coefficients and saved-point evaluation completed',
        'original_added_build_only':True,'inherited_full_graph_built_by_this_audit':False,'LP_run_by_this_audit':False,
        'early_price_rows':324,'actual4_rows':216,'actual5_rows':108,'floor_rows':36,
        'price_coefficients_compared':324*1905,'floor_coefficients_compared':36*1905,'all_coefficients_compared':360*1905,
        'distinct_hidden_projection_keys':len(seen),'literal_binary_states':sum(2**len(k[4]) for k in seen),
        'compressed_candidates':sum(2*len(k[4]) for k in seen),'points':output,'comparisons':comparisons,
        'limits':'All-new 324+36 row coefficients on the inherited fixed16hist layout, plus four saved points. Full old4927/4963 not rerun here; two new complete original CLI verifications separately recorded; not complete SPE or optimum.'}
    (HERE/'replay/added-row-and-point-audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ('points','comparisons')},ensure_ascii=False))
    for name,value in output.items():print(name,json.dumps(value['summary'],ensure_ascii=False))
    for c in comparisons:print(json.dumps({k:v for k,v in c.items() if k!='changed_columns'},ensure_ascii=False))
if __name__=='__main__':main()
