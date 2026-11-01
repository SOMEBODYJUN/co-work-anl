---
source_id: d9e2deb241f3440413f7
kind: cleanup-review
title: two-player collision-free LP best point (finite exact endpoint)
status: finite-exact-certificate-candidate
source_sha256: 8470454396d1ae7e138a08c7b01451c648bcc58c7ea7230693f9af91d329958e
---

# d9e2deb241f3440413f7: `two_player_collision_free_best.json`

## 来源与冻结指纹

* 冻结路径：`research/workspaces/customer-attraction/R-51ca8c2b36184c41818099bc490374ca/construction/two_player_collision_free_best.json`。
* source id：`d9e2deb241f3440413f7`；blob `2378aeff7356bf9a63b873a283bda81494cc0376`；343 bytes；SHA-256 `8470454396d1ae7e138a08c7b01451c648bcc58c7ea7230693f9af91d329958e`。
* `legacy-cleanup` commit `68fad804ec5946cb296f77dc5b336308a66abf12` 与 `main` commit `aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c` 的同路径字节完全相同，均为上述哈希。
* 原始 JSON 已逐字段读入本批 `source.json`；未将 LP 浮点输出误称为 JSON 内的证明证书。

## 冻结内容的精确解码

原文字段为：

```json
{
  "topics": ["A", "B", "C", "D"],
  "replies": [1, 0, 3, 0],
  "actual": [2, 3],
  "comparison": [0, 3],
  "ratio": "5/4",
  "types": [[1, "1/4"], [7, "1/2"], [8, "1/4"], [10, "1/4"]]
}
```

主题位掩码按 A=0、B=1、C=2、D=3 解读。`replies[a]` 是首行动 a 后的第二位回复；所以 A→B、B→A、C→D、D→A，实际路径是 C→D。`comparison=[0,3]` 是 A、D。`types` 是非负客户质量（不是已经整数化的客户数）：

| mask | 客户兴趣 | 质量 |
|---:|---|---:|
| 1 | A | 1/4 |
| 7 | A,B,C | 1/2 |
| 8 | D | 1/4 |
| 10 | B,D | 1/4 |

掩码集合排除了同时含 C、D 的客户，故实际 C、D 不碰撞。实际覆盖质量
\(W=|C\cup D|=1/2+(1/4+1/4)=1\)。比较 A、D 覆盖全部质量 \(1/4+1/2+1/4+1/4=5/4\)，所以记录的 `ratio=5/4` 正确。总质量是 5/4，因为比较覆盖允许超过实际覆盖。

把所有质量乘以 4 得到合法单位客户实例：一名 A 客户、两名 A,B,C 客户、一名 D 客户、一名 B,D 客户。此时实际 C→D 的 \(W=4\)，比较 A,D 的覆盖为 5，仍为 5/4。该缩放正好是既有端点构造中 \(X\) 的两名客户、A-only、B∩D、D-only 的五客户版本。

## 相关程序及有限检查

直接生成 JSON 的 `two_player_collision_free.py`（source id `0d96e50335c33022effb`，SHA-256 `c7390c9a74878e92cd3dd7e41589310761118c5a4823e035f2b745e54a5d8842`）枚举四主题回复表并固定 `replies[2]=3`；客户掩码只取非空且不同时含 C、D 的 11 类。对每个回复表，它加入每个首行动 a、每个第二行动 b 的真实末位最佳回复行
\(U(\mathrm{reply}[a],a)-U(b,a)\ge0\)，以及根行动 C 相对每个 a 的行
\(U(C,D)-U(a,\mathrm{reply}[a])\ge0\)。对每个二主题比较对，用浮点 `scipy.optimize.linprog` 在 \(W=1\)、客户质量非负的锥上最大化比较覆盖。`replies[2]=3` 后有 \(4^3\times\binom42=384\) 个 LP；原 stdout 报 `LPs 384 best 1.25`，先遇到 6/5 点，随后该记录的 A,D 点达到 5/4。浮点 LP 只负责发现点。

逐点 exact reconstruction 在生成器内把权重用 `Fraction(...).limit_denominator(100000)` 重建，并用全部上述行断言；没有保存 LP 对偶，所以这不是对所有实例或所有策略的上界证明。对本 JSON 的独立有理复算得到：所有 16 个 continuation 行和 4 个 root 行非负，最小 slack 为 0，\(W=1\)、\(O=5/4\)；乘以 4 后所有客户质量为整数，因而是可直接逐动作核验的有限完整两人 SPE 证据。

同目录的必要回复松弛程序/报告 `two_player_collision_free_bound.py`/`.json`（source ids `23c59afb9f2a6498f7c7`/`a8d42614cbe6ed3610f9`）独立给出 ratio 5/4、乘子
`root_T1=3/4`、`actual_last_T2=1/4`、`actual_last_R1=3/4`、`actual_last_R2=1/4`、`BR_R1_T2=3/4`、`BR_R2_T1=1/4`，最小 residual 0；它是必要真实回复 relaxation 的 LP 对偶发现，不是本 JSON 的证明。

`audit_two_player_overlap.py`/`.json`（source ids `514a5475422ce77ab849`/`8790d2f2ec1c1e3501f0`）不用 LP，逐一检查 64 个会员位、两个端点及笛卡尔积；报告端点 p=1,q=0 为 \(W=4,I=0,OPT=5\)，并核验 \(8OPT=10W+2I\)。`audit_background_two_player.py`/`.json`（source ids `33a7ad7c1c761c51c319`/`a688a554b33bce8def2f`）在 9 个背景值、每值 64 位共 576 行检查背景恒等式与非负余项。父审 `audit_overlap_sensitive_suffix.py`/`.json`（source ids `73156991c19992692b88`/`e683f8facb5bd5a29287`）独立核验 512 个 membership/background 组合及 p,q=0…4 端点，报告 rational overlap denominator ≤10；这些检查支持既有解析端点，但不把有限枚举升级为一般量词。

## 与已归档对象的比较

已读同目录 `two_player_overlap_refinement.md`（`4157a234ca8cf21dc537`）的完整解析证书：对任意共同目录、完整两人纯 SPE，\(8OPT_2\le10W+2I\)，实际无碰撞时给 5/4；并给无碰撞五客户端点和笛卡尔积锐性。`background_two_player_refinement.md`（`410387249f58e966c0db`）把结论扩展到任意整数背景的末两人剩余利润，但明确不能沿前缀相加为一般 half。两稿及后续归档对象 `archives/customer-attraction/state/定理/末两人新生重叠的顺序利润税界--定理.md` 已承载一般符号证明和五客户端点；本 JSON 的独有信息是 LP 发现的四主题掩码、回复表、分数权重和 4 倍整数化清单。

已读 `parent_review/path_tail_review.md`：其 Hamming/尾树构造在早期离轨节点失效，主 Q-CAG-HALF 仍 OPEN，与本两人端点无冲突。已读 `global/README.md` 与 `uniform_portfolio_induction_boundary.md`：它们只把两人结果作为已知接口，并明确 m≥3 的 uniform-portfolio 推广未证；没有把本 JSON 当成多人结论。`independent/probe_background.py` 及两个 `background_*_nonmonotone.json` 是有限非单调性探针，不能改变本条两人证据的量词。

## 判断与处置建议

分类为**有限 exact SPE 端点证据（候选发现的有理化结果）**：缩放后可证明这个五客户、四主题、两玩家实例达到 `OPT/W=5/4`，但 JSON 本身没有一般不等式证明，也没有覆盖任意目录/人数/背景。`ratio=5/4` 是该实例的比较覆盖比，不是 Q-CAG-HALF 的反例（它大于 1 而不是证明低于 1/2），也不是 m≥3 结论。

建议保留 `source.json` 作为原始有限证据，并将其独有数据并入既有“末两人新生重叠的顺序利润税界”定理的端点/证据说明；无需新建一般定理。若需重跑，先将生成器复制到隔离目录（避免覆盖冻结 JSON），执行：

```bash
python3 two_player_collision_free.py
python3 two_player_collision_free_bound.py
python3 audit_two_player_overlap.py
python3 audit_background_two_player.py
```

前一程序需要 NumPy/SciPy；后三个审计只用 Python 标准库。独立缩放后的 16 个末位和 4 个根比较可用 Fraction 逐动作复算；任何把 LP 最优值、有限会员表或背景末两人界外推到一般六人 half 的做法均应拒绝。

