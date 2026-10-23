"""Definition-level kernel for the two-root cross-child identity only."""
from fractions import Fraction as F
from pathlib import Path
import json

HERE=Path(__file__).resolve().parent
REPO=HERE.parents[5]
SOURCE=REPO/'research/workspaces/customer-attraction/R-d22a706a03c5499d941a6a97f94128a8/representation/high_insertion_2cycle_348_exact.json'


def main():
    data=json.loads(SOURCE.read_text())
    clients=[]
    for row in data['instance']['customers']:
        clients.extend([frozenset(row['topics'])]*row['multiplicity'])
    strategy={tuple(row['history']):row['action'] for row in data['certificate']['actions']}

    def follow(prefix):
        z=tuple(prefix)
        while len(z)<3:
            z+=(strategy[z],)
        return z

    def pay(z,who):
        return sum((F(1,sum(a in likes for a in z))
                    for likes in clients if z[who] in likes),F())

    def phi(background,tail):
        value=F()
        for likes in clients:
            old=sum(a in likes for a in background)
            new=sum(a in likes for a in tail)
            value+=sum((F(1,old+j) for j in range(1,new+1)),F())
        return value

    def insertion(query,z):
        return sum((F(1,1+sum(a in likes for a in z))
                    for likes in clients if query in likes),F())

    A,B=2,5
    ZA,ZB=follow((A,)),follow((B,))
    a,b=ZA[1],ZB[1]
    ZAb,ZBa=follow((A,b)),follow((B,a))
    VA,VB,VAb,VBa=ZA[2:],ZB[2:],ZAb[2:],ZBa[2:]
    RAB=phi((A,),ZB[1:])-phi((A,),ZA[1:])
    RBA=phi((B,),ZA[1:])-phi((B,),ZB[1:])
    gammaA=pay(ZA,1)-pay(ZAb,1)
    gammaB=pay(ZB,1)-pay(ZBa,1)
    assert gammaA>=0 and gammaB>=0
    deepA=phi((A,b),VB)-phi((A,b),VAb)
    deepB=phi((B,a),VA)-phi((B,a),VBa)
    assert deepA<=0 and deepB<=0
    FA=phi((A,),VAb)-phi((A,),VA)
    FB=phi((B,),VBa)-phi((B,),VB)
    assert RAB==deepA+FA-gammaA
    assert RBA==deepB+FB-gammaB
    KAB,KBA=insertion(A,ZB),insertion(B,ZA)
    dA,dB=pay(ZA,0),pay(ZB,0)
    etaAB=sum((F(1,(1+sum(a in likes for a in ZB[1:]))*(2+sum(a in likes for a in ZB[1:])))
               for likes in clients if A in likes and B in likes),F())
    etaBA=sum((F(1,(1+sum(a in likes for a in ZA[1:]))*(2+sum(a in likes for a in ZA[1:])))
               for likes in clients if A in likes and B in likes),F())
    assert KAB+KBA==dA+dB+RAB+RBA-etaAB-etaBA
    report=dict(status='Exact cross-child identities and the involved real IC rows passed; no WP2 proof.',
                source=str(SOURCE.relative_to(REPO)),root_pair=[A,B],
                real_first_child_actions=[a,b],root_branches=[ZA,ZB],
                cross_child_branches=[ZAb,ZBa],
                joint_regrets=[RAB,RBA],deep_terminal_regrets=[deepA,deepB],
                deletion_potential_drifts=[FA,FB],child_ic_slacks=[gammaA,gammaB],
                diagonal_root_payoffs=[dA,dB],cross_insertions=[KAB,KBA],
                cross_intersection_taxes=[etaAB,etaBA],
                R_identity_residual=RAB+RBA-deepA-deepB-FA-FB+gammaA+gammaB,
                K_identity_residual=KAB+KBA-dA-dB-RAB-RBA+etaAB+etaBA,
                scope='Reuses a previously verified complete SPE for a formula kernel, not a new counterexample or a corpus scan.')
    text=json.dumps(report,default=str,ensure_ascii=False,indent=2)+'\n'
    (HERE/'two_query_recursion_audit.json').write_text(text)
    print(text)


if __name__=='__main__':
    main()
