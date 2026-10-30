# root净券uniform-subset与角色价格包络的独立核对

2026-10-24。被审稿为 `../parent/role_price_envelope.md`。首次读取含证明；本页是逐式独立重构，非盲。以下局部凸包、全图HIT引用与层积分公式通过；没有actual钱包cap或half结论。

对raw full/fresh行，每个q_j逐客户只是diagonal J的一部分，所以q_j<=J<=J+L。SAFE净行current概率p_i=(J+L)/w，非current p_j=q_j/w，因此p_j<=p_i。合法删正边并增加current质量后仍然成立。所用分母须是该同一图的v或nu，不能额外减chi而默认仍成立。

若一个概率向量满足p_j<=p_i，令U_t={j!=i:p_j>=t}，以(1+|U_t|)dt混合uniform({i} union U_t)，积分t从0到p_i。总混合质量p_i+sum p_j=1；current积分为p_i，其它角色为p_j。反向每个uniform-subset行本身都满足p_j<=p_i，凸组合保留。所以root的局部凸包刻画准确。

全图价格需用全图HIT，不能直接把局部最大均价当终端最大均价。固定source i，以lambda_i为基线丢掉低价角色的负项，对高价角色按降序lambda_(1)...lambda_(l)逐层用k/(k+1)。结果等价于

    lambda_i+sum_(k=1..l)
             [lambda_(k)-lambda_i]/[k(k+1)]
      =lambda_i/(l+1)+sum_(k=1..l)lambda_(k)/[k(k+1)]。

利用sum_(k=1..l)1/[k(k+1)]=l/(l+1)核对了baseline系数。l=0、价格并列、lambda为集合指示、lambda恒1等边界正确。所有sources线性叠加得到root的共同加权终点关系。

HIT是relay提出、root/credible分别收到陈述后重构；价格层积分是其推论，不另算独立全局付款。适用同一固定净券图与合法初始化；它没有无条件覆盖观察随机路径后再适应删源而改变条件分布的实验。lambda恒1只返M<=M，actual(j,x)单券、同角色券sum<=u_i及half均仍未证。
