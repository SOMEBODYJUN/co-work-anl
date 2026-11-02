# 在轨保底、实际尾PAIR与hybrid原审计恢复

七主源共21612B，全部clean show、全文读、双冻结字节SHA核同；正文为[四个有限锥精确边界](../../../state/计算/在轨保底与末两人聚合行的四份精确边界--计算.md)和[hybrid障碍的原实现附记](../../../state/障碍/在轨精确行与全部固定深度尾局的联合截断--障碍.md)。source-manifest给稳定源ID、原path、blob、SHA与完整原件；没有把字段检查当数学判断。

original中两py与五json原字节不改。原hybrid在轨m10/200、尾m4/4608与m5/110000的完整合同已恢复；本批0原audit、0新hybrid策略运行。成熟m10/m4复用，m5原110000未被本批重新执行；计数公式核对另见hybrid-report-and-mature-binding.json。

四个旧浮点点另用Fraction公式与精确RREF恢复原始、对偶。第一次包装成功m5/m6/m7、在m8欠定dual有理化后发现严格负余项；首次源码与stdout/stderr保留。随后一次方程秩只读诊断，添加该精确列约束，第二包装仅m8成功；已成功前三份未重复运行。共2个新包装入口、1次m8方程秩诊断、0原LP、0规范游戏求解器。执行记录分列，当前final脚本默认可复算4份，也接受--only 8。

new-terminal-transport-exact-certificates.json保存合并完整证书；各m文件是当次立即保全的完整分项，含52质量、49正乘子、342行slack、7936全类型余项。合并仅拷贝已成功结果，不增加数学入口。原浮点与新有理点分开，所有新证书仅认证所列必要行锥，且给相应真实SPE弱上界；不提供下点的游戏或完整SPE，不反五人或六人half。

复现可在新输出目录运行：python -I -B check_terminal_transport_reports.py original replay.json 。不要覆盖original文件。方程恢复用旧支持与正行名猜基，最终全矩阵接受条件无浮点容差。完整公式、端点证明、原程序输入/输出合同、首个失败余项及修正原因均在正文；relations保第三阶段证据，未改正式图。
