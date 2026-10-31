# 归一化flat菜单的三态/资源度三正规形：Exact-first 独立审查

审查者：general_query_response_review。2026-10-18。

冻结前仅读取本Claim Exact及获准的路径归约Exact，未读取typed/rainbow/root作者论证或任一Proof。

- 正规形Exact SHA-256：`33094582e9804d6a0a7aaa78122b5eac90e2fb65e5d9089aa939b7b618092a29`
- 路径依赖Exact SHA-256：`7bbfc817db6081f574f7d2dd6c171c2b587152809c87adb071f99e5334635835`

**明确结论：按所述完整normalized flat域，新正规形有效，无fatal。以下独立重证树步骤与路径步骤，给任意positive whole-state partial witness及C<2完整actual schedule的双向算法；V0/OPT2另处理。**

## 1. 必须保留的实际对象及K1

原state的W恰1，全部incidence jobs（含p0和全部未选states）始终存在。原state/private机及其incidences可保持原identity，树中成为对应leaf的original-state分支。每原selector J_g成为root group的selector；K_g>1时它的目标资格确实改成root新state机，不声称保留原selector旧资格。Leaf groups拥有自己的新增selector jobs。

K_g=1时树仅一个root-leaf，无own resource、无新增group/job/state；root菜单就是唯一原state，原selector和资格均不变。这一边界无须启动不存在的root singleton。原state未必是“diffuse”时间型：它可本身是unit singleton；解码要求的是原state分支，不添加轻端假设。

## 2. 树步骤：任意positive partial allocation的两向映射

令0<v≤1。每份witness每group选一个state，并取得该state内的资源子集；资源跨groups互不交。

### 正向

源g选原leaf s并获得原资源子集B_g，质量≥v。取其root-to-s路径：

- 路径上每个internal Q_x选往下一child y的singleton {a_y}，取得a_y，质量1。
- 终点leaf Q_s选原state分支，取得完整给定B_g，包括其中可有的零权资源，质量≥v。
- 其它所有vertices选择自己的own singleton并取得a_x；root不在此列，且所有off-path vertices都非root、确有own state。

每个a_x恰用一次：若x在主路径非root，由parent取得，Q_x不用own；若x在off-path，由Q_x自己取得，parent没有选择它。旧资源与own资源fresh隔离，不同原trees的own资源也隔离。原B_g跨g不交。因此全部新groups同时满足≥v，指定原leaf与B_g精确保留。

### 逆向：不假设只有一条活路径

给任意中间target value≥v分配。若root-leaf，直接读其原state分支及资源子集。否则root只能选择某child y的unit singleton。因v>0、资源不可拆，该singleton必须得到完整a_y。

故Q_y不能选own singleton：否则它也必须取得a_y，与root的分配冲突。若y是internal，其实际state只能选某child own resource，继续；若y是leaf，其实际state只能是原state分支。有限树必终止于一个实际选原state的leaf，其所分原资源子集质量≥v。

其它off-path groups可以任意改态，甚至另外选多个原state leaves；不妨碍这条由root实际选择和资源阻塞强迫的下降链。每原g只解码该root链的一个leaf及其bundle，忽略其它leaf选择；源本来只需每组选一个state。各抽取bundle是target已有互不交bundles的子族，所以仍全局不交。

因此树步骤给每个正阈值的精确iff。该decoder的“保留/可解码原state及subset”指forward给定原选择、inverse的root链选择，不声称把同一旧group的所有off-path leaves同时当成源选择。

## 3. 资源路径步骤：仅据其Exact独立重证

在树后的实际groups上，对某资源u的d个incident groups按顺序建ports z1,...,zd及d−1个helpers，helper j可选unit singleton zj或z(j+1)。每旧group的全部states用同一port，不按state分配不同port。

### Positive allocation

若原资源u由第k个旧group取得，就把它改为zk，并让helper j在j<k时取zj，在j≥k时取z(j+1)。若u未分配，任选一个k作为未用孔。每helper得一个不同port、质量1，原bundle质量和原state不变。

反过来，任意positive target allocation使每个helper取得其实际选中的整个singleton port；d−1helpers占用d−1个不同ports，因此旧groups合计最多取得一个port。把旧port zk逆映为u，不会产生跨组资源冲突，且p保持，所有原partial subsets和states保留。d1无helpers，d0可保unused原机或在解码时恢复其idle机，均不影响值。

### 任意完整actual C<2

每helper所选private机的selector1与singleton incidence private1不能同时留private，否则load2。因此该selected job必export；各resource端时间1，C<2迫d−1选中helper jobs占不同ports。其它未选helper jobs可以自行export，但只会进一步占用ports；旧jobs因此仍至多有一个跨ports export到同一旧u。逆映全部旧job原private/原resource端后load不增，删helper jobs得到完整旧schedule，完全不要求target预先是规范matching。

正向任意旧C<2调度，每旧u最多一枚unit export。为该旧job所属group的port留孔，其它ports按上述匹配交给helpers；若无旧export任选孔。全部旧job private端及selector不变；每helper selected incidence export，selector放该private机，另一state incidence留private。每新private和port负载至多1≤C，故得到全部jobs的完整实际target≤C。原p0 job若被export也按真实unit export占孔，不忽略它。

## 4. 树步骤的完整actual schedule映射

对任意normalized flat实例，完整C<2调度给positive selected-state allocation：取每selector实际所在state及该state已export的资源子集。全资源unit且C<2给子集跨groups不交；所选机private负载恰

\[
1+1-\text{exported private mass}\le C,
\]

所以每group export质量≥2−C>0。零p exports可以保留在subset中，不改变质量。

反向给value≥v的whole-state partial allocation，selector放实际所选state，所分资源的对应incidence jobs export，其余所有states全部未export jobs留各自private机。每selected机≤2−v，未selected机恰1，资源机≤1，所以全部原jobs实际峰≤2−v。没有漏掉未选states。

据此，source σ的C<2取v=2−C，按第2节构造树allocation，再上述规则实际生成中间全部jobs。原J_g在root新机，新leaf selector在所选原leaf机；原selected leaf inc jobs按给定subset export，原unselected states inc jobs全停原private，总量1。所有新增singleton states的incidence也全部执行：selected者export、未selected者private1，每新增selector恰一次。完整peak≤C。

任意中间actual τ的C<2，同样提取其actual selected-state subsets，按第2节的root阻塞链解码一枚actual原state及其actual subset。源J_g改放解码的原leaf/private机，其unit负载替代target新增leaf selector；全部未选原states的incidences停private1，所选leaf按抽取subset export。其源selected负载≤C、其它private1及resource≤1，全部原selectors/incidences仍各执行一次。原target root selector不是被丢弃，而是同一源job重定位至源合法leaf机；新增tree selectors删除，不重复执行原job。

组合时先树后path：正向完成树actual再用路径映射；逆向先从任意P* actual恢复完整树actual，再root-chain解码。每一步≤给定C<2，不调用OPT或见证oracle。

## 5. V0与OPT2：不在端点偷用资源独占

所有实例仍normalized、finite explicit、nonempty groups，V∈[0,1]，actual OPT∈[1,2]：全private加selector基线峰2，selector强迫至少1。

两步骤对全部positive v有iff，因此V精确相等。若一边V0、另一边正，则取后者的正有理达到值作v即矛盾；不需要对v0任意分配作root-chain decoder。v0时singleton可未分配，阻塞未必成立，Exact并未作该错误要求。

对OPT，若一边有<2 actual，则上述完整映射给另一边不更大；对两边有限达到的<2最优值用双向映射即相等。若源OPT2而target<2，逆映给源<2矛盾，反之同理，故端点也相等。不从C=2断言resource独占。也可用已独立证明的normalized relation OPT=2−V，但actual双向证据已经单独给出。

## 6. 先后顺序、显式数量与bit complexity

令原group数m、state总数S=ΣK_g、incidence总数L。树步骤对任意K≥1精确有：

- vertices/groups：2K−1；own resources：2K−2；
- original-state branches：K；new singleton states：4K−4；
- total states：5K−4（K1也正确）。

总中间groups=2S−m，states/private机=5S−4m，own资源=2S−2m，incidence jobs=L+4S−4m，selectors=2S−m。旧原jobs中仅selector资格按声明修改，原incidences未复制；新增对象均是实在physical jobs/machines。

记树后真实resource-group membership总量D。按完整菜单计，包括p0，D≤L+4S−4m。路径ports数D，helpers数H=Σ(d_u−1)_+≤D，每helper添两states/private机、selector一件、incidence两件。故最终每group≤3states、每resource≤3groups（一个旧group及至多两个相邻helpers），所有数量O(S+L+|U|)。Dense jobs×machines矩阵也poly。

必须树后再算ports。旧group多个states拆成不同leaf-groups后，同一原资源membership可以大幅增加；若先降度再拆leaf，其port可重新被很多leaf-groups共享，不能保证finalΔ3。当前顺序正确。

所有新private权1，旧有理p原样复制；binary tree大小O(K)、路径长度按显式membership，解码最多扫描这些vertices/ports/jobs，不按1/v、1/(2−C)、分母或时间数值展开。给定actual负载为有理部分和，阈值2−C及输出时间表的位长poly。

## 7. 范围

严格norm1是actual未选state负载1和2−export质量公式的实质前提，不把任意Σp>1的SC行免费纳入。Original菜单已显式；增加groups/resources的全局耦合也不与先前“同U逐玩家显式norm1菜单规模”障碍矛盾。

不声称M保持、所有groups one-heavy/two-diffuse、源hardness已闭合、general UM可免费分解成flat、或新全局算法/反面。内部groups可有three-heavy singleton states，leaf是one-heavy/one-original-state，path helpers是two-heavy，分类准确。

**最终独立冻结：新正规形Exact及所用路径Exact在上述全域内有效，无fatal；未读取任何作者Proof或他人论证。**
