---
id: "customer-attraction/r2fc-background-induction-artificial-probe-and-two-player-fresh-template"
kind: "computation"
type_tag: "计算"
title: "R-2fc 背景人工负载探针与两人 fresh 证书模板"
status: "finite-experiment-and-template-obstruction"
truth_status: "artificial-negative-search-finite-only; universal-coefficient-template-infeasible"
review_level: "source-bytes-read-and-reexecuted-with-captured-output"
scope: "R-2fc8878b4bdd4328bbc1bcf1df8ca831/background_induction 下两份程序；q=6、剩余两人、人工背景有限随机试验与二值 fresh 系数模板"
summary: "artificial_background_probe.py 在放宽的独立背景类型上按默认 200 次随机试验未发现负候选；two_player_fresh_certificate.py 对 64 个二值类型、192 行（fresh、p=1、斜率）构造的非负 slack LP 返回 infeasible。两项都不是合法 CAG 六人 half 证书：前者没有共同目录产生的合法过去，后者只否定这一特定系数模板。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-2fc8878b4bdd4328bbc1bcf1df8ca831/background_induction/artificial_background_probe.py"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-2fc8878b4bdd4328bbc1bcf1df8ca831/background_induction/artificial_background_probe.py"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-2fc8878b4bdd4328bbc1bcf1df8ca831/background_induction/two_player_fresh_certificate.py"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-2fc8878b4bdd4328bbc1bcf1df8ca831/background_induction/two_player_fresh_certificate.py"
---

# 对象边界

本页依照[共同目录、均分价值与完整历史纯SPE](../定义/共同目录完整历史模型--定义.md)记录两份已认领源码的实际语义、运行结果和可复用范围。共同目录模型的合法输入是有限单位客户、有限非空共同主题目录、按固定次序观察全部有序历史各选一次主题，以及所有离轨历史上的完整纯SPE。任何背景负载都必须由同一目录中的过去主题行动产生；不同有序历史即使留下相同计数，也不强制共享续局。

这两份源码都位于 `R-2fc8878b4bdd4328bbc1bcf1df8ca831/background_induction/`。源码原字节已保存于[本批证据](../../tools/evidence/R-2fc-background-induction-20261031/)，SHA-256 分别为 `9765d276e0a2441a754c7f10426be48da79ddb6b938c83fe510eb1d142d3a2d5` 和 `ce97b69091244b64c745a88b52f4e70a1b07d1778b262d9a286e2f7fac6bcfa4`，与冻结清单一致。`clean show` 已按两个 source ID 实际调用；冻结 blob 需要远端 promisor fetch，但当前浏览器代理端口不可达，调用分别以退出码 1 失败。随后从对应冻结提交的公开 raw 页面读取完整正文，并用上面哈希逐字节核对；失败输出、原文副本和运行材料均保留在证据目录，不打印任何凭据。

# `artificial_background_probe.py`：人工背景的有限探针

## 程序做什么

默认参数为 `q=6`、`trials=200`、`seed=982327`，剩余人数固定为 2。程序把每种非空标签掩码 `mask∈{1,…,2^q−1}` 与一个独立的背景数 `b∈{0,1,2,5}` 配成类型 `(mask,b)`，共 `63×4=252` 个类型。`member` 记录客户是否接受各标签，`bg` 直接取这些独立指定的 `b`，`fresh` 只保留 `b=0` 的类型。对每个动作对 `(a,b)`，收益系数使用

\[
\frac{\text{member}}{\text{bg}+\text{member}_a+\text{member}_b},
\]

分母为零的项由程序置零。每个随机试验为每类抽取一个非负整数权重：以 0.2 概率取 `randrange(20)`，否则取零。接着，分别为每个首动作 `a` 选择使第二位回复 `b` 的收益最大的标签（平局随机打破），再从这些回复构造第一位的最大收益动作。`rows` 收集所有第二位与第一位单步偏离差，LP 约束为 `-rows·w≤0`、权重和为 1、权重非负。

对每个两标签比较集 `comp`，目标是

\[
\text{profit}_{(first,last)}+\text{fresh 新覆盖}_{(first,last)}
-\text{fresh 新覆盖}_{comp}.
\]

一旦 LP 严格小于 `-10^{-8}`，程序会写 `artificial_background_candidate.json` 并打印 `FOUND`；否则每 25 次打印进度，完成全部试验后打印 `completed`。源码文档字符串已经明确这类输入是“not represented by legal past topics”，即人工扩大模型；发现点也不能直接称 CAG 反例。

## 实际运行

在独立副本目录运行默认入口：

```sh
python3 artificial_background_probe.py
```

结果为退出码 0，实际耗时 10.552999 秒，时间边界 120 秒；stderr 为空。stdout 逐字保存于 `run/artificial/stdout.txt`：试验 0、25、50、75、100、125、150、175 均报告 `no negative candidate`，最后为 `completed 200 no negative candidate`。程序没有生成 `artificial_background_candidate.json`，其缺失已在 `run-manifest.json` 明确记录。

这是一个“有限实验”，其量词只是固定随机种子、固定 252 类人工权重模型和 200 次随机抽样中没有找到候选。它不量化所有共同目录、所有合法过去、所有客户权重或所有完整 SPE；未发现也不推出普遍非负，更不能升级为六人 half 正面结果。

## 合法 CAG 缺口

在合法 CAG 中，客户类型的重数可以按接受标签集合压缩，但 `b_x` 必须由同一共同目录中的过去有序主题产生，且同一客户类型的负载由其接受标签与该过去行动共同决定。此程序让 252 个 `(mask,b)` 类型彼此独立，直接把 `b` 取 0、1、2、5；没有过去行动、目录、客户集合或完整有序历史可以回放这些负载。因此它只探测“人工背景输入接口”是否在该随机子类上出现负点，不能成为合法背景反例，也不验证原 CAG 的 SPE 量词。

# `two_player_fresh_certificate.py`：两人 fresh 的特定证书模板

## 模板和量词

程序使用六个二值成员标签 `LABELS='ABTSQR'`。`LAST` 由三组末位比较组成：在 `(A, predecessor=A)` 下选择 `B` 后比较其他五个动作；在 `(T, predecessor=T)` 下选择 `Q` 后比较其他五个动作；在 `(S, predecessor=S)` 下选择 `R` 后比较其他五个动作。再加两个根比较分支 `root_T`、`root_S`，共 17 个非负 slack 变量。

对 64 个二值 incidence pattern `bits∈{0,1}^6`，程序分别计算：

1. `p=0` 的 fresh 行；
2. `p=1` 的 occupied-at-1 行；
3. `p=1` 到 `p=2` 的收益斜率行（因为每个 occupied 客户的分子是 `p` 的仿射函数）。

每个 pattern 贡献三行组，因而总计 `64×3=192` 行。右端用 `target(bits,p,fresh)` 表示目标的 fresh 覆盖和 occupied 背景下的仿射增量；左端由 17 个 slack 乘子给出。`scipy.optimize.linprog` 试图在 slack 非负条件下最小化乘子和。若找到可行解，程序会把浮点乘子取有理近似，逐行检查精确 Fraction residuals 非负，并写 `two_player_fresh_certificate.json`，其声明范围是“P+Delta >= fresh_OPT_2 at every fixed background”。

这个模板的全称是：对每个独立二值客户成员模式、fresh 背景及用仿射斜率代表的正整数背景，试图用同一组根/末位比较非负余项支付两人 fresh 最优覆盖。它没有枚举共同目录、客户重数、完整有序策略树或任意平局的可达性，也没有把 LP 可行性等同于 SPE 存在。

## 实际运行

在独立副本目录运行：

```sh
python3 two_player_fresh_certificate.py
```

结果为进程退出码 0、实际耗时 0.772910 秒、时间边界 120 秒、stderr 为空；stdout 唯一内容为：

```text
The problem is infeasible. (HiGHS Status 8: model_status is Infeasible; primal_status is None)
```

由于源码在 `not res.success` 分支只打印 solver message 后 `return`，所以 shell 退出码 0 不表示证书成功。没有写出 `two_player_fresh_certificate.json`；该缺失以及 stdout/stderr/status 的哈希均见 `run-manifest.json`。实际结论是：**这一组预先选定的 17-slack、192-row 非负系数模板不可行**。它不是“存在合法 CAG 反例”的证明，也不是所有可能系数、所有两人证明或所有 fresh 量词都不可能的证明；需要另找证书结构，或在合法实例上独立构造完整有理反例。

## 与既有正文的准确关系

[背景首步反例发现与精确重放](背景首步反例发现与精确重放--计算.md)的历史 README 已把两份程序分别记作“人工背景有限试验”和“两根比较/末回复/跨末节点三分支非负系数模板不可行”。本批完成了这两项的原文实读、哈希核对和默认入口重跑，但运行结果不改变既有 23/488 客户合法背景首步反例的范围：它们只否定逐步 `u+a+O_{r-1}(b+1_A)≥O_r(b)`，而其整体余额仍为正（分别 `47/10` 和 `104`）。后续 52 客户根路径证据另行否定整体 `P+Δ≥O_r`；这些对象都不能被本页两份有限/模板结果替代。

[固定背景下恰两名剩余玩家的税界](../引理/固定背景两人税界--引理.md)证明的是另一项有真实偏离回复的任意两比较主题利润上界。这里的 fresh LP 模板试图支付 `P+Δ` 与 fresh 二主题覆盖的特定系数组合，且在其预选系数空间不可行；两者量词、对象和证明接口不同，不能把本 LP 的 infeasible 误写成既有两人税界失败。

Q-CAG-HALF-6 的目标仍是对**所有**共同目录、单位客户和完整六人纯 SPE 证明 `2W≥OPT_6`。本批既没有合法六人输入，也没有六人完整策略树、普遍量词或根/离轨 SPE 证书；因此不升级、不削弱该六人 half 命题的状态。

# 证据和复现

[证据目录](../../tools/evidence/R-2fc-background-induction-20261031/)保存：

- `source/`：两份与冻结 SHA 完全一致的源码副本；
- `clean_show_attempts.txt`：两个 `clean show` 实读调用及远端不可达的退出码 1 原始输出；
- `run/artificial/`、`run/two_player/`：原始 stdout、stderr、时间边界、运行副本；
- `run-manifest.json`：源 ID、完整提交、哈希、命令、时间、退出码、输出文件和“未生成 JSON”状态。

重跑依赖 Python 3.12.14、NumPy 2.3.5、SciPy 1.17.0。源代码中的默认参数未改写，运行只在证据独立副本中进行；没有 git/checkpoint/done 操作。
