"""Narrow exact checks of A12--A15's explicit teaching examples.

This is neither a canonical nonlinear solver nor a replay of the old suites.
"""
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
import json

ROOT=Path(__file__).parent

def serial(x):
    if isinstance(x,Q):return str(x)
    if isinstance(x,dict):return {str(k):serial(v) for k,v in x.items()}
    if isinstance(x,(list,tuple)):return [serial(v) for v in x]
    return x

def loads(weights,profile):
    return (sum((w*p for w,p in zip(weights,profile) if p is not None),Q(0)),
            sum((w*(1-p) for w,p in zip(weights,profile) if p is not None),Q(0)))

def costs_by_realizations(weights,sites,layout,profile,customer,cost):
    s,t=layout; other=[j for j,p in enumerate(profile) if p is not None and j!=customer]
    sums=[Q(0),Q(0)]
    for bits in product((0,1),repeat=len(other)):
        probability=Q(1)
        other_load=[Q(0),Q(0)]
        for j,bit in zip(other,bits):
            probability*=profile[j] if bit else (1-profile[j])
            other_load[0 if bit else 1]+=weights[j]
        for side,site in enumerate((s,t)):
            sums[side]+=probability*cost(customer,site,weights[customer]+other_load[side])
    return tuple(sums)

def verify_table(weights,sites,table,cost):
    checked=0
    for (s,t),profile in table.items():
        assert len(profile)==len(weights)
        for i,w in enumerate(weights):
            a=i in sites[s];b=i in sites[t];p=profile[i]
            if not a and not b:assert p is None;continue
            if a and not b:assert p==1;continue
            if b and not a:assert p==0;continue
            assert 0<=p<=1
            c1,c2=costs_by_realizations(weights,sites,(s,t),profile,i,cost)
            assert (p==0 or c1<=c2) and (p==1 or c2<=c1),(s,t,i,p,c1,c2)
            checked+=1
    return checked

def factor_at(weights,table,layout):
    s,t=layout;x,y=loads(weights,table[layout]);ratios=[Q(1)]
    for r in sorted({u for pair in table for u in pair}):
        if r!=s:
            v=loads(weights,table[r,t])[0]
            if not x and v:return None
            ratios.append(v/x if x else Q(0))
        if r!=t:
            v=loads(weights,table[s,r])[1]
            if not y and v:return None
            ratios.append(v/y if y else Q(0))
    return max(ratios)

def travel_examples():
    weights=[Q(1,2)]*3;sites=[{0,2},{0,1},{1,2}]
    preferred={0:0,1:1,2:2};records=[]
    for epsilon in (Q(1,100),Q(0)):
        table={}
        for s,t in product(range(3),repeat=2):
            p=[]
            for i in range(3):
                if i not in sites[s] and i not in sites[t]:p.append(None)
                elif i not in sites[t]:p.append(Q(1))
                elif i not in sites[s]:p.append(Q(0))
                elif s==t or not epsilon:p.append(Q(1,2))
                else:p.append(Q(int(s==preferred[i])))
            table[s,t]=p
        cost=lambda i,s,z:z+(0 if s==preferred[i] else epsilon)
        checked=verify_table(weights,sites,table,cost)
        factors={str(pair):factor_at(weights,table,pair) for pair in table}
        assert min(factors.values())==(2 if epsilon else 1)
        if epsilon:assert set(factors.values())=={Q(2)}
        records.append({'epsilon':epsilon,'full_table':{str(k):v for k,v in table.items()},
                        'factors':factors,'checked_common_customer_conditions':checked})
    vertices=[(Q(0),Q(0)),(Q(2),Q(0)),(Q(1),Q(1))]
    clients=[(Q(1,2),Q(0)),(Q(7,4),Q(1,4)),(Q(3,4),Q(3,4))]
    squared=[]
    for i,(x,y) in enumerate(clients):
        row=[(x-a)**2+3*(y-b)**2 for a,b in vertices]
        assert sorted(row)==[Q(1,4),Q(9,4),Q(13,4)]
        assert {j for j,d in enumerate(row) if d<=Q(64,25)}=={preferred[i],(preferred[i]+1)%3}
        squared.append(row)
    return {'cases':records,'distance_squared':squared,'radius_squared':Q(64,25),
            'scope':'two explicit complete tables; universal lower bound uses the analytic all-NE argument'}

def interval_constraint(a,b,relation):
    low,high=Q(0),Q(1)
    if relation=='ge':return interval_constraint(-a,-b,'le')
    if not b:return (low,high) if (a==0 if relation=='eq' else a<=0) else None
    root=-a/b
    if relation=='eq':return (root,root) if 0<=root<=1 else None
    if b>0:high=min(high,root)
    else:low=max(low,root)
    return (low,high) if low<=high else None

def intersect(a,b):
    if a is None or b is None:return None
    low=max(a[0],b[0]);high=min(a[1],b[1]);return (low,high) if low<=high else None

def cube_nine_states():
    states=['P1','P2','M'];own={'P1':(Q(1),Q(1)),'P2':(Q(0),Q(0)),'M':(Q(0),Q(1))}
    relation={'P1':'le','P2':'ge','M':'eq'}
    coefficients=[(Q(-98),Q(306)),(Q(-61),Q(250))];cells={};points=[]
    for s1,s2 in product(states,repeat=2):
        p1=intersect(own[s1],interval_constraint(*coefficients[1],relation[s2]))
        p2=intersect(own[s2],interval_constraint(*coefficients[0],relation[s1]))
        cells[s1+','+s2]=None if p1 is None or p2 is None else (p1,p2)
        if cells[s1+','+s2] is not None:
            assert p1[0]==p1[1] and p2[0]==p2[1]
            points.append((p1[0],p2[0]))
    assert set(points)=={(Q(1),Q(0)),(Q(0),Q(1)),(Q(61,250),Q(49,153))}
    spectrum=sorted({Q(1)+2*p1+3*p2 for p1,p2 in points})
    assert spectrum==[Q(15611,6375),Q(3),Q(4)] and Q(7,2) not in spectrum
    conditional=[]
    for p in points:
        values=[costs_by_realizations([Q(2),Q(3)],[{0,1},{0,1}],(0,1),p,i,
             lambda i,s,z:(z+(Q(1) if s==0 else Q(0)))**3) for i in range(2)]
        assert all((prob==0 or c[0]<=c[1]) and (prob==1 or c[1]<=c[0]) for prob,c in zip(p,values))
        conditional.append({'p':p,'costs':values})
    assert interval_constraint(Q(0),Q(0),'eq')==(Q(0),Q(1))
    return {'coefficients':coefficients,'nine_cells':cells,'NE_points':points,
            'first_load_spectrum':spectrum,'nonattainable_target':Q(7,2),'conditional_costs':conditional,
            'constant_zero_cost_cell':((Q(0),Q(1)),(Q(0),Q(1)))}

def four_site(values,core_probabilities):
    n=2*max(len(values),2);T=sum(values);a=list(values)+[0]*(n-len(values))
    w=[1+Q(n*x-T,16*n*n*T) for x in a]
    M=Q(5*n,2);q=Q(13,20*n);R=Q(143*n*n+13,40*n);d=Q(27*n,10)
    weights=[M]+w+[q,n-q,Q(n),R-M-q,Q(n,5)]
    sites=[set(range(n+1))|{n+1,n+2},set(range(n+1))|{n+3},{0,n+1,n+4},{0,n+5}]
    reach=[sum((weights[i] for i in site),Q(0)) for site in sites]
    table={}
    for s,t in product(range(4),repeat=2):
        p=[]
        for i in range(len(weights)):
            if i not in sites[s] and i not in sites[t]:p.append(None)
            elif i not in sites[t]:p.append(Q(1))
            elif i not in sites[s]:p.append(Q(0))
            elif s==t:p.append(Q(1,2))
            elif {s,t}=={0,1}:p.append(core_probabilities[i] if s==0 else 1-core_probabilities[i])
            elif {s,t}=={0,2}:p.append(Q(int((s==2) if i==0 else (s==0))))
            else:p.append(Q(int(reach[s]<reach[t])))
        table[s,t]=p
    checked=verify_table(weights,sites,table,lambda i,s,z:z)
    factor=factor_at(weights,table,(0,1));x,y=loads(weights,table[0,1])
    expected=Q(13,10) if values==[1,1] else Q(6136,4695)
    assert factor==expected
    assert (x,y)==((Q(177,16),Q(175,16)) if values==[1,1] else (Q(2817,256),Q(2815,256)))
    return {'source':values,'n':n,'weights':weights,'reach':reach,'core_probabilities':core_probabilities,
            'core_loads':(x,y),'actual_complete_rule_factor':factor,'full_table':{str(k):v for k,v in table.items()},
            'checked_common_customer_conditions':checked,'scope':'given full rule attainment, not a NO-instance optimum claim'}

def near_oracle(D,light,k,H=Q(1)):
    cells=[]
    for states in product((-1,0,1),repeat=len(light)):
        mixed=k+sum(s==0 for s in states)
        numerator=D+sum((w*s for w,s in zip(light,states)),Q(0))
        if mixed==1:
            if numerator:continue
            low,high=-H,H
        else:
            low=high=numerator/(1-mixed)
        for w,s in zip(light,states):
            if s==1:high=min(high,w)
            elif s==-1:low=max(low,-w)
            else:low=max(low,-w);high=min(high,w)
        low=max(low,-H);high=min(high,H)
        if low<=high:cells.append({'light_states':states,'gap_interval':(low,high)})
    return cells

def near_examples():
    inputs=[
      ('B-one-light-mixer',Q(0),[Q(1),Q(3,4)],2,[Q(11,16),Q(0)],[Q(19,32)]*2,(Q(49,16),Q(43,16))),
      ('B-boundary',Q(7,4),[Q(1),Q(3,4)],2,[Q(0),Q(0)],[Q(1,2)]*2,(Q(15,4),Q(15,4))),
      ('C-one-move-tie',Q(11,4),[Q(1,4),Q(1,2),Q(1)],4,[Q(1),Q(0),Q(0)],[Q(3,8)]*4,(Q(6),Q(13,2))),
      ('D-reflection',Q(-11,4),[Q(1,4),Q(1,2),Q(1)],4,[Q(0),Q(1),Q(1)],[Q(5,8)]*4,(Q(13,2),Q(6))),
      ('A-reject',Q(3),[Q(1)],0,None,None,None),
      ('C-k-one-reject',Q(2),[Q(1)],1,None,None,None),
      ('C-after-tie-reject',Q(9,4),[Q(1,4),Q(1,2),Q(1)],2,None,None,None),
      ('empty-light',Q(1),[],3,[],[Q(3,8)]*3,(Q(13,4),Q(15,4))),
      ('empty-zero',Q(0),[],1,[],[Q(1,2)],(Q(1),Q(1))),
      ('tiny-light',Q(0),[Q(1,2**30)],1,[Q(1,2)],[Q(1,2)],(1+Q(1,2**31),1+Q(1,2**31))),
    ]
    records=[]
    for name,D,light,k,pl,ph,expected in inputs:
        cells=near_oracle(D,light,k)
        accepted=pl is not None;assert bool(cells)==accepted,name
        row={'name':name,'D':D,'H':Q(1),'light':light,'heavy_weights':[Q(2)]*k,
             'fixed_heavy_support':'all genuinely mixed','near_band_feasible':accepted,'complete_light_support_cells':cells}
        if accepted:
            weights=light+[Q(2)]*k;p=pl+ph;a=max(D,Q(0));b=max(-D,Q(0))
            x=a+sum((w*z for w,z in zip(weights,p)),Q(0))
            y=b+sum((w*(1-z) for w,z in zip(weights,p)),Q(0));assert (x,y)==expected
            costs=[]
            for i,(w,z) in enumerate(zip(weights,p)):
                c1=a+w+sum((v*q for j,(v,q) in enumerate(zip(weights,p)) if j!=i),Q(0))
                c2=b+w+sum((v*(1-q) for j,(v,q) in enumerate(zip(weights,p)) if j!=i),Q(0))
                assert (z==0 or c1<=c2) and (z==1 or c2<=c1),(name,i)
                costs.append((c1,c2))
            assert abs(x-y)<=1 and all(0<q<1 for q in ph)
            row.update({'probabilities':p,'loads':(x,y),'gap':x-y,'direct_conditional_costs':costs})
        records.append(row)
    return records

def main():
    report={'scope':'new narrow exact arithmetic for explicit A12-A15 teaching examples; no canonical suite replay',
      'travel_and_geometry':travel_examples(),'cube_and_constant_cells':cube_nine_states(),
      'four_site_witnesses':[four_site([1,1],[Q(81,160),Q(1),Q(0),Q(1),Q(0)]),
                             four_site([1],[Q(1281,2560),Q(0),Q(257,510),Q(257,510),Q(1)])],
      'near_band_ten_cases':near_examples()}
    out=ROOT/'replay/teaching-witnesses.json';out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(serial(report),ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'status':'passed','travel_tables':2,'cube_support_states':9,
       'four_site_full_tables':2,'near_band_cases':10,'report':str(out)},ensure_ascii=False))

if __name__=='__main__':main()
