# 原件、唯一入口和版本证据

五primary26831B：root17219B长稿、relay3887B检查点、parent4933B当前审计及378B/414B两报告。source-manifest记录完整冻结commit/blob/SHA；original按原repo相对路径保raw。9份已全读当前正文只作comparison并独立SHA快照，未替9来源done。

程序无外部input/dependency/local import，dependency-manifest为空。run-original-once.py先exclusive创建新replay，以原字节在新source-root镜像路径真实Python CLI一次，--output新路径原程序open x拒覆盖。默认只stdout；无源函数仪器化或额外调用；失败会保留不自动retry，实际exit0/assert启用/stderr0。不要再运行wrapper或原程序。

新报告414B与锚版raw精确同SHA；stdout392B紧凑JSON仅语义相同。378B初版原件保全，当前源有anchor字段，未声称重跑历史初版。report-version-and-domain-notes只是结构/算术解读。complete-built-input-catalogues.json是完整806输入目录显式列表，input-domain.json定义余全部有限循环；原程序本身不读这些外层解释文件。

原run只静态替槽，无SPE/payoff/IC/half/FLOW/NET调用；93908为同槽逐索引锚次数，1311/29979为每配对bool计数。详细数学/版本/边界在正式计算资源，不因PASS升级root未付动态账。
