"""Exact coefficient audit of partitioned queries and random-matching identities."""
from fractions import Fraction as F
from itertools import permutations
import json
from math import comb
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[5]
sys.path.insert(0,str(ROOT))
from customer_attraction import Instance,StrategyCertificate,verify_certificate


def coefficient_audit():
    tested=0
    for m in range(1,6):
        perms=tuple(permutations(range(m)))
        for actual in range(1<<m):
            c=actual.bit_count()
            for optimum in range(1,1<<m):
                k=optimum.bit_count();full=[];part=[]
                for pi in perms:
                    eligible=[i for i,j in enumerate(pi) if optimum>>j&1]
                    shares=[F(1,c+1-(actual>>i&1)) for i in eligible]
                    q=sum(shares,F(0));r=min(shares)
                    b=sum((F(1,c*(c+1)) for i in eligible if actual>>i&1),F(0)) if c else F(0)
                    assert q==F(k,c+1)+b
                    event=all(actual>>i&1 for i in eligible)
                    assert r==(F(1,c+1)+F(event,c*(c+1)) if c else 1)
                    full.append(q);part.append(r)
                avgq=sum(full,F(0))/len(perms);avgr=sum(part,F(0))/len(perms)
                assert avgq==F(m+1,m)*F(k,c+1)-(F(k,m) if not c else 0)
                expected=F(1,c+1)+F(comb(c,k) if c>=k else 0,comb(m,k)*c*(c+1)) if c else F(1)
                assert avgr==expected
                assert min(part)>=F(1,m)
                tested+=1
    return tested


def source_audit():
    source=ROOT/'research/workspaces/customer-attraction/R-a0bb57fa24044a8794bc7991918a19c6/static_matching/static_matching_counterexample.json'
    d=json.loads(source.read_text());ins=Instance.from_dict(d['instance'])
    cert=StrategyCertificate.from_dict(d['certificate']);verification=verify_certificate(ins,cert)
    verification.assert_valid();path=verification.terminal_history
    target=tuple(d['unique_optimal_supports'][0]);m=len(path)
    A=D=F(0);expected_r=F(0)
    for t in ins.customers:
        c=sum(a in t.topics for a in path);k=sum(a in t.topics for a in target)
        A+=F(t.multiplicity*k,c+1)
        if not c:D+=t.multiplicity*k
        if k:
            expected_r+=t.multiplicity*(F(1,c+1)+F(comb(c,k) if c>=k else 0,comb(m,k)*c*(c+1)) if c else F(1))
    values=[]
    for pi in permutations(target):
        q=r=F(0)
        for t in ins.customers:
            c=sum(a in t.topics for a in path)
            shares=[F(t.multiplicity,c+1-int(path[i] in t.topics))
                    for i,a in enumerate(pi) if a in t.topics]
            q+=sum(shares,F(0))
            if shares:r+=min(shares)
        values.append((q,r))
    avgq=sum(v[0] for v in values)/len(values);avgr=sum(v[1] for v in values)/len(values)
    assert avgq==F(m+1,m)*A-D/m
    assert avgr==expected_r
    return {'full_SPE_histories':verification.checked_histories,
            'full_SPE_comparisons':verification.checked_deviations,
            'A':str(A),'D':str(D),'W':ins.welfare(cert.terminal_counts),
            'min_full_query':str(min(q for q,r in values)),
            'average_full_query':str(avgq),
            'min_partitioned_query':str(min(r for q,r in values)),
            'average_partitioned_query':str(avgr)}

if __name__=='__main__':
    print(json.dumps({'all_incidence_pairs_m1_through_m5':coefficient_audit(),
                      'prior_52_client_source':source_audit()},indent=2))
