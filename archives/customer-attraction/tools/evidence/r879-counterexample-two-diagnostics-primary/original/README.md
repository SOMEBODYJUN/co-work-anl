# 独立反例攻击工作区

2026-10-23，目标为一般Q-CAG-HALF的真正反例；未发现反例，目标仍OPEN。

## 当前资产

* `shared_omission_bank_baseline_no_go.md`：共享遗漏、目标相关任意银行、共同逐客户银行基线的单目标重复惩罚停界。仅两末位BR已强迫所有目标遗漏相同、每支一次惩罚、有效组核值相同。含带符号收益差与非负总损失精确恒等式；个人探索ID CA-WS-SHARED-OMISSION-SINGLE-TARGET-BANK-BASELINE-NOGO-v1，待独立团队审查。
* `targeted_shared_omission_suffix_obstruction.md`：原共同银行版本的合并指针；不重复正文。
* `audit_shared_omission_suffix.py`、`shared_omission_suffix_audit.json`：8组显式单位客户/Fraction回放，全部恒等式精确通过；不是SPE证书。

已查旧稿R-486bb9adb8cd4d9a940dbf3b1ab0b1de/credible/common_terminal_exchange.md：复用先审真实末位菜单的思想。本稿不需其早期common-terminal交换身份，但限定重复同一惩罚主题与共同银行基线；正文写明范围区别，不作新颖性断言。

## 下一步

构造必须让尾部惩罚分散到不同主题、先加载其他遗漏，或让真实分支改变银行基线。仅增加重复次数、更换目标银行H_i都被现有两目标恒等式排除。先检查完整末位菜单，再考虑根激励；不要继续同模板调参数。

## 后续指定接口诊断

`insurance_menu_mean_diagnostic.md`及`audit_insurance_menu_mean.py`、`insurance_menu_mean_audit.json`：只诊断现成双早期Cartesian保险族能否击穿局部加强ψ(p)≤D(p)。找到了一个对全部查询逐行支付真实对应根偏离收益的共同完整端点列，因此该机制和空稀释均不能击穿；一般候选未证。3组合法参数共27行显式单位客户Fraction回放通过。已直接向smoothness_duality和root报告，未继续扩样。
