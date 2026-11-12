# visible_maximum_joint_v6_solve：正式释放后的 preflight 障碍

**状态：STOPPED_PRECONSUMPTION_SOURCE_PIN_SCHEMA_MISMATCH。** Main 已明确释放原一次完整 4177 行求解；本席按冻结入口执行 preflight 时发生接口不匹配，因此没有进入优化器。当前实际优化调用为0，单次额度未消费。

身份：Boss1 / six-boss1-20261111 / `/root/visible_joint_v6_solve` / full。

## 已实读并核对

- Main release SHA：`eef504e3ad50d3e2f901e12a8689a95415986be2552c73cd885041e4d8dbdbaf`。
- 独立 X 更正 SHA：`a2b83e67ce90597faa005cb893da647555bbb58b0d502fd3f03c12db924172b7`。
- Main 语义释放 SHA：`36cdf31f302aefc738a300b9b25a5b29ef9a97e85bdf0499c2beba50bc153c85`。

准确模型已写入 `model_erratum_read_binding.json`：固定完整纯 SPE 的实际 A1,…,A6，令 P_y 为实际前四动作负载；一次选 X∈argmax_Q Σ_{y∈cov(Q)}1/(P_y+1)，最大化范围是整个共同合法标签目录。同一个 X 用于全部会员位、查询和强制分支；不声称它在其他背景下仍最大。C 是最大裸覆盖标签，O 是达到 OPT6 的六合法标签覆盖并；只在 OPT6>0 时归一化。新增局部任意合法 T 可特化为该 X，但不能取消继承旧行所需的 X 最大性。

## 实际停止位置

`preflight.py --released` 返回退出码1，在冻结 `contract.py:355` 抛出 `ValueError: Explicit source closure is required`。该 gate 要求顶层非空 `sources` 字典；实际已冻结、SHA吻合的 source_pins.json 为 `schema=v6_exact_read_set_pins_v1`，顶层只有 `schema/read_scope/files`，`files` 是带 path、sha256、bytes 的列表。实际清单有 44 个路径唯一且字段合法的条目。程序在读取该清单所列来源、全部模型校验和消费标记之前停止。

source_pins SHA：`d90e383c1824ea5b3eebb8fbe93b9c53c6a071bb72684740f25f28492c6a5fc0`。输入 SHA 仍为 `8f953bca6b65a8093d5fcf0fdb5a432ba3603137fe1015cd06fc8f6324e68769`；输入、源码、冻结清单都没有修改。此处不是数学不可行或数值求解失败，也不是完整输入已经通过 gate。

`single_lp_consumed.json`、`source_pins_at_solve.json`、`discovery_output.json`、`released_preflight_result.json` 均不存在。没有调用 solve_once，没有点、证书、最优值或最优面结果。不会自行适配 frozen gate 或重写来源清单；等待 Main 明确处理并重新绑定这个接口后再继续。

源准备和脚手架的已推送 checkpoint 由 Main 指定为 `b03738737870367e2da8a091d4d6f0e26b16d892`。Main release 和本次障碍记录是本地新增，未冒称已推送。Git、RUN、map、registry未修改。原静态冻结摘要保留在本包 `scaffold_summary_before_release.md`。
