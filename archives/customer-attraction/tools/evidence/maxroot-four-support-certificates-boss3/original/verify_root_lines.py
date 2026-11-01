"""Standard-library definition-level replay of the v2 root-line JSON.

Does not import any discovery generator, NumPy, SciPy, or rounded floats.
This is a replay of the already-known maximum-root/two-copy mechanism.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json

def share(bit,den):return F(bit,den) if bit else F(0)
def verify(path=None):
    path=Path(path) if path else Path(__file__).with_name('root_lines_certificate_v2.json')
    cert=json.loads(path.read_text());n=cert['n'];count=3*n-5
    assert n==6
    paths=[tuple(range(n)),(0,n-1)+tuple(range(n,2*n-2)),(0,1,n-1)+tuple(range(2*n-2,count))]
    reports=[]
    for line in cert['lines']:
        B,C=F(line['B']),F(line['C']);assert B>=0
        mult={name:F(value) for name,value in line['multipliers'].items()}
        assert min(mult.values())>=0
        assert sum(v for name,v in mult.items() if name.endswith('O'))==1
        minimum=None;zero=0
        for bits in product(range(2),repeat=count):
            pays=[]
            for seq in paths:
                den=sum(bits[j] for j in seq)
                pays.append([share(bits[j],den) for j in seq])
            def coefficient(name):
                fields=name.split(':')
                if fields[0]=='CAP':return F(bits[0]-bits[int(fields[1])])
                if fields[0]=='copy':return pays[0][1]-pays[1][1] if fields[1]=='second' else pays[0][2]-pays[2][2]
                pi=int(fields[0][1:]);seq=paths[pi]
                if fields[1]=='lastO':
                    pre=sum(bits[j] for j in seq[:-1])
                    return n*pays[pi][-1]+F(pre,pre+1)
                if fields[1]=='pairO':
                    pre=sum(bits[j] for j in seq[:-2])
                    h=pays[pi][-2]+pays[pi][-1]+F(bits[seq[-2]],(pre+1)*(pre+2))
                    return F(n,2)*h+F(pre,pre+1)
                assert fields[1]=='floor'
                pos,query=int(fields[2]),int(fields[3]);assert pos>=pi+1
                den=n-pos+sum(bits[j] for j in seq[:pos])
                return pays[pi][pos]-F(bits[query],den)
            residual=B*pays[0][0]+C*bits[0]-sum(v*coefficient(name) for name,v in mult.items())
            assert residual>=0,(bits,residual)
            if minimum is None or residual<minimum:minimum=residual
            zero+=residual==0
        reports.append({'B':str(B),'C':str(C),'states':2**count,'minimum_residual':str(minimum),'zero_count':zero})
    return {'status':'PASS','scope':'known maximum-root/two-copy graph, four new supporting parameters only','reports':reports}

if __name__=='__main__':print(json.dumps(verify(),indent=2))
