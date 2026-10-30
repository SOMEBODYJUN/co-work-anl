---
id: "weighted-congestion/ordinal-boundaries-exact-replay-and-faulhaber-correction"
kind: "computation"
type_tag: "计算"
title: "序势边界与Bernoulli纠错的精确核验"
status: "three-original-audits-reproduced-plus-new-independent-correction"
summary: "三原程序实际运行通过，完整产物与冻结报告一致；独立Newton插值补核修正Faulhaber单调性解释，保全源、全部输出、依赖和差异。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:tests/audits/weighted_congestion/marginal_potentials/verify.py"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:tests/audits/weighted_congestion/ordinal_potentials/verify_full_faulhaber_failure.py"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:tests/audits/weighted_congestion/ordinal_potentials/verify_power_objective.py"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:evidence/runs/weighted_congestion/marginal_potentials/evidence.json"
---

# 序势边界与Bernoulli纠错的精确核验

## 完整原件、执行环境与结果边界

本9源全部原字节保存在[original](../../tools/evidence/ordinal-boundaries/original/)，[source-manifest](../../tools/evidence/ordinal-boundaries/source-manifest.json)列稳定ID、全部完整冻结提交/path、大小及SHA；主稿/审查/程序/边际报告均完整实读。另7源只读比较依赖见[comparison-manifest](../../tools/evidence/ordinal-boundaries/comparison-manifest.json)，没有重复认领Boss2三报告或其他已完成源码。

三原程序以原字节实际执行，Python3.12.14，只有标准库：Fraction负责判定，Decimal只负责边际报告的显示，Bernoulli程序用整数 `math.comb`。没有第三方求解器、容差、随机数或外部数据下载。命令、cwd、完整Python/platform、exit与所有stdout/stderr保存在[replay-manifest](../../tools/evidence/ordinal-boundaries/replay-manifest.json)。全部exit0，三stderr均为空。

在证据目录下的实际命令为（完整绝对路径另由manifest记录）：

```bash
python3 original/tests/audits/weighted_congestion/marginal_potentials/verify.py --output replay-marginal.json
python3 original/tests/audits/weighted_congestion/ordinal_potentials/verify_full_faulhaber_failure.py --repo original
python3 original/tests/audits/weighted_congestion/ordinal_potentials/verify_power_objective.py
```

第一程序用显式 `--output`；第二程序完整JSON从stdout保全，`--repo original` 使源码自hash读取本轮保存的**同字节原脚本**；第三程序固定写源码邻的 `power_objective_exact_checks.json`，这个新产物仍保留，并另复制为证据根的 `replay-power.json`。不改原代码，不覆盖集中cache或冻结报告。三次完整stdout另存 `.stdout.txt`，不是仅留最后PASS。

| 原程序 | 新完整JSON | 新JSON SHA-256（与冻结相同） |
|---|---|---|
| 固定边际 | `replay-marginal.json` | `ba0b649a090cd7d64e5286319cd5e391f54cdc14bf53cd6f75f978c9221570ce` |
| Faulhaber | `replay-faulhaber.json` | `d0c4ec1bb03acbcae0ad043755291786e46639146d3bbb40cfcc21697acc5772` |
| 成本幂 | `replay-power.json` | `c2c97dc2c94dbd04e1f0b7ff25b1c369cdc52264d3fc9acf34dc9a917043a671` |

完整比较记录在[replay-comparison](../../tools/evidence/ordinal-boundaries/replay-comparison.json)。源hash和报告hash分列，既不拿stdout摘要代完整JSON，也不删字段后声称逐字节相同。后两冻结报告只作他批材料比较，不进入本9源回执。

## 固定边际程序：精确两序和、误差与非平凡倍率

程序 `orders` 真正求重先/重后有限幂和；`check` 对两条右端黎曼和分别夹在精确积分与网格误差之间，计算比值和严格低于它的千分有理目标。若比值恰为千分有理数，再减 $1/1000$，以确保严格；显示Decimal精度24，不决定任何断言。

9个入报告的 $d=n$ 是2、3、4、8、16、32、64、128、256；$t=2\,d.\mathrm{bit\_length}()/d$ 完全由整数产生。它不是解析最优 $d^{2/(d+1)}-1$ 的精确实现，也没有用超越近似伪装有理输入。额外4个不入records的边界输入 $(d,n,t)$ 为 $(1,1,1)$、$(2,1,1/1000)$、$(3,2,100)$、$(7,13,1/10000)$，同一函数的全部断言都实际执行。另对 $d=1,\ldots,256$ 的32896个系数比 $1/(d+1-k)$ 检查 $1/d\le\cdot\le1$。

报告 $d=2$ 的重/轻权都为1，两序比值恰为1，排除目标 $999/1000$ 不在模型 $\alpha\ge1$ 范围，不能报为非平凡近似下界。$d=32$ 比值约20.908、$d=256$ 约232.369均仅为这些有限向量的下界，不是精确最优 $\kappa_d(w)$。程序不枚举子集图圈、不求最短路或自由玩家乘子，也不建立实际无均衡游戏。任意 $d$ 两序证明、$d+1$ 玩家显式族及[最大圈比等价](../等价/固定权向量边际夹逼的最大圈比--等价.md)来自正文。

## 成本幂程序：九个字面两状态游戏

`costs` 从权、每名玩家的资源集合及仿射系数逐资源重建全部负载/费用。4个 $q=1/2$ 输入 $r=2,3,5,10$，$R=r^2,m=18(r-1)^2$；共享资源各有一个固定用户。坏/好目标分别 $4r-3$ 与 $1+3(r-1)\sqrt2$，程序先检查被平方项正，再用 $16(r-1)^2<18(r-1)^2$ 判严格，不用浮点根号。最大样本1459玩家和1459资源。

5个 $q=2$ 输入 $R=2,3,10,100,1000$，$H=R^2$；固定者同时占用私人基线资源和共享资源。两态费用按实际构造精确等于 $(R,H+1/2)$、$(1,H+1)$，目标差 $7/4$。仅移动者有两策略，所以两态穷尽；严格改善和另一态精确PNE来自正费用及这组完整动作，不是忽略其他玩家偏离。所有9条记录的完整输入参数、目标证书、改善比及结果都在原/新JSON。

本程序仅采样 $q=1/2,2$，不数值外推到任意实指数；通用[凹幂拆分/凸幂基线证明](../障碍/仿射费用下非线性成本幂选态的无界损失--障碍.md)承担任意实 $q\ne1$ 的量词。也不把它计为较早多列对象中缺失的非可分程序恢复：来源、具体构造和实际文件不同。

## 原Bernoulli程序与新独立纠错

原 `bernoulli_numbers` 以 $B_1=-1/2$ 的三角递推产生系数；`faulhaber_coefficients` 双重二项展开 $B_{m+1}(x+1)$ 再减常数。原程序核 $m=1,\ldots,21$、$n=1,\ldots,8$ 的168个整数求和值，以及14次 $x=3/2$ 的负归一化导数和20次 $x=6/5$ 的负函数值，共170项。它的源码SHA字段与本轮原件一致，完整报告逐字节相同。**报告正确不代表原稿的单调性转述正确。**

原稿定义 $Q=\widehat S/x^{m+1}$，却称需要单调增加。一次 $Q_1=1/2+1/(2x)$ 已递减，所以原14次负导数单点不能识别高次新失败。本轮新增[独立补核程序](../../tools/evidence/ordinal-boundaries/independent_faulhaber_correction.py)，用整数求和值的Newton前向插值重建多项式，不导入原实现、不用Bernoulli递推；它不是历史报告或改写原程序。实际执行：

```bash
python3 -B archives/weighted-congestion/tools/evidence/ordinal-boundaries/independent_faulhaber_correction.py > archives/weighted-congestion/tools/evidence/ordinal-boundaries/independent-faulhaber-correction.json 2> archives/weighted-congestion/tools/evidence/ordinal-boundaries/independent-faulhaber-correction.stderr.txt
```

exit0、stderr空，21个次数各核整数 $0,\ldots,8,m+2,m+3$ 共231项；额外4个导数是 $Q'_1(1)=-1/2$、$Q'_1(3/2)=-2/9$、$Q'_{14}(1)=1/6$、$Q'_{14}(3/2)=-19246442/43046721$，另独立核20次负值。完整全部系数、倒数导数、源码hash和Python/platform都在[新完整输出](../../tools/evidence/ordinal-boundaries/independent-faulhaber-correction.json)。新增 $+1/6$ 与原负导数合起来才自足证明14次双向不单调；没有声称原170项包含它。

原文引用的外部论文原Lemma在本轮未取得：官方web HTML/PDF读取均工具错误/空内容，无本地原件。因此正式[Faulhaber对象](../障碍/完整Faulhaber延拓的变号与单调性纠正--障碍.md)只证明自己定义函数的性质，不把当前源稿转述错误归给论文，也不宣称最早失败次数、某个游戏无势或无均衡。

该正文另以已核 $\widehat S_{20}(6/5)<0=\widehat S_{20}(0)$ 推导**字面**负载目标的一玩家使用/空反例，明确它是新解析推论，不增加任何已执行游戏计数；不声称测试了未取得的外文模板或任何不同归一化。

## 比较依赖的实际复用与计算边界

任意乘子程序曾由他批真实复跑四组压缩多尺度证书；有限复制程序曾由他批复跑298项，分为180幂和/单调交叉、54整数复制、64资源置换平均。后者import作者 `finite_ratio` 作比较器，不能称第二独立多尺度全证明。现有[资源可分证书计算对象](资源可分证书的精确核验--计算.md)保存这些真实历史执行；本轮完整旁读相关代码/报告并保全所读字节，没有无理由重复执行它们或把298计入本轮新3运行。其有限报告不能代替[统一跨游戏桥](../定理/跨游戏统一可加序势的复制夹逼桥--定理.md)的一般下确界证明。

所有新产物归独立 `ordinal-boundaries` 目录；没有修改共享README/关系图、别人的正式正文或Boss2报告。程序证据角色限于具体实现、有限输入和新纠错；五个一般数学对象、真实全状态下界与这些计数分别定位，见[审查](../审查/统一序势与非线性选态的量词和纠错--审查.md)。未外审、未认证新颖性或求解复杂度。
