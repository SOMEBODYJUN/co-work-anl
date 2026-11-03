# 个人区 README 恢复入口抽查 A（只读）

2026-10-25。范围：`research/workspaces/customer-attraction/` 首级 actor 目录按字典序前57个（从 R-059140... 到 R-80ed37...）。先读仓库 AGENTS.md；未执行 Git、work.py、外部消息、凭据读取或共享修改。本报告是导航与状态审计，不是全部数学证明复审。

## 覆盖与方法

Python 按实际文件统计：57个首级actor，296份递归 README.md，共768,588字节。对57份根README的成果/候选/失败状态做人工抽读，并对239份子目录README提取、逐项浏览标题及“新增/已证/反例/未证/OPEN/勘误/缺口”等状态语句；关键发现进一步打开自足正文核对定义和量词。不宣称296份README全文逐式审核，更不宣称对应数学已审。

四份恢复文件为 RESULTS_LEDGER、WORKSPACE_RESULTS、SYNTHESIS、general_half_proof。此前57个actor中，WORKSPACE_RESULTS文本出现39个，general_half_proof出现2个；另外两份按机制组织，未直接出现这57个actor的字符串。18个actor字符串在四文件均未检出。此项仅证明恢复路由覆盖不足，不证明数学原创性，也不证明已按机制出现的内容数学上漏账。

## 最重要的三项状态修复

1. **GLOBAL 背景归纳已假但旧README仍OPEN。**
   - 旧状态：`R-2fc8878b4bdd4328bbc1bcf1df8ca831/background_induction/README.md` 第8–9行及第32行；其 `coverage_opportunity_step_obstruction.md` 第9–20行定义 P=未来玩家总利润、Δ=背景负载为0客户的实际新增覆盖、freshOPT=至多r目录主题的fresh最优覆盖。
   - 现有否定：`R-5c4f6385eec046eb9a20052facacba11/background/global_actual_prefix_counterexample.md` 第7–20行定义完全相同，52单位客户、六主题四人完整SPE的实际前缀(A,B)给 P=17、Δ=0、freshOPT_2=18。第62–75行说明全部259有序节点、1554含自身比较的全树证据；`parent/actual_prefix_independent_review.md`为独立来源。
   - 建议：历史源保留，默认失败地图从“GLOBAL已被否定”进入上述实际前缀反例；旧README顶部加定向历史纠错链接。此反例不否定空根half，也不否定2P≥F_r(b)。

2. **静态最优主题存在匹配已假，但新桌面仍称未证。**
   - 旧/未修状态：`R-79a883d99127437ebe4f0423a181f01b/independent_audit/README.md` 第22–46行。候选精确为：对每个完整SPE终局z，存在OPT_m最优元组和排列使 Σ_i F_i(Tπ(i))≤W，F_i(T)=u_i(T,z_-i)。
   - 现有否定：`R-105f776c3e6d4a22bb7c380c5df8edc7/dynamic_exchange/static_optimal_assignment_counterexample.md` 第14–46行给同一定义的反例：m=3，六主题、1953单位客户，唯一最优支持{1,2,5}；W=1735、OPT=1740，全部最优排列的最小静态和为1736。正文第8–12行连到盲原始证书审查和父方单位客户独立实现。
   - 建议：把该静态候选标FALSE并定向链接唯一反例源。**不能**改写为动态SM-opt-exists失败；动态真实后继匹配不是同一候选。

3. **弱 iid 的旧未反驳表述滞后于已入库反族。**
   - 旧状态：`R-7e9f44beea424d469713364afe7dd180/README.md` 第17行，以及 `aggregate_security/strong_iid_failure.md` 第3、87行。
   - 已核同一定义：该正文第5行明确Z为谐势最优iid的总期望覆盖，第87行明确弱桥是(5/6)Z_3≤W，非真正v或额外槽。它说“本例不反驳弱桥”本身正确，但第3行/根README无范围的“弱桥未被反驳”作为当前状态已过时。
   - 现行否定：`research/current/customer_attraction/iid_security_and_flow_barriers.md` §1.2第116–122行，任意m≥41完整SPE满足 W<(1−1/(2m))Z_m，且W≥m v_m、half仍成立。建议入口纠错引用此共享唯一源，不回写旧证书。

另：`R-18e993ca519949aba29e030d3d7b15b3/README.md` 第21行仍有“聚合2W≥(m+1)u_m仍OPEN”，但第13行已明确否定且第15行明示后文历史保留。这是大段历史夹在恢复入口造成的认知负担，不应报为现行数学账本自相矛盾。根读取层可指向第13行的修正及R-7e9f44的23客户完整证书。

## 真正需要补入恢复路由的个人资产（不自动提升canonical）

以下正文均存在，且所列文件名在上述四份恢复文件中未检出。已打开其精确合同或正文起始定义核对；数学真值、独审范围及原创性仍以原文及实际审查为准。建议放入一个短的“截止后增量/待清洗”机制表，让下一轮按义务查，不能一律并入默认长读链。

| 机制与来源 | 作者当前声称的精确增量 | 读取动作与限制 |
|---|---|---|
| `R-105f776c3e6d4a22bb7c380c5df8edc7/parent/deletion_regret_envelope.md` | 任意非负整数背景b,d与任意尾人数，保留同一全历史策略，ΣR_j≤ΣK_j−E_d(q)；作者称有盲独立重构 | 一般删除误差组件，优先接到现有虚拟回放机制；不证明删后SPE或half |
| 同actor `parent/average_suffix_deletion.md` | 任意完整SPE，对全部实际删位的后缀误差共同支付，(ASD)/(VR) | 与R-4ffa...虚拟回放保留来源依赖；后缀游戏不是同一个m−1人根游戏，不能免费归纳 |
| `R-65d0f88edf3849b39ca5eb79760e970b/credible_attack/prefix_credible_exit_compiler.md` | 任意前j位的可信退出编译，旧路径+可信尾为输入，half缺口成本(2j+1)Δ；j=1复用旧常数三 | 前缀编译的一般工具，有内部独立重构来源；不解决稳健不等式 |
| `R-3bc48d936f044f12b0fa743482ff5eb0/credible/heterogeneous_prefix_repair.md` | 上一前缀编译的异质层积分加强：精确half缺口代价2Σδ_i+maxδ_i | 应与上一行按同机制合并路由，分别保留统一/异质合同和实际审查；没有越过门槛的目标反例 |
| `R-5a15745a45ba44adb7d26c0557faacb7/parent/terminal_amount_cap.md` | AMOUNT预算下，多末位孩子共享同一B_m钱包的两倍列容量；代数不要求SPE；另有趋二完整SPE锐族 | 只列为末层容量工具；DEEP-CAP2与合法初始化仍未证，不能标一般half组件已接通 |
| `R-059140e622784d85a4e3a4dd6554f506/menu_covariance/last_successor_peeling.md` | 同一目录分布p的真实末位BR剥离关系，把余项缩为中间负载漂移 | 原文首页称“未独立审查”，根README另链接父方独审；应路由到实际审查，核清版本再定等级。余项无符号，非已闭付款 |
| `R-79a883d99127437ebe4f0423a181f01b/construct/homogeneous_screen.md` | 同主题最佳回复的通用反例筛选不等式OPT_m≤[1+(m−1)/r]K | 作为反例构造筛选按需查；不能与同actor已失败的静态最优匹配候选混读 |

R-174070...的route5a纠错已保存，R-105f...及R-65d...也保留独立纠错来源：旧“遗漏半额付款”只给三分之一保障/OPT≤3W，而非half；L1–L4保留。应由一个失败/更正条目统一路由，不能按多个actor计为多项新一般进展。

## 最小实际整理建议

- 默认恢复只读目标/模型/短义务链，个人区索引不默认长读。给个人区统一一条“持续备份、可能历史、非当前真值”的读取合同；已有历史警示而仍夹着旧OPEN的README不必全部重写。
- 全量个人区根README列表可自动生成“来源恢复表”；逐机制的准确增量应保持短的人工表。二者不同，前者能保证114个actor不丢，后者不能用生成器伪造数学状态。
- 为上述三项确切状态滞后在共享失败地图/当前义务处补唯一现行源；个人README只做定向勘误链接，证书及旧正文原字节不改。
- 删除误差、前缀保险与异质保险应作为同机制链路，保留实际依赖与可恢复来源。不要把整个个人区复制成第二份证明源，也不要在总账、综述、工作稿各自复制长证明。
- 本抽查未发现任何可据README宣称一般half已解决的成果；所有新资产应按原声明等级列“待清洗/按需查”，不制造新研究或升级数学状态。

## 统计附录

L=RESULTS_LEDGER，W=WORKSPACE_RESULTS，S=SYNTHESIS，G=general_half_proof。符号仅表示actor字符串出现，不表示覆盖其所有成果或完成审查。

| actor | 递归README数 | README字节 | 四恢复文本出现 |
|---|---:|---:|---|
| R-059140e622784d85a4e3a4dd6554f506 | 3 | 4992 | — |
| R-077c0cacfba24288be91dee1acf6d484 | 7 | 27676 | W |
| R-0f99797b33de46bfb498541a0bc5fae9 | 7 | 20634 | W |
| R-102f9599ca8646f0a41e49f9b507732d | 1 | 1672 | W |
| R-10559a151192423eb02b095dfc1c1b03 | 1 | 1603 | W |
| R-105f776c3e6d4a22bb7c380c5df8edc7 | 13 | 30590 | — |
| R-12bf6a96d24c48eca828620d6642e203 | 7 | 17731 | W |
| R-171cd7d518434f36a48cd50df29c9303 | 12 | 20285 | W |
| R-1740705e79f14baba6326b951a52152f | 2 | 6032 | — |
| R-18e993ca519949aba29e030d3d7b15b3 | 12 | 46412 | W |
| R-21674f0a89d74b80ae16410012678daf | 2 | 6054 | W |
| R-24bfbfd5ec7845b79374a1938c335df7 | 4 | 6763 | WG |
| R-24e40cab6b8d43ecbbf1c15c4d0edcd5 | 2 | 5065 | — |
| R-27557809587746c59216a46867c9eb07 | 10 | 29190 | W |
| R-28e8b1905f3b4a1f934d87d8071ccd67 | 3 | 5017 | W |
| R-29b83efed6b045678e3b7ee11dffb7b3 | 7 | 24885 | — |
| R-2d91ff13b4b44effbe7e78a60470bcc7 | 7 | 10374 | — |
| R-2e5a6ea95aff4f4c89f75237a74ba472 | 5 | 8721 | W |
| R-2f6cae284faf43fea7a09c0a4fe7c679 | 9 | 13539 | W |
| R-2fc8878b4bdd4328bbc1bcf1df8ca831 | 8 | 23981 | W |
| R-31bbb6cfd6594bc8bb076db7b2950993 | 3 | 5409 | W |
| R-324fbf8f72b041578583b51189f13d1a | 1 | 4600 | W |
| R-373daba10913464c93771a808d88fce3 | 3 | 6133 | W |
| R-3b6b03db882e4de48cfa5b406f57ef8f | 2 | 2470 | W |
| R-3b9429e7635a48208e072c8f1597126a | 7 | 28941 | — |
| R-3bc48d936f044f12b0fa743482ff5eb0 | 7 | 9776 | — |
| R-3d2531ded15f453daef73b30eef82940 | 3 | 10356 | — |
| R-3d6f7a072d5e489eb5a0bdc4d32bb769 | 4 | 7892 | W |
| R-3f637fd71daa4432a913847f7ffab862 | 1 | 2972 | W |
| R-40c4c69781f84bed97ee4821df6cfe34 | 5 | 7065 | W |
| R-4243b113e6fc4c25a197dec299f08049 | 7 | 16400 | WG |
| R-428f842e483745ffbe55235bfd7d250a | 1 | 2969 | — |
| R-44b24f3962bd4f68a4b6913610c0d417 | 6 | 22169 | W |
| R-486bb9adb8cd4d9a940dbf3b1ab0b1de | 4 | 6715 | W |
| R-4ffa8b85fa8847e09e45dcafc8e1326f | 7 | 17022 | — |
| R-51ca8c2b36184c41818099bc490374ca | 4 | 11129 | W |
| R-5a15745a45ba44adb7d26c0557faacb7 | 7 | 11763 | — |
| R-5bb00b5c3cf740f099eae62130632b56 | 1 | 1744 | W |
| R-5c4f6385eec046eb9a20052facacba11 | 5 | 8688 | W |
| R-5d61c5324e744dc0a66133207fcbd010 | 5 | 18130 | W |
| R-5dbadd913a00492e994a6cfca3ec53fc | 4 | 6904 | W |
| R-5e9dedd2606746ff8afbbb73bf816e7a | 2 | 3695 | W |
| R-64201cd12083425899e2d643ec9bc087 | 11 | 49051 | W |
| R-65d0f88edf3849b39ca5eb79760e970b | 13 | 32930 | — |
| R-6bb0323d87294932af2aa23b47b9d4ad | 7 | 17023 | — |
| R-6cf1f30515fe44eeba28d5390d6940e7 | 3 | 9885 | W |
| R-6cfe7c79118a41f6bd5659aa5d780852 | 7 | 10866 | W |
| R-6d2394b19d17411183724da7c822018d | 1 | 2115 | — |
| R-6e3a5707f1f94c1d86bcbc61b4db4345 | 5 | 15238 | W |
| R-731efdb50dd844178e597d804bdd4596 | 7 | 10740 | W |
| R-75bfd8f0f91740408bf08f0c9f5e2aa1 | 6 | 21918 | W |
| R-79a883d99127437ebe4f0423a181f01b | 7 | 27871 | — |
| R-79ba259d49c84076a1e442869624b4d9 | 2 | 3998 | — |
| R-7c3db62487a34730a704a4f2eb401556 | 7 | 16394 | W |
| R-7e9f44beea424d469713364afe7dd180 | 7 | 21981 | W |
| R-7eb35cf5aa0f402c892d23bc658a0639 | 1 | 3461 | W |
| R-80ed37d4641f4bd28dd05019f2b4bcd2 | 1 | 959 | — |

读取时四恢复文件SHA-256（避免把以后导航改动冒充本抽查基线）：

- `research/customer_attraction/RESULTS_LEDGER.md`：`c8c9ddecbfbb829893ad40965796b22c5751820dbbd5195a526dba71f15c0415`
- `research/customer_attraction/WORKSPACE_RESULTS.md`：`a1ccaef71c38f852031ac77f0d9adab88e9b3eabc51ed3cf238ee3149a12570a`
- `research/customer_attraction/SYNTHESIS.md`：`e3504ab4fcac2dbad04f7e816b85671365970c7247de7cc46fae3a7c62c25a3b`
- `research/current/customer_attraction/general_half_proof.md`：`f2009f88f5b8bb1b63e646e571a2430c4bd0ebc41a93fc97f04a8fc3885d4b99`
