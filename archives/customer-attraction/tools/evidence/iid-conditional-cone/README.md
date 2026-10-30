# 固定三人六主题条件独立支付证据

本目录保全三份本批冻结来源、两份仅供复验的已有证书/审计，以及新写的兼容依赖和定义级核验。来源逐项路径、两个完整冻结commit、字节数与SHA256见 `PROVENANCE.json`。本批只认领的三源为 `83e2c17503487ad17ccf`、`c33bc23b30923b1599aa`、`d20de7b503c8668a5cb5`；参考证书及审计未冒记本批完成。

数学解释见[支持恢复计算对象](../../../state/计算/条件独立支付证书的支持恢复与精确复验--计算.md)及[条件定理](../../../state/定理/六主题三人固定策略的条件独立支付--定理.md)。原生成器缺少外部导入 `symmetric_ne_bridge_attack`，直接运行的失败保留在 `replay/original-generator-unavailable.json`；新依赖是按定义重构，不冒称原模块。

从仓库根运行：

```sh
python archives/customer-attraction/tools/evidence/iid-conditional-cone/original/tests/audits/customer_attraction_iid_conditional_cone.py
python archives/customer-attraction/tools/evidence/iid-conditional-cone/run_generator_reconstruction.py
python archives/customer-attraction/tools/evidence/iid-conditional-cone/verify.py
```

第一项只需标准库，实际输出已保存为 `replay/original-audit.json`，与冻结运行JSON逐字段相等。第二项需要NumPy/SciPy，运行未经修改的冻结发现代码和显式重构依赖；输出与冻结证书全部字段相同。第三项只需标准库，独立检查冻结与生成证书全部63列、全部乘子、36客户点258项完整激励及自然前缀流。它不导入前两项、兼容依赖或SPE求解器。

`replay/definition-check.json`给实际精确核验；`generator-reconstruction.json`记发现运行模式和版本。证书证明整个固定策略/固定均匀分布的条件客户锥，有限运行没有认证任意策略、任意分布、一般人数或六人half。旧底稿的强桥开放状态被后续真实SPE反例取代，静态定理及此特定正证书不受影响。
