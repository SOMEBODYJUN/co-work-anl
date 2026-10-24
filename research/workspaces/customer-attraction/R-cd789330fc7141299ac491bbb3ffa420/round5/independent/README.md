# round5 / independent 恢复点

目标始终为一般 `Q-CAG-HALF`；当前 OPEN，无主定理证明或目标反例。

- `two_block_security_reduction.md`：两位 block 候选 PB-strong / PB-extra，后者若普遍成立则一般 half 的完整充分归约；真实阈值加强 TH 只作充分义务，不与 PB 等同；最小人数坏点的真实后继配对输入及目前跨枝支付缺口。
- `attack_two_block.py` 与三个 `two_block_*attack.json`：只针对强 PB 的固定完整策略锥定向攻击。500 份四人六主题与 200 份五人六主题未分离，仅有限阴性；不再扩大同类数量。
- `attack_two_block_full_history.py`、`two_block_full_history_attack.json`：另 50 份允许不同有序历史独立平局的完整策略锥，未分离。不是全输入正面证据。
- `two_block_dual_diagnostic.json`：一份浮点对偶机制诊断；没有精确证书身份。静态背景仅用实际主题但 IC 跨全部深度，尚无一般构造。
- `review_broadcast.md`：全fresh/全客户广播表示组件的独立解析审查；核心 LOSS、合法域、DAG 消元、COUPON-LOAD 通过，明确尚无共同容量或half。两处范围措辞已通知作者。
- `broadcast_blind_reconstruction.md`：阅读作者稿之前依root消息写出的盲重构；`broadcast_author_snapshot.md`冻结本次所读作者稿。
- `audit_broadcast.py`、`audit_broadcast.json`：独立22单位客户完整SPE审计，确实触发非零fresh边及terminal past-C出口；43历史258含自身IC，精确通过质量及coupon账。它只核该例实现，不作一般计算证据。

接续应解析 PB-extra 真实两位总信用；不要重启阴性扫描，不要把 TH 的加强失败（若找到）自动当 PB 失败。第二位复制根只有同枝等利；现成八标签菜单参数点 a=1,b=9 表明，根菜单排序、尾 floor、末位全 BR 与复制根信用仍必须加上第二位其他真实跨主题 IC。root 统一保存；本分支未读凭据、未作 git mutation 或 work.py start/send。
