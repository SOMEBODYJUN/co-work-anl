#!/usr/bin/env python3
"""Fraction audit of one strict-greedy boxed lexmax selector obstruction."""
from fractions import Fraction as F
from itertools import product

S = 'HMNLR'
clients = [('PH',446,'H'),('PM',230,'M'),('PN',189,'N'),('PL',159,'L'),('PR',100,'R'),('X',46,'HM'),('x',2,'HM'),('Y',82,'MN'),('y',81,'MN'),('Z',4,'NL'),('z',30,'NL')]
q = dict.fromkeys(S,0)
w0 = dict.fromkeys(S,0)
origin = {}
trace = []
for _ in range(11):
    scores = {s:F(w0[s],q[s]+1) if q[s] else F(sum(w for name,w,opts in clients if name not in origin and s in opts)) for s in S}
    maximum=max(scores.values())
    winner=[s for s in S if scores[s]==maximum]
    assert len(winner)==1
    s=winner[0]
    trace.append((s,maximum))
    if q[s]==0:
        for name,w,opts in clients:
            if name not in origin and s in opts:
                origin[name]=s
                w0[s]+=w
    q[s]+=1
assert trace==list(zip('HMHNMHLMHNR',map(F,(494,393,247,223,F(393,2),F(494,3),159,131,F(247,2),F(223,2),100))))
assert tuple(q.values())==(4,3,2,1,1) and tuple(w0.values())==(494,393,223,159,100)
boxed=[]
for choices in product((0,1),repeat=6):
    totals=dict(zip(S,(446,230,189,159,100)))
    assignment={}
    for (name,w,opts),bit in zip(clients[5:],choices):
        s=opts[bit]
        assignment[name]=s
        totals[s]+=w
    if any(not q[s]*100<=totals[s]<=(q[s]+1)*100 for s in S):continue
    lex=tuple(sorted(F(totals[s],q[s]) for s in S for _ in range(q[s])))
    deviations=tuple((name,s,t,F(totals[s]-w,q[s]),F(totals[t],q[t])) for name,w,opts in clients[5:] for s in [assignment[name]] for t in opts if t!=s and F(totals[s]-w,q[s])>F(totals[t],q[t]))
    boxed.append((assignment,totals,lex,deviations))
assert len(boxed)==24
maximum=max(row[2] for row in boxed)
winners=[row for row in boxed if row[2]==maximum]
assert len(winners)==1
assignment,totals,lex,deviations=winners[0]
assert assignment=={'X':'M','x':'H','Y':'M','y':'N','Z':'L','z':'N'}
assert tuple(totals.values())==(448,358,300,163,100)
assert deviations==(('Z','L','N',F(159),F(150)),)
assert totals['N']+4==304>300
initial=[row for row in boxed if all(row[0][name]==origin[name] for name,_,_ in clients[5:])]
assert len(initial)==1 and not initial[0][3]
print('Exact strict-greedy boxed lexmax audit passed: 64 states, 24 boxed, unique bad lexmax; initial boxed NE.')
