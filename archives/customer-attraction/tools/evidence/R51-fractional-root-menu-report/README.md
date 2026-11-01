# R51分数根菜单831B报告的原始证据与独立字段核验

主源ID `ffb62fe84028190eeb5c`，完整路径
`research/workspaces/customer-attraction/R-51ca8c2b36184c41818099bc490374ca/security/fractional_root_menu_audit.json`。
831B，SHA-256为`619560f7f2c91aad9ee82c911d8f9589468a161424c9685b8379e59100faad9c`，两冻结提交`68fad804ec5946cb296f77dc5b336308a66abf12`与`aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c`内容相同。主源用`work.py clean show`全文读完16字段，随后由同一reader导出[原报告](original/fractional_root_menu_audit.json)。

[读域与原件清单](reading-manifest.json)逐项列完整路径、来源提交、字节和SHA。本子任务不claim/done其它比较源，也不冒称读完整个R51工作区。

## 实际原样运行

全文读配套`1864478e226928da29a3`（3033B）及`2b1766f3d4198f0abba8`（2397B）边界稿，保[原程序](original/audit_fractional_root_menu.py)和[原边界稿](original/fractional_root_menu_boundary.md)。程序只用标准库和固定有限循环；没有导入规范模型、原整数菜单审计或SPE求解器。main会写脚本旁报告，故将源码原样复制到`replay/`隔离执行，原件不变：

```sh
PYTHONDONTWRITEBYTECODE=1 python3 archives/customer-attraction/tools/evidence/R51-fractional-root-menu-report/replay/audit_fractional_root_menu.py
```

本次exit0，stderr为空，stdout和生成JSON均831B，与冻结报告逐字段及逐字节相同：

- [真实stdout](replay/original-entry.stdout.json)
- [原入口生成报告](replay/fractional_root_menu_audit.json)
- [真实运行状态、Python版本、耗时与字节比较](replay/execution-state.json)

当前代码可精确生成该报告，不证明历史调用命令。Boss导入调用`audit()`与配套程序负责人另做原CLI，都是同源复核；不将重复执行当作两个独立数学实现。源码专门审查见[配套审查页](../../../state/审查/R51分数根菜单审计器--审查.md)。

## 独立输入、完整策略和16字段

另全文读且按冻结SHA核保存：

- `c838c11dfaa7a54dcca8`，1846B [18类型原输入](original/aggregate_theta_input.json)。
- `b312212275551b29955a`，4339B [43节点原完整策略](original/aggregate_theta_strategy.json)。

二者与当前既有36客户菜单/聚合例的输入、策略同一。独立核验器先核策略恰覆盖全部43个有序决策历史，再按该完整动作表实际滚动全部偏离。它不调用原审计器、不导入规范模型/solver；收益采用另一份输入的18类重数精确求和，不复用原程序的combinations建客户列表。

```sh
PYTHONDONTWRITEBYTECODE=1 python3 archives/customer-attraction/tools/evidence/R51-fractional-root-menu-report/verify_report_independent.py
```

[独立核验器](verify_report_independent.py)完整验证16字段；[结果](replay/independent-field-audit.json)保所有重建字段、216个有序终局的守恒核对、43历史258比较、126正差/132零差/最小正差2、真实尾菜单、分数数组及跨组对/四主题贡献。另存[全部258行IC](replay/independent-ic-table.json)，每行保历史、行动、规定叶、真正偏离叶和精确差。43项为self，215项为改变行动；不能把258都称严格偏离。这里只认证这份给定完整纯SPE，没有枚举全部SPE策略。

`fractional_menu_minmax=161/15`在原代码中是返回字面值；原代码实际只核中点六个值及每单位客户二阶导分子非负，没有连续优化器。本次核每类型的仿射分母端点正性、二阶导分子和组交换保持客户表。全参数最优性来自凸性加交换对称的解析证明，承接[既有引理](../../../state/引理/真实根菜单标签支持的分数化精确停界--引理.md)，不把检查中点说成证明全区间。

独立核验还给当前实例整数静态安全值$v_3=10$的有限双边证书：均匀查询面对全部36个整数二槽背景的最低值为10；对偶均匀取六个同组不同标签对，每查询值为10。这与分数背景先平均负载的333/35、受限两尾分数最优161/15、整数真实尾菜单11严格区分。

## 实读相关文本与状态校正

除上述五原件，全文读了R51 security README（`ed8311f754fff3363215`）与`extra_mass_interface.md`（`7236f1b2778753536f65`）；没有运行其它浮点探针或把其扫描条数混入这份831B报告。

当前正式正文全文比较：

- 共同目录完整历史模型。
- 真实根菜单标签支持的分数化精确停界：已经解析证明本例连续最优性，当时明确未读原程序/JSON；本报告补实际程序证据，不重造引理。
- 自适应后继与真实菜单安全值障碍：同36客户输入的整数两尾菜单11、真正$v_3=10$与全历史SPE。
- 三人聚合末位保底反例：同策略$W34,OPT36,\theta_3=12$，不同被否定命题。
- 笛卡尔银行逐人分数门槛反族、笛卡尔银行完整根菜单反例：后续一般FF-LEADER在$m\ge3$、extra-one在$m\ge4$失败，不能沿用原scope的旧OPEN，也不能把银行值倒填本36客户例。

`scope`原字符串完整保留，字段校验只核它与冻结文字相同，不将历史开放状态当数学程序的输出证明。36例所有六标签各1/3的自由背景实际已给333/35<10；本例不反驳自由逐人桥的一般性，后续银行族另外反驳。真正整数聚合和half也未由本报告否定；$W34\ge3v_3=30$、$2W68>OPT36$。

当前工作树按文件名、161/15、333/35、根菜单/FF-LEADER等检索，冻结inventory按R51及原aggregate输入/策略定位；实际读域由清单限定。正式[计算正文](../../../state/计算/R51分数根菜单有限审计--计算.md)保全部16字段语义、连续证明与有限程序的分界、实际复现及后续范围。

没有新游戏、搜索、LP/连续优化、世界新颖性或外审认证。关系理由在计算正文末尾，三级超图留第三阶段；本子任务未commit/push/checkpoint/clean done/新claim，等待父Boss保存。
