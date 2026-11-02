# 最优指派 dual 与逆 SD 共同预算的接合尝试

2026-10-24。root 指定读取 Boss10 round7 的 `parent/optimal_coordinate_initialization.md`、`transport/frozen_optimal_assignment_working.md`。随后 root 指出旧强 FOMA 反例，本稿已读旧正文并停止强桥正面研究。

**身份：未完成一般付款尝试。没有得到新的共同预算、一般福利界或合法新反例。** 未运行新的固定规模批次、LP 阴性扩样或策略搜索；下列计算是全输入代数，用于检查两种真实预算接法是否吻合，不作为已经闭合的充分桥包装。

## 1. 强 FOMA 已有合法反例，不能继续标 OPEN

旧资产

`R-a0bb57fa24044a8794bc7991918a19c6/static_matching/optimal_static_matching_counterexample.md`

给出了完整历史纯 SPE：m=4、W=47、OPT=52，唯一最优主题多重集为 (0,1,4,5)，每个冻结指派成本至少48。这正是否定

    exists optimal T: min_pi sum_i u_i(T_pi(i),B_-i)<=W.

已有独立定义级审查。它不是本轮新发现，亦不反驳 half。round7 冻结指派稿将 FOMA-EXISTS/ALL 标为未证，与这个旧资产冲突；应由上层合并状态，本分支不改他人正文。

允许继续研究的弱匹配预算是

    exists optimal T: K(T;B)<=(1+1/m)W.

其充分性来自旧已证 `OPT<=K+(1-1/m)W`；本稿没有证明该弱预算。改用它不会把原强 FOMA 的付款自动修复。

## 2. 直接把最小冻结指派 dual 送入逆 SD 的方向不吻合

固定同一个最优主题多重集及其到角色的排列。对一个最优覆盖客户 x，写

    c=c_B(x), d=c_T(x),
    t=|{i:x in B_i intersect T_i}|.

这里 d>=1，0<=t<=min(c,d)。c=0 的 fresh 客户单列处理。

冻结成本的实际交集 bonus 为

    t/[c(c+1)]                         (c>0).

所以 Hungarian 最小指派在全客户总和上倾向减小这一正交集量；它不控制 actual-fresh 客户，因为它们没有任何 H_ij bonus。

另一方面，逆 SD 第一正价为

    q^B_(i->j)(x)
      =1_(x in T_i intersect B_j minus T_j)/(d delta_i),
    delta_i=c+1-1_(x in B_i).

当 c>0 时，所有接收角色 j 的数量正好为 c-t；对每个接收角色 l，满足 x in B_l minus T_l 时，其列请求为

    H_l(x)=(1/d)[t/c+(d-t)/(c+1)]
          =(dc+t)/[dc(c+1)].                       (COL)

其余角色该客户列请求为零。因此第一正价总额是

    PB(x)=(c-t)(dc+t)/[dc(c+1)].                    (PB)

这两个式子直接从原 q^B 支持求和，没有使用或误用逐客户 IC。c=0 时 PB=0，没有零分母。

在固定 c,d 下，PB 的分子对 t 的差为

    [(c-t-1)(dc+t+1)]-[(c-t)(dc+t)]
       =c(1-d)-2t-1<0.

所以增大实际交集 t 会降低该客户的第一总正价 PB。最小冻结 bonus 与压低第一正价的方向相反。由 COL，单个实际角色的请求仍满足 H_l(x)<=1/c，但最小指派 dual 本身没有给出更强、能购买未来请求的余量。

这不是一个不可能定理：不同客户的匹配权重不同，当前 d_l=min(r_l,u_l) 也会随指派改变。尤其不能仅因总 PB 下降，就断言每个残余钱包 `R_l=2u_l-d_l-H_l` 单调增加。该计算只指出两份预算不能按名称或 dual 形式直接相加。

## 3. 真正 off-IC 已付与未付项

坐标初始化合法保留

    OPT=sum_l(d_l+H_l)+sum_i b_i,
    d_l<=u_l, H_l<=u_l,
    b_i=(r_i-u_i)_+.

root 的逐客户 CLIP 先证明源正部和不超过完整真实偏离收益，最后仅调用一次 whole-IC。因此本稿没有把每个客户源标签当成 actual 同客户钱包，也没有按客户重权使用 IC。

将未来量 b_i 接全客户 SAFE/CLIP 后，已知的是非负守恒

    sum_l Aout_l=sum_i b_i.

末偏离树可以把真实 off-IC 逐条放到对应边；它仍不提供每个 actual 角色的共同入流容量。尤其初始未来边的 `x notin B_j` 支持只在第一接收位置成立，全客户 whole-profit 重采不保留这个客户支持。不能用原源 x 的单位库存替代后续实际角色的钱包。

本轮未能将某个最优指派的 Hungarian dual、EX 最优性交换行或真实 off-IC 组合成

    Aout_l<=2u_l-d_l-H_l   for all l,

也未能证明其总量版本。总量版本代入初始化恰为 half，不能因初始化守恒就被视为已经得到。

## 4. 与 ADM 菜单的比较没有补回付款

ADM 菜单允许对固定 actual 经济路径重新选择 cap 合法可信完成；它的有限信号别名表示已经另作独立内部审查。本指派对象则冻结 actual 其它角色，不是 ADM 的一列真实完成。

因此没有合法关系允许直接用 ADM 的端点选择压低 K，或用 Hungarian dual 支付 ADM 全端点的共同查询 cap。即便已知某个真实偏离端点对当前角色 cap 在 u_i，冻结成本与该真实成本间的未来捕获税仍要由完整 off-IC 实际支付；它不因信号别名或最佳排列自动消失。

本轮到此停止未付推导，未新增另一条充分等价作为成果。可继续的真实任务仍是：给残余未来请求构造一个共同 actual cap 的通用非负支付，或为弱匹配预算给合法全历史反例。上述强 FOMA 反例的正确身份必须保留。
