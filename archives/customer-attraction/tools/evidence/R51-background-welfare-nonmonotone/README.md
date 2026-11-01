# R51固定两名未来者的背景总福利非单调证据

正式对象：[R51背景福利非单调证书](../../../state/反例/R51背景福利非单调证书--反例.md)。主源 `786e0b678d81d2d39f1e` 为1040字节JSON，固定同一13客户四主题目录、余两人，比较背景 \(e_0\to2e_0\)，总人数相应3→4；最坏总覆盖13→12。

- `original/` 和 `manifest.json`：九份通过 `work.py clean show ID --out PATH` 导出的冻结原字节及逐文件SHA-256；四个规范包文件仅服务原probe重放。
- `verify_independent.py` / `independent-replay.json`：不导入规范包，展开13名单位客户，直接穷尽完整两人尾策略候选空间并按定义比较。旧背景恰1份完整SPE，新背景恰2份。输出保全部末位收益、完整策略、首位真实比较、终局计数及总支付恒等式。
- `replay_probe_fixed.py` / `probe-fixed-replay.json`：在固定原JSON上调用原 `check`；没有调用随机 `run` 或 `minimize`。与独立结果及原最小福利/计数对一致。
- `replay_probe_discovery.py` / `probe-discovery-replay.json`：另一次当前重放默认 `run()` 和 `minimize()`。默认seed102首trial0先得22客户22→20，贪心减重结果逐JSON值等于主源；原历史命令仍未知。
- 每份新入口的 `.event.json` / `.stderr.txt`：实际命令、Python版本、耗时、退出码、stdout哈希和真实stderr。三入口均exit0、stderr空。

可从仓库根目录依次运行：

```sh
python3 archives/customer-attraction/tools/evidence/R51-background-welfare-nonmonotone/verify_independent.py
python3 archives/customer-attraction/tools/evidence/R51-background-welfare-nonmonotone/replay_probe_fixed.py
python3 archives/customer-attraction/tools/evidence/R51-background-welfare-nonmonotone/replay_probe_discovery.py
```

这不是完整三人/四人根策略树枚举，也没有认证指定非空背景的根SPE到达性。总覆盖与未来玩家利润和分开；相邻 `background_nonmonotone.json` 是另一份利润证书。两背景本身均满足half，不能据此声称六人或一般half反例。
