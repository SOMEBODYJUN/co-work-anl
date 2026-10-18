# PI simplex-coset tagged LINE：作者 Proof 实际读后

Reviewer：bicriteria_set_packing_bridge，2026-10-18。仅 clone 外 scratch；不改 repo、Git、Work 或任何旧 raw。

## 1. 实际读取顺序与正式文件

本 reviewer 先仅据指定 v1 Exact 独立全文重构并冻结；root 实际全文读取该独立源后才取得并解封作者 Proof。本次实际全文读取作者 Proof 的全部 §1–9：

`/workspace/scratch/038d9dcc4cac/tagged_affine_line_pairwise_independent_simplex_tiny_value_proof_v1.md`

SHA256 `4278590caacc424c5df2574ecd8d70a9d53f08fb42f0703aee9bee088913d474`。

对应 Exact：`tagged_affine_line_pairwise_independent_simplex_tiny_value_exact_v1.md`，SHA256 `670bd2deb41f4b5fc9df6ca3f0ed460ca2daaa3a9cca38604561bfff3d7b10d2`。

不改的独立 Exact-only 记录：`tagged_affine_line_pairwise_independent_simplex_tiny_value_v1_independent_review.md`，SHA256 `db3db1a1f09f1392ba880a749959171ea131d044acdb7772e0c315dcadf2112f`。

Claim ID：`UM-TAGGED-AFFINE-LINE-PI-SIMPLEX-TINY-VALUE-v1`。

结论：**PASS。作者全文证明与先行独立重构一致，未发现 fatal、缺失状态、实际调度例外或精确数值错误。** 本次仅认证此 simplex Claim；未读其它新作者推导、其它 reviewer 记录或 one-primary Claim。作者 Proof 关于其自身是否接触 reviewer 推导的描述按其 provenance 声明记录；不作为本 reviewer 可独立观察的额外事实。root 已在 Exact 前与作者讨论，不能记作本 Claim 的 blind reviewer。

## 2. 作者 §1–2：trace、common C、全部 pairs

R 为 odd prime >=3、ν非平方，二次域及 trace 表达式正确。trace pairing矩阵diag(2,2ν)非奇异；T为R+1个不同projective directions。非零w的trace-kernel恰一维，故t0存在且唯一，w=0时全部T可用且first规则确定。任意指定t可取其非零orthogonal w，这也保证helper的positive neighborhood遍及整个D_a。

E map由block0和∞的spanning trace coordinates恢复u、v，故维数4、R^4个不同完整tuples。作者对pair uniform分为同block和异block：同block的不同t forms独立，K→F_R²为bijection；异finite blocks的(u+av,u+bv)为可逆K-linear map，finite/∞同理。因此每个pair精确uniform，不只single marginals。helper是固定coset shift，全部primary/fresh pairs同样覆盖。

coefficient vectors (t,ta)和(0,t)确为F_R^4的全部projective representatives，q=(R^4−1)/(R−1)，common full simplex身份成立。所有groups使用同一C、只改变offset，padded完整q-coordinate tuple对ζ单射；没有把只看一个block时的R²种值偷换成完整R^4个tuple。

## 3. 作者 §3–4：所有 states、固定 j 与真实资源

main v!=0时α=−u/v使w_α=0；v=0时∞ block的w=0，包括全零ζ。其R+1个正点确在intercept0的真实state lines中。helper任意ζ在t0处E=0，真实slope是−j、intercept j，所以z1处正是y0。每helper state仅一正点且norm1，main等权R+1点norm1；其余全部完整line incidences保留私权0。

每个primary只被main和本block R−1 helpers共享，intercepts恰0与F_R^*，degree R；fresh degree1且命名分离。全部state内恰qR个不同资源，变量tag阻止跨变量身份合并。每group一part一个真实变量的padding是完整对象，并非免费假设。

每个helper可通过一个原ζ把onehot置于任意指定t；finite a取(w,0)、∞取(0,w)。给定w_a时恰R²个ζ由fresh labels区分且全部保留，作者不合并它们、不删其zero jobs。fresh的私权全0不代表fresh labels恒0；PI仍来自完整E-coordinate labels。

## 4. 作者 §5：所有 partial 的上界与精确 attaining witness

若某helper质量0，minquality立即<=2/(R+1)。否则每helper必须取得其唯一正点；每block R−1 helpers强迫占用D_a中R−1个不同点。main任意所选state的正质量在某个D_α的R+1等权点上，只剩至多2点，所以质量<=2/(R+1)。这个上界量化所有states及任意partial subsets，没有full-support分配要求；zero/fresh资源不提供额外质量。

main取(0,0)、在D_∞预留2点，再给每block R−1 helpers各配不同点；§4为每个目标点返回原indexed state。helpers质量1，main质量2/(R+1)，资源按tag/block分离，故精确V成立。算法既不需要外部source witness，也不删任何主state。

## 5. 作者 §6：任意 actual 完整σ及全部jobs

attaining全调度将selectors放选中private，main导出两个正jobs，每selected helper导出唯一正job，其它全部jobs留自身private。这包括全部未选states的全部incidences、完整fresh-variable行及私权0任务。资源峰<=1，未选private行和1，selected helper负载1，selected main负载2−2/(R+1)，因此确是完整ordinary实际上界。

对任意完整eligible σ：C>=2时下界已成立；C<2时selector所在private确定一个原indexed state。selected helper的私权1job若不export，与selector同处就负载2，故必须导出；resource端均时间1，C<2使同resource最多一件。由此每block必有R−1个不同D_a点被selected helpers占用，无论其它未选states的jobs如何安排。selected main至多export两个正jobs，其private至少负载2−2/(R+1)。未选states的其它exports只会消耗capacity，无法削弱此下界。

作者没有假定任意σ按attaining witness选态，也没有把所有未选jobs免费丢弃或默认留private作为lower-bound前提。C=2与C=2−2/(R+1)等号均覆盖；前者直接分支，后者由完整witness达到。因此actual OPT的精确值闭合。R=3给V1/2、OPT3/2正常，R2明确不在输入域。

## 6. 作者 §7：ordinary CSP exact value

block trace code中的每个vector至少有一个zero coordinate（非零w的kernel有projective rep，w0更显然），所以不含非零constant vector。不同j的−j·1+C_block cosets两两不交。于是每block至多一helper可满足；若main满足，其每block都在j0 coset，所有非零j helpers均不能满足。任何global assignment最多B个constraints满足，而main满足时实际仅main一项。

所有primary label −1，各block选H_(a,1)并给其专属fresh label0，符合该helper ζ0的完整coset tuple。不同helper的fresh variables互异，所以这些completion同时合法，达到B个accepted constraints。main不能接受全−1 tuple；其余helpers也不能增加同block满足数。因此val_CSP=B/[1+B(R−1)]精确成立。该计算是global assignments的事实，不把local uniform PI certificates当成global consistency。

## 7. 作者 §8：finite O(R^11) 与 dense O(R^19)

精确counts保持：variables q+H(q−(R+1))，states GR^4，incidences I=GqR^5，resources N_var R²，machines GR^4+N_varR²，jobs G+I，finite entries2I+GR^4。私时0端仍真实列出，selectors共有GR^4个finite options。

q、G为O(R³)，variables O(R6)、states O(R7)、resources/machines O(R8)、incidences/jobs O(R11)。因此完整sparse finite-option表和全部state/line资料为O(R11 polylogR)。作者明确指出这不是dense all-jobs-by-machines矩阵大小；dense有O(R19)项（再计log编码），仍是expanded-size多项式。此区别与本 reviewer 独立源中已注明的表示解释一致，无需改旧Exact字节。

ν扫描、field arithmetic、local uniform 1/R4 certificates、CSP达到赋值、选态/分配及全部job assignment均由真实展开对象的固定次多项式控制。R只是binary参数时不声称poly(logR)免费输出；没有compact oracle或按隐藏reciprocal weight复制的编码。原states、fullzero incidences和freshplanes均计入真实规模。

## 8. 作者 §9：唯一 main 瓶颈与专题页审查边界

本Claim排除的是仅从full local pairwise independence、common coset code、common arity/partiteness推出常数actual-export的普遍保证。它是明确易算family，不是NP-hard source或对任意NO source的decoder。q约R³、common C和arity都随R变化，不能当作固定arity且R充分大相关primary硬源的既有image。

唯一diffuse main是最低质量瓶颈；其余helpers全为onehot。移去main后，每block R−1个helpers可注入R+1个D_a点，全部remaining groups取得质量1；所有未选helper jobs留private可给完整实际unit schedule。因此“tiny minquality”不支持dummy/deletion-budget robustness或许多groups同时低质量。作者对此限制的明确写法正确，不削弱本精确V/OPT值。

helpers各共同包含R+1个primary，属于不同于one-primary接口的结构。后续两段专题页可以将one-primary unit escape作为由general审的结构边界，将本simplex反例作为本 reviewer的正式数学scope；本记录**不读取、不认证one-primary Claim**，也不将general的审查写成本 reviewer的审查。待root提供实际最终页面和SHA后，再实际全文读并按明确指定的simplex相关段及相应shared header核scope；目前没有对未给定canonical字节作预先认证。

本 reviewer独立源末尾关于simplex coset只含singleton Cartesian rectangles的辅助观察不是作者§9明写的前提，不用于替代作者scope；也不把它冒称root运行的检查。本文未运行有限数值实验或程序实现，没有外审或全球新颖性认证。旧Exact、独立记录保持原字节，后续范围审查另冻。
