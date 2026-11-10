"""Round47 read-only native field consumption; no scientific row regeneration.

Reads every native field, preserves schema/family grouping losslessly, checks
the concrete threshold interface and compares already-saved certificates.
Never imports/runs the old generators or either prior independent auditor.
All output is confined to this script's staging directory. Run with python -B.
"""
from pathlib import Path
from collections import Counter, defaultdict
from fractions import Fraction as F
from itertools import product, combinations
import ast
import gzip
import hashlib
import json
import sys

ROOT = Path('/workspace/scratch/bbb425bb840f/co-work-anl-boss6')
HERE = Path(__file__).resolve().parent
TASK = 'customer-attraction-3a-3a-2b85a6bf64caddc5'
E = 'archives/customer-attraction/tools/evidence/'
PAIR = E+'full156-pair-master-point/original/pair_master_exact.json'
COMBINED = E+'full156-tail-parent-report/original/research_5/combined_branch_master_exact.json'
SLACK = E+'pair-threshold-closure-program/all-row-slacks.json'
ADDED = E+'full156-pair-master-point/current-added-row-audit.json'
RUN = E+'pair-threshold-closure-program/run-report.json'
CONTRACT = E+'full156-kernel-generator/input-contract.json'

def sha(b): return hashlib.sha256(b).hexdigest()
def pin(x): return sha(json.dumps(x, ensure_ascii=False,sort_keys=True,separators=(',',':')).encode())
def dump(p,x): p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def read(p): return json.loads((ROOT/p).read_text())
def group(g):
    f,d,wi,wj=g
    assert f in (0,1) and d in (0,1) and len(wi)==len(wj)==3
    assert all(x in (0,1) for x in wi+wj)
    assert not (f==0 and d==1)
    return f,d,tuple(wi),tuple(wj)

def family(name):
    if name.startswith('('): return 'tuple:'+str(ast.literal_eval(name)[0])
    if name.startswith('old_') and name[4:].isdigit(): return 'old-position'
    if name.startswith('new_B_'): return 'new_B'
    if name.startswith('new_C_'): return 'new_C'
    return name.split(':',1)[0]

def stat(records):
    vals=[F(x['slack']) for x in records]
    return dict(rows=len(vals), positive=sum(x>0 for x in vals),zero=sum(x==0 for x in vals),negative=sum(x<0 for x in vals),minimum=str(min(vals)),distinct_rationals=len(set(vals)))

def walk(x, counts):
    counts[type(x).__name__]+=1
    if isinstance(x,dict):
        for k,v in x.items(): assert isinstance(k,str);walk(v,counts)
    elif isinstance(x,list):
        for v in x:walk(v,counts)
    else: assert x is None or isinstance(x,(str,bool,int,float))

def main():
    assert not sys.flags.optimize
    task=read('research/operations/map-v2/tasks/'+TASK+'.json')
    ready=json.load(open('/workspace/scratch/bbb425bb840f/boss6-staging/ready-full156pair-round47.json'))
    registry=read('research/registry.json'); objects={x['object_id']:x for x in registry['objects']}
    assert (task['state'],task['owner'],task['request_id'])==('claimed','Boss6','cedc1aeda90c456184f42a585b8ba7d1')
    assert pin(task['definition'])==ready['definition_pin']=='078c5037e264e32a87d64bdd1791e7180b07b798efb1b091f04cc9d26a48ddca'
    assert task['definition']['input_pins']==ready['input_pins']
    references={}
    for oid,p in task['definition']['input_pins'].items():
        assert pin(objects[oid])==p
        for ref in [objects[oid]['body']]+objects[oid]['evidence']:
            b=(ROOT/ref['path']).read_bytes();assert sha(b)==ref['sha256']
            references[ref['path']]={'sha256':sha(b),'bytes':len(b)}
    pair=read(PAIR); combined=read(COMBINED); slacks=read(SLACK)
    added=read(ADDED); run=read(RUN); contract=read(CONTRACT)
    assert sha((ROOT/PAIR).read_bytes())=='090586fb86af4e80b33eb24893d72fa2d240d156d639bcb97a9f8b413eddb2d2'
    assert sha((ROOT/COMBINED).read_bytes())=='d1aeba67e20c8d8fc7ff38cd6566ac05c3771731f586584e5c6f1dfe233472a8'
    assert list(pair)==['scope','W','O','rows','original_Z_variables','overlap_variables','minimum_slack','free_vertex_variables','variables']
    assert list(combined)==['scope','base_rows','first_raw_rows','additional_index_class_rows','O','W','strict_half_gap','verified_rows','minimum_slack','positive_columns','columns']
    schemas={'K':['kind','weight'],'hist':['kind','actual_bits','d','hist','weight'],'joint-reply':['kind','hist_column_old','group','state','weight'],'overlap':['kind','hist_column','groups','weight']}
    hist={};hi=None;column_families=defaultdict(list); old_pointer_differences=0
    for i,c in enumerate(combined['columns']):
        assert list(c)==schemas[c['kind']];F(c['weight']);column_families[c['kind']].append([i,c])
        if c['kind']=='hist':
            hi=i; assert len(c['actual_bits'])==6 and set(c['actual_bits'])<={'0','1'}
            assert len(c['hist'])==8 and all(isinstance(n,int) and n>=0 for n in c['hist'])
            assert sum(c['hist'])==6
            hist[i]={'column':c,'mass':F(c['weight']),'states':{}}
        elif c['kind']=='joint-reply':
            g=group(c['group']);st=tuple(c['state']);assert st in ((0,1),(1,0),(1,1))
            assert st not in hist[hi]['states'].setdefault(g,{})
            hist[hi]['states'][g][st]=F(c['weight'])
            old_pointer_differences+=c['hist_column_old']!=hi
        elif c['kind']=='overlap':
            assert c['hist_column'] in hist and len(c['groups'])==2
            gg=[group(g) for g in c['groups']];assert gg[0]!=gg[1]
            assert all(g in hist[c['hist_column']]['states'] for g in gg)
    assert {k:len(v) for k,v in column_families.items()}=={'K':1,'hist':16,'joint-reply':582,'overlap':1306}
    PAT=tuple(product((0,1),repeat=3));positive={i:h for i,h in hist.items() if h['mass']}
    for i,h in hist.items():
        assert all(set(s)=={(0,1),(1,0),(1,1)} for s in h['states'].values())
        h['rad']={g:s[1,0]+s[1,1] for g,s in h['states'].items()}
        assert all(F()<=q<=h['mass'] for q in h['rad'].values())
        words=[w for w,n in zip(PAT,h['column']['hist']) for _ in range(n)]
        expected={(f,int(i==j),words[i],words[j]) for f,i,j in product(range(2),range(6),range(6)) if f or i!=j}
        assert expected==set(h['rad'])
        assert sum(n*w[0] for n,w in zip(h['column']['hist'],PAT))==h['column']['d']==1
    assert len(positive)==10 and sum(h['mass'] for h in hist.values())==1
    assert sum(h['mass'] for h in hist.values() if '1' in h['column']['actual_bits'])==F(pair['W'])==F(combined['W'])
    assert 1-2*F(pair['W'])==F(combined['strict_half_gap'])>0
    slab_groups=defaultdict(list); zsum=defaultdict(F);cursor=0;interface=[];aux=0
    for i,h in positive.items():
        cuts=sorted({F(),h['mass'],*h['rad'].values()});begin=cursor
        for lo,up in zip(cuts,cuts[1:]):
            key=(i,str(lo),str(up));assert lo<up
            for g,q in h['rad'].items():
                v=pair['variables'][cursor];assert list(v)==['hist_column','left','right','group','r','weight']
                assert (v['hist_column'],F(v['left']),F(v['right']),group(v['group']),v['r'])==(i,lo,up,g,int(up<=q))
                y=F(v['weight']);assert 0<=y<=up-lo
                zsum[i,g]+=y;slab_groups[str(key)].append([cursor,v]);cursor+=1
            aux+=len(h['rad'])*(len(h['rad'])-1)//2
        interface.append({'hist_column':i,'actual_bits':h['column']['actual_bits'],'histogram':h['column']['hist'],'mass':str(h['mass']),'groups':len(h['rad']),'slabs':len(cuts)-1,'Z_records':cursor-begin})
    assert cursor==364 and len(slab_groups)==29 and aux==2528
    changed=sum(zsum[i,g]!=s[0,1]+s[1,1] for i,h in positive.items() for g,s in h['states'].items())
    assert changed==contract['Z_marginals_different_from_old_raw']==73
    assert old_pointer_differences==525
    assert len(slacks)==10344 and all(list(r)==['index','name','slack'] and r['index']==i for i,r in enumerate(slacks))
    slack_families=defaultdict(list)
    for r in slacks:
        assert isinstance(r['name'],str);F(r['slack']);slack_families[family(r['name'])].append([r['index'],r])
    sections={}
    for name,s in run['row_sections'].items():
        actual=stat(slacks[s['begin_inclusive']:s['end_exclusive']]); sections[name]=actual
        assert all(actual[k]==s[k] for k in ('rows','positive','zero','negative','minimum'))
    assert sum(x['positive'] for x in sections.values())==3233 and sum(x['zero'] for x in sections.values())==7111
    compare=[]
    for name,start in [('Z_to_Z',5108),('PAIR_RZ',5168),('PAIR_ZZ',5228)]:
        rr=added['added_row_families'][name]['all_slacks'];assert len(rr)==60
        for j,r in enumerate(rr):
            row=slacks[start+j];nm=row['name']
            parsed=ast.literal_eval(nm[4:]) if name=='Z_to_Z' else ast.literal_eval(nm)
            got=(parsed[0],parsed[1],parsed[2]) if name=='Z_to_Z' else (parsed[1],parsed[2],parsed[3])
            assert got==(r['families'][0],r['families'][1],tuple(r['equality_pattern']))
            assert F(row['slack'])==F(r['slack'])
        compare.append({'family':name,'saved_records_compared':60,'all_exact_equal':True})
    assert sections['overlap_upper']['rows']==added['overlap_upper_bounds']==5056
    assert sections['overlap_upper']['zero']==added['zero_overlap_upper_slacks']==4574
    assert run['point_sha256']==sha((ROOT/PAIR).read_bytes()) and run['fixed_master_sha256']==sha((ROOT/COMBINED).read_bytes())
    assert run['all_row_slacks_sha256']==sha((ROOT/SLACK).read_bytes())
    assert run['source_sha256']==sha((ROOT/(E+'full156-pair-master-point/related/pair_closure.py')).read_bytes())
    assert run['wrapper_sha256']==sha((ROOT/(E+'pair-threshold-closure-program/capture_original.py')).read_bytes())
    assert run['stdout_sha256']==sha((ROOT/(E+'pair-threshold-closure-program/stdout.txt')).read_bytes())
    assert run['original_main_calls']==1 and run['linprog_or_solve_float_calls']==0
    # Complete reversible, family-grouped native reading; preserve every field.
    grouped={PAIR:{'head':{k:v for k,v in pair.items() if k!='variables'},'array_key':'variables','groups':dict(slab_groups)},COMBINED:{'head':{k:v for k,v in combined.items() if k!='columns'},'array_key':'columns','groups':dict(column_families)},SLACK:{'head':None,'array_key':None,'groups':dict(slack_families)}}
    byte_roundtrips={}
    for path,g in grouped.items():
        rows=sorted((r for block in g['groups'].values() for r in block),key=lambda r:r[0]);assert [r[0] for r in rows]==list(range(len(rows)))
        data=[r[1] for r in rows];decoded={**g['head'],g['array_key']:data} if g['head'] is not None else data
        encoded=(json.dumps(decoded,ensure_ascii=False,indent=2)+'\n').encode();assert encoded==(ROOT/path).read_bytes()
        byte_roundtrips[path]=True
    pack={'format':'lossless-schema-family-groups-v1','decode':'Flatten [original_index, exact_record] within each source groups; sort by original_index; restore array at array_key after ordered head; json.dumps(ensure_ascii=False,indent=2)+newline reproduces source bytes.','sources':grouped,'complete_small_contracts':{p:read(p) for p in (ADDED,RUN,CONTRACT)}}
    packed=gzip.compress(json.dumps(pack,ensure_ascii=False,separators=(',',':')).encode(),mtime=0)
    assert json.loads(gzip.decompress(packed))==pack
    (HERE/'native-lossless-reading.json.gz').write_bytes(packed)
    inventories={}
    for p in (PAIR,COMBINED,SLACK,ADDED,RUN,CONTRACT):
        data=read(p);counts=Counter();walk(data,counts)
        inventories[p]={'bytes':(ROOT/p).stat().st_size,'sha256':sha((ROOT/p).read_bytes()),'top_level_keys':list(data) if isinstance(data,dict) else None,'all_native_nodes_traversed_by_type':dict(counts),'read_mode':'all fields lossless schema/family consumption; not coefficient/LP regeneration'}
    canonical=[]
    core=task['definition']['object_ids'][0]
    for p in registry['edge_files']:
        edge=read(p)
        if core in edge['source_ids']+edge['target_ids']:canonical.append({'path':p,'sha256':sha((ROOT/p).read_bytes()),'reviewed_edge_id':edge['edge_id']})
    summary={'status':'PASS_NATIVE_FIELD_CONSUMPTION_AND_MATURE_CONTRACT_BINDINGS','scope':'Native field reading, source and concrete threshold interface only; saved slack comparisons, no new scientific feasibility run.','task_id':TASK,'owner':task['owner'],'request_id':task['request_id'],'definition_pin':pin(task['definition']),'object_pins':task['definition']['input_pins'],'all_registered_body_and_evidence_bytes_checked':references,'native_inventories':inventories,'lossless_byte_roundtrips':byte_roundtrips,'combined_column_schemas':schemas,'combined_column_family_counts':{k:len(v) for k,v in column_families.items()},'all_364_six_field_records_aligned_in_original_order':True,'hist_layer_interface':interface,'R_positive_layers':29,'new_Z_records':364,'overlap_auxiliaries':2528,'old_joint_pointer_not_current_count':old_pointer_differences,'changed_positive_hist_Z_marginals':changed,'saved_10344_sections':sections,'saved_slack_family_stats':{k:stat([r for _,r in v]) for k,v in slack_families.items()},'saved_180_comparisons':compare,'overlap_saved_statistics_equal':True,'canonical_core_endpoint_matches':canonical,'canonical_scan_count':len(registry['edge_files']),'new_scientific_runs':0,'new_prior_auditor_runs':0,'new_original_generator_runs':0,'not_claimed':['regeneration of original 10344 coefficients','new independent5236-row evaluation','scientific validation of every1905 old coordinate/row','matrix generation or24336-pair enumeration','full six-player strategy or universal half']}
    dump(HERE/'native-consumption.json',summary)
    print(json.dumps({'status':summary['status'],'columns':1905,'slabs':29,'records':364,'changed_Z_groups':changed,'saved_sections':sections,'compressed_lossless_bytes':len(packed),'canonical_matches':canonical,'new_scientific_runs':0},ensure_ascii=False,indent=2))

if __name__=='__main__':main()
