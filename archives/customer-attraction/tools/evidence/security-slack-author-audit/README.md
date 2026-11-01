# 静态安全亏量的作者精确审计

[正式程序对象](../../../state/程序/静态安全亏量的作者精确审计程序与有限等号族--程序.md)完整说明6289B源、2274B十二例原表、匹配原始/对偶、精确亏量、sharp分支与平方舍入核。原件唯一共享给同批定理和后继审查；后继4501B程序的另一运行不计作本作者事件。

唯一新原main直接正常assert执行一次，无profile/helper替换，约0.209653秒、exit0、stderr空；stdout及新文件均2274B、逐字同原SHA3c5e5507bcefdb1652bb66a5851e9505e7b88665ae98affebe38c9809333e670，原码前后SHA同。没有第二次同表独立核、LP、SPE或DP。replay保真实argv/环境/时间与原始输出，不补造原作者历史命令。

run_original_once.py参数依次是original/audit_security_slack.py、original/security_slack_audit.json及一个尚不存在的输出目录。包装器拒绝旧目录，复制源码后以python -I -B运行并传--output；源本身用open('x')拒绝覆盖，但在打开目标前已跑完整main。源码导入有main保护，不执行审计。

有限域为十二固定例：1308个静态无序背景，其中1299项sharp身份；另700个两点负载切线恒等式。一般唯一最优负载/舍入定理、任意完整SPE与实际前缀条件均须保持各自证明，不能由有限passed继承。manifest和self-check只核字节、结构、AST与路径，不是新一轮数学计算。
