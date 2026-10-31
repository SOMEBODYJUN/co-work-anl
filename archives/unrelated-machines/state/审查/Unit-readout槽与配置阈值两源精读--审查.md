---
id: "unrelated-machines/unit-readout-slots-and-configuration-threshold-two-source-review"
kind: "review"
type_tag: "审查"
title: "Unit-readout 槽与配置阈值两源精读"
status: "typed-forest-read-fixed-D-boundary"
summary: "两份 review 确认 unit-readout typed forest 的 calibrated cardinality slots/bounded-density 算法、严格单位 5/3 与 closed-tree threshold 合同：一次全局 Hall 匹配给完整原 jobs 实际 assignment；固定 D 给 2−1/(4D) 受限比例，k<D fallback 失败即 OPT=2；正部 CONFIG 与闭合两树阈值双向成立。均依赖唯一 incoming、统一 small/unit 资格和固定-D/closed-tree域，不升级一般 UM。"
source_refs:
  - "clean:d8c5ebc428447d7c968c"
  - "clean:29d5e565ca37bcc9cbd8"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/reviews/unrelated_machines/unit_readout_calibrated_cardinality_slots_review.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/reviews/unrelated_machines/unit_readout_configuration_threshold_review.md"
---

# 来源与范围

`d8c5ebc428447d7c968c`（SHA `91d7cd4c34a39da263ca64e8bc9cecfe1d6376be2a0ef57f2c0b91c3dd004fa2`）审 calibrated cardinality slots/bounded-density；`29d5e565ca37bcc9cbd8`（SHA `d6ba5e4738e07a1085082d0dae86ce8c13b68dc472fcd73c9ad7a1870fb2f042`）审 positive-part CONFIG、strict-unit gap 与 closed-tree threshold。两源均 clean show 全文实读，导出与 manifest 在 `archives/unrelated-machines/tools/evidence/unit-readout-20261031/`，receipt 草稿在 `cleanup/workspaces/Boss2/unit-readout-receipts-20261031.json`。

# 1. Calibrated cardinality slots 与 bounded-density

每个内部 row 有唯一 incoming unit、`k` 个统一 `1/k` small；incoming 质量 y 加 small 质量 `1−t` 满足整数槽预算 `y+Σ(1−t)≤L=k−r+1`。树/端点真实资格由同一次 Hall 匹配覆盖，不逐机分别匹配；incoming 占首槽、small 可跨相邻槽，质量 Hall 而非每槽半片计数。每原 job 全列质量恰1，输出全部原 jobs 的真实 assignment；内机负载至多 `1+(k−r)/k=C_r`（incoming row），无 incoming row 至多1，外 unit 机至多一 port。

校准递推 `x_h=a+(1/2−a)/k^h`、`a=(r−1)/(k−1)` 给统一分数 witness；k=1 旁路。给定真实 C=1 witness 才必有整轨 LP，不能把一般 OPT 直接写成 5/3。固定 D 密度 `d_c≤D A_c` 时，k≥D 分支给 `x_h≤1/D`、`r/k>1/(4D)`，实际峰 `C_r<2−1/(4D)`；k<D 用变量到 clause capacity matching，成功走一条真实路径，失败则任意 C<2 调度会提取容量匹配，故 OPT=2，all-parent assignment 是精确最优。D 必须固定才有统一 ε；D 随输入/目标变化不升级一般 UM。

槽审计覆盖给定 witnesses、固定 D、空/非法/大分母输入；没有通用 LP solver、全结构类 OPT 生产实现或一般 hardness。VW Theorem7 已有 `2−1/k` 是外部经典改善，本对象不认领其新颖性。

# 2. 正部 CONFIG、严格单位 5/3 与闭合两树

正部“iff”充分方向不能只用下界 `z≥q−t` 与总和；正文取最小 `c=(q−t)+` 并裁剪到合法联合概率区间，q=0/1、s=0 旁路。每枚 small 串接圆段 ≤q，每点覆盖 ≤s，含 incoming 配置真实负载 ≤`1+s/k`，外机 singleton，父/子边际共享同一组 t；局部分解不要求一个全局联合分布。

严格单位多数轨：activearity≤2A；未选轨 density 可无界，未选轨全 parent，不能对其强加 active LP。active incoming 先槽，列和1，一次 Hall 匹配共同计费 selectors/edges/leaves/inactive jobs；root 与 non-root 都包含。k=1 用整数容量流。只在存在 C=1 witness 时得到整轨 LP，不声称一般 OPT 5/3。

严格阈值 `s0` 强迫 child t≥incoming，整轨 LP 恰 CONFIG1；`s1` 允许一 incoming 带一 small，层边际可衰减。闭合两树条件 `(k−s)^h≤2k^(h−1)` 有必要/充分双向，经典 `α_h≥1/2` 与 `Tconf=1+1/k` 在 k≥3、s0/s1 量词下精确。one-hot 应用中正文字上界1、负文字上界字母数−1；只有重复/平衡后仍保共同整轨 LP witness 的编译适用，未构造完整 Label Cover reduction。

整轨见证程序实际枚举有限 cases 并重算 all original jobs；独立单行配置分解以 Fraction 认证正/负网格点。软件只支持证据与给定 witness，不提供全局 LP/OPT oracle。

# 3. 对象关系、依赖与未解

两源都使用唯一 incoming、统一 small 时间、共同 unit 资格、显式树深度和一次全局槽匹配；这些不是一般 UM 前提。VW/ST/Hall/CONFIG 等是经典工具，不能由本 review 改写为新颖性。fixed-D `2−1/(4D)`、strict-unit `5/3`、closed-tree `Tconf` 各有独立量词，不能互相替换或外推到任意 machine matrix。

未提供一般 UM `2−ε` 算法/硬度、全配置输出器、真实凸包点求解、Label Cover reduction 或当前六人 SPE 结论；外审/全球新颖性未认证。处置为 `typed-forest-read-fixed-D-boundary`，引用时须保留 fixed D、k<D fallback、strict unit、CONFIG1 与 closed-tree 前提。
