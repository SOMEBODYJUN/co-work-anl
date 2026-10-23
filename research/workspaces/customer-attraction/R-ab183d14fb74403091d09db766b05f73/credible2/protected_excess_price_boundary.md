# 既有唯一最优遗漏反例的保护价格边界

2026-10-22，Boss6个人推论。底层完整 SPE、唯一最优组合及解析族均属于
Boss5既有资产
[optimal_omission_exchange_counterexample.md](../../R-171cd7d518434f36a48cd50df29c9303/global/optimal_omission_exchange_counterexample.md)。
本页没有发现新的底层反例，不影响 Q-CAG-HALF；作用是明确关闭一个更强价格
接口，避免把已失效的整个遗漏支付换成价格语言后继续当开放机制。

## 被关闭的价格候选

旧 `R-6e3.../continuation_induction/prefix_price_induction.md` 的二人
PROTECTED-SHARP 候选是：对终局遗漏客户 D，

    B_D(u_A) <= max(0,u_B-u_A),
    B_D(v)=sup_(z>=0)[sum_(x in D)min(1,sum_(T contains x)z_T)-v sum_T z_T].

其自然全人数推广 `B_D(u_i)<=sum_(j>i)(u_j-u_i)_+` 若真，对实际最小收益玩家
会支付全部最优遗漏而推出 half。但此强支付早已被 Boss5 底层反例否定。

## 同一解析族的匹配精确原始与对偶

沿用来源 k>=3 的六主题 A,B,T,Q,R,S 与完整二人策略。实际(A,B)不交，

    u_A=6k-2, u_B=7k-2, W=13k-4.

唯一最优是 T,Q；全体实际遗漏客户 D 恰由以下六类组成：

| 兴趣标签 | 重数 |
| --- | ---: |
| T、Q 各自私有 | 各3k−1 |
| TR、TS、QR、QS | 各2k−1 |

所以 T∩D 与 Q∩D 不交，各大小7k−3，合计14k−6；R∩D、S∩D各大小4k−2，
A∩D、B∩D为空。取查询 z_T=z_Q=1，其他零，得到

    B_D(6k-2) >= (14k-6)-2(6k-2)=2k-2.

为证反向界，从 T 私有和 Q 私有客户中各标记 k−1名客户，令其 y_x=1，
其他 D 客户 y_x=0。标记总数2k−2，且对每个合法主题 X，

    sum_(x in X∩D)(1-y_x) <= 6k-2.

具体六主题剩余值是 `(0,0,6k-2,6k-2,4k-2,4k-2)`。对任意 z>=0，逐客户
有 `min(1,d_x)<=y_x+(1-y_x)d_x`，求和即

    sum_(x in D)min(1,d_x) <= (2k-2)+(6k-2)sum_X z_X.

故有匹配的精确值

    B_D(u_A)=2k-2 > k=u_B-u_A,  gap=k-2>0.

71客户 k=3 时价格4、超额尾利3、违反1。比率 `(2k-2)/k` 趋2，因此任何试图
以固定倍数 `lambda (u_B-u_A)_+` 普遍支付 B_D 的命题，至少需要 lambda>=2。
这里仅给必要界，没有证明 lambda=2 足够。

## 仍必须保留的净覆盖

原族的实际独占于最优并集之外的客户 G=13k−6。真正差额是

    OPT-W=|OPT\actual|-G=k,

而非遗漏14k−6。保留 G 的价格/净覆盖候选没有被本页否定。使用同一旧实例
关闭更强接口，不等于得到一般净覆盖的新支付机制。

`protected_price_boundary.py` 无 optimizer 实现原始/对偶核对，且通过 canonical
全有序历史验证器及 canonical all-outcomes solver 检查来源完整 SPE。通式证明
依据以上解析，不依赖所选4个 k 的有限回归。独立数学审查尚未发生。
