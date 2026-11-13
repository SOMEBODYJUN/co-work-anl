# 六人实际末主题分支与四菜单补价证据

正式说明：[实际末主题分支分离器与四菜单补价原点核验](../../../state/计算/实际末主题分支分离器与四菜单补价原点核验--计算.md)。

本包六个primary源为 B_family_oracle.py、branch_family_lp.py、maxroot_identity_master.py、B_menu_prices_master.py、maxroot_identity_exact.json 和 all_menu_prices_exact.json。original/research_2 保存六原件；source-manifest.json 保完整双冻结提交、原路径、源ID、大小和SHA。replay/research_2 另有原字节执行副本与三个related依赖模块，related不在本批done范围。两个大点的全部4849列和所有质量保留，没有只截header。

本轮真实事件：

- branch_family 原默认入口一次：23425不等式、1087变量，浮点beta=2.3266306390622455，7.1258秒、exit0。没有恢复有理系数，输出不是严格界或SPE。
- B_menu_prices_master --all-families --verify 原入口一次：5692行、4849列、精确W匹配、最小slack0，62.0787秒、exit0，stderr空。全部代码/依赖/输入位于clone外独立运行树；没有重新求LP。
- 保存的两份结构/价格审计报告包含两点的描述符、194 joint上界、2612 overlap上界、64条件边缘、最大M身份、O/W及四菜单28新价。当前保存的 audit_point_structure_and_prices.py 只读取新5692点，核描述符、质量、边缘、最大M身份、O/W和28新价，未实现报告中的joint/overlap上界循环；不能把报告全部字段归为当前脚本的可复现输出。5692行完整通过仍仅由前一项同实现原入口承担，独立检查不是第二套全矩阵。
- point-comparison.json 保前后全部描述符同一、214隐藏质量变化、正列252→261、K及16hist/W不变。旧5664点新28价恰一条source2实际末价负，新5692点该价归零且28价全非负。旧5664全矩阵没有为本批重复长跑，其作者报告与本轮新增精确比较分开。

replay 中两个 *-execution.json 及对应 stdout/stderr 是保存的实际事件记录。structure-and-prices-audit.json、maxroot-structure-and-prices-audit.json 是保存的独立检查报告，当前脚本的复现范围见下文；其 header_only_until_separate_original_matrix_check 字段保各输入原header，其中新5692另有原入口通过记录，旧5664原header不代表全矩阵已被独立复核。

重建时先在仓库根材料化到一个新的绝对路径：

    python3 archives/customer-attraction/tools/evidence/b-family-menu-prices-boss3/materialize_runtime.py /absolute/new-runtime

这个工具先复用既有 combined-branch-master-program 封包的47份冻结依赖，逐项SHA核后覆盖本包9份文件；根work.py只是无执行内容的找根标记。当前source-manifest实际有8条，使用仓库相对local_original/local_replay字段，其中部分记录只保basename；第9份是正文已绑定SHA的maxroot_identity_exact.json。2026-11-11的Boss1研究接续发现旧工具仍要求stored_path和每条path，导致KeyError；现工具兼容当前字段，并单独核验补齐该原点。原始证据字节未改。材料化不运行任何研究入口或Git命令。随后需要时可以显式运行：

    python3 -B /absolute/new-runtime/research/workspaces/customer-attraction/R-5662d5cb0e5845a980ed10a3b3224cb1/research_2/B_menu_prices_master.py --all-families --verify
    python3 -B archives/customer-attraction/tools/evidence/b-family-menu-prices-boss3/audit_point_structure_and_prices.py /absolute/new-runtime

后一条只重写本包replay/structure-and-prices-audit.json，不写original。当前保存的audit_point_structure_and_prices.py仅接受一个runtime参数并固定读取all_menu_prices_exact.json；它不能直接重建maxroot-structure-and-prices-audit.json及point-comparison.json，后两份仍是保存的历史报告。当前脚本未实现历史报告中的194个joint及2612个overlap上界检查。原全图验证需要NumPy/SciPy，独立结构/价格审计只用标准库。assert必须开启。run_entry_once.py 是两个原事件的组织脚本，拒绝覆盖已存在事件记录；它不是额外一次执行声明。

B_family_oracle 的有效数学source限1至4，原码不显式拦截5等范围外输入。其有理权、448型max表和精确负点值可认证一个成功返回切；None只表示数值容差下未分离。本包没有为它虚构一次搜索事件，也没有运行maxroot独立优化入口或依赖其尚未加载的root支持线文件。

所有点仍是固定16hist必要图，不是完整SPE、游戏反例、严格最优福利常数或一般/六人half证明。
