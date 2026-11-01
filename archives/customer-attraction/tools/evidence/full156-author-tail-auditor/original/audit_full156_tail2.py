"""Exact complete r=2 SPE check of one threshold-materialized full catalogue."""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib
HERE=Path(__file__).resolve().parent
source=HERE.parent/'research_5/full156_tail2_kernel_10344.json';raw=source.read_bytes();d=json.loads(raw);labels=d['topics'];U=[[int(x) for x in row] for row in d['payoff_numerators']];D=int(d['payoff_denominator_for_normalized_point']);n=len(labels);a,b=d['actual_last_pair']
BR=[];floors=[];minBR=[]
for i in range(n):
 val=max(U[j][i] for j in range(n));bs=[j for j in range(n) if U[j][i]==val];BR.append(bs);v=min(U[i][j] for j in bs);floors.append(v);minBR.append([j for j in bs if U[i][j]==v])
M=max(floors);queries=[i for i,v in enumerate(floors) if v==M];gap=M-U[a][b];oldhalf=1-2*F(d['source_W']);actualBR=b in BR[a];repair_stop=gap>0 and 3*F(gap,D)>=oldhalf
report={'status':'one finite full-catalog r2 exact audit, not an inherited full six-player SPE','source_sha256':hashlib.sha256(raw).hexdigest(),'topic_count':n,'fixed_prefix_labels':[labels[i] for i in d['fixed_prefix']],'target_last_pair_labels':[labels[a],labels[b]],'actual_last_is_BR':actualBR,'actual_penultimate_u':str(F(U[a][b],D)),'actual_last_u':str(F(U[b][a],D)),'actual_last_BR_labels':[labels[i] for i in BR[a]],'max_min_credible_floor':str(F(M,D)),'penultimate_deficit':str(max(F(0),F(gap,D))),'strict_deficit':gap>0,'best_security_queries':[{'action':labels[i],'all_BR_labels':[labels[j] for j in BR[i]],'minimizing_BR_labels':[labels[j] for j in minBR[i]],'guaranteed_u':str(F(floors[i],D))} for i in queries],'target_tail_is_full_SPE':actualBR and U[a][b]>=M,'old_half_gap':str(oldhalf),'three_times_penultimate_deficit':str(3*max(F(0),F(gap,D))),'heterogeneous_repair_fixed_target_blocked_already_by_last_deficit':repair_stop,'unit_customer_scale':d['unit_customer_scale'],'payoff_common_denominator':str(D)}
(HERE/'full156_tail2_exact_audit.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
