# round3_general / residual：同一 fresh 剩余容量

2026-10-24。范围固定为任意有限单位客户、共同有限目录、任意人数、全部有序历史纯 SPE。**Q-CAG-HALF、原 full-SAFE 限定 RESIDUAL-CAP 和扩展 FRESH-RESIDUAL 都仍 OPEN；本轮没有新全输入福利界，也没有真正残余容量反例。**

## 文件与实际结果

- [ell_merge_working.md](ell_merge_working.md)：本分支的共同 reset 列、真 ell 加权关系、固定 ν 下重复退款的失败步骤，以及比较全部源主题时仍未付的二次偏离叶。它是未完成推导。
- [offhistory/common_reset_ell_working.md](offhistory/common_reset_ell_working.md)：子分支独立推导同 reset 的精确 fresh 密度和 ell 组内位置；两份推导已对照一致。没有证明共同 Σβ 或 actual 钱包 cap。
- [offhistory/positive_fresh_candidate.json](offhistory/positive_fresh_candidate.json)：一份真实完整 SPE，存在正 fresh reset 边；只作自然 ν 核的非零域种子。
- [offhistory/positive_fresh_audit.json](offhistory/positive_fresh_audit.json) 与 [audit_positive_fresh.py](offhistory/audit_positive_fresh.py)：定义级精确回放全部156个历史、780项IC及OPT；root residual再次运行通过。该例的R-only极大current对全部最优T匹配都没有future源，故不是目标初始化的正传播例，更不是FR?反例。

## 未闭合处

对同一角色 k、同一 prescribed 动作 a，全部旧历史 reset 到同一个 A。fresh 输出列密度为

    Λ_(j,x)=Σ_t β_t 1_(x∈A_j\V_(t,j))/c_(V_t)(x)。

离轨返回实际主题的真 IC 只给

    Σ_tβ_tw_t=Σ_th_t+Σ_tβ_tX_t−Σ_tβ_tell_t，

其中 w_t 是不同旧历史的真实返回叶上 C 利润。没有将这些互斥 w_t 共同支付到一份 actual 剩余钱包。保持同ν/P/流时额外扣ell会破坏守恒；改图必须重算，不能混入原限定路由量词。

全部其它源主题的完整IC可以看见 fresh 竞争，但产生带旧首偏离和新查询的二次偏离叶；其共同请求仍未支付。本次没有成熟付款结果可提交独立定理审核。下一步应直接处理这条真实共同付款，不扩张任意外生注入的局部密度专项。

本分支只修改本目录，无git/work.py或共享文件操作。计算仅用于检验明确一般候选，不以固定规模正面结果或有限阴性作结论。
