# 类内有序三元时钟编译障碍的独立重构与冻结攻击

## 受审对象与结论

本次只审 `WC-CLASS-INTERNAL-CLOCK-COMPILER-OBSTRUCTION-v1`，不重审同文件前七节的两个既有Claim。

- 最初独立重构在未读探索者证明时进行，只得到精确对象和候选目标。
- 作者冻结第8节：`class_internal_clock_compiler_obstruction_section8.md`，SHA256 `e401464769ee2eae6a0a185e1be43e0e19f3425ef29dc91bb33412731a692512`。
- 中间canonical全文SHA256为 `d15bdb03c0815b1ebbc1f4f3d093195c2e70366d9b4ef19fa66c24dda6992c13`。其第8节相对冻结稿只有一项规范补充：新增资源对彼此互不相交且每对仅由指定三人使用。
- 最终受审canonical全文：`research/current/weighted_congestion/class_front_phase_quotient.md`，SHA256 `84bd90dc436541fd5042bd412a09012b73caecc55c652a5bc3ee5b0b706cebcd`。相对中间稿只修订开头三个ID的导航与前两个ID的证据限定，以及第8节的审查状态、独立代码/审查/冻结输出合同。全部实际系数、表格、公式、数学范围与结论未变；这些规范差异已重新逐项核对。

结论：限定在fresh、同权类内、递增三元、两侧同费非负非减时钟的追加架构内，局部一般证明和固定有理反例均成立；独立审计未见fatal objection。结论不代表外部同行评审，也不判定全类近似均衡目标。

## 先重构的局部机制

令同一类权重为w，递增三元为j0<j1<j2，其资源侧为动作位依次异或(0,1,0)。任意类front沿索引至多变位一次，其任意递增子序列因此不可能是010或101。这一点不依赖j0=0；作者从最初锚定三元扩展到任意递增三元是正确的。

于是每一对时钟资源的三名用户分为2+1。对任意参与玩家翻位，只有二人组成员的2w→2w，或单人组成员的w→3w；未参与玩家在该对资源的成本差恒零。前者不改变费用；后者由非减性使当前费用不超过偏离后费用。故任一front对全部单人翻位都是该时钟子游戏的exactPNE，包括翻位后离开front的玩家。

这比只检查合法front端点更强。需要保留的方向区别是：离开front并不意味着对每个参与的稀疏clock都触发；某些clock仍是2w→2w。作者第8.4节已明确避免该误述。

对任意有限族fresh资源对，逐项相加得到每位玩家的clock成本差非正。固定base profile若对所有玩家已有严格负成本差，添加后仍严格负。幅度、时钟数量、费用次数均不进入这个符号论证。非负性同时保证exactPNE蕴含任意alpha≥1的alpha-PNE；所有零费用边界也直接用不等式处理。

## 固定输入的独立资源审计

独立代码不导入作者或仓库的成本函数、phase表及窗口审计。只读取固定输入的八个实际有理资源系数，再自行物化十二名玩家两动作的完整资源子集。每个状态从所选集合累加真实资源负载，对每位玩家的另一动作逐资源重算偏离后含自身的真实负载。物理负载用以16为分母的整数表示，费用用Fraction精确聚合。

作者原fixture源码SHA256为 `ecef0a5f213f2f87b9731dddd7273ff792dce8fd07679c6590c43e2ceea48951`。独立代码与原fixture的全部十二人当前/偏离费用和最小环margin逐项一致；该交叉核对不替代独立实现。

审计覆盖：

- MODEL有效性：三类每类四人，权重(1,1/4,1/16)，64个资源；八个实际系数均正，资源费用次数8。每人恰两动作，非空、互异且互不相交。
- 原同序双轮的24条真实偏离均为严格21/20改善，margin均大于3/4；第8.3节三条gamma的精确有理值全部相等核对通过。
- 指定front相位(0,0,1)的十二条真实偏离均满足old-post<-1/2；第8.3节十二格更强的有理上界逐格通过。这是strict exactPNE，不能误述成仅端点稳定。
- 全部4096个profile、512个product front重新核算。得到16个exactPNE且均strict，24个21/20-PNE，8个exactPNE product front。这些额外有限计数不是一般时钟结论所需，也不推出任何普遍存在命题。
- 对N=1至10全部动作串，核对无任何递增三元010/101触发当且仅当类front；在全部front上枚举17028个三元参与玩家翻位，只有2w→2w或w→3w。3960个合法front边的参与三元翻位均为2w→2w。N=1、2无三元的边界被包含。
- 另直接给固定front追加所有类内递增三元clock，以次数0、1、2、8、16和不同正大幅度交叉检查，均保留strict exactPNE。任意函数/任意次数的结论来自上述一般符号证明，而非这些有限示例。

## 重放合同

独立源文件：`tests/audits/weighted_congestion/cyclic_clone/independent_class_internal_clock_compiler.py`。该文件与独立审查者先在仓库外形成的实现逐字节一致。

源文件SHA256：`b3311dffb851cdd5e5cf5778212291d19f8e2ffb3f85b0274346a0fdd8aeaeaa`。

执行命令：

```sh
python3 tests/audits/weighted_congestion/cyclic_clone/independent_class_internal_clock_compiler.py
```

程序只向stdout输出JSON，固定八个有理实际系数写在源码中，不接触或重写任何冻结证据。输出记录Python版本、真实执行命令、源码hash、冻结第8节hash、原fixture hash、精确范围和完整front费用。canonical运行记录应存为 `evidence/runs/weighted_congestion/cyclic_clone/class_internal_clock_compiler_obstruction_independent.json`；仓库外首次精确运行输出与之区分，不原位重写早期冻结记录。

## 攻击边界与未解义务

1. fresh且只有指定三人使用是局部负载计数的必要架构假设。多个clock共用同一资源对、外来玩家负载或辅助玩家均未被排除。受审canonical已经显式写清。
2. 两侧同费、同权、非减性均被真实使用；不能外推到跨类时钟、两侧不等费或乱序相位。
3. 固定base严格21/20环只是输入性质；添加clock后不要求保留原环。均衡保留结论已经足够否定“对所有这种输入仅追加允许clock即可得到无21/20-PNE”的compiler。
4. 本fixture只提供倍率21/20的输入反例，不自动排除仅面向更大、随次数增长倍率或带额外输入假设的compiler。第8.5节明确未证明所有近线性倍率base都有稳定front。
5. base次数为8，添加任意次数clock后的最高次数可以变大。障碍是任意次数输出均保留exactPNE，不能误写为所有输出仍是degree8。
6. 非负非减一般函数用于局部引理；其中非负系数多项式子类完全满足MODEL所需。没有外部均衡定理或未检查的theorem import。
7. 正文开头的两个旧Claim及其原第5节反例身份不得被新固定输入替换。新的ID和证据合同须独立接入；数学结论没有升级为全类Cd/ln d命题。

未见上述范围内仍成立的实质反驳。唯一全类问题的量词不由这个固定架构反例闭合。
