# route5a §4 的覆盖余额勘误

2026-10-24。个人检查记录，未独立审查，不改共享稿。原 Q-CAG-HALF 仍 OPEN。

来源为 `R-1740705e79f14baba6326b951a52152f/route5a/sequential_deviation_share_lemma.md`，读到的版本日期为 2026-10-23。该稿 L1--L4 的逐客户推导不受此记录影响。这里只指出 §4 从遗漏半额付款到原 half 的推导尚缺信用，**不声称其条件性结论在完整 SPE 类中已有反例**。

设实际并集为 U、福利 W=|U|，比较并集为 C、O=|C|。令

\[
I=|C\cap U|,\qquad L=|C\setminus U|,\qquad E=|U\setminus C|.
\]

则逐集合恒有

\[
W=I+E,\quad O=I+L,\quad O-W=L-E.
\tag{1}
\]

对比较主题排列 π，记其原 L2 付款为

\[
A_\pi=\sum_{i=1}^m\frac{|T_{\pi(i)}\setminus U|}{m-i+1}.
\]

完整 SPE 给 `W>=A_pi`。原 §4 附加条件是 `A_pi>=L/2`，所以其直接可证链只有

\[
O=I+L\le W+2A_\pi\le3W.
\tag{2}
\]

这条链不能给 `O<=2W`。例如抽象非负余额 `I=W=1,E=0,L=2,A_pi=1` 满足上面已列的标量条件，却有 O=3。这是标量推理的反模型，不是 CAG 实例或 SPE 反例。

若同一个合法付款另满足

\[
A_\pi\ge O-W=L-E,
\tag{3}
\]

则 `O-W<=A_pi<=W` 确实推出 half。更强的 `A_pi>=L` 也足够，但不应要求全部遗漏总能由一份 W 支付：已有 `R-171cd7d518434f36a48cd50df29c9303/global/optimal_omission_exchange_counterexample.md` 的完整二人 SPE 有 W=35、唯一最优并集 O=38、L=36>W，故这种遗漏全额付款不可能普遍成立。原 half 在该例仍严格成立。

因此一般跨枝预算必须保留 E：它是实际覆盖但比较并集外的合法信用，目标余额为 L-E，而不是 L，也不是 L/2。
