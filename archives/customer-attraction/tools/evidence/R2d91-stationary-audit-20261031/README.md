# R-2d91 relay/security stationary audit evidence

本证据包处理本批三个已领取源版本：一个明确废弃且不可执行的 relay 草稿，以及一份 stationary fractional security JSON 与其独立 `Fraction` 检查脚本。三源均完整读取；废弃草稿按保留/不执行处置，两个 security 源在隔离目录实际重放。

## 源哈希

| clean id | source | bytes | SHA-256 | 处置 |
|---|---|---:|---|---|
| `2e32e9a7403ca9c6a26e` | `relay/abandoned_probe_uncovered_budget.py` | 4611 | `346cc864013934ae21ca1585d36682b4cc2195f6307765938b49ae99c5c2e64b` | 原文标明 ABANDONED；不执行 |
| `a14a025eaabac25f48df` | `security/audit_stationary_extra_fractional.json` | 1050 | `dfabbae544977de0513427fe029718dd54398f8e30fbf15355bfc92c67886cd6` | 完整字段读取，和生成 JSON 逐字节相同 |
| `b59d80ac2b02969bd86e` | `security/audit_stationary_extra_fractional.py` | 4622 | `97cd6a52e771603531d61dab179ee58ad690a57a4912e95c40f097045e45bd23` | 独立有理数重放，exit 0 |

## 实际重放

`audit_stationary_extra_fractional.py --output generated.json` 返回码为 0，标准错误为空，`generated.json` 与冻结 JSON `cmp` 相同。独立 `verify_stationary_audit.py` 返回 `PASS`。

冻结 security 结果为：1274 个单位客户，43 个有序历史，258 项含自身比较；实际终局 `(0,3,4)`，利润 `(541/2,613/2,269)`，福利 846，最优覆盖 1032；指定平稳分布 `(1/4,1/4,0,1/4,1/4,0)` 下查询 2 相对根的差 `1149/910`，均匀分数背景上限 `441/2`，固定两槽整数背景上限 `252`。这是指定 stationary `r`-mass fractional root cap 的有限反例，不能外推自由 extra-one、aggregate safety 或六人 half。

relay 草稿的首行和入口明确写着 `ABANDONED AND NOT RUN`，并在 `__main__` 以 `SystemExit` 拒绝执行；它所针对的 `W >= OPT_m(N \ actual_union)` 已被既有 71 客户完整 SPE（`W=35`、缺失 36）否定。本批保留原字节和不执行理由，不把未运行程序当作实验。

## 与既有正文的关系

stationary JSON/脚本的数学内容并入既有《真实尾平稳均值的额外查询封顶》对象；本批闭合该对象此前“原 audit blob 缺失”的历史本地证据缺口。废弃 relay 源的独有内容已并入《自然捕获的共同配对最优价与固定尾重置》资源，保留其未执行和已失效的状态。对象仍明确：stationary 失败只针对固定核和指定分数背景，relay 草稿不构成任何新结论。
