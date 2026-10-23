# 本轮精确命题账本

## Q-CAG-HALF

完整身份沿用 [共享模型](../../../current/customer_attraction/model.md) 与 [目标](../../../questions/customer_attraction_half_coverage.md)：任意有限单位客户N、有限非空共同目录S⊆2^N、m≥1、每个完整有序历史纯SPE均有2W≥OPT_m。全部离轨、历史平局、重复、空主题和零客户保留。**状态OPEN**；本轮没有证明或主目标反例。

## B10-BACKGROUND-HISTOGRAM-CREDIT-NO-v1

- **Objects / Domain / Quantifiers：** 任意CAG-MODEL实例与全部完整纯SPE节点；b过去负载，c剩余r人真实负载，P其利润，F_r(b)为同背景r主题元组最大总剩余利润。
- **Definitions / Assumptions：** H只含b_x≥1客户的(b_x,c_x)多重集合。实例无关任意实函数G_r(H)，G_r(空)=0，C_h=G_r(H)。不要求可加、单调、连续或符号。
- **Exact Conclusion：** 不存在这样的G同时普遍满足F_r≤2P+C和Δ+C_child−C_parent≤2u。
- **Dependencies：** Cartesian产品完整SPE与F可加；all-big已知族；本轮AB完整族及F_r=2r−1；旧prefix_balance交叠族及精确Ftail。
- **Evidence：** 两产品同r63、H=4032*(1,63)+4032*(1,0)，合同要求G≥−2898及G≤−3170。root解析重构，另外两研究员未读root稿独立攻击通过；root与general_exchange独立Fraction回归。
- **Counterevidence / Objections：** 未发现成立异议。b=0信息在两实例不同；看见全客户直方图、尾福利或目录的状态未被排除。
- **Status：** 自足解析证明、独立内部重构；外审/新颖性未认证。不反驳half，不修改其量词。
- **Related Files：** [正文](dynamic_credit/background_histogram_credit_obstruction.md)、[root审计](dynamic_credit/product_credit_independent_audit.json)、[独审](general_exchange/independent_audit/histogram_product_review.md)。

## B10-IID-SUPPORT-AVERAGE-NO-v1

- **Objects / Domain：** 两真实提供者、任意偶k≥8外围主题和一个hub，单位客户；静态比较为同目录三人iid对称Nash。
- **Construction / Definitions：** M=3*C(k,k/2)核心客户，每个k/2外围子集有3客户并喜欢hub；外围各再M/3私有客户。q均匀外围，hub概率0，g=1−1/k+1/(3k²)。
- **Exact Conclusion：** q为静态3人对称iid Nash，λ3=M(7/24+g/3)。两人真实强制根按q抽外围后末位唯一hub，平均D=7M/12<λ3；真实SPE根选支持外hub，首位3M/4>λ3。gap=M(3k²−24k+8)/(72k²)>0。
- **Dependencies / Evidence：** 会员计数与全部两人BR；父、child及root分别推导，root单位客户精确核验。
- **Scope / Objections：** 只反驳“用静态iid均衡q平均真实根偏离即可支付λ”的桥。extra-slot首位及half均未被否定。没有外审或新颖性认证。
- **Related Files：** [发现正文](iid_extra_slot/child/hub_family.md)、[root独审](parent/iid_support_hub_independent_audit.json)。
