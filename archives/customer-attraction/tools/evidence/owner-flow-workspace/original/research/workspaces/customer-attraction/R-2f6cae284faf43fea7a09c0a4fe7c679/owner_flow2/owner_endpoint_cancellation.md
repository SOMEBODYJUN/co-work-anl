# 固定最优前缀链中的 owner 端点与 signed 债务严格抵消

2026-10-24，Boss21/owner_flow2。以下仅保存 parent 通知的既有发现，并从 TREE-F 独立重构。它是全输入精确恒等式，不是新的付款，也不声称发现归属或新颖性。Q-CAG-HALF 仍 OPEN。

固定同一完整历史纯 SPE、同一最优有序元组 T，以及真实叶

    Z^i=finish_sigma(T_1,...,T_i), i=0,...,m.

Z^0 是实际叶，Z^m=T。任意全局固定合法 owner Q 给同一 F_Q、ell_Q、e_Q。置

    Gamma_i=u_i(Z^{i-1})-u_i(Z^i)>=0,
    D_i^Q=F_Q((Z^i)^{-i})-F_Q((Z^{i-1})^{-i}),
    J_Q=sum_i[D_i^Q+e_i^Q(Z^{i-1})-e_i^Q(Z^i)].

每一步 UNIT 展开完整原 IC 给

    F_Q(Z^i)-F_Q(Z^{i-1})
      =D_i^Q+e_i^Q(Z^{i-1})-e_i^Q(Z^i)-Gamma_i.

望远镜且 F_Q(T)=OPT，得到

    F_Q(Z^0)+J_Q=OPT+sum_i Gamma_i.             (INVARIANT)

右边不依 owner。因此两个固定合法 owner Q,Q' 总有

    J_Q'-J_Q= -[F_Q'(Z^0)-F_Q(Z^0)].

把 J 的负项先截去、仅保留正去槽债，或把 query error 的上界代入其负号，都会破坏这项精确抵消。沿同一链只优化实际 F_Q 端点，不能产生一般 half 的新付款。

owner 自由若要有实际作用，应改变一份真实合法共同容量构造，例如本目录 [actual 净券列的 owner-switch](owner_coupon_joint_capacity.md)；那里的 Delta K 总和也为零，只改变实际角色之间的需求分配。此区别不表示已证明后一构造可平衡。

原 TREE-F 来源是 R-cd789330fc7141299ac491bbb3ffa420/round3/GENERAL_PROOF_WORKING.md §4；任意 owner 前缀误差来源是 ../random_portfolio/arbitrary_owner_prefix_budget.md。所有 profile 仍是原 sigma 的真实完成叶，没有冻结后继或压缩有序历史。
