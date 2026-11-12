# Boss1 对 Q_D 与私有树参数障碍 ALL 边的独立3D复核

复核当前 `b5-qd-and-private-tree-config-force-decoder-parameter-growth`、三个当前对象登记和单核 repair 收据。实读目标定理全文、flat CONFIG/FSLP 主定理全文、私有树正文的有界重数 v3 整节（含证明与边界），以及 Santa/UM 值桥的“精确模型”至“规模、规范化与明确的限制”。这里调用 v3 已证的有限存在性；没有新开外部论文或把原作者外部阅读、LP、程序运行记成本次动作。

## 源下界必须属于完整 flat 实例

Q_D 有一 main 组和 D² 个 helpers，D≥2。main 第 a 态含 D 个各值 1/D 的 g_(a,j)；相应 helper 只能选自己的 g_(a,j) 或共享 A_a 的 unit singleton。正值不交分配中，main 若在一行取两份 g，就迫两个 helpers 同占 A_a。因此 main 至多获 1/D；选一份 g、对应 helper 选 A_a、其余 helpers 选自己的 g 达到 1/D。

把每组 selector 放选中 state 的独立 private，领取的正 incidence 外送资源端，其余所有原 incidence（包括未选 states）留各自 private。所选 private 负载为 2−value，未选 private 为一，资源最多一枚 unit，得到完整 OPT_D≤2−1/D。反向 C<2 使每资源独占；每组 selector 所在 state 必须导出至少 2−C 的质量，恢复全组不交分配，故 C≥2−1/D；C≥2 分支平凡。源是 flat 全组值 V，不能换成 gated 的部分组平衡 β*。

完整 CONFIG(1) 的共同 λ 取 main 各态 1/D、helper home/parking 为 1−1/D、1/D。每 g 容量一，每 A_a 容量 D·(1/D)=1。private 以 λ 放 selector、以 1−λ 放完整 incidence，资源 singleton 权 λ，每原 job 恰覆盖一。Q_D 的 incidence 均正；当前共享审查对一般零 incidence 的补句不改变这份族的任何数值。源的其它 SC 正规化并未用于下界方向。

## 目标上界的参数和全任务语义

目标是 v3 的显式完全私有满 d 叉高 h 树，d,h≥1；父端小时间严格为 1/d，内部与叶子下端为 unit，叶外机唯一，所有 state 原作业存在，内部机不共享。μ 是每完整 state 叶逆像的最大重数，跨 state 总共享不受此 μ 约束。

CONFIG(1) 代入 v3 得 a=d。令 r=ceil(d/(μ+2))。因 d 为整数且 r−1<d/(μ+2)，

\[
d\ge(\mu+2)(r-1)+1,
\quad d-\mu(r-1)\ge2r-1\ge1.
\]

对整数 h≥1，凸性给 (2r−1)^h+1≥2r^h。因此 v3 的两个精确 blocker 前件成立。该证明在同一 full-state λ 的实际叶 multiplicity 容量上比较逆像叶数，不额外除 μ，也不把 raw 子树直接当 rainbow。

已证 rainbow/Haxell 选择给每 root 的真实 state 和 r 子树。活跃内部机一枚 incoming unit 加 d−r 枚 1/d small，负载 2−r/d；非活跃原内部机全父置负载一。所有未选 state、零 λ state、未选枝任务都回填，资源全局不交使每外机最多一 unit。由此确有目标完整调度 C′≤2−r/d<2。分母是原 d，辅助 a-tree 不是修改物理输入；只使用有限存在性，不声称变参数位多项式构造。

## 必要条件与解码的精确量词

目标定理假设：每一份目标低峰 C<2 的完整调度，都存在峰不增的源完整调度。将这项合同用于上述已存在的 C′，得到

\[
2-1/D=\operatorname{OPT}_D\le C'\le2-r/d,
\quad Dr\le d.
\]

r≥1 给 d≥D；r≥d/(μ+2) 给 μ≥D−2。少任一源的完整实际下界或上界，就不能完成这次比较，因此原单条 ALL 必须保留。

若仅给 μ≤μ0，v3 可用较松 μ0 重复推导 D ceil(d/(μ0+2))≤d。D>μ0+2 时矛盾；D=μ0+2 时 D ceil(d/D)≤d 等价 D|d。这些只为必要条件。固定 d≤d0 也排除 D>d0；没有给参数边界的实现或锐性。

CONFIG(1) 已确保目标 OPT′<2，有限显式实例的完整合法调度集合有限且非空，故最优达到。低峰解码作用于目标最优调度给 OPT_D≤OPT′；反向若此标量不等式成立，对每一份目标低峰调度取同一份源最优调度即可。这个反向只是存在性，无须输入未知 OPT 给算法。不能由这种存在性等价宣称存在有效编译或多项式解码器。

原边 accepted / unconditional / whole 正确：已证两源无条件证明“若 CONFIG1 和解码合同，则必要参数增长”这一整条定理；解码是目标定理内部前件，而不是被隐去的开放证明前提。固定 μ 或 d 的该结构路线被切断，一般 UM、不同结构、有损解码和不保 CONFIG1 的路线没有被排除。N 的 binary selector/port 正规化有额外 selectors 与不同处理时间，不能从图是二叉就套本定理 d=2。

精确当前 pins、已读文件 SHA 与单核任务收据另存 refs；此次无新边、无源改动或科学运行。
