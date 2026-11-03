---
id: customer-attraction/signed-harmonic-cone-probe
kind: computation
type_tag: 计算
status: source-read-diagnostic-only
truth_status: floating-discovery-LP; no-negative-candidate-claim
source_refs:
  - clean:c0b7eec3d3f90abbec9e:research/workspaces/customer-attraction/R-12bf6a96d24c48eca828620d6642e203/signed_harmonic/cone_probe.py
---

# signed-harmonic 策略锥 LP 诊断入口

完整实读 3864 B script（SHA `abe9a7904da5e1e709a8a8c28546662fd40bb52d2f67bfcd53c42584ca75650e`）。它随机生成完整计数策略，构造激励锥、重复最优元组和 harmonic/linear 目标，使用 SciPy LP 探索负候选，必要时用 MILP 做整数恢复。README 记录既有 trials 未分离且主动停止，不把浮点无分离写成证明。本批未运行；脚本依赖 NumPy/SciPy 和 customer-attraction 结构，不能升级一般 budget 或 half。
