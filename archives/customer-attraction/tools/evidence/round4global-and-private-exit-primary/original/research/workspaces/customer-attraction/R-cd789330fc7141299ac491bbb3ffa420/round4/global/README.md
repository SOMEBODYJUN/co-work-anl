# 第四轮：直接一般半覆盖与独立审查

2026-10-23。主目标Q-CAG-HALF仍OPEN；复用同clone/actor。全部新工作只面向任意人数、任意有限共同目录、全部有序历史纯SPE，不继续固定ghost恒等式、受限正面类或策略锥扩样。

- [MIN-PI独立审查](review_min_pi.md)：按root指定审查其已冻结单个证书；15748单位客户、43完整历史、258比较及P0至P4全部计数独立精确复算通过。MIN-PI被否定；half/EI未被该例否定。没有运行发现优化器。
- [独立审计代码](audit_min_pi_independent.py)与 `min_pi_independent_audit.json`：只读取客户bitmask重数及完整策略，明确展开单位客户，不导入SPE oracle、规范verifier或发现脚本。
- [direct floor与私有花瓣归约](direct_floor_and_exit_working.md)：原总m的逐人FLOOR仍OPEN。已证fresh-petal归纳，以及从任意floor反例构造同m私有花瓣反例的全输入正规形；root独立重构范围一致。剩余是PARTICIPATE?，不把它当half反例正规形。`diagnose_direct_floor.py` / `direct_floor_diagnostic.json`仅记录一个旧完整锥、一个合法prefix的有限诊断，无反例不构成证明。

一般主线在 [direct_query_cover_working.md](direct_query_cover_working.md)：每个实际位置只选一份合法query混合，允许同一query同时覆盖所有剩余遗漏库存，再用G单位自由取消。它的逐客可行性(COVER?)、全价格分离式(PRICE?)及更弱均匀总量(ROW-MASS?)均未证明。若任一所需充分式闭合，整行原IC直接给half；它不以NET或WP为前提。

当前多行动合流的割价格还不是某合法主题的未加权收益，尚无从坏割抽出真实可盈利偏离的一般关系。原策略也不能免费移到被价格重加权的客户实例。本轮没有新支付突破，不把充分归约、凸对偶、等价改写或有限阴性计为证明进展。旧五人模板十bits投影在对象语义处停止，未运行发现优化器或扩编译任务。
