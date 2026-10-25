# 任意剩余人数 priced 投影与排序压缩的独立审查

审查对象：研究员mechanism给出的任意k投影，明确代码版本为 `customer_attraction/priced_hidden_reply.py` 中 `branch_value`、`projected`、`projected_by_count`，及双方消息确认的同一公式。本审查不修改其代码。

## 数学结论

**该投影对任意总人数m、任意真节点且剩余人数k≥2有效；给出的按隐藏数排序是精确最小化。** 未发现数学漏洞。它产生合法必要行，不自行完成一般m的因子二全局证书。

固定同一完整SPE，实际末位收益为u_m，实际末位前缀负载为ell_x，所有目录主题的共同最大大小为K。在任一有序历史h的真节点，余k人、背景p_x、规定者最终收益r。强制该人选任意合法T后，令同一策略给出的真后继依次为F_1,…,F_{k−1}。令G=F_{k−1}，另取合法Q。记源强制后的收益为v_T、该分支末位收益为v_G。

对任意非负alpha_j、beta_j、mu，定义：

```text
P_j = u_m − sum_x 1_{F_j}(x)/(ell_x+1) ≥ 0
C_j = K − |F_j| ≥ 0
B   = v_G − sum_x 1_Q(x)/(p_x+t_x+sum_{j<k−1} f_{j,x}+1) ≥ 0.
```

源真节点IC给出r−v_T≥0。令z=p+t+sum f，将这些非负项求和：

```text
(r−v_T) + sum alpha_j P_j + sum beta_j C_j + mu B
```

逐客户移项，恰得到

```text
r + (sum alpha) u_m + (sum beta) K − sum_x h_x,

h(p,ell,t,q,f)
 = t/z + sum_j (beta_j+alpha_j/(ell+1)) f_j
   − mu f_last/z + mu q/(p+t+sum_{j<last} f_j+1).
```

取psi=min_f h后，再加每客户h−psi≥0即证明投影。这个推导保持所有历史和目录主题的身份，不要求不同前缀具有相同策略，也没有将被强制选T的玩家当作其分支最佳回复。实际末位对整个共同目录的价格上界允许支付任何离轨F_j；所有这些支付必须在最终证书中共同计入同一个u_m和K。

排序证明：令c_j=beta_j+alpha_j/(ell+1)。固定非末位隐藏人数s=sum_{j<last} f_j与末位g=f_last后，两个份额和查询项的分母只依赖s,g，不依赖被选中的非末位身份。剩余项sum_{j<last} c_j f_j的精确最小值就是s个最小c_j之和C_s。因此只需遍历

```text
s=0,…,k−2,  g∈{0,1},
t/(p+t+s+g) − mu*g/(p+t+s+g)
  + C_s + c_last*g + mu*q/(p+t+s+1).
```

每个ell值应重新计算并排序c_j；不应假定同一排序在所有ell下保持不变。零分子份额定义为0，代码将t/z和g/z分开计算，正确处理p=t=s=g=0。

## 适用边界

- k=2时不存在可排序的非末位隐藏者，s只取0，公式仍有效。
- alpha、beta、mu非负用于合法叠加IC/价格/容量。排序代数本身可容许负c_j，但这不使负alpha或beta的投影自动合法。
- r属于所选真节点，可能是离轨节点收益；不能直接把所有r认作实际某位u_j。
- 只有所列源IC、末位单个查询IC及逐主题价格/容量的系统具有当前排序结构。若加中间玩家IC、多个身份相关查询或隐藏变量交叉项，需要重新证明压缩，不能沿用此结论。
- 任意k投影是可推广的行生成器；五人证书的53权重、BG/PC/DEEP表和全局抵扣仍不能原样推广。

## 独立实现与真实六人检验

独立审查测试写于 `tests/audits/customer_attraction_priced_hidden_reply.py`。测试先直接枚举所有隐藏二元位，与被审查的排序实现比较；再通过精确分数逆向归纳构造m=6完整纯SPE。平局按完整有序历史的哈希选取，所以不将相同负载的历史合并。检查每一个剩余至少两人的真节点、全部合法强制T、全部合法查询Q、三组非负参数，并逐条核对投影和完整非负slack恒等式。

测试已通过：k=2,…,10共3024组排序对字面二元枚举；16个六人完整SPE、2664个真源节点、112794条投影及完整slack恒等式。覆盖空目录主题、单主题目录、不同主题交叉、全部强制T和查询Q、零/均匀/非均匀参数。结果另存 `evidence/customer_attraction/priced_hidden_reply_projection.json`。该有限测试是对定理实现和节点语义的审查佐证；一般m的有效性来自上面的代数证明，有限测试本身不证明一般m结论。

## 对mechanism成稿的补充核对

已读取成稿 `research/current/customer_attraction/priced_hidden_reply_projection.md` 第4节至第5节，与先前双方确认公式一致。第4.1节的多实际安全价格锚点推广也成立：背景固定时，每个隐藏位仍仅增加一个已知线性成本，故同样可按成本排序；各实际收益的预算仍须在最终主证书共同核对。

第4.2节强PAIR汇总系数正确。对全部比较索引i<j求和时，每个主题会员位出现m−1次；同时 `sum_{i<j} t_i t_j=binom(d,2)=d(d−1)/2`。因此

```text
binom(m,2) H ≥ sum_x [(m−1)d_x/(p_x+1)
                  − d_x(d_x−1)/(2(p_x+1)(p_x+2))].
```

普通两利润行本身扣除两次g，因此其汇总的二阶重叠扣除确为该强行的两倍。这一核对是组合代数审查，未把它错误记作已完成一般m的全局支付。
