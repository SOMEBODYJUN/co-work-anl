# 固定阶压缩乘法向量贪心的真实最优源反例：独立审查

## 1. 被审精确身份、冻结指针与实际审查顺序

被审正文为 `research/current/unrelated_machines/truncated_multiplication_vector_greedy_barrier.md`，精确身份为 `UM-TRUE-MOMENT-VECTOR-GREEDY-LINEAR-GAP-v1`。本审查覆盖其普遍合法性及 `nT` 上界、固定阶真实最优源的严格顺序无关下界、全空间投影义务和总位复杂度；不是外部同行评审，也不认证全球新颖性或独立论文价值。

初次实际读取正文的 SHA256 为：

`586072e7aecd428cc10d2e3937fb203b9cb8ed1f1bd15d0326a9f7b7f8debd43`。

审查中提出零最优值句子的承诺范围应明确，主研究者随后只将该句改为“在上述最优源承诺下，T=OPT=0时输出零负载”。最终实际核对并采用的 SHA256 为：

`78b4800ea278a61a3805f7a91aeec531078e5661cac1a4cd3a19c943c0ad9246`。

已把新句反替换为旧句并重算哈希，准确恢复初次 SHA256，故这一增量确实只有上述澄清，没有把旧审查自动套到未读的新数学改动。

内部审查者为 `conditional_probe_attack`。实际顺序是：先收到固定 V1 的向量评分规则并独立重构压缩后的容量义务；随后收到主研究者提出的三次多项式源及固定 r 推广的精确构造，但没有收到主证明推导；审查者独立推出正交分解、fresh 乘法公式、严格评分和真实源容量，完成独立有限核验后，才读取上述冻结正文。多项式源的提出来源是主研究者，不把“独立重构证明”写成独立发现该族。先前精确平局的 Hadamard 探索不承担本严格反例的证明。

**结论：在最终冻结正文的精确合同内，未发现仍成立的致命数学异议。** 下文区分一般证明审查、真实有限计算及未覆盖部分；本审查没有改动正文、算法实现或状态登记。

## 2. 普遍合法性、线性上界及零边界

源 D 是概率分布，故常数1非零。对每任务 j，所有可用选择指示之和在源上恰为1，压缩后仍有 `sum_i A_ji=I`。若当前 psi 非零，所有候选作用不可能同时为零；选择最大评分后下一向量仍非零。这也证明可选的归一化不会在实际步骤遇到零除。

零源概率的边在 L2 取商后是零函数，其算子恒零，不能被选中。因此选中边有正源概率，在某个真实 T 可行支撑态出现。处理时间非负给该边处理时间不超过 T；选择的也是原输入可用边。每任务输出恰一个机器，每机至多累加 n 项各不超过 T，得到 `C_max<=nT`。这里没有误用仅期望满足的容量：每个支撑态本来就是真实调度。

退化情形已闭合：

- n=0时不处理任务，空映射负载为0。
- T=0时，每条实际被选边的处理时间都为0。
- 单可用机器、正时间但零源概率的冗余边、零处理时间边都不引起除法或不可用输出。
- 当最优源承诺为T=OPT时，上界才可改写为n OPT；此时T=OPT=0给零负载。

审查中特别攻击了“仅OPT=0是否足够”：一个任务在两台机器时间分别为0和1，而D只使用时间1的机器、T=1时，本规则会输出负载1，虽然原实例OPT=0。故不带最优源/T=0承诺的零句不成立。最终冻结稿已明确承诺范围，§5也一直准确陈述T=0，不再有此歧义。

## 3. 全部参数上的真实源、实际最优值及标签原子

固定整数r>=1，设d=2r+1、B=2d。素数q>B确保域上d次首一多项式非零，且所有所用不同求值点存在。随机低阶系数有q^d种等权取值；首一项是固定项，不是又多一个随机系数。

每个方程f(t)=y有至多d个域中解。g把0和1合并，故普通机器0至多收到2d=B个unit任务，其他普通机器至多d个。anchor在独立专用机器上负载恰B。每个系数态因此都是makespan准确为B的合法调度；anchor对任意调度都给B的下界，所以OPT准确为B。也可直接把q个普通任务在q-1台普通机均衡到负载至多2，核对不存在额外隐藏障碍。

不同系数标签可能表示同一实际调度。推送均匀系数测度并合并重复调度后，所有指示函数的内积不变，故Vr及其压缩作用不变；不能把标签个数说成互异调度数。正文已准确区分。

对任意h<=d个不同点，前h个低阶系数的求值矩阵是非奇异Vandermonde矩阵；其余d-h个系数固定后，每个目标求值向量有唯一前h系数。因此每个目标共有q^(d-h)个原像。逐坐标施加g给真正的d重独立分类变量，普通机边际为2/q、1/q、...、1/q，全部严格正。整个源是实际有限分布，所有更高阶矩同时存在且来自同一源，不是仅拟合的低阶抽象算子。

## 4. 对全Vr的投影、未来特征和商空间

令W_j为单任务零均值分类函数空间。每个单任务函数可分为常数和W_j，所以Vr由各个W_S（不同任务零均值函数的乘积）张成。两块的内积最多涉及2r个不同任务；索引集不同时存在一个只出现一次的零均值因子，独立性使内积为零。同块Gram是各单任务正定Gram的张量积，边际严格正使其非退化。因此正文式(5)确实是取L2零范数商之后的正交直和，没有靠形式多项式维数忽略额外零空间。

设fresh任务j未处理，psi只使用已处理任务。写psi=u+v，u为次数小于r的部分，v为纯r次部分。对h=x_ji-p：

\[
P_r(hv)=0,\qquad A_{ji}\psi=p\psi+hu.
\]

关键检查是测试整个Vr，而不只测试过去特征。取v中r个过去任务的乘积，再乘fresh h，共r+1个零均值任务块；任意Vr测试项最多覆盖其中r个，必有一个块未被覆盖。即使测试项包含任意未来任务，联合范围仍至多2r+1个任务，故期望为零。给定的2r+1重独立确实足够；只用2r重独立不能免费完成这个最终正交检查。

hu属于Vr，且只引入fresh任务本身，不引入任何未来特征。因此对任意已处理集合、任意下一fresh任务，该表示都可继续归纳；自适应选择任务顺序也不能避开它。

独立性又给psi与hu正交，以及 `||hu||^2=p(1-p)||u||^2`。所以

\[
\|A_{ji}\psi\|^2=p\|u\|^2+p^2\|v\|^2.
\]

本式由压缩后的真实范数得出，没有把未投影乘法的范数误当成评分。非零psi使右式在p>0上严格递增；迭代常数分量更明确地每次乘正概率，因此始终为正。取p0=2/q、p1=1/q，评分差准确为 `||u||^2/q+3||v||^2/q^2>0`。

故每个普通任务都唯一选择普通机0，完全不依赖平局规则。anchor的唯一选择指示恒1，其压缩是恒等算子，插在任意位置均无作用。q>B使最终makespan恰q，近似比准确为q/B。量词是每个固定r、所有素数q>B、同一实例的所有任务顺序；有限检查没有被拿来代替这个全称归纳。

正文闭式(12)也已独立重构：对已处理集合F，保留真实条件乘积展开的所有次数<=r项；新一步只删最高r+1次项。不同ANOVA块正交给范数的二项式求和。这个闭式与全空间投影证明是两项不同的检查，不能只核闭式而省略未来测试义务。

## 5. 固定阶总位复杂度及不能外推的量词

给定显式精确有理矩时，固定r的候选单项式数是输入选择数的固定次多项式。Gram内积最高2r阶，作用内积最高2r+1阶。真实源承诺使Gram半正定；可用精确有理消元选择非退化主子基，在同一个固定基中解所有作用方程。无须用可能含无理数的正交归一化算法。

有理消元的分母与分子位长受输入整数化矩阵的行列式界控制，是矩阵显式总位长的多项式。选择阶段只有n次更新；可给每个固定作用矩阵清共同分母，n次矩阵乘法的分母位长按所乘矩阵编码长度累加，分子再增加矩阵维数的对数项。故这是总位多项式，不是只说每次算术操作多项式。数学上不必归一化psi，避免引入平方根；极小但非零评分也用精确有理比较，不按浮点下溢当零。

在坏例中，固定r时q^(2r+1)个标签源及逐原子求值的规模是显式调度矩阵规模的多项式，次数允许依赖这个已固定的r。给出更高阶完整真实矩不会自动把压缩空间从Vr提高到别的阶数。r随输入增长时，正文没有声称同一个统一多项式次数；本审查也没有增加此断言。

## 6. 实际独立有限核验与未检查范围

审查者独立写了scratch程序 `vector_probe_polynomial_independent.py`，未导入规范生成器或主审计。Python为3.12.14，源、残差、范数和比较用整数及Fraction，使用isqrt作精确试除上界；没有浮点容差。随机seed=20261017只用于选择第三种任务顺序，系数源本身是完整枚举，不是随机采样。

每组都枚举全部q^(2r+1)个系数态，核每个源态容量、anchor以及全部大小d的点集Vandermonde非零；另选三个d点集实际枚举全部求值元组并核每种恰出现一次。按正序、逆序和该seed的排列，逐步从真实源重算投影候选的范数与严格评分。

| r | q | 完整标签源原子数 | 普通机0的实际最大源负载 | 其他普通机的最大源负载 | 实际评分核验数 | 对完整V1的残差核验数 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 7 | 343 | 4 | 3 | 126 | 126 |
| 1 | 11 | 1331 | 6 | 3 | 330 | 330 |
| 1 | 13 | 2197 | 6 | 3 | 468 | 468 |
| 2 | 11 | 161051 | 7 | 5 | 330 | 0 |
| 2 | 13 | 371293 | 8 | 5 | 468 | 0 |

r=1时，每个残差均针对常数及全部任务全部普通机器指示逐项核对，包含未来任务特征，确实确定了真实投影，不是只验证过去特征。r=2时没有形成完整V2矩阵、没有有理求逆、没有对完整V2全部测试列核残差；只核实际源、有限独立性、ANOVA投影候选的实际范数及严格评分。一般投影正确性依赖第4节全空间证明。

有限运行没有穷尽全部任务排列，没有枚举r>=3的完整源，也没有把大参数公式核对伪装成实际源展开。anchor位置没有作为额外有限排列枚举；任意位置结论来自其恒等算子证明。正文正在落地的规范代码、输入及冻结JSON不是本审查脚本，本审查没有因此宣称已逐行审查或重跑它们。

以下附录保留本次独立scratch核验的完整源文本，避免仅留下“检查通过”的不可复现断言；它是审查附录，不冒充正文的规范审计入口。

## 7. 结论与剩余范围

最初零源措辞的适用范围已澄清。对最终冻结版本未发现仍成立的fatal objection；全称证明已按真实源、全Vr正交、所有顺序、退化输入及总位复杂度分别攻击。

此结果只针对固定D、固定Vr、逐任务最大化压缩后向量范数的准确贪心规则。它不证明SA、LS、SOS或配置松弛有整数间隙，不排除重建矩、真正条件化、容量反馈或直接选一个真实源支撑调度。全球新颖性、外部审稿和独立论文价值未认证。UM-TARGET-v1仍开放。

## 附录：本次独立核验完整代码

实际源码 SHA256：`7252b1f552218e451a9a3bbdf5497730c959ebfa3a9f438a4d1f207a2420fdd3`。运行命令为 `python3 vector_probe_polynomial_independent.py`；输出只到stdout，以下参数和seed与表中实际运行一致。

```python
"""Independent exact finite audit of real polynomial-schedule sources.
No project/canonical implementation is imported.  r=1 checks actual projection
residuals against every linear feature. r=2 checks the ANOVA projection formula's
actual norms and source support, with finite-field independence certificates;
it does not form the complete enormous V_2 matrix.
"""
from fractions import Fraction as F
from itertools import combinations
from math import comb, isqrt
import numpy as np

def source(q,r):
 d=2*r+1;bound=2*d
 assert q>bound and all(q%v for v in range(2,isqrt(q)+1))
 coeff=np.indices((q,)*d,dtype=np.int64).reshape(d,-1).T
 vals=np.empty((len(coeff),q),dtype=np.int64)
 for t in range(q):
  vals[:,t]=(pow(t,d,q)+sum(coeff[:,a]*pow(t,a,q) for a in range(d)))%q
 choices=np.where(vals<=1,0,vals-1)
 maxloads=[int(np.max(np.sum(choices==i,axis=1))) for i in range(q-1)]
 assert maxloads[0]<=bound and max(maxloads[1:])<=d
 assert (q+q-2)//(q-1)<=2<=bound
 # Exact invertibility of the coefficient-evaluation map for every d-point set.
 subsets=list(combinations(range(q),d))
 for S in subsets:
  det=1
  for i,a in enumerate(S):
   for b in S[i+1:]:det=det*(b-a)%q
  assert det%q
 # Actually enumerate evaluation tuples for three distinct d-point sets.
 tested=[]
 for S in (subsets[0],subsets[len(subsets)//2],subsets[-1]):
  if S in tested:continue
  tested.append(S)
  packed=np.zeros(len(coeff),dtype=np.int64)
  for a in S:packed=q*packed+vals[:,a]
  assert np.all(np.bincount(packed,minlength=q**d)==1)
 return choices, {'q':q,'r':r,'degree':d,'source_atoms':len(coeff),'source_load_max_by_machine':maxloads,'anchor_and_OPT':bound,'all_vandermonde_subsets':len(subsets),'actual_bijective_evaluation_subsets':len(tested)}

def exact_square_sum(v):
 maxval=int(np.max(np.abs(v)))
 assert len(v)*maxval**2<2**63
 return int(v@v)

def audit(q,r):
 X,report=source(q,r);N=len(X);scale=2**r;rho=F(q-2,2)
 linear=None
 if r==1:
  linear=np.column_stack([np.ones(N,dtype=np.int64)]+[(X[:,t]==i).astype(np.int64) for t in range(q) for i in range(q-1)])
 rng=np.random.default_rng(20261017)
 orders=[list(range(q)),list(reversed(range(q))),rng.permutation(q).tolist()]
 projection_checks=score_checks=0
 for order in orders:
  Es=[np.ones(N,dtype=np.int64)]+[np.zeros(N,dtype=np.int64) for _ in range(r)]
  for k,t in enumerate(order):
   state=sum(2**(r-l)*Es[l] for l in range(r+1))
   lower=sum(2**(r-l)*Es[l] for l in range(r))
   norm=F(exact_square_sum(state),N);low=F(exact_square_sum(lower),N)
   assert F(int(np.sum(state)),N)==scale
   assert norm==scale**2*sum(F(comb(k,l))*rho**l for l in range(min(k,r)+1))
   assert low==scale**2*sum(F(comb(k,l))*rho**l for l in range(min(k,r-1)+1))
   scores=[]
   for i in range(q-1):
    indicator=(X[:,t]==i).astype(np.int64);c=2 if i==0 else 1;p=F(c,q)
    projected_times_q=c*state+(q*indicator-c)*lower
    score=F(exact_square_sum(projected_times_q),q*q*N)
    assert score==p*p*(norm-low)+p*low
    scores.append(score);score_checks+=1
    if linear is not None:
     residual=q*indicator*state-projected_times_q
     assert np.all(residual@linear==0)
     projection_checks+=1
   assert scores[0]>max(scores[1:])
   newu=q*(X[:,t]==0).astype(np.int64)-2
   for l in range(r,0,-1):Es[l]=Es[l]+newu*Es[l-1]
 report.update({'ordinary_job_orders_checked':len(orders),'actual_score_comparisons':score_checks,'full_linear_projection_residual_checks':projection_checks,'full_Vr_projection_matrix_built':False,'output_loads':[q,2*(2*r+1)],'ratio':str(F(q,2*(2*r+1)))})
 return report

if __name__=='__main__':
 for q,r in [(7,1),(11,1),(13,1),(11,2),(13,2)]:print(audit(q,r),flush=True)
```

## 后续冻结增量：同行来源说明

在上述审查及附录冻结后，正文§6新增一段公屏seq252的来源说明。当前实际核对的正文SHA256为：

`3db8fd05677780e40074ddf33f5bdb64c6fefc0260f6e6396e17b25e093da4cc`。

已读取新增整段，并从当前文本中只删除该段及其段后空行，重算SHA256，准确恢复本审查先前采用的 `78b4800ea278a61a3805f7a91aeec531078e5661cac1a4cd3a19c943c0ad9246`。因此本次增量确实只涉及来源说明，原有对象、算法、量词、构造、公式、证明、复杂度及附录均没有改变；原数学审查结论在此新冻结版本仍适用。

新增段把boss2公屏较早报告的五机全unit精确2反例归于对方，同时明确小证书尚未由本文作者亲自重算、只记录同行报告且不作为本稿证明依赖。本补充也没有重算该同行证书，不能读作对其数学正确性、全球优先性或独立核验状态的再次认证。本稿独立承担的范围仍是任意固定阶、同一实例任意顺序的严格失败及线性无界族。该证据级别与来源区分没有引入新的数学异议，也没有升级主目标状态。
