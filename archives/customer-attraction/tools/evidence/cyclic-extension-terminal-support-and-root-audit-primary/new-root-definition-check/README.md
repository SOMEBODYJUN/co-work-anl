# 精确捕获与可移植复现

verify-root-and-full-history.py保唯一真实成功执行的原字节、SHA及其当时绝对输入路径，execution.json和stdout.json不改。replay-with-local-input.py仅把这一条I/O路径换成明确输入（默认同包related-original原5707字节），断言原代码及输入SHA，不改数学代码。未来可从任意位置运行该wrapper。

本次wrapper仅用--prepare-only核原码/输入SHA与编译，mathematical_execution=false；没有重复258比较或冒作第二次数学成功。实际数学入口仍一次。
