# CLIP独立核对及真实off-IC方向检查

2026-10-24，mixed_menus。读credible `../credible/safe_coupon_netting.md`后逐式独立重构，非盲审。§3–4解析通过；未证明一般half、总费用下降或coupon cap。任意m、一般共同目录、全有序history不变。

## CLIP保持什么

固定context v>0，实际行u，正recipient总P，退款F=N+e。既有全客户恒等式为v=u+P−F，0<=F<=u。任删c<=min(P,F)的正边并同步将退款减c，等式不变，当前净行u−F+c仍在[0,u]。

最大取消c=min(P,F)给P'=(v−u)_+、F'=(u−v)_+、当前净行min(v,u)。past优先删除后past剩(P^<−F)_+，future剩min(P^>,(v−u)_+)。保留的正边均是原边子容量，所有future prescribed-context域及past actual coupon标签保留。

用q'重新递推h'=b+incoming、beta'=h'/v。角色DAG归纳得beta'<=beta。质量相消为

    Σb=Σbeta'[min(v,u)+P'^<]。

整行净系数beta' min(v,u)/u=h'/max(v,u)。若u=0，actual IC迫D=0；任何非空主题在有限客户游戏中有正query收益，所以a为空且v=0，与context v>0不容。故此处无隐含零除。

beta'下降不保证净行费下降：删除正边同时减少退款，可把将来质量移回当前。不同context同role系数仍能叠加，本核对未提升共同容量。

## fresh-only与off-history IC

fresh核把v换为nu=u_i(B;N\C)，退款换为Y+N+e，仍有nu=u+P−(Y+N+e)。CLIP同理只在nu>u时传播。

令X=u_i(B;C)，v_S为同一off-history g中改选原实际主题S_i后沿原策略的真实收益，ell=X+nu−v_S>=0。于是

    nu=v_S−X+ell。

真实off-IC本身给nu>=(v_S−X)_+，而不是nu的上界。尤其终止型nu<=u必满足v_S<=u+X；传播型可写

    (nu−u)_+<=[v_S−u−X]_++ell。

后一式保留非负ell，却没有一份actual钱包支付它。因此不能把ell>=0反过来当成CLIP传播量下降，也不能由这个局部方向推出总cap。它约束了低fresh利润停点的C imitation外部选择，但跨context的C收益和ell仍须同一真实容量关系。

截至本次攻击：CLIP本身未发现漏洞；仅添加已有off-IC符号未得新总容量不等式。此处没有声称任何方法不可能，也未追加有限反例或固定规模扫描。
