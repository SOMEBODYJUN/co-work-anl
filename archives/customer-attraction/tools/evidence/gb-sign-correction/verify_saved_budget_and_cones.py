"""Independent exact local check for a sign correction; no source rerun or LP."""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
from functools import lru_cache
import hashlib,json
REPO=Path('/workspace/scratch/37f0f9248cfc/boss4-research')
OUT=Path(__file__).resolve().parent
BASE=REPO/'archives/customer-attraction/tools/evidence/security-cones-new/original'
def sha(raw):return hashlib.sha256(raw).hexdigest()
def engine(policy,n,k):
    actions={tuple(r['history']):r['action']for r in policy}
    histories={h for depth in range(n)for h in product(range(k),repeat=depth)}
    assert len(actions)==len(policy)and set(actions)==histories
    assert all(a in range(k)for a in actions.values())
    @lru_cache(None)
    def finish(h):
        return h if len(h)==n else finish(h+(actions[h],))
    def single(a,z,mask):
        return F(1,sum(bool(mask&(1<<b))for b in z))if mask&(1<<a)else F()
    return actions,histories,finish,single
budgets=[]
for path in sorted(BASE.glob('all_SPE_GB_*.json')):
    raw=path.read_bytes();d=json.loads(raw);n=d['players'];k=d['topics']
    actions,H,finish,single=engine(d['strategy']['actions'],n,k)
    types=[(sum(1<<a for a in row['topics']),row['multiplicity'])for row in d['game']['customers']]
    def utility(a,z):return sum((w*single(a,z,mask)for mask,w in types),F())
    gapmin=None;checks=0
    for h in H:
        own=utility(actions[h],finish(h))
        for a in range(k):
            gap=own-utility(a,finish(h+(a,)));assert gap>=0
            gapmin=gap if gapmin is None else min(gapmin,gap);checks+=1
    z=finish(());W=sum(w for mask,w in types if any(mask&(1<<a)for a in z))
    p=list(map(F,d['security']['primary']));assert min(p)>=0 and sum(p)==1
    def query(a,B):
        return sum((w*F(1,1+sum(bool(mask&(1<<b))for b in B))for mask,w in types if mask&(1<<a)),F())
    backgrounds=list(product(range(k),repeat=n-1))
    primal=min(sum((p[a]*query(a,B)for a in range(k)),F())for B in backgrounds)
    Q=[(tuple(row['rivals']),F(row['probability']))for row in d['security']['dual']]
    assert sum(q for B,q in Q)==1 and all(q>=0 and len(B)==n-1 for B,q in Q)
    dual=max(sum((q*query(a,B)for B,q in Q),F())for a in range(k))
    assert primal==dual
    if 'value'in d['security']:assert F(d['security']['value'])==primal
    C=F()
    for i in range(n):
        h=z[:i]
        for a in range(k):
            leaf=finish(h+(a,));B=leaf[:i]+leaf[i+1:]
            assert len(B)==n-1
            C+=p[a]*sum((p[t]*w*F(1,1+sum(bool(mask&(1<<b))for b in B))for t in range(k)for mask,w in types if mask&(1<<t)),F())
    assert list(z)==d['outcome']and W==d['W']and C==F(d['sum_C'])
    assert C-W==F(d['GB_violation_sumC_minus_W'])<0
    lines=raw.decode().splitlines()
    budgets.append(dict(path=str(path.relative_to(REPO)),sha256=sha(raw),players=n,topics=k,ordered_decision_histories=len(H),incl_self_IC=checks,min_IC=str(gapmin),specified_p=[str(x)for x in p],exact_static_saddle_value=str(primal),static_ordered_backgrounds=len(backgrounds),achieved_W=W,achieved_C=str(C),achieved_C_minus_W=str(C-W),positive_W_minus_C=str(W-C),field_lines={key:next(i for i,line in enumerate(lines,1)if '"'+key+'"'in line)for key in ['GB_violation_sumC_minus_W','W','sum_C','possible_ordered_SPE_paths']},scope='Recomputed the saved attaining policy and its static saddle exactly; all-SPE maximum direction and exhaustiveness from original generator proof, not re-enumerated here.'))
selected=BASE/'selected_security_cones.json';raw=selected.read_bytes();d=json.loads(raw);cones=[];coords=0
for case in d['cases']:
    n,k=case['players'],case['topics'];actions,H,finish,single=engine(case['policy'],n,k);masks=list(range(1,1<<k))
    root=finish(())
    rows=set()
    for h in H:
        own=tuple(single(actions[h],finish(h),mask)for mask in masks)
        for a in range(k):
            row=tuple(x-single(a,finish(h+(a,)),mask)for x,mask in zip(own,masks))
            rows.add(row)
    certs=[]
    for cert in case['certificates']:
        Q=[(tuple(B),F(q))for B,q in cert['Q']]
        assert sum(q for B,q in Q)==1 and all(len(B)==n-1 and min(B)>=0 and max(B)<k and q>=0 for B,q in Q)
        target=[F(int(any(mask&(1<<a)for a in root)),n)if cert['target']=='aggregate'else single(root[int(cert['target'])],root,mask)for mask in masks]
        minres=None;sparse=0
        for a,terms in enumerate(cert['lambda']):
            combined=[F()for mask in masks]
            for term in terms:
                row=tuple(map(F,term['row']));lam=F(term['coefficient'])
                assert row in rows and lam>=0
                sparse+=1
                combined=[x+lam*y for x,y in zip(combined,row)]
            for index,mask in enumerate(masks):
                mean=sum((q*F(1,1+sum(bool(mask&(1<<b))for b in B))for B,q in Q),F())if mask&(1<<a)else F()
                residual=target[index]-mean-combined[index]
                assert residual>=0
                minres=residual if minres is None else min(minres,residual);coords+=1
        assert len(cert['lambda'])==k
        certs.append(dict(target=cert['target'],query_count=k,interest_types=len(masks),min_exact_residual=str(minres),nonnegative_sparse_multipliers=sparse,Q_support=len(Q)))
    cones.append(dict(case=case['name'],root_path=list(root),policy_histories=len(H),true_IC_rows=len(rows),certificates=certs))
assert coords==4914 and sum(len(c['certificates'])for c in cones)==13
result=dict(scope='New independent exact correction check only, not a rerun of old generators/audits and not new primary source dispositions.',all_checks_passed=True,saved_five_budget_policies=budgets,selected_cones_path=str(selected.relative_to(REPO)),selected_cones_sha256=sha(raw),selected_cones=cones,certificates=13,exact_coordinate_residuals=4914,claim_or_done_actions=0)
(OUT/'verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(dict(all_checks_passed=True,budget_policies=len(budgets),budget_ICs=sum(r['incl_self_IC']for r in budgets),selected_certificates=13,exact_coordinates=coords),ensure_ascii=False))
