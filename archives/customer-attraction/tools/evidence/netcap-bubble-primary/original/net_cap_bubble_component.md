# 净孩子超额cap与保背景的实际前缀换位

原half仍OPEN。以下为一般分析域和精确操作，非福利新界。M(h)=max_A min_(childSPE) u_current；R(h)中的有序终局恰满足每个后缀角色利润≥其M，这是旧可信拼合的直接形式。

## 净cap

原actual-prefix h_i后的raw终局z令S_i=Σ_(k>i)[u_k−M(z_<k)]，B_i=d_i−S_i。原source有S_i≥0、B_i≤d_i≤u_i。分析中可释放actual行动标签，取每行质量1的全部raw终局q_i，要求总约束Σ_i E B_i≤W。不是辅助SPE；删除进入槽负载仍合法。

shadow LP有一个μ≥0与行η_i，使r_i(z)=η_i+μB_i(z)−w·ell_i(z)≥0。最优处G=μ[I_total+Σ_i E_source S_i]+Σ_i E_source r_i，只展开同一KKT银行，不另领μW。

真source孩子z在未来j复制进入主题A后得z′。Γ_j≥0且d_i(z′)=u_j(z′)，所以

    B_i(z′)−B_i(z)=u_j(z)−d_i(z)
      +Σ_(i<k<j)[u_k(z)−u_k(z′)]+S_desc(z)−S_desc(z′)。

统一μ消去root变化与currentΓ；中间前缀损失未付。

## BUBBLE

实际主题记b_i。取z=(h_i,A,b_i,Y)，Y为该前缀后真正完整尾SPE。换位v=(h_i,b_i,A,Y)。两项之后计数相同，复制未来全部策略可得下一actual-prefix行i+1强制A的真正child SPE。不认同原σ的不同历史平局。

    ell_i(z)=ell_(i+1)(v), d_i(z)=d_(i+1)(v),
    B_i(z)−B_(i+1)(v)=M(h_i,A)−u_(i+1)(z)。

commonμ下r_i(z)−r_(i+1)(v)=η_i−η_(i+1)+μ[M(h_i,A)−u_(i+1)(z)]。若z由source第一后继强制b_i得到，括号=真Γ−source canonical slack。tree已独立重构上述关系。

该操作可行且保背景，但到达分布未必等于下一行source；多源重复前送可堆积角色质量，η与source库存不免费望远镜。没有一般付款。

[精确QA脚本](audit_netcap_bubble.py)与[冻结结果](netcap_bubble_exact_audit.json)在五份单位客户输入含空/零、m1核FLOOR/COPY/BUBBLE，非一般half证据；一般解析由count-isomorphic拼合与逐项消去承担。
