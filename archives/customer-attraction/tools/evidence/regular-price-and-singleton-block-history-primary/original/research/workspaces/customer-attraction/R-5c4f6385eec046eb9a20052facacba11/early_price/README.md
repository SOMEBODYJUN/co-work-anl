# 早期玩家价格预算：本轮研究备份

对象为一般 Q-CAG-HALF 的早期候选 B(u_i)<=W 或 OPT_m-W<=m u_i；两者一般情形
仍 OPEN，没有在本目录里证明或反驳。

- [解析稿](symmetric_singleton_price.md)：关联度正则目录的完整价格一维公式；
  逐关联度充分判据；主题块充分对称且某玩家单占一个主题块时，无须SPE已有
  B(u_i)<=W-u_i。完整参数证明和作者自审已写，待根代理安排独立审查。
- [独立定义级脚本](audit_symmetric_singleton.py)和[输出](symmetric_singleton_audit.json)：
  从兴趣mask直接构造轨道、枚举带重复终局，以Fraction核对公式；有限实现审计
  不代替无限参数证明。
- [最初探索程序](two_group_orbits.py)：组内/组间对称、第二人反组、后续fresh跟随
  第二组的完整策略锥；所有重复历史以组负载分拆列出。输出
  [k=m](two_group_orbits.json)、[k=2m](two_group_orbits_2.json)只是浮点LP探索记录。
  解析单占块定理已说明整个根玩家攻击方向为何不能给正分离；不追加同类阴性样本。

只修改本目录；未执行git、work.py、公屏或外发。下一步是独立审查解析稿，随后
用关联度正则精确价格接口在更一般全Gamma锥中攻击，或打破单占块/对称条件。
