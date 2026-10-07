# 10｜读懂并独立核验一份精确证书

前面几章证明“存在一个布局和一套客户续局”。本章把这些对象落实成数据。我们要能读出每个概率的含义，重新算出每名客户的条件成本，再检查设施的全部单边偏离。一个程序打印 `passed`，只有在读者知道它检查了什么以后，才成为可以理解的证据。

本章使用[共同目录双设施构造器](../facility_spe/shared_phi.py)、[任意设施数有限构造器](../multi_facility_spe/two_exists.py)和[独立定义级检查器](../tests/multi_facility/definition_check.py)。求解器本轮没有修改。程序的完整命令合同见 [USAGE.md](../USAGE.md)。数学定义已在第 01 章建立；这里重新列出核验所需的全部条件，读者不必猜测程序字段。

## 10.1 输入先表达同一个可达关系

**定义 10.1（显式实例与概率矩阵）。** 一个有 $m$ 个物理地点、$k$ 家带标签设施和 $n$ 名客户的实例，由每名客户的正有理权重 $w_i$、可达地点集 $S_i\subseteq\{0,\ldots,m-1\}$ 以及设施数 $k$ 给出。布局为 $\ell=(\ell_0,\ldots,\ell_{k-1})$。客户 $i$ 在此布局可用的设施标签集是

$$F_i(\ell)=\{f:\ell_f\in S_i\}.$$

客户策略矩阵 $p=(p_{if})$ 中，$p_{if}$ 是客户 $i$ 选择设施 $f$ 的概率。可行性要求 $p_{if}\ge0$，不可达设施上 $p_{if}=0$；若 $F_i(\ell)\ne\varnothing$，该行之和为 1，否则整行为零。矩阵表示各客户独立随机化，不包含跨客户的相关抽签。

共同目录双设施的一个输入按地点列出客户：

```json
{"weights":[2,3,5],"locations":[[0,1],[1,2]]}
```

`weights[i]` 是 $w_i$，`locations[t]` 是地点 $t$ 的覆盖集合。这里客户 0 只可达地点 0，客户 1 可达两地，客户 2 只可达地点 1。省略 `U1/U2` 表示两家共用全部地点；若明确写出两个目录，共同目录程序要求二者相同。

任意设施数入口按客户列出地点。同一可达关系、三家设施的写法是：

```json
{"m":2,"k":3,"clients":[
  {"weight":2,"sites":[0]},
  {"weight":3,"sites":[0,1]},
  {"weight":5,"sites":[1]}
]}
```

两个格式的数据方向相反，不能原封不动交给另一入口。地点与客户编号从 0 开始。双设施证书的 `deviator` 使用 1、2；任意设施数证书的 `facility` 和矩阵列号使用 $0,\ldots,k-1$。同一物理地点上两家设施仍有不同列号。

权重可用整数或精确分数字符串，例如 `"1/3"`。`Fraction` 保存整数分子、分母；等号和严格不等号均用精确算术。任意设施数入口拒绝二进制浮点权重，双设施命令行对 JSON 十进制另有精确解析。下面的核验使用整数或分数字符串，以固定同一个有理输入。

## 10.2 从概率行重算客户均衡

**命题 10.2（定义级客户核验）。** 固定定义 10.1 的布局与可行矩阵。令

$$L_f=\sum_jw_jp_{jf},\qquad c_{if}=w_i+\sum_{j\ne i}w_jp_{jf}\quad(f\in F_i(\ell)).$$

该矩阵是精确独立混合客户 Nash 均衡，当且仅当每名参与客户在其每个正概率设施上的条件成本都等于全部可达设施中的最小值，即

$$p_{if}>0\ \Longrightarrow\ c_{if}=\min_{g\in F_i(\ell)}c_{ig}.$$

**证明。** 客户一旦确定选择 $f$，自己的贡献是完整的 $w_i$；其他客户独立选择，期望贡献是上式中的和。任意混合偏离的期望成本是这些纯行动成本的凸组合。因此当前支持只用最小成本行动，等价于没有任何纯或混合偏离能够降低期望成本。设施期望收益按线性期望等于 $L_f$。证毕。

这里必须排除客户自身再加回完整自重。直接比较 $L_f$ 会检查另一个条件。例如两家设施同址，只有一名重 $w$ 客户，概率行为 $(p,1-p)$：两设施收益为 $(wp,w(1-p))$，但客户两个条件成本都是 $w$。因此任意 $p$ 都是均衡；要求两设施均值相等会错误地只保留 $p=1/2$。

双设施 `shared_phi.py` 的 `exact_ne(a,b,weights,probabilities)` 使用与命题 10.2 等价的差额式。`load_pair` 算出期望收益 `x,y`，对一名重 `w`、选择第一家概率 `z` 的客户执行：

```python
difference = x-y+w*(1-2*z)
if (z != 0 and difference > 0) or (z != 1 and difference < 0):
    raise ValueError("Customer profile is not an exact Nash equilibrium")
```

`difference` 是“确定选第一家成本减确定选第二家成本”。`z != 0` 表示第一家在支持中，差不能为正；`z != 1` 表示第二家在支持中，差不能为负。真混合时两项同时检查，强制差为零。端点与无差异端点都保留。

`menu` 只有通过这一核验才登记条目，`family` 说明条目来自哪种构造。`solve` 对每个有序地点对取第一设施菜单收益最小的条目，计算全目录菜单威胁，再寻找两家都满足倍率条件的在轨条目。这对应第 02 章的菜单 $u$、全目录威胁 $d$ 和两项配额。一个所得因子小于 $\phi$ 的证书仍只说明这个因子可达到；菜单没有包含全部 NE，不能据此宣称实例最优。

## 10.3 站点分配怎样变成逐设施策略

任意设施数程序的 `site_groups(layout)` 把标签按物理地点分组。若地点 $t$ 有 $q_t$ 家设施，`uniform_profile` 把分到 $t$ 的每名客户在该站全部标签上设为 $1/q_t$，其他列为零。这是第 03 章的“地点纯、站内均匀”策略；站内均匀描述每名客户独立抽签，不意味着客户质量真的被拆成几份。

`search_lexmax` 枚举所有物理占据，再枚举每个占据的所有可行地点纯分配。若 `mass[s]` 是分到 $s$ 的客户总重，程序计算：

```python
key = tuple(sorted(mass[s] / len(groups[s]) for s in layout))
```

若某地点有三家设施，该地点在 `layout` 中出现三次，单位设施收益也写入三次。排序向量逐设施计数，随后按字典序比较。例如 $(3,3,7)$ 优于 $(2,8,8)$，因为最先不同坐标是 $3>2$。

占据用 `combinations_with_replacement` 枚举，消去只差标签置换的重复占据。对称性保留排序目标的全部可能值，输出仍保留完整标签，偏离按标签核验。这里是真实的全局穷举；`search_audit.site_allocations_evaluated` 只记录本输入枚举了多少候选。有限全局最大值落实了存在性证明，没有提供一般输入位长多项式算法。

## 10.4 有限条目如何描述完整续局

**定义 10.3（达到倍率的证书）。** 对给定实例和 $\alpha\ge1$，证书包含一个在轨布局、它的精确客户 NE、每个实际单设施偏离后的精确客户 NE，以及所有其余布局的确定默认客户均衡规则。若设施 $f$ 的在轨收益是 $a_f$，每个目标地点 $r\ne\ell_f$ 的偏离收益须满足

$$L_f(\ell^{f\to r})\le\alpha a_f.$$

即使 $a_f=0$ 也检查此不等式；此时任何正偏离收益都使证书失败。

任意设施数 `construct` 的主要字段如下：

| 字段 | 数学含义 |
| --- | --- |
| `on_path.layout` | 带标签在轨布局 |
| `on_path.site_assignment` | 每名客户选择的物理地点；未覆盖记为 -1 |
| `on_path.probabilities` | 定义 10.1 的独立概率矩阵 |
| `deviations` | 每个标签与每个其他地点的一步偏离条目 |
| `default_rule` | 未列布局的固定纯初态及严格改善规则 |
| `factor` | 声明的设施搬迁乘法上界 |
| `complexity` | 本构造采用穷举及有限改善的范围说明 |

`deviation_witness` 对一项偏离以该设施在轨收益 $a_f$ 形成帽 $2a_f$，按主证明分池和装箱，再由 `pure_improve` 完成精确纯 NE。在轨可以混合，离轨可以纯；完整续局并不要求每个子博弈采用同一种策略形态。

一步偏离条目只有 $k(m-1)$ 个。两个不同标签的一步偏离不可能产生同一个新布局：若它们修改不同坐标，新布局在那个坐标上便不同；同一标签改到不同地点也不同。因此条目不会争抢一个布局的续局。`evaluate_continuation` 先查在轨，再查一步偏离，其余布局执行默认修复。

默认规则把每位被覆盖客户先放到最小可达设施标签，再依确定顺序执行严格客户改善。第 04 章的平方势证明它有限终止于纯 NE，因此它确实定义每个未列布局的续局。当前朴素默认修复没有一般位长多项式迭代界。证书无需存储 $m^k$ 行，不代表默认求值已是一般多项式。

## 10.5 达到、最优以及完整性分别怎样核验

**命题 10.4（证书证明的结论）。** 若定义 10.3 的每个客户策略通过命题 10.2，实际偏离条目恰好覆盖全部 $(f,r)$，每个收益不等式成立，并且默认规则对每个剩余布局返回精确客户 NE，则该证书证明本实例有倍率不超过 $\alpha$ 的纯选址近似 SPE。它本身不证明 $\alpha=\alpha^*(I)$。

**证明。** 完整规则在每个子博弈给出客户 NE，所以客户层的子博弈条件成立。在轨每家设施的全部合法单边偏离都已列出，倍率不等式使任何偏离收益都不超过其在轨收益的 $\alpha$ 倍，这正是设施条件。若要证明最优，还须排除全部其他布局及客户 NE 的更小倍率证书；本证书没有这些排除信息。证毕。

独立检查器 `check_ne` 不导入构造器的均衡核心。它先查维数、可达性、非负与行和，再直接重算：

```python
costs = {f: w[i] + sum(w[j] * p[j][f] for j in range(n) if j != i)
         for f in accessible}
minimum = min(costs.values())
assert all(costs[f] == minimum for f in accessible if p[i][f] > 0)
```

`check_certificate` 还核对偏离集合、重新计算收益并检查倍率。其 `all_layouts=True` 对未列布局独立枚举纯 NE，以确认这些子博弈可以完成；它没有自动执行证书指定的默认规则。要检查默认规则的实际输出，须对每个布局另行调用 `evaluate_continuation`。以下复现做两件事。检查器使用 Python `assert`，请按下列普通解释器命令运行；`python -O` 会关闭这些核验断言。

## 10.6 一个可以完整读完的小实例

从仓库根运行 Python 3。若输出已经存在，任意设施数入口会拒绝覆盖，复现时换一个新文件名。

```sh
mkdir -p study_outputs
python3 -m facility_spe.shared_phi examples/shared/tiny.json --output study_outputs/shared.json
python3 -m facility_spe.cli.verify_phi examples/shared/tiny.json study_outputs/shared.json
python3 -m multi_facility_spe examples/multi_facility/rational.json --output study_outputs/kfac.json
```

随后运行以下 Python 代码：

```python
import json
from itertools import product
from pathlib import Path
from multi_facility_spe.two_exists import evaluate_continuation
from tests.multi_facility.definition_check import check_certificate, check_ne

cert = json.loads(Path("study_outputs/kfac.json").read_text())
print(check_certificate(cert, all_layouts=True))
inst = cert["instance"]
count = 0
for layout in product(range(inst["m"]), repeat=inst["k"]):
    p = evaluate_continuation(cert, layout)
    check_ne(inst, layout, p)
    count += 1
print("chosen continuation checked at", count, "labeled layouts")
```

这个输入有 3 个地点、4 家设施和 4 名客户；权重为 $1/97,3/7,11/13,2/5$，可达地点分别为 $\{0\},\{0,1\},\{1,2\},\{2\}$。完整循环检查 $3^4=81$ 个带标签布局，另有 $4(3-1)=8$ 个实际设施偏离。它是这份有限实例的完整核验，不替代任意输入证明。

读输出时先抄下一行概率，按 $c_{if}$ 手算；再抄下一项设施偏离，指出哪些客户失去原设施、哪些增加新选项，重算偏离标签的收益。最后说明 `factor` 是达到上界还是最优值。能够完成这三步，程序数据与前面的数学证明才真正连在一起。
