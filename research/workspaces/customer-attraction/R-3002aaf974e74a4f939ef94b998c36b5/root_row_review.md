# 最大根再查询证书：父方原行阅读与第二实现核验

对象为 `research_4/ROOT_REQUERY_ZH.md`、其中三条新保存局部行及一个旧三复制图新方向支撑。结论：以下准确范围的内部复核通过；没有六人 half 闭合、外审或新颖性结论。

## 真实策略语义

对任意原模型六人完整历史纯 SPE，r 是原实际根利润；在原根强制选最大主题 T 后得到 P0，原根 IC 给 r≥vT。P0 首位被强制，不被当作该枝的最优者。P0 第二/三/四位的复制 E 分支各在同一原有序源处分叉；QI 回源 `(T)` 选择 P1 真末主题 I，QL 回源 `(T,A)` 选择 P2 真末主题 L，QD 则在 P1 的源 `(T,E)` 选择 P0 合法主题 D。源 IC 使用各自真实源收益，所有后继沿同一原策略；未冻结后继或跨源识别利润。

逐一核对证书的 `copy_edges`、共同前缀与 `first_genuine`：强制位置之后才使用原枝安全 IC；所有 LAST 使用真正末位，PAIR 使用真正末两人。安全分母 b+6−i 是包括当前者的最大未来负载，因此是合法偏离收益下界。CAP 只用共同目录最大主题大小 K。

LAST 来自六最优主题的末位查询。PAIR 所用原两人税为 `research/current/customer_attraction/two_remaining_tax.md` (1)：任意两个比较主题的剩余利润≤实际末两人利润加实际倒二主题税。对十五个比较索引对求和，每个最优客户挑一个覆盖索引，其五对至少给5/(b+1)，故 O≤3H+Σb/(b+1)。最优并集外的税只使右侧增大，不删除其信用。没有导入五人背景定理。

所有图标签允许相同。将真实会员嵌入独立位立方体只扩大逐客户核验域，不限制任意历史依赖平局，也不要求每个位型可同时由 SPE 实现。任意大整数单位客户重数由逐客户非负求和覆盖。全零不需除 K 或 W。

## 第二实现实际覆盖

父方另写 `audit_root_rows.py`，只读证书数据与旧抬升点，不导入作者程序、发现器或 LP。根据字面路径、源边与权值直接重建容量、真 IC、安全、LAST、PAIR 的整数系数；分母以60清除。预先核验累计绝对值上界小于2^63，所有符号检查用整数。结果及每份输入 SHA-256 在 `root_row_audit.json`。

实际检查：旧三复制方向32768型，QI 524288型，QL与QD各262144型。四者最小残差均为0，唯一零型均为全零会员。父方从权值独立算得 a、β 与作者表一致。证明的求和恒等式、真源范围及量词已逐式阅读；这一记录是内部数学与实现复核，不是外审。

复跑命令（从仓库根；四个输入依次列出）：

```sh
python research/workspaces/customer-attraction/R-3002aaf974e74a4f939ef94b998c36b5/audit_root_rows.py research/workspaces/customer-attraction/R-3002aaf974e74a4f939ef94b998c36b5/research_4/root_requery_baseline_o4.2_exact.json research/workspaces/customer-attraction/R-3002aaf974e74a4f939ef94b998c36b5/research_4/root_requery_o4.2_exact.json research/workspaces/customer-attraction/R-3002aaf974e74a4f939ef94b998c36b5/research_4/root_requery_third_L_o4.2_exact.json research/workspaces/customer-attraction/R-3002aaf974e74a4f939ef94b998c36b5/research_4/root_requery_branch_D_o4.2_exact.json --output /workspace/scratch/ca750226330e/root_row_audit_replay.json
```

## 对旧点的作用与仍缺义务

父方从旧3889关系点的实际会员直方图重算r，并核其总实际利润等于保存的W；K与O直接取该旧点。四条已保存根行的该点余量均为严格负有理数，见核验JSON。这只排除该指定点，不排除原3889行加新根行的全部共同可行点，更不是原游戏反例。

尤其旧三复制图只重新选择方向就已切掉该点。因此“切旧点”不能全归为新回复身份，也未证明新查询图相对旧完整行锥有严格能力增益：作者报告的浮点最优差还缺旧锥的精确原始证书。可靠增量是明确的新局部行、其完整域有理证明及共同主系统可直接使用的新支撑；下一步需要重选整体主乘子或精确构造加行后的共同点。
