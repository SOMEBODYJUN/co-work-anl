# second-only regret compiler：未读作者证明的独立重构

2026-10-24，mixed_menus。审查过程：先仅向global索取精确合同及完整银行策略规则；在未读取其新正文的情况下完成本页重构。本文冻结的是这一阶段，不把后续对稿称作盲审。任意m>=3、一般有限单位共同目录；未证明Q-CAG-HALF。

## 合同与必须保留的fallback

旧完整计划实际根C、second T，实际根收益u、second收益v。选中C孩子仅second节点最大regret δ>0，其所有更深历史均SPE；其它根孩子也需合法补全。另对每个旧根动作A存在一棵真正完整child SPE R_A，旧根在该branch收益<=u，包括A=C。等价u>=M_m；不能由旧计划根IC安全自动推出R_C。

取有理s>=δ。必要时按共同分母复制全部旧客户后取整数银行规模。新目录是旧主题与银行主题的完整Cartesian乘积，客户宇宙互不交。

银行互不交资源为X大小2s、Y大小(m−2)s、m−2个Z_j各s。银行capacity是(2,m−2,1,...,1)，总2m−2>=m。实际银行profile为Z0,X,Y^(m−2)。

## 全history银行SPE与未满capacity

任意银行history已有p个行动，尚余m−p人。空余capacity总数Σ(c_r−load_r)_+>=Σc_r−p>=m−p。存在未满资源。

按剩余人数逆归纳，任何完整银行SPE当前收益>=s：改选未满资源后，所有后继SPE玩家按归纳有收益>=s，因此他们不会选择已经满的资源（该动作即使无后继也严格低于s），最终当前资源不会被过填，当前收益至少s。基础末位直接成立。

所以完整BI存在，任意其出口都满足该性质；已占一次的Z0再选至多s/2<s，所有tail银行SPE均不再选择Z0。

## core-fill完整策略

对global root银行X或Y，若此前只选core且X<=2、Y<=m−2，则规定任一未满core；遇首次Z或core过填后，该整出口后缀固定完整银行BI。

未出口路径最终core刚好填满，当前规定收益s。改另一个未满core也最终s；改已满core无论后继都<s；改Z无论后继都<=s。出口BI保证全部后续历史。因此core-fill为全history SPE，根银行X/Y所得恰s。

## 选中root后n=m−1人的银行修复

global Z0已占，tail只用X(2s)、Y((n−1)s)、其余n−2个未占Z；额外Z0偏离<=s/2。

H：首X之后永久规定Y，包括所有后续离轨history。规定Y最终count<=n−1，收益>=s；改X已至少有一个X，收益<=s；改任何Z<=s。H完整，实际首X独享2s。

L_X：首X后第一tail规定X，此后H。第一tail X最终=s；若改Y，之后H使其最终Y=s；若改Z，整个出口可固定任意完整BI，当前Z<=s。其余节点全SPE。故L_X中首X收益s。

L_Y：首Y后，尚全Y时当前规定X；第一个非Y若为X，此后永久H；若为Z，该整出口固定BI。全Y节点选X独享2s；改Y有后继时下一位X、之后H，当前Y=s，已末位时Y<s；改Z<=s。H/BI两种后缀均SPE。故L_Y中首Y收益s。

L_Z：首Z之后任取完整银行BI，首Z自身收益<=s（重复Z0更低）。所有tail prescribed银行收益>=s，extra Z0从不被选。

以上完整动作规则适用于n=2（m=3）：此时无未占Z，但额外Z0仍可作为低价出口，H/L_X/L_Y的末位边界均成立。

## Cartesian策略与联合偏离

选中global root(C,Z0)后，旧坐标执行给定second-defect计划。joint second恰为(T,X)时用H；任何其它joint second行动(a,q)用L_q。模式只由joint second一次选定，之后旧策略仅读旧history，银行策略仅读银行history。

选中second的实际总收益v+2s。任意联合偏离旧收益<=v+δ，银行<=s，所以总收益<=v+δ+s<=v+2s。没有只检查单坐标偏离。

所有更深节点上，旧坐标为完整SPE后缀，银行为固定模式完整SPE。任何联合偏离的两坐标收益增量分别<=0，相加仍<=0。银行后继不得因更深旧行动重新切换H/L模式。

其它global root(A,q)后，旧坐标用fallback R_A。q=X/Y时银行用core-fill，q=Z_j时任取完整银行SPE。实际root(C,Z0)银行s（没有tail复制Z0），旧收益u；任何root联合偏离(A,q)旧收益<=u、银行<=s，故<=u+s。这包括旧C不变但银行改X/Y，必须用R_C而不能照用有缺陷child。

## 福利和精确范围

实际旧profile保持。银行实际覆盖(m+1)s，最优m槽可取全部m个互不交银行资源，覆盖(2m−2)s。完整Cartesian使旧/银行OPT可逐槽配对，故

    W_new=W_old+(m+1)s，
    OPT_new=OPT_old+(2m−2)s，
    2W_new−OPT_new=(2W_old−OPT_old)+4s。

若先复制旧客户清分母，三项旧值及δ同步按相同比例放大。s=δ允许平局。δ=0时旧计划已无该缺陷，本文不借s=0制造空银行；无须编译。

**盲重构结论：在明确fallback、全history银行规则和模式一次选定条件下，compiler成立。** 它修的是指定第二节点而非任意散布缺陷；若嵌入更早祖先，旧/新祖先收益cap须另核。未将本构造当half证明或自动适用root-only保险。
