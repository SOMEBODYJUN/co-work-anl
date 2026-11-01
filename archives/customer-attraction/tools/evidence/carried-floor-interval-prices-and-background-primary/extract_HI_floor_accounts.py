"""New narrow postcheck: G29/floor path account and C5 packet decoding.

No true-SPE BI, full-policy IC, original imports, optimizer, or discovery.
The original price verifier checks all price/primal rows but does not compute
G_I; this fills that precise finite-output gap from the literal input.
"""
from pathlib import Path
from fractions import Fraction as F
from functools import lru_cache
from collections import Counter
import json,sys
HERE=Path(__file__).resolve().parent
def read(p):return json.loads(p.read_text())
def raw(name):
 rows=read(HERE/'related-source-reading-and-entry-plan.json')['files']
 r=next(a for a in rows if Path(a['source']['path']).name==name)
 stage=HERE.parents[4];return stage/r['raw_target']
candidate=read(raw('interval_price_strict_candidate.json'));ins=candidate['instance'];p=len(ins['topics']);m=ins['players'];types=[(frozenset(c['topics']),c['multiplicity']) for c in ins['customers']];zero=(0,)*p
def add(b,a):return b[:a]+(b[a]+1,)+b[a+1:]
@lru_cache(None)
def U(q):return tuple(sum((F(w,sum(q[j] for j in B)) for B,w in types if a in B),F()) if q[a] else F() for a in range(p))
floors={};allowed={}
@lru_cache(None)
def HI(b):
 if sum(b)==m:return frozenset((b,))
 children=[HI(add(b,a)) for a in range(p)];level=max(min(U(q)[a] for q in children[a]) for a in range(p));eligible=tuple(a for a in range(p) if max(U(q)[a] for q in children[a])>=level);floors[b]=level;allowed[b]=eligible
 return frozenset(q for a in eligible for q in children[a])
@lru_cache(None)
def G(b):
 if sum(b)==m:return F()
 HI(b);return floors[b]+min(G(add(b,a)) for a in allowed[b])
H=HI(zero);paths=[]
def walk(b,path,levs):
 if sum(b)==m:paths.append({'actions':path,'q':b,'floors':list(map(str,levs)),'sum_floors':str(sum(levs,F()))});return
 for a in allowed[b]:walk(add(b,a),path+[a],levs+[floors[b]])
walk(zero,[],[])
minimum=min(F(a['sum_floors']) for a in paths);assert minimum==G(zero)==F(candidate['G_I'])==F(80,3)
assert len(paths)==candidate['path_count']==57 and len({(tuple(a['actions'][:i].count(j) for j in range(p)),a['actions'][i]) for a in paths for i in range(m)})==candidate['edge_count']==50
W=lambda q:sum(w for B,w in types if any(q[a] for a in B))
assert min(map(W,H))==int(candidate['minimum_HI_terminal_W'])==25 and len(H)==7
packet=read(raw('interval_extra_one_c5_packet.json'));nodes={tuple(r['prefix']):r for r in packet['interval_witness_records']};M=6;P=5
@lru_cache(None)
def decode(b):
 if sum(b)==M:return frozenset((b,))
 return frozenset(q for a in nodes[b]['allowed'] for q in decode(add(b,a)))
assert sorted(decode((0,)*P))==[tuple(q) for q in packet['root_interval_terminal_counts']]
child=decode((1,0,0,0,0));values=[(q,F(1,q[4]+q[0])+F(1,q[0]+q[1])) for q in sorted(child)];hist=Counter(v for q,v in values)
assert len(child)==23 and {str(k):v for k,v in hist.items()}=={'1/2':2,'7/12':4,'2/3':7,'5/6':8,'1':2}
assert len(sys.argv)==2;out=Path(sys.argv[1]);assert not out.exists(),'one actual new postcheck only'
obj={'identity':'new narrow HI floor-account completion, not either original audit','price29':{'HI_terminal_counts':sorted(map(list,H)),'HI_state_count_by_actual_new_cache':HI.cache_info().currsize,'nonterminal_floor_states':len(floors),'allowed_paths':paths,'path_count':len(paths),'edge_count':50,'G_I':str(G(zero)),'minimum_HI_W':25,'G_source_candidate_value_confirmed':True,'true_SPE_or_price_constraints_rechecked':False},'C5_packet_only_decoding':{'child_e0_terminal_counts_and_U0':[{'q':q,'U0':str(v)} for q,v in values],'child_e0_count':23,'U0_histogram':{str(k):hist[k] for k in sorted(hist)},'decoded_root_terminal_counts_match_original_packet':True,'no_new_true_SPE_BI_or_ordered_policy_IC':True},'original_entries':0,'new_narrow_deterministic_entries':1,'old69_or_NI3025_entries':0}
out.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'status':'PASS','G29':'80/3','paths29':57,'HIstates29':HI.cache_info().currsize,'C5_packet_e0_decoded':23,'new_true_BI_or_policy_audit':0}))
