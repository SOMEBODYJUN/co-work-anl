"""Recover a rational common hidden-tail witness for the 71-weight family."""
from fractions import Fraction as F
import json
import sympy as sp
from ordered_root_envelope import solve
from root_envelope import OUT

def S(x):return sp.Rational(x.numerator,x.denominator)
def Q(x):return F(int(x.p),int(x.q))
def main():
    result,model=solve(return_model=True)
    support=[i for i,y in enumerate(result['float_dual']) if -y>1e-10]
    positive=[i for i,x in enumerate(result['float_primal'][:len(model['parameters'])]) if x>1e-9]
    eq=[];rhs=[]
    for k,context in enumerate(model['contexts']):
        eq.append([F(int(model['metadata'][j]['context_index']==k)) for j in support]);rhs.append(model['context_mass'][context])
    for i in positive:
        eq.append([model['rows'][j][0][i] for j in support]);rhs.append(model['c'][i])
    A=sp.Matrix([[S(x) for x in r] for r in eq]);b=sp.Matrix([S(x) for x in rhs])
    sol,free,indices=A.gauss_jordan_solve(b,freevar=True)
    print(json.dumps({'support':len(support),'equalities':len(eq),'free_parameters':len(free),'free_indices':indices}),flush=True)
    assert len(free)<=1
    if len(free):
        t=free[0];aff=[]
        for x in sol:aff.append((Q(x.subs(t,0)),Q(sp.diff(x,t))))
        inequalities=list(aff)
        for i in range(len(model['parameters'])):
            a=model['c'][i]-sum(model['rows'][j][0][i]*aff[k][0] for k,j in enumerate(support))
            b=-sum(model['rows'][j][0][i]*aff[k][1] for k,j in enumerate(support))
            inequalities.append((a,b))
        lo=None;hi=None
        for a,b in inequalities:
            if b==0:assert a>=0,(a,b)
            elif b>0:
                v=-a/b;lo=v if lo is None else max(lo,v)
            else:
                v=-a/b;hi=v if hi is None else min(hi,v)
        assert lo is None or hi is None or lo<=hi,(lo,hi)
        chosen=(lo+hi)/2 if lo is not None and hi is not None else lo if lo is not None else hi if hi is not None else F(0)
        ys=[a+b*chosen for a,b in aff]
    else:
        ys=[Q(x) for x in sol];lo=hi=chosen=None
    assert min(ys)>=0
    for row,v in zip(eq,rhs):assert sum(x*y for x,y in zip(row,ys))==v
    residual=[]
    for i,p in enumerate(model['parameters']):
        x=model['c'][i]-sum(model['rows'][j][0][i]*y for j,y in zip(support,ys));assert x>=0,(p,x)
        residual.append({'parameter':list(p),'slack':str(x)})
    lower=model['u'][0]-sum(model['rows'][j][1]*y for j,y in zip(support,ys))
    assert lower>0
    output={'status':'EXACT NONSEPARATION WITNESS FOR ALL 71 NONNEGATIVE WEIGHTS',
        'scope':'Fixed given actual histogram; averages six indexed root deviations; independent conditional hidden tails, not a complete SPE',
        'point_sha256':result['input_sha256'],'parameter_count':len(model['parameters']),'contexts':len(model['contexts']),
        'support':[{'row_index':j,'actual':model['contexts'][model['metadata'][j]['context_index']][0],
                    'd':model['contexts'][model['metadata'][j]['context_index']][1],
                    'root_membership':model['contexts'][model['metadata'][j]['context_index']][2],
                    'tail':model['metadata'][j]['tail'],'mass':str(y)} for j,y in zip(support,ys)],
        'context_masses':[{'context':list(c),'mass':str(model['context_mass'][c])} for c in model['contexts']],
        'column_slacks':residual,'strict_lower_bound_for_every_row_slack':str(lower),
        'lower_bound_float':float(lower),'free_parameter_interval':None if chosen is None else {'lower':str(lo),'upper':str(hi),'chosen':str(chosen)}}
    (OUT/'ordered_root_exact_nonseparation.json').write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps({k:v for k,v in output.items() if k not in ('support','context_masses','column_slacks','free_parameter_interval')},indent=2))

if __name__=='__main__':main()
