"""Recover exact aggregation obstruction; independently audit all stated rows."""
from pathlib import Path
from fractions import Fraction as F
import json
import argparse
from strengthened_global_projection import build

HERE=Path(__file__).resolve().parent
M=5


def get_witness():
    data=json.loads((HERE/'strengthened_global_projection.json').read_text())
    support=[a['mask'] for a in data['atoms_float']]
    vals=[a['mass'] for a in data['atoms_float']]
    rows,names,covered,opt,coeff=build(M)
    equations=[[F(a!=0) for a in support]]
    rhs=[F(1)]
    for row in rows:
        c=[F(float(row[a])).limit_denominator(1000000) for a in support]
        if abs(sum(float(z)*x for z,x in zip(c,vals)))<1e-7:
            equations.append(c);rhs.append(F(0))
    augmented=[row+[value] for row,value in zip(equations,rhs)]
    pivot=0
    for col in range(len(support)):
        chosen=next((j for j in range(pivot,len(augmented)) if augmented[j][col]),None)
        assert chosen is not None
        augmented[pivot],augmented[chosen]=augmented[chosen],augmented[pivot]
        scale=augmented[pivot][col]
        augmented[pivot]=[x/scale for x in augmented[pivot]]
        for j in range(len(augmented)):
            if j!=pivot and augmented[j][col]:
                factor=augmented[j][col]
                augmented[j]=[a-factor*b for a,b in zip(augmented[j],augmented[pivot])]
        pivot+=1
    assert all(not any(row[:-1]) and not row[-1] for row in augmented[pivot:])
    return {a:augmented[j][-1] for j,a in enumerate(support)}



def audit(mass):
    atoms=[(a|(1<<(M+t)),v/M) for a,v in mass.items() for t in range(M)]
    assert all(v>=0 for _,v in atoms)
    bit=lambda z,c:(z>>c)&1
    dot=lambda f:sum((v*f(z) for z,v in atoms),F(0))
    W=dot(lambda z:F(bool(z&((1<<M)-1))))
    O=dot(lambda z:F(bool(z>>M)))
    assert W==1 and O>2
    sizes=[dot(lambda z,c=c:F(bit(z,c))) for c in range(2*M)]
    K=max(sizes);rootmax=[c for c,s in enumerate(sizes) if s==K]
    coefficient=F((M-1)**2)-F(M*M*(M-3)**2,2*(3*M*M-7*M+2))
    counts={'floor':0,'AP':0,'BNS_C_all_maxima':0,'improved_exchange_all_players_all_maxima':0}
    records=[]
    slacks={key:None for key in counts}
    def check(name,slack):
        assert slack>=0,(name,slack)
        counts[name]+=1
        slacks[name]=slack if slacks[name] is None else min(slacks[name],slack)
    for i in range(M):
        k=M-i
        b=lambda z:(z&((1<<i)-1)).bit_count()
        u=dot(lambda z:F(bit(z,i),(z&((1<<M)-1)).bit_count()) if bit(z,i) else F(0))
        ws=[dot(lambda z,c=c:F(bit(z,c),b(z)+k)) for c in range(2*M)]
        weightedmax=max(ws);maxima=[c for c,s in enumerate(ws) if s==weightedmax]
        records.append({'player':i,'u':str(u),'weighted_K':str(weightedmax),'weighted_maxima':maxima})
        for c in range(2*M):
            check('floor',u-ws[c])
        if k>=2:
            for c in range(2*M):
                p=F((k-1)*(M-1))+F(k*k,2)
                for d in range(2*M):
                    f=dot(lambda z:F(bit(z,d),b(z)+k) if bit(z,c) else F(bit(z,d),b(z)+1))
                    check('AP',ws[c]+p*(u-ws[c])-f)
            for c in maxima:
                Mc=k+max([b(z) for z,v in atoms if v>0 and bit(z,c)]+[0])
                for d in range(2*M):
                    f=dot(lambda z:F(bit(z,d),b(z)+k) if bit(z,c) else F(bit(z,d),b(z)+1))
                    check('BNS_C_all_maxima',weightedmax+(k-1)*(Mc-1)*(u-weightedmax)-f)
        for c in rootmax:
            for d in range(2*M):
                q=dot(lambda z:F(M*bit(z,d)*(1-bit(z,c))+bit(z,d)*bit(z,c)))
                check('improved_exchange_all_players_all_maxima',K+coefficient*(M*u-K)-q)
    return {'scope':'Exact obstruction to aggregating the listed actual-node necessary conditions; NOT SPE counterexample.',
            'm':M,'W':str(W),'comparison_union':str(O),'excess_over_2W':str(O-2*W),'unweighted_K':str(K),'unweighted_maxima':rootmax,'coefficient':str(coefficient),
            'group_mass':{str(a):str(v) for a,v in mass.items()},'group_interpretation':'For each mask a and each t=0,...,4, mass group_mass[a]/5 belongs to actual-mask a and comparison topic t alone.',
            'checked_rows':counts,'minimum_slacks':{k:str(v) for k,v in slacks.items()},'actual_nodes':records}

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--output')
    args=parser.parse_args()
    report=audit(get_witness())
    if args.output:
        with Path(args.output).open('x') as output:
            output.write(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ['group_mass','actual_nodes','group_interpretation']}))
