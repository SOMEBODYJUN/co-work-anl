# 1269行必要条件点上的最优交换范围

状态：固定证据点的精确读出；不是新的六人SPE或半覆盖证明。由本轮 six_3 提出，父方按原 JSON 独立用 `Fraction` 汇总。

冻结输入：`research/workspaces/customer-attraction/R-3e17a9e6e3f747fd9cca4f93b99486d6/astra/promotion_joint_atoms_exact.json`。其中 `histograms` 有16项，每项 `d=1`，`d` 是六个最优比较主题的会员重数。29项 `RZ_atoms` 权重总和恰为1，正质量只在 histogram 索引 `[2,3,4,5,6,7,9,11,12,13,14]`，所以 `d=0` 质量恰为0。`promotion_states` 给多个条件菜单的隐藏位权，不能把各菜单权重再次加为客户总量；其引用的 histogram 也全有 `d=1`。

可在仓库根重放核心读出：

```python
import json
from fractions import Fraction
from collections import defaultdict

p = 'research/workspaces/customer-attraction/R-3e17a9e6e3f747fd9cca4f93b99486d6/astra/promotion_joint_atoms_exact.json'
a = json.load(open(p))
h = a['histograms']
mass = defaultdict(Fraction)
for atom in a['RZ_atoms']:
    mass[atom['hist_index']] += Fraction(atom['weight'])
assert len(h) == 16 and {row['d'] for row in h} == {1}
assert sum(mass.values()) == 1
assert [i for i in range(len(h)) if mass[i] > 0] == [2,3,4,5,6,7,9,11,12,13,14]
assert sum(w for i,w in mass.items() if h[i]['d'] == 0) == 0
```

于是此固定点的全体客户都在比较并集 `O` 中。任何在其客户支持上选择的合法回复主题及有限个回复的并集都不能覆盖 `O` 外的客户。将某些比较主题替换为回复主题的最优覆盖基数行左侧新增客户恒0、右侧失去客户非负，因此这些行均自动成立。该判断只说明 **此点** 无法靠纯 `OPT` 交换基数行排除；它不判断其他点，也不处理实际真实策略、早期玩家利润或新的跨枝 IC。
