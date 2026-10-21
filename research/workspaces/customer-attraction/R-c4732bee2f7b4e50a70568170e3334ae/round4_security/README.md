# Round 4 安全值研究

主目标 `Q-CAG-HALF` 与真正聚合安全值桥仍 OPEN。

- `iid_closure.md`：既有八客户静态CCE间隙立即否定强iid福利桥的逻辑闭包；
  同实例精确iid最优cap和任意混合共同边际iid排除；区分不同边际独立竞争者。
- `audit_iid_closure.py`、`iid_closure_audit.json`：从8个单位客户独立重建84项
  完整有序历史比较、真安全鞍点和`Q(sqrt(669))`精确iid计算。
- `weak_iid_counterexample.md`：新的弱iid桥反例；m>=2,K>=2的完整解析SPE政策，
  每个m=K>=53的显式严格证书，m53的159单位客户与m100的300单位客户有理回归，
  以及同族渐近失败机制。
- `audit_weak_iid.py`、`weak_iid_audit.json`：小参数完整树、300单位客户证人和
  精确有理切口审计；真正v_m<=2由合法固定静态背景支付，原half未被反驳。

下一义务：一般真正安全值桥尚缺全局支付；强/弱全局iid桥均已被排除。
不得把新状态修正称为新实例，或把共同边际iid失败扩张成任意独立背景失败。
