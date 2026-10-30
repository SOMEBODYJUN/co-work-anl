#!/usr/bin/env python3
"""线性次数全状态下界的乘积前沿精确审计。

按实际资源使用者与偏离后负载，独立核验小输入的前后端点、任意相位
light费用上界、返回窗口奇偶方向和缺陷计数；以精确幂和核验实际族的
有限参数，并以整数运算核验大参数的时钟次数预算。所有运算均为
Fraction或任意精度整数；有限审计不替代任意参数和全部状态的一般证明。

输入参数、实际命令、代码与输入SHA256、Python版本均记录在输出中。
未采用随机过程，seed为null；指定输出必须不存在，禁止覆盖冻结证据。
"""
from fractions import Fraction as F
from math import comb
from pathlib import Path
import argparse, hashlib, json, platform, shlex, sys
sys.set_int_max_str_digits(0)

def bit(N,x,j):
    x%=2*N
    return int(j<x) if x<N else int(j>=x-N)

def pairs(m,N,a,b,K,o):
    out=[]
    for j in range(N):
        h=j*m+a; row=[(h,0)]
        for k in range(K):
            v=(j+k)%N;u=v*m+b
            row.append((u,int(u>h)^int(o<0)))
        out.append(row)
    return out

def literal(N,m,w,p,test,phases,u):
    s=[bit(N,phases[a],j) for j in range(N) for a in range(m)]
    old=new=F()
    for row in pairs(m,N,*test):
        sg=dict(row)
        if u not in sg:continue
        sides={v:s[v]^ph for v,ph in row}
        loads=[sum((w[v%m] for v,z in sides.items() if z==side),F()) for side in (0,1)]
        side=sides[u]
        old+=loads[side]**p
        new+=(loads[1-side]+w[u%m])**p
    return old,new

def expected_light(N,p,wa,wb,a,b,K,o,r):
    old=new=F();es=[]
    for k in range(K):
        h=(-k)%N;sig=int(b>h*3+a)^int(o<0)
        e=int(bit(N,r,h)==sig);es.append(e)
        old+=((K-k)*wb+wa*e)**p
        new+=((k+1)*wb+wa*(1-e))**p
    return old,new,es

def literal_audit(config):
    count=0;returns=0;outside=0
    m=config["classes"]
    assert m==3
    assert config["window_rule"]=="all integers 1 <= Q < N"
    for N in range(config["N_min"],config["N_max"]+1):
      for Q in range(1,N):
        w=[F(1),F(1,Q),F(1,Q*Q)]
        for p in config["degrees"]:
          X=sum(((1+F(r,Q))**p for r in range(1,Q+1)),F())
          for r in range(2*N):
            n=Q-min(r,Q) if r<=N else min(r-N,Q)
            fo=((1+F(n,Q))**p,(2-F(n,Q))**p)
            assert literal(N,m,w,p,(0,1,Q,-1),(0,r,0),0)==fo
            nb=Q-min((r+1)%(2*N),Q) if (r+1)%(2*N)<=N else min((r+1)%(2*N)-N,Q)
            ba=((2-F(nb,Q))**p,(1+F(nb,Q))**p)
            assert literal(N,m,w,p,(0,1,Q,-1),(0,r,0),(N-1)*m)==ba
            if not (0<=r<=Q or N<=r<=N+Q):
                assert fo==(F(2)**p,F(1)) or ba==(F(2)**p,F(1))
                outside+=1
            for direction in (0,1):
                u=(N-1)*m+1 if direction else 1
                old,new=literal(N,m,w,p,(0,1,Q,-1),(r,0,0),u)
                assert old<=X and new<=X
                count+=1
            # Full-window return light, no imported endpoint table.
            eps=w[2];U=sum(((1+j*eps)**p for j in range(1,N+1)),F());V=sum(((j*eps)**p for j in range(1,N+1)),F())
            O,Qv,es=expected_light(N,p,F(1),eps,0,2,N,+1,r)
            assert literal(N,m,w,p,(0,2,N,+1),(r,0,0),2)==(O,Qv)
            Ob,Qb,eb=expected_light(N,p,F(1),eps,0,2,N,+1,(r+1)%(2*N))
            assert literal(N,m,w,p,(0,2,N,+1),(r,0,0),(N-1)*m+2)==(Qb,Ob)
            returns+=2
          # Every near-return parity and T, including zero and largest T.
          alpha=F(config["near_defect_alpha"]);eps=w[2];W=(1+N*eps)**p
          U=sum(((1+j*eps)**p for j in range(1,N+1)),F());V=sum(((j*eps)**p for j in range(1,N+1)),F());Z=U-alpha*V
          for T in range(N):
            for parity in (0,1):
              r=(-parity*N-T)%(2*N)
              if parity==0:
                old,new,es=expected_light(N,p,F(1),eps,0,2,N,1,r)
                assert es.count(0)<=T+1
                assert literal(N,m,w,p,(0,2,N,1),(r,0,0),2)==(old,new)
              else:
                new,old,es=expected_light(N,p,F(1),eps,0,2,N,1,(r+1)%(2*N))
                assert es.count(1)<=T+1
                assert literal(N,m,w,p,(0,2,N,1),(r,0,0),(N-1)*m+2)==(old,new)
              assert old-alpha*new>=Z-(alpha+1)*(T+1)*W
              returns+=1
    return {'literal_endpoint_bounds':count,'literal_return_costs_and_near_defects':returns,'outside_short_intervals_full_heavy_exits':outside,'scope':'Small exact input families only; formula proof remains necessary.'}

def psums(n,p):
    ss=[n]
    for k in range(1,p+1):
        num=(n+1)**(k+1)-1-sum(comb(k+1,j)*ss[j] for j in range(k))
        assert num%(k+1)==0
        ss.append(num//(k+1))
    return ss

def shifted(n,t,p):
    ss=psums(n,p)
    return sum((F(comb(p,k)*ss[k])*t**k for k in range(p+1)),F()),F(ss[p])*t**p

def healthy_constants(p):
    alpha=F(p,10);Q=p**4;m=2
    while 2**(m-1)<p*p:m+=1
    N=p**(4*m-5);eps=F(1,Q**(m-1))
    H=F(2**p)-alpha;X,Y=shifted(Q,F(1,Q),p);L=alpha*X-Y
    U,V=shifted(N,eps,p);W=(1+F(1,p))**p;J=alpha*W-1;Z=U-alpha*V
    Aprev=(2*L/H)**(m-2);AR=H/(2*J)
    assert N*eps==F(1,p) and m<=p and N>=p**7 and N>Q
    assert Y<=F(1,2**p)*X and W>2 and W<3 and J>3
    assert F(Q,40)*H<=L and 2*L/H>=1
    assert AR*Z>3*Aprev*L
    D0=(alpha+1)*((m-1)*Q+1)*W
    assert D0<=Z/30
    gamma0=H-alpha*AR*W
    gammain=alpha*X-2*Y
    gammaret=AR*(Z-D0)-alpha*Aprev*X
    assert gamma0>H/3 and gammain>H/2 and gammaret>H/2
    # Exact sufficient clock degree; no logs used.
    B=m*Q**(m-1)*2**p;eta=H/4;Lc=comb(N-1,2)
    threshold=eta/(4*alpha*alpha*B*Lc)
    D=1
    while F(2,3)**D>threshold:D+=1
    return {'p':p,'m':m,'Q':Q,'N_decimal_digits':len(str(N)),'clock_D_exact_budget':D,'degree_max_p_D':max(p,D),'all_fraction_constant_assertions':True,'front_margin_guarantee':'H/4','scope':'Exact scalar comparisons, not whole front enumeration.'}

def large_clock_budget(p):
    """整数验证 8m p^(12ell) 2^p <= 45 3^p，避免百万次幂和。"""
    ell=1
    while 2**ell<p*p:ell+=1
    m=ell+1
    lhs=8*m*p**(12*ell)*2**p
    rhs=45*3**p
    assert lhs<=rhs
    return {"p":p,"ell":ell,"m":m,
            "inequality":"8*m*p**(12*ell)*2**p <= 45*3**p",
            "integer_budget_passed":True,
            "lhs_bit_length":lhs.bit_length(),"rhs_bit_length":rhs.bit_length(),
            "Faulhaber_at_this_p":False,
            "scope":"Exact clock-budget majorant only; not full-state enumeration."}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input",type=Path,required=True,help="实际JSON参数输入")
    parser.add_argument("--output",type=Path,required=True,help="新JSON结果；拒绝覆盖")
    args=parser.parse_args()
    if args.output.exists():
        parser.error(f"refusing to overwrite existing output: {args.output}")
    raw=args.input.read_bytes()
    config=json.loads(raw)
    assert config["schema_version"]==1
    out={"status":"all exact assertions passed",
         "metadata":{"python":platform.python_version(),
                     "source_path":str(Path(__file__).resolve()),
                     "source_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                     "input_path":str(args.input.resolve()),
                     "input_sha256":hashlib.sha256(raw).hexdigest(),
                     "command":shlex.join([sys.executable,*sys.argv]),
                     "precision":"exact Fraction and arbitrary-precision integer arithmetic; no floats",
                     "seed":None,"randomness":"none"},
         "literal":literal_audit(config["literal"]),
         "healthy_constants":[healthy_constants(p) for p in config["actual_family_degrees"]],
         "large_clock_budgets":[large_clock_budget(p) for p in config["large_clock_budget_degrees"]],
         "scope":"Finite exact audits of formulas and scalar budgets only. General all-state theorem is proved in the manuscript."}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    with args.output.open("x",encoding="utf-8") as f:
        json.dump(out,f,ensure_ascii=False,indent=2)
        f.write("\n")
    print(json.dumps({"status":out["status"],"output":str(args.output),
                      "literal":out["literal"],
                      "actual_family_degrees":config["actual_family_degrees"],
                      "large_clock_budget_degrees":config["large_clock_budget_degrees"]},ensure_ascii=False))


if __name__=="__main__":
    main()
