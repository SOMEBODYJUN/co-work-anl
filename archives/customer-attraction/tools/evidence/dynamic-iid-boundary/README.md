# 动态iid背景与固定策略条件支付证据

本目录初批保留六份冻结原字节文件、三份原审计的真实运行输出及一份补充定义重构；续批另保留两份原始运行JSON、内部审查和英文底稿，共十份原字节文件。正文分别为[残余值/租金定理](../../../state/定理/合法前缀残余独立同分布价值与租金--定理.md)、[实际前缀局部反例](../../../state/反例/实际前缀的独立同分布局部漂移--反例.md)、[固定策略条件证书](../../../state/定理/六主题三人固定策略的条件独立支付--定理.md)和[计算范围](../../../state/计算/动态独立查询与条件支付的精确核验--计算.md)。初批源定位、大小、哈希及环境见[PROVENANCE.json](PROVENANCE.json)，续批四来源见[frozen-four-provenance.json](frozen-four-provenance.json)；初批记录中的旧运行未比较标志只描述初批，不抹去其当时范围。

在本目录运行以下命令即可只读重算并打印；默认不覆盖已保存输出：

```sh
python3 original/tests/audits/customer_attraction_dynamic_iid.py
python3 original/tests/audits/customer_attraction_dynamic_iid_independent.py
python3 original/tests/audits/customer_attraction_iid_conditional_cone.py
python3 check_semantics.py
python3 check_frozen_reports.py
```

前两份原审计允许显式 `--input`、`--certificate`、`--output`。`--output` 使用独占创建，已有文件将报错；本轮以仓库外新路径运行后才复制结果，不改冻结输入或旧报告。第三份原审计按脚本相对位置读取 `original/evidence/certificates/customer_attraction/iid_security_conditional_36.json`，所以保留原路径层级。四个脚本均只依赖Python标准库。本轮未跑规范CLI验证器，不把旧审查中的规范验证结果当作本轮运行。

`replay/dynamic.json`核全部2801历史19607项比较及56组有限多项式系数；`replay/dynamic-independent.json`展开60单位客户并算全部16807终局；二者分别重建三个残余静态KKT状态。`replay/conditional.json`核固定六主题三人策略的全部63客户列有理分解，并算36客户点的流余项。`replay/semantics.json`额外核动态完整平局规则、实际偏离表、固定均匀分布的194/9残余支付、条件36权重点的全部258 SPE比较与六条静态NE等式。

`check_frozen_reports.py`实际只读运行两份原审计，把完整stdout与两份冻结历史运行及上述初批重放逐字节对照；另独立按二项式公式重算三个残余态的全部七查询、势、支付、租金和覆盖，以及 $PPX0$ 旧均匀分布的完整账本。输出[frozen-reports.json](replay/frozen-reports.json)为PASS；两份冻结JSON不是另一个独立实例，报告哈希和输入/证书绑定全部一致。内部审查的第三路数学重算和规范CLI结果只按原文记载，未冒称本批另跑；旧底稿的全局OPEN文字由正式正文解释其后续纠正。

两份动态原审计互不导入且不导入构造器或规范求解器；条件原审计也不使用优化器。补充代码不导入三份原审计。本轮实际读取并重放这些既有独立实现，并补充一个已知证书的定义重构；不声称外部盲审。动态有限反例只否定原总人数系数的逐节点iid漂移；本例满足全局弱桥。条件证书只证明固定策略和固定均匀q对应的条件客户锥。普遍强弱iid桥已由其他反族否定，真正安全值聚合桥与六人一般half仍另论。一般凹势/KKT及租金/债务恒等式的正确性依赖正文解析证明，不能由有限程序结果代替。
