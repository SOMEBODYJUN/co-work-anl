---
batch: R-2fc-background-induction-20261031
kind: evidence
status: captured
sources:
  - id: 9d4c2a56314808399f98
    path: research/workspaces/customer-attraction/R-2fc8878b4bdd4328bbc1bcf1df8ca831/background_induction/artificial_background_probe.py
    sha256: 9765d276e0a2441a754c7f10426be48da79ddb6b938c83fe510eb1d142d3a2d5
  - id: 000d50d7154ab9d643e7
    path: research/workspaces/customer-attraction/R-2fc8878b4bdd4328bbc1bcf1df8ca831/background_induction/two_player_fresh_certificate.py
    sha256: ce97b69091244b64c745a88b52f4e70a1b07d1778b262d9a286e2f7fac6bcfa4
---

# R-2fc background induction 运行证据

本目录保存 Boss2 认领的两份源码的完整正文副本、实读尝试、运行 stdout/stderr、时间边界和机器可核对清单。源码副本的 SHA-256 与 `cleanup/inventory.jsonl` 冻结元数据一致。

## 原文读取

对每个 source ID 都实际调用了：

```sh
python3 co-work-anl/tools/cleanup.py --repo co-work-anl show 9d4c2a56314808399f98 --out .../source/artificial_background_probe.clean-show.py
python3 co-work-anl/tools/cleanup.py --repo co-work-anl show 000d50d7154ab9d643e7 --out .../source/two_player_fresh_certificate.clean-show.py
```

`clean show` 需要从 Git promisor remote 拉取冻结 blob；当前环境到 `browser-proxy port 8889` 不可达，因此两次均返回退出码 1。原始 stderr/stdout 保存在 `clean_show_attempts.txt`。之后在同一冻结提交的公开 raw 页面逐字节读取两个正文并保存至 `source/`，两份哈希分别匹配 `9765d276…d3a2d5` 与 `ce97b690…6bcfa4`。因此这里保留了实际源码和失败边界，没有把网络读取失败伪装成 clean-show 成功。

## 运行记录

两个脚本都复制到独立运行目录后按默认参数执行，命令均受 `timeout 120s` 约束。完整机器记录在 `run-manifest.json`，包括 Python/NumPy/SciPy 版本、UTC 开始/结束时刻、秒数、退出码、stdout/stderr 哈希及预期 JSON 是否生成。

| source | 默认入口 | 结果 | 实耗时 | 退出码 | 生成 JSON |
|---|---|---|---:|---:|---|
| `9d4c2a56314808399f98` | `python3 artificial_background_probe.py` | 200 次人工背景随机试验无负候选；stdout 最后一行 `completed 200 no negative candidate`；stderr 空 | 10.552999 s | 0 | 否（未命中 `FOUND`） |
| `000d50d7154ab9d643e7` | `python3 two_player_fresh_certificate.py` | HiGHS 报 `The problem is infeasible`；源码在失败分支 `return`，故 shell 仍为 0；stderr 空 | 0.772910 s | 0 | 否（LP 不可行，未进入 JSON 写入段） |

`run/artificial/stdout.txt`、`run/artificial/stderr.txt`、`run/artificial/status.txt` 与 `run/two_player/*` 是未经修改的原始输出。不存在的 `artificial_background_candidate.json` 和 `two_player_fresh_certificate.json` 在清单中明确标为 `present: false`；没有凭据、token 或外部秘密写入证据。

## 数学身份和禁止升级

`artificial_background_probe.py` 使用 `q=6`、剩余两人，把每个 `(mask,b)`（`b∈{0,1,2,5}`）独立当作客户类型，因而是人工扩大背景模型。它没有共同目录和过去有序主题来产生负载 `b`，也没有全量合法 CAG SPE 量词；200 次固定 seed 的阴性只能是有限实验。

`two_player_fresh_certificate.py` 只在 64 个二值 incidence pattern 上建立 192 行（fresh、`p=1`、仿射斜率）的 17-slack 非负系数 LP，目标是为特定的两根/三组末回复模板寻找统一 `P+Delta >= fresh_OPT_2` 证书。LP infeasible 只说明这份预先选定模板没有非负解；它既不是合法 CAG 反例，也不是所有两人证明结构都不可能，更不是六人 half 结论。

与已归档的 23/488 客户合法背景首步反例相比，本批没有新增合法客户实例或完整策略树。那些反例只否定单步余额，整体余额仍正；后续 52 客户根路径反例另行处理。六人 `2W >= OPT_6` 仍需原模型下对所有目录、客户和完整纯 SPE 的证明，不能由本批两个程序升级或改写。
