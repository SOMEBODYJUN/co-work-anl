# 两步安全链攻击程序及三份四人记录

模型边界补注：本包按程序标签接口保留同覆盖异标签。严格集合目录下，覆盖互异者直接适用；别名点若合并，须另证完整有序策略、背景与真实后继下降，本文不默认。原标签、原件、数值、策略账本和所有旧运行事件均保留；本次只改说明与静态指纹，未新增数学运行。

正文：[两步安全链的自适应策略锥攻击与三份四人记录](../../../state/程序/两步安全链的自适应策略锥攻击与三份四人记录--程序.md)。四primary91316B全部实读，完整原件和全部历史动作保留；原程序0导入、0main、0函数调用、0LP/MILP、0随机扫描。

- [original/pair_attack.py](original/pair_attack.py)：5887B唯一正式原件。实际依赖为[22102B common_q_generator.py](../transport-tail-common-q-20261031/common_q_generator.py)和其顶层导入的[6608B policy_patterns.py](../transport-round-obstacle-20261031/policy_patterns.py)，均全文读，只复用既有同SHA原件，不重复制/重跑它们的成熟批次。
- [pair_n4k6.json](original/pair_n4k6.json)、[pair_n4k6_bg001.json](original/pair_n4k6_bg001.json)、[pair_n4k6_bgall.json](original/pair_n4k6_bgall.json)保全部7/8/8根字段、各8个best字段、189个质量坐标和777个完整有序动作。[all-fields-reading-view.json](all-fields-reading-view.json)仅对已保存JSON作无损紧凑阅读，含signed zero，不执行模型。
- [source-manifest.json](source-manifest.json)包含四主源、实际两依赖和5431B源README；[comparison-manifest.json](comparison-manifest.json)与[review-record.json](review-record.json)区分同名PAIR、plain首对桥、数值上界和后继证据。
- [audit_saved_points.py](audit_saved_points.py)是唯一实际执行的定义级脚本，原字节不改。[exact/execution.json](exact/execution.json)保执行脚本、三输入和输出SHA，Python3.12.14、断言开启、exit0，elapsed0.3419855859974632秒。
- [exact/exact-audit.json](exact/exact-audit.json)24457B保三个记录的decimal、binary、明确整数校准共九解释；[exact/complete-ledger.json.gz](exact/complete-ledger.json.gz)97902B保13986逐历史比较和558行/3348项静态收益。它不import原程序，不调用Space/BI/LP/RNG。
- [artifact-manifest.json](artifact-manifest.json)、[self-check.json](self-check.json)与[check_package.py](check_package.py)只验证源字节、静态格式、已保存账本、链接与回执，不再次运行数学核验。

基表缺prefix字段，而当前冻结代码无条件输出prefix；旧README还明确初批允许全兴趣、后期才剔除。不能称基表为当前代码原字节运行输出，也不能从名字补背景。新审计只**明确另定义空背景解释**；另两表按原有序prefix [0,0,1]及[0,1,2,3,4,5]。原elapsed/completed不是本次运行统计，原随机轨迹没有恢复。

三点的精确解释都是大块与不交小块：显式5、8、13单位客户校准沿原完整策略给根/尾安全值同为归一1/5、1/8、1/13，真正带尾PAIR=0；正文给全历史及全静态背景解析证明。字面decimal/binary质量也单独核验，不能把校准点回写成原小数。基表p按两种解释都略大于概率总质量1，裸表达的微负没有合法分布前提；显式归一p后为0，未改原JSON。

执行脚本和execution中的绝对scratch路径是实际事件身份，未倒写路径；同basename由本包原件/脚本对应，checker核其同字节。脚本有输出目录存在即拒绝的保护，不能在本包覆盖已保存证据。未来新复现须另建目录复制原输入/脚本，产生新事件；本轮没有如此重复。

同批[联合计数策略程序](../../../state/程序/固定路径计数策略与客户质量的两步安全联合搜索--程序.md)和[三份其它保存点](../../../state/计算/两步安全链的三份浮点保存点与六客户校准--计算.md)是不同输入/策略域，未由本三点借认证。带尾PAIR在本四源仍是候选；已有PB-extra反例针对plain首对，不能直接移来反驳带尾项。
