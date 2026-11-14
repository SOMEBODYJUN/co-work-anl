"""Independent exact local checks; finite checks do not certify an SPE."""
import hashlib
import itertools
import json
from fractions import Fraction as Q
from pathlib import Path

ROOT = next(p for p in Path(__file__).resolve().parents if (p/'work.py').is_file())
OUT = Path(__file__).with_name("parent-math-check.json")

def div(n, d):
    return Q(n, d) if n else Q(0)

def pair(p, d, e, x, y):
    return Q(x+y, p+1)-Q(x*y+d, (p+1)*(p+2))-div(d+e, p+d+e)

def nine(p,t,q,h):
    b,c,j,v=h
    z1,z2=p+t+b+c,p+c+j+v
    return (50142*div(t,z1)+21056*div(c,z2)+925*b
            +6052*(Q(q,p+t+b+1)-div(c,z1))
            +2782*(Q(j,p+t+b+1)-div(c,z1))
            +4014*(Q(v,p+t+b+1)-div(c,z1))
            +4004*(Q(b,p+c+j+1)-div(v,z2))
            +924*(Q(v,p+c+2)-div(j,z2))+736*pair(p+t,b,c,j,v))

def run():
    # These are polynomial/rational identities for arbitrary nonnegative p;
    # exact bounded replay catches sign and numerator errors in our transcription.
    counts={"three_ic_identity":0,"pair_redundancy":0,"disagreement_identity":0}
    for p in range(12):
        g=lambda a,b: Q(a*b,(p+1)*(p+2))
        u=lambda a,b: Q(a,p+1)-g(a,b)
        for d,e,x,y,r in itertools.product(range(2),repeat=5):
            rhs=(u(d,e)-u(x,r))+(u(r,x)-u(y,x))+(u(e,d)-u(r,d))+g(d,d)-g(d,r)
            assert -pair(p,d,e,x,y)==rhs
            counts['three_ic_identity']+=1
        for d,e,y in itertools.product(range(2),repeat=3):
            assert pair(p,d,e,d,y)==Q(y,p+d+1)-div(e,p+d+e)-Q(d*(1-e),(p+1)*(p+2))
            counts['pair_redundancy']+=1
        for d,e,x,y in itertools.product(range(2),repeat=4):
            lhs=pair(p,d,e,x,y)-(pair(p,d,e,x,x)+pair(p,d,e,y,y))/2
            assert lhs==Q((x-y)**2,2*(p+1)*(p+2))
            counts['disagreement_identity']+=1
    table=[]
    for p in range(4):
        row=[]
        for t,q in itertools.product(range(2),repeat=2):
            minimum=min(nine(p,t,q,h) for h in itertools.product(range(2),repeat=4))
            assert minimum==Q(65146*t+6052*q,p+1+2*t)+925*t
            row.append(str(minimum))
        table.append(row)
    boundary=min(nine(4,1,0,h) for h in itertools.product(range(2),repeat=4))
    assert boundary==Q(29576,3)<Q(71621,7)
    src=ROOT/'research/workspaces/six-boss2-20261111-cross/joint_requery/actual_signature_witness.json'
    data=json.loads(src.read_text())
    assert sum(Q(s['mass']) for s in data['support'])==1
    actual=[sum(Q(s['mass'])*div(s['a'][i],sum(s['a'])) for s in data['support']) for i in range(6)]
    assert actual[3]==Q(data['r_u4']) and actual[5]==Q(data['u6'])
    lower=sum(Q(s['mass'])*min(nine(sum(s['a'][:3]),s['t'],s['q'],h) for h in itertools.product(range(2),repeat=4)) for s in data['support'])
    slack=71198*actual[3]+925*Q(data['K'])-lower
    assert slack==Q(-90896,19269)==Q(data['new_slack_integer_scale'])
    assert slack/71198==Q(-45448,685957131)==Q(data['new_slack_normalized'])
    report={"status":"PASS","scope":"Exact local identities, nine-row envelope and actual-linked arithmetic; no claim of complete SPE or half-coverage.","identity_fixtures":counts,"nine_row_minimum_table":table,"p4_true_minimum":str(boundary),"p4_invalid_formula":str(Q(71621,7)),"actual_support_atoms":len(data['support']),"actual_utilities":list(map(str,actual)),"integer_new_slack":str(slack),"normalized_new_slack":str(slack/71198),"input":{"path":str(src.relative_to(ROOT)),"sha256":hashlib.sha256(src.read_bytes()).hexdigest()}}
    OUT.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(report,ensure_ascii=False))

if __name__=='__main__':
    run()
