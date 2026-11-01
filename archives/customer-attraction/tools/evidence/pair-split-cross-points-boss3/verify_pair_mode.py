"""Bind every compact coordinate, verify its full frozen sparse matrix, and
independently construct a common cube atom recipe and omitted safe prices.
No original main or optimizer is called. Each mode needs a fresh process.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product,combinations
from collections import Counter,defaultdict
import json,sys,time,hashlib,importlib,platform
HERE=Path(__file__).resolve().parent
BASE='research/workspaces/customer-attraction/R-5662d5cb0e5845a980ed10a3b3224cb1/research_5'
PAT=tuple(product((0,1),repeat=3));ORBS=((0,0),(1,0),(1,1))
def share(n,d):return F(n,d) if n else F()
def group(x):return x[0],x[1],tuple(x[2]),tuple(x[3])
def metadata(v):return json.loads(json.dumps({k:x for k,x in v.items() if k!='weight'}))
def grouped_columns(cols):
    gs=defaultdict(dict);hi=None
    for j,c in enumerate(cols):
        if c['kind']=='hist':hi=j
        elif c['kind']=='joint-reply':gs[hi].setdefault(group(c['group']),{})[tuple(c['state'])]=j
    return gs
def main():
    if len(sys.argv)!=3 or sys.argv[1] not in ('split','cross'):
        raise SystemExit('usage: verify_pair_mode.py split|cross /absolute/prepared-runtime')
    mode=sys.argv[1];runtime=Path(sys.argv[2]);assert runtime.is_absolute() and sys.flags.optimize==0
    filename='pair_closure_exact.json' if mode=='split' else 'pair_cross_exact.json'
    baseline_name='split_basic_exact.json' if mode=='split' else 'cross_source_priced_optimum_exact.json'
    primary=next(x for x in json.loads((HERE/'source-manifest.json').read_text()) if Path(x['path']).name==filename)
    raw=(HERE/primary['stored_path']).read_bytes()
    assert len(raw)==primary['size'] and hashlib.sha256(raw).hexdigest()==primary['sha256']
    assert (runtime/primary['path']).read_bytes()==raw
    point=json.loads(raw);assert set(point)=={'scope','W','O','rows','original_Z_variables','overlap_variables','minimum_slack','free_vertex_variables','variables'}
    saved=point['variables']
    for v in saved:
        assert tuple(v)==('hist_column','left','right','group','r','weight')
        assert isinstance(v['hist_column'],int) and v['r'] in (0,1)
        assert F(v['left'])>=0 and F(v['right'])>F(v['left'])
    script=runtime/BASE/'pair_closure.py'
    start=time.time();sys.argv=[str(script)]+(['--split'] if mode=='split' else ['--cross','--priced','--optimum'])
    sys.path.insert(0,str(script.parent));pc=importlib.import_module('pair_closure')
    old,vs,bounds,names,rows,bs,slabs,overlaps=pc.build();build_seconds=time.time()-start
    assert Path(pc.zz.SOURCE).name==baseline_name and not pc.zz.MASTER_MODE and pc.zz.SPLIT_MODE
    assert pc.zz.CROSS_MODE==(mode=='cross')
    assert len(vs)==len(saved)==point['original_Z_variables']
    assert [metadata(v) for v in vs]==[metadata(v) for v in saved]
    assert len(overlaps)==point['overlap_variables']
    assert len(names)==len(rows)==len(bs)==point['rows']
    nold=3945 if mode=='split' else 4927;nz=len(vs)
    assert len(rows)==nold+180+2*len(overlaps)
    ys=[F(v['weight']) for v in saved]
    assert all(0<=y<=b for y,b in zip(ys,bounds))
    for v,b in zip(vs,bounds):assert b==F(v['right'])-F(v['left'])>0
    cols=old['columns'];weights=[F(c['weight']) for c in cols]
    assert len(cols)==1905 and len(weights)==1905 and min(weights)>=0
    hist={j:c for j,c in enumerate(cols) if c['kind']=='hist'}
    assert len(hist)==16 and all(c['d']==1 and sum(c['hist'])==6 for c in hist.values())
    O=sum((weights[j]*int(c['d']>0) for j,c in hist.items()),F())
    W=sum((weights[j]*int(any(map(int,c['actual_bits']))) for j,c in hist.items()),F())
    assert O==F(point['O'])==1 and W==F(point['W'])==F(old['W'])
    groups=grouped_columns(cols);rm={(hi,g):weights[st[1,0]]+weights[st[1,1]] for hi,gs in groups.items() for g,st in gs.items()}
    expected=[];expected_slabs=0
    for hi,gs in groups.items():
        mass=weights[hi]
        assert all(0<=rm[hi,g]<=mass for g in gs)
        if not mass:continue
        cuts=sorted({F(),mass,*[rm[hi,g] for g in gs]})
        for l,u in zip(cuts,cuts[1:]):
            if u==l:continue
            expected_slabs+=1
            for g in gs:expected.append({'hist_column':hi,'left':str(l),'right':str(u),'group':[g[0],g[1],list(g[2]),list(g[3])],'r':int(u<=rm[hi,g])})
    assert [metadata(v) for v in saved]==expected
    assert len(slabs)==expected_slabs
    full=ys+[F()]*len(overlaps)
    for (key,j,k),v in overlaps.items():full[v]=min(ys[j],ys[k])
    slacks=[b+sum((v*full[j] for j,v in row.items() if v and full[j]),F()) for row,b in zip(rows,bs)]
    assert min(slacks)==F(point['minimum_slack'])==0 and all(s>=0 for s in slacks)
    raw_end=nold+180
    for row in rows[:raw_end]:
        assert all(v>=0 for j,v in row.items() if j>=nz)
    reportdir=HERE/'replay'/mode;reportdir.mkdir(parents=True,exist_ok=True)
    row_records=[{'row':j,'name':n,'slack':str(s)} for j,(n,s) in enumerate(zip(names,slacks))]
    (reportdir/'all-row-slacks.json').write_text(json.dumps(row_records,ensure_ascii=False,indent=2)+'\n')
    parts={}
    for label,l,u in [('old_affine',0,nold),('Z_to_Z',nold,nold+60),('PAIR_RZ',nold+60,nold+120),('PAIR_ZZ',nold+120,nold+180),('overlap_upper',nold+180,len(rows))]:
        vv=slacks[l:u];parts[label]={'rows':len(vv),'positive':sum(v>0 for v in vv),'zero':sum(v==0 for v in vv),'negative':sum(v<0 for v in vv),'minimum':str(min(vv)),'identically_zero_rows':sum(not rows[j] and not bs[j] for j in range(l,u))}
    # Independent conservation reconstruction of all old1905 coordinates.
    by_group=defaultdict(list)
    for j,v in enumerate(saved):by_group[v['hist_column'],group(v['group'])].append(j)
    mapped=[F()]*1905;mapped[0]=weights[0]
    for hi in hist:mapped[hi]=weights[hi]
    for hi,gs in groups.items():
        for g,st in gs.items():
            jj=by_group[hi,g];v11=sum((ys[j] for j in jj if saved[j]['r']),F());v01=sum((ys[j] for j in jj if not saved[j]['r']),F())
            mapped[st[1,1]]=v11;mapped[st[1,0]]=rm[hi,g]-v11;mapped[st[0,1]]=v01
            assert min(mapped[j] for j in st.values())>=0 and sum((mapped[j] for j in st.values()),F())<=weights[hi]
            assert mapped[st[1,0]]+mapped[st[1,1]]==rm[hi,g]
    for j,c in enumerate(cols):
        if c['kind']=='overlap':
            g,h=map(group,c['groups']);mapped[j]=min(rm[c['hist_column'],g],rm[c['hist_column'],h])
    assert min(mapped)>=0 and mapped[0]==weights[0] and all(mapped[hi]==weights[hi] for hi in hist)
    # Construct one common set of R/Z memberships, not independent pairwise choices.
    atoms=[];atoms_by_slab={};atom_z_checks=0;atom_overlap_checks=0
    for key,gs in slabs.items():
        hi,left,right=key;m=F(right)-F(left);indices=list(gs.values())
        cuts=sorted({F(),m,*[ys[j] for j in indices]});current=[]
        for l,u in zip(cuts,cuts[1:]):
            if u==l:continue
            atom={'hist_column':hi,'R_slab_left':left,'R_slab_right':right,'local_left':str(l),'local_right':str(u),'mass':str(u-l),'R_one_variables':[j for j in indices if saved[j]['r']],'Z_one_variables':[j for j in indices if u<=ys[j]]}
            atoms.append(atom);current.append(atom)
        assert sum((F(a['mass']) for a in current),F())==m
        for j in indices:
            assert sum((F(a['mass']) for a in current if j in a['Z_one_variables']),F())==ys[j];atom_z_checks+=1
        atoms_by_slab[key]=current
    for (key,j,k),idx in overlaps.items():
        actual=sum((F(a['mass']) for a in atoms_by_slab[key] if j in a['Z_one_variables'] and k in a['Z_one_variables']),F())
        assert actual==full[idx]==min(ys[j],ys[k]);atom_overlap_checks+=1
    assert sum((F(a['mass']) for a in atoms),F())==sum(weights[hi] for hi in hist)==1
    (reportdir/'common-cube-atom-recipe.json').write_text(json.dumps({'scope':'one rational common membership space before index permutation averaging/unit scaling; not a strategy','atoms':atoms,'total_mass':'1','all_Z_integrals_checked':atom_z_checks,'all_ZZ_min_intersections_checked':atom_overlap_checks},ensure_ascii=False,indent=2)+'\n')
    (reportdir/'mapped-1905-weights.json').write_text(json.dumps({'scope':'new Z and common-threshold RR interpretation, not original source or SPE','fixed_source_sha256':hashlib.sha256(Path(pc.zz.SOURCE).read_bytes()).hexdigest(),'weights':list(map(str,mapped))},indent=2)+'\n')
    # Independent actual-node prices that are outside these finite pair graphs.
    ui=[sum((weights[hi]*share(int(c['actual_bits'][i]),sum(map(int,c['actual_bits']))) for hi,c in hist.items()),F()) for i in range(6)]
    old_prices=[];caps=[]
    for i in range(6):
        for slot,label in ((1,'B'),(2,'C')):
            cost=sum((weights[hi]*F(sum(count*w[slot] for w,count in zip(PAT,c['hist'])),6-i+sum(map(int,c['actual_bits'][:i]))) for hi,c in hist.items()),F())
            old_prices.append({'actual_position':i+1,'family':label,'row_scale':'sum of six indexed topics','slack':str(6*ui[i]-cost)})
    for slot,label in ((1,'B'),(2,'C')):
        size=sum((weights[hi]*sum(count*w[slot] for w,count in zip(PAT,c['hist'])) for hi,c in hist.items()),F())
        caps.append({'family':label,'slack':str(6*weights[0]-size)})
    floor_rows=[]
    for i in range(6):
        for member in (0,1):
            for f,diag in ORBS:
                ct=6 if diag else 30;value=ct*ui[i]
                for hi,gs in groups.items():
                    c=cols[hi];den=6-i+sum(map(int,c['actual_bits'][:i]));hc={w:n for w,n in zip(PAT,c['hist'])}
                    for g,st in gs.items():
                        ff,dd,wi,wj=g
                        if (ff,dd)!=(f,diag):continue
                        mult=hc[wi] if diag else hc[wi]*hc[wj]-(hc[wi] if wi==wj else 0)
                        marginal=(mapped[st[1,0]]+mapped[st[1,1]]) if member==0 else (mapped[st[0,1]]+mapped[st[1,1]])
                        value-=mult*marginal/F(den)
                floor_rows.append({'key':[i,member,f,diag],'actual_position':i+1,'member':'R' if member==0 else 'Z','slack':str(value)})
    # Sizes in a uniformly index-permuted realization: each named orbit is uniform.
    sizes={f'actual-{i+1}':sum((weights[hi]*int(c['actual_bits'][i]) for hi,c in hist.items()),F()) for i in range(6)}
    for slot,label in enumerate(('T','B','C')):
        sizes[label+'-average']=sum((weights[hi]*F(sum(count*w[slot] for w,count in zip(PAT,c['hist'])),6) for hi,c in hist.items()),F())
    for member,label in ((0,'R'),(1,'Z')):
        for f,diag in ORBS:
            ct=6 if diag else 30;size=F()
            for hi,gs in groups.items():
                hc={w:n for w,n in zip(PAT,cols[hi]['hist'])}
                for g,st in gs.items():
                    ff,dd,wi,wj=g
                    if (ff,dd)!=(f,diag):continue
                    mult=hc[wi] if diag else hc[wi]*hc[wj]-(hc[wi] if wi==wj else 0)
                    marginal=(mapped[st[1,0]]+mapped[st[1,1]]) if member==0 else (mapped[st[0,1]]+mapped[st[1,1]])
                    size+=F(mult,ct)*marginal
            sizes[f'{label}-{f}-{diag}']=size
    assert all(v<=weights[0] for v in sizes.values())
    changed=Counter(cols[j]['kind'] for j,(a,b) in enumerate(zip(weights,mapped)) if a!=b)
    summary={'mode':mode,'status':'complete current frozen matrix and compact variable semantics verified',
      'point_sha256':hashlib.sha256(raw).hexdigest(),'point_header':{k:v for k,v in point.items() if k!='variables'},
      'fixed_source':str(Path(pc.zz.SOURCE).relative_to(runtime)),'fixed_source_sha256':hashlib.sha256(Path(pc.zz.SOURCE).read_bytes()).hexdigest(),
      'program_sha256':hashlib.sha256(script.read_bytes()).hexdigest(),'zz_program_sha256':hashlib.sha256((script.parent/'zz_threshold_closure.py').read_bytes()).hexdigest(),
      'effective_argv':sys.argv,'python':platform.python_version(),'build_seconds':build_seconds,'total_seconds':time.time()-start,
      'original_build_calls':1,'original_CLI_called':False,'optimizer_called':False,'all_variable_metadata_bound_both_native_and_threshold_reconstruction':True,
      'positive_histograms':sum(weights[hi]>0 for hi in hist),'R_slabs':len(slabs),'Z_variables':nz,'ZZ_overlap_variables':len(overlaps),
      'actual_zero_Z':sum(y==0 for y in ys),'actual_upper_Z':sum(y==b for y,b in zip(ys,bounds)),
      'actual_interior_Z':sum(0<y<b for y,b in zip(ys,bounds)),'saved_free_vertex_field':point['free_vertex_variables'],
      'old_R_marginals_preserved_all_groups':True,'changed_1905_coordinates_by_kind':dict(changed),
      'common_cube_atoms':len(atoms),'all_common_Z_marginals':atom_z_checks,'all_common_ZZ_minima':atom_overlap_checks,
      'O':str(O),'W':str(W),'K_fixed':str(weights[0]),'all_row_parts':parts,'all_rows_minimum':str(min(slacks)),
      'old_BC_price_rows':old_prices,'old_BC_capacity_rows':caps,'new_RZ_actual_floor_rows':floor_rows,
      'negative_old_BC_prices':[r for r in old_prices if F(r['slack'])<0],
      'negative_R_floors':[r for r in floor_rows if r['member']=='R' and F(r['slack'])<0],
      'negative_Z_floors':[r for r in floor_rows if r['member']=='Z' and F(r['slack'])<0],
      'orbit_theme_sizes':{k:str(v) for k,v in sizes.items()},'maximum_orbit_theme_size':str(max(sizes.values())),
      'K_attained_by_symbolic_catalogue_after_index_averaging':max(sizes.values())==weights[0],
      'limits':'Same original coefficient builder; independently read threshold/atom identities and omitted prices. No optimization, full SPE, or historical210ae7 code identification.'}
    (reportdir/'semantic-and-full-matrix-report.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in summary.items() if k not in ('old_BC_price_rows','old_BC_capacity_rows','new_RZ_actual_floor_rows','orbit_theme_sizes')},ensure_ascii=False))
if __name__=='__main__':main()
