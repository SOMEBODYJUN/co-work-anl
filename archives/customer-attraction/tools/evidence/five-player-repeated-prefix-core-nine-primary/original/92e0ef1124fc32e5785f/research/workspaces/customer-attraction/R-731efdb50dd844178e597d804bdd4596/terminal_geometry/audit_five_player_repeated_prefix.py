"""Definition-level audit of the proposed five-player certificate.

No imports of optimization or discovery code. Exactly reconstructs every row
from the real terminal paths or explicit legitimate worst-load guarantees.
Independent mathematical review is still required; this is an author's audit.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json

WEIGHTS={'S':420,'Z0':16,'V0':78,'FB':1471,'FA':799,'BQ':245,
         'MR':20,'CR':405,'BR':105,'QV':107,'MZ':10,'CZ':254,
         'BZ':222,'QZ':24,'BT':444,'RT':64,'ZT':72,'CL':159}
CORNERS=[(0,0),(0,5),(1,0),(1,5),(5,0),(5,5)]
EXPECTED=[[0,11700,0,0,229650,182850],[2580,14280,0,0,218720,171920],
 [19230,28530,2400,0,168840,119640],[41950,51250,22320,19920,183680,134480],
 [45520,54010,1200,8520,63180,65820],[44835,53325,3,7323,59934,62574],
 [46047,54297,2,7082,53765,56165],[51717,59967,4917,11997,57600,60000]]

def one(bits,d,ell,h):
    c,a,b,q,r,v,z=bits
    flags=dict(zip(('C','A','B','Q','R','V','Z'),bits))
    pairs=[(1,1)]*h+[(1,0)]*(d-h)+[(0,1)]*(ell-h)+[(0,0)]*(5-d-ell+h)
    assert len(pairs)==5
    for i,(t,l) in enumerate(pairs):flags[f'T{i}']=t;flags[f'L{i}']=l
    def utility(theme,path):
        return F(flags[theme],sum(flags[x] for x in path)) if flags[theme] else F(0)
    actual=['C','C','C','A','B'];branchB=['C','C','B','Q','R'];branchA=['C','C','A','V','Z']
    uC=utility('C',actual);uA=utility('A',actual);uB=utility('B',actual)
    zQ=utility('Q',branchB);zR=utility('R',branchB);zZ=utility('Z',branchA)
    def last(query,reply):return utility(reply,['C','C','C',query,reply])
    rr={key:F(0) for key in WEIGHTS}
    for i in range(5):
        T=f'T{i}';L=f'L{i}'
        rr['S']+=uA-utility(T,['C','C','C',T,L])
        rr['Z0']+=uB-last('A',L)
        for j in range(5):
            if i!=j:rr['V0']+=last(T,L)-last(T,f'L{j}')
        rr['MR']+=last(T,L)-last(T,'R');rr['MZ']+=last(T,L)-last(T,'Z')
        rr['BT']+=uB-last('A',T)
        rr['RT']+=zR-utility(T,['C','C','B','Q',T])
        rr['ZT']+=zZ-utility(T,['C','C','A','V',T])
        rr['CL']+=uC-F(flags[L],2*c+3)
    rr['FB']=uC-utility('B',branchB);rr['FA']=uC-utility('A',branchA)
    rr['BQ']=uB-last('A','Q');rr['BR']=uB-last('A','R');rr['BZ']=uB-last('A','Z')
    rr['CR']=uC-F(r,2*c+3);rr['CZ']=uC-F(z,2*c+3)
    rr['QV']=zQ-F(v,2*c+b+2);rr['QZ']=zQ-F(z,2*c+b+2)
    G=sum((F(WEIGHTS[k],1000)*rr[k] for k in WEIGHTS),F(0))
    return F(2*int(c+a+b>0)-int(d>0))-G

def main():
    assert WEIGHTS['S']-5*WEIGHTS['V0']-WEIGHTS['MR']-WEIGHTS['MZ']==0
    count=0;minimum=F(100);observed=[];hchecks=0
    for actual in product(range(2),repeat=3):
        table=[]
        for d,ell in CORNERS:
            vals=[one(actual+rest,d,ell,max(0,d+ell-5)) for rest in product(range(2),repeat=4)]
            table.append(int(60000*min(vals)))
        observed.append(table)
        for rest in product(range(2),repeat=4):
          bits=actual+rest
          for d in range(6):
           for ell in range(6):
            first=None
            for h in range(max(0,d+ell-5),min(d,ell)+1):
                rho=one(bits,d,ell,h);assert rho>=0,(bits,d,ell,h,rho)
                if first is None:first=rho
                else:assert first==rho;hchecks+=1
                count+=1;minimum=min(minimum,rho)
    assert observed==EXPECTED,(observed,EXPECTED)
    report={'status':'definition_level_author_audit_passed','customer_columns':count,
        'h_independence_checks':hchecks,'minimum_residual':str(minimum),
        'weights':WEIGHTS,'scale':60000,'table':observed,
        'scope':'conditional m=5 actual path C,C,C,A,B; independent review pending'}
    Path(__file__).with_name('five_player_definition_audit.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))
if __name__=='__main__':main()
