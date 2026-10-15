# 低阶成本空间、稀疏资源与 selector dual：独立攻击报告

## 审查对象与结论

审查对象是根对话固定副本 `/workspace/scratch/ecf05625b47b/selector_local_moment_bridge_reviewed_freeze.md`，SHA256：

`f4541469f8aadbb57037b10e1248ed6b1db24d493e31d0d1974c0f85bb6aecbe`。

一般实参数证明的结论为 **PASS（内部独立重构及攻击，非外部审查）**：主待审命题的共同成本空间上界 D、≤D 正系数单项式资源压缩、≤Σm_i 个零费 private-action markers、原 core 结构保持、概率 dual 的 ≤D+1 状态支持均正确。稿中新增的 one-mover degree-moment/separation 等价与 entirely transient parity dual 例也未发现漏洞。没有获得全类 O(d/log d) 上界、动作数或人数 cutoff、或随 d 增长的非存在下界。

审查前先只读 MODEL、既有 finite_action_duality.md 和相关 core 定义，完成 `independent_reconstruction.md` 后才读作者稿。独立重构与原稿在证明接口上吻合，但不是将原稿改写后冒充独立重构。

## 冻结版本的可追溯性

根对话最初给出的待审 note hash 为 `1f852f5f6dd5daedcff77859b31f4be1b71815b70fcd9d6e35434f4949d8fbbb`；我首次实际读取作者目录时其 hash 已为 `3ae034e3a114c5bb4a84e015f450b5008c1f2360461de1ff3fa08e138cb57cc3`。此不匹配当时立即报根对话，不能宣称审查了最初 hash。随后作者又在原路径写入 f454 版，根对话另存固定副本并要求据此审查。

我将初读 3ae 版本和最终 f454 版本分别保存在本目录 `author_read_3ae034.md`、`reviewed_freeze_f4541469.md`，各自 hash 已精确核对。3ae→f454 唯一差异是 §2 增加一般 M=Σm_i 上界：

`D <= M sum_{r=0}^{min(d,n-1)} (M-n)^r/r! = O_d(M^{d+1})`。

该增补正确：对每 i，r 阶基本对称和 ≤ `(Σ_{j≠i}(m_j−1))^r/r!`，再以 M−n 控制并求和；r=0 的项按空积1处理。没有其他数学或边界变化。初始 1f852→3ae 的差异未在本审查中取得，故本 PASS 只挂最终明确固定的 f454。作者 audit 脚本 hash 始终为 `faa86c37eb121de2f12b0a3f0ebf3f5e9b2a6433eef559253ea638f0a9c4efab`；重跑时当前 exact_audit.json 已挂 f454，与重跑结果完全相同。

## 对主证明的攻击

1. **截断空间是否真的共同、是否丢掉自己的动作依赖？** 对每玩家 i，自己动作保持全部 m_i 维函数，对手只取至多 d 名玩家的 contrast 张量。单项式资源的自己的指示量可提在外，资源被使用时自己的负载贡献固定为 w_i；故余式至多涉及 k≤d 名对手。m_j=1 时没有 contrast，公式自然为零维因子。完整空间 W 是所有玩家分量的直和，不能只对单个成本表数维后忘记乘玩家数。

2. **锥压缩是否暗中引入负费用、变次数或损坏全部状态？** 沿线性关系减到一个正系数归零时，其余仍非负；最终只保留原有正项的签名和次数。保持的是完整向量 C∈W，因而所有玩家/状态/真实偏离都保持。系数允许改变；不能同时要求单位系数或原 resource 身份保持。相同签名不同次数作为不同 monomial type 计数没有矛盾。

3. **零费用、空策略、标签与非空资源？** 全零 C 可以保留零个正费用资源；至多 M 个 markers 保证资源集非空及动作标签分开。即使原有空策略，改变其底层集合而保成本合法；稿件没有宣称逐字保留空集策略。m_i=1 不妨碍一般压缩；core 断言另要求每名玩家至少两个动作。

4. **core 空交是否可能被新分解破坏？** 原空交意味着每个原资源对每玩家的动作关联块都 proper。只在原支持中锥消元保此性质；single-action markers 也 proper，并保证非空、反链。若任意选择全部签名字典的新分解，空交可能不再自动成立；稿中明确选原签名，故此攻击不成立。

5. **dual 支持界是否依赖 stationary/recurrent，或只保被压缩资源而漏掉其他列？** B=A_hQ 的 rank≤D。等价地，Ψ_h(s) 是 W 上完整偏离 functional 的坐标。对 augmented `(Ψ,1)` 做仿射消元保持完整 feature vector，因此保全部资源列期望，不依赖先对某一游戏压缩资源。任一已有概率 dual 可减至≤D+1；它不是 dual 存在性定理，也不限制支持为 recurrent。

6. **对 α、权重或算术域有隐藏限制？** 正权保证 MODEL 与一名 mover 的 span 隔离系数非零；α 可取任意实 α≥1。表示与 convex elimination 的证明适用于一般实数据，不因 Fraction 审计只测有理点而退化成有理域命题。稿件未承诺实参数的有理证书。

## 对新增机制的攻击

§4 的相反方向签名产生互为负的 α=1 列，故每个原始非负 test 的期望必须相等。k=0 逼两方向质量均1/2。由 r 次 `(w_i+Σ_{j∈T}w_j1_{s_j=u_j})^r`，顶阶系数为 `r!∏w_j>0`，减去低阶项即可归纳得到全部 categorical degree≤d 的 context moments。所需单动作对手块也是 proper，故 core cone 并不损坏 span。有限凸包分离给严格 polynomial separator 的等价，空方向集合由常数处理。α>1 时只能保留原始非负 tests 的 multiplicative sandwich；稿中没有错误推广到所有 signed polynomials。

§5 的 flag 保证所有支持状态真实 transient：flag0 偶态先翻玩家1成奇态，下一步翻flag；flag1永不离开，并单调清除坐标2,…,m，最后只剩唯一二循环。支持上的成本差为 even/odd parity sum；玩家1完整成本的 active-variable degree≤k+1≤d+1<m=d+2，因此交替和逐 monomial 为零。权重任意正实不改变次数。α>1 再减非负 arrival term 仍为dual。唯一二循环本身也有两边均重dual，故此例只能证明“transient 支持可以可行”，不能证明“transient mass 必要”或“recurrent 限制有无界损失”；稿件已明确这些限制。

“Cross-player compensation in (4) is in general necessary”这一句可由 n=2,d=1 的四状态交替玩家 square selector 具体化：每玩家的两个方向在不同 opponent context，degree1 无法单独匹配；给每条边以 mover weight 的质量可抵消每个 affine resource margin。该句正确，但若整合稿希望完全自足，可补这一小例或链接已有 affine weighted-cycle 论证。它不是主结果的缺口。

## 独立精确审计的范围

`independent_exact_audit.py` 未调用作者实现，以 direct resource loads、anchored categorical finite differences、独立 Gaussian row elimination 交叉核验；输出为 `independent_exact_audit.json`，全部通过：

- 七组完整成本压缩，覆盖 n=1、m_i=1、d=0、分数权、非二元动作、full/core 签名与全零费用。压缩前正单项式数量 1/21/126/63/52/40/0，最终 1/3/14/6/15/10/0，均≤对应 D。最后一组字典有8个可用 monomial types 但原正支持为0。
- 1730 个 order>d 的 anchored categorical finite differences 精确为零；90 个全部玩家/状态成本表位置在各组压缩前后精确相同，包含重复检验位置。
- 两组 n=5,d=0 的32状态概率 dual：α=1 全部真实翻同一玩家，支持压至2；α=3/2 按状态选择不同玩家的 self-move，支持压至10，均≤D+1=11。两组都对1023个完整签名列保全部期望且满足dual。self-move 仅用于一组代数接口边界，不当成 parity family 的真实移动例。
- one-mover span 在动作数(2,3,2)、分数权、full/core两字典、d=0/1/2中，primitive-test span 秩分别等于完整context moment维数1/4/6。
- 作者标准库audit完整重跑，与当前冻结 JSON 的全部字段相同；重跑结果保存在 `author_audit_rerun.json`。该审计本身是有限验证，不能替代一般证明。

代码 SHA256：`b7d1ac642f61fe2ec447c6c3e50c711ce28834795b64236ad3a2cb2c017e9b0a`。
独立 JSON SHA256：`9ce2ccebe46ad8bc255fe4afbef0648308a26a2fdc11b0f0ef2d59d148d85e59`。

## 状态边界

没有未解决的数学 blocker。源路径“freeze”曾被原位修改是已记录并由固定副本、精确diff与hash纠正的 provenance 事件；它不证明数学错误，也不能省略不提。该报告不是优先权或文献新颖性核查，不升级为外部同行审查，不把有限审计当全类增长界。

## 入库路径与最小适配

现行正文[有限次局部矩、全成本压缩与暂态择证对偶](../../../current/weighted_congestion/template_certificates/selector_local_moments.md)与所审f454固定版的数学Claim/式子相同；改中文首标题、身份/状态/导航，删去未需依赖的“cross-player一般必要”解释句，保留“任意selector不保证单mover证书”的范围。两份规范audit只把启动读会话freeze文件求hash替换为所审hash的字面元数据；所有成本、输入、消元与断言不变，令后续研究者无需暂存路径。新源码hash和规范运行由`selector_local_moments.json`、`independent_selector_local_moments.json`记录；本审查前述旧代码hash只标识所审原稿。两份代码路径为`tests/audits/weighted_congestion/template_certificates/verify_selector_local_moments.py`和`tests/audits/weighted_congestion/template_certificates/independent_selector_local_moments.py`。

## Canonical 入库后的只读适用核对

根对话整合后再次只读核对 `research/current/weighted_congestion/template_certificates/selector_local_moments.md` 与 f454 固定版的完整 diff：三条 Claim 与全部承重式保持相同；只有中文标题、状态/导航/审计合同，以及将“cross-player compensation 一般必要”的解释句改为“不保证任意 selector 的 one-mover-supported certificate”。这些变动不改变已审数学命题，故本内部 PASS 适用于该 canonical 数学正文。

两份 canonical audit（`verify_selector_local_moments.py`、`independent_selector_local_moments.py`）逐份 diff 仅有一行把启动时读取 scratch proof 文件求 hash 改为 f454 hash 的字面元数据；全部输入、成本计算、消元、差分与断言均未改，原有限审计适用。后续规范运行的新 source hash 与回放由根对话单独记录，不把本审查的旧 source hash 冒充为新文件 hash。

本次发现并已报根对话的唯一入库问题为正文 §8 的 review 相对链接少一级 `..`（`../../reviews/` 应为 `../../../reviews/`）；它是导航问题，与上述数学及 audit 适用结论无关。本子审查没有修改 repository。
