---
id: customer-attraction/R105-zero-regret-repair-scripts-review-20261031
kind: review
type_tag: 审查
title: R105 零 regret 修复脚本三源接续审查
status: complete-source-read-integrated-script-boundaries
truth_status: exact-enumerator-and-finite-search-code; no Q-CAG-HALF claim
review_level: full-source-read-script-logic-and-output-scope
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-105f776c3e6d4a22bb7c380c5df8edc7/new_cross_branch/audit_zero_regret_repair.py
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-105f776c3e6d4a22bb7c380c5df8edc7/new_cross_branch/audit_zero_regret_repair.py
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-105f776c3e6d4a22bb7c380c5df8edc7/new_cross_branch/search_zero_repair.py
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-105f776c3e6d4a22bb7c380c5df8edc7/new_cross_branch/search_zero_repair.py
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-105f776c3e6d4a22bb7c380c5df8edc7/new_cross_branch/simplify_zero_repair.py
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-105f776c3e6d4a22bb7c380c5df8edc7/new_cross_branch/simplify_zero_repair.py
evidence_paths:
  - archives/customer-attraction/tools/evidence/R105-zero-regret-scripts-20261031/manifest.json
  - archives/customer-attraction/tools/evidence/R105-zero-regret-scripts-20261031/audit_zero_regret_repair.py
  - archives/customer-attraction/tools/evidence/R105-zero-regret-scripts-20261031/search_zero_repair.py
  - archives/customer-attraction/tools/evidence/R105-zero-regret-scripts-20261031/simplify_zero_repair.py
related_objects:
  - ../审查/R105零regret修复JSON完整枚举接续审查--审查.md
  - ../审查/R105跨枝候选与实际根有限探针接续审查--审查.md
  - ../问题--问题.md

# R105 零 regret 修复脚本三源接续审查

三份脚本分别负责：对 18 客户 witness 做无 canonical solver 的完整策略枚举；随机探索实际 regret-only 修复候选；以及用 MILP 将已找到 witness 缩到小整数输入。它们都明确不搜索或证明 Q-CAG-HALF。

## 1. audit_zero_regret_repair.py

脚本逐单位展开 witness JSON 的客户类型，用 Fraction 计算尾部效用和覆盖；all_spe 枚举每个末位动作表与每个首位动作，逐节点检查最佳回应。旧/删后两人游戏都各有 4^5=1024 策略；脚本断言原 SPE 唯一 (2,[2,2,1,2])、删后唯一 (3,[2,3,1,1])、两个实际 regret 为 0、旧福利17、删后福利16、删后OPT17。它还分类空背景三人根的四个子游戏并断言唯一根终局 [1,3,2]，防止把背景主题误当实际根动作。

## 2. search_zero_repair.py

脚本只测试一个明确的 actual-regret-only 修复候选。随机生成四主题客户重数，计算两人/三人终局表、旧策略和删后可行菜单；可选 actual-root 模式要求删除主题成为空背景三人 SPE 的实际根，并在 50000 次试验中报告 found=false。代码注释明确：有限搜索结果不是证明，只有在独立精确证书后才可保存。该结果与 actual_root_probe JSON 的 seed/trials 字段一致。

## 3. simplify_zero_repair.py

脚本读取固定旧/新策略，建立全部逐客户激励和福利不等式行，用 scipy MILP 最小化非负整数客户重数。输出仅用于将候选缩为 18 客户 witness，并写明 purpose 为反驳 actual-regret-only welfare repair，不是 Q-CAG-HALF 反例。MILP 解的最小性不是数学必须；最终结论由 independent audit 脚本和完整 JSON 枚举提供。

## 4. 状态与边界

三脚本的独有内容是“如何生成/审计/缩小 witness”的复现逻辑；其数学结论已由 JSON 完整枚举和 Markdown 证明接续。随机搜索的 found=false 仅是候选特异负证据；MILP 只找到一组整数输入，不证明全局最小性。三源不提供一般 half 证明、实际根单删反例或任意人数结论。

本批原件、脚本和 manifest 已保全；哈希、字节、控制字符和 git diff --check 均通过。未执行 Git commit、push 或 clean done。
