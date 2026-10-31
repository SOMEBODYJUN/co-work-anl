# 归一化XOS最小菜单规模：作者 Proof v2 实际 read-after

审查者：general_query_response_review。2026-10-18。

读取顺序：先只据Exact独立证明并冻结；root全文读后才授权本轮首次全文读取作者v2 Proof。未读旧v1作者Proof、其它review；本文件冻结前尚未读取canonical。旧独立字节保持不改，未修改repo/Git/Work。

冻结对象SHA-256：

- Exact：`6208afa100822520502e368c1cf3814d6d5bd520e3fdaec363efc33961eb2d3d`
- 独立Exact-first：`8cf66cfa4c3845080d3323053bedb07d87922f42b03f8094c2c30931d8a6cc5c`
- 作者Proof：`fcc28dbc9e726f6b5b2ba403943a6a0fe99b4ecf136898174965a54657bd3d7c`

**明确结论：作者Proof v2有效，与独立推导一致，无fatal。**

## 逐项核对

1. 非负norm1使每clause正support非空；d0得k1。d≥1先排除support≤d，再用最重d项质量≥d/h与low条件推h≥ceil(d/η)。此处为非严格≥，允许d/η整数时h恰k，未破坏锐端点。
2. 全部t-subset的unit条件是有限max实际达到1，norm1与非负使该clause整个正support包含于T。任取其中k项uniform后仍覆盖原被覆盖的T；任何tiny B新值≤d/k≤η。无用大support clauses也可转换。作者没有误称新f在每B都≤旧f，而只保证两个合同条件。
3. Menu→k-family大小≤K及反向uniform实现均完整，Θ方向是每个t集包含某个指定k集。重复indexed clauses和重复F不会减少最小数；没有假设usual covering-design的反方向。
4. 每k-set覆盖的t-sets数是C(2t−k,t−k)，union counting给一般ratio下界；重叠只减有效覆盖，未错误认定下界对所有参数可达。
5. d0恰是singletons hitting全部t-sets，complement至多t−1，最小t+1；t1时正确为2。ηt正整数时k=t，每个T只能由T自身覆盖，所以必须全部中央二项式个；uniform clauses以d/t=η达到low的≤边界。固定有理η的分母倍数说明也正确。
6. d≥1时t−k=floor({ηt}/η)，余数严格<1给≤ceil(1/η)−1，包括1/η整数的精确减1。覆盖分母≤(2t)^c；central项≥4^t/(2t+1)给固定η的增长下界。
7. 全部t-subsets uniform 1/t给可行性，故K_min不是空约束量；一般精确值用Θ表示，不声称poly计算。已给完整菜单的uniform转换可poly，但其输入可能已指数大，不能偷换为从短additive source poly输出菜单。
8. 一玩家2t个1/t项的source可显式用O(t log(t+1))位列出，固定η下输出K超任意该长度固定次幂；未误称2^{Ω(source总位长)}。若η随输入变化，c不再常数；证明没有推广同一固定多项式分母。
9. 同U、逐玩家、非负norm1、finite explicit max及全部unit/tiny subsets是实质条件。额外资源/玩家、全局耦合、只保reachable bundles、unit completeness损失或implicit表示均没有被排除；没有来源hardness或一般UM结论。

Proof各节与冻结Exact的量词和边界一致，无需数学修正。未进行软件枚举，不把保存或有限实验等同证明/外审。

**冻结判断：Exact与作者Proof规模v2通过；下一步canonical审查另立记录并限定对应章节。**
