# 接续结果的精确身份

共同基准：CAG-MODEL与原Q-CAG-HALF，任意目录、任意人数、单位客户/提供者、
完整有序历史纯SPE。一般half仍OPEN。以下个人资产均无外审或新颖性认证。

## B5-SPARSE-RENT-COMPLETE-SPE-NO-v1

- **Objects / quantifiers:** 对每个整数q>=2，m=2q、两客户、共同目录恰为两个互斥
  单例A/B。任意非终端有序历史计数a,b，a>=q时选B、b>=q时选A，否则任意纯历史依赖chi。
- **Exact conclusion:** 每个这样定义的完整策略均SPE。可选chi使实际路径A B^q A^(q-1)，
  W=OPT=2。对j1..q-1取I_j={q+1+j}、theta_j=1/j，Gamma=1；任意rho>0的reset租金
  总和为H_(q-1)/[(rho+1)(rho+2)]，故没有只依rho的有限常数乘Gamma W上界。
- **Dependencies / evidence:** 未满节点终局必q/q；超载节点真实遵从/偏离收益严格比较。
  作者与另一研究员独立解析全历史重构，互不导入的Fraction核验。
- **Scope / objections:** 仅否定取消连续性后相同费用的普遍预算；实际福利最优，不是half反例。
  不排除带符号运输或clock费用。[正文](coupling/sparse_slot_complete_spe_obstruction.md)、
  [独审](independent/sparse_spe_rent_review.md)。

## B5-CHRONOLOGICAL-RENT-DECOMPOSITION-v1

- **Objects / domain / quantifiers:** 任意有限实际主题路径、任意未来稀疏槽I_j、固定
  全行权theta>=0、实rho>0。b_j是前缀客户负载，b_t是实际t时的累计负载；
  a=b_j+k是该行第k个所选客户hit的局部排名，b=b_t是实际排名，因此b>=a。
- **Exact statement:** 每个旧reset租金等于clock费用加非负premium；单个所选hit的premium为
  b_j(b-a)(2rho+a+b-1)/[(rho+a-1)(rho+a)(rho+b-1)(rho+b)]。
  clock使用b_j/[(rho+b_t-1)(rho+b_t)]，不重置实际排名，任意稀疏槽下其总和仍
  <=Gamma sum_{c>0}[1/(rho+1)-1/(rho+c)]，Gamma=max_t sum_{j:t in I_j}j theta_j。
- **Evidence / scope:** 有限倒数差的精确分解与首hit零系数；作者解析，父方已独立
  展开同一系数。真实SPE稀疏族rho1的clock=1/4-1/[2q(q+1)]有界，全部发散来自premium。
  尚未从真实SPE激励产生clock项或支付premium；不是一般效率定理。[正文](coupling/chronological_sparse_rent_and_skip_premium.md)。

## B5-SIGNED-DELTA-ALL-QUERIES-NO-v1

- **Objects / definitions:** 采用上层prices/early_menu_load_defect.md的有符号delta_i(mu)，
  i遍历实际非末位，所有i使用同一个mu。旧13人36客户六主题完整纯SPE为P^10 A A B。
- **Exact conclusion:** W33、末位w3、OPT36；mu=delta_T时sum delta_i=5，严格大于
  half充分预算(W+w)/(2m)=18/13，差47/13。所有最优m主题多元组均匀mu中的最大值
  为1373/507，计数(A,B,T,D,E,P)=(1,1,1,9,0,1)，仍超预算671/507。
  因此即使限制为“任意最优比较组合”的总预算也是假。
- **Counterevidence to overreach:** 最优组合中最小值-38375/5577，于(10,1,1,0,0,1)；
  全目录均匀mu给7/132。存在有利最优组合版没有被否定。原half余量30。
- **Dependencies / evidence:** 既有完整策略输入，当前两份互不导入的真实自动机重放，
  全部27243节点112050比较，全部2002个最优计数组合与有理二次矩阵精确核验。
  [父方独审及程序](parent/signed_delta_independent_review.md)。

## B5-QUERY-OVERLAP-RESIDUAL-v1

- **Objects / quantifiers:** 代数参数d>=0、a in {0,1}、eta>=0、q,e in [0,1]、u>=0。
  令t=min{1/(d+1),1/(d+2)+eta/(d+a+1)}，
  R=q min(1,u)-u/(d+1)-eta e/(d+a+1)+ue/[(d+1)(d+2)]。
- **Exact conclusion:** R<=(q-t)_+ min(1,u)-(u-1)_+/(d+2)。u<=1由两端点仿射性，
  u>=1由斜率<=-1/(d+2)证明，不依赖有限参数枚举。
- **Application in the original model:** 任意给定完整SPE和同一查询组合z，总质量tau>=1，
  各i保留真实current slack s_i和实际末位菜单slack z_i，再扣正文的非负查询信用E_i。
  令C_G=tau sum_i s_i+(1/2)sum_{i<m}z_i，则
  m Coverage(z)<=(m+tau-1/2)W-w/2+tau sum_{i<m}delta_i-C_G-sum_i E_i。
  对某个最优组合，若右侧缺陷满足正文(6)相应含E的总支付义务，即得half；该义务未证。
- **Evidence / status / scope:** 作者解析及Fraction边界核验，另一研究员未读作者实现的
  独立两段证明、末位E公式、tau系数与总和审查通过。13人最坏重复组合的修复只是指定
  数据点，不将其提升成一般成功。[正文](prices/signed_delta_selection_boundaries.md)、
  [独审](independent/signed_delta_residual_review.md)。

## 两个静态校准的准确范围

- **Weak CCE / old weak-iid family:** 对公屏Boss2 m>=2、J>=2多花瓣真实SPE族，实际W=2m，
  profile Q_1 B^(m-1)是福利2m+1的静态PNE，故该族满足弱CCE桥。
  m>=3的更低相关占用混合给福利2m+4/[m+6+3(m-1)/J]；只是静态上界，不声称最低CCE恰等。
  [补充正文](independent/weak_cce_boss2_family.md)的解析约束及参数审计支持该结论；一般弱CCE仍OPEN。
- **POOL / same family:** 对同一个完整SPE及每个查询分布p，写a=p_A,b=p_B，
  精确池化负载给P(p)<=2-a+a(1-b)/(2m-a)<=2=W/m。
  它是整个无限族的全p解析校准，不是一般POOL或真正安全值支付定理。
  二人POOL部分只是既有末两机制的明确重构。[正文](security/pool_structural_checks.md)。

## 开放状态

最优比较组合的选择性delta预算、clock全树运输、真正安全/POOL聚合、弱CCE桥与
corrected myopic-ceiling half义务均保持OPEN。强/弱iid桥已由公屏对应真实反例否定；
不应再用旧摘要中的OPEN覆盖后来的具体反例。
