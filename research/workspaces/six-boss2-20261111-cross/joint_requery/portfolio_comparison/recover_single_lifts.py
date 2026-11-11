"""Recover exact single-Q hidden lifts at the fixed actual-signature point.

QR only selects a square candidate subsystem. Fraction elimination, all mass
equalities, nonnegativity and every one of the 76 rows certify the result.
"""
from pathlib import Path
from fractions import Fraction as F
import sys,json,hashlib,time
import numpy as np
from scipy.linalg import qr

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent))
import portfolio_master as portfolio
from explore_projection import solve,ALL_NAMES,features
from separate_master import blocks_from_columns
from compare_5744 import single_visible


def square_solve(A,b):
    M=[list(row)+[rhs] for row,rhs in zip(A,b)];n=len(M)
    assert all(len(row)==n+1 for row in M)
    for col in range(n):
        choices=[i for i in range(col,n) if M[i][col]]
        if not choices:raise ValueError('singular rational subsystem')
        pivot=min(choices,key=lambda i:M[i][col].numerator.bit_length()+M[i][col].denominator.bit_length())
        M[col],M[pivot]=M[pivot],M[col]
        pc=M[col][col]
        for j in range(col,n+1):M[col][j]/=pc
        for row in range(col+1,n):
            if not M[row][col]:continue
            f=M[row][col]
            M[row][col]=F(0)
            for j in range(col+1,n+1):M[row][j]-=f*M[col][j]
    x=[F(0)]*n
    for i in range(n-1,-1,-1):x[i]=M[i][-1]-sum(M[i][j]*x[j] for j in range(i+1,n))
    return x


def recover(res,columns,visible,u,K,k,r_actual):
    support=[ci for ci,x in enumerate(res.x) if x>1e-10]
    assert len(columns) in support
    fslist=[]
    for ci in support:
        if ci==len(columns):fslist.append(None);continue
        vi,h=columns[ci];p,ell,t,q,_=visible[vi]
        if len(h)==4:h=(*h,0,0)
        fs,bud=features(p,ell,t,q,*h,k);fslist.append(fs)
    _,bud=features(0,0,0,F(0),0,0,0,0,0,0,k)
    equations=[];rhs=[];labels=[]
    for vi,state in enumerate(visible):
        equations.append([F(int(ci!=len(columns) and columns[ci][0]==vi)) for ci in support]);rhs.append(state[-1]);labels.append('mass:'+str(vi))
    for ni,name in enumerate(ALL_NAMES):
        if res.ineqlin.residual[ni]>1e-8:continue
        equations.append([F(-bud[name][0]) if ci==len(columns) else fs[name] for ci,fs in zip(support,fslist)])
        rhs.append(bud[name][1]*u+bud[name][2]*K);labels.append(name)
    Af=np.asarray(equations,dtype=float)
    _,R,pivots=qr(Af.T,pivoting=True,mode='economic')
    rank=int(sum(abs(R[i,i])>1e-10 for i in range(min(R.shape))))
    assert rank==len(support),(rank,len(support))
    selected=list(map(int,pivots[:len(support)]))
    exact=square_solve([equations[i] for i in selected],[rhs[i] for i in selected])
    assert min(exact)>=0
    r_min=exact[support.index(len(columns))]
    # The recovered optimum need not be proved optimal for the present goal:
    # a feasible witness at r_min <= r_actual suffices for every single-Q row.
    assert r_min<=r_actual,(r_min-r_actual,float(r_min-r_actual))
    masses=[F(0)]*len(visible);sums={n:F(0) for n in ALL_NAMES};records=[]
    for ci,fs,w in zip(support,fslist,exact):
        if ci==len(columns) or not w:continue
        vi,h=columns[ci];masses[vi]+=w
        for n in ALL_NAMES:sums[n]+=w*fs[n]
        records.append({'visible':vi,'hidden':list(h),'mass':str(w)})
    assert masses==[v[-1] for v in visible]
    slacks={n:bud[n][0]*r_actual+bud[n][1]*u+bud[n][2]*K-sums[n] for n in ALL_NAMES}
    assert min(slacks.values())>=0
    # Also verify the recovered r_min itself is feasible, without trusting QR.
    assert min(bud[n][0]*r_min+bud[n][1]*u+bud[n][2]*K-sums[n] for n in ALL_NAMES)>=0
    return {'r_recovered_feasible':str(r_min),'r_actual_minus_recovered':str(r_actual-r_min),'support':records,'selected_equation_labels':[labels[i] for i in selected],'all_76_slacks_at_actual':{n:str(x) for n,x in slacks.items()},'minimum_slack_at_actual':str(min(slacks.values())),'mass_equalities_exact':True,'nonnegative_masses_exact':True}


def main():
    started=time.monotonic();i=3;member=0;orb=(0,0)
    if len(sys.argv)>1:orb=tuple(map(int,sys.argv[1].split(',')))
    package=json.loads((HERE.parent/'portfolio_selected_5744.json').read_text());raw=Path(package['source_path']).read_bytes();assert hashlib.sha256(raw).hexdigest()==package['source_sha256']
    blocks=blocks_from_columns(json.loads(raw)['columns']);actual=list(map(F,package['actual_utilities']));r=actual[i];u=actual[5];K=F(package['K']);k=6-i
    joint=portfolio.visible_distribution(blocks,member,orb,i)
    newcut=next(c for c in package['cuts'] if c['i']==i and c['member']==member and tuple(c['orb'])==orb)
    target=HERE/f"exact_single_lifts_5744_i{i}_m{member}_orb{orb[0]}{orb[1]}.json"
    out={'scope':'All 17 single-Q 76-row projected cones are exactly feasible at one fixed actual-signature visible distribution, while its joint 332-row cut is strictly negative. This is a projection separation, not an SPE.','source_path':package['source_path'],'source_sha256':package['source_sha256'],'i':i,'k':k,'member':member,'orb':orb,'r_actual':str(r),'u6':str(u),'K':str(K),'query_menu':package['query_menu'],'joint_negative_slack':newcut['exact_slack'],'joint_row_sha256':newcut['row_sha256'],'queries':[]}
    for qi in range(17):
        visible=single_visible(joint,qi);res,columns,names=solve(visible,u,K,ALL_NAMES,k);assert res.success
        restored=recover(res,columns,visible,u,K,k,r);restored.update({'query':qi,'label':package['query_menu'][qi],'visible':[{'state':[p,ell,t,str(q)],'mass':str(w)} for p,ell,t,q,w in visible]})
        out['queries'].append(restored);out['elapsed_seconds']=time.monotonic()-started;target.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
        print(json.dumps({'query':qi,'support':len(restored['support']),'minimum_slack':restored['minimum_slack_at_actual'],'margin_float':float(F(restored['r_actual_minus_recovered']))}),flush=True)
    out['status']='PASS';out['all_queries_exactly_feasible']=True;out['exact_old_row_checks']=17*len(ALL_NAMES);out['elapsed_seconds']=time.monotonic()-started;target.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
    print('PASS',target,out['elapsed_seconds'])


if __name__=='__main__':main()
