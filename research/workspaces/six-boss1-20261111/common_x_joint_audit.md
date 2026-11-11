# 同一 X 联立系统：核心恢复与 Actions 交接独立审计

Boss1，RUN `six-boss1-20261111`；审计席 `/root/common_x_joint_audit`。
本稿只审具体恢复合同、符号与产物交接，不替代 Main 的普遍数学原件审读。
所有写入限于本稿与同名目录；无优化器调用、无 Git/RUN/registry 写入。

## 1. 当前结论

**23625×21021 基准的 420 个真实交叠核心恢复合同通过独立审读及合成探针。**
没有发现把列 20601…21020 重新赋成 `min(x,q)` 的执行路径。原 7954 个 max
和 2790 个 min 仍分别按原单调方向规范化；两者的合计 10744 与真实 y 严格分离。

同时发现并精确复现了 Actions 结果接收器的五项交接缺口：漏列数组、数值报告
中的数组 SHA 不符、返回缩放漂移、失败执行仍列为 eligible、重复清单名。
生成席已修复；独立复验确认合法 control 仍接收，前述异常全部拒绝恢复资格。
这些缺口影响计算候选与冻结输入的绑定；完整有理 primal/dual 检查仍是最终数学
门槛，不能据此声称旧代码已经产生错误最优性证书。

基准矩阵 SHA256 为
`77781e837b86d7ec8e85634935377fd8183e4c3e945120dc4dd368a40bb1d09c`。
本审计未重跑已完成的数百万逐系数生成器检查，也未读取云端新解。

Main 授权另建的 `common_x_joint_lp/final/` 也已完成增量审计：
**23676×21021、3313758 非零，51 行接口、NPZ 新增尾、六项自足输入和恢复
交接复验全部 PASS。** 最终矩阵 SHA 为
`1b4a4e544e5b9eeea1fa64b3849a9d4cc532b997a5ad972ce33df81c224551e7`。
详见第 9 节。本席没有等待或调用云端求解。

## 2. 实读来源及变量分类

实读 `common_x_own_lift/report.md`、`main_common_X_pair_facets.md`、
`root_x_joint_contract.md` 的 own 合同、`early_x_anchor_queries.md` 的真实分支
及统一 AP 付款、`maxb_h3_bridge.md` 的同一 X 与 H3 接口，并实读
`common_x_joint_lp/` 下七份装配、求解、接收、恢复与证书源文件。
没有把旧 source 文中的“虚拟 upper 可取 min”移植到新 own 系统。

| 零基列区间 | 个数 | 在当前恢复器中的身份 |
|---|---:|---|
| 0…4848 | 4849 | 原核心 |
| 4849…12802 | 7954 | 原规范 max |
| 12803…15592 | 2790 | 原规范 min |
| 15593…20584 | 4992 | shared624 核心质量 |
| 20585…20600 | 16 | 同一个 X 的 hist 核心质量 |
| 20601…21020 | 420 | 真实 X–查询交叠核心 |

核心总数为 10277，辅助总数为 10744，没有新增列。虽然 420 个旧描述符保留
`kind=X-query-overlap-upper` 以维持坐标身份，`semantic_upgrade` 明确覆盖它：
`effective_kind=real-common-X-query-overlap`、`recovery_role=core`、
`canonical_min_permitted=false`。现行恢复器按区间和显式结构分类，不按旧 kind
字样进行 canonical-min 分派。

## 3. 支持、活动面与 canonical 重算

`recover.load()` 核心表必须等于 `range(4849)+range(15593,21021)`，辅助表必须
等于 `range(4849,15593)`；禁 min 表和真实交叠表都必须恰为 20601…21020。

`primal()` 的候选支持先遍历全部 shared624/X/y，再遍历全部原核心，只以当前
数值候选的正质量阈值提议非零支持。没有根据旧点的六个零 hist 删除定义域。
低于阈值的质量被置零只是一次恢复尝试，最终仍须满足完整精确系统；由此
可能恢复失败，不能产生未经精确检查的可行声明。

投影中的 `representation` 仅含原 max/min 辅助，并断言与全部 420 y 不相交。
活动方程保留正支持中的 y 系数；不在支持的核心按零处理，不通过某个 min
表示消掉 y。312 对 shared624 质量等式与 16 对 B4 质量等式的正向行强制加入，
反向行只在选择方程时去重；最终全矩阵核验仍检查正反两行。

`canonical_old()` 只允许写入 4849…15592。它在浮点选片和有理完成两条路径中
均保存 420 y 的前值并逐值断言未变；有理完成外层另保存、核对全部 10277
核心值。随后检查所有列非负、归一恰为 1、每一行精确余量非负、目标与继承
下界关系，最后才保存有理候选。

独立 verifier 不导入恢复器。它重新核原 10744 canonical 等式，并核保存的
`core_solution_before_auxiliary_completion` 恰好覆盖全部核心且与最终值相同。
每个真实 y 必须等于所恢复的支持值，或在缺席支持时为零；没有将其与 min
比较为相等的要求。

## 4. 单调性与全部 scope

基准独立验证器扫描每个原辅助量的全部出现：原 max 的阈值行中只有 +1，
其余为负；原 min 的两个上界为 −1，其他为正，目标和归一均无这两类辅助。
新增 H3/AP/own 行没有原辅助系数。因此原辅助规范化保持可行性。
420 y 在新 own 行中出现负系数，正是禁止其旧单调提高的原因。

全部 16 hist、4992 shared624 隐藏列与 312 对质量等式仍在输入中；旧点六个
零 hist 仅用于旧点诊断，未冻结新点对应质量。旧 point 在基准 verifier 中
先只核旧 22297 行，然后计算新增行的诊断值；没有要求旧完整 point 在新矩阵
可行才允许构造或运行。已知旧点的新负行因此不妨碍新的自由求解。

局部 own 八格仅证明每组 (X,Q,R) 的完成。代码与报告均没有把 210 份局部核
升级成跨组、跨根、全目录共同客户律或完整 SPE；新必要 LP 的有限最优值也
不被当作原六人问题的反例。

## 5. Actions 符号、缩放及 dual

令精确必要行矩阵为 A，规范为 `Ax≥0`，每行缩放 s_i>0。NPZ 保存

`B_i=−A_i/s_i`，供 `linprog(A_ub=B,b_ub=0)` 使用。

数值余量回算为 `(-Bx)_i s_i=(Ax)_i`，符号正确。若 SciPy 返回的 ≤ 行边际
为 m_i≤0，则恢复用 `λ_i=−m_i/s_i≥0`。worker 的

`c−αn−Bᵀm = c−αn−Aᵀλ`

与精确恢复/独立 verifier 使用的对偶恒等式一致。恢复器最终在完整 21021
列重算残差非负，并核全部行/列互补；新 y 与所有其他非负核心使用同一套
残差条件，没有被当作可删除或任意重算的辅助列。

worker 默认只做输入验证，实际执行需 Actions 环境，只含一次 `linprog` 调用，
保存全形状 primal、行/归一/上下界 marginals、residuals、scales 及状态。
空缺数组保留 NaN，失败不自动再求解。源码快照、输入摘要、输出清单及日志
随发现包保存；独立 audit 没有执行 worker 或任何优化器。

原 worker 清单里的 `required_next` 误写 `full22297/21021`，已随交接修补改正
为基准实际行数和 420 core/10744 auxiliary/210 八格要求；最终包须使用最终行数。

## 6. 接收器缺口、修复与独立复现

原 `prepare_recovery.py` 的 SHA 为
`f7c660191effcb27745080f93e67171c86130b9f09918ad8997ac1d6e732b9a1`。
它只逐个检查 manifest 已列出的文件，没有要求必需集合，也没有将数值报告的
数组 SHA 和返回 scales 与冻结输入比较；eligible 未核真实执行状态。

| 合成包，仅测交接 | 原接收器 | 修复接收器 |
|---|---|---|
| 合法完整 control | eligible=true | eligible=true |
| 清单漏掉 `floating_solver_arrays.npz` | 错收 eligible=true | 断言拒收 |
| `numerical.arrays_sha256` 错误 | 错收 eligible=true | 断言拒收 |
| 返回 scales 为冻结输入的两倍 | 错收 eligible=true | 断言拒收 |
| execution exit=1/status failed，数组自报成功 | 错收 eligible=true | 保留材料，eligible=false |
| output 清单存在重名 | 错收 eligible=true | 断言拒收 |

修复由生成席落地，本审计没有修改其文件。已复验的准确源码 SHA：

| 文件 | 修复版 SHA256 |
|---|---|
| `prepare_recovery.py` | `a256fe386630de8168e10dd493805061efa72baa9d4ff1d0f5b8b58e25dfcc9e` |
| `recovery_model.py` | `5bf00f7c026683c91c78766316ea864d2d69631176747f145b76381876645bfc` |
| `actions_solve.py` | `1799a93dbe94d03b1ce9acb189d7c3e8e4bf9d87b1e7bdcb9aa2719795798d65` |

修复接收器要求九个必要输出名、唯一 basename 和安全内域路径；同时核输入
清单、driver 快照、数组的双向摘要、完整形状、availability 的顺序、唯一求解
调用记录、数值/数组/真实 execution 三方成功状态。返回 scales 与冻结 NPZ
逐项相等且有限为正。选择性标准库 NPY 读取只读 scales/shape，避免为这次
交接检查再次载入数百万 CSR 系数。

这些均是可重放的合成接口测试，没有创造或宣称任何新可行 LP 点。

## 7. 非 min 八格与核心不变探针

独立探针直接调用被审代码的 canonical 函数，以 21021 维合成向量覆盖全部
7954 max、2790 min、10277 core。旧辅助初始设为 99，前两原质量为 3/5 与
1/5；重算后全部 max 为 3/5、全部 min 为 1/5。420 y 设为各不相同的有理
数，全部 10277 core 在有理与浮点两种调用中逐值未变。独立 verifier 的
10744 个 canonical 检查也通过。

另测一个直接触及本轮风险的 own 组：

`H=1,m00=m11=0,m10=m01=1/2,x=1/2,yQ=yR=1/4`。

独立八格函数取 β=0，X=1 四格为 `(0,1/4,1/4,0)`，X=0 四格同样非负。
把两条 y 强制改成旧 `min(x,q)=1/2` 后，O6=−1/2，L=1/2>U=0，函数确实
拒绝。这说明探针检测的是“不得改写真实 y”的具体数学差异，而非仅检查
变量命名或数量。

## 8. 可复验资产与边界

证据目录 `common_x_joint_audit/` 包含：

- `baseline_sources/` 与 `baseline_source_hashes.json`：发现缺口时七份源码快照。
- `probe_contract.py`：仅标准库、仅写审计目录的合成探针。
- `baseline_probe_results_v2.json`：同一完整 fixture 对旧源码复现五项缺口。
- `hardened_probe_results.json`：修复源码的合法 control、异常拒收和 core/八格结果。

复验命令使用 `python -B .../probe_contract.py --source SOURCE --expected hardened
--output AUDIT_NEW_PATH.json`；输出路径必须在审计目录且不存在。测试不调用
装配器、数值求解器或 Git；fixture 在完成后删除，只保留摘要和原源码快照。

当前没有恢复云端点，没有声称新 exact optimum，没有排除整个旧最优面。

## 9. 最终 23676 行版本增量审计

### 9.1 已批准的唯一 51 行

Main 明确授权的输入为 `main_prefix_maxx_interface/rows_51.json`，SHA
`1a1876a01a505e74b1497fc1ac1ad62400b93bf648f53bf9966fc630f13b770c`。
本席没有重跑 1440 型数学证明；只对已审定接口做独立坐标复核。

从无权原描述符的 actual bits 重建三条

`SAFE_i=u_i−Σ_h x_h/(b_h+7−i)`，

逐条验证全部 51 行满足

| actual i | 新 C | 旧 C−新 C | 精确关系 |
|---:|---:|---:|---|
| 1 | 206/5 | 9/5 | new = old AP − (9/5) SAFE₁ |
| 2 | 121/4 | 9/4 | new = old AP − (9/4) SAFE₂ |
| 3 | 61/3 | 8/3 | new = old AP − (8/3) SAFE₃ |

全部 5124 个稀疏系数相等；每行 16 个 X 质量坐标齐全；420 个交叠系数与旧
AP 完全相同且为正，每个 y 在全 51 行恰出现三次；10744 旧辅助列没有出现。
actual3 的 17 行还与 `early3_maxx_cone/rows_17.json` 逐项相等，只被追加一次。
新行的真实总行号为 23625…23675，原 own 22365…23624 的索引未移动。

### 9.2 核心、旧证据与 NPZ

最终 `coordinate_structure.json` 除 shape 和矩阵 SHA 外，所有字段与基准
逐项相等，包括全部 core/aux/y 范围、328 个强制质量等式、禁 min 表和语义
覆盖。`own_blocks.json` 的 210 块逐项继承，矩阵引用更新；继承 dual 的全部
旧乘子、21021 项残差和下界值均不变，零延伸区间更新到 `[22297,23676)`。

独立增量检查通过标准库读取最终 NPZ 的 shape、scales、indptr、目标和归一，
并从压缩 NPY 中只取新增 51 行的 data/indices 尾部。旧 23625 个 scales、
23626 个 indptr 以及全部目标/归一数组不变；新增 5124 个 data/indices 与
源精确行的 `−A_i/s_i` 和原列索引逐项相等。尾部终点精确为 3313758。
这没有重复读取并逐系数测试原 3308634 个数据值。

最终源 verifier 自身还核了完整基准前缀、最终全部列、字面公式以及
oldAP−ΔSAFE 两条重建路径；已检查它的实际 PASS 报告及对应 SHA。本席的
增量证据没有伪装成再次执行整份数百万系数验证。

### 9.3 路由、六项自足输入及恢复交接

`recover.py` 和修补后的 `recovery_model.py` 字节不变。最终接收器只将
`WORK` 调整为 `HERE.parents[1]`；worker/准备入口只调整实际尺寸和
`REPO=HERE.parents[4]`，均准确回到仓库根。独立 verifier 的 descriptors、
bridge、own 重建、辅助符号、dual、canonical 和八格函数 AST 与基准相同。

worker 的全部输入只来自同一个 final 目录：

1. `actions_solve.py`；
2. `exact_matrix.json.gz`；
3. `floating_problem.npz`；
4. `structure_and_lower_verification.json`；
5. `inputs_manifest.json`；
6. `runtime_inputs_manifest.json`。

运行清单绑定前五份，请求绑定全部六份；本席逐项核实际路径、字节数和 SHA。
worker 的运行路径不读取基准目录或任何未列出的仓库 Python helper，只依赖
标准库、NumPy、SciPy。Main 的命令准确指向 final worker，输出留在其自身
`actions_discovery/`；没有新建第二次求解请求。

最终代码再次执行与第 6 节同一套 probe：合法 control 接收，五种异常均无
恢复资格；精确/浮点 420 y 不变和非 min 八格的正反例再次通过。

| 最终证据 | SHA256 |
|---|---|
| 精确矩阵 | `1b4a4e544e5b9eeea1fa64b3849a9d4cc532b997a5ad972ce33df81c224551e7` |
| NPZ | `df95f1922e99cd25d28fdef39bbd5137d2d3bf7de2b2ab968203860d120c392f` |
| 独立全结构 PASS | `cf76cfc0005572ba01ef641c955331c0438c2e942af8a31abbf277c19874ebb8` |
| runtime manifest | `3c09448e59a2e3061b2bccd2712fae5ac304badeffaa40c8edbb951b041e1b76` |
| Actions request | `e2eb6280ba08a5fa946b8758f958bebe4e1ced8cc7fde8a4b59d55fa2d8b4b15` |
| 最终接收器 | `3f13f6f76495d7a317cd5758629c09c6deb2554f1111f794b7981b951e0dd552` |
| 最终 worker | `a09339fa1f16a4c3908d99c0390eeb32d1c53cb4bd4492286c1364f0149da28c` |
| 最终 verifier | `d8ca3b8471d9c612a088a786ab84d098e60ed477517d2cb9699b38e16acb4f52` |

新增独占审计资产：`audit_increment.py`、`interface51_probe_results.json`、
`final_increment_probe_results.json`、`final_contract_probe_results.json`、
`final_source_inheritance.json`。最终恢复合同开头的残留基准尺寸叙述也经提醒
由生成席改正；被审可执行源及六输入的 SHA 未因此改变。

**结束状态：本次明确恢复风险与最终增量交接审核完成，未留未修复阻塞项。**
这仅放行已审必要系统的数值发现与后续精确认证流程，不提前认证任何尚未
返回的云端点、LP 新最优值、全目录共同律或完整 SPE。
