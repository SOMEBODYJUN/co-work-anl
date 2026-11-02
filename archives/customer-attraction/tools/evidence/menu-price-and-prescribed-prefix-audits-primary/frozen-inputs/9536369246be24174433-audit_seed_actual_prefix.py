"""Locate exact failure of a proposed actual path in a targeted finite game.

All comparison thresholds use the full SPE continuation set, not an arbitrary
selector or a local relaxation. These are finite-instance obstruction witnesses.
"""
from bigint_controller_attack import Attack,ExactPayoffs,solve,HERE
from fractions import Fraction as F
from pathlib import Path
import argparse,json,numpy as np,time
p=argparse.ArgumentParser();p.add_argument('input');p.add_argument('prefix');a=p.parse_args();start=time.time();source=HERE/a.input;seed=json.loads(source.read_text());C=Attack(seed);w=[q['multiplicity'] for q in seed['customers']];P=ExactPayoffs(C,w);out,mins,floor=solve(C,P)
path=tuple(range(6));target=tuple([1]*6+[0]*(C.k-6));t=C.levels[6].index(target);total=sum(w);checks=[]
for depth in range(6):
 q=tuple(int(j<depth) for j in range(C.k));qi=C.levels[depth].index(q);ft,fa=floor[depth][qi];target_in=bool(t in out[depth][qi]);current=path[depth];u=P.val(t,current);v=P.val(ft,fa);children=C.child[depth][qi];child=int(children[current]);next_in=bool(t in out[depth+1][child]);rec={'depth':depth,'current_actual_label':seed['topics'][current],'actual_terminal_retained_here':target_in,'actual_terminal_retained_after_actual_action':next_in,'actual_player_u_over_total':str(F(u,60*total)),'best_security_action_label':seed['topics'][fa],'SPE_security_floor_over_total':str(F(v,60*total)),'strict_floor_gap_over_total':str(F(v-u,60*total)),'floor_minimizing_terminal_counts':C.term[ft].tolist()};checks.append(rec);print(json.dumps(rec),flush=True)
report={'status':'exact full-SPE continuation threshold check for one finite input','input':a.input,'old_actual_path':list(path),'old_actual_counts':target,'old_actual_welfare_over_total':str(F(sum(v for v,c in zip(w,C.cover[t]) if c),total)),'checks':checks,'seconds':time.time()-start};(HERE/(a.prefix+'_actual_prefix_audit.json')).write_text(json.dumps(report,indent=2)+'\n')
