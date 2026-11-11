# 当前标签元组源澄清的应用与复核

本文件说明当前状态；同包 `source-clarification.md`、`source-clarification.json`、`source-reference-inventory.json` 原字节保留为源更正前的历史提案和170项引用快照。它们的“尚待Root应用”“v2”和旧SHA是原快照内容，不是当前待办，也没有被改写成仿佛本轮又做了一次全仓引用扫描。精确历史SHA及本轮定向核对范围见 `current-source-refresh.json`。

当前 signed 为 v3，输入pin `133e3bed60171a4bfcd5a49eec4330324a99998b2a92c60dc0b6dce1bc877309`。当前正文SHA为 `e131b381683729532c961d175a879ae0ed73d4e1d392681d14fc5f323c2dad74`，标签元组永久退出审查SHA为 `2a1c8458efb4e48917c6a7af77df37076aee259dd7f5f2f7ee5eb7a07e02e66f`。本worker逐条核对原提案四项替换：每项旧文0处、新文恰1处，正文实际SHA等于当时预测的补丁后SHA。当前任务SHA为 `9da5abf93179446a04a9a1f237bba8a561fe388132e3ffcf5bd1fd45a6216557`，e7仍为v1且pin不变。

本轮全文实读当前task及两个核心完整登记、全部9个不同reading文件（包括signed整页及新增审查），另核三个现有源owner记录和对应正文/审查引用：signed v3、M-04595ddc5e2849e08c5fe21138dc8208 v2、M-28e6e7f3210943bc961637e22c5322a8 v2。当前共同material与这些引用均指向新正文。后二对象仅核当前完整登记及变动的引用，本轮没有重新审其task范围外底层原稿。旧170项清单和旧队列全依赖扫描保留历史身份，不据此声称所有历史引用已机械刷新。

源补丁与完整证明相容：行动为原标签Cartesian元组，历史直接保元组身份；唯一首次异常后全部坐标含own-action永久进入相应完整子SPE，后续异常不reset。已退出节点逐坐标IC相加，正常早期节点用ΣU≤Σu，末位用各组件BR。OPT既有投影上界，也有同m槽配对下界；共同Q同时清原客户质量与所有donor层高。其余LP线性、辅助最小、C单调、固定表认证逆向和W0/m2/空层边界不受更正影响。

当前完整证明见 `review.md`，稳定边ID仍为 `cag-e15ef294-signed-u-table-proves-complete-fixed-exit-lp-contract`，数学判断仍是accepted、unconditional、whole_result。它支持e7整个当前注册statement；不声称已找到负点，不使用HALF5、覆盖商或产品exact-M可加作额外前提。没有运行LP、BI、随机或历史科学程序。

本worker仅在独立staging写交付。Root复制后串行native bind/check；边字节一经绑定改动，须重新计算receipt中该边asset SHA，再checkpoint与done。源/registry勘误本身已应用，不再列作交付前置。
