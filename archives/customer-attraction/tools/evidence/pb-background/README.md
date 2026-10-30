# PB任意合法背景反例：冻结原件与精确算术

完整数学结论分别见[PB子SPE反例](../../../state/反例/任意合法背景的前两人额外槽安全值--反例.md)、[实际前缀障碍](../../../state/障碍/PB大背景的最后单例偏离--障碍.md)、[四份审查的范围](../../../state/审查/PB背景反例的全历史审查与版本--审查.md)及[计算对象](../../../state/计算/PB背景反例的标量证据与实际前缀算术--计算.md)。

`original/`按原相对路径保存四份历史审查、一个标量程序及其JSON；全部原字节及来源SHA256核对见[PROVENANCE.json](PROVENANCE.json)。原审查中的历史相对链接保持原样，其中指向的其他独立脚本是另外的来源，不是当前标量复现所需的导入，也未在本批自动登记完成。

## 安全地重放原标量程序

原程序在模块顶层计算，并把JSON写在自己的路径旁；它会覆盖已有同名JSON。请使用一个新的运行目录，避免覆盖冻结原报告。从仓库根执行以下完整步骤；目录已存在时会停止，可另选新目录名：

~~~bash
python3 -B - <<'PY'
from pathlib import Path
import shutil
import subprocess

base = Path('archives/customer-attraction/tools/evidence/pb-background')
source = base / 'original/research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round5/menu/pair_background_scalar_audit.py'
fresh = Path('cleanup/workspaces/Boss3/customer-structure/pb-scalar-fresh-run')
fresh.mkdir(parents=True, exist_ok=False)
target = fresh / source.name
shutil.copyfile(source, target)
assert source.read_bytes() == target.read_bytes()
subprocess.run(['python3', '-B', str(target)], check=True)
PY
~~~

只需标准库。参数在原程序内固定，无CLI参数、外部输入、优化器、网络或随机数。使用普通Python保留assert，不用-O/-OO；-B只禁止pycache。

本轮实际以同样方式在新工作目录运行一次；完整生成JSON与原件逐字节一致，SHA256同为`d332f7fe7584e3ea435637cc286f5562056ea087a7d76edafecd7deacad66f65`。新报告、完整stdout和实际命令/版本/比对在`replay/`。旧“待独立审查”状态是原件文字；后来的数学审查另列，不通过改JSON来制造历史。

## 复算实际前缀障碍的标量

以下只打印同一整数与Fraction计算，不枚举路径：

~~~bash
python3 - <<'PY'
from fractions import Fraction as F

k, d, q, r, Q, H, M = 3, 20, 12, 2475, 2063, 100000, 10**9
L0 = d * Q * (q * M + 1)
L = L0 + r * d * k * q
regular_prefix_bound = F(L0, d * q)
actual_upper = F(1, H * M)
deviation_lower = F(d * q, M + L + 2)
margin = d * q * H * M - (M + L + 2)
assert regular_prefix_bound < H * M
assert margin > 0 and deviation_lower > actual_upper
print(L0, L, regular_prefix_bound, actual_upper, deviation_lower, margin)
PY
~~~

本轮直接重算结果保存在`replay/prefix_obstruction_arithmetic.json`，对应正交叉乘积23504878998176738。这个新记录与旧PB标量报告是两个不同对象。

两个计算都不展开48,495,120名客户或巨大完整策略树。子SPE的全部历史激励和实际前缀的不可能性由各自数学正文给出，代码只核明确标量。
