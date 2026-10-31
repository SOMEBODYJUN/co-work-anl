---
id: customer-attraction/r28-certificate-dynamic-audit
kind: review
category: 审查
title: R-28 空稀释、加入冲突与 UTP 有限审计
status: integrated-finite-audits
truth_status: exact-finite-results; no-general-half-proof; no-certified-counterexample
source_refs:
  - clean:6428425c5f2d179bda44
  - clean:e7b636c58363075d0597
  - clean:25623d0276ff9bcce131
  - clean:39d94cf8fbd2c99e909f
  - clean:dcca41f3ea1230dad37a
  - clean:5209aad2ad96dc0ebe89
  - clean:3bd18bf79f9166429ee3
  - clean:da14edc75259534416f5
  - clean:6db6fa7471aaa2e1a0ed
  - clean:67bcd1e5d345605fc7e0
  - clean:517b02cd2eea8b5358c3
  - clean:a62b7a378ecbc3ea24f7
  - clean:a541fe42e26e2f0969cb
  - clean:be13357485a38d6a56f5
  - clean:78639434fb10c28feb7f
  - clean:c28a144021f51fbc1dba
  - clean:2ee6853fcb25f83330d5
  - clean:d79cafeaf057f5b0fd67
  - clean:922e5ec827e40811b409
  - clean:d3619a01f7340af36965
---

本批实际读取了 R-28e 的二十个源：失败路线与工作台说明、旧三十四客户证书的独立有理审计、端点混合/私有停车/UTP 有限诊断、加入冲突和图冲突的自包含验证、尾循环盲审、三份预选的纯 theta 检查，以及七客户和旧三十四客户回复循环审计。结论始终按“完整证明、条件结论、有限实验、障碍、原模型反例”分开；没有把有限负结果升级为一般反例，也没有把必要投影升级为 SPE。一般目标 Q-CAG-HALF 仍为 OPEN。

## 1. 旧三十四客户例：空稀释的定义级全历史核验

`audit_empty_dilution_rescue.py/json` 直接读取旧三十四单位客户的冻结实例和证书，不导入原作者审计或 canonical solver。它枚举 3 个玩家、7 个主题的 57 个有序历史，并对 342 个非自身偏离逐一比较；实际路径为 `(X0,Y0,Y1)`，福利 $W=32$，均分基准 $W/m=32/3$，实际支付向量 $(29/3,67/6,67/6)$。21 个带重数的强制端点对应 19 个不同终局；实际完整列的最大主题条目是 `Y2=17/2`，严格低于 $32/3$。

同一脚本还固定了根空端点 `(Empty,X0,X1)`，逐客户比较实际与根空端点的负载，验证实际负载逐项不小于该空端点。对查询主题 `X2`，三组端点求和为
\[
D_q=63/2,\qquad H_{\varnothing,q}=65/2,\qquad G_q=41/2.
\]
取 $\varepsilon=1/24$ 后，强项为 $\varepsilon D_q=21/16$，空稀释项为 $\varepsilon(1-\varepsilon)H_{\varnothing,q}+\varepsilon^2G_q=4/3$，差为 $-1/48$；但对全部位置和全部强制动作取最小 `X2` 条目仍为 $13/2$，因此该旧例的全端点空稀释最小值为 $13/48$。`all_checks_passed=true` 只说明这个指定证书的定义级核验通过，不能推出自由完整端点菜单 $F$ 的一般分离，也不能改变目标的开放状态。

这正是旧空稀释路线的边界：把空行强行加入会产生可计算的强聚合缺口，但该证书的同一真实终局又同时 cap 全目录；一阶齐次性与完整菜单归一化需要另行证明，不能由该单例跨到一般客户类型。

## 2. 端点混合、私有停车和 UTP：保留为有限诊断

`endpoint_mix_probe.json` 给出 9 个有限端点混合诊断。代表性行：路径 `[2,3]` 的福利为 4，混合值 1.3，预算 2，gap 为 `-0.7`；路径 `[0,0,1]` 的福利为 8，值约 1.9962，预算约 2.6667，gap 约 `-0.67045`；其余行同样没有产生正分离。它们只扫描给定证书和给定端点集合，不是全历史 SPE 检验，故归为“有限实验/路线障碍”。

`parking_extra_one.py/json` 对 directed private-parking 参数做 48 个数值诊断（$k=1,2,3$ 的参数区间）。所有 gap 均为负，范围约 $[-3.602,-1.050]$；这说明该定向停车族没有在所扫区间击穿 weak extra-one 桥，但没有任何普遍性，因为脚本使用浮点 LP 和预设参数，只有找到正 gap 时才会构造精确实例。

`utp_attack.py` 的 `utp_p5m5.json` 是 seed `2026102321` 下 $p=5,m=5$、600 次的 directed UTP 有限诊断，`positive=false`。它不是随机搜索的定理，也没有把 Markov 终局一致性当作 UTP 证明。失败路线文件明确记载：静态回复循环单调性已有七客户透明反例，空查询桥对自由完整菜单未形成分离，森林 UTP 与 Markov 终局扫描均停止在有限阴性。

## 3. 加入冲突：精确的表示障碍，但不是客户吸引反例

`join_conflict_verification.json` 与自包含 `verify_join_conflict.py` 做了精确枚举。覆盖 singleton 游戏中有 14 个完整策略、6 个 Markov 策略；两类在该特例产生的终局计数相同（`[1,2]` 或 `[2,1]`）。加入一个 generic anonymous game 后，完整策略有 7 个、Markov 策略有 3 个；完整策略可实现 `[0,3],[1,2],[2,1],[3,0]` 四类终局，而 Markov 只保留 `[0,3]` 和 `[3,0]`。因此把全历史 continuation 直接“join”为 Markov/匿名策略会丢失中间计数状态。

其精确收益向量为 $(1/2,1)$ 与 $(1,1/2)$，根比较每个策略 14 次。这个 crossing 证明的是 generic non-CAG 边界：join 不保留充分状态，不能把它作为当前客户吸引模型的正式反例；它对第三阶段的关系证据有用，提醒后续必须保留完整历史及任意平局。

`graph_conflict_probe.py` 又给出 $p=5$、目标 `[0,2,4]` 的 10 个二元集合 witness：`root=4`、`second=2`、`last=0`、`root_floor=0`。该输出是图状冲突探针的可复现实例，不是完整客户吸引 SPE 或 half 缺口证明。

## 4. 回复循环和尾部势：小例精确复核，旧例只作对照

`blind_tail_cycle_audit.py` 在 7 客户例逐节点列出 13 个历史的选动作和三动作偏离收益。实际终局为 `CCA`，支付 $(13/6,13/6,8/3)$，福利 7；根租金矩阵的对角和为 $25/6$、交叉和为 $13/3$。`audit_reply_cycles.py` 同时验证 39 个（含自身）动作比较，最小 SPE slack 为 0，报告 cycle difference `-1/6`、two-point parent slack repair `0`、tail potential regrets $(0,1/2)$。这把静态回复势不能统一支付的障碍精确化，但 7 客户例没有给出新的 half 反例。

同一 `reply_cycle_audit.json` 对已有三十四客户例做 43 个历史、258 个含自身比较：实际 `(X0,Y0,Y1)`、福利 32、最小 slack 0；查询 `X2,Y2` 的两个分支支付向量都为 $(29/3,35/3,35/3)$，cross-branch tail difference 为 $(0,0)$，但 cycle difference 和 two-point repair 都为 `-2`，tail potential regrets 为 $(1,1)$，实际尾部相对根的 surplus 为 3。它确认旧例的缺口机制，却不是本批新发现。

## 5. 纯 theta 三证书检查与运行边界

`extra_slot_pure_theta_probe.py/json` 只读取三份预选现有证书：34 客户 individual-security、36 客户 aggregate-theta、61 客户 root-tax。它们分别有 43、43、259 个决策节点；所有 complete pure SPE 检查通过，全部历史 violation count 均为 0。最小实际前缀 margin 分别为 2、$5/2$，以及第三份证书的对应有限值。该源明确声明“无随机或扩展样本”，所以只能保留为条件结论，不是一般 theta 定理。

本批若干探针硬编码了缺失的旧工作区路径或依赖（例如旧 R-d22 证书、`customer_attraction` 包及示例模块）。在当前 clone 中不能独立重跑的部分已保留原始 JSON、脚本和运行边界；没有用替代路径伪造输出。四个自包含运行（blind tail、join verifier、graph conflict、reply-cycle audit）均已保存 stdout/stderr，并通过 exit 0。

## 6. 接续关系

后续若要继续，必须把以下内容接回完整纯 SPE 和客户目录层：

1. 将加入冲突的“缺失历史状态”编码为真实客户类型，而不是泛化 anonymous game；逐历史核对 continuation、BR/IC 和同福利均分。
2. 对空稀释只使用可审计的全端点菜单，区分根空端点、强制中间端点和实际终局，避免把 single-column cap 当作自由 $F$ 上界。
3. 将 7 客户回复循环与 34 客户旧例的支付差作为障碍证据，寻找跨真实分支可实现的支付转移；静态势或单一末端 top-up 不能替代。
4. 保留零客户、空主题、重复类型、离轨历史和任意平局；没有这些约束下的压缩不构成当前六人 SPE 问题的证明。

正文只归档可精确核验的有限结论、失败机制和依赖缺口；目标“每份完整历史纯 SPE 至少覆盖六主题最大覆盖人数的一半”仍未解决。

证据、来源清单及四个实际运行输出见 [R-28 evidence](../../tools/evidence/R28-certificate-dynamic-20261031/README.md)。
