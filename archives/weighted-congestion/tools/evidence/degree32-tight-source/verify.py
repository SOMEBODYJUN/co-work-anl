"""Verify the degree-32 source threshold and its optimizer's discrete branch."""
from fractions import Fraction as F
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
SOURCE = Path('archives/weighted-congestion/tools/evidence/symmetric-source/original/tests/audits/weighted_congestion/source_degree32/verify.py')
SOURCE_SHA = '0d3afd04aa12c17e68a04b39645e9f0658c19c4f9222ad3bcc9f395f38da3cfb'
LOW = F(71,40)
HIGH = F(1775001,1000000)
CUTOFF = F(1,56)
CORE = (6,2)
WINDOW = F(31,625), F(249,5000)
WITNESS = F(463,9321), F(51511,456862)


def engine_at(repo):
    path=repo/SOURCE
    assert sha256(path.read_bytes()).hexdigest()==SOURCE_SHA
    spec=importlib.util.spec_from_file_location('frozen_bernstein',path)
    engine=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(engine)
    return engine


def ratios(w,beta):
    n,k=CORE
    a,b,c,d,z=(1+w)**32,(1+w)**k,(1+n*w)**k,(n*w)**k,w**32
    return (1+n*beta*a)/(c+n*beta), (b+beta*z)/(d+beta*a)


def cover(engine,threshold,restrict):
    p,q=threshold.numerator,threshold.denominator
    engine.P,engine.Q=p,q
    assert (1+CUTOFF)**32<threshold
    digest=sha256()
    leaves=coefficients=depth=0
    nontrivial=[]
    for n in range(1,57):
        for k in range(1,33):
            a,b=CUTOFF,F(1,max(1,n-1))
            poly=engine.obstruction(n,k)
            for w in (a,b):
                A,B,C,D,W=(1+w)**32,(1+w)**k,(1+n*w)**k,(n*w)**k,w**32
                assert engine.horner(poly,w)==n*(q*A-p)*(q*B-p*D)-(p*C-q)*(p*A-q*W)
            spans=((a,WINDOW[0]),(WINDOW[1],b)) if restrict and (n,k)==CORE else ((a,b),)
            for left,right in spans:
                vector=engine.bernstein_integer_vector(poly,left,right)
                cert=engine.certify(vector)
                leaf_map={row['path']:row for row in cert}
                assert len(leaf_map)==len(cert) and engine.verify_tree(vector,leaf_map)==set(leaf_map)
                leaves+=len(cert)
                coefficients+=len(vector)*len(cert)
                depth=max(depth,*(len(row['path']) for row in cert))
                row=[n,k,str(left),str(right),cert]
                digest.update((json.dumps(row,separators=(',',':'))+'\n').encode('ascii'))
                if len(cert)>1:
                    nontrivial.append([n,k,str(left),str(right),[r['path'] for r in cert]])
    return {'threshold':str(threshold),'polynomials':56*32,'leaves':leaves,'coefficients':coefficients,'max_depth':depth,
            'aggregate_leaf_sha256':digest.hexdigest(),'subdivisions':nontrivial}


if __name__=='__main__':
    assert __debug__
    engine=engine_at(Path(sys.argv[1] if len(sys.argv)>1 else '.').resolve())
    w,beta=WITNESS
    assert WINDOW[0]<w<WINDOW[1] and 0<beta<1
    H,L=ratios(w,beta)
    assert H>LOW and L>LOW
    data={'finite_reduction_cutoff':str(CUTOFF),'witness':[6,2,str(w),str(beta)],
          'witness_margin':str(min(H,L)-LOW),'isolation':cover(engine,LOW,True),'upper':cover(engine,HIGH,False)}
    print(json.dumps(data,ensure_ascii=False,indent=2))
