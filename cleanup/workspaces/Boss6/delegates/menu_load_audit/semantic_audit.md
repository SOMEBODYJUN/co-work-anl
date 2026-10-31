---
id: "customer-attraction/early-menu-load-defect-independent-audit"
kind: "review"
type_tag: "审查"
title: "早期真实菜单负载缺陷的独立有限审计"
status: "finite-audit-passed-global-payment-open"
truth_status: "finite exact replay; conditional analytic bridge remains unclosed"
review_level: "full-source-read-replay-and-related-object-comparison"
scope: "B5-EARLY-MENU-LOAD-DEFECT-v1; arbitrary early position candidate, variable real relay loads, local Fraction identities"
source_refs:
  - "clean:c3e4387bcefcaf1c8183:research/workspaces/customer-attraction/R-171cd7d518434f36a48cd50df29c9303/prices/audit_early_menu_load_defect.py"
  - "clean:a145c1b6c7a8d241d9c7:research/workspaces/customer-attraction/R-171cd7d518434f36a48cd50df29c9303/prices/early_menu_load_defect.md"
  - "clean:2413e95a47f7e647a302:research/workspaces/customer-attraction/R-171cd7d518434f36a48cd50df29c9303/prices/early_menu_load_defect_audit.json"
  - "local:archives/customer-attraction/state/审查/R171有符号delta余项与tau支付独立复核--审查.md"
  - "local:archives/customer-attraction/state/审查/R-171接续工作区主张边界与开放义务--审查.md"
---

# 早期真实菜单负载缺陷的独立有限审计

## 阅读范围和对象身份

我完整读取了启动规则、价格目录 README、`early_menu_load_defect.md`（12,191 字节）、审计脚本（6,366 字节）和冻结 JSON（351 字节），并阅读了共同目录完整历史模型、三份末两人价格/负载正文、R-171 有符号 delta 解析复核、R-171 接续边界页及两个相关障碍页。源脚本与清单中的 SHA-256 一致：

- `c3e4387bcefcaf1c8183` / `4fa63b22445756c0f49eef6726f231698dcc8228947da2e0a1c4f7e9a8daa237`，审计实现；
- `a145c1b6c7a8d241d9c7` / `77d40a9102164fbb3e6264e98dc9b097d4cc3cdcb466972fd6e22648933dc07f`，解析候选；
- `2413e95a47f7e647a302` / `5d0d64a13cec377149338a9515f82bdd3281d630a9f0bf38a4ff31f93ae1349f`，冻结审计报告。

CAG-MODEL 的承重量词仍是有限单位客户、有限非空共同目录、单位提供者、全部有序历史上的纯 SPE；脚本本身没有重新实现这个策略树。价格文档把本对象标为 `B5-EARLY-MENU-LOAD-DEFECT-v1`，并明确说一般 Q-CAG-HALF 仍 OPEN。

## 程序实际检查的输入、输出和恒等式

程序只使用 Python `Fraction`、有限笛卡尔积和一个固定随机种子；没有读取外部数据、没有调用 SPE 求解器、没有搜索福利最优值。`U(bg,x,y)=x/(bg+1+y)` 是单客户收益项。`check_identity` 接受一个已有负载 `p`、按当前主题分支变化的中继负载列表 `loads`、当前/末位 membership 位 `ss, rr`、非负组合权 `z` 和参数 `eta`。它分别形成：

- 真实分支的当前偏离松弛 `S`、末位比较松弛 `Z`、真实后继交叉比较 `V`；
- 把所有中继负载冻结在实际分支 `base` 后的参考量 `S0,V0`；
- `tau=sum(z)`、归一化分布 `mu=z/tau`、有符号负载差 `xi,ze` 及 `epsilon(mu)`。

脚本逐项断言候选文档的关键关系

\[
G_0=G-\tau\epsilon(\mu),
\qquad
\delta(\mu)=\epsilon(\mu)-V/\tau^2,
\qquad
G_0=S+\eta Z/\tau-\tau\delta(\mu),
\]

以及固定背景下 `S0`、`V0` 的 `d,L,H` 消元公式和对 `q=0,1/3,1` 的逐客户残差恒等式。它还检查

\[
\epsilon(\mu)\le \Gamma_x\le \xi_x^+-\xi_x^-/4
\]

的有限样本版本，并在“所选主题不增加中继拥挤、末位覆盖分支与中继负载同向排序”条件下断言 `epsilon <= 0`。这正对应解析页的负载缺陷、`δ_*\le\epsilon_*`、四分之一范围界和非恒定负载零缺陷充分条件。

`check_corners` 检查放大矩形域残差在端点取得最大值；`check_range_sharp` 检查放宽的局部模式达到 `Gamma`。代码注释明确后者**不声称是 SPE**。最后两组循环只检查卸载租金上界和全局实际残差的有限参数不等式。

## 独立复跑结果

在独立目录中物化源文件后执行：

```text
python3 audit_early_menu_load_defect.py
python3 -m py_compile audit_early_menu_load_defect.py
cmp -s canonical_early_menu_load_defect_audit.json early_menu_load_defect_audit.json
python3 -m json.tool early_menu_load_defect_audit.json
```

输出为：

```json
{"status": "all exact local algebra checks passed", "scope": "finite implementation audit, no SPE claim and no general welfare proof", "identity_and_envelope_cases": 14288, "parametric_corner_cases": 540, "relaxed_range_sharpness_cases": 300, "unloading_actual_rent_cases": 352, "global_actual_residue_cases": 80, "seed": 202610215}
```

`py_compile` 和 JSON 解析均通过；`cmp` 退出码为 0，重生成的 351 字节 JSON 与冻结 JSON 逐字节相同。计数可由循环结构直接解释：12,288 个确定性 identity/envelope 组合加 2,000 个 seeded 随机组合；540 个参数角点；300 个范围尖锐性组合；352 个卸载租金组合；80 个 residue 组合。

## 语义分类：有限审计、条件候选，不是定理或障碍

本批程序结果应归类为**有限实现审计**。它支持以下有限结论：给定代码中的有限输入，所有 `assert` 通过；边界值和随机样本没有发现代数方向错误；冻结输出与独立重跑一致。

它不能单独升级为全参数定理，理由是：随机部分只有固定种子下的 2,000 个样本；其余也只是有限笛卡尔积；程序没有枚举完整策略树、离轨历史、真实中继策略或 SPE；`check_range_sharp` 明确使用不保证均衡的放宽模式；没有构造客户福利、`OPT` 或 `2W` 比较。解析页中的恒等式和 envelope 由该页自己的推导承重，脚本只能作为实现级交叉检查。

它也不是障碍或反例：没有任何输入产生失败见证、`2W<OPT`、福利比下降或策略不可实现的结论。R-171 13 人 signed-delta 障碍只否定“任意查询/任意最优组合都能统一付清”的加强桥，保留主半覆盖余量；本审计没有撤销该边界。

## 与现有 canonical 对象的关系

- [真实末两人加权分数价格包络](../../../../../archives/customer-attraction/state/定理/真实末两人加权分数价格包络--定理.md) 使用同类 `S/Z/V` 菜单行和矩形域最大化，但量词是固定合法前缀后**恰两名剩余玩家**，背景 `p` 不随当前偏离改变。早期菜单对象新增任意早期位置、真实中继可随 `T` 改变的 `l_T(x)`，以及 `epsilon/delta` 缺陷项；不能把两页互相替代。
- [真实末两人新增与保护分数价格](../../../../../archives/customer-attraction/state/定理/真实末两人新增与保护分数价格--定理.md) 给出 fresh/protected 集的两尾价格和真实末位复制信用。早期对象保留同一真实末位比较，但把中继负载外部性显式留下；一般缺陷支付仍未完成。
- [真实末两主题负载继承](../../../../../archives/customer-attraction/state/定理/真实末两主题负载继承--定理.md) 在额外支配条件 `p_x\ge\alpha 1_A+\beta 1_B` 下直接得到条件福利界。早期菜单文档的 `epsilon_*` 价格桥不假定该支配条件；其全人数结论只在 (9) 的额外支付条件或零缺陷条件下成立。
- [R171 有符号 delta 余项与 tau 支付独立复核](../../../../../archives/customer-attraction/state/审查/R171有符号delta余项与tau支付独立复核--审查.md) 复核了相同标量残差、`S/Z` 归一化和末位信用方向，同时明确没有给出全局 `epsilon/delta` 支付。两者因此互相印证局部代数，但都保留跨全树预算缺口。
- [R-171 接续工作区主张边界与开放义务](../../../../../archives/customer-attraction/state/审查/R-171接续工作区主张边界与开放义务--审查.md) 已把早期菜单缺陷列为“条件价格上界、一般支付未解”；这与本次有限审计的分类一致。相关联合后继负载障碍和 signed-delta 13 人障碍都不是本对象的反例升级路径。

## 独有内容及后续去向

相对上述两尾 canonical 结果，本对象应保留的独有内容是：

1. 任意早期位置的真实中继负载列表 `l_T(x)`，不冻结中继主题标签或后继续局；
2. 精确的 `G0=G-tau epsilon(mu)` 有符号缺陷恒等式，以及扣除真实末位交叉信用后的 `delta_*` 加强；
3. `Gamma_x` 范围包络、仅卸载时 `epsilon_* <= 3P_M/8` 的真实中继利润支付；
4. 条件性全人数半覆盖式 `OPT_m <= W + (m-1/2)u_i + m epsilon_{*,i}` 和允许非恒定负载的零缺陷条件。

这些内容已独立保存到 `cleanup/workspaces/Boss6/delegates/menu_load_audit/` 的 evidence manifest、源快照和本页；建议的将来 canonical 归档位置是 `archives/customer-attraction/state/审查/早期菜单负载缺陷与有限审计--审查.md`，本次没有写入该位置，也没有改写任何 canonical 文件。

## 保留的限制

- `epsilon_*` 或 `delta_*` 没有一般 SPE 下的全局支付证书；不能从局部价格桥推出一般 `B_1(min_i u_i)\le W`。
- 卸载租金界只适用于文档明确的卸载方向；含新增中继负载的任意菜单不自动获得该支付。
- 范围尖锐性和 corner 端点检查是放宽域/有限样本结果，不是可实现 SPE 的锐性证明。
- 没有证明 `2W\ge OPT_6`、一般 Q-CAG-HALF、算法/硬度，也没有建立反例。

因此处置建议是：将脚本和 JSON 作为有限证据保留，将解析页作为条件候选/开放支付义务的审查对象；不要把本批有限通过登记为定理、障碍或主目标完成。
