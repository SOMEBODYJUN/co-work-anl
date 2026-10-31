---
source_id: "f00e3e92df90c1dab67c"
source_path: "history/source/notes/unrelated_machines/sol_general_repair_shared_ud_tiny_state_potential_author_self_audit_v1.md"
source_sha256: "ad50e4e7376ceb50c08e86a75eaa94800f78c9262f8438a130ea89224a0bd9c9"
source_size_bytes: 6223
kind: "author-self-audit"
status: "integrated-candidate; not-independent-review"
disposition: "integrated"
related_sources:
  - "22eb4747b3c8214c2765:sol_general_repair_shared_ud_tiny_state_potential_19_10_exact_v1.md"
  - "e2370ab75fef1534990c:sol_general_repair_shared_ud_tiny_state_potential_19_10_author_proof_v1.md"
---

# 来源角色与读取范围

该冻结源是作者在完整读取同题 Exact v1 与 Proof v1 后写出的后置自核，明确声明“不是独立审票”，也没有打开 fresh reviewer 的独立稿。它不能被计作第三份独立证明。作者实读的关联源为：Exact v1（3867 bytes，SHA-256 80fd4ff5b6aab2993e42b995ea369e9441543e754cf3642800c84a784c63cf1d）和 Proof v1（13302 bytes，SHA-256 409ce88433cd698d477862098023f7e064dbe7a75426117f3c617e70aad7f435）。本源没有改变 canonical 的 k^4 tiny / 19-10 审查身份。

## 1. 交换耦合的承重内容

对固定 λ>0、profile S 及其中任意 λ-optimal fractional utility W，叶匹配 vacancy matroid 是满秩 transversal matroid 的对偶；helper-incidence copies 与零 dummy 只是该 matroid 的 parallel extension，loops、rank-0 和空 B 不改变定义。作者把 Proof §4 的单元素敏感性改写为 symmetric basis exchange：删除最大权 basis 中的元素 e，和删除后最优 basis 做一次交换即可保持最优；插入一元素同理。dummy copies 使删除 helper candidate 不降低 rank。

删旧 helper 的 copies 后其他 helper 的 weighted utility 总增量 G 不超过旧 owner utility A；加入新 copies 后其他 helper 的总损失 L 不超过新 owner utility B。即使同一 outer 有其他 helper，owner 坐标仍落在 [-A,B]，其余坐标落在 [-B,A]，跨 outer 的 L1 变化不超过 A+B+|A-B|=2 max(A,B)。这说明叶 matching 可以整体改变，证明并不假设只改一条匹配边；它同时给出所需的 Linf 与 L1 控制。

作者只在证明中对固定 profile 的 integral network optimal face 使用凸分解；每个分量都保持 λ-optimal，helper claims 可用零 dummy 补成 basis，逐分量耦合后取平均。算法本身不把该分解当作 oracle。

## 2. 势近似与有理位复杂度

精确 P(S) 只作为数学比较使用。QP 改写的严格凸性作用于 deficits，足以推出 P(S)-Phi(What) >= ||d(What)-d*||^2；不要求 W* 唯一。固定 profile 的资源分配后端可写成：先按 helper candidates 的最大权 a_u 建边代价，求最小费用完整叶 matching；未被叶使用的资源交给 argmax helper 或零 dummy。它不枚举 joint helper profiles。

Frank-Wolfe 取 gamma_t=2/(t+2)。从 t=0 开始，第 t>=1 个 iterate 的 vertex 权重为 2(r+1)/(t(t+1))，r=0,...,t-1。输入有理 payoff 的一个公共分母 D1 控制迭代分母，故 W 的分母可取 D1 t(t+1)，不发生逐迭代分母倍增；gradient 与 matching costs 的乘积只增加多项式位长。固定次数 ceil(4k/xi)、固定初始 matching 和 tie rule 给出确定的 What。

作者给出 Phi 的梯度 Lipschitz 常数 2、域直径平方不超过 k，初始 gap 不超过 2k，与 4k/(t+2) 的收敛界相容。该段是证明/复杂度边界，不是软件执行记录。

## 3. 常数与 sound FAIL 的语义

作者自核用 Fraction 重算了常数：epsilon²=225/256；k>=2 的 profile-gain 下界在 Dsum=9/80 为 293/81920，k=1 单独分支为 177/8192=885/40960，prefix-flow 后下界为 799/4096。若近似 What 某坐标小于 25/128，deficit 稳定性使精确 P 的最优 deficit sum 大于 9/80。在反证中，真实 V>=15/16 只用于取得一个共同真实 target profile O；submodular exchange 与曲率界强制某个可枚举 helper 替换使 P 增加至少 rho/H，大于近似误差 xi，所以无增益才 sound 地推出 actual V<15/16。

因此 FAIL 证明的是实际 V<15/16，不是某个必要 LP 点失败，也不是 LP 不可行即 actual infeasible。实际 V<15/16 时仍可成功或继续；势有界且每次近似 P 增加 tau，保证输入多项式步数停止。初始叶图没有完整 matching 时，exact threshold-UD iff 直接给出 V<15/16。

## 4. 有限自审运行及边界

作者新增并实际执行 sol_general_repair_shared_ud_potential_exchange_small_network_audit_v1.py，直接枚举原资源 helper ownership 与剩余叶 matching，不调用 matroid exchange 算法或 Proof 的 coupling 构造。240 个小例均通过，共 26,674 个可行原资源 ownership、242 个全部旧最优 outer-vectors；所审资源数 4/5、helpers 3、叶数 1/2，含 160 个异质 lambda 和 160 个变更 helper 仍有同 outer 其他 helper 的情形。全部使用 Fraction，stdout 冻结为对应 _run_v1.json。

该运行只测试有限 integral exchange coupling，且不满足新 Exact 的 tiny 限制；它没有执行完整 Phi/Frank-Wolfe/profile 搜索、tiny 输入、prefix-flow 或全部 unrelated-machines jobs。因此不能写成端到端软件认证、一般 UM 算法验证或独立审查。

## 5. 与现有对象的关系与处置

本源应并入现有 shared-UD tiny-home / 19-10 版本审查链，和 sol_general_repair_shared_ud_tiny_state_potential_19_10_exact_v1、author_proof_v1 保持不同 source identity；它补的是作者对 exchange、位复杂度、常数和 FAIL 语义的自核，不是新 theorem。现有 Boss11共享UD叶tiny-home-k二次扩域三源审查--审查.md 及其 evidence manifest 承接 k² v3/v4 结构；本源不自动把旧 k⁴ 对象升级到 k²/v4，也不扩展到一般 UM-TARGET-v1。

建议正式去向：新增一个版本来源审查对象或追加至对应 shared-UD review；evidence 目录保存本源原字节、关联 Exact/Proof SHA，以及 _run_v1.json（若可定位）。第三阶段关系只可标为“作者自审→既有证明版本”，不能标作独立证明或外部审稿。
