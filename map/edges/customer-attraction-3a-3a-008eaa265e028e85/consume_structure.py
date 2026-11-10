"""Lossless schema/family reading, not a replay of the mathematical audits.

Read every native matrix cell and every named finite-record field.  Preserve
their source positions and exact scalar values in family blocks.  Decode and
compare with each complete native JSON.  No BR enumeration, row coefficient
generation, LP, atom construction or equilibrium search is performed here.
"""
from pathlib import Path
from collections import Counter, defaultdict
from fractions import Fraction
import hashlib
import json

BASE = Path('/workspace/scratch/bbb425bb840f/co-work-anl-boss6')
OUT = Path(__file__).resolve().parent
E = 'archives/customer-attraction/tools/evidence/'
SOURCE = {
    'kernel': E+'full156-tail-parent-report/original/research_5/full156_tail2_kernel_10344.json',
    'welfare': E+'full156-tail-parent-report/original/research_5/full156_tail2_welfare_10344.json',
    'combined': E+'full156-tail-parent-report/original/research_5/combined_branch_master_exact.json',
    'pair': E+'full156-pair-master-point/original/pair_master_exact.json',
    'slacks': E+'pair-threshold-closure-program/all-row-slacks.json',
}
EXPECTED = {
    'kernel': '876f063e9e88679c8803011775b04a4b707b8b586dfd3a840fd056f9ddcef3d4',
    'welfare': 'fe8fb09f7527f8f4cd26ad67f6e43be5bc84cb5d9c47fea39fd0661bab0e5256',
    'combined': 'd1aeba67e20c8d8fc7ff38cd6566ac05c3771731f586584e5c6f1dfe233472a8',
    'pair': '090586fb86af4e80b33eb24893d72fa2d240d156d639bcb97a9f8b413eddb2d2',
    'slacks': '58c27a27d36dfb83f35143483b9298c0eb38897511bfe7fc05bd308498a9df30',
}

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def save(name, obj):
    (OUT/name).write_text(json.dumps(obj, ensure_ascii=False, separators=(',', ':'))+'\n')

native, refs = {}, []
for role, path in SOURCE.items():
    raw = (BASE/path).read_bytes()
    assert sha(raw) == EXPECTED[role]
    native[role] = json.loads(raw)
    refs.append({'role': role, 'path': path, 'sha256': sha(raw), 'bytes': len(raw)})

families = {}
for i, desc in enumerate(native['kernel']['original_descriptors']):
    family = desc[0] if len(desc) == 2 else f'{desc[0]}{desc[1]}'
    families.setdefault(family, []).append(i)
assert {k:len(v) for k,v in families.items()} == {'A':6,'T':6,'B':6,'C':6,'R0':30,'R1':36,'Z0':30,'Z1':36}

structured = {'schema':1, 'method':'exact scalar palette and all family blocks; all native fields retained',
              'source_refs': refs, 'families': families, 'matrices': {}, 'records': {}}
matrix_summary = {}
for role, fields in [('kernel',['F_numerators','G_numerators','payoff_numerators']),('welfare',['welfare_numerators'])]:
    obj = native[role]
    record = {'original_key_order':list(obj), 'metadata':{k:v for k,v in obj.items() if k not in fields}, 'fields':{}}
    rebuilt = dict(record['metadata'])
    matrix_summary[role] = {'all_top_level_fields':list(obj), 'fields':{}}
    for field in fields:
        data = obj[field]
        vector = field == 'F_numerators'
        flat = data if vector else [v for row in data for v in row]
        assert len(data)==156 and (vector or all(len(row)==156 for row in data))
        assert all(isinstance(v,str) and str(int(v))==v for v in flat)
        palette = list(dict.fromkeys(flat))
        index = {v:i for i,v in enumerate(palette)}
        blocks = {}
        coverage = set()
        for a, ai in families.items():
            if vector:
                blocks[a] = [index[data[i]] for i in ai]
                coverage.update(ai)
            else:
                for b, bi in families.items():
                    blocks[a+'/'+b] = [[index[data[i][j]] for j in bi] for i in ai]
                    coverage.update((i,j) for i in ai for j in bi)
        assert len(coverage)==len(flat)
        decoded = [None]*156 if vector else [[None]*156 for _ in range(156)]
        for a, ai in families.items():
            if vector:
                for k,i in enumerate(ai): decoded[i]=palette[blocks[a][k]]
            else:
                for b,bi in families.items():
                    for k,i in enumerate(ai):
                        for l,j in enumerate(bi): decoded[i][j]=palette[blocks[a+'/'+b][k][l]]
        assert decoded==data
        record['fields'][field]={'scalar_type':'native decimal integer string','palette':palette,'blocks':blocks}
        rebuilt[field]=decoded
        matrix_summary[role]['fields'][field]={'consumed_scalars':len(flat),'exact_palette_values':len(palette),
            'family_blocks':{k:len(v) if vector else [len(v),len(v[0])] for k,v in blocks.items()},
            'normalization':'Q=60S' if role=='kernel' else 'S', 'decoded_all_values_equal_native':True}
    rebuilt={k:rebuilt[k] for k in obj}
    assert rebuilt==obj
    assert (json.dumps(rebuilt,indent=2)+'\n').encode()==(BASE/SOURCE[role]).read_bytes()
    record['decoded_native_bytes_equal']=True
    structured['matrices'][role]=record

# Group every complete combined column by kind and current histogram, retaining
# original array offsets.  No coordinate is treated as a new mathematical node.
combined=native['combined']
grouped=defaultdict(list)
current=None
histmap={}
for i,col in enumerate(combined['columns']):
    Fraction(col['weight'])  # exact scalar parse; does not evaluate necessary rows
    if col['kind']=='hist':current=i
    owner=current if col['kind']=='joint-reply' else col.get('hist_column')
    grouped[(col['kind'], owner)].append({'position':i,'native_record':col})
    if col['kind']=='joint-reply':histmap[col['hist_column_old']]=current
groups=[{'kind':kind,'current_hist_column':owner,'records':rows} for (kind,owner),rows in grouped.items()]
decoded=[None]*len(combined['columns'])
for group in groups:
    for row in group['records']:
        assert decoded[row['position']] is None
        decoded[row['position']]=row['native_record']
assert decoded==combined['columns']
structured['records']['combined']={'metadata':{k:v for k,v in combined.items() if k!='columns'},
    'original_key_order':list(combined),'groups':groups,'legacy_to_current_hist':list(histmap.items()),
    'decode_equals_all_native_columns':True}

pair=native['pair'];pg=defaultdict(list)
for i,row in enumerate(pair['variables']):
    assert set(row)=={'hist_column','left','right','group','r','weight'}
    for key in ('left','right','weight'): Fraction(row[key])
    assert row['r'] in (0,1)
    pg[(row['hist_column'],row['left'],row['right'])].append({'position':i,'native_record':row})
pairgroups=[{'hist_column':h,'left':left,'right':right,'records':rows} for (h,left,right),rows in pg.items()]
decoded=[None]*len(pair['variables'])
for group in pairgroups:
    for row in group['records']:decoded[row['position']]=row['native_record']
assert decoded==pair['variables']
structured['records']['pair']={'metadata':{k:v for k,v in pair.items() if k!='variables'},
    'original_key_order':list(pair),'layers':pairgroups,'decode_equals_all_native_variables':True}

run=json.loads((BASE/(E+'pair-threshold-closure-program/run-report.json')).read_text())
slacks=native['slacks'];sections=[]
for name,part in run['row_sections'].items():
    rows=slacks[part['begin_inclusive']:part['end_exclusive']]
    assert len(rows)==part['rows']
    for row in rows:
        assert set(row)=={'index','name','slack'}
        Fraction(row['slack'])
    sections.append({'family':name,'contract':part,'native_records':rows})
assert [row for section in sections for row in section['native_records']]==slacks
assert [row['index'] for row in slacks]==list(range(10344))
structured['records']['slacks']={'sections':sections,'all_native_names_and_exact_slacks_preserved':True,
    'new_row_generation':False,'new_slack_evaluation':False}

# Complete small/current audit records: preserve every field and every row,
# including reported row fingerprints, BR tie labels, and provenance metadata.
AUDITS=[
 'full156-tail-parent-report/original/audit_full156_reply_set.json',
 'full156-tail-parent-report/field-audit.json',
 'full156-author-tail-report/original/full156_tail2_exact_audit.json',
 'full156-author-tail-report/replay/field-audit.json',
 'full156-author-tail-report/replay/all-156-BR-rows.json',
 'full156-tail-minimum-author-summary/original/full156_tail2_min_welfare.json',
 'full156-payoff-kernel-data/independent-report.json',
 'full156-welfare-kernel-data/welfare-audit.json',
 'full156-kernel-generator/input-contract.json',
 'full156-kernel-generator/rerun/execution.json',
 'full156-kernel-generator/rerun/comparison.json',
 'full156-tail-parent-auditor/rerun/execution.json',
 'full156-author-tail-auditor/rerun/execution.json',
 'full156-pair-master-point/current-added-row-audit.json',
 'pair-threshold-closure-program/run-report.json',
 'combined-branch-master-point/current-point-audit.json',
 'combined-branch-master-program/rerun/execution.json',
]
audit_records=[]
for relative in AUDITS:
    raw=(BASE/(E+relative)).read_bytes();obj=json.loads(raw)
    # Round-trip all fields/records, retaining key order and exact string values.
    assert json.loads(json.dumps(obj,ensure_ascii=False))==obj
    audit_records.append({'path':E+relative,'sha256':sha(raw),'bytes':len(raw),'native_record':obj})
structured['mature_audits']=audit_records
save('structured-native-reading.json',structured)

summary={'status':'complete-lossless-structural-consumption; mathematical-audits-reused-not-replayed',
    'matrix_reading':matrix_summary,
    'combined':{'all_fields':list(combined),'all_columns':len(combined['columns']),
        'kinds':dict(Counter(c['kind'] for c in combined['columns'])),
        'column_fields_by_kind':{k:sorted({f for c in combined['columns'] if c['kind']==k for f in c}) for k in ['K','hist','joint-reply','overlap']},
        'groups':len(groups),'all_positions_retained':True,'legacy_to_current_hist':list(histmap.items()),
        'semantic_scope':'hist/current blocks plus complete old R/Z and overlap coordinates structurally consumed; old 5108 row mathematics reused only from exact event'},
    'pair':{'all_fields':list(pair),'variables':len(pair['variables']),'all_six_fields':True,'layers':len(pairgroups),
        'layer_variable_counts':[{'hist_column':p['hist_column'],'left':p['left'],'right':p['right'],'records':len(p['records'])} for p in pairgroups],
        'semantic_scope':'left/right/weight are mass; r is a fixed R bit; diag is named-index equality; new Z does not preserve all old Z/RZ margins'},
    'slacks':{'records':len(slacks),'all_index_name_slack_fields_consumed':True,
        'family_ranges':run['row_sections'],'semantic_scope':'all preserved mature exact results; not new coefficients or original verification'},
    'mature_audits':[{'path':r['path'],'sha256':r['sha256'],'bytes':r['bytes'],
        'top_level_fields':list(r['native_record']) if isinstance(r['native_record'],dict) else None,
        'records':len(r['native_record']) if isinstance(r['native_record'],list) else None} for r in audit_records],
    'scientific_replays_this_script':0,'LP_calls':0,'BR_enumerations':0,'matrix_generations':0,
    'new_checks':['source byte identities','exact scalar parsing','schema and indexing consumption','lossless encode/decode equality including all native cells/records','byte round-trip for both complete matrices'],
    'not_claimed':['new 5108/10344 row certification','new 156 squared BR classification','new integer-customer reconstruction','new complete six-player strategy check']}
save('structure-consumption-report.json',summary)
print(json.dumps({'status':summary['status'],'matrix_scalars':156+3*156*156,
    'combined_columns':1905,'pair_variables':364,'slack_records':10344,
    'mature_audits':len(audit_records),'output_bytes':(OUT/'structured-native-reading.json').stat().st_size},ensure_ascii=False))
