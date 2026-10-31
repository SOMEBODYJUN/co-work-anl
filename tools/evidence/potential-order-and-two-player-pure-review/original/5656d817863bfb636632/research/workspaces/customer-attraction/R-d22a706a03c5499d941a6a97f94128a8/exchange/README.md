# Boss10：最优覆盖交换与客户级预算

本目录是 Q-CAG-HALF 的个人研究备份；只使用有限单位客户、共同主题目录、全部有序历史纯 SPE。
主目标仍 OPEN。

## 已完成

- `unique_optimum_omission_obstruction.md`：71 客户、2 人、6 主题的完整 SPE；实际 W=35，唯一最优主题集合 {T,Q} 覆盖 38，却遗漏实际覆盖外 36 客户。否定“存在某个最优组合，其遗漏数不超过 W”的直接支付，也否定最大化实际交集的最优组合修补。不是 half 反例。
- `audit_unique_optimum_omission.py`：不依赖求解器或规范 SPE 实现，展开 71 位单位客户并用 Fraction 核验全部 42 个节点行动比较、21 个无序主题对和连续价格解析界。
- `unique_optimum_omission_audit.json`：上述审计的冻结输出。
- `full_menu_potential_rise_obstruction.md`：24客户完整三人SPE反驳 `K_ab>u_root=>Phi(Z(a))>Phi(Z(b))`，同时反驳“每个势最大列都是blocker”；仍存在好的势最大列，未否定纯列存在或混合完整终局菜单。791来源例另给严格Φ下降。
- `audit_phi_rise_obstruction.py` / `phi_rise_24_exact.json` / `phi_rise_exact.json`：直接展开24或791单位客户，精确重算57节点399比较；root分别独立核验通过，正文已链接。

## 当前状态与下一步

本团队已按定义完整核验。父研究者已按原始类型和规则独立展开，不读取本审计代码；其独立审计见 `../parent/audit_optimal_omission.py` 与 `../parent/optimal_omission_independent_audit.json`。后来确认同一71客户证书已在 Boss5 公屏107出现，本目录准确身份为 Boss10 独立重现，不声明新增或新颖性。尚无外审认证。
唯一最优遗漏支付失败不影响 OPT−W<=m u_i 一类保留完整最优覆盖的动态预算。
继续攻一般真实跨分支机制及允许局部欠债的整体支付。当前精确候选为 ownpay 混合完整根终局菜单：存在Q使每查询a都有 Σ_b Q_b(K_ab−d_b)≤0。该候选比根阈值菜单强，仍开放。

## 已停止的探索与未提升材料

`probe_integral_price.py` 与 `integral_price_probe_m3.json` 只是有限完整策略锥阴性探索，不证明一般价格预算；已停止扩特殊人数样本。
`phi_rise_candidate.json` 保留791例发现检查点。
`phi_rise_small_candidate.json` 是停止优化前已返回的24客户浮点候选；现已由root及本目录分别完成完整规则精确核验，主正文使用其精确证书，不声明整数最小。
