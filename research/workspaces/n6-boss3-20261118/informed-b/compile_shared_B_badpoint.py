"""Compile the fixed shared-B necessary-LP point into an original unit-client menu.
Rational checks certify only its stated necessary rows. True subtree SPE is
checked separately by exact_tail.py; a missing IC will not be hidden.
"""
from fractions import Fraction as F
from pathlib import Path
import json,itertools
import importlib.util

BASE=Path(__file__).parent

def compile_point():
    bad=json.loads((BASE/'probe-shared-B-fullprefix-all-output.json').read_text())['best']
    masses=[(a['block'],tuple(a['bits']),F(a['mass']).limit_denominator(1000000)) for a in bad['atoms']]
    assert all((m*68).denominator==1 for _,_,m in masses)
    clients=[]
    covers=[set() for _ in range(11)]
    for block,bits,mass in masses:
        for _ in range(int(mass*68)):
            x=len(clients);clients.append((block,bits))
            if block<6:covers[block].add(x)
            for k,v in enumerate(bits):
                if v:covers[6+k].add(x)
    assert len(clients)==408
    assert all(len(a)==68 for a in covers)
    assert len(set(map(frozenset,covers)))==11
    labels=[{'name':('T'+str(a)) if a<6 else 'E' if a==6 else 'F'+str(a-7),'clients':sorted(v)} for a,v in enumerate(covers)]
    data={'clients':len(clients),'K':68,'labels':labels,'prefix_labels':['T4','T5','E'],'prefix_counts':[0,0,0,0,1,1,1,0,0,0,0]}
    (BASE/'shared-B-67-136-original-input.json').write_text(json.dumps(data,indent=2)+'\n')
    def payoff(history,a):
        loads=[sum(x in covers[b] for b in history) for x in range(len(clients))]
        return sum((F(1,loads[x]) for x in covers[a]),F())
    h=[4,5,6]; rows=[]
    for j,(a,y) in enumerate(bad['pattern']):
        a+=7;y+=7;leaf=h+[j,a,y]
        actual=payoff(leaf,a);last=payoff(leaf,y);forced=payoff(leaf,j)
        last_values=[payoff(h+[j,a,b],b) for b in range(11)]
        assert last==max(last_values)
        devs=[]
        for k in range(11):
            vals=[payoff(h+[j,k,b],b) for b in range(11)]
            mx=max(vals);br=[b for b,v in enumerate(vals) if v==mx]
            minown=min(payoff(h+[j,k,b],k) for b in br)
            maxown=max(payoff(h+[j,k,b],k) for b in br)
            devs.append({'action':labels[k]['name'],'last_BRs':[labels[b]['name'] for b in br],
                'current_min_payoff':str(minown),'current_max_payoff':str(maxown),
                'strictly_profitable_for_every_last_BR':minown>actual})
        W=len(set().union(*(covers[b] for b in leaf)))
        rows.append({'forced_anchor':j,'candidate_pair':[labels[a]['name'],labels[y]['name']],
                     'forced_payoff':str(forced),'forced_payoff_over_K':str(forced/68),
                     'penultimate_payoff':str(actual),'last_payoff':str(last),
                     'last_is_true_best_reply':True,'candidate_leaf_W':W,'candidate_leaf_OPT6':408,
                     'candidate_leaf_2W_minus_OPT6':2*W-408,'penultimate_deviations':devs})
    (BASE/'shared-B-67-136-exact-completion-check.json').write_text(json.dumps({'K':68,'clients':408,'q':5,'rows':rows,'scope':'Exact original menu completion of a necessary-relaxation point; candidate leaf and last BR are checked, all penultimate deviations enumerated; not assumed SPE.'},indent=2)+'\n')
    return rows

if __name__=='__main__':
    rows=compile_point()
    print(json.dumps([{'forced_anchor':r['forced_anchor'],'forced_payoff_over_K':r['forced_payoff_over_K'],'penultimate_payoff':r['penultimate_payoff'],'profitable_deviations':[d for d in r['penultimate_deviations'] if d['strictly_profitable_for_every_last_BR']],'W':r['candidate_leaf_W']} for r in rows],indent=2))
