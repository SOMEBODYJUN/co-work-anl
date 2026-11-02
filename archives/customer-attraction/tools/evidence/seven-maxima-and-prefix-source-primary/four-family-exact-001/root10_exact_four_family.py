"""One exact reconstruction of the five source-listed active states.

No SciPy, source import, LP discovery, game construction or SPE execution.
The rational primal/dual equality and every one of the 130 residuals are
checked explicitly.  This fills a specific gap: the original 2777B script
only solves a floating LP despite its final exact-re-evaluation comment.
"""
from fractions import Fraction as F
from pathlib import Path
from hashlib import sha256
from datetime import datetime, timezone
import json
import sys
import time

BASE = Path(__file__).resolve().parent
OUT = BASE/'root10-four-family-exact.json'

def div(a,b):
    return F(a,b) if b else F(0)

def solve(matrix, rhs):
    n=len(rhs)
    aug=[[F(v) for v in row]+[F(rhs[i])] for i,row in enumerate(matrix)]
    assert len(aug)==n and all(len(row)==n+1 for row in aug)
    for c in range(n):
        pivot=next(i for i in range(c,n) if aug[i][c])
        aug[c],aug[pivot]=aug[pivot],aug[c]
        factor=aug[c][c]
        aug[c]=[v/factor for v in aug[c]]
        for i in range(n):
            if i!=c:
                factor=aug[i][c]
                aug[i]=[a-factor*b for a,b in zip(aug[i],aug[c])]
    result=[row[-1] for row in aug]
    assert all(sum((F(v)*z for v,z in zip(row,result)),F())==F(b)
               for row,b in zip(matrix,rhs))
    return result

def main():
    assert not OUT.exists(), 'refuse to overwrite the one recorded exact execution'
    started=datetime.now(timezone.utc).isoformat();clock=time.perf_counter()
    manifest=json.loads((BASE/'sources/root10-manifest.json').read_text())
    source=next(x for x in manifest if x['id']=='edac9c07ed8f93d82f3f')
    data=Path(source['local_file']).read_bytes()
    assert len(data)==source['size'] and sha256(data).hexdigest()==source['sha256']
    private=[F(6+t,(t+1)*(42-5*t)) for t in range(5)]+[F(1,12)]
    shared=[F(2,42-5*t) for t in range(5)]+[F(7,72)]
    alpha=[min(private[t:]) for t in range(6)]
    beta=[min(shared[t:]) for t in range(6)]
    FP=sum(alpha[:4]);FV=sum(beta[:4])
    assert alpha==[F(1,12)]*6 and FP==F(1,3) and FV==F(26657,111888)
    rows={}
    for f in (0,1):
        for k in range(7):
            if not f+k:continue
            for p in range(5):
                for d in (0,1):
                    j=p+d+f;m=f+k
                    base=F(1,2) if j else F(-1,2)
                    floor=FP if m==1 else FV if m<=6 else F(2,3)
                    G=F(k,p+1) if f==0 else F(6-k,p+1)+F(2*k,p+2)
                    K=F(k*(6-k),p+1)+F(k*(k-1),p+2)
                    co=[floor-div(p,j),F(k,p+d+1)-div(6*f,j),
                        G-div(6*(d+f),j)-F(6*d,(p+1)*(p+2)),
                        K-div(15*(d+f),j)-F(15*d,(p+1)*(p+2))]
                    rows[f,k,p,d]=(base,co)
    assert len(rows)==130
    active=[(1,0,0,1),(0,1,0,0),(1,1,4,0),(1,0,0,0),(0,1,0,1)]
    primal=solve([[-c for c in rows[s][1]]+[F(1)] for s in active],
                 [rows[s][0] for s in active])
    weights=solve([[rows[s][1][i] for s in active] for i in range(4)]+[[1]*5],
                  [0,0,0,0,1])
    assert all(v>=0 for v in primal[:4]) and primal[-1]<0
    assert all(v>=0 for v in weights) and sum(weights)==1
    dual=sum((v*rows[s][0] for v,s in zip(weights,active)),F())
    assert dual==primal[-1]
    residuals=[]
    for state,(base,co) in rows.items():
        residual=base+sum((a*b for a,b in zip(primal[:4],co)),F())
        assert residual>=primal[-1]
        residuals.append({'state':state,'base':str(base),'coefficients':list(map(str,co)),
                          'residual':str(residual),'gap_above_optimum':str(residual-primal[-1])})
    assert min(F(x['residual']) for x in residuals)==dual
    assert Path(source['local_file']).read_bytes()==data
    result={
        'actor':'Boss3','scope':'exact specified four-family uniform-residual optimum on 130 enlarged columns only; no game/SPE/half counterexample',
        'started_utc':started,'finished_utc':datetime.now(timezone.utc).isoformat(),
        'elapsed_seconds':time.perf_counter()-clock,'python':sys.version,'assertions_enabled':__debug__,
        'source_id':source['id'],'source_bytes':len(data),'source_sha256':source['sha256'],
        'source_unchanged':True,'original_program_runs':0,'LP_or_float_optimizer_runs':0,
        'new_fixed_exact_reconstruction_runs':1,'active_states_from_source_markdown':active,
        'alpha':list(map(str,alpha)),'beta':list(map(str,beta)),'FP':str(FP),'FV':str(FV),
        'primal_a_b_c_e_epsilon':list(map(str,primal)),
        'dual_masses_in_active_order':list(map(str,weights)),
        'dual_mass_sum':str(sum(weights)),
        'dual_four_coefficient_sums':[str(sum((v*rows[s][1][i] for v,s in zip(weights,active)),F())) for i in range(4)],
        'dual_base':str(dual),'all_130_residuals_at_least_epsilon':True,
        'exact_active_states':[row['state'] for row in residuals if F(row['residual'])==dual],
        'rows':residuals,
    }
    OUT.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ['source_id','elapsed_seconds','primal_a_b_c_e_epsilon','dual_masses_in_active_order','dual_four_coefficient_sums','dual_base','exact_active_states']},ensure_ascii=False))

if __name__=='__main__':main()
