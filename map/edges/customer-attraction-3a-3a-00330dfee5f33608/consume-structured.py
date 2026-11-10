"""Read every JSON field and stored rational; never rebuild or evaluate an IC row.

This is a structural reading ledger, not a new scientific verification. The
author's phi/evaluate/verify/LP code is neither imported nor called. Original
tokens, pointer ranges, family index runs, schemas and exact payload digests
make the complete reading auditable without copying huge tables into prose.
"""
from pathlib import Path
from fractions import Fraction
from collections import Counter, defaultdict
from itertools import product, combinations
from bisect import bisect_right
from decimal import Decimal
import ast
import hashlib
import json
import re

REPO = Path('/workspace/scratch/bbb425bb840f/co-work-anl-boss6')
OUT = Path(__file__).parent
BASE = 'archives/customer-attraction/tools/evidence/'
POINT = BASE+'explicit-joint-rz-and-root-extension-primary/original/research/workspaces/customer-attraction/R-a8ee6fdb155c47da95540775b4a6a2db/closure/joint_atoms_exact.json'
SCHEMA = POINT.replace('joint_atoms_exact.json','joint_atoms_old_schema.json')
SLACK = BASE+'explicit-joint-rz-and-root-extension-primary/old3889-replay/all-old-slacks.json'
MID = BASE+'ra241-middle-new-source/original/research/workspaces/customer-attraction/R-a241704002304c95bca9ef95d516b61f/review/'
ZZ = BASE+'optimal-support-and-zz-audits-boss3/'
EXTRA = [
 BASE+'explicit-joint-rz-and-root-extension-primary/source-manifest.json',
 BASE+'explicit-joint-rz-and-root-extension-primary/full-field-review.json',
 BASE+'explicit-joint-rz-and-root-extension-primary/old3889-replay/event.json',
 ZZ+'original/closure_independent_review.json', ZZ+'replay/zz-prefix-review.json',
 ZZ+'replay/execution-record.json',
 BASE+'ra241-middle-new-source/source-manifest.json',
 BASE+'ra241-middle-new-source/complete-report-reading.json',
 BASE+'ra241-middle-new-source/execution-scope.json',
 MID+'middle_transport_audit.json',MID+'new_source_cut_audit.json',
 BASE+'ra241-second-source-primary/point-version-comparison.json',
]

def sha(b): return hashlib.sha256(b).hexdigest()
def enc(x): return json.dumps(x,ensure_ascii=False,separators=(',',':'),sort_keys=True,default=str).encode()
def runs(indices):
    result=[]
    for i in indices:
        if result and result[-1][1]==i: result[-1][1]=i+1
        else: result.append([i,i+1])
    return result

class CompleteJSON:
    """Recursive token reader retaining exact source ranges, including floats."""
    def __init__(self, name):
        self.name=name; self.raw=(REPO/name).read_bytes(); self.s=self.raw.decode(); self.pos=0
        self.nodes={}; self.leaves=[]; self.lines=[i for i,c in enumerate(self.s) if c=='\n']
        self.data=self.value(''); self.ws(); assert self.pos==len(self.s)
        # Independent standard JSON parse checks the structural reader's result.
        assert self.data==json.loads(self.s,parse_float=Decimal)
    def ws(self):
        while self.pos<len(self.s) and self.s[self.pos] in ' \t\r\n': self.pos+=1
    def value(self,p):
        self.ws(); start=self.pos; c=self.s[self.pos]
        if c=='{':
            self.pos+=1; self.ws(); v={}
            if self.s[self.pos]!='}':
                while True:
                    self.ws(); k,end=json.JSONDecoder().raw_decode(self.s,self.pos); assert isinstance(k,str); self.pos=end
                    self.ws(); assert self.s[self.pos]==':'; self.pos+=1
                    assert k not in v, ('duplicate key',p,k)
                    v[k]=self.value(p+'/'+k.replace('~','~0').replace('/','~1')); self.ws()
                    if self.s[self.pos]=='}': break
                    assert self.s[self.pos]==','; self.pos+=1
            self.pos+=1; typ='object'
        elif c=='[':
            self.pos+=1; self.ws(); v=[]
            if self.s[self.pos]!=']':
                while True:
                    v.append(self.value(p+'/'+str(len(v)))); self.ws()
                    if self.s[self.pos]==']': break
                    assert self.s[self.pos]==','; self.pos+=1
            self.pos+=1; typ='array'
        else:
            v,end=json.JSONDecoder(parse_float=Decimal).raw_decode(self.s,self.pos); self.pos=end
            typ=type(v).__name__; self.leaves.append((p,start,self.pos,typ))
        self.nodes[p]=(start,self.pos,typ)
        return v
    def span(self,p):
        a,b,t=self.nodes[p]
        return {'json_pointer':p,'char_range_half_open':[a,b],
         'utf8_byte_range_half_open':[len(self.s[:a].encode()),len(self.s[:b].encode())],
         'lines_inclusive':[bisect_right(self.lines,a)+1,bisect_right(self.lines,b-1)+1],
         'node_type':t,'exact_source_token_sha256':sha(self.s[a:b].encode())}
    def summary(self):
        h=hashlib.sha256()
        for p,a,b,t in self.leaves:
            h.update(enc([p,t]));h.update(b'\0');h.update(self.s[a:b].encode());h.update(b'\n')
        top=[]
        items=self.data.items() if isinstance(self.data,dict) else enumerate(self.data)
        for k,v in items:
            p='/'+str(k).replace('~','~0').replace('/','~1'); x=self.span(p)
            x['primitive_leaf_count']=sum(q==p or q.startswith(p+'/') for q,_,_,_ in self.leaves)
            x['length']=len(v) if isinstance(v,(list,dict)) else None
            if not isinstance(v,(list,dict)): x['value']=str(v) if isinstance(v,Decimal) else v
            top.append(x)
        return {'path':self.name,'sha256':sha(self.raw),'utf8_bytes':len(self.raw),
          'characters':len(self.s),'lines':len(self.s.splitlines()),'complete_char_range':[0,len(self.s)],
          'complete_byte_range':[0,len(self.raw)],'primitive_leaf_count':len(self.leaves),
          'primitive_types':dict(Counter(t for _,_,_,t in self.leaves)),
          'all_primitive_pointer_type_and_exact_token_stream_sha256':h.hexdigest(),
          'all_top_level_fields_consumed':top}

docs={p:CompleteJSON(p) for p in [POINT,SCHEMA,SLACK]+EXTRA}
point,old,slack=(docs[p].data for p in [POINT,SCHEMA,SLACK])
assert sha(docs[POINT].raw)=='b4c40bc9ab35ea5ba162d84e5f8020af54e66f9c167af11bbc07acf2185998a4'
assert sha(docs[SCHEMA].raw)=='50a8645a1b365e21b94ce601e4ce40fa3b44a2743735ec639e70ead44c0cefd4'
assert sha(docs[SLACK].raw)=='95a5aba2c3f197c7a032aa43e43113dbddff2f9e172dfe044c004206746bcb5f'

# Complete point structure: all16 histograms, all194 group descriptors and all
# 27 full bit vectors/weights are read, not inferred from the markdown tables.
assert set(point)=={'scope','rows','O','W','strict_half_gap','minimum_slack','K','histograms','groups','atoms'}
assert len(point['histograms'])==len(point['groups'])==16 and len(point['atoms'])==27
hists=[]; mass=defaultdict(Fraction); counts=Counter(); atoms=[]
for i,a in enumerate(point['atoms']):
    assert set(a)=={'hist_index','R','Z','weight'}
    hi=a['hist_index']; assert 0<=hi<16
    assert len(a['R'])==len(a['Z'])==len(point['groups'][hi])
    assert all(type(b)==int and b in (0,1) for b in a['R']+a['Z'])
    w=Fraction(a['weight']);assert w>0;mass[hi]+=w;counts[hi]+=1
    atoms.append({'index':i,'hist_index':hi,'R':''.join(map(str,a['R'])),'Z':''.join(map(str,a['Z'])),'weight':a['weight'],
                  'source_range':docs[POINT].span('/atoms/'+str(i))})
for hi,(h,groups) in enumerate(zip(point['histograms'],point['groups'])):
    assert set(h)=={'kind','actual_bits','d','hist'} and h['kind']=='hist'
    assert len(h['actual_bits'])==6 and set(h['actual_bits'])<=set('01')
    assert len(h['hist'])==8 and all(type(n)==int and n>=0 for n in h['hist']) and sum(h['hist'])==6
    words=[w for w,n in zip(product((0,1),repeat=3),h['hist']) for _ in range(n)]
    assert sum(w[0] for w in words)==h['d']==1
    expected=sorted({(f,int(i==j),words[i],words[j]) for f in (0,1) for i,j in product(range(6),repeat=2) if f or i!=j})
    actual=[(g[0],g[1],tuple(g[2]),tuple(g[3])) for g in groups];assert actual==expected
    hists.append({'index':hi,**h,'groups_count':len(groups),'complete_groups':groups,
                  'source_range':docs[POINT].span('/groups/'+str(hi)),
                  'positive_atoms':counts[hi],'mass':str(mass[hi])})
assert sum(map(len,point['groups']))==194
assert sum(counts[h]>0 for h in range(16))==10
for k in ['O','W','strict_half_gap','minimum_slack','K']: Fraction(point[k])
assert Fraction(point['O'])-2*Fraction(point['W'])==Fraction(point['strict_half_gap'])>0

# Every saved old descriptor and every saved value. Only compare stored
# representations; no RR aggregation and no old matrix generation are done.
assert len(old['columns'])==len(slack['all1905_values'])==1905
schema_families={}; bykind=defaultdict(list)
for i,c in enumerate(old['columns']):
    k=c['kind'];bykind[k].append(i);Fraction(c['weight'])
    assert c['weight']==slack['all1905_values'][i]
for k,indices in bykind.items():
    schema_families[k]={'count':len(indices),'index_runs_half_open':runs(indices),
      'descriptor_schemas':[{'keys':list(ks),'count':n} for ks,n in Counter(tuple(old['columns'][i]) for i in indices).items()],
      'positive':sum(Fraction(old['columns'][i]['weight'])>0 for i in indices),
      'all_descriptors_and_values_sha256':sha(enc([[i,old['columns'][i]] for i in indices]))}
assert {k:len(v) for k,v in bykind.items()}=={'K':1,'hist':16,'joint-reply':582,'overlap':1306}
assert sum(x['positive'] for x in schema_families.values())==527
hist_columns=bykind['hist']; old_ids={}
for hi,ci in enumerate(hist_columns):
    c=old['columns'][ci];assert {k:v for k,v in c.items() if k!='weight'}==point['histograms'][hi]
    assert Fraction(c['weight'])==mass[hi]
    gj=point['groups'][hi]; js=old['columns'][ci+1:ci+1+3*len(gj)]
    assert all(x['kind']=='joint-reply' for x in js)
    assert len({x['hist_column_old'] for x in js})==1
    old_ids[hi]=js[0]['hist_column_old']
    assert [(x['group'],x['state']) for x in js]==[(g,list(s)) for g in gj for s in [(0,1),(1,0),(1,1)]]
    os=[old['columns'][i] for i in bykind['overlap'] if old['columns'][i]['hist_column']==ci]
    assert [x['groups'] for x in os]==[[a,b] for a,b in combinations(gj,2)]

# Read every row-name (including embedded coefficient JSON/tuple descriptors),
# every rational slack and every runtime-input record. No coefficient is
# constructed and no saved slack is recomputed from a point.
assert len(slack['row_names'])==len(slack['all_slacks'])==3889
families=defaultdict(list); embedded_schemas=Counter(); named=[]
for i,(name,v) in enumerate(zip(slack['row_names'],slack['all_slacks'])):
    q=Fraction(v);assert q>=0
    if name.startswith('('):
        desc=ast.literal_eval(name);assert isinstance(desc,tuple);family=desc[0]
    else:
        family=name.split(':',1)[0]
        if family.startswith('old_'): family='old'
        if family.startswith('new_B_'):family='new_B'
        if family.startswith('new_C_'):family='new_C'
        if ':{' in name:
            inner=json.loads(name.split(':',1)[1]); embedded_schemas[tuple(inner)]+=1
            def rational_walk(x):
                if isinstance(x,dict):
                    for v in x.values():rational_walk(v)
                elif isinstance(x,list):
                    for v in x:rational_walk(v)
                elif isinstance(x,str) and re.fullmatch(r'-?\d+(?:/\d+)?',x):Fraction(x)
            rational_walk(inner)
    families[family].append(i); named.append((name,v))
row_families=[]
for family,indices in families.items():
    vals=[Fraction(slack['all_slacks'][i]) for i in indices]
    row_families.append({'family':family,'count':len(indices),'index_runs_half_open':runs(indices),
       'negative':sum(v<0 for v in vals),'zero':sum(v==0 for v in vals),'positive':sum(v>0 for v in vals),
       'minimum':str(min(vals)),'maximum':str(max(vals)),
       'all_index_name_exact_fraction_payload_sha256':sha(enc([[i,*named[i]] for i in indices]))})
isbound=lambda n:n.startswith(('joint-state-upper:','overlap-upper:'))
rawidx=[i for i,n in enumerate(slack['row_names']) if not isbound(n)]
boundidx=[i for i,n in enumerate(slack['row_names']) if isbound(n)]
assert len(rawidx)==slack['raw_rows']==1083 and len(boundidx)==slack['bound_rows']==2806
assert sum(Fraction(v)==0 for v in slack['all_slacks'])==slack['zero_slacks']==2329
assert sum(Fraction(v)>0 for v in slack['all_slacks'])==slack['positive_slacks']==1560
assert sum(Fraction(slack['all_slacks'][i])==0 for i in rawidx)==117
assert sum(Fraction(slack['all_slacks'][i])==0 for i in boundidx)==2212
assert slack['input_sha256']==sha(docs[SCHEMA].raw)
assert len(slack['runtime_inputs_read'])==26
for inp in slack['runtime_inputs_read']:
    assert set(inp)=={'path','size','sha256'} and inp['size']>=0 and re.fullmatch('[a-f0-9]{64}',inp['sha256'])

# Mature evidence contracts: complete stored reports, not a new 117612/810 loop.
z=docs[ZZ+'original/closure_independent_review.json'].data
zp=docs[ZZ+'replay/zz-prefix-review.json'].data
assert z['ZZ_rows']==zp['ZZ_rows'] and len(z['ZZ_rows'])==60
for row in z['ZZ_rows']: Fraction(row['value'])
zzcounts={'zero':sum(Fraction(x['value'])==0 for x in z['ZZ_rows']),
 'positive':sum(Fraction(x['value'])>0 for x in z['ZZ_rows']),
 'structurally_empty':sum(x['literal_label_pairs']==0 for x in z['ZZ_rows'])}
assert zzcounts=={'zero':24,'positive':36,'structurally_empty':18}
middle=docs[MID+'middle_transport_audit.json'].data
v1=docs[MID+'new_source_cut_audit.json'].data
assert middle['evaluations'][0]['sha256']==v1['source_sha256']==sha(docs[POINT].raw)
for e in middle['evaluations']:
    assert Fraction(e['lhs'])-Fraction(e['rhs'])==Fraction(e['slack'])<0
assert Fraction(v1['lhs'])-Fraction(v1['rhs'])==Fraction(v1['slack'])<0
assert v1['K']==point['K']

report={'artifact_kind':'complete-native-structure-and-saved-contract-reading',
 'claim':'Every primitive JSON token and complete array/object was consumed. Counts/signs compare saved values; no IC coefficient/phi/matrix was evaluated.',
 'files':[d.summary() for d in docs.values()],
 'point':{'all_histograms':hists,'all27_atoms':atoms,'scope':point['scope'],'rows':point['rows'],
          'O':point['O'],'W':point['W'],'K':point['K'],'strict_half_gap':point['strict_half_gap']},
 'old_schema':{'families':schema_families,'hist_current_columns':hist_columns,'hist_old_column_ids':old_ids,
       'all1905_saved_values_match':True,'descriptor_lineage_regeneration':False},
 'all_old_slacks':{'all3889_saved_rows_consumed':True,'raw_index_runs':runs(rawidx),'bound_index_runs':runs(boundidx),
       'families':row_families,'embedded_json_schemas':[{'keys':list(k),'count':v} for k,v in embedded_schemas.items()],
       'all26_saved_runtime_input_records':slack['runtime_inputs_read'],
       'counts':{'raw':1083,'bound':2806,'zeros':2329,'positive':1560,'raw_zeros':117,'bound_zeros':2212},
       'elapsed_seconds_in_return_locals':str(slack['elapsed_seconds']),
       'outer_event_elapsed_seconds':str(docs[BASE+'explicit-joint-rz-and-root-extension-primary/old3889-replay/event.json'].data['elapsed_seconds'])},
 'ZZ_saved_report_reuse':{'all60_records_equal':True,'counts':zzcounts,'all60_record_payload_sha256':sha(enc(z['ZZ_rows'])),
       'literal_terms_historical_only':117612,'old_matrix_prefix_executed':False},
 'middle_saved_report':middle,'v1_saved_report':v1,
 'execution_boundary':{'new_IC_row_evaluations':0,'phi_evaluations':0,'old3889_replay':0,'ZZ117612_replay':0,
       'original_scientific_entries':0,'LP_or_solver':0,'structural_parser_execution':1,
       'scope':'Fraction parsing, stored table signs, schema/index validation and saved lhs-rhs arithmetic only.'}}
(OUT/'structured-consumption.json').write_text(json.dumps(report,ensure_ascii=False,indent=2,default=str)+'\n')
print(json.dumps({'complete_files':len(docs),'primitive_leaves':sum(len(d.leaves) for d in docs.values()),
 'all_old_families':[{k:x[k] for k in ['family','count','zero','positive','index_runs_half_open']} for x in row_families],
 'schema':schema_families,'ZZ':zzcounts,'no_scientific_replay':True},ensure_ascii=False,indent=2))
