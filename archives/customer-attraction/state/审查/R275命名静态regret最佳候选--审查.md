---
id: "customer-attraction/R275-named-regret-single-best"
kind: "review"
type_tag: "审查"
title: "R275 命名静态 regret 最佳候选"
status: "finite-floating-candidate-reviewed"
truth_status: "candidate-with-positive-slack; no-universal-regret-theorem"
summary: "冻结 named_regret_single_best.json 保存一个 p=n=4 的命名静态 regret 锥候选；目标为 fractional_actual_load_failure，归一化权重下报告 slack=1/17，未给出整数客户实例或完整纯 SPE 证书。"
source_refs:
  - "clean:4a6b1f292d8e46cd1d6c:research/workspaces/customer-attraction/R-27557809587746c59216a46867c9eb07/direct_global/named_regret_single_best.json"
  - "clean:768d1e5c2d6213be6e42:research/workspaces/customer-attraction/R-27557809587746c59216a46867c9eb07/direct_global/named_static_common.py"
  - "clean:f33ccbb3431f96f3ee85:research/workspaces/customer-attraction/R-27557809587746c59216a46867c9eb07/direct_global/named_static_common_best.json"
  - "local:archives/customer-attraction/tools/evidence/R275-named-regret-agent/manifest.json"
evidence_paths:
  - "archives/customer-attraction/tools/evidence/R275-named-regret-agent/named_regret_single_best.json"
  - "archives/customer-attraction/tools/evidence/R275-named-regret-agent/named_static_common.py"
  - "archives/customer-attraction/tools/evidence/R275-named-regret-agent/named_static_common_best.json"
---

# 来源身份与搜索语义

主源 `4a6b1f292d8e46cd1d6c` 是 2,403 字节 JSON，冻结 SHA-256 为 `951ecd71171058fe82d93064a67540921587a7e84e3e886dfaae0f6eb73e5a15`。名称为 `fractional_actual_load_failure`，参数 `p=4,n=4`。JSON 保存 15 维权重、根终局计数 `target=[1,3,0,0]`、测试动作 `a=2`、整份 85 历史策略表和一个数值 `slack`。权重含 0.1764705882、0.1176470588、0.7058823529 等分数近似，说明它是 fractional 候选；文件没有给出整数客户重数、客户主题集合或独立全历史效用证书。

相关 `named_static_common.py` 从既有策略证书构造 `gamma` 激励行，使用 `Gx≥0` 的策略锥、覆盖归一化和静态公共负载表达式，逐动作最小化目标。该接口解释了 JSON 的“命名 regret”语义，但相关脚本本身也只运行浮点 LP；`named_static_common_best.json` 是同类扫描的另一保存点，不能倒写成主源的精确证明。

# 候选字段及边界

`target=[1,3,0,0]` 表示候选终局主题计数，`a=2` 是被测试的动作。`policy` 列出长度 0 至 3 的所有历史动作，共 `1+4+16+64=85` 条，因而它确实携带一份完整策略表的候选表示。报告的 `slack=0.058823529411764705=1/17` 为正，表明在该浮点权重和该目标下，扫描器没有发现目标方向的负 regret；它不是“已证明存在严格 SPE”的证据。

权重向量的 15 个坐标对应四主题非空客户类型的枚举位序，但本 JSON 没有把坐标恢复为整数客户数，也没有展示每个历史的精确收益差、平局规则或有理对偶证书。因此不能把 `slack>0` 解释为任意客户分布下的激励定理，更不能据此推出六人半覆盖。

# 可复用内容与后续缺口

可复用的是把一个命名的静态负载方向写成策略锥上的线性目标，并在保存点同时记录完整历史动作表、目标终局、被测动作和归一化权重。后续若要升级结论，必须从 15 维权重恢复具体整数客户实例，逐历史用 Fraction 重算 `G` 和效用，明确所有离轨平局，并把静态 regret 目标与真实终局福利/客户覆盖量词分开。

本来源应保留为有限候选与算法接口证据。正 slack 是该候选的边界信息，不是普遍 regret 上界、半覆盖反例或定理。
