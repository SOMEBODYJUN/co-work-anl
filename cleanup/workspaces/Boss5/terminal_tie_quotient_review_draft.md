---
kind: source-review-draft
source_id: 8aff4f2a9c9f5e116926
source_path: research/current/customer_attraction/terminal_tie_quotient.md
source_sha256: f14c514b3301450f4da558479a3da8d5ce600c71279c2b8190b1e297733f3273
reviewer: Boss5/terminal_tie
status: ready-for-parent-review
recommended_disposition: integrated
recommended_target: archives/customer-attraction/state/方法/末端平局商空间支付与局部二次判别--方法.md
---

# `terminal_tie_quotient.md` 语义清洗草稿

## 1. 来源识别和范围

本源是 2026-10-10 的机制稿，固定共同有限目录、单位玩家/客户和完整有序
历史纯策略，研究把每个末节点的回复替换成同主题计数代表的规范化。它提出
两个对象：`CA-TERMINAL-TIE-QUOTIENT-LIFT`（末行商空间的条件性证书提升）和
`CA-TERMINAL-TIE-LOCAL-QUADRATIC`（固定计数内的局部精确判别）。正文明确
不声称规范化策略仍为 SPE，也不声称任意输入都有提升、更不声称一般六人
half 覆盖。

与同批来源比较后，源的数学内容已经由现有方法对象
`archives/customer-attraction/state/方法/末端平局商空间支付与局部二次判别--方法.md`
承接；本草稿记录实际阅读、独有边界和复现结果，不能把该现有对象倒读为源已
自动完成。

## 2. 基本代数接口

对长度 `n-1` 的末前缀计数 `q` 选代表 `g_q`，写代表回复
`b_q=sigma_n(g_q)`，实际回复集合 `A_q`，类型 `T` 的前缀负载
`p_q(T)=sum_S q(S) 1[S in T]`。对 `a in A_q` 与代表不同的前缀，源定义

`R_{q,a;T}=(1[a in T]-1[b_q in T])/(p_q(T)+1)`。

两条真实末行满足 `R_{q,a}=Gamma_{ell(q,a),b_q}` 与
`-R_{q,a}=Gamma_{g_q,a}`，所以任意有符号组合
`z=sum theta_{q,a} R_{q,a}` 都能按 `theta` 正负拆成两类非负真实行支付。
这只给出一个可显式使用的子空间 `H_sigma`，不是全部真实行锥的最大线性空间。
任何原 SPE 客户质量 `w` 对每个 `R` 的内积均为零。

若规范化只改末回复，真实早期行与规范化早期行的逐类型差为

`bar Gamma_{h,a}=Gamma_{h,a}+delta_{ell_h,sigma(h)}-delta_{ell_{ha},a}`，

末行则按代表行拆分。给规范化证书
`d=bar Gamma^T bar lambda+bar r`，保留早期支付后可写成

`d=Gamma^T lambda0 + bar r + E`。

若存在系数 `theta` 使

`r'=bar r+E-sum(theta R) >= 0` 逐类型成立，

则由 `R` 的正负真实行表示得到完整原证书。故
`bar r+E in R_+^types + H_sigma` 是“保留早期乘子、只加结构末行修正”
这一指定模板的充要条件；它不是任意原真实证书存在性的必要条件。允许重新
选择早期乘子时，机制更宽。

## 3. 有限成功和固定证书障碍

源的三主题、三提供者例按类型顺序 `(A,B,AB,C,AC,BC,ABC)`，比较目标为
`d=2c-o=(1,-1,1,1,1,1,1)`。规范化只把 `AC,CB` 末回复改成 `C`，根终局
`CAC` 和根覆盖保持。

* 早期规范化乘子 `(2,1,1)` 给
  `bar r=(0,0,1,1/2,5/6,2/3,1)`，运输余项
  `s=(0,-1/2,1/2,-1/2,1/2,2/3,1)`。
  取 `-2 R_AC+3 R_CB` 后余项为
  `(0,0,0,0,4/3,2/3,1)`，因此该目标有严格商空间提升；新增真实行
  是 `2 Gamma_{CA,B}` 和 `3 Gamma_{CB,C}`。
* 同一目标的合法规范化证书乘子 `(4,1,2)` 给
  `bar r=(0,0,1,0,1,0,1)`，运输后
  `s_bad=(0,-1/2,1/2,-2,1/3,0,1)`。
  合法三客户质量 `w=(0,0,1,1,0,1,0)` 使原全部 39 个比较非负、
  `R_AC.w=R_CB.w=0`，但 `s_bad.w=-3/2`。因此该固定早期支付不能由
  任何结构末行或任意新增非负真实行修复；它只是否定“任意既定规范化
  证书自动保权提升”，不是 half 反例，因为该例仍有 `W=OPT_3=3`。

这两个数值边界必须同时保留：商空间接口确实严格扩大逐类型非负条件，
固定乘子失败也不能扩大成规范化一般不可能或原目标不存在证书。

## 4. 局部判别、跨计数和可达性

固定计数 `q` 后，把早期运输净流聚合为 `K_{a,S}`，令 `x_i=1[i in T]`，
`p=sum_i q_i x_i`，`N=sum_{a,S}K_{a,S} x_S(x_a-x_b)`。局部相反行和写成
`J=sum_i eta_i x_i`。源给出等式 `N=pJ` 的一次/二次系数条件，并额外要求
`eta_i=0` 对所有 `q_i=0` 的坐标成立；否则 `p=0` 的外部 singleton 类型会被
遗漏。满足这些 `O(m^2)` 线性条件当且仅当固定计数内的所有类型列逐项相等。
逐计数消去只是全局充分条件，不能当成必要条件，因为不同计数的 reciprocal
行可以跨计数支付。

源还给出两个真实可达边界：

1. 四人三主题四条真实偏离边在两个改变叶形成非均匀净流
   `(0,1,-1)` 与 `(-1,0,1)`，但误差逐类型严格相消为零；这不是把行平均，
   也不意味着任意净流都可路由。
2. 四人两主题的单行误差 `(-1/6,0,0)` 不在其单独计数 reciprocal 行空间，
   却由跨计数系数 `2/5` 和 `-3/5` 的两条真实 reciprocal 行支付。由此应
   在共同全部类型列上检查全局商空间。

真实运输图按最后一次偏离次数严格降阶，源/目标叶受原策略后缀约束；不能先
 任意指定 `kappa` 再声称存在非负行乘子。均匀净流只消掉一部分商空间分量；
 非比例净流还留下 incumbent 重分配债，不能只保留未覆盖客户债。

## 5. 实际审查和复现

已读并比较的相关材料包括：同批固定乘子障碍正文、末回复商空间独立交叉
审查、两份 Fraction 审计脚本及冻结 JSON、现有方法对象和审查对象。源的独有
内容是局部二次判别的 `p=0` 约束、四边真实相消、跨计数支付和可达性限制；
这些不是简单 duplicate，应与现有方法对象、障碍对象及审查对象分别保留链接。

在当前 clone 使用归档中的等价冻结重放脚本执行：

```sh
python3 archives/customer-attraction/tools/evidence/terminal-tie-quotient/replay/customer_attraction_terminal_tie_independent.py
python3 archives/customer-attraction/tools/evidence/terminal-tie-quotient/replay/customer_attraction_terminal_tie_quotient.py
```

两条命令返回码均为 0；输出分别为 2090 和 1826 字节，与冻结报告内容一致。
关键独立结果为：39 个完整 SPE 比较、273 个变换恒等式、63 个互反恒等式、
63 个未覆盖分解；四边 840 个行/类型检查；跨计数系数 `(2/5,-3/5)`；局部
系数等价性检查 8019 次；并明确报告 `universal_half_coverage_proved=false`。

## 6. 建议处置和接续

建议将来源 `8aff4f2a9c9f5e116926` 标为 `integrated`，目标为现有方法正文，
并在其 source_refs/审查对象中保留本源 ID 与冻结版本 hash。建议同时链接：

* `archives/customer-attraction/state/障碍/固定乘子提升的商空间边界--障碍.md`；
* `archives/customer-attraction/state/审查/末回复商空间独立精确审计--审查.md`；
* `archives/customer-attraction/state/审查/末回复商空间的有限审查与局部判别--审查.md`。

不应将该源标为 duplicate 或 needs-decision，也不应把有限成功证书写成一般
六人 half 定理。后续若要推进主命题，必须对每个完整策略与比较元组共同选择
规范化早期乘子、真实可达的商空间系数和逐类型非负余项；当前源只提供条件
接口及有限精确边界。
