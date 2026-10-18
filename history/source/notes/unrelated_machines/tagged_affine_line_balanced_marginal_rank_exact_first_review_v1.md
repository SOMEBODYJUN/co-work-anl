# Tagged affine LINE均匀单边际/tiny实际值：rank独立Exact-first重构 v1

审查者：rank_deficiency_fee，2026-10-18。仅读指定Exact后独立重构；未读取作者Proof、作者口头策略、rainbow新策略或其它agent推导。Root已听作者策略，不把其后续核对倒称盲审。本记录先冻，只交root；未改repo/Work/Git。

## 1. 实际读取对象与结论

实际全文读取：

`/workspace/scratch/038d9dcc4cac/tagged_affine_line_balanced_marginal_tiny_value_exact_v1.md`

wholeSHA256：`b081198ffd09ee9e8549c75d4aa2c9d1cef0648a445b45cc6b00f9eb71bb2c50`。

对象ID：`UM-TAGGED-AFFINE-LINE-BALANCED-MARGINAL-TINY-VALUE-v1`。

独立结论：基础/可选padding对象均合法，所有incidence slope marginal均匀，V=1/(R−1)、完整actualOPT=2−1/(R−1)及显式构造/计数均成立，未发现standing fatal。认证不是hypercube、pairwise-independent hard image或困难性。

## 2. 几何/权重/边际逐项合法性

R≥3 prime。变量u_a,v_a各a∈F_R且tag全互异。资源块每tag是F_R²；full state包含每参加变量的一条完整tagged line。Groups M及H_(a,j)，j≠0。u_a的intercepts为M的0及helpers各j≠0，恰R个互异；v_a仅helpers各非零j，R−1个互异。变量degree≤R。

Main state t在全部u_a上slope=t；其唯一正权集合B_t={(u_t,z,tz):z≠0}属于自己u_t line，R−1枚各权1/(R−1)，总1。其它所有full-line incidences仍存在但权0。

Helper H_(a,j) stateℓ在u_a labelℓ，在v_a labelℓ−a−j。若ℓ≠a，给定正权点取z=j/(a−ℓ)≠0，它位于u_a的原line，因为

    ℓz+j=ℓj/(a−ℓ)+j=aj/(a−ℓ)=az。

故该点是B_a中一枚。分母不为0。若ℓ=a，v_a label=−j，(v_a,1,0)满足(−j)·1+j=0，亦在原line。每helper state恰一个正权1点，其余0，总权1。

Main states均匀t使每个u_a incidence标签均匀F_R。Helper states均匀ℓ，其u_a label为恒等、v_a label为平移，均是F_R置换，所以每incidence每label概率1/R。没有将任意state权或positive支持当full几何line；边际是输入显式local distribution，不是由实际YES推导。

## 3. 所有state/partial选择的V上界

记p_a=(v_a,1,0)。对每个固定a，所有R−1个helpers H_(a,j)的任何state，其唯一正点均属于

    B_a∪{p_a}。

它们可任意挑state，但不是预先绑到B_a某点。任何min质量μ>0的partial allocation，都迫每helper实际领取其selected state那一枚正权1点；领取零权点不能替代。

令main所选state为任意t。Block t中的R−1个helpers须领取R−1枚不同正点；其中至多一枚可为共同fallback p_t。因此至少R−2枚不同B_t点已经被helpers占用。Main唯一正权集合B_t大小R−1，最多还能领取一枚，质量≤1/(R−1)。

若某allocation最小值本来0，上界也自动成立。因此这对**所有state choices、所有任意partial subsets**都给V≤1/(R−1)，不假定固定helper选择、不只核某个见证。

## 4. 达界真实资源分配的显式finder

固定任意t，例如t=0，令main选state t并只领取

    m_t=(u_t,1,t)，

质量1/(R−1)。Helpers选择如下：

* H_(t,1)选ℓ=t，领取p_t=(v_t,1,0)；
* 其余所有H_(a,j)选ℓ=a−1，领取(u_a,j,aj)。

后一选择确有ℓ≠a，且其正点z=j/(a−(a−1))=j，完全使用原state。对a≠t，这组helpers j≠0分别领取B_a全部点，互不相同；对a=t，除j=1以外领取B_t除m_t的所有点，剩余helper在不同v_t tag上fallback。不同a的u-tags不交，main只领取m_t，因此全资源共同不交。

每helper获得1，main恰1/(R−1)，达界V≥1/(R−1)。构造只做显式modR运算，无未知allocation/OPT/source解输入；R=3时仍有j≠1的非零helper，所有式成立。结合上界精确V=1/(R−1)。

## 5. 完整actual UM的上下界

完整矩阵每state独立private，每resource独立资源机；每group一selector只能在本组private time1。每full-line incidence独立原job，private按原p（可0）/对应资源机1，其它∞。没有删除zero或unselected jobs。

**达界全部原jobs。** Selector按第4节选态，main m_t对应job及每helper所领取正点job外送；其余全部原incidences留各自private。Selected main负载

    1+(R−2)/(R−1)=2−1/(R−1)；

selectedhelper private仅selector1，unselected private全部原权总1；资源领取不交，所以至多一unit。全部原jobs恰一次、原端合法、同一assignment全机受控；zero jobs留private0。峰恰所写值。

**任意完整actual下界。** C≥2时所需下界自动成立，只看C<2。每helper selector占其实际selected private1，该state唯一正incidence也time1，若留private会成2，故必须真正外送其正资源。资源unit在C<2时至多一job。Main实际selector所在state记t；其block t helpers至多一枚外送fallback，至少R−2枚不同B_t资源已实际占用，所以main最多外送一件positive incidence。Main原正质量1、每正点1/(R−1)，因此至少1−1/(R−1)正private质量必须留在selected private，与selector合计≥2−1/(R−1)。

这里不限制其它unselected states是否也实际外送；这些额外jobs只占资源，不会为main释放更多B_t。Zero incidence的外送也不能减小其正private质量。本下界覆盖全部原任务的任意完整调度。结合上界，actualOPT精确2−1/(R−1)。

## 6. 共同R-arity/R-partite padding

Parts c∈F_R，u_a在parta，v_a在parta+1。R≥3下这两parts不同。Main已有每part一个u变量；对每helper及其余R−2个parts，各加一个只属于该helper的新tag变量w_(a,j,c)，intercept0，stateℓ的labelℓ，整条R点line权全0。

新变量degree1、各state新incidences全保留、state总权仍1。State均匀ℓ给每新incidence label均匀。每helper现在每part恰一变量，arityR；main不变。

V不变：所有新增点质量0，任意padded allocation删除这些点不改质量且保原资源不交；原allocation直接不领新点即可扩展。ActualOPT不变：任意base实际调度将所有新zero jobs放原private0给合法padded同峰；任意padded调度删除新jobs/新资源机限制为原basejobs，负载不增。旧private/selector身份不变，因此上下界都成立，未将新jobs丢弃后冒称原完整schedule。

Uniform单边际不等于pairwise independence：main不同u变量labels均同一t，helpers两旧label相差常数，padding新label也是ℓ；任意这些确定性双坐标joint支持仅R种而非R²种。此页没有pairwise-independent承诺。

## 7. 计数、端点与显式位长

基础n=1+R(R−1)，每group恰Rstates，所以S=Rn。变量2R，资源2R·R²=2R³。Main incidences为Rstates×R变量×R点=R³；helpers为R(R−1)×Rstates×2变量×R点=2R³(R−1)，合

    I=R³(2R−1)。

完整P机器S+2R³、jobs n+I；每incidence两finite端（即便private0），selectorsfinite总S，所以finite=2I+S，dense=(S+2R³)(n+I)。

Padding加R(R−1)(R−2)fresh变量，变量总v'=2R+R(R−1)(R−2)，resources v'R²。State/group不变，每statearityR、每变量R点，故

    I'=S·R²=R³n。

Jobs n+I'、机器S+v'R²、finite2I'+S、dense为其机器数×jobs数。也可由I加每fresh变量Rstates×Rpoints得到同一I'。所有计数均与Exact相同。

唯一处理时间为0、1/(R−1)、1、∞，位长O(logR)；field运算、完整支持生成、上述witness/全原jobassignment与负载回算均按显式对象规模多项式（基础/填充均polyR）。不承诺仅binaryR时poly(logR)输出。R3给V1/2、actualOPT3/2，无退化；R2不在正式域，不擅自扩展。没有有限数值试验作为证明。

## 8. 最终范围与结论

此是原tagged affine LINE的真实完整几何支持：每incidence标签边际均匀但正权高度state相关，degree≤R，实际partial值1/(R−1)趋0。它反驳“此几何+均匀单边际+任意norm1权足以给统一正下界”的合同。

不认证Chan/LST的balanced pairwise-independent code-coset hard image，不把构造称其PCP输出，不提供NP-hard源或source YES/NO gap，不声明源CSP最大满足比例。本例并非cube，也不排额外pairwise independence或其它source结构的桥。

本次独立Exact-first完整重构无standing fatal；构造与上下界覆盖全部states/jobs及所有低负载actual。未读取作者Proof/rainbow新策略，后续作者读后需另冻，原记录保字节不变。
