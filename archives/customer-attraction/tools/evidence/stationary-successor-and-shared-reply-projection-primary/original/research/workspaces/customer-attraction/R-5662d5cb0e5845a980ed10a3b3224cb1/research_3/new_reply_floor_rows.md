# 实际全前缀对新索引回复的安全查询

状态：解析合法新增行；在指定旧16直方图支撑必要图上给出精确新停止点。没有六人完整 SPE，也没有全域 half 结论或新的福利因子。

## 同一原策略与新增三十六行

沿 research_5/README.md 的准确标签：R_(0,i,j) 是历史 (A1,A2,A3,T_i,B_j) 后的真末回复，i!=j；R_(1,i,j) 是同一历史把 B_j 换成 C_j 的真末回复，全部 i,j。Z_e 是实际四前缀后强制第五位选 R_e 所得真末回复。它们全属于同一原完整历史 SPE 的共同目录。

把 e 分成 (f,diag)=(0,0),(1,0),(1,1) 三类，每类边数 n_e 分别为 30、30、6。任选 member=R 或 Z，并记 Q_e 是该类对应的回复主题。对每个实际源位置 k=0,...,5，真实实际前缀旧负载 p_k、剩余含当前人数 6-k，得到

    n_e u_k - sum_e sum_(x in Q_e) 1/[p_k(x)+6-k] >= 0.        (FLOOR)

证明对每个合法 Q_e 在实际源强制选择它，再沿原策略真实执行：该偏离者每名所选客户至少取得分母 p_k+6-k 的份额；对各真实源 IC 求和即可。没有冻结偏离后的后继，也没有将被强制者认作新分支的最优者。k=5 是真实实际末价端点。

同一 (f,diag,wi,wj) 组的边数是：diag 时 hist[wi]（wi=wj）；offdiag 时 hist[wi]hist[wj]−1_(wi=wj)hist[wi]。因此 (FLOOR) 在旧 joint-reply 状态 (r,z) 上仿射：hist 基系数 n_e e_k/c，新状态列增量为

    - multiplicity * state[member] / [sum_(l<k)e_l+6-k].

实现 all_reply_actual_floors.py 直接保留原 1905 列，未固定 R/R 或 Z/Z 联合分布。added_rows(cols) 可供其他联合图复用。

## 精确分离及停止点

在 research_5 的 cross_source_priced_optimum_exact.json 点上，四条新早源 R 行严格负。最小是 (k=2,member=R,f=0,diag=0)：

    -4749850661723892253166888285611 / 107365313311072858536618851786648.

它只说明该旧必要点违反原游戏的一项真实查询关系。

将全部36行与旧4927行（含旧 B_i/C_i 全实际源floor、容量、priced及OPT单换）共同重优化，仍有精确可行点：

    O=1,
    W=348849746216199535907980629211183 / 729080852958937593380920238282304
      ≈0.47847882001071673 < 1/2.

all_reply_floors_exact.json 保存全部1905列（168正列）；4963条行、非负列及O归一化均由 Fraction 重算，最小余量0。此是作者精确计算层结果；未有独立整图实现审查。它仅限制这个固定支撑的必要行图，没有完整目录 SPE 策略，不能作为主目标反例。

重放（不覆写证据）：

    python all_reply_actual_floors.py --check-old
    python all_reply_actual_floors.py --priced --optimum --verify
