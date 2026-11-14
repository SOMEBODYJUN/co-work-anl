# ZZ 分裂必要系统有理点：核心审读与范围边界

任务 `customer-attraction-3a-3a-f5d8acecff979b30` 只覆盖核心对象
`customer-attraction/zz-diagonal-split-rational-necessary-point`（registration pin
`65ef9e3bb281af401f33d7c1082adb0f74745530a97d3bf729717d2034a9819e`）。本轮按任务声明完整读取 10 份 distinct staged refs；`split_basic_exact.json` 按两个连续区段读取并整体 JSON 解析。交付只写本任务声明目录和 receipt，不修改 registry、全局 coverage、integration、队列、任务状态或 Git。

## 核心数学结论

核心点固定 `split_basic_exact.json` 的输入（SHA
`b12c4aa6b3cd106f3fb8e8a56be7469988456c0cb6e02b1741db8c09d587b34a`）：一个共同容量 `K`、16 个 hist（10 个正质量、6 个零质量）、全部固定 hist 质量和固定 `R` 边缘。对每个正 hist 沿共同 `R` 阈值轴切成 22 个 slab，重新选择 275 个 `Z` slab 质量。其精确表 `zz_split_exact.json`（SHA
`312732da47c24fe39259c339cf669231162f1402c85a4036a8a351abaef7f51c`）给出

- `4005 = 3945 + 60` 条必要行全部通过，`minimum_slack=0`；
- `O=1`，
  \[
  W=\frac{77122220724026571141557320969163}
          {161324472800190691224726909402699}<\frac12,
  \]
  且
  \[
  O-2W=\frac{7080031352137548941612267464373}
                 {161324472800190691224726909402699}>0;
  \]
- 275 个 `Z` 质量中 125 个正、150 个为零，21 个是严格内点（`free_vertex_variables=21`）；
- 60 个 `Z-Z` 聚合槽保留 18 个结构性空槽，42 个非空槽中 29 个正、31 个为零，最小值为 0。

这里的 3945 行来自旧 3889 行和 56 条 `i=j`/`i\ne j` 对角拆分行；程序逐列断言每一对新行相加回对应旧行，容量列为 30K 与 6K，未增加客户或策略变量。60 个 `Z-Z` 槽是末位必要 IC 的聚合，不是 60 个独立约束。

## 模型、量词和行的真实来源

共同模型是有限单位客户、有限非空带标签目录，六名单位提供者按固定顺序观察全部有序历史、终局均分客户价值；完整 pure-SPE 要对每名玩家、每个合法历史和每个单标签偏离沿同一策略的真实续局比较。定义文件同时保留重复标签、同覆盖异标签、空主题、零客户和离轨平局。核心点只记录某个固定实际路径产生的 `R/Z` 末位必要关系。

固定同一完整策略的实际前四位后，令 `R_e` 为强制前缀下的真实末位回复，`Z_e` 为强制 `R_e` 后的真实回复。对任意合法 `Z_f`，末位 IC 的每客户项为

\[
\frac{z_e-z_f}{p_a+1+r_e},
\]

其中 `p_a` 是实际前四位负载、`r_e,z_e` 是 `R_e,Z_e` 会员位。固定 `R` 边缘后按共同阈值切层，层内 `z` 变量把这个必要系统线性化；接口审计逐字段核对全部 275 个变量、边界和 60 个 ZZ 槽。它证明的是固定必要系统的有限可行点，不能反推某一完整策略、所有离轨 IC、查询合法性或共同目录的全局容量条件。

## 有理会员实现与坐标变更

`point-audit.json`（SHA
`b498a95526e79f6080068d9b33b68967d9bd44791b430f91b4a94c8e2ec0e726`）把每个 slab 内的 `R` 位固定，再按全部 `z` 端点嵌套切分，得到 43 个正质量有理代表原子。原子总质量为 1，所有 22 个 slab 的原子质量和恰等 slab 长度；由这些原子恢复的 582 个显式 `R/Z` joint 坐标和 1306 个 `R-R` 坐标，逐项与重构后的积分一致。这支付了本次 275 变量 lift 的共同会员测度实现（清分母后可转为单位客户重数），但仍没有把会员原子标成一份完整标签策略。

当前 275 点不是 `split_basic_exact.json` 中旧 1905 个质量的原样复制。重构保持 194 组 `R` 边缘，改变 62 个 joint 坐标、193 个 overlap 坐标和 45 个 `Z` 组边缘；`R` 组边缘不变。源 3945 点的 193 个 overlap 中有 189 个低于真实 Fréchet 下界，这是把源点字面解释为同一客户交叠时的障碍；本点用共同阈值重新得到的坐标和 43 原子是另一点，不能把旧 1905 overlap 值与新 275 点混用。

## 证据核验及其边界

`execution.json`（SHA
`56f1f3e98bd230c1052e3d53f94505262f2318a33ecb3c73c1d374a8627ce2a0`）记录原 `zz_threshold_closure.py --split --verify` 一次执行：Python 3.12.14、NumPy 2.3.5、SciPy 1.17.0、assert 开启、31.252 秒、exit 0、stderr 为空、LP 调用 0、冻结文件未变。它支付的是原实现对当前新 `Z` 坐标的 4005 行回代，不是第二个独立矩阵生成器。

`interface-audit.json`（SHA
`e464fae786d22bbb8bfe02cf2b334da3083dcb41a2897eee72ed58c141308708`）独立解析 split 输入接口并复用其 60-ZZ 分数表：16 hist、194 组、582 joint、1306 overlap、22 slab、275 变量，60 槽 31 零/29 正。`point-audit` 明确 `existing_ZZ_result_reused.new_row_replay=false`，因此不能把它说成在本轮又独立重跑了 ZZ 矩阵；当前边只按两份证据的各自范围报告。

## 可实现性和迁移缺口

1. 43 原子只实现固定 hist/R/Z 会员测度和重构的 pairwise 坐标；没有为所有有序历史指定同一 `sigma`，也没有支付所有真实后继、容量和标签可达性条件。
2. `W<1/2` 是固定必要系统点的低覆盖数值；`O=1` 是该记录的归一化，不等于共同目录中的 `OPT_6`，因此不构成一般六人 half 反例或定理。
3. 释放 `Z/RZ` 边缘、允许跨组任意 `R` 联合、改变 hist/R 输入或引入未付的完整策略行，都必须在新坐标上重新核验；不能从当前 4005 PASS 免费迁移。
4. 后继 7931 点虽与本点有相同变量描述和相同 `W`，但有 103 个 `Z` 变量质量改变，且 `full_pair_graph_reverified=false`；其 PAIR/交叠行可行性不能从当前点继承。默认 3949、cross 4987、7931 等阶段点也各有自己的输入和范围。

## 对端比较处置

任务声明的两个 overlap 对端是 `customer-attraction/diagonal-basic-row-split-exact-necessary-point` 与 `customer-attraction/diagonal-reply-budget-split-basic-graph-program`，均标为 3B follow-up。当前 3A 已核清它们作为 source point/拆分程序的接口和当前 4005 lift 的差异，但没有发布 3B successor task，也没有把对端当作本 core 的 coverage 端点。后续应专门比较：4005 的共同阈值重构是否能在对端的 1905 坐标合同下保持全部 3945 行，以及 56 拆分程序的系数/列序约束能否迁移到改后的 275 点；在此之前只保留本 core 的 context/self-check 边。
