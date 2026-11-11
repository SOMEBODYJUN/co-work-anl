# 一背景五尾完整投影独立审计：PASS

独立审计席仅写本页与 background_projection_audit/，没有修改旧文件、
LP 输入、RUN 或登记状态，没有 Git 写入。优化器调用为 0，原大型
隐藏域 oracle 调用为 0，不导入或运行 Main 构造器。

已亲读正式 owner
customer-attraction/one-prefix-five-profit-exclusive-charge v4 的第 3、4
节及 Main 投影证明。继承其完整 53 行来源证明，从冻结利润条件表
独立完成以下算术：

| 检查对象 | 结果 |
| --- | --- |
| 12288 个 \((ABCDEUVWXY,k)\) 条件值 | 完整、唯一、缩放整数一致 |
| 384 组各 32 个条件值重新取最小 | 与两份原 192 格表完全一致 |
| 448 个六槽删除均值 | 与逐索引删除一致 |
| 4096 个六槽会员模式、24576 次索引删除 | 全部通过，重复索引保留 |
| 全部 actual/X/O 客户类型 | 256 个全部保留，含 128 个 \(o=0\) 类型 |
| 最终系数 | 257 列与 Main 冻结 JSON 全部一致 |
| 真五尾利润与共同 \(K\) | \(V=W-u_1\)，\(K\) 列为 \(-226487/10^{21}\) |

被比较的 Main 最终投影 SHA-256 为
f39ae91167d96f015c188159e3efb9dcbf7436640e058467b0ead1386c4744cc。
X 位保留，128 对只翻转 X 的列系数精确相同。

指定 v3 代表点的代入值为

\[
-\frac{1084303104035871921035240700211255159170652321213}
{132457405400589739043679174720000000000000000000000}
\approx-0.0081860512121358847561.
\]

指定 v4 代表点的代入值为

\[
\frac{1156524037867798928682196120160148354108266098075758921763}
{323722713611618348911809571085826504600000000000000000000000}
\approx+0.0035725761253049483048.
\]

两值均独立用精确 primal 重算，并与 Main 最终输出一致。v3 指定点违反
该必要行；v4 指定点满足该行。这里不从代表点外推整面，不声称 SPE
可实现性，也没有证明六人 half 或给出完整 SPE 反例。

完整范围说明、推导、全部输入 pin、算术边界和复现命令见
[审计证明](background_projection_audit/proof.md)。
精确有限包：

- [独立程序](background_projection_audit/rebuild_independent.py)
- [全部条件归组及最小值](background_projection_audit/conditional_minima.json)
- [全部删槽均值](background_projection_audit/deletion_averages.json)
- [完整列与两点代入](background_projection_audit/audit_result.json)
- [哈希清单](background_projection_audit/SHA256SUMS)

原条件表下每格隐藏直方图／菜单完整域的真实性由已登记来源继承，
本轮没有假称再次穷尽该大型 oracle。本包完成即冻结，后续由 Main 决定。
