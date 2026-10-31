# 最终新增 §13 实读范围与后置攻击 v2

Reviewer：/root/sol_general_repair，2026-10-18。

## 冻结对象与真实阅读

最终草稿为 diluted_shared_terminal_raw_k2_with_row_degree_final_v1.md，SHA256 fb705e62ae3344a24c95ca962d4fa2cfd83dbc57422eb59fd6285713e29a121b；已实际计算为 33439 bytes、440 行。**只完整实读第246–440行的新增 §13**，约3585 tokens，未读本最终文件的旧前245行正文。

实际按原字节截取首245行，长度19100 bytes，SHA256 7128241668e8f7b5abe014775f9d0d3b4f59a5bfecbb2f1aef8e357272bb01b4，与 root 给的旧前缀身份相同。这个 byte/hash check 不认证旧正文或把新增审查回填旧 Claim。

已先行实际全文读取新 Exact e23ae495b4a997f081e0de06323e5dd9563c98d3828b78804ddc7670b16c9f6a，冻结独立重构4294c156fa6feb502b6c3e90bec6c0bd8fb9e8e5ecc4008c2cf9b71838cf3447；root释放后全文读作者Proof7fb8ae7e6635853417963a5ff379406cbc3a0abf347a73015ebc79c1a207c407，另冻读后c3ac3d56ef9ae27b1b4041adf7b8bb91b78c63b303f7fc27d3a70757672081d6。此次是最终正文读后，不是新 blind 票。

## 数学范围：无新增 fatal

1. 正式新 ID UM-DILUTED-SHARED-TERMINAL-ROW-DEGREE-GAP-v1 的参数与旧 v1 明确分开。d≥2 固定、k≥d、D=max(4,d)，M含新subset吸收项；生成时间和总位长的多项式次数可依 d，不把 binary d 当 variable 输入统一 polynomial。
2. 原机器、全部原 jobs、所有有限端点表与计数自足。实际 OPT=2−floor(sqrt(k))/k 的完整上下界涉及所有 assignments；未用样本 law 或 source oracle，未漏 inactive components。
3. common F 的全原 job identities、global M2、每行全部degree≤d endpoint moments与每台机器全部原 global affine q localizers被清楚分开。没有 joint CONFIG selector M2、higher q/event localizer 或 inactive-home 假设。
4. 逐具体subset的 finite-difference trade 包含 mixed unit+homes、pure-home degree d、重复因子、多个unit零矩；unit/no-unit correction同 S 抵消，foreground没有双加。背景吸收常数和全 row list 合法性与已审作者证明一致。
5. coefficient-norm支配的12kL+12Lk³+6kL(k−1)²≤30Lk³、old-half正slack、H positive mean及全component conditional variance付款在正文均完整。allcontexts没有退化为只看本component或只测endpoint diagonal。
6. explicit finite-law moment generation、partial injections/permutations、不可容纳先置零和fixed-D bit成本与已审证明相同。dense input规模也为fixed d多项式；不是借小support枚举掩盖全局指数 law。
7. 缩放后target一且真实OPT趋二，CONFIG-first/ST上界二给 sharp supremum。没有计算hardness、general算法或generic SDP finder结论。
8. 跨行AiRj event负式已经degree≤3；next mixed d+1 的a/L只属指定真实finite law自然延伸。当d+1>D，不声称已有degree-D restriction无其他extension。这一重要限制正文明确保留，不能从任意阶global PSD自然延伸反推更高阶load/SOS通过。

## 软件与来源的认证限度

最终正文记载新四例行trade audit仅覆盖(d,k)=(2,2),(3,3),(4,4),(4,7)，分别11、42、163、1471个squarefree行单项式，并明确未枚举global M2/localizers、未认证一般d。此范围叙述没有与数学定理混用；旧k=2 first/pair的50维audit未升级为新证据。

**本人没有打开或运行 enhanced audit代码、作者JSON、旧代码，也未读取root replay scope。** 因此代码SHA acee8c713dc7886dd03405031f8dd1d71c7ac67c7274a1fadc5fa715e36f8cc8、JSON SHA416d764ad20172efde6e845efab8c33f176bd45f34ba50d29acb88dfb0bf9841、有限数量和byte-identical CLI等均只属于正文对作者/root的归属说明，不是本审者复验。

在冻结v1后、冻结本v2前，root已回报亲自完成规范CLI：tests/audits/unrelated_machines/diluted_shared_terminal_row_degree_trade_audit.py（acee8c…原字节）以--output写入全新目录row_trade_four_cases.json；四例passed，输出与作者JSON逐字相同，SHA256为416d764ad20172efde6e845efab8c33f176bd45f34ba50d29acb88dfb0bf9841。root将完整argv/cwd/范围冻结于/workspace/scratch/038d9dcc4cac/boss11_diluted_row_degree_trade_root_replay_scope.json。因此正文的完成时态已有root实际完成回报对应；本人未打开该scope、代码或输出，仍不把它登记成自己的独立软件复验。v1保留其冻结时的未来状态，不回写历史。

**最终结论：新增§13的数学合同/证明/范围无standing fatal；只按新增195行给最终读后。** 原前缀仅hash，软件未读跑，外审、全球新颖性、joint-CONFIG/higher-event合同及一般UM目标都不认证。
