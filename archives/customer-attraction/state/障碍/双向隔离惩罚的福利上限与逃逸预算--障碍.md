---
id: "customer-attraction/reciprocal-isolation-welfare-and-escape-budget"
kind: "obstruction"
type_tag: "障碍"
title: "双向隔离惩罚的福利上限与逃逸预算"
status: "proved-conditional-architecture-bound; escape-budget-unpaid"
summary: "任意k双向真实隔离惩罚的锐上限、正整数等号和撤销隔离后的E必要阈值，含重复追随者末位冲突；不约束所有SPE。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d22a706a03c5499d941a6a97f94128a8/CLAIMS.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-d22a706a03c5499d941a6a97f94128a8/CLAIMS.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d22a706a03c5499d941a6a97f94128a8/FAILED_ROUTES.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-d22a706a03c5499d941a6a97f94128a8/FAILED_ROUTES.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d22a706a03c5499d941a6a97f94128a8/README.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-d22a706a03c5499d941a6a97f94128a8/README.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d22a706a03c5499d941a6a97f94128a8/RESEARCH_STATE.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-d22a706a03c5499d941a6a97f94128a8/RESEARCH_STATE.md"
---

# 双向隔离惩罚的福利上限与逃逸预算

## 假设及真正结论

固定k≥1，m=k+1，单位客户全集恰为两两不交D及X_i,Y_i之并。有限共同目录含C_i=X_i、A_i=X_i∪Y_i、B_i⊆X_i∪Y_i∪D及D，也可含N的任意其他子集。给定一份**完整有序历史纯SPE**，实际路径C_1,…,C_k,D。

每个实际i前缀保留过去C_j。改A_i后的同一策略真实分支末位B_i，改B_i后的真实分支末位A_i；两枝中间所有主题均避开X_i∪Y_i∪D，彼此其他动作可不同。其他离轨历史不作额外限制。这是条件性架构，不是每个SPE必有的结构。

记x_i=|X_i|,y_i=|Y_i|,d=|D|,S=Σx_i,Y=Σy_i。则
\[
2(k+1)OPT_{k+1}\le(3k+2)W,\qquad W=S+d.
\]
W>0才取比值OPT/W≤(3k+2)/(2k+2)；零实例不除零。

## 三条真实比较与锐性

令v_i=|B_i∩(X_i∪Y_i)|/2+|B_i∩D|。在A_i分支末位的B_i，以及B_i分支早期偏离者本人，局部均只同A_i分摊，D部分独占，故完整收益同为v_i。旧C_j避开局部池、中间避开条件均承重；没有改写过去。

A_i分支末位可改D取得d，给v_i≥d；实际第i位可改B_i得v_i，给x_i≥v_i。实际末位D可改A_i得x_i/2+y_i，给d≥x_i/2+y_i。因此
\[
x_i\ge v_i\ge d\ge x_i/2+y_i,\quad S\ge kd,\quad Y\le kd-S/2.
\]
k个A_i加D恰k+1槽覆盖N，故OPT=S+Y+d≤S/2+(k+1)d。代入
\[
(3k+2)(S+d)-2(k+1)[S/2+(k+1)d]=(2k+1)(S-kd)\ge0
\]
即证。额外目录不改变全集上界与满覆盖见证。d=0时迫所有x_i=y_i=0。k1无需无固定点置换，界5/4。正等号强制每个x_i=d、y_i=d/2，因此单位客户d必须正偶数。既有全人数无拥挤族x_i=d=2,y_i=1实现；其**存在**和全历史Q/B递归来自[无拥挤族资源](../资源/无拥挤完整均衡族原稿与有限探索的准确范围--资源.md)，不能仅凭本页必要条件造完整策略或宣称该比率约束所有SPE。

## 撤销隔离后的可量化缺口

仍保同一无拥挤实际路径及全客户池，取消两枝中间避开。假设改A_i后的真实末位B_i；令v_i是该末位收益，b_i是实际i改B_i后的本人最终收益，d_i^Q是A_i枝末位改D的收益。定义
\[
\Delta_i=v_i-b_i,\quad T_i=d-d_i^Q,\quad E=\sum_i(\Delta_i+T_i).
\]
T_i≥0，Δ_i可负。由x_i≥b_i、v_i≥d_i^Q，得S≥kd−E。实际末位仍给Y≤kd−S/2，故同代数给
\[
2(k+1)OPT\le(3k+2)W+(2k+1)E.
\]
这是待支付缺额，未证由W统一控制。若真有OPT>2W，上界OPT≤S/2+(k+1)d先迫S<2(k−1)d/3，结合S≥kd−E得
\[
E>(k+2)d/3.
\]
必要但非充分；小局部不对称不足。多个后继拥挤B_i、跨组主题、A_i枝提前覆盖D都是可能逃逸机制，各须重新完整验证。

## 相同追随者方案的具体冲突

本段是另一个具体重复尾方案，不套用前节m=k+1的比率界。固定r≥1、D=Z⊔R，局部核心X_i∪Y_i与D不交；除已指定的实际C_i、偏离A_i及下面列出的尾行动外，其余行动均不覆盖X_i∪Y_i∪R。

设局部核心a=|X_i|+|Y_i|>0，B_i=X_i∪Y_i∪Z，实际末端为r次同D；拟在A_i枝用r次B_i稀释。实际末位从D改B_i，公共Z份额相同，所以D最佳要求|R|/r≥|X_i|/2+|Y_i|≥a/2。拟惩罚分支末位B_i可改尚未覆盖R的D，其最佳要求a/(r+1)≥|R|。合并r(r+1)≤2；r≥2不可能，r1还迫Y_i为空。只算早期a/(r+1)会漏末位改D。拆Z或异质奖励须另证，不被这里概括排除。

## 原件与审查身份

实际全文读bdd683848aab07c77142、73e78b9e31ec4e9518da、4fa30e438229f7d5436d，精确原件在[related清单](../../../../tools/evidence/d22-frontier-ledger-primary/related-source-manifest.json)。原独审先盲重构再核对非均匀等号/零边界，这是内部解析审查历史，不新增当前外审。全部k量词由上面解析承担，0随机或枚举新run。下一对象必须保真实分支收益、D被预覆盖量及总E，而不是给必要条件点就称half反例。
