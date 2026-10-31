# 自然 incoming 密度账的独立审查

2026-10-24，dynamic。审查对象：[rank 原稿](../rank/incoming_density_diagonal_ledger.md)。**结论：解析恒等式、全部父子守恒以及所用 IC 的适用域通过独立重构；无总费用上界，也未证明 half。**

审查过程先仅按 root 给出的精确陈述重构，在阅读原稿前保存[盲重构冻结稿](review_density_ledger_blind.md)，随后才阅读作者全文逐项核对。这里的“盲”只指首次重构未读作者证明，不表示未收到公式陈述。作者第1节已明确限定 R 客户与原自然 fairshare 流，符合本次审查所需承重条件。

## 1. 局部式与符号

对父来源 g，A 为 reset 后 actual-prefix query 叶、B 为父查询叶、W 为父自然 j 节点改选 actual S_j 的真实叶。完整行动 a 上的测度 μ_A(x)=(1/c_A(x))/D 必须包含全部 a 客户，f_g 在非 tracked 客户上补零。写 J_g=Σ_x f_g(x)/c_B(x)，则

    D Cov_(μ_A)(f_g,c_A/c_B)=J_g−θ_g v_j(B)。

所以

    θ_g u_j=J_g+θ_g[u_j−v_j(W)]
                 −D Cov_(μ_A)(f_g,c_A/c_B)−θ_g ell_g。

作者 COV 的负号正确；ell_g=v_j(B)−v_j(W) 的有利负号正确。全行动归一化不可偷换为 tracked 子集归一化。D=0 时 a_g=0，省略该 g 合法；对有正 a_g 的 g，D>0，且 B 的 j 行动包含 a，故 c_B 在测度全域均正。

## 2. 全父子共同首项

每父 q 的每客户 x 发向恰 c_q(x)−1 位真实未来 coverer，每位收到 f_q(x)/c_q(x)，且每条边以父叶 B=q 的 c_q 作 diagonal 分母。因此全部父子来源恰贡献

    Σ_g J_g=Σ_(q,x)(c_q−1)f_q/c_q²=M−H。

初始证明使用原实际完全遗漏 R 与向全部真实 future coverer 均分的 fairshare 流。作者新增第6节后，第二个条件已放宽为固定总 captured mass、出口仍进入自然规定行动；补充证明与独审见第5节。任意 owner-return、改变当前吸收的 priority 路由或 I-query，仍不能未经重证搬用该计数。

同一 child query 可有多父来源：incoming 吸收分子与 θ 对来源线性，故先按 g 分拆再合并仍是同一份 query whole-IC 系数。涉及 B 的 covariance 必须保留父来源标签；原稿已经这样做，没有将互斥父叶利润视为同一实际钱包。

## 3. IC 合法性与准确强度

j 严格位于父查询角色之后，父强制行动以后都沿原 sigma，所以在 B 的自然 j 历史中，a=B_j 确为原规定行动；W 是该历史中选择合法 actual S_j 后沿原 sigma 的完整叶。这证明 ell_g>=0。θ_g 是固定非负常数，故 L 是完整真实后继 IC 的合法非负加权和，而非客户级 IC。

原 actual-prefix query IC 给 D<=u_j，但不比较不同前缀的 u_j 与 v_j(W)。因此 T 仍有符号；COV 也没有固定符号。H>=0、L>=0 不足以推出 K_in 已付，GLOBAL-SLACK 也没有提供 T+COV−L 的新上界。原稿对该边界的声明准确。

## 4. 独立精确回归

[独立脚本](audit_density_ledger_independent.py)不导入作者程序或规范求解器，仅重放三个已有完整策略，展开单位客户，用 Fraction 先核全部原始 IC，再取一份字典序最优主题元组，对全部遗漏客户注入 rho=1，逐父来源核 covariance、LOCAL、tracked diagonal、ABS、M−H、GLOBAL-IN 和 GLOBAL-SLACK。[冻结输出](density_ledger_independent_audit.json)通过：

| 既有完整策略 | 原 IC 比较 | reached query | 非零 incoming context |
| --- | ---: | ---: | ---: |
| root_tax_failure | 1554 | 3 | 0 |
| individual_security_failure | 258 | 2 | 0 |
| portfolio_matching_failure | 30 | 3 | 1 |

前两份没有 incoming，只核空项边界；不能宣称它们经验验证了非零局部式。第三份有真正非零 covariance、actual-return 及 offhistory slack：

    M=42，H=163/4，ΣJ=5/4，K_in=5/2，
    T=5/88，COV=5/4，L=5/88。

故 K_in=(M−H)+T+COV−L 精确成立，且 covariance 确有正费用。这里 rho=1 只验证作者明确允许的任意固定残源版本；它不是同一实例的最优 Hall 取消试验，也不否定共同选取消后可能出现的有利上界。

普遍正确性由第1—3节的解析重构承担；有限回归仅校对定义与实现，没有新游戏、策略扫描或一般福利证据。

## 5. 作者新增第6—7节的范围补充

上述第1—4节首先审查了作者初始第1—5节、原等份自然 fairshare 流。随后作者证明只固定当前吸收与总 captured mass 即可任意分配自然 recipient；其[补充独审](review_density_ledger_supplement.md)已通过。第2节现已据此标明较宽条件；[盲重构冻结稿](review_density_ledger_blind.md)保留最初只核等份版本的过程记录。自由 TOTAL-TRIM 的合法性亦通过，SOURCE-NET 不随任意删源继承；未证明总费用界。
