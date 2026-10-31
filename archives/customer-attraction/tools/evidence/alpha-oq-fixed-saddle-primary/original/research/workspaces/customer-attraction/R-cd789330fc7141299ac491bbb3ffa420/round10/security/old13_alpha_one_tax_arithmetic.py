"""Exact arithmetic on the one already-loaded old13 refined-tax packet.
No LP, no solver, no search or new instance. Full SPE status is inherited from
its existing complete automaton audits, not re-established by this scalar read.
"""
from pathlib import Path
from fractions import Fraction as R
import gzip,json,hashlib
ROOT=Path(__file__).resolve().parents[6]
OUT=Path(__file__).resolve().parent
PATH=ROOT/'research/workspaces/customer-attraction/R-c50fecc37aa44fb4a69a2122bb70e5fe/security/refined_tax_k10_packet.json.gz'
raw=PATH.read_bytes();d=json.loads(gzip.decompress(raw));I=d['instance'];m=I['players'];nodes=d['nodes'];k=len(I['topics']);j=d['root'];actual=[]
while not nodes[j].get('terminal'):
 q=nodes[j];a=q['action'];actual.append(a);j=q['children'][a]
c=tuple(nodes[j]['counts']);assert c==tuple(actual.count(a)for a in range(k))==(2,1,0,0,0,10)
types=[(tuple(q['topics']),q['multiplicity'])for q in I['customers']]
loads=[sum(c[a]for a in S)for S,w in types]
W=sum(w for (S,w),h in zip(types,loads)if h>0)
J=sum((R(w,h+1)for (S,w),h in zip(types,loads)if h>0),R())
g=[sum((R(w,h+1)for (S,w),h in zip(types,loads)if a in S),R())for a in range(k)]
F=[sum(((R((m+1)*w,h+1)if h>0 else R(m*w))for (S,w),h in zip(types,loads)if a in S),R())for a in range(k)]
# Exact frozen common-query identity F(T)=sum_i f_i(T).
frozen_sum=[]
for a in range(k):
 total=R()
 for z in actual:
  total+=sum((R(w,h-int(z in S)+1)for (S,w),h in zip(types,loads)if a in S),R())
 frozen_sum.append(total)
assert F==frozen_sum
assert (m,W,J)==(13,33,R(359,66))
assert g==[R(5,3),R(3,2),R(3),R(5,2),R(5,2),R(25,11)]
assert F==[R(70,3),R(21),R(39),R(34),R(34),R(350,11)]
assert m*max(g)-W-J==max(F)-W-J==R(37,66)>0
r={'scope':'Exact scalar implication of an already audited complete old13 SPE; no new instance, LP or search. Both specified sufficient bridges are false.','source':str(PATH.relative_to(ROOT)),'source_sha256':hashlib.sha256(raw).hexdigest(),'m':m,'actual':actual,'counts':c,'W':W,'unit_customers':sum(w for S,w in types),'J_base':str(J),'g':[str(x)for x in g],'F_common_frozen_sum':[str(x)for x in F],'m_max_g_minus_W_minus_J':str(m*max(g)-W-J),'max_F_minus_W_minus_J':str(max(F)-W-J),'maximizing_topic_for_both':2,'maximizing_topic_label':I['topics'][2],'same_query_is_entirely_uncovered':all(h==0 for (S,w),h in zip(types,loads)if 2 in S)}
(OUT/'old13_alpha_one_tax_arithmetic.json').write_text(json.dumps(r,indent=2)+'\n')
print(json.dumps(r,indent=2))
