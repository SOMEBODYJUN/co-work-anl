---
id: customer-attraction/r29-direct-floor-fixed-cone-audit
kind: computation
type_tag: 计算
status: exact-replayed-selected-cones-no-universal-result
truth_status: finite-fixed-cone-diagnostic; zero-negative-witnesses; general-half-open
source_refs:
  - clean:b9b05a1363351610ed09 research/workspaces/customer-attraction/R-29b83efed6b045678e3b7ee11dffb7b3/boss/attack_direct_floor.py
  - clean:d75c0c96529172663f0a research/workspaces/customer-attraction/R-29b83efed6b045678e3b7ee11dffb7b3/boss/direct_floor_attack.json
  - clean:d3ab33c80233d8bf079e research/workspaces/customer-attraction/R-29b83efed6b045678e3b7ee11dffb7b3/counterexample/README.md
  - related:archives/customer-attraction/state/资源/一般半覆盖工作稿的有限攻击与分支导航--资源.md
  - related:archives/customer-attraction/state/资源/DIRECT与前缀门槛的历史量词和后来反驳--资源.md
evidence_paths:
  - archives/customer-attraction/tools/evidence/R29-direct-floor-20261031/manifest.json
  - archives/customer-attraction/tools/evidence/R29-direct-floor-20261031/source/attack_direct_floor.py
  - archives/customer-attraction/tools/evidence/R29-direct-floor-20261031/source/direct_floor_attack.json
  - archives/customer-attraction/tools/evidence/R29-direct-floor-20261031/source/counterexample_README.md
  - archives/customer-attraction/tools/evidence/R29-direct-floor-20261031/replay/direct_floor_replay.json
---

# R29 固定完整 SPE 锥的逐人覆盖门槛有限复核

## 1. 候选命题的准确范围

攻击脚本检验的候选是

\[
 2m u_i\ge \operatorname{OPT}_m,
\]

其中 `m` 是玩家数、`u_i` 是某个实际玩家的终局收益，`OPT_m` 是同一实例至多 `m` 个主题的覆盖最优值。若它对每个实例、每份完整根纯 SPE 和每个玩家都成立，把 `m` 行相加才可得到半覆盖；因此它是充分加强条件，不等于真正 half 命题，也不等于净缺口形式 `m u_i\ge OPT_m-W`。

源代码将一份**已给定的完整有序历史策略**变成 `StrategyCone`，在所有非空客户类型重数上允许非负变量；每一行约束是该固定策略的真实历史偏离 IC。LP 只为固定锥和有限比较支持寻找候选重数，随后以 `Fraction` 恢复并重新核验所有锥行、总客户归一化和整数克隆的真实历史。源文件和 JSON 自身写明：固定锥不是全部 SPE 锥的并集，程序不能给出 universal conclusion。

## 2. 实际冻结数据和重放

`direct_floor_attack.json` 有两个边界检查：`players=1` 与 `players=3` 的单主题零客户可行性均为真；一个客户时收益分别是 `1` 与 `1/3`，脚本记录的 direct margin 都是 `1`。主报告包含 15 个冻结完整策略来源，主题数为 4、5 或 6，玩家数为 2、3 或 4。每个报告记录 exact feasible vertices 数和最小已检查余量：

| 报告数 | exact feasible vertices | 最小余量 | 精确负见证 |
|---:|---:|---:|---:|
| 15 | 448 合计 | `6/41`（来自 `prefix_balance_failure.json`） | 0 |

逐项最小余量是 `9/38, 1/4, 1/6, 1/4, 1/5, 3/5, 9/38, 9/38, 9/38, 1/4, 6/41, 1/5, 9/38, 1/6, 1/5`；它们都为正。把这组记录准确说成“在选定固定 SPE 锥上没有找到精确负见证”即可，不能说扫描了所有目录、所有完整策略或所有人数。

我把源脚本放在一个与其 `ROOT` 相容的临时重放布局中，挂接结果分支已有的 `customer_attraction_strategy_lp.py`、证书 JSON 和 exact model。`PYTHONDONTWRITEBYTECODE=1 python3 attack_direct_floor.py` 的 JSON 输出与冻结 `direct_floor_attack.json` 字节完全相同（两者 SHA-256 均为 `510cc783995077f912c4d8a29fbe3ceaf404aaeecf39d665a7b450dec70e25f7`）。这验证了记录的程序路径和字段，但不增加其数学量词。

## 3. 历史 README 的独有边界

伴随 README 不是新证书。它准确记录了该分支没有完整证明、没有真正 half 反例，也没有新增已支付的一般福利关系；三窗菜单独立复核只检查一个局部获利偏离，不是新障碍或福利结果。它还撤回更强的 `|O\C|\le W` 桥，保留

\[
 |O\setminus C|\le |I|+2|G|,
 \quad I=O\cap C,;G=C\setminus O,
\]

并说明后续银行完整族才承担逐人 DIRECT/PREFIX 的真正反驳。该 README 的独有作用是把有限锥记录放回历史分支，防止把“无负点”误写成正面普遍定理。

## 4. 和后来银行族的关系

既有银行族对象给出 `m\ge5` 的完整根纯 SPE 逐人门槛反例：`u_1=1+1/(m-1)`、`W=2m`、`OPT_m=3m-2`，从而 `OPT_m/(2m)-u_1>0`。本批不重新证明银行控制器，只把 R29 的固定锥有限检查与它比较：前者没有覆盖后来银行实例，也没有覆盖所有 SPE 锥；后者才负责完整历史量词下的逐人加强失败。两者不冲突。

真正六人目标仍是：六人、六提供者、有限单位客户、完整有序历史纯 SPE，终局客户价值在覆盖者间均分；现有固定锥“无负点”不触及该全称命题。空主题、重复、零客户和任意平局仍留在模型边界内。

## 5. 接续义务

若继续研究该候选，必须先扩大固定策略锥到完整纯 SPE 策略空间，或者证明某种锥覆盖定理；随后要给出有理对偶/最小性证书，而不是只增加浮点 LP 点。若目标是证明真正 half，则还要把逐人收益、共同客户支付和 `|O\setminus C|` 的真实偏离预算接到同一完整历史证书。当前这三份来源准确处置为“有限复核已完成、一般命题开放”。
