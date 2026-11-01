# 共同客户匹配损失与相邻负载正性

本分支继续一般Q-CAG-HALF；主目标仍 **OPEN**。本轮得到任意q,m可用的共同客户
匹配损失的显式非负层分解，并在真正完整类型727/728松弛点上发现严格joint-only
非补全证据。它们尚未提供将各分支损失付到根福利W的机制。
精确身份、审查程度和局限见 `CLAIMS.md`。

## 已证材料

- `shared_incidence_loss.md`：任意负载、任意有限加权多菜单的非负层分解；两菜单
  loss 的梯形整数系数；共同前缀倒三偏离族的两级负载闭式。对D行用菜单补位
  化为同一正性公式。末两人交叠和全部五种pair索引等号模式未被删去。
- `verify_shared_loss.py` / `shared_incidence_loss_checks.json`：零导入独立精确重建；
  9360条多菜单层恒等式、9008条双菜单整数系数恒等式、69原子的逐标签全匹配
  最大值与有理余量。解析证明承担任意q,m结论。
- `exact_joint_727_separation.json`：AB源查询second族V,W；单O余量均正，而joint
  OO余量约−0.1326305442207082。父分支已另行零导入枚举独审。
- `exact_joint_728_separation.json`：AB源查询AE族R,S；单O余量约(0.11756614924,0)，
  joint约−0.1097318191173584。只排除该点，不是完整模板或一般SPE上界。
- `adjacent_load_signatures.md`、`verify_adjacent_load.py`、`adjacent_load_checks.json`：
  同一分支上相邻真实前缀负载的两边缘唯一恢复联合；累计分布交错是精确正性条件。
  这使terminal+pair混合支持函数可从两种兼容签名恢复共同source成本。

## 浮点探索材料

- `joint_pair_feasibility.py` / `.json`：固定最终717点，对second→AB/AE的每组30个
  pair-orbit行检验同一transport；结果数值可行，不升级成精确可行性或SPE。
- `multimarginal_feasibility.py`：固定客户原子及质量，变量为三个记录族在同一
  客户的联合槽计数；同时保留220个cross-pair真实五型行和选出的cross-terminal行。
  输出`multimarginal_<输入文件stem>.json`。已有727与728结果；旧无输入后缀报告
  是727点，已按源文件名改名。所有数值可行/不可行只作发现，727核心分离已另行精确化。
  可重建的浮点求解器数组未作为数学证书保留。

运行示例（仓库根）：

```sh
python research/workspaces/customer-attraction/R-c4732bee2f7b4e50a70568170e3334ae/round5_coupling/verify_shared_loss.py
python research/workspaces/customer-attraction/R-c4732bee2f7b4e50a70568170e3334ae/round5_coupling/verify_adjacent_load.py
python research/workspaces/customer-attraction/R-c4732bee2f7b4e50a70568170e3334ae/round5_coupling/multimarginal_feasibility.py research/workspaces/customer-attraction/R-c4732bee2f7b4e50a70568170e3334ae/round5_pricing/exact_optimum_primal_joint_terminal.json
```

## 下一承重义务

共享loss的正性意味着各菜单不能分别占用同一批低背景槽。下一步是把这些loss
在同一个完整策略的不同真实前缀之间联合收费，使最终总收费由根W控制。
目前每个source family的actual-share项和负载跳跃仍在该离轨family；不能把它们
直接等同或有界于根路径收益。既有根总税反例也阻止直接求和所有分支self-tax。

继续可尝试：在共同前缀树上找到允许局部欠账的望远镜权；或保留同一客户跨全部
目标菜单的联合直方图，联合早期真实偏离行，让必要的负载跳跃预算自己消去。
这些均是候选，不是已经建立的支付引理。不再无限逐点增加少量行追小数常数。
