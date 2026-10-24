# credible round5：全 fresh 广播与真实后继信用

2026-10-24。只研究一般 Q-CAG-HALF；目标仍 OPEN。root 汇总提交；本目录未作 git/work 操作。

- `all_fresh_submarkov_elimination.md`：任意完整历史 SPE 上的全 fresh 利润归一化路由。证明全子集 sub-Markov 界、严格角色 DAG 消元及 C-only exact 余账；全客户版给 past-C actual coupon 出口、同 context 同客户的正负取消和谱系因果区间。末尾只备注可选真实 off-history slack clipping。全部 R/outside 广播不新增利润质量；actual coupon 及重复实际钱包尚未支付。状态：解析草稿，待独立审查。
- `audit_submarkov_elimination.py` / `submarkov_elimination_regression_v2.json`：作者自核，只重放两个已有完整 SPE 证书，核 IC、sub-Markov 子集界、真实后继与 past coupon 域及精确消元。不搜索实例，不核一般 cap1。OPT-owner 初始化未激活正传播边；另用引理所准许的单位利润注入，核 root_tax 旧证书上一条非零 all-customer 边。没有正 fresh 边可作该回归，明确不称已测非零 fresh 链。初版输出 `submarkov_elimination_regression.json` 保留不覆盖。
- 下一步：把 C-only 余账与同一 actual I/G、gamma 和 source 钱包耦合；或证明别的真正全局预算。不得把消元本身提升为一般 half 或旧 K_in 收缩。
