---
id: unrelated-machines/flat-unit-resource-path-k2-contract
kind: review
type_tag: 审查
title: flat 单位资源路径 K2 证书合同四源清洗
status: integrated-source-cleaning
truth_status: restricted-certificate-equivalence
review_level: full-source-read-independent-exact-first-plus-author-proof
summary: "四份冻结来源共同给出 D_+ 单位资源路径变换在明示 degree-four K2 合同下的双向有限证书变换；结论只适用于完整 ordinary jobs、全局 M2、真实 CONFIG 一二阶边际及可选 affine load localizer 的 typed 合同。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/sol_flat_unit_resource_path_c2_exact.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/sol_flat_unit_resource_path_c2_independent_exact_first.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/sol_flat_unit_resource_path_c2_proof.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/sol_flat_unit_resource_path_c2_author_read_after.md"
source_ids:
  - "4a4ac300f175b4b06b39"
  - "a408d59fdcb0c413a6bc"
  - "b944cc8a64e07c6303df"
  - "cd36f07696f54f46bfee"
source_sha256:
  - "c2c590f3e916d992e6d591e25ccad0f1c8818586ed8a2b4d0a8fd5a2ab1be0d9"
  - "6e24cdb2b7dcdcfa98f482e371604728b7994c0cc4da70fa601474fd6c3e8639"
  - "09d9e2b1d3373d2e17f01fb764fab339bd869da7acfbf9479e8eb90225fdde7e"
  - "6ec5c4ad908f137402034d723baaebc0eda12ab42fb76828496ea13a4a96e091"
source_blobs:
  - "2be68194164adc21786985679ce19028071be69b"
  - "10753e50c1ec784f7a6f24b8658fa8ca1bc700a1"
  - "dc197a458404be763895f9f267049239460a1592"
  - "512d0551f5aafdb3e99d15b55c1e31279f1acbf1"
source_commits:
  - "68fad804ec5946cb296f77dc5b336308a66abf12"
  - "aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c"
evidence_manifest: ../../tools/evidence/sol-flat-unit-resource-path-k2-20261031/source-manifest.json
related_objects:
  - "../定理/完整菜单的资源度三路径归约--定理.md"
  - "./归一化菜单福利与配置证书双源审查--审查.md"
---

# 1. 来源身份与实际阅读

本批四份来源均从冻结提交以 `clean show` 导出并逐字节核对 SHA-256。`4a4ac300f175b4b06b39` 是 3008 字节 Exact；`a408d59fdcb0c413a6bc` 是 15504 字节 independent Exact-first；`b944cc8a64e07c6303df` 是 14827 字节作者 Proof；`cd36f07696f54f46bfee` 是 13942 字节作者 read-after。两冻结提交 `68fad804ec5946cb296f77dc5b336308a66abf12`（legacy-cleanup）和 `aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c`（main）内容一致；导出字节及清单见 `archives/unrelated-machines/tools/evidence/sol-flat-unit-resource-path-k2-20261031/`。

阅读顺序保留来源自己的版本边界：independent Exact-first 只以 Exact 和已明确给出的 D_+ 定义重构，之后才读作者 Proof；read-after 是在独立重构之后的作者二次审查。作者自述曾与其他内部工作讨论，因此这不是外部盲审或新颖性认证。

# 2. K2 合同和精确量词

输入是完整显式 normalized-flat ordinary (P(Q))：所有 indexed states、selectors、每个 incidence job、正/零 incidence、未选状态的 jobs 和 unused resources 都保留。对每个旧单位资源，按 distinct positive-neighbor groups 排序；D_+ 将组的所有原 incidence（包括零 incidence 和未选状态导出）路由到该组的一个 port，组没有正邻居的零 incidence 使用该资源固定 fallback port，(d=0) 旧资源保留。相邻 ports 之间加入两根 private、两状态、单位 selector/单位 incidence 的 path leaf；新旧物理标签不合并。

固定有理 (1le T<2)。K2 证书是有限有理 machine-CONFIG 列表（每机配置权和为1，负载至多 (T)），与一个全局有理 Boolean degree-(le4) moment functional (L) 共享每个 job 的一阶和同机二阶 membership；(L) 满足所有 Boolean 与 exact one-hot 恒等式直到四次，并对所有全局 degree-(le2) 多项式平方满足 M2 PSD。合同还可要求每一台物理机及全局 affine (q) 的

[
L((T-\operatorname{load}_i)q^2)\ge0 .
]

若两侧同时启用或同时省略这项 affine load localizer，结论相同。四源的精确主张是：对每个 (Q,T)，K2((P(Q),T)) 可行当且仅当 K2((P(D_+(Q)),T)) 可行；给定任一侧的完整有限有理证书，可在显式输入和证书长度的总位长多项式时间内构造另一侧证书。这是证书转换，不是求解器、调度算法或任意更强 C2 层级的等价。

# 3. 共同承重引理：单位端点的二阶根与派生 hole

因为 (T<2)，一个只含单位作业的合法 CONFIG 至多放一件作业。因此同一物理单位机上不同 endpoint indicators (x,y) 的二阶边际为 (L(xy)=0)。Boolean 恒等式给 (L((xy)^2)=0)，再由 M2 PSD 的 Cauchy--Schwarz，(xy) 对所有允许的二次 multiplier 都是 null。任意这类端点和的 (S) 满足 (S^2-S=0)（在四次合同内），并且派生 affine Boolean 乘积满足

[
L(hk)=L((hk)^2)\ge0 .
]

这一步只用明示的同机 pair 边际和全局 M2，不偷加任意 quartic literal positivity，也不假定存在完整联合调度分布。

# 4. 正向证书变换

对旧资源的所有原端点按 D_+ port 分组为 (O_1,\ldots,O_d)，包括正、零、inactive-state exports。令 (K=\sum_iO_i)，(Q=1-K)，选固定 hole port (f)，令 (H_i=O_i+\mathbf1[i=f]Q)。这些是由旧 unit pair-null 关系支持的互斥 affine holes，\(\sum H_i=1\)。路径叶 (j) 的两个 selector 和两个 unit incidence endpoint 取

[
L_j=\sum_{i>j}H_i,\qquad R_j=1-L_j .
]

新变量均为旧 indicator 的 affine 替换，pullback 保持 degree-(le4) moments、Boolean/one-hot identities 和 M2。port occupancy 满足

[
P_1=K,
\quad P_i=1\ (1<i<d),
\quad P_d=1,
]

（(d=1) 时只有 (P_1=K)）。由派生 affine Boolean 与 M2，任一 port 上不同 unit jobs 的 pair moment 为零；用各 singleton 一阶权及 empty residual 重建合法 CONFIG。新 leaf private root 的 selector 与 private incidence 互补、负载恒为1；旧 private-root CONFIG、零作业身份和所有旧 moments 原样保留。若合同含 affine load localizer，旧 private roots pullback，新 leaf/root 与满载 ports 用恒负载，hole port 用旧资源 localizer；故正向仍成立。

这是一个对全局单一 (L) 的扩展，而不是把每个 port 的局部证书事后拼接。所有原作业（含未选状态和 zero）都留在 functional 中。

# 5. 逆向投影和额外导出

从任意目标证书出发，不能假定新 leaf 遵循正向 canonical assignment。对叶 selector (a,b) 与 incidence port indicators (x,y)，private endpoint 冲突给 (a(1-x)=0)、(b(1-y)=0)。利用 (a+b=1)，(q=(1-x)(1-y)) 是 null；因此 extra-export (e=x+y-1) 是 degree-four affine Boolean。对每个旧 port 的 unit job sum 定义 hole (H_r=1-\sum(\text{port jobs}))。精确计数恒等式为

[
N_{\rm old}+\sum_rH_r+\sum_{j=1}^{d-1}e_j=1 .
]

其中 (N_{\rm old}) 包含所有原 routed exports，零和 inactive-state 不能删掉。上述各项的一阶和及两两乘积非负；乘恒等式以一个 summand，并用其 Boolean 性，得到不同原 exports 之间 pair moment 全为零，包括不同 ports 的 pair。于是可在旧 resource 上用每个原 endpoint 一阶权加 empty residual 重建 singleton/empty CONFIG，且保留所有原 moments。旧 private-root lists 原样复制；旧 affine load localizers 由 restriction 继承，单位资源 localizer 可由

[
L((T-N)q^2)=(T-1)L(q^2)+L(((1-N)q)^2)\ge0
]

得到。(d=0) 保留旧资源，(d=1) 直接由同机 unit pair exclusion 处理。

作者 Proof 还给出 selector-difference 路线：令边界 (L_0=1,L_d=0)，内部 (N_i=L_i(1-L_{i-1})) 为 null，(H_i=L_{i-1}-L_i)，由 (H_i^2-H_i=2N_i) 与 M2 先证 (H_iH_j) null，再证每个旧 export 只能落在对应 hole，最后得到跨 port old pair exclusion。这与 independent Exact-first 的 empty/extra conservation 路线是两种相容的代数证明，不是两个独立全局概率法则。

# 6. 位复杂度、参数和证据边界

每个旧资源新增 (d-1) 叶，且 (sum d) 不超过显式正 incidence 数；新变量是固定次数 affine 整数和，四次 moments 展开以及 singleton/empty 权重的有理编码长度相对 supplied certificate 多项式。该结论依赖“完整有限有理证书作为输入”，不声称对任意最短 CONFIG 证书、精确 SDP oracle 或搜索过程给出统一复杂度。

(T<2) 是 unit pair exclusion 和 leaf-root 冲突的关键；(T<1) 两侧均因原 unit selector 无合法配置而不可行；(T\ge2) 不作保持声明。零一阶权、空资源、重复 indexed states、多个原 states 共享一个 port、原 inactive exports 均在量词内。合同保持的是证书可行性与原 moments，不是 integer perfect completeness、完整 schedule law 或 OPT 值。

# 7. 与既有对象的关系和处置

`归一化菜单福利与配置证书双源审查--审查.md` 已经记录相邻的 FSLP/CONFIG、菜单树正规形以及同类 raw K2 路径合同；本页新增四份具体 source provenance、D_+ 定义下的完整零/inactive routing 量词、independent-first 与 author read-after 的版本关系，以及 selector-difference/extra-export 两条逆向证明路线。`完整菜单的资源度三路径归约--定理.md` 是 ordinary menu/path 的实际值与度约束对象，不能替代本页的全局 degree-four K2 证书合同。

四源处置如下：

- `4a4ac300f175b4b06b39`：`retained-candidate-exact-contract`；给出精确对象和双向量词，未含作者证明。
- `a408d59fdcb0c413a6bc`：`integrated-independent-exact-first`；冻结于 Proof 之前，独立重构无 fatal，但不等外部审查。
- `b944cc8a64e07c6303df`：`integrated-author-proof`；给出正向 hole、逆向 extra-export、localizer 和位长推导，范围止于明示 K2。
- `cd36f07696f54f46bfee`：`integrated-author-read-after`；逐段复核作者 Proof 与 independent-first 的兼容性，未扩大到弱 C2 或一般 UM。

这些来源支持受限 K2 证书合同的后续引用；不支持一般 unrelated-machines 近二算法、NP-hardness、全局联合配置法则或运筹清晰六人 SPE half 覆盖结论。第三阶段可把本页与已有资源路径定理建立“证书合同增量”关系，但不能把它们合并为一般调度等价。
