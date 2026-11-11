"""Recover an exact 16-feature separating wallet from one phase-I support.

No further optimization: homogeneous equality of selected hidden costs plus
sum(lambda)=1 determines a rational direction, which is checked globally.
"""
from fractions import Fraction as F
import json,time,sys,platform,traceback
import numpy as np
import sympy as sp
import transfer as T
from certify import projected

HERE=T.HERE
started=time.monotonic()
receipt={'argv':[sys.executable,*sys.argv],'cwd':str(T.Path.cwd()),'python':platform.python_version(),'script_sha256':T.sha(T.Path(__file__)),'transfer_sha256':T.sha(HERE/'transfer.py'),'certify_sha256':T.sha(HERE/'certify.py'),'started_utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())}
try:
    fixed=T.read(HERE/'fixed_problem.json');raw=np.load(HERE/'phase1_raw_arrays.npz')
    names=[n for n,v in zip(fixed['names'],raw['ineq_dual']) if -v>1e-10]
    assert len(names)==16
    equations=[];refs=[]
    for cell in fixed['cells']:
        si=cell['cell'];support=[h for h in range(16) if raw['x'][16*si+h]>1e-10]
        if len(support)<2:continue
        samples=tuple(tuple(s) for s in cell['samples'])
        base=T.values(names,tuple(cell['actual']),samples,T.HIDDEN[support[0]])
        for h in support[1:]:
            v=T.values(names,tuple(cell['actual']),samples,T.HIDDEN[h])
            equations.append([x-y for x,y in zip(v,base)])
            refs.append({'cell':si,'hidden':h,'base_hidden':support[0]})
    M=sp.Matrix([[sp.Rational(v.numerator,v.denominator) for v in r] for r in equations])
    basis=M.nullspace()
    assert len(basis)==1,(M.shape,len(basis))
    vec=basis[0];vec=vec/sum(vec)
    weights={n:F(int(v.p),int(v.q)) for n,v in zip(names,vec)}
    assert all(v>=0 for v in weights.values()) and sum(weights.values())==1
    proof=projected(weights,fixed,'exact_compact_phase1_wallet')
    assert F(proof['exact_slack'])<0
    import math,functools
    denominator=math.lcm(*(v.denominator for v in weights.values()))
    integers={n:int(v*denominator) for n,v in weights.items()}
    divisor=functools.reduce(math.gcd,integers.values())
    integers={n:v//divisor for n,v in integers.items()}
    proof['primitive_integer_weights']=integers
    proof['normalization_integer_sum']=sum(integers.values())
    proof['discovery']={'equation_count':len(equations),'rank':int(M.rank()),'nullspace_dimension':len(basis),'support_names':names,'equation_refs':refs,'homogeneous_cost_equations':[[str(v) for v in r] for r in equations],'phase1_arrays_sha256':T.sha(HERE/'phase1_raw_arrays.npz'),'optimizer_calls':0}
    path=T.write('compact_separating_row_exact.json',proof)
    print(json.dumps({'status':'EXACT_SEPARATOR','equations':len(equations),'primitive_integer_weights':integers,'wallet':proof['wallet'],'exact_slack':proof['exact_slack'],'slack_float':proof['slack_float'],'file_sha256':T.sha(path)},ensure_ascii=False),flush=True)
    receipt['status']='SUCCESS'
except BaseException as e:
    receipt.update(status='FAILED',error=repr(e),traceback=traceback.format_exc());raise
finally:
    receipt['elapsed_seconds']=time.monotonic()-started
    T.write('execution_compact_wallet.json',receipt)
