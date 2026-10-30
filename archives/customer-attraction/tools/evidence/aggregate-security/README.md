# 静态安全值、聚合末位保底及尾部正规化：精确证据

`PROVENANCE.json` 将九份实际读取的冻结来源逐项绑定到原路径、完整来源commit、库存SHA256及当前保存位置。`original/`内全部字节通过`work.py clean show ID --out PATH`导出，哈希与inventory逐项相同。三份旧JSON均保留原字节，没有用新运行覆盖历史记录。每个完整来源版本的数学去向见正文及逐源done记录。

本轮实际运行四个原字节Python程序，均退出0。它们使用标准库整数和Fraction；不导入规范SPE求解器或浮点优化器。运行结果在`replay/`：

| 输出 | 实际检查 | 范围限制 |
| --- | --- | --- |
| aggregate.json | 合法36客户输入/43节点策略，另n=3,4,5的两组辅助势全部distinct历史及拆分算术 | 后三项仅signed代数和fresh策略；不代表导出了三个合法正客户输入 |
| independent.json | 独立展开36个单位客户，258项节点比较、全部216终局和36末位前缀，匹配原证书 | 固定六主题三人实例，不是一般证书验证器 |
| oblivious.json | n=1,…,6六个锐例和36客户例的匹配原始/对偶安全值 | 检查七个静态输入；不证明真实SPE聚合桥 |
| tail_minimum.json | 两份完整策略、全末位/终局算术及集合值逆向归纳，最小福利34与36 | 固定36客户实例；一般正规化门槛由数学证明承担 |
| comparison.json | 三份有对应冻结记录的输出完整JSON及逐字节比较，均相同 | aggregate.json未与另一未领旧报告比较，不虚称所有旧运行都已重放 |

## 从当前checkout复现

以下命令从一个有效Git checkout根执行，Python不能带`-O`（原程序用assert）。新输出目录用另一个尚未有相应JSON的名字；三个CLI采用独占写，避免覆盖旧证据。

```sh
mkdir -p workspaces/replay-aggregate-security
python3 archives/customer-attraction/tools/evidence/aggregate-security/original/tests/audits/customer_attraction_aggregate_theta.py --output workspaces/replay-aggregate-security/aggregate.json
python3 archives/customer-attraction/tools/evidence/aggregate-security/original/tests/audits/customer_attraction_aggregate_theta_independent.py --output workspaces/replay-aggregate-security/independent.json
python3 archives/customer-attraction/tools/evidence/aggregate-security/original/tests/audits/customer_attraction_oblivious_security.py --output workspaces/replay-aggregate-security/oblivious.json
```

前三个脚本按自身的`parents[2]`定位所保存的原输入/证书，故保持`original/tests/audits`、`original/examples`及`original/evidence`的相对层级。aggregate脚本只为记录运行版本而调用`git rev-parse HEAD`；不同checkout的这个字段可以变化，数学证书不依赖特定新结果提交。

原尾部脚本直接执行时会写相邻的`audit_tail_minimum.json`。本次使用下面方式完整执行其模块级定义和所有assert，避开`__main__`的相邻文件覆盖逻辑，并把实际报告写到单独位置；原代码没有修改。

```sh
python3 - <<'PY'
import json
import runpy
from pathlib import Path
source = Path('archives/customer-attraction/tools/evidence/aggregate-security/original/research/workspaces/customer-attraction/R-24bfbfd5ec7845b79374a1938c335df7/normalization/audit_tail_minimum.py')
report = runpy.run_path(str(source), run_name='frozen_audit_replay')['report']
out = Path('workspaces/replay-aggregate-security/tail_minimum.json')
out.parent.mkdir(parents=True, exist_ok=True)
with out.open('x') as stream:
    json.dump(report, stream, indent=2)
    stream.write('\n')
PY
```

全部实质代码在原脚本。数学结论和有限结果的对应关系见[精确核验对象](../../../state/计算/静态安全值与聚合保底的精确核验--计算.md)。本目录没有新的一般求解器、没有外部评审证书，也没有将辅助游戏的数据当作单位客户原模型。
