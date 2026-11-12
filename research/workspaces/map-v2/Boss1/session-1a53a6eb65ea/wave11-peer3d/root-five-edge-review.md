# Boss1：五条现役转移边的限定复核

本记录接收 GATED-XOS-3D 与 INF-CHAIN-3D 两份独立数学报告，只确认其明确列出的五条现役关系及相应端点版本，不接管各 done owner 的其它核心覆盖。原边保持原字节，不重新绑定，不新造相同关系。

## 实读与责任边界

Boss 本轮完整读取两份 proof-review、五条边正文及七个端点的完整登记合同；门控主正文《归一化门控菜单v2三源精读与13-8算法版本审查》本轮重新全文实读。有限 SC 主证明与完整门控值桥沿用同一持续会话此前的原文实读；无限 helper 定理本轮已从第1节读到第10节并独立重构。两个 fresh worker 的 refs 另列其实际新读的作者 Proof、原 PDF 指定页和其它正文区间。Boss 不把 worker 的 PDF 新读冒称自己的 PDF 新读，也不把数学重构等同于重跑科学程序。此次未重跑 LP、历史证书、枚举或审计。

版本检查从当前 registry、现役 edge_files 与真正持有精确资产的 done receipt 三方相认。原目录46e/f72任务已撤回；两条有限/无穷链边的有效持有者是已完成联合3B的862d68637cc402ea。后续整合脚本还须确认当前同一文件 SHA、规范 pin、endpoint pins 和有效 receipt，不能仅凭这段说明清除变更。

## 一、XOS 独立系数界仅支付福利步骤

对单资源，跨组独立的非负系数 a_i，令 X_i=Pr(a_i>0)，V_i=E[a_i]/X_i，并按 V_i 降序排列。容量给 ΣX_i≤1。首个非零者的辅助福利不大于最大系数；前缀成功率由 AM–GM 和凹弦得到

`1−∏(1−X_i) ≥ [1−(1−1/k)^k] ΣX_i ≥ c_n ΣX_i`。

以非负 V_k−V_(k+1) 作 Abel 求和即得 `E max a_i ≥ c_n ΣE a_i`。零概率项删去，n=1时常数为1。目标先按 z 为每组选同一个原 state，再以 x/z 提议，各组对单资源仍独立；X_g=Σ_s x_gsu、E a_gu=Σ_s p_gsu x_gsu。每组实际取得的资源来自其所选同一个 state，故原 max-state 价值逐样本支配赢家系数，不必声称它是最终 bundle 的 maximizing clause。

有限 levels 的尾积分给精确有理条件期望乘积式。逐 state 只枚举 z>0，逐 coin 只走正概率分支，选条件期望不降者。条件化后不重用初始 Σ概率≤1，只重算精确乘积。概率从原有理点重算，分母位长由输入总位数控制，无指数 bundle 枚举、无递归平方。这支付给定可行点的福利步骤；求 LP、平衡化、完整 jobs 回填及13/8余量仍列在原 contribution.remaining。保留 contribution 和原迁移方向。

## 二、一般门控13/8确为完整目标

一般福利 LP 总可行，真实 allocation 选 attaining state 后嵌入，故 W*≤L≤n；不要求 unit-FSLP。值桥正向把 pin 留根，选中 connector 放 gate、selector 放 attaining private，仅导出其真实所得正 incidence；未选 selector 放 gate，其余全部 incidence（含零和未选 state）留 private。完整峰值为至多2−b。逆向 C<2 时每资源至多一个 unit job，gate connector 迫使 selector 到某 private，因而得到质量至少2−C的真实不交 bundles；root 给组数比例至少2−C。故 OPT=2−β*，b=0另用完整峰2基线。

排序得到 b=max_k min(k/n,r_(k))。若 h=#{r>b}>nb，则 k=h直接违背最大值定义；因此 W≤h+(n−h)b≤n(2b−b²)。最优平衡 witness 给 W*≥n(β*)²。合成 W≥(1−1/e)L≥(5/8)W* 后得到 `C≤1+sqrt(1−5β*²/8)`。与 `(13/8)(2−β*)` 比较时，平方余量为 `(209β²−468β+260)/64`；在[0,1]导数≤−50，最小为1/64，两边非负。因此现役 V 边支付全部未知 OPT 的确定性位多项式算法合同，whole成立。

## 三、robust两阈值准确分别处理

R 使用源合同内的福利保证，不只引用最终13/8比值。YES真实 allocation 嵌入 LP 给 L≥(1−η)n。NO_≥和NO_>分别取 h=#{r≥δ}及h=#{r>δ}，低组分别为r<δ、r≤δ；均由 h<γn、δ<1 得严格 `W<[γ+(1−γ)δ]n`。若被接受，L>0且1−1/e>5/8，与域条件矛盾。γ的互补比例是1−γ；统一子域右端最大39/64、左端最小39/64，严格舍入常数支付等号角点。保留两种NO各自的whole合同，不由此声明存在NP源编译。

## 四、固定阈值和同一无穷输出

高正度旧物品的d份owner-private copies与d−1个相邻helper构成路径。旧owner取自己的copy，以其位置为hole，左helper取左copy、右helper取右copy；未用旧物品任选hole。反向正阈值下d−1个helper至少消耗d−1份不同copy，旧玩家至多占一份，故可投影回旧物品。固定t版本helper值t只保证阈值t及相应见证。任意实t的数学公式与显式二进制有理t的位多项式编码是不同量词，不把实数当有限输入。

raw CONFIG 正向取owner边际q_r，容量给Σq≤1，补成w≥q且Σw=1，令W_k为前缀。helper的两singleton质量为1−W_k与W_k，copy的helper负载恰1−w_r，故总负载≤1。反向每helper的每份合法正阈值配置至少消耗一个copy，行质量为1；总copy容量d扣除至少d−1后留下原玩家边际至多1。旧玩家只在自己的copy有正值，逐配置投影不重复旧物品。无需共同整数分配的随机化解释。

取helper=∞时同一输出先于所有有限s>0构造，上述公式均不含s；由全部正阈值可达集相同，整数OPT及最高raw CONFIG阈值的扩展值相同，包括零和无穷。有限H不能替代：s>H时每helper至少需两copy，总消耗2(d−1)>d，整数和CONFIG均不可能。封顶/缩放只是逐阈值证明辅助，不能悄悄改变输出的量词。

## 五、度、规模及来源变化

内部copy为一个旧正端加两个helper端，总正度3；至多两个旧∞端排在路径两端，才保物品∞度≤2。此处DegreeThree约束物品，绝不等于机器或玩家总度三。令S=Σ(d−1)，输出n+S、m+S、E+2S；给定Q项有理配置证书正向支持最多Q+2S，分母乘积的对数不超过输入分母总位长。整数转换、raw CONFIG证书转换和求解配置LP分别说明。

共享来源的零job勘误只把flat互补private配置补成全部incidence，零job覆盖λ+(1−λ)=1。当前五边与端点的证据版本已按此更新；它不改变上述福利、值桥或unit path的数学。维持五条现役语义，不改原定理范围。

## 整合处置

五边全部保留：X为已证局部贡献，V、R和两条阈值构造边均为已证whole。只登记这五条关系的复核与端点，不采用任一拥有任务中未读的其它核心；并发新增的未审变更必须保留。两份独立报告、refs及本记录作为实际整合证据保存。
