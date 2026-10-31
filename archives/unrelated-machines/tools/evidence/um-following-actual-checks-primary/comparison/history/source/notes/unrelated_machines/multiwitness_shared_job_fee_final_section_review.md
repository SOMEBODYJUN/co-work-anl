# 多见证共享任务收费的 canonical 第6节最终全文审读

实际审读对象：`co-work-anl-boss11/research/current/unrelated_machines/two_witness_query_separation.md`，本次实际文件 SHA256 `bf942037e600967fa86b76c2b1f0db41673a2bae71411e1afb6527d6f332c709`。

此前已经完成：v1 Exact-only 独立重构并冻结空K反例；独立Fraction枚举；随后读取v2 Exact与作者Proof全篇。这次收到canonical通知后，实际读取了该文件完整第1–6节（工具输出共4997 tokens），尤其逐段审读了新第6节所有对象、结论、证明、范围与复杂度。此记录是非盲最终正文审查，不冒充第二次独立重构。

核验结果：新第6节的限定数学合同通过，没有新增standing fatal。

- 原矩阵有`2p+2`台互异机器、`2p+1`枚互异任务、`4p+2`条finite资格，稠密项数为`(2p+2)(2p+1)`；没有遗漏背景任务、隐式预载或额外资格。
- sigma0全部原任务峰恰1；每个sigma_r实际移动原q_r、x_r、f，查询改owner集合恰为`{q_r}`。每个H、A、R、S的负载已逐族核对。
- OPT1下界使用`c+sum b>=1`以及峰<1迫x/f去R，不是从某条可选unit资格推下界。
- 任意K的`min(2,max(1,B_K))`有两份完整实际上界及`C<2`时强迫`x_K->R`的下界，含空K、B=1、B=2、B>2。
- 费用闭阈值中`B_K=beta`仍可行、`c+B_K=beta`归fee0；空K的费用0，beta=2所有pattern可让f原地。beta<2的强迫论证未被错误延伸到等号2。
- 容量s的实阈值比较、s>=2的三半免费单例、异权非空K严格和式与`|K|<2`均正确。v1空集异议被明确保留，v2修复没有倒改旧版本。
- 计算与输出使用实际原任务、二进制有理求和，不展开分母或s。指定pattern不可行与原P合法可行分开，含p=1及c=1的owner费/新增unit费区别。

与原第1–5节无冲突：旧分离和计数命题以同一P的两份共同strict actual为输入，新特例只有sigma0及每个singleton自己的sigma_r，p>=2、b=c=1时共同全开模式OPT恰2，根本没有旧定理所需的sigma1。若只选sigma0及一个sigma_r，旧Q只有一项，支付同一f费用1完全兼容。新段也明确区分旧预载星与同一P身份竞争，不把多份单例见证并成全开见证。

第6节保持受限结果的正确等级：此P显式OPT1、可精确求解，没有OPT gap，未给标签复制、跨测试预算或源NO decoder；不能据此升级UM-TARGET-v1正反面。外审、全球新颖性与独立论文价值仍未认证。

独立有限证据仍为此前已冻的`multiwitness_fee_fraction_audit.json`（359参数组、135712完整原分配、4660模式OPT、23908闭阈值fee比较）；本次没有为最终正文审读而重复或扩大枚举，也未更改旧冻结输出。
