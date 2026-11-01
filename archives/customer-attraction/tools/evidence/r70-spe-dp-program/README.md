# R70浮点终局集合与完整历史有理后核证据

完整语义见[程序正文](../../../state/程序/浮点终局全集递推与完整历史有理后核程序--程序.md)。主源 `44c5afc4b6e2b6b72b90`，6396 B，SHA256 `abf6a57871a79b1642ddcd9672a077e9b4b8e55e80bb390acee247e7d74ce8a3`。

- [original/spe_dp.py](original/spe_dp.py)：全文实读、未修改原件。四公开函数，无CLI或文件副作用，仅NumPy及标准库。
- [check_interfaces.py](check_interfaces.py)：三个独立小输入的原API驱动；不处理两个保存点、不导入其它求解器、不调用LP。
- [interface-audit.json](interface-audit.json)：原返回、完整小策略、精确接受/拒绝记录。
- [interface-execution.json](interface-execution.json)、[stdout](interface-stdout.txt)、[stderr](interface-stderr.txt)：一次真实驱动事件，3次solve/3次reconstruct/4次verify，其中3次成功、1次预期拒绝，LP0。
- [source-manifest.json](source-manifest.json)：冻结源、全文比较和共享事件范围。
- [check_package.py](check_package.py)、[self-check.json](self-check.json)：最终原字节、事件、链接、回执静态自查；不重复数学运行。

两个正常例是两标签两人零客户，以及三标签两人、0/1同覆盖而2为空题；它们保重复动作与全部离轨。第三例为一人、两个不交主题大小2^53和2^53+1：原float solve错误保两终局并选0，原Fraction verify以根偏离1的slack−1拒绝，正确动作1的表被接受。它证明浮点筛选并非所有整数输入上的精确终局全集；不反驳集合值逆归纳定理。没有改原函数来制造失败。

运行方式：`python check_interfaces.py --source original/spe_dp.py --output NEW.json`。输出必须不存在。需要NumPy；程序只保存这三个已声明小域的结果，不启动随机搜索。当前真实一次事件已经保留，无需为了封包重复执行。

同目录存量random点的唯一原solve(witness=True)由[策略LP包](../r70-strategy-lp-program/README.md)连同7LP保存，完整19608动作表供数据方共用。本包不重复它。两存量客户表及同一完整σ的有理认证由[数据包](../r70-six1-best-data/README.md)保存；不冒称那次独立核调用本原verify，也不把固定锥7个精确对偶当本函数的输出。

另由root对SIX_SEARCH的新首样本执行原入口，属于不同输入；它不计入本包3个小solve，也不是重新运行冻结trial711。所有实际事件按输入/入口分别记录。新小域测试不证明一般福利、全策略最差界或全集无舍入遗漏；这些额外结论必须另有精确重算或结构证明。
