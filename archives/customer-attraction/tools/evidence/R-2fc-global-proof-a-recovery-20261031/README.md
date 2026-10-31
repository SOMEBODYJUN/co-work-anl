# R-2fc global_proof A：六个 blob 恢复与候选复核

本包恢复了先前因 partial clone promisor 缺失而暂记 `needs-decision` 的六个 `global_proof` 源，并在同一批中读取、登记了其所依赖的 `truncated_potential_candidate.json`。七个源均由 `Boss2` 先认领后读取；每次 `clean show` 返回 0，原始 stdout/stderr 保存在 `clean-show/`，源字节及库存 SHA/大小保存在 `source/` 与 `source-manifest.json`。

## 逐源处置

| ID | 文件 | 处置 | 实际工作 |
|---|---|---|---|
| `484d7024f388657d79d9` | `audit_collision_free_family.py` | integrated | 逐行读取 Q/B/fallback 递归、全历史偏离检查；`py_compile`，独立副本运行 `k=1,2,3`。|
| `2c9581cd1e1a35237ff2` | `audit_collision_free_obstruction.py` | integrated | 逐行读取五客户无碰撞障碍和 `Fraction` 比较；独立副本运行通过。|
| `da6d610ba50965200a82` | `audit_truncated_potential.py` | integrated | 逐行读取权重整数化、完整有序历史和普通/截断势计算；以恢复的固定候选运行精确审计。|
| `1121e1bd7ded184bd117` | `collision_free_family_audit.json` | integrated | 全文读取；与 family 脚本独立重放 JSON 逐字节相同。|
| `e5a0724f34d98235f952` | `collision_free_ratio_best.json` | retained | 全文读取固定 `q=6,r=3` 浮点候选；只作为探针发现记录，不作定理。|
| `181f33c049afe9962dba` | `collision_free_ratio_probe.py` | retained | 全文读取随机 LP、负载筛选和容差；`--trials 3 --seed 29393` smoke run 退出 0。|
| `631f2695cbf46ff1c2a2` | `truncated_potential_candidate.json` | retained | 全文读取 `q=6,r=3,trial=86,seed=29395` 候选；作为固定输入供精确脚本审计。|

## 精确复现结果

- 碰撞自由 Q/B 族：`k=1,2,3` 分别得到 `(W,OPT)=(4,5),(6,8),(8,11)`，比率 `5/4,4/3,11/8`；所有记录的逐历史 slack 非负，最小 slack 为 0。它是有限端点复现与存在型族证据，不是所有 SPE 的结论。
- 五客户障碍：`W=4, OPT=5, Phi=4`，5 个历史、20 项比较（15 项非自身），二层占用 4。它否定按实际占用直接支配最优覆盖的桥，但 `2W=8>5`。
- 恢复候选的 Fraction 审计：78 个整数单位客户，实际路径 `(1,5,5)`，`W=54, OPT=75, Phi=截断Phi=141/2`，258 项比较、最小 slack 0。`Phi-OPT=-9/2` 仅说明该固定候选不支持势桥；`2W=108>75`，不是 half 反例。
- `collision_free_ratio_best.json` 的 `objective=1.116279069767442` 是浮点 LP 发现值；小规模 smoke run 没有改善点。它与精确 Q/B 审计分层保存，不能外推为无拥挤族上界。

`run/validation.json` 为 `passed=true`，并核对源 SHA/大小、四个脚本编译、family 逐字节重放、五客户精确数值、固定候选精确数值、浮点 smoke 输出和 `2W>OPT` 边界。没有从这七个源推出六人、任意人数、所有纯 SPE 的一般 half 结论。
