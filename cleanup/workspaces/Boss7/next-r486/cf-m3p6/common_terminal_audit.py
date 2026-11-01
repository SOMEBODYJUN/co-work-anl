"""Expand unit customers for the failed q-punisher lift; no SPE asserted."""
from fractions import Fraction as F
from collections import Counter
from pathlib import Path
import json

def run(t,k):
    q=t-1;topics={}
    for i in range(k):
        X={('X',i,j) for j in range(t)};Y={('Y',i,j) for j in range(t-1)}
        topics['C',i]=X;topics['A',i]=X|Y
        for l in range(q):topics['B',i,l]=X|{('b',l,j) for j in range(t-1)}
    for l in range(q):topics['D',l]={('b',l,j) for j in range(t-1)}|{('d',l,0)}
    def payoff(action,terminal):
        return sum((F(1,sum(x in topics[a] for a in terminal)) for x in topics[action]),F(0))
    def join(action,prefix):return payoff(action,prefix+[action])
    actual=[('C',i) for i in range(k)]+[('D',l) for l in range(q)]
    coverage=set().union(*(topics[a] for a in actual));opt=set().union(*(topics['A',i] for i in range(k)),*(topics['D',l] for l in range(q)))
    assert len(coverage)==t*(k+t-1) and len(opt)==len(coverage)+k*(t-1)
    lastactual=payoff(actual[-1],actual);lastopt=join(('A',0),actual[:-1])
    assert lastactual==t and lastopt==F(3*t,2)-1
    inequalities=[]
    for i in range(k):
        tail=[('B',i,l) for l in range(q)]
        branchA=[('C',h) for h in range(i)]+[('A',i)]+[('C',h) for h in range(i+1,k)]+tail
        l=q-1;branchB=[('C',h) for h in range(i)]+[('B',i,l)]+[('C',h) for h in range(i+1,k)]+[('A',i)]+[('B',i,j) for j in range(q) if j!=l]
        assert Counter(branchA)==Counter(branchB)
        last=payoff(('B',i,l),branchA);early=payoff(('B',i,l),branchB)
        assert last==early==t
        for h in range(k):
            if h==i:continue
            alternative=join(('A',h),branchA[:-1]);assert alternative==F(3*t,2)-1
            inequalities.append({'i':i,'h':h,'last_B':str(last),'early_B_same_terminal':str(early),'last_deviation_A_h':str(alternative),'slack':str(last-alternative)})
    return {'t':t,'q':q,'k':k,'m':k+q,'unit_customers':len(opt),'actual_W':len(coverage),'intended_OPT':len(opt),'actual_last':str(lastactual),'actual_last_A_deviation':str(lastopt),'is_intended_last_BestReply':lastactual>=lastopt,'common_terminal_comparisons':inequalities}
if __name__=='__main__':
    load_checks=0
    for alpha in [F(0),F(1,4),F(1,2),F(1)]:
        for actual_load in range(1,9):
            for branch_load in range(17):
                if alpha*(1+branch_load)<=actual_load:
                    assert F(1,1+branch_load)>=alpha/actual_load
                    load_checks+=1
    report={'scope':'exact local obstruction arithmetic; no complete SPE claim','load_distortion_scalar_checks':load_checks,'cases':[run(t,k) for t in range(2,9) for k in [2,3]]}
    out=Path(__file__).with_name('common_terminal_audit.json');out.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'cases':len(report['cases']),'all_t_above_two_fail_last':all(not r['is_intended_last_BestReply'] for r in report['cases'] if r['t']>2),'output':str(out)}))
