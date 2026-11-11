"""Fixed-19662-point COMPLETE624 transfer, with a literal independent audit.

Only actual4/R/family0-off and the original sixteen histograms are used.
No peer discovery, feature, projection or solver module is imported.
All writes are confined to this directory; old input bytes stay frozen.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product, combinations_with_replacement
from collections import defaultdict
from functools import lru_cache
import gzip, hashlib, json, sys, time, platform, traceback

HERE = Path(__file__).resolve().parent
WS = HERE.parent
REPO = WS.parents[2]
PEER = REPO / 'research/workspaces/six-boss2-20261111-cross'
POINT = WS / 'union_augmented_lp/augmented_lp_exact.json'
OURS = WS / 'union_augmented_lp/exact_matrix.json.gz'
MATRIX = PEER / 'joint_requery/complete624_actual4_R00_v1_matrix.json.gz'
MAP = PEER / 'joint_requery/complete624_actual4_R00_v1_mapping.json'
PINS = {
    POINT: 'b0ca65cfe61e5e3ef09537cba2a986c171aeaa7106f673077f803c80ee2b68e3',
    OURS: '99253e05bfe4c5705619777a5989ec9fab5c38dc7e56f934bbe8d9c071040ded',
    MATRIX: '556c3cac51e87a699d1f3a9c427f556836932b6fc2399fa330f375c6efd8231a',
    MAP: '24a601ebc1e2f7dc5e175bca453a5ab05433e046dfc7c2a782e830849817d109',
}
STATES = tuple(product((0, 1), repeat=2))
HIDDEN = tuple(product((0, 1), repeat=4))
WORDS = tuple(product((0, 1), repeat=3))

def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def canon(value): return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
def read(path):
    with (gzip.open(path, 'rt', encoding='utf-8') if path.suffix == '.gz' else path.open(encoding='utf-8')) as f:
        return json.load(f)
def write(name, value):
    p = HERE/name
    assert not p.exists(), p
    p.write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n')
    return p
def pay(n, d):
    assert d or not n
    return F(n, d) if n else F(0)
def sparse(d): return [[j, str(v)] for j, v in sorted(d.items()) if v]

def feature_names():
    names = ['sourceT', 'sourceC']
    names += [kind+':'+label for label in ('b','c','j','v','s','ss') for kind in ('price','cap')]
    for kind, labels in [('last1','tbjv'),('last2','tbcj'),('safeB','tcjv'),('safeJ','tbcv')]:
        names += [kind+':'+label for label in labels]
        names += [kind+':q'+str(q) for q in range(17)]
    for br in (1,2):
        names += [f'pair{br}:{a},{b}' for a,b in combinations_with_replacement(('t','b','c','j','v'),2)]
        for q in range(17):
            names += [f'pair{br}:q{q},{label}' for label in ('t','b','c','j','v')]
            names += [f'pair{br}:q{q},q{q}']
        for a in range(14):
            names += [f'oldpair{br}:{a},{b}:product' for b in range(a+1,17)]
        for a in range(14,17):
            for b in range(a+1,17):
                names += [f'oldpair{br}:{a},{b}:same', f'oldpair{br}:{a},{b}:off']
            names += [f'oldpair{br}:{a},{a}:off']
    names += [node+':'+label for node in ('priorR','priorZ') for label in 'bcjv']
    assert len(names)==len(set(names))==624
    return set(names)

def samples_for(actual, words, i, j, rz):
    assert i != j
    remain = [k for k in range(6) if k not in (i,j)]
    samples = tuple((q,) for q in actual+words[i]+words[j]+rz)
    samples += tuple(tuple(words[k][f] for k in remain) for f in range(3))
    means = tuple(sum(s, F(0))/len(s) for s in samples)
    moments = tuple(F(sum(words[k][f]*words[k][g] for k in remain),4) for f,g in ((0,1),(0,2),(1,2)))
    return samples, means, moments

@lru_cache(None)
def overlaps(samples, name):
    _, pair, mode = name.split(':')
    i,j = map(int,pair.split(','))
    xs,ys = samples[i],samples[j]
    if mode=='product':
        assert i<14 and i<j
        pairs = tuple(product(xs,ys))
    elif mode=='same':
        assert 14<=i<j<17
        pairs=tuple(zip(xs,ys))
    else:
        assert mode=='off' and 14<=i<=j<17
        pairs=tuple((x,y) for a,x in enumerate(xs) for b,y in enumerate(ys) if a!=b)
    return F(sum(x*y for x,y in pairs),len(pairs))

def values(names, actual, samples, h):
    """Direct true-history denominators; old-query overlap is literal sampling."""
    q=tuple(sum(s,F(0))/len(s) for s in samples)
    p,ell=sum(actual[:3]),sum(actual[:5])
    r,z=q[12],q[13]
    b,c,j,v=map(F,h)
    u=dict(t=r,b=b,c=c,j=j,v=v,s=F(0),ss=F(0))
    u.update({f'q{i}':a for i,a in enumerate(q)})
    beta1,beta2=p+r,p+c
    den1,den2=beta1+b+c,beta2+j+v
    common={
        'sourceT':pay(r,den1), 'sourceC':pay(c,den2),
    }
    answer=[]
    for name in names:
        if name in common:
            e=common[name]
        else:
            kind,label=name.split(':',1)
            if kind=='price': e=u[label]/(ell+1)
            elif kind=='cap': e=u[label]
            elif kind=='last1': e=u[label]/(beta1+b+1)-pay(c,den1)
            elif kind=='last2': e=u[label]/(beta2+j+1)-pay(v,den2)
            elif kind=='safeB': e=u[label]/(beta1+2)-pay(b,den1)
            elif kind=='safeJ': e=u[label]/(beta2+2)-pay(j,den2)
            elif kind in ('pair1','pair2','oldpair1','oldpair2'):
                if kind.startswith('old'):
                    ij,mode=label.split(':')
                    ii,jj=map(int,ij.split(','))
                    xx,yy,rho=q[ii],q[jj],overlaps(samples,name)
                else:
                    xxname,yyname=label.split(',')
                    xx,yy=u[xxname],u[yyname]
                    rho=xx if xxname==yyname else xx*yy
                beta,first,last,den=(beta1,b,c,den1) if kind.endswith('1') else (beta2,j,v,den2)
                e=(xx+yy)/(beta+1)-(rho+first)/((beta+1)*(beta+2))-pay(first+last,den)
            elif kind=='priorR':
                beta=p+q[6]+q[10]
                e=u[label]/(beta+1)-pay(r,beta+r)
            elif kind=='priorZ':
                beta=sum(actual[:4])+r
                e=u[label]/(beta+1)-pay(z,beta+z)
            else: raise AssertionError(name)
        answer.append(e)
    return answer

def budget_coefficients(name):
    if name in ('sourceT','sourceC'): return (F(1),F(0),F(0))
    if name.startswith('price:') and name[6:] in ('b','c','j','v'): return (F(0),F(1),F(0))
    if name.startswith('cap:') and name[4:] in ('b','c','j','v'): return (F(0),F(0),F(1))
    return (F(0),F(0),F(0))

def load():
    for p,s in PINS.items(): assert sha(p)==s,(p,sha(p),s)
    return read(POINT),read(OURS),read(MATRIX),read(MAP)

def audit():
    point,ours,mat,mapping=load()
    x=[F(c['weight']) for c in point['columns']]
    desc=[{k:v for k,v in c.items() if k!='weight'} for c in point['columns']]
    assert desc==ours['columns']
    assert desc[:4849]==mat['columns'][:4849]
    assert len(x)==15593 and len(ours['rows'])==19662
    assert ours['objective'][:4849]==mat['objective'][:4849]
    assert ours['normalization'][:4849]==mat['normalization'][:4849]
    assert all(F(v)==0 for v in ours['objective'][4849:]+ours['normalization'][4849:])
    assert all(F(v)==0 for v in mat['objective'][4849:]+mat['normalization'][4849:])
    W=sum(F(c)*v for c,v in zip(ours['objective'],x))
    O=sum(F(c)*v for c,v in zip(ours['normalization'],x))
    assert W==F(point['W']) and O==1
    names=[r['feature_name'] for r in mat['rows'][12042:]]
    assert set(names)==feature_names() and len(names)==624
    saved=[{} for _ in range(4992)]
    old=[]
    for ri,row in enumerate(mat['rows'][12042:]):
        assert row['index']==12042+ri and row['name']=='macro624:budget:'+names[ri]
        assert row['nonzero']==sorted(row['nonzero']) and len({j for j,v in row['nonzero']})==len(row['nonzero'])
        d={}
        for col,value in row['nonzero']:
            if col<4849:d[col]=F(value)
            else:
                assert col>=7639
                saved[col-7639][ri]=F(value)
        old.append(d)
    blocks={}
    for col,c in enumerate(desc[:4849]):
        if c['kind']=='hist':
            hist=col;blocks[hist]={'desc':c,'groups':{}}
        elif c['kind']=='joint-reply' and c['group'][:2]==[0,0]:
            key=(tuple(c['group'][2]),tuple(c['group'][3]))
            blocks[hist]['groups'].setdefault(key,{})[tuple(c['state'])]=col
    assert len(blocks)==16
    actual=[sum(x[col]*pay(int(b['desc']['actual_bits'][i]),sum(map(int,b['desc']['actual_bits']))) for col,b in blocks.items()) for i in range(6)]
    budgets=[]
    for i,name in enumerate(names):
        su,up,cap=budget_coefficients(name)
        expected={0:cap} if cap else {}
        for hist,block in blocks.items():
            a=tuple(map(int,block['desc']['actual_bits']))
            v=su*pay(a[3],sum(a))+up*pay(a[5],sum(a))
            if v:expected[hist]=v
        assert expected==old[i],name
        budget=su*actual[3]+up*actual[5]+cap*x[0]
        budgets.append(budget)
        assert budget==sum(x[col]*v for col,v in old[i].items())
        assert mapping['budgets'][i]['external_coefficients']=={'u4':str(su),'u6':str(up),'K':str(cap)}
    geometry=[];literal_pairs=0;checks=0
    for hist,block in blocks.items():
        a=tuple(map(int,block['desc']['actual_bits']))
        words=tuple(w for w,n in zip(WORDS,block['desc']['hist']) for _ in range(n))
        assert len(words)==6
        pairs=defaultdict(list)
        for i in range(6):
            for j in range(6):
                if i!=j:pairs[words[i],words[j]].append((i,j))
        assert set(pairs)==set(block['groups']) and sum(map(len,pairs.values()))==30
        for key in sorted(pairs):
            gi=len(geometry)//4
            rec=mapping['groups'][gi]
            assert rec['group_index']==gi and rec['hist_column']==hist
            assert rec['group']==[0,0,list(key[0]),list(key[1])]
            assert rec['literal_index_pairs']==[list(p) for p in pairs[key]]
            omega=F(len(pairs[key]),30)
            assert F(rec['orbit_weight'])==omega
            stcols=block['groups'][key]
            assert set(stcols)=={(0,1),(1,0),(1,1)}
            for si,rz in enumerate(STATES):
                st=rec['states'][si]
                m={hist:F(1),**{col:F(-1) for col in stcols.values()}} if rz==(0,0) else {stcols[rz]:F(1)}
                mass=sum(x[col]*v for col,v in m.items())
                assert mass>=0
                ss,qs,mom=samples_for(a,words,*pairs[key][0],rz)
                for i,j in pairs[key]:
                    assert samples_for(a,words,i,j,rz)==(ss,qs,mom)
                    literal_pairs+=1
                assert st['old_marginal_affine']==sparse(m)
                assert st['visible']=={'p':sum(a[:3]),'ell':sum(a[:5]),'t':rz[0],'queries':list(map(str,qs)),'moments':list(map(str,mom))}
                cols=list(range(7639+64*gi+16*si,7639+64*gi+16*si+16))
                assert st['hidden_columns']==cols
                erow=11418+8*gi+2*si
                eq={col:F(1) for col in cols}
                eq.update({col:-v for col,v in m.items()})
                assert mat['rows'][erow]['nonzero']==sparse(eq)
                assert mat['rows'][erow+1]['nonzero']==sparse({col:-v for col,v in eq.items()})
                for hi,h in enumerate(HIDDEN):
                    col=cols[hi]
                    d=mat['columns'][col]
                    assert d['hist_column']==hist and d['group']==rec['group'] and d['state']==list(rz) and d['macro_hidden']==list(h)
                    ev=values(names,a,ss,h)
                    for fi,e in enumerate(ev):
                        assert -omega*e==saved[col-7639].get(fi,F(0)),(col,names[fi],e)
                    checks+=624
                geometry.append({'cell':len(geometry),'group':gi,'hist_column':hist,'state':list(rz),'mass':str(mass),'old_marginal_affine':sparse(m),'omega':str(omega),'actual':list(a),'samples':[list(s) for s in ss],'hidden_columns':cols})
    assert checks==3115008 and literal_pairs==1920 and len(geometry)==312
    fixed={'point_sha256':sha(POINT),'matrix_sha256':sha(MATRIX),'original4849_coordinates':list(map(str,x[:4849])),'objective_original4849':ours['objective'][:4849],'normalization_original4849':ours['normalization'][:4849], 'actual_utilities':list(map(str,actual)),'K':str(x[0]),'W':str(W),'O':str(O),'names':names,'budgets':list(map(str,budgets)),'cells':geometry}
    write('fixed_problem.json',fixed)
    report={'status':'PASS','inputs':[{ 'path':str(p.relative_to(REPO)), 'sha256':s} for p,s in PINS.items()], 'entire_original4849_descriptors_equal':True,'entire_original4849_objective_equal':True,'entire_original4849_normalization_equal':True,'our10744_auxiliary_coefficients_zero':True,'marginal_equalities_checked':312,'hidden_variables':4992,'feature_coefficients_independently_rebuilt':checks,'literal_ordered_pair_checks':literal_pairs,'budget_rows_independently_rebuilt':624,'original_zero_histograms_retained':sum(x[h]==0 for h in blocks),'zero_RZ_marginals_retained':sum(F(c['mass'])==0 for c in geometry),'W':str(W),'O':str(O),'actual_utilities':list(map(str,actual)),'K':str(x[0]),'optimizer_calls':0,'scope':'fixed16 hist, actual4/R/family0-off only; no 17th padding hist; no full SPE claim'}
    write('contract_audit.json',report)
    print(json.dumps(report,ensure_ascii=False),flush=True)

def solve():
    import numpy as np
    import scipy
    from scipy.optimize import linprog
    from scipy.sparse import coo_matrix
    fixed=read(HERE/'fixed_problem.json')
    assert read(HERE/'contract_audit.json')['status']=='PASS'
    for p,s in PINS.items(): assert sha(p)==s
    mat=read(MATRIX)
    rr=[];cc=[];vv=[]
    for i,row in enumerate(mat['rows'][12042:]):
        for col,value in row['nonzero']:
            if col>=7639:
                rr.append(i);cc.append(col-7639);vv.append(-float(F(value)))
        rr.append(i);cc.append(4992);vv.append(-1.0)
    A=coo_matrix((vv,(rr,cc)),shape=(624,4993)).tocsr()
    eq=coo_matrix((np.ones(4992),(np.repeat(np.arange(312),16),np.arange(4992))),shape=(312,4993)).tocsr()
    b=np.array([float(F(v)) for v in fixed['budgets']])
    m=np.array([float(F(c['mass'])) for c in fixed['cells']])
    objective=np.zeros(4993);objective[-1]=1
    options={'primal_feasibility_tolerance':1e-10,'dual_feasibility_tolerance':1e-10,'ipm_optimality_tolerance':1e-12,'time_limit':120}
    t0=time.monotonic()
    res=linprog(objective,A_ub=A,b_ub=b,A_eq=eq,b_eq=m,bounds=(0,None),method='highs-ds',options=options)
    arrays={'A_data':A.data,'A_indices':A.indices,'A_indptr':A.indptr,'A_shape':A.shape,'eq_data':eq.data,'eq_indices':eq.indices,'eq_indptr':eq.indptr,'eq_shape':eq.shape,'b':b,'m':m,'objective':objective}
    if res.success:
        arrays.update(x=res.x,ineq_residual=res.ineqlin.residual,ineq_dual=res.ineqlin.marginals,eq_residual=res.eqlin.residual,eq_dual=res.eqlin.marginals,lower_residual=res.lower.residual,lower_dual=res.lower.marginals)
    p=HERE/'phase1_raw_arrays.npz';assert not p.exists();np.savez_compressed(p,**arrays)
    report={'status':int(res.status),'success':bool(res.success),'message':str(res.message),'method':'highs-ds','options':options,'phase1_objective':float(res.fun) if res.success else None,'optimizer_calls':1,'fixed_hidden_variable_count':4992,'all_marginal_equalities':312,'all_budget_rows':624,'numerical_seconds':time.monotonic()-t0,'numpy':np.__version__,'scipy':scipy.__version__,'point_sha256':sha(POINT),'matrix_sha256':sha(MATRIX),'raw_arrays_sha256':sha(p),'positive_hidden_float':int(sum(res.x[:4992]>1e-10)) if res.success else None,'scope':'numerical discovery only; exact certificate follows'}
    write('phase1_result.json',report)
    print(json.dumps(report,ensure_ascii=False),flush=True)

if __name__=='__main__':
    stage=sys.argv[1]
    receipt={'argv':[sys.executable,*sys.argv],'cwd':str(Path.cwd()),'python':platform.python_version(),'stage':stage,'script_sha256':sha(Path(__file__)),'started_utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())}
    started=time.monotonic()
    try:
        globals()[stage]()
        receipt['status']='SUCCESS'
    except BaseException as e:
        receipt['status']='FAILED';receipt['error']=repr(e);receipt['traceback']=traceback.format_exc()
        raise
    finally:
        receipt['elapsed_seconds']=time.monotonic()-started
        write('execution_'+stage+'.json',receipt)
