# Boss4 incidence/directed 十源交付

本批10个稳定源版本已完整实读并逐源整合，回执为[incidence-directed-receipts.json](incidence-directed-receipts.json)。处置均为integrated；源正文、审查、代码与完整输入/结果保留原字节，实际输出独立保存。本批未执行Git写入、sync、claim、done、checkpoint或远端操作，交Boss按当前local-only边界保全；回执不是远端勾选完成声明。

## 自足正文

| 路径（均相对仓库根） | 内容 |
| --- | --- |
| archives/weighted-congestion/state/定理/潜在使用森林的精确均衡--定理.md | 任意实权、任意有限耦合策略、任意有限非负非减费用；贪心阈值/背景非增、两侧报价、冻结偏离、森林拼接完整证明 |
| archives/weighted-congestion/state/归约/单核心挂树的私人成本提升--归约.md | 一附属分量至多一核心根、删除玩家不使用E0；ψ单射、同一固定lift对任意实α≥1提升、不升次数 |
| archives/weighted-congestion/state/反例/单环潜在使用图的二次均衡缺失--反例.md | 原始四资源输入、四态八偏离、圈秩1、最佳α=72/71与端点，仅固定二次例 |
| archives/weighted-congestion/state/定理/统一强迫分叉反馈的割均衡--定理.md | 精确资源拓扑/UF与α≥T_d；标量S/M、B1—B3、含自环CUT、逐人真实偏离及共享side后续边界 |
| archives/weighted-congestion/state/审查/森林报价与分叉割的内部审查--审查.md | 两审查的历史独立性、冻结hash、10项森林攻击和分叉预算/自环攻击、范围与证据层次 |
| archives/weighted-congestion/state/计算/森林报价与分叉割的精确有限核验--计算.md | 三脚本实际生成规则/参数/断言、全部计数、有限证据角色、实际复跑与零差异、独立脚本弱拒绝断言说明 |

## 原件与复现

目录：`archives/weighted-congestion/tools/evidence/incidence-directed/`，可整体本地保存。

- `source-manifest.json`保留10源ID、commit/path、blob、字节大小、SHA256；`original/`保留全部10原件。
- `replay/incidence-author.json`、`incidence-independent.json`、`directed-fanout.json`是本轮真实运行结果；三程序全部退出0，Python3.12.14，三个JSON均与冻结输出逐字节一致。
- `replay/comparison.json`保存原/新hash和空差异；`replay/run-record.json`记实际命令与三个前缀冻结hash核对。
- 新增`replay.py`先核10原件hash，再调用原程序入全新输出目录；它亦经实际运行，`replay/wrapper-check.json`记录三次退出0/byte_identical/json_equal。包装不是历史独立实现。

完整源程序没有修改，原JSON未覆盖；新输出hash分别cadb43ec13d6faea35de1dff85d210f56704a9b7217ebaf72483a271b45ba2e2、084fb519c85a7934e091bfac9c9364bab94b80ae3ca438265cb026fb2a0a5f8f、0cd5da3ffd0b160f4f0b2c7478147b1073efdca9de720244b89728f3a4cc9f43。

## 实际比较与关系判断

完整读MODEL、旧questions入口、后续linear_degree_allstate_lower_bound.md全篇；实读shared_side_truncated_potential.md §1—7/§10和同权截断势/多源平方根两份审查；读当前必选背景消除空交反链核心。旧全类Cd/ln d OPEN已纠正为被后续全状态线性族严格否定。健康改善环、全部前沿覆盖和非法态时钟修复分开，不用改善环代替全状态结论。

本轮当前仓库与缓存检索仅作为定位；Boss另实际执行四稳定ID全冻结*.md内容搜索，依次18/18/17/12命中，本清洗者检查了返回定位：除已读主文/对应审查外均为CATALOG、current claims、frontier CLAIMS、FILES、PRO_BRIEF入口，未出现新增承重纠错。结果与查询manifest保存在证据包related-search/，不把入口当独立证明。共享side扩大拓扑但改hub权/倍率或引入局部权比、AS+B等条件，不替代本异权私有side精确T_d定理；森林报价支撑单根归约、单环反例反驳普遍单环扩域，这些关系已在正文解释和链接。阶段三尚未正式写超边，未复制旧图。

## 未解决与交接

本10源无尚未读完或未理解的语义单元。外部同行评审和全球新颖性均未认证；更宽的多根附属树、核心资源挂接、UF失败、动作异费或多人side须另建精确合同。原分叉初始临时稿e3d74b...未作为源提供，本轮只记录审查声称的前后四节相同，不伪造亲做diff；当前规范freeze前缀已亲自hash核中。

收尾检查：6正文与新证据README的全部本地Markdown链接存在；10回执均具有三个实读/比较/独有内容标志和全部存在的targets。全部写入只在本任务新文件内，未改共享README或其他任务正文。

只读交付QA另核主数学、量词、四态表、CUT自环与lift冻结接口；据其对照原代码，已修正文中作者随机多项式项数为2—5、作者core项数为1—5，并把样本T₂<6/5改为足够的T₂≤6/5。未修改任何原件或重做已通过的原审计。
