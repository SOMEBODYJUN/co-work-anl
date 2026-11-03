"""Exact, optimizer-free dual audit for the universal-punisher lifting exclusion."""
from universal_punisher import extra, HERE, F, json

MULTIPLIERS={
 0:{'last_BR_other_T':F(4,5),'T0_penultimate_IC':F(1,5)},
 1:{'last_BR_other_T':F(4,5),'T0_penultimate_IC':F(1,5)},
 2:{'last_BR_other_T':F(4,5),'T0_penultimate_IC':F(1,5)},
 3:{'last_BR_other_T':F(4,5),'T0_penultimate_IC':F(1,5)},
 4:{'last_BR_other_T':F(2,7),'T0_penultimate_IC':F(2,7),'fixeddev_6_replyT0_BR_fixed':F(3,14),'fixeddev_6_penultimate_IC':F(3,14)},
 5:{'last_BR_other_T':F(2,7),'T0_penultimate_IC':F(2,7),'fixeddev_6_replyT0_BR_fixed':F(3,14),'fixeddev_6_penultimate_IC':F(3,14)},
 6:{'last_BR_other_T':F(1,2),'T0_penultimate_IC':F(1,8),'fixeddev_6_penultimate_IC':F(3,8)},
 7:{'T0_penultimate_IC':F(1,2),'fixeddev_7_replyT0_BR_fixed':F(1,2)},
 8:{'last_BR_other_T':F(1,2),'T0_penultimate_IC':F(1,8),'fixeddev_8_penultimate_IC':F(3,8)},
 9:{'T0_penultimate_IC':F(1,2),'fixeddev_9_replyT0_BR_fixed':F(1,2)},
 10:{'T0_path_floor_1':F(5,16),'T0_path_floor_4':F(1,4),'last_BR_other_T':F(7,16)},
}

def main():
 report=[]
 for last,multipliers in MULTIPLIERS.items():
  atoms,r,bits,u,G,rows,rhs,names,own=extra(last)
  assert sum(multipliers.values())==1 and min(multipliers.values())>0
  aa=[sum(mu*rows[names.index(name)][j] for name,mu in multipliers.items()) for j in range(len(atoms))]
  bb=sum(mu*rhs[names.index(name)] for name,mu in multipliers.items())
  # For x in [0,1]^64, a*x >= sum min(0,a_j).
  lower=sum(min(F(0),v) for v in aa)-bb
  assert lower>0,(last,lower)
  report.append({'last_reply':('ABCDEUVWXY'[last] if last<10 else 'T0'),'multipliers':{n:str(mu) for n,mu in multipliers.items()},'minimum_common_violation_at_least':str(lower),'minimum_common_violation_decimal':float(lower),'linear_coefficients':[str(v) for v in aa],'weighted_rhs':str(bb)})
  print(report[-1]['last_reply'],float(lower),flush=True)
 # If the last reply after T0 is a different T, T0 keeps its entire
 # ABC-residual payoff. Its own last BR after fixed deviation V implies
 # that residual is at least the fixed reply W's utility after ABCV.
 atoms,r,bits,u,G,*_=extra(6)
 fixed_W_after_V=sum(rr*F(b[7],sum(b[j] for j in (0,1,2,6))+1) for rr,b in zip(r,bits))
 other_margin=fixed_W_after_V-u[3];assert other_margin>0
 out={'status':'exact exclusion of one universal-T last-punisher lift of the old 64-atom mass point; not a half theorem or general alignment exclusion','fixed_bad_deviations':['E','V','W','X','Y'],'single_shared_reply':'T0','fixed_last_reply_certificates':report,'other_T_last_reply_margin':str(other_margin),'other_T_last_reply_margin_decimal':float(other_margin)}
 (HERE/'universal_punisher_exact.json').write_text(json.dumps(out,indent=2)+'\n')
if __name__=='__main__':main()
