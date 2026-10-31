---
id: unrelated-machines/flat-unit-resource-path-k2-canonical-section12-review
kind: review
type_tag: 审查
title: flat 单位资源路径 K2 canonical 第12节读后复核
status: integrated-source-cleaning
truth_status: restricted-certificate-equivalence-review
review_level: informed-canonical-read-after
summary: "冻结 canonical 文本只读 §12/12.1--12.7；在已审 Exact、independent-first、Author Proof 和 read-after 基础上，复核 degree-four K2 双向有限有理证书转换，未追认旧 prefix。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/sol_flat_unit_resource_path_k2_canonical_append_review.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/source/notes/unrelated_machines/sol_flat_unit_resource_path_k2_canonical_append_review.md"
source_ids:
  - "401d4f62a09ea94d0a16"
source_sha256:
  - "0945c8b2cedbe4661ad6e6a5433254a045220bb6c4a27b097406c9dca1839526"
source_blob: "ff7947f384d2e5f4c207ceb6f2a6bb1dd1ba9b6c"
evidence_manifest: ../../tools/evidence/sol-flat-unit-resource-path-k2-canonical-append-20261031/manifest.json
related_objects:
  - "./flat单位资源路径K2证书合同四源清洗--审查.md"
  - "../定理/完整菜单的资源度三路径归约--定理.md"
---

# 1. 实际阅读范围与版本身份

`401d4f62a09ea94d0a16` 是 `sol_flat_unit_resource_path_k2_canonical_append_review.md`，冻结 SHA-256 为 `0945c8b2cedbe4661ad6e6a5433254a045220bb6c4a27b097406c9dca1839526`，大小 10673 字节。该源是已知 Exact、independent Exact-first、Author Proof 与 author read-after 之后的 informed canonical review，不是新的 blind review。本文只把其释放的 canonical §12/12.1--12.7 当作实际语义阅读范围；旧 §1--11、canonical review 链接及未释放的 native C2 文本只做来源指纹，不替它们签字。原文报告其先核全篇 hash/长度，再逐行读 340--536；本轮也以 `clean show` 导出后完成全文阅读。

既有四源对象已分别记录 D_+ 路由、完整 ordinary jobs、全局 M2、同机 first/pair CONFIG、可选 affine load localizer、正向 hole 与逆向 extra-export/selector-difference。canonical §12 的独有内容是把这些条件固定到新的 `UM-FLAT-UNIT-RESOURCE-PATH-K2-PRESERVATION-v1` ID，核对次数上界、inactive/zero incidence、四次次数账本、所有原 moments 保持和位复杂度；它没有改变四源主量词，也没有提供新的调度、硬度或软件证据。

# 2. K2 合同的准确域

域为有限显式 normalized-flat ordinary job 矩阵，所有 indexed states、selectors、incidence jobs、正/零 incidence、未选状态 jobs 与 unused resources 均保留。每个旧单位资源按 distinct original groups 形成 D_+ ports；同组多个 indexed states 共享 own port，零 incidence 仍是独立 job，有 own port 时走该处，否则走固定 fallback port；`d=0` 旧资源不删。每个正邻居相邻 port 之间加入两根 private、两状态、单位 selector/单位 incidence 的 path leaf。不同旧资源标签不合并。

参数是有理 `1 <= T < 2`。证书包括每台机器权和为 1、负载至多 `T` 的有限有理 CONFIG 列表，以及共享所有 job 一阶和同机二阶 membership 的有理 degree-4 Boolean moment functional `L`。`L` 满足四次 Boolean/exact-one-hot 恒等式，并对所有 degree-2 多项式平方满足 M2 PSD。可选合同条件是每台物理机及所有全局 affine `q` 的 `L((T-load_i)q^2) >= 0`；两侧必须同时启用或同时省略。结论是给定完整有限有理证书时，原问题与 D_+ 后问题在该 typed K2 合同下可行当且仅当，且证书转换在输入和证书位长上多项式；它不是任意实 SDP 可行性的搜索算法。

# 3. 次数与 null 账本

`T<2` 使单位机合法 CONFIG 至多放一件 distinct job，所以同机 endpoint 指示量的二阶边际为零。Boolean 恒等式将其平方仍置零，M2 Cauchy--Schwarz 再允许与任意 degree-2 multiplier 相乘。对同一 job 不同端的 one-hot pair，交叉期望由 Boolean 二次项平方非负并逐项归零；不能把一阶 one-hot 直接跳成任意高阶恒等式。`L(r^2)=0` 的 degree-2 `r` 可乘 degree-2 多项式，生成 degree-4 radical。

canonical §12 明确核算：Boolean 恒等式乘到 degree 4，job one-hot 也乘到 degree 4；unit CONFIG 的 `K^2-K` 乘任意 degree-2 multiplier 仍在四次内，`0<=L K<=1` 分别来自 Boolean PSD 与 `L((1-K)^2)>=0`。因此式 (12.6) 的差值 `(K^2-K)q^2` 可消去，右侧剩余项是 degree-2 平方。不存在额外假设所有 quartic literal 非负，也不存在把 CONFIG 权重当全局随机变量的步骤。

# 4. 正向 canonical 构造

对每旧资源把全部原资源端指标（包含 zero 与 inactive exports）按 D_+ port 写为 `O_1,...,O_d`，`K=sum O_i`、`Q=1-K`，固定 hole port `f`，令 `H_i=O_i+1[i=f]Q`。`H_i` 是由旧 unit-clique radical 支持的互斥 affine holes，和为 1。新叶 `j` 取 `L_j=sum_{i>j}H_i`、`R_j=1-L_j`；所有新变量是旧全局变量的 affine forms，四次 moment 表由 pullback 定义，故 Boolean、one-hot、M2 与旧 joint moments 保持。

端口 load 为首 port `K`、中间与末端为 1（`d=1` 时仅有 `K`）。派生 affine Boolean 与 M2 给出同端口不同 unit jobs 的 pair-null；用一阶权和 empty residual 重建合法 CONFIG。新叶 private root 的 selector 与 incidence 互补、负载恒 1；旧 private-root lists、zero jobs、所有旧 moments 原样保留。若有 affine load localizer，旧 root 直接 pullback，满载 ports 为恒等式，hole port 用旧资源 localizer；不需要新的 SDP oracle。

# 5. 任意反向证书与 extra-export

反向不假定叶使用 canonical assignment。叶 selector `(a,b)` 与 incidence port indicators `(x,y)` 的 private endpoint 冲突给 `a(1-x)=0`、`b(1-y)=0`；由 `a+b=1`，`(1-x)(1-y)` 为 null，故 `e=x+y-1` 是 degree-4 affine Boolean extra-export。每个旧 port 的 unit job sum 定义 hole，精确计数包括全部旧 routed exports、每个 hole 和所有 extra-export，等于 1；zero 与 inactive incidence 不能删除。

各项一阶和及两两乘积非负。将计数恒等式乘一个 summand 并使用 Boolean 性，得到不同原 exports（含不同 ports）的 pair-null；以每个原 endpoint 的一阶权和 empty residual 重建旧 resource CONFIG，保留原 moments。`d=0` 直接保留，`d=1` 由同机 unit pair exclusion 处理。作者 Proof 的 selector-difference 路线以 `L_0=1,L_d=0`、内部 `N_i=L_i(1-L_{i-1})` null 和 `H_i=L_{i-1}-L_i` 证明 hole pair-null；它与 independent-first 的 empty/extra conservation 路线相容，但不是第二个联合概率法则。

# 6. 计数、位长与限制

令 `L_+=sum max(d_u-1,0)`；每叶新增两根、一个 selector、两 incidence jobs，新增 finite endpoints 为 6。全矩阵机器数为 `S+2L_++m_+`，jobs 数为 `n+I+3L_+`，finite endpoints 为 `S+2I+6L_+`，且 `L_+` 不超过显式正 incidence 数。degree 固定为 4，affine 展开只读取已有 moments，分母位长按输入证书多项式增长；不按 `1/probability` 展开，也不声称任意最短 CONFIG 证书的统一搜索复杂度。

`T<2` 是 unit pair exclusion 的关键；`T<1` 时原 unit selector 没有合法 finite CONFIG，双方均不可行；`T>=2` 不作保持声明。结论保持的是有限有理证书可行性、原 moments 和 typed localizer，不是 integer perfect completeness、完整 schedule law、OPT 值或一般 unrelated-machines 近二结果。

# 7. 来源判断与处置

canonical §12 明确不主张 path 思想新颖性；本轮不把其引用的 STOC’09 Theorem 3 当作 degree-four certificate preservation 的现成证明。它也没有运行 checker、SDP finder、数值实验或软件实现，global novelty 与 `UM-TARGET-v1` 仍未认证。结论为：在上述 raw K2 有限有理合同内，§12/12.1--12.7 与已审四源同对象、同量词、同次数预算，未发现足以推翻的 fatal；审查 PASS 只限该范围，旧 prefix 和 native C2/primitive-SA1/M1 不在签字范围。

本对象与 `flat单位资源路径K2证书合同四源清洗--审查.md` 是增量关系：前者记录四源主证明，本文只记录 canonical §12 的 informed read-after、次数账本与 zero/inactive 计数补强。后续映射可建立“canonical append 复核 -> K2 证书合同”边，不得把它合并为一般调度等价。
