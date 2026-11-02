# 独立静态CCE审计的两个策略版本

本包九份主来源共71,609字节，均从`work.py clean show ID --out`正常取得，按`source-manifest.json`核冻结大小及SHA-256。它们来自同一旧工作区`independent_bottleneck`；原件从未修改。两个冻结分支位置同字节，不算两次证明。

`original/independent_cce_audit.py`默认检查42单位客户，`--small`检查8单位客户，两入口都使用早期有序策略σH。`original/count_policy_cce_audit.py`检查8客户的另一计数统一策略σC。三入口各仅在原字节隔离副本上有限运行一次，均exit0、stderr空；没有新实例扫描。保存的真实本轮stdout、stderr、完整新报告和执行事件见`runs/`，总核对见`verification.json`。

| 本轮入口 | 精确有限范围 | 新报告与冻结报告 |
|---|---|---|
| independent默认 | 21历史84比较，64有序静态列；W32、OPT42、CCE下界33 | 不全字节/不全JSON相同。新增两个simple顶层字段和64行simple_dual_value；只删这些新增字段后旧结构逐字段完全相同。 |
| independent --small | σH，21历史84比较、64有序静态列、11点原始分布、12个体CCE约束；W6、OPT8、锐值544/87 | 全JSON及字节相同。 |
| count_policy默认 | σC，21历史84比较；W6、各人2；不自行核静态CCE | 全JSON及字节相同。 |

复验命令：`python3 archives/customer-attraction/tools/evidence/independent-cce-ordered-count-versions-primary/replay_bundle.py`。程序会核九源SHA，再把原脚本复制到新临时目录运行，避免其自动写同目录JSON覆盖冻结输入。stdout只含摘要；完整逐行结果由原程序在副本目录生成，二者均保存。42的33是固定非负对偶的逐终局下界，不是已给达到分布的CCE精确最小值。8客户的原始/对偶匹配才给精确最低值544/87。

两策略只有历史(1)与(1,2)的动作不同；σC的存在不推出一般计数净化。完整数学、版本比较、逐源去向和接续边界由对应正式资源对象给出；本包的重跑不新增外部审查人，不处理六人half。
