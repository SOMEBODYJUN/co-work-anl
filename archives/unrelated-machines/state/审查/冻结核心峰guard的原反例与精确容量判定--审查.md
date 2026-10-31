---
id: unrelated-machines/composition-review-frozen-core-guard-and-exact-capacity-contract
kind: review
type_tag: 审查
title: 冻结核心峰guard的原反例与精确容量判定
math_scope: fixed-real-core-plus-common-size-residual-assignment
status: corrected-exact-restricted-flow-contract; historical-code-not-production-backend
summary: 补组合review后加fatal修复，guard覆盖孤立冻结机器；完整数学候选搜索与tiny布尔程序/1200递归边界不互冒。
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/reviews/unrelated_machines/composition_decoder_obstruction_review.md
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/reviews/unrelated_machines/composition_decoder_obstruction_review.md
---

# 冻结核心峰guard的原反例与精确容量判定

## 本页身份和原fatal

本页只处理组合review末段的冻结核心遗漏，不把它并入需求树组合、prefix law或两实际见证。36行主源全部读，另全文读现行[共同尺寸算法](../算法/冻结核心共同尺寸的未知阈值搜索--算法.md)及[审查/实现边界](共同容量修复的判定与实现边界--审查.md)。本来错误属于判定证明/代码，非改输入域或重定义最优值。

已冻结真实核心负载f_i≥0，新任务每件在资格E_j上用共同q>0，目标

$$B^*=\min_{\tau(j)\in E_j}\max_i(f_i+q|\tau^{-1}(i)|).$$

旧实现先令容量max(0,floor((B−f_i)/q))就判满流。取f=(2,0)、一件q1新任务只可机2、B1，容量(0,1)满流返回True，但真实完整最优值2。删除过载核心机器也不能消除其真实负载。原root实际运行过这个程序反例，本批不冒称新run。

## guard后的双向判定与未知阈值

先查每E_j非空，再**对所有机器**拒B<max f，包括孤立无任务机器。通过后令c_i=min(n,floor((B−f_i)/q))≥0，建任务容量1、资格边容量1、机器汇容量c_i的网络。真实峰≤B调度给整数满流；满流给每任务一个资格端并有f_i+q计数≤B，故双向精确。截n不变可行性，不按巨大容量展开槽。

每实际峰属于S={f_i+qt:全部i,0≤t≤n}。排序去重，在单调满流谓词上二分首成功值；最大候选max f+qn对每机容量≥n，有资格端便可行，因此首值恰B*，保流回溯实际分配。候选≤m(n+1)，O(log(m(n+1)+1))为**流调用数**，排序/每次流/回溯另付多项式。候选及floor交叉比较按f,q输入位长收费，不遍历数值时间或q倒数。

空新任务返回全部冻结峰max f；q0直接任取资格端、不除q。含任务资格组件若各有自己的q_C、机器侧不交，可独立做并取所有B_C*及所有孤立f_i最大；多尺寸若共享机器则不能分离成此单计数网络。

## 真实先验、版本与实现限度

fee_cascade_review只据修复Exact先独立重构guard必要、整数容量/真实计数等价、候选含t0与孤立/空残余；再读修前正文/脚本，修后/孤立机两句另实际核。root加guard及反例/空任务回归并逐候选与原矩阵oracle比，未改旧来源字节。组合review当前403e9a81b578859deaa0da55029adce8ce1a1ba1f6f34b76ed8c0ddbcb5b17da不同于历史读后bd3b3d52d9796f74c57e00b524820a9bc97443b248e31694e4b3eba1f69b6dc9；本批简单去尾guard也未复原后者，**不声称取得或全读未知旧字节**。

修后tiny脚本只有feasible谓词、brute oracle和小例，没有未知阈值完整二分器/实际分配后端。前置BFS不更新匹配，仅查每任务有正容量端；后递归DFS才增广。合法长链m=n1200、f0、q=B1，任务j=0..1198资格{j,j+1}、最后任务资格{0}，真实可行τ(1199)=0、τ(j)=j+1；历史固定Python栈下递归谓词RecursionError已实际确认。这限制代码规模，不反驳迭代最大流的数学位多项式算法。

独立scratch扩大实验与root小例/后来归档driver分身份；未取得的扩大harness/JSON不伪称本批复跑。此接口只在给定核心、共同尺寸/资格后精确修复，不选择一般核心、不提取一般矩阵结构，也不提供一般FAIL⇒OPT>T或统一次二算法。[原件/读域/关系](../../../../tools/evidence/um-foundation-composition-configuration-reviews/README.md)。
