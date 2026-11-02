# R8e450逐人净差三源证据

三原件共7204B：minimum_payoff_bridge_search.py2437B、minimum_payoff_bridge_search.json2444B、sampled_bridge_extend.py2323B，全部实际全文读入。原文件未经修改保于original/<source-id>/；双冻结commit、原路径、ID、size、SHA256及Git blob见source-manifest.json，clean show回执见export-metadata。

正式对象是[完整搜索程序合同](../../../state/程序/逐人净覆盖差的可信续局锥搜索与四种子扩展--程序.md)和[全部20条原记录](../../../state/计算/两类五人五题策略的二十条净差浮点记录--计算.md)。后者保原float位串，不用猜测的有理数取代精确证据。

dependency-manifest.json复用strategy-cones/original中的两个helper及四规范模块，总59284B；两个helper本批全文读，规范包此前已全文读并核当前同SHA，certificate中离轨selector的最小化限制另行复读。没有原入口、helper主入口、LP、BI、随机或新数学checker执行。

两个原脚本无main守卫，import会执行顶层循环并可能覆盖输出。若未来明确运行，应在clone外恢复原research/workspaces/customer-attraction/R-8e45018cd1354e279ca636fdb82cf0f1/structural路径和root/tests/audits、root/customer_attraction依赖，另提供NumPy/SciPy。原两个脚本共用反例输出名，按源码分别记录精确目标与输入/策略身份后才有可复验发现；本批没有修改冻结源来补门槛。

reading-ledger.json保存全部20记录和其索引，及从源码实读的两builtin输入、五个结构种子/前四处理范围。missing-output-scan.json记录当前inventory及全部increments中的两缺失输出名称检索，不将缺条目推断为历史未运行。

comparison-bindings.json和relations.json保实际比较的逐人净差、价格、尾利润及已失败地板的不同量词。verification.json只作文件与交付核对，不冒数学证明。正文与依赖必须显式checkpoint确认pushed、远端核真后才分别提交三源done。
