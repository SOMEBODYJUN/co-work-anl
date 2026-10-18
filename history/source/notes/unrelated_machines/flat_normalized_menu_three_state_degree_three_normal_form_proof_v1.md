# Normalized flat 三态/度三正规形：作者 Proof v1

对应 `UM-NORMALIZED-FLAT-MENU-THREE-STATE-DEGREE-THREE-NORMAL-FORM-v1`；完整对象与全部原P见同名Exact文件。Exact先发root/rainbow，rainbow已仅读Exact独立重构positive path及实际全job逆映射，此后冻结作者Proof。仅发root，未主动发rainbow作者证明。

构造只重构标准selector/单位匹配机制；无新原创、一般UM降度或hardness声明。资源路径步骤依赖先前 `UM-FLAT-MENU-RESOURCE-DEGREE-THREE-PATH-REDUCTION-v1` 的完整实际合同。

selector计数按Exact第1节的flat规则：每树顶点是一group，恰有一件unit selector；该件可去该group的所有state private机器。每indexed state各有一台private机器与自己的incidence jobs，并不各自增加selector。Exact第2节“按同一flat规则”始终采用这一含义。

## 1. 正值分配的前向路径

给源每group选定原state s及资源子集B_g，最小质量v>0。对B_g中的全部资源保留原名、原权、原indexed state；在B_g树中取root至state s所对应leaf的唯一原路径。

路径internal group选通往下一child的singleton state，完整领取该child的own-resource，价值1。路径leaf选原state s并领取原B_g，价值≥v。所有非路径group选自己的own singleton并完整领取own-resource，价值1；root无own但它本来就在路径。K=1时root即leaf，直接采用原state。

这些own-resources互不冲突：路径上的非root own-resource由parent领取；该group自身不选own。非路径group的parent不向它走，所以它的own-resource无人预占。不同旧groups的树/own-resources互异；它们领取的原资源仍是源不交B_g。因此所有target groups同时价值≥v。

## 2. 任意正值分配的逆向路径，不假设单路径激活

给中间target任意allocation min≥v>0。若root internal，它只能选某child的singleton；为了有正值必须完整领取其own-resource a_child。该child不能选own state，因为同一resource已被parent领取，而选own singleton若不领取只能得0。child若internal就只能选一个child singleton并领取；递归同理。有限binary树最终到leaf，该leaf不能own，因此必须选原indexed state s。K=1直接到唯一原state。

收集每旧group g解码leaf实际领取的原资源子集B_g，保留其原state权。leaf在target已得≥v，故原group也得≥v。不同g的B_g仍不交，因为原资源是同一个target对象，分配本已全局不交。

其它分支可能自行不用own，可能另有很多原state leaves在target得到资源；不需要禁止它们，只提取上述root路径的一枚leaf，丢弃额外claim只会释放资源。没有把多个leaves资源合并到一个原state。

有限allocations取最大，1、2节给所有v>0等价；V=0也由正值逆映射闭合。normalized状态给V≤1，helper value1足以保持原正v。

## 3. 任意源actual C<2的全job前向映射

可保留所有旧incidence job的实际目的地：它们原private机器作为相应leaf的原state private机器保留，旧resource资格不改。每旧group的原selector实际所在state s确定上述唯一root-leaf路径。

为路径internal groups选child singleton，给其原selector放对应新private机，将该singleton incidence完整外送child own-resource；路径leaf的selector放原M_gs。其余非路径groups选own singleton、selector放own private，own incidence外送own-resource。所有新增未选state incidence jobs留自身private，时间1。

对原M_gs，原单位selector现由target路径leaf selector替代，旧incidence分配全不动，所以负载与源一致；其它原state private机器上没有新增selector。所有新增private机器负载≤1，新own-resources按第1节各至多一unit。原resource负载与源相同。源C≥1，所以目标全部原jobs完整执行且峰≤C。

这里即使源把未选state的旧incidence也外送，仍原样保留；没有省略或复制这些jobs。

## 4. 任意中间target actual C<2的全job逆映射

内部root selector实际选singleton private state。该state的incidence job若不外送，将与selector形成负载2>C，因此它真正unit执行于对应child own-resource。

若child selector选own state，其own incidence同样必须外送同一own-resource；两个unit同机将负载2，矛盾。故child selector不能选own。继续沿它实际选择的child singleton递归，直到一个leaf实际选择原indexed state。K=1时唯一selector本来就落原state。

现在保留所有旧incidence jobs的实际目的地（旧private M_gs或旧resource R_u），删除全部新增incidence/aux selectors/own-resources与新private机器。每旧group的原selector J_g由target root位置移到所解码原state M_gs。解码leaf的target selector原本已在此机器耗时1，把它删掉并放回原J_g恰替换一个unit；其它leaf若自行激活原state，它的aux selector被删除，只会减负载。所有旧private与旧resource峰因此不增。

未选singleton jobs额外外送只会占更多own-resources，不能撤销路径上由实际selected-state job强制的unit占位。任意target多个分支激活/partial原state导出都被本逆映射覆盖。所有旧原jobs最终恰一次、资格全部原样合法。

## 5. OPT2与复合资源路径降度

两边非空groups的unit selector保证OPT≥1；全部private schedule给OPT≤2，因为每indexed state总private质量1。第3–4节双向保持所有C<2；若任一边OPT=2另一边<2，则逆/正映射矛盾，故中间actualOPT精确等于源，含2边界。

再按资源路径Exact/Proof处理**中间完整菜单**的真实memberships，其双向C<2映射与OPT2闭合给最终P* OPT仍相等；其positive allocation双向及V0闭合给V相等。必须先拆state再降资源度：多个原states现在是不同leaf groups，旧resource degree可以增长，后一步正是按这些真实groups分ports。

## 6. 精确规模及范围

设原group数n，原indexed states总数S，原incidence数I。每个K叶满二叉树有2K−1顶点，2K−2个非root own-resources。K=1单叶也符合以下总计：

- groups 2S−n；
- indexed states 5S−4n；
- 新singleton incidences 4S−4n，另原I件incidences各保留一次；
- 新own-resources 2S−2n。

因此中间全部state/finite资格/机器/jobs线性于旧S+I；source有理权只复制一次，新增权为1。资源路径新增数按中间memberships为多项式；dense P*仍poly源总位长。算法只扫描binary树、实际selector/目的地和路径，不按分母倒数枚举；资源subset witness也显式扫描。

最终K≤3、resource group-degree≤3。group interaction M不声称保持，原state weights归一化没有被解除，Σp>1的普通SC行不在source域。内部groups可以是three-heavy-only，leaf是one-heavy/one-original-state，路径helpers是two-heavy-only；不能声称得到one-heavy/two-diffuse的更窄语法。

此正规形只允许把一份**已经证明**的normalized flat tiny-gap源传到(K3,Δ3)，没有给NP/ETH/UGC源gap，也没有一般UM结构识别算法或全球新颖性认证。
