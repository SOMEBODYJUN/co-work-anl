# R-171 credible continuation 五源比较记录

## 来源、哈希与处置

| ID | 文件 | 大小 / SHA-256 | 处置 | 实际运行或读取 |
|---|---|---:|---|---|
| `f9e2f6cfcb88db161bc1` | continuation/credible/README.md | 2095 B / `17dacad4de0cb2f6e058163c5cc09e355a70ad60d630fb923990f3820ad6006b` | integrated | 完整实读；核已知低根种子、默认 8 步范围和“无一般结论”边界 |
| `cc2b103c4eac0db152c4` | continuation/credible/low_root_discovery.py | 4767 B / `7f749456b5a6dd3b53152161996db4251c8b06d286580f2f5f8e291b97e6cde3` | integrated | 冻结依赖下 `--steps 1 --seed 319221`；21 endpoints，W=OPT=43，ratio=1 |
| `4b7ae57ed9a151791e7f` | credible/count_milp.py | 4932 B / `524ab41949a978705df1994dc155280e030bb9b3a17acc8ffe02badfdb172c42` | integrated | p=2 小重放 optimal；15 vars/6 binary/38 constraints，exact ratio=3/2 |
| `02e6f3a21754aed40129` | credible/finite_attempt_summary.json | 53907 B / `38bbf08c7588ebe323bac3466ce3a5aed0a97aabe92b843a48bfc722966dc098` | retained | 全部 JSON 结构/94 walk records/4 MILP records 已解析 |
| `bce1cf4e732bc5d5309f` | credible/minimum_root.py | 2925 B / `8aa093cb8d7f37b639c78e0ce466d4e24ba9f3495d0abb62dd44eae570f5c3a4` | integrated | 固定脚本完整 12 步；根份额 916/5449 后稳定 1/6，每步 W=OPT |

原文统一保存于 `original/`；重放和输出分别保存于 `replay/low-root-step1/`、`replay/count-milp-small/`、`replay/minimum-root/`。

## 数学对象与策略量词

### A. 低根可信锥

低根种子是 p=7,m=5 的 43 客户实例，根计数 `(1,1,1,0,0,1,1)`、根 payoff 5、W=OPT=43。`low_root_discovery.py` 只在通过 `ExactSPESolver` 的真实终局菜单中选完整有序策略，并追加首根约束 `u1/W<=5/43`；LP 是候选生成器，随后有理恢复、整数克隆、规范证书和独立全历史检查才算 accepted endpoint。

本轮一步 replay 接受 21 个端点，ratio 仍为 1。README 记录的默认 8 步/168 endpoints 与此不同参数范围；不能把一步重放说成完整默认运行。

### B. 计数 Markov MILP

`count_milp.py` 把历史压成计数状态，MILP 变量为状态/动作连续 payoff 与 binary action choice，再把单一 count policy 展开至全部有序历史做 exact verification。p=7 的三组摘要分别 timeout、infeasible、timeout；p=2 小例 exact 结果 W=2、OPT=3、ratio=3/2。计数共享是候选子类约束，不能推出所有完整 SPE 的 bound。

### C. 最小根 credible cone

`minimum_root.py` 固定 p=7,m=5、目标 `(0,0,0,1,1,1,2)` 和 seed 128420，在每个 credible cone 中最小化第一动作 payoff。12 步均有 exact accepted endpoint；首步 `916/5449`，后 11 步 `1/6`，W=OPT 分别 27245 与 6。该序列不是所有策略锥的全局最小值。

### D. 冻结有限摘要

`finite_attempt_summary.json` 的根 scope 已明确“finite sampled complete-history credible policy cones; no universal bound or target counterexample”。三组 walk 共 94 endpoints，最高 OPT/W=171/100；四组 MILP 含三组 p=7 未获 primal（两 timeout、一 infeasible）和一组 p=2 exact ratio=3/2。摘要没有任何 ratio>2 记录。

## 与近期 R-171 / customer-attraction 对象的比较

- 与 `R-171接续工作区主张边界与开放义务--审查`：同样把 credible、稀疏租金、遗漏和早期激励拆成不同义务；本批没有把低根候选转成共同根支付。
- 与 R-171 coupling 的稀疏槽 clock/skip-premium：低根/credible 搜索只生成策略锥端点，不支付连续窗口条件下的 ghost rent，也不消除 skip-premium。
- 与 dynamic-credit 一步 LP：本批优化的是完整策略锥或 count-Markov 候选，不是局部 coverage/profit 投影；任何 `OPT/W` 比率都不能与动态一步 gap 拼接。
- 与已有 credible strategy-cone 审计：本批沿用“固定策略锥 + exact primal acceptance + ordered-history verifier”的证据层级；count-Markov MILP 另外保留计数共享限制。

## 结论边界

五源共同支持的是有限候选探索、精确端点验收、MILP 状态分层和低根搜索边界。它们没有证明：

1. 任意人数/目录/完整 SPE 的 `2W>=OPT`；
2. 低根实例存在或不存在的全局定理；
3. count-Markov MILP 的全历史复杂度、算法或 hardness；
4. 任何 `OPT/W>2` 的完整策略反例；
5. unrelated-machines 的可迁移结论。

处置分开为 README/脚本 integrated、摘要 JSON retained；不把 timeout、infeasible、有限阴性或固定比率当数学反例。
