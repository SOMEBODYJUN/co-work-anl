# 五人推送分数候选快照证据

正式对象：[五人个体安全推送分数候选快照](../../../state/计算/五人个体安全推送分数候选快照--计算.md)。主源只有 `ed2276b6a2900e10abda`；下列相关来源用于语义比较与输入闭包，不代办其完成。

| 本目录文件 | 身份与SHA256 |
|---|---|
| `original.json` | 原1335字节JSON；`207bb54c38056a422191ffdc2ef0a134626b6d3a601cc075f035e2104a623f89` |
| `source-security-README.md` | R51原2281字节说明，源ed8311f754fff3363215；`efacb525fc904d5a92e0a7582c742dcbb504d9abebd79e95cd10b256d0e5b5a2` |
| `source-full-terminal-probe.py` | R51原2785字节完整终局探针，源8cfac6eb31c4cd8c7d99；`35bfea8b46cd34818f8a53ef7229c3afbf74a264c73481c1bd6f7f1384cda26c`；这是比较代码，非主JSON生成器，未执行 |
| `audit_snapshot.py` | 本轮新标准库实现，使用确定的冻结输入/动作函数；不是旧发现程序、优化器或第二份SPE选择器 |
| `current-exact-reconstruction.json` | 本轮新执行输出；内含Python版本、脚本SHA、三个实际输入路径/size/SHA和全部检查结果 |

三份原件均由 `WCG_ACTOR=Boss7 python3 work.py --save repository-cleanup clean show ID --out 路径`取得，冻结来源为 `68fad804ec5946cb296f77dc5b336308a66abf12`与`aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c`下的原路径。主JSON及两个R51原件的路径前缀均为 `research/workspaces/customer-attraction/R-51ca8c2b36184c41818099bc490374ca/security/`；原文件名分别为 `pushforward_fractional_candidate_five_individual_security_0.json`、`README.md`、`full_terminal_push_probe.py`。

已在正式证据目录保全的必需依赖直接按原字节复用，不另复制1.3MiB同一策略：

- [原4405字节游戏](../security-chain-boundary/original/examples/customer_attraction/five_individual_security.json)，源29621c1ecaeeaf2b18f3，SHA `689cae34e0cbed60583710cd8e40a06b558cde59ddd566b2cb89e06ab5e8700f`。
- [原1319525字节完整证书](../security-chain-boundary/original/evidence/certificates/customer_attraction/five_individual_security.json)，源1ba3cfe5c71248cd5770，SHA `372bea6caf743792be542c411e9bcb961b6af6d31dc89d76e6a903e609be990f`。
- 已全文比较同处 [原Fraction审计](../security-chain-boundary/original/tests/audits/customer_attraction_five_individual_security.py)及[原报告](../security-chain-boundary/original/evidence/runs/2026-10-10/five_individual_security_independent.json)，不重放该旧86客户审计，也不借其PASS认证新weight。

本次执行：

```sh
python3 archives/customer-attraction/tools/evidence/pushforward-fractional-five-snapshot/audit_snapshot.py --output archives/customer-attraction/tools/evidence/pushforward-fractional-five-snapshot/current-exact-reconstruction.json
```

最终执行exit0、stdout/stderr空。程序拒绝禁用assert的Python `-O`。开发时初稿曾有一处未闭括号，执行即SyntaxError，未产生成功结果；修复后完成核验，再加入版本/脚本SHA与assert防护并重新执行，所交报告对应最终脚本。当前运行不是冻结发现器重放；冻结搜索未定位该发现器。

真实检查范围：完整读三输入、验证SHA、逐项核29类型和11111动作完整域；分别在字面十进制权重及明确382整数客户/73恢复权重下计算全部111110含自身IC；重建十个根真分支；重现原浮点删根gap并对比完整五槽；将保存p精确归一后核恢复点正差；核p4=p9=1/2时全部十查询；核全目录均匀质量4/5背景；枚举2002个五槽无序带重复主题组合求恢复点OPT。未执行随机搜索、LP/SLSQP、全p优化、所有SPE枚举或自由分数最优值求解。

字面小数p和为1−10⁻¹⁸，旧动作函数在字面权重下有17253项极小负IC；新的显式有理恢复则全部IC通过。两者身份不能合并。八标签受限连续最优223/219来自正式正文凸对称证明，不是程序对连续域的有限枚举。自由均匀cap1525/1533仅为足够的上界，未冒充自由精确最优值。
