# 固定二维回复边缘的共同阈值诊断

主源15e62005d22b07b4ef67的[2017B原件](original/zz_direct.py)保持字节不变；[正式程序正文](../../../state/程序/固定二维回复边缘的共同阈值诊断程序--程序.md)给出固定域、同步最大证明、六负行和接续边界。

- [dependency-manifest.json](dependency-manifest.json)：11份被导入的下层Python和816498B实际输入，指向已经归档的共享原件并核冻结清单身份。
- [replay_once.py](replay_once.py)：复制上述原路径依赖及主源码到全新目录，放惰性work.py定位标记，直接执行原脚本一次，不修改输入/函数、不使用runpy或profile。
- [rerun/execution.json](rerun/execution.json)：本次唯一原入口exit0、1.129秒、前后输入不变；[stdout](rerun/stdout.txt)与[生成的status](rerun/zz_direct_status.json)逐字节同，[stderr](rerun/stderr.txt)为空。此status是新重放产物，不冒充未定位的历史原status。
- [audit_intervals.py](audit_intervals.py)及[interval-audit.json](interval-audit.json)：另按共同区间的字面均分收益独立核60行，保16hist、194组全四态、34区间原子及逐hist行分解。148104原子—边对项、1531交叠同时达到上界；6负/33正/21零；旧1306个RR坐标中164个被共同阈值抬升。
- [review-record.json](review-record.json)：全文来源、依赖导入范围、原运行和独立核的准确身份。
- [self-check.json](self-check.json)：最终文件/JSON/AST/链接/回执与原字节检查。

本包0次LP、0次旧3889验证器。旧点“3889行可行”仍为其既有证据身份；本程序固定hist/R/RZ并另选R联合，未逐坐标保全部旧点。即使会员区间能清分母变成单位客户，它也没有完整SPE动作表。

复现原脚本需允许在隔离目录写输出，不能把import当只读操作。可在结果仓根运行下面的包装器，目标必须是不存在的新目录：

    python archives/customer-attraction/tools/evidence/zz-direct-fixed-marginal-program/replay_once.py --repo . --source archives/customer-attraction/tools/evidence/zz-direct-fixed-marginal-program/original/zz_direct.py --manifest archives/customer-attraction/tools/evidence/zz-direct-fixed-marginal-program/dependency-manifest.json --output /tmp/zz-direct-new-replay

本包已经保存一次实际执行，无需为清洗再次运行。若只核区间公式，可使用正式正文给出的独立核命令；不得将固定完成域失败改写为任意R联合、旧点全域或一般六人SPE不可能。
