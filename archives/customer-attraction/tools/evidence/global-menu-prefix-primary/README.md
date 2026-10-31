# 固定末菜单与前缀付款：五主源证据

实际认领pushed c59d0557ab194d2f8e0cf6563e29b97427609a1e，actor Boss4，local_sync synced；唯一capture为boss4-r3-next10aj-claim.json。本批五ID与实际claim交集全五，观察与原回执保cleanup工作区。五源共22828B，包含1033B入口、1992B/17873B第一版代码/报告、1178B/752B第二版代码/报告；均正式确认后clean show全文取回，双冻结逐字节核SHA。

对应[自足模板障碍](../../../state/障碍/固定末菜单的非均匀前缀付款边界--障碍.md)及[两版系数资源](../../../state/计算/末菜单系数模板的发现与缩放证书--计算.md)。当前无完整SPE反例、无一般方法不可能性或六人half证明。三四人正系数已精确核验，五至十三人第二版失败只有浮点身份。

original/保五主源完整相对路径。comparison-original/另保4382B解析稿terminal_menu_nonuniform_barrier.md，两冻结核SHA，角色为comparison-only-not-primary；它已在现有审查中被引用，本批阅读用于理解程序合同及核局部笔误，不给该源额外receipt/done。source-manifest.json合五主源与一个比较源；两程序本身不读取任何文件或本地helper，只依赖标准库/numpy/scipy，故没有虚构运行输入包。

## 新原入口各一次

replay-tree/保未改原码与完整相对路径。两个输出原先均不存在。工作区prepare_and_run.py在已有execution时拒绝重跑，每版仅一次原入口：

| 入口 | 实际参数与通道 | 结果 |
|---|---|---|
| menu_prefix_lp.py | 默认max-m10，仅指定新--output；报告由原open(...,'x')写 | 1.195249080657959秒，exit0，16次LP；17873B全字节同SHA7668b9e1da59250f32914bd6ce24b3f0ee90c8ed716fc2897de8c03dba195deb |
| menu_prefix_lp_v2.py | 默认无参数，m3至13；原码只print，wrapper原样保存stdout | 7.076197624206543秒，exit0，11次LP；752B全字节同SHA4c7981200e5ff67b68a8032da454acb8353a317aa6270bc6bd17ca374551c8ff |

Python3.12.14/numpy2.3.5/scipy1.17.0，两个stderr均空，原码未变。replay-v1/与replay-v2/各保新报告、stdout/stderr、完整execution事件。V1原文件无末尾换行，stdout另有print换行；V2新报告本来就是stdout。没有为追求一致改格式或扩大人数扫描。

## 另一次独立精确检查

exact_template_check.py是本轮标准库Fraction核验，实际执行1次，未计时，不导入原码、不调用scipy或原main。exact-template-check.json保完整结果：m3/m4全部128+400=528个整数d/ell类型行非负、24种实际会员位各自的最坏值/达到位置；m3原active的有理权重(1/9,2/3,2/9)给固定G模板系数0且右侧−1/3；另保有限人数A-only校正、非SPE松弛路径及银行逐人后续更正算术。普遍三族矛盾、矩形六角点归约和非SPE性由正文证明，不从有限检查外推。

解析比较稿把A-only,d1的G错误写成ell任意时m−1；实际为m−1+ell/(4m)。取ell0即可保其全m障碍，原代码计算正确，原件完整不改。README的弱逐人OPT/(2m−1)历史OPEN也经已完整读当前银行反族更新为m≥4失败，不能把历史目标状态冒作现状。相关对象全文指纹与差异保related-material.json。

五主源receipt、数学自查、关系判断、传输校验和下一候选在同名cleanup工作区。串行复制、发布和done由Boss执行；这里记录本地成熟交付，不声称已推送本批正文。
